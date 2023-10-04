import json
import os
import requests
import subprocess
from typing import List

def get_release_tags() -> List[str]:
    tags_env = os.environ['TAGS']
    if tags_env == '':
        print("ERROR: TAGS environment variable is not set.")
        exit(1)

    tags = json.loads(tags_env)
    if len(tags) == 0:
        print("ERROR: TAGS is empty")
        exit(1)

    releases = []
    github_release_url = "https://api.github.com/repos/lavanet/lava/releases"

    response = requests.get(github_release_url)
    releases_json = response.json()

    for release in releases_json:
        if release['tag_name'] in tags and release['draft'] == False and release['prerelease'] == False:
            releases.append(release['tag_name'])

        if len(releases) == len(tags):
            break

    return releases

def main():
    releases = get_release_tags()
    latest_release = releases[0]

    # build versions
    for release in releases:
        build(release)

    # build latest
    build(latest_release, "latest")

def build(version_tag: str, docker_tag = None):
    if docker_tag is None:
        docker_tag = version_tag

   
    images = [["rpc", "lava-rpc"]]

    use_cache_env = os.environ.get('USE_CACHE')
    use_cache = use_cache_env != None and use_cache_env != 'false' and use_cache_env != '' and use_cache_env != '0'

    if use_cache:
        print("Using cache")

    for [dockerfile_path, image_name] in images:
        if image_exists_in_repo(image_name, docker_tag):
            print(f"Image {image_name}:{docker_tag} already exists in repository, skipping")
            continue
        else:
            print(f"Building: lava tag={version_tag}, docker image {image_name}:{docker_tag}")

        args = ["docker", "buildx", "build", ".", "-t", f"us-central1-docker.pkg.dev/lavanet-public/images/{image_name}:{docker_tag}", "--build-arg", f"TAG={version_tag}", "-f", "Dockerfile", "--push"]

        if use_cache:
            args = args + ["--cache-from", "type=local,src=/tmp/.buildx-cache", "--cache-to", "type=local,dest=/tmp/.buildx-cache-new"]

        exit_code = subprocess.Popen(args, cwd=f"dockerfiles/{dockerfile_path}").wait()

        if exit_code != 0:
            print(f"ERROR: Failed to build {image_name}")
            exit(1)

def image_exists_in_repo(image_name: str, tag: str) -> bool:
    args = ["docker", "manifest", "inspect", f"us-central1-docker.pkg.dev/lavanet-public/images/{image_name}:{tag}"]

    exit_code = subprocess.Popen(args).wait()
    return exit_code == 0


if __name__ == '__main__':
    main()

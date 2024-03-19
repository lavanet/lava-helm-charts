from sys import argv
import requests
import os
import subprocess
import json

registry_domain = 'us-central1-docker.pkg.dev'
repository = 'lavanet-public/images'

def split_tag(tag):
    # split with 0 as default value
    tag = tag.replace('prerelease-v', 'v')
    tag_split = tag.split('.')
    tag_split = tag_split + [tag_split[0], "0", "0"]

    def safe_str_to_int(s, default=0):
        try:
            return int(s)
        except ValueError:
            return default

    tag_split = [safe_str_to_int(x) for x in tag_split]

    return (tag_split[0], tag_split[1], tag_split[2], tag_split[3])


def get_tags(type: str):
    if type not in ["lava-consumer", "lava-provider", "lavap"]:
        raise Exception(f'Unknown type {type}')

    url = f'https://{registry_domain}/v2/{repository}/{type}/tags/list'
    response = requests.get(url)

    if response.status_code == 200:
        tags = response.json().get('tags', [])
        tags = [tag for tag in tags if tag.startswith('v') or tag.startswith('prerelease-v')]

        tags.sort(key=lambda tag: split_tag(tag), reverse=True)

        return tags

    else:
        raise Exception(f'Error fetching tags: {response.content}')

def get_digest(tag, type: str):
    url = f'https://{registry_domain}/v2/{repository}/{type}/manifests/{tag}'
    headers = {
        'Accept': 'application/vnd.docker.distribution.manifest.v1+json, '
                  'application/vnd.oci.image.index.v1+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.headers.get('Docker-Content-Digest')
    else:
        raise Exception(f'Error fetching digest for tag {tag}: {response.content}')

def get_latest_target(type: str) -> str:
    result = subprocess.run(["./bin/lavad", "q", "protocol", "params", "--node", "https://public-rpc-testnet2.lavanet.xyz:443/rpc/", "--output", "--json"], capture_output=True, text=True)
    response = json.loads(result.stdout)

    if (type == "lava-consumer"):
        return response["params"]["version"]["consumer_target"]

    if (type == "lava-provider"):
        return response["params"]["version"]["provider_target"]

    if (type == "lavap"):
        return response["params"]["version"]["provider_target"]

    raise Exception(f'Unknown type {type}')


def find_latest_oci_tag(type: str):
    tags = get_tags(type)
    latest_digest = get_digest('latest', type)

    for tag in tags:
        if get_digest(tag, type) == latest_digest:
            return tag

    raise Exception(f'Could not find tag with digest {latest_digest}')

def main(type: str):
    common_tag: str = find_latest_oci_tag(type)
    latest_target: str = get_latest_target(type)

    common_tag = common_tag.replace("prerelease-v", "v")
    latest_target = latest_target.replace("prerelease-v", "v")

    if common_tag.strip().replace("v", "") == latest_target.strip().replace("v", ""):
        print(f"{type} latest is image is up to date");
    else:
        print("latest tag is incorrect, updating...")
        print(f"tagging {type} v{latest_target} as latest")

        exit_code = subprocess.Popen(["gcloud", "artifacts", "docker", "tags", "add", 
                        f"us-central1-docker.pkg.dev/lavanet-public/images/{type}:v{latest_target}", 
                        f"us-central1-docker.pkg.dev/lavanet-public/images/{type}:latest"
        ]).wait()

        # maybe it failed because the tag not moved from prerlease to release yet
        # but the chain is the source of truth so tag the prerlease as latest
        if exit_code != 0:
            exit_code = subprocess.Popen(["gcloud", "artifacts", "docker", "tags", "add", 
                            f"us-central1-docker.pkg.dev/lavanet-public/images/{type}:prerelease-v{latest_target}", 
                            f"us-central1-docker.pkg.dev/lavanet-public/images/{type}:latest"
        ]).wait()


        # if its still erroring out, then we have a problem
        if exit_code != 0:
            raise Exception(f'Error tagging latest: {exit_code}')


if __name__ == '__main__':
    if len(argv) != 2:
        print("Usage: python tag_latest.py <lava-consumer|lava-provider|lavap>")
        exit(1)
    
    main(argv[1])

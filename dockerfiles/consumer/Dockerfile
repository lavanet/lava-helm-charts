###############################################################################
################################## BUILDER ####################################
###############################################################################
FROM ubuntu as builder

RUN apt-get update && apt-get install -y curl git

ARG TAG

RUN [ -z "$TAG" ] && echo "TAG is required (ex: v0.24.0)" && exit 1 || true

WORKDIR app

# create bin directory
RUN mkdir -p /app/bin

# download lava binaries
RUN curl -L "https://github.com/lavanet/lava/releases/download/${TAG}/lavad-${TAG}-linux-amd64" > /app/bin/lavad && \
    chmod +x /app/bin/lavad  && \
    curl -L "https://github.com/lavanet/lava/releases/download/${TAG}/lavap-${TAG}-linux-amd64" > /app/bin/lavap && \
    chmod +x /app/bin/lavap && \
    curl -L "https://github.com/lavanet/lava/releases/download/${TAG}/lavavisor-${TAG}-linux-amd64" > /app/bin/lavavisor && \
    chmod +x /app/bin/lavavisor

###############################################################################
################################## RUNTIME ####################################
###############################################################################
FROM debian:stable-slim

WORKDIR app

RUN apt-get update && apt-get install -y ca-certificates

COPY --from=builder /app/bin/* /app/bin/

ENV PATH="/app/bin:${PATH}"

FROM alpine:latest
ARG TAG
ENV TAG=$TAG
RUN [ -z "$TAG" ] && echo "TAG is required (ex: v0.22.0)" && exit 1 || true

###############################################################################
################################## BUILDER ####################################
###############################################################################
FROM ubuntu as builder

RUN apt-get update && apt-get install -y curl git build-essential

ARG TAG
ENV TAG=$TAG
WORKDIR app

# download lavad binary
RUN curl -L "https://github.com/lavanet/lava/releases/download/${TAG}/lavad-${TAG}-linux-amd64" > /app/lavad
RUN chmod +x /app/lavad

# download genesis.json file
RUN curl -L https://github.com/lavanet/lava-config/raw/main/testnet-2/genesis_json/genesis.json > /app/genesis.json

###############################################################################
################################## RUNTIME ####################################
###############################################################################
FROM debian:stable-slim

WORKDIR app

COPY --from=builder /app/lavad /app/bin/lavad
COPY --from=builder /app/genesis.json /app/data/genesis.json

COPY run /app/bin/run
RUN chmod +x /app/bin/run

ENV PATH="/app/bin:${PATH}"

CMD ["run"]

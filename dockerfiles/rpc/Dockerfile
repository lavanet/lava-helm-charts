###############################################################################
################################## BUILDER ####################################
###############################################################################
FROM ubuntu as builder

RUN apt-get update && apt-get install -y curl git build-essential tar

ARG TAG
ARG COSMOVISOR_TAG="v1.5.0"

RUN [ -z "$TAG" ] && echo "TAG is required (ex: v0.22.0)" && exit 1 || true

WORKDIR app

# download lavad binary
RUN curl -L "https://github.com/lavanet/lava/releases/download/${TAG}/lavad-${TAG}-linux-amd64" > /app/lavad && \
    chmod +x /app/lavad

# download cosmovisor
RUN curl -L "https://github.com/cosmos/cosmos-sdk/releases/download/cosmovisor/${COSMOVISOR_TAG}/cosmovisor-${COSMOVISOR_TAG}-linux-amd64.tar.gz" > cosmovisor.tar.gz && \
    tar -xf "cosmovisor.tar.gz" -C /app && \
    chmod +x /app/cosmovisor

# download config and genesis.json files
RUN mkdir -p /app/config

RUN curl -L https://raw.githubusercontent.com/lavanet/lava-config/main/testnet-2/genesis_json/genesis.json > /app/config/genesis.json
RUN curl -L https://raw.githubusercontent.com/lavanet/lava-config/main/testnet-2/default_lavad_config_files/app.toml > /app/config/app.toml
RUN curl -L https://raw.githubusercontent.com/lavanet/lava-config/main/testnet-2/default_lavad_config_files/client.toml > /app/config/client.toml
RUN curl -L https://raw.githubusercontent.com/lavanet/lava-config/main/testnet-2/default_lavad_config_files/config.toml > /app/config/config.toml

###############################################################################
################################## RUNTIME ####################################
###############################################################################
FROM debian:stable-slim

WORKDIR app

COPY --from=builder /app/lavad /app/bin/lavad
COPY --from=builder /app/cosmovisor /app/bin/cosmovisor
COPY --from=builder /app/config/* /app/data/config/

COPY run /app/bin/run
RUN chmod +x /app/bin/run

ENV PATH="/app/bin:${PATH}"

CMD ["run"]

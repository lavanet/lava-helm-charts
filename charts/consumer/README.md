# Lava consumer Helm Chart

Running a lava consumer on Kubernetes is a 2 step process.

1. Run the consumer using the Helm chart
2. Create a staking transaction for the consumer

## 1. Run the consumer using the Helm chart

#### Helm Command

```bash
helm install myconsumer \
    oci://us-central1-docker.pkg.dev/lavanet-public/charts/lava-consumer \
    --values myvalues.yaml
```

#### Prerequisite

Before running the consumer we need to create a kubernetes secret with your account key (`lavad keys export ...`) and the password.
Please see the [secret.example.yaml](secret.example.yaml) file for an example.

#### Required Config

To run the Helm chart you need to consumer some `REQUIRED` values. Anything marked at required in the [values.yaml](values.yaml) file is required.

Please see [/examples/consumer/values.example.yaml](/examples/consumer/values.example.yaml) file for an example for what values you will need to provide.

Please see our [docs](https://docs.lavanet.xyz/consumer-setup) for more information on configuration.

The `configYaml` section in the [/examples/consumer/values.example.yaml](/examples/consumer/values.example.yaml) file has an example config for a consumer that works on `LAV1`

## 2. Create a staking transaction for the consumer

Once you deploy the consumer into kubernetes using the helm file, and the deployment is marked as ready and running by kubernetes you can stake your consumer.

```bash
lavad tx subscription buy [plan-name] [address] [flags]
```

_Check the output for the status of the staking operation. A successful operation will have a code **`0`**._

#### Geolocations

```javascript
USC = 1; // US-Center
EU = 2; // Europe
USE = 4; // US-East
USW = 8; // US-West
AF = 16; // Africa
AS = 32; // Asia
AU = 64; // (Australia, includes NZ)
GL = 65535; // Global
```

#### Flags Details

- **`--from`** - The account to be used for the consumer staking (e.g., **`my_account`**).
- **`--geolocation`** - Indicates the geographical location where the process is located (e.g., **`1`** for US or **`2`** for EU).
- **`--keyring-backend`** - A keyring-backend of your choosing (e.g., **`test`**).
- **`--chain-id`** - The chain_id of the network (e.g., **`lava-testnet-2`**).
- **`--gas`** - The gas limit for the transaction (e.g., **`"auto"`**).
- **`--gas-adjustment`** - The gas adjustment factor (e.g., **`"1.5"`**).
- **`--node`** - A RPC node for Lava (e.g., **`https://public-rpc-testnet2.lavanet.xyz:443/rpc/`**).

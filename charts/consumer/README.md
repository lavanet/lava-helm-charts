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

## TODO

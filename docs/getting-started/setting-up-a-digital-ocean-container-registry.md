# Setting up a Digital Ocean Container Registry (DOCR)

This section will show you how to create a DOCR registry using the `doctl` CLI.

From the command line run the following:

```shell
doctl registry create <YOUR_REGISTRY_NAME> --subscription-tier basic
```

!!! note
    Please replace the **`<YOUR_REGISTRY_NAME>`** placeholder with a valid name.
    You can have only `1` registry endpoint per `account` in `DOCR`. A `repository` in a `registry` refers to a collection of `container images` using tags.

## Configuring DOKS for Private Registries

From the command line run the following:

```shell
doctl registry kubernetes-manifest | kubectl apply -f -
```

This will configure your `DOKS` cluster to fetch images from your newly created `DOCR`.

This step can also be achieved via the DO cloud console. Please follow this [guide](https://docs.digitalocean.com/products/container-registry/how-to/use-registry-docker-kubernetes/#kubernetes-integration).

For more info on this topic please see this [Kubernetes Starter Kit DOCR Creation](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers/tree/main/02-setup-DOCR).

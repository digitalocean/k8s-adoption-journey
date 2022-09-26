## Introduction

In this section you will learn you how to create a [DigitalOcean Container Registry](https://docs.digitalocean.com/products/container-registry/) (**DOCR**) registry using `doctl`.

A docker container registry is required to store all [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app images used in this guide. For each microservice you need a separate repository in the registry. The microservices-demo app consists of **nine microservice**, hence a total of nine Docker repositories will be created in the registry.

Following command will create a `professional tier` Docker registry in the `nyc3` region, named `microservices-demo`:

```shell
doctl registry create microservices-demo \
    --subscription-tier professional \
    --region nyc3
```

!!! notes
    - The **professional tier** is required to store all docker images used in this guide which costs **20$/month**.
    - You can have **only one registry endpoint per account** in **DOCR**. A **repository** in a registry refers to a **collection of container images** using tags.

## Configuring DOKS for Private Registries

From the command line run the following:

```shell
doctl registry kubernetes-manifest | kubectl apply -f -
```

This will configure your DOKS cluster to fetch images from your newly created container registry.

This step can also be achieved via the DigitalOcean cloud console. Please follow this [guide](https://docs.digitalocean.com/products/container-registry/how-to/use-registry-docker-kubernetes/#kubernetes-integration).

For more info on this topic please see this [Kubernetes Starter Kit DOCR Creation](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers/tree/main/02-setup-DOCR).

!!! note
    Please note that DOCR creation can also be achieved from the [Digital Ocean Cloud Console](https://docs.digitalocean.com/products/container-registry/quickstart/).

Next, you will learn how to create a DOKS cluster to use as a Kubernetes development environment, and start working with microservices.

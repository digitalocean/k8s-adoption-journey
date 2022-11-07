## Introduction

In this section you will learn you how to create a [DigitalOcean Container Registry](https://docs.digitalocean.com/products/container-registry/) (**DOCR**) registry using `doctl`.

A docker container registry is required to store all [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app images used in this guide. For each microservice you need a separate repository in the registry. The microservices-demo app consists of **nine microservice**, hence a total of nine Docker repositories will be created in the registry.

## Prerequisites

To complete this section you will need:

1. Doctl utility already installed, as explained in the [Installing Required Tools -> Doctl](installing-required-tools.md#installing-doctl) section.
2. Make sure that you're authenticated with the DigitalOcean API as explained in the [Authenticating with the DigitalOcean API](do-api-auth.md) section.

## Provisioning a DigitalOcean Container Registry for Microservices Development

Following command will create a `professional tier` Docker registry in the `nyc3` region, named `microservices-demo`:

```shell
doctl registry create microservices-demo \
    --subscription-tier professional \
    --region nyc3
```

!!! note
    - The **professional tier** is required to store all docker images used in this guide which costs **20$/month**.
    - Above example is using **microservices-demo** as the registry name. Don't forget to adjust according to your setup.
    - It is recommended to use a region for your registry that is closest to you for faster image download/upload operations. Run the following command - `doctl registry options available-regions` to check available regions.

Next, you will prepare a personal GitHub repository to store all required assets for the `microservices-demo` application, as well as the initial configuration to make it work.

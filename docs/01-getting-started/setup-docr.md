## Introduction

In this section you will learn you how to create a [DigitalOcean Container Registry](https://docs.digitalocean.com/products/container-registry/) (**DOCR**) registry using `doctl`.

A docker container registry is required to store all [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app images used in this guide. For each microservice you need a separate repository in the registry. The microservices-demo app consists of **nine microservice**, hence a total of nine Docker repositories will be created in the registry.

## Prerequisites

1. Doctl utility already installed, as explained in the [Installing Required Tools -> Doctl](installing-required-tools.md#installing-doctl) section.
2. Kubectl utility already installed as explained in the [Installing Required Tools -> Kubectl](installing-required-tools.md#installing-kubectl) section.
3. Make sure that you're authenticated with the DigitalOcean API as explained in the [Authenticating with the DigitalOcean API](do-api-auth.md) section.

## Provisioning a DigitalOcean Container Registry for Microservices Development

Following command will create a `professional tier` Docker registry in the `nyc3` region, named `microservices-demo`:

```shell
doctl registry create microservices-demo \
    --subscription-tier professional \
    --region nyc3
```

!!! notes
    - The **professional tier** is required to store all docker images used in this guide which costs **20$/month**.
    - You can have **only one registry endpoint per account** in **DOCR**. A **repository** in a registry refers to a **collection of container images** using tags.
    - It is recommended to use a region for your registry that is closest to you for faster image download/upload operations. Run the following command - `doctl registry options available-regions` to check available regions.

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
    Please note that this step should be configured for each new cluster you create in your DO account.

## Building and pushing docker images to DOCR

In this section you will build and push the docker images required by the next sections. The sample application used throughout this adoption journey is the [Online Boutique](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) application.

1. Navigate to the repository created in [Setup Github Repository](setup-github-repository.md)

2. Change directory to the `microservices-demo` folder:

    ```shell
    cd microservices-demo
    ```

3. Login to DOCR:

    ```shell
    doctl registry login
    ```

4. Run the `make-docker-images.sh` script (make sure to export the required environment variables):

    ```shell
    export REPO_PREFIX="registry.digitalocean.com/microservices-demo"
    export TAG=1.0.0

    ./release-scripts/make-docker-images.sh
    ```

    !!!info
        You will be pushing an initial release first to DOCR (1.0.0) and use that to deploy to the `staging` and `production` environments in the upcoming sections. Later on, GitHub Actions will take care of building, tagging and pushing images to `DOCR`.
        This process might take about 15 minutes.

Next, you will learn how to create a DOKS cluster to use as a Kubernetes development environment, and start working with microservices.

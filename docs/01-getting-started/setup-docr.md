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
    - You can have **only one registry endpoint per account** in **DOCR**. A **repository** in a registry refers to a **collection of container images** using tags.
    - It is recommended to use a region for your registry that is closest to you for faster image download/upload operations. Run the following command - `doctl registry options available-regions` to check available regions.

## Building and Pushing the Online Boutique Application Images to DOCR

In this section, you will push to DOCR the first version (`v1.0.0`) of the [Online Boutique](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) demo application. This step is required to perform the initial testing of the application in the upcoming sections of this guide.

1. Clone your `microservices-demo` repository if you haven't already (make sure to replace the `<>` placeholders first):

    ```shell
    git clone https://github.com/<YOUR_GITHUB_ACCOUNT_USERNAME>/microservices-demo.git
    ```

2. From the command line, change directory to the `microservices-demo` folder (if not there already):

    ```shell
    cd microservices-demo
    ```

3. Login to DOCR:

    ```shell
    doctl registry login
    ```

4. Run the `make-docker-images.sh` script after setting required environment variables first:

    ```shell
    export REPO_PREFIX="registry.digitalocean.com/microservices-demo"
    export TAG="v1.0.0"

    ./release-scripts/make-docker-images.sh
    ```

    !!!info
        You will be pushing an initial release first to DOCR - `v1.0.0`, and use that to deploy to the `staging` and `production` environments in the upcoming sections. Later on, GitHub Actions will take care of building, tagging and pushing images to `DOCR`.

Next, you will setup the development environment and deploy the `microservices-demo` application to the associated DOKS cluster, as well as setting up `ingress` and `monitoring`.

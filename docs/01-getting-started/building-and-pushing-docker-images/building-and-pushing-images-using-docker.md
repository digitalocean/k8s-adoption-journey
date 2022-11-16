## Introduction

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

With Docker, you manage your infrastructure in the same way you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you significantly reduce the delay between writing code and running in production.

## Build and Push Online Boutique Application Images

In this section you will build and push to [DOCR](setup-docr.md) all required images for the online boutique demo project using docker CLI. A helper script is used to ease the process, named [make-docker-images.sh](https://github.com/digitalocean/kubernetes-sample-apps/blob/master/microservices-demo/release-scripts/make-docker-images.sh).

Follow below steps to build and push online boutique demo application images using `docker` CLI:

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
        This script will go through each of the microservices and perform a `docker build` and a `docker push` tagging each image with the service name and the `TAG` environment variable exported above.
        You will be pushing an initial release first to DOCR - `v1.0.0`, and use that to deploy to the `staging` and `production` environments in the upcoming sections. Later on, GitHub Actions will take care of building, tagging and pushing images to `DOCR`.

Next, you have the option to study [Cloud Native Buildpacks](https://buildpacks.io/) project to build and push docker images without having to write a single Dockerfile.

If not, skip to the [Development Environment](setup-doks-dev.md) section where you will learn how to setup DOKS and deploy the `microservices-demo` application to your development environment, as well as configuring `ingress` and `monitoring`.

## Introduction

Cloud Native Buildpacks transform your application source code into images that can run on any cloud. In this section you'll learn the basics of using buildpacks and create the images required for the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) project.

[Buildpacks](https://buildpacks.io/docs/concepts/components/buildpack/) allow you to convert your source code into a secure, efficient, production ready container image without the need to write a Dockerfile so you can focus all your attention on writing the application code. They provide framework and runtime support for your applications. Buildpacks examine your apps to determine all dependencies it needs and configures them appropriately to run on any cloud.

Each buildpack is comprised of two phases:

- The `detect` phase which runs against your source code to determine if the buildpack is applicable or not. Once a buildpack is detected to be applicable, it proceeds to the build stage. Detection criteria is specific to each buildpack – for instance, an `NPM buildpack` might look for a package.json, and a `Go buildpack` might look for Go source files.
- The `build` phase runs against your source code to set up the build-time and run-time environment, download dependencies and compile your source code (if needed) and set appropriate entry point and startup scripts.

[Builders](https://buildpacks.io/docs/concepts/components/builder/) are an ordered combination of buildpacks with a base build image, a lifecycle, and reference to a run image. They take in your app source code and build the output app image. The build image provides the base environment for the builder (for eg. an Ubuntu Bionic OS image with build tooling) and a run image provides the base environment for the app image during runtime. A combination of a `build image` and a `run image` is called a `stack`.

## Build and Push Online Boutique Application Images

In this section you will build and push required images for the online boutique demo project using [pack](https://buildpacks.io/docs/tools/pack/) CLI, a tool maintained by the `Cloud Native Buildpacks` project to support the use of buildpacks. A helper script is used to ease the process, named [make-cnb-docker-images.sh](https://github.com/digitalocean/kubernetes-sample-apps/blob/master/microservices-demo/release-scripts/make-cnb-docker-images.sh).

!!! note
    Cloud Native Buildpacks images work best when run on an x86 architecture workstation. ARM is not 100% supported at this time.
    To be able to use pack you will need to install it as explained in the [Installing Pack](installing-required-tools.md#installing-pack-optional).

Follow below steps to build and push online boutique demo application images using `pack` CLI:

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

4. Run the `make-cnb-docker-images.sh` script after setting required environment variables first:

    ```shell
    export REPO_PREFIX="registry.digitalocean.com/microservices-demo"
    export TAG="v1.0.0"

    ./release-scripts/cnb-docker-images.sh
    ```

    !!!info
        This script will go through each of the microservices and perform a `pack build and publish`, tagging each image with the service name and the `TAG` environment variable exported above. Using Cloud Native Buildpacks means that even if there are no Dockerfiles present, pack will be able to detect which buildpack to use and proceed to the build step.
        You will be pushing an initial release first to DOCR - `v1.0.0`, and use that to deploy to the `staging` and `production` environments in the upcoming sections. Later on, GitHub Actions will take care of building, tagging and pushing images to `DOCR`.

    !!!tip
        If you need to run one of the Python microservices (recommendationservice or emailservice) with a different runtime than what the builder is offering you can change the python runtime in the [Python version](https://github.com/digitalocean/kubernetes-sample-apps/blob/master/microservices-demo/src/emailservice/.python-version) file.
        The `entrypoint` needs to be explicitly set for `Python microservices` when using Cloud Native Buildpacks. This is set in the [Procfile](https://github.com/digitalocean/kubernetes-sample-apps/blob/master/microservices-demo/src/emailservice/Procfile). Any changes to the entrypoints of `Python` microservices need to be set in the `Procfile`.

Next, you will learn how to setup DOKS and deploy the `microservices-demo` application to your development environment, as well as configuring `ingress` and `monitoring`.

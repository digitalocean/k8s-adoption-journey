## Introduction

In this section you will create the GitHub repository hosting the sample application used through this guide. It's a web-based e-commerce app (online boutique) consisting of 11 microservices of which only 9 are used by this guide. In terms of functionality, users can browse items, add them to the cart, and purchase them.

The online boutique application is a clone of the original [GoogleCloudPlatform](https://github.com/GoogleCloudPlatform/microservices-demo) project. It will be used as a demo for the Kubernetes adoption journey. The [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) project from the DigitalOcean [kubernetes-sample-apps](https://github.com/digitalocean/kubernetes-sample-apps) repository has been stripped down to focus only on the major parts required by the adoption journey.

For more information and architecture details, please visit the [GoogleCloudPlatform](https://github.com/GoogleCloudPlatform/microservices-demo) GitHub repository.

Why not create a fork? There are several reasons why a fork is not desired for the adoption journey completion:

1. Each PR opened on your fork will point to the upstream repository by default. You will want to have PRs opened against your repo when testing each section of the adoption journey guide, especially in the continuous integration chapter.
2. Full history of the upstream repo will be present in your fork as well. This can create lot of noise.
3. All projects from the kubernetes-sample-apps upstream are pulled in your fork as well. You only care about microservices-demo.

Next, you will start by creating your own GitHub repository hosting the online boutique demo application source code and configuration files.

## Prerequisites

To complete this section you will need:

1. A GitHub account you own. You can create one for free [here](https://github.com/join/).
2. A [Git client](https://git-scm.com/downloads/) to perform operations on your GitHub repository. Usually bundled with your Linux distro.
3. [Wget](https://www.gnu.org/software/wget/) and unzip utilities. Usually bundled with your Linux distro.

## Set Up Online Boutique GitHub Repository

1. Navigate to [Github](https://github.com/) website and log in using your GitHub account.
2. In the upper-right corner of any page, use the `+` drop-down menu, and select `New repository`.
3. Set the `Repository name` to `microservices-demo`.
4. Click on the `Create repository` button.
5. From the command line clone the newly created repository to your local machine (make sure to replace the `<>` placeholders accordingly):

    ```shell
    git clone git@github.com:<YOUR_GITHUB_USERNAME>/microservices-demo.git
    ```

6. Change directory to your local clone:

    ```shell
    cd microservices-demo
    ```

7. Run the following command to download a zip file of the entire [kubernetes-sample-apps](https://github.com/digitalocean/kubernetes-sample-apps) repo:

    ```shell
    wget https://github.com/digitalocean/kubernetes-sample-apps/archive/refs/heads/master.zip -O kubernetes-sample-apps.zip
    ```

8. Unzip the `microservices-demo` project folder from the `kubernetes-sample-apps.zip` file:

    ```shell
    unzip kubernetes-sample-apps.zip 'kubernetes-sample-apps-master/microservices-demo/*'
    ```

    !!! info
        This will result in a `kubernetes-sample-apps-master` folder being created from the `unzip` process.

9. Copy the content of the `microservices-demo` from the `kubernetes-sample-apps-master` to the current working directory:

    ```shell
    cp -r kubernetes-sample-apps-master/microservices-demo/* .
    ```

10. Remove the `kubernetes-sample-apps-master` and `kubernetes-sample-apps.zip`:

    ```shell
    rm -rf kubernetes-sample-apps-master kubernetes-sample-apps.zip
    ```

    !!! info "The repository structure should look like the following:"
        ```text
        ├── kustomize
        │   ├── base
        │   ├── dev
        │   ├── prod
        │   ├── staging
        │   └── kustomization.yaml
        ├── release-scripts
        │   ├── README.md
        │   ├── license_header.txt
        │   ├── make-docker-images.sh
        │   ├── make-release-artifacts.sh
        │   └── make-release.sh
        ├── src
        │   ├── cartservice
        │   ├── checkoutservice
        │   ├── currencyservice
        │   ├── emailservice
        │   ├── frontend
        │   ├── paymentservice
        │   ├── productcatalogservice
        │   ├── recommendationservice
        │   └── shippingservice
        ├── tilt-resources
        │   ├── dev
        │   │   └── tilt_config.json
        │   └── local
        │       └── tilt_config.json
        ├── CODE_OF_CONDUCT.md
        ├── CONTRIBUTING.md
        ├── LICENSE
        ├── README.md
        └── Tiltfile
        ```

11. Add, commit and push all the changes to your origin:

    ```shell
    git add .
    git commit -m "Initial repository layout"
    git push origin
    ```

At this point your online boutique GitHub repository is prepared and ready to use through this guide. Next, it is important to set main branch protection as well.

## Set Up Main Branch Protection

You should define branch protection rules to disable force pushing, prevent branches from being deleted, and optionally require status checks before merging.

1. From [Github](https://github.com/), navigate to the main page of your repository.
2. Under your repository name, click `Settings`.
3. In the `Code and automation` section of the sidebar, click `Branches`.
4. Next to `Branch protection rules`, click Add rule.
5. Set the `Branch name pattern` to `master`:
6. Tick the following options:
    - Require a pull request before merging
    - Dismiss stale pull request approvals when new commits are pushed

Next, a quick introduction is given for the main project layout and important folders/files containing main configuration.

## Understanding Online Boutique Application Structure

The e-commerce web application used in this guide is using the following layout (some parts are stripped down for simplicity):

```text
.
├── kustomize
│   ├── base
│   │   ├── cartservice.yaml
│   │   ├── checkoutservice.yaml
│   │   ├── currencyservice.yaml
│   │   ├── emailservice.yaml
│   │   ├── frontend.yaml
│   │   ├── kustomization.yaml
│   │   ├── namespace.yaml
│   │   ├── paymentservice.yaml
│   │   ├── productcatalogservice.yaml
│   │   ├── recommendationservice.yaml
│   │   ├── redis.yaml
│   │   └── shippingservice.yaml
│   ├── dev
│   │   └── kustomization.yaml
│   ├── local
│   │   └── kustomization.yaml
│   ├── prod
│   │   └── kustomization.yaml
│   ├── staging
│   │   └── kustomization.yaml
│   └── kustomization.yaml
├── release-scripts
├── src
│   ├── cartservice
│   ├── checkoutservice
│   ├── currencyservice
│   ├── emailservice
│   ├── frontend
│   ├── loadgenerator
│   ├── paymentservice
│   ├── productcatalogservice
│   ├── recommendationservice
│   └── shippingservice
├── tilt-resources
│   ├── dev
│   │   └── tilt_config.json
│   └── local
│       └── tilt_config.json
├── README.md
└── Tiltfile
```

Explanation for the above project structure:

- `kustomize` - main folder containing project kustomizations. Project deployment is managed via [Kustomize](https://kustomize.io/). Each environment is represented and managed via a Kustomize overlay folder - [dev](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/dev), [staging](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/stating), [prod](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/prod), etc. Overlays contain environment specific configuration over the [base](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/base) folder. The `base` contains common configuration across all environments.
- `release-scripts` - contains utility shell scripts used to create, build, tag and push project docker images.
- `src` - this is the main project folder containing source code for all application microservices. It also contains required Dockerfiles to build each component image. It is a standardized layout (except for `cartservice` component). You will find here each project unit tests as well (not all are implemented yet though).
- `tilt-resources` - Tilt [configuration profiles](https://docs.tilt.dev/tiltfile_config.html) for each environment supported by the sample application.
- `Tiltfile` - main project [Tilt](https://tilt.dev/) logic. You will learn more about Tilt in the [development section](tilt-local.md).

Next, you will learn how to create a DOCR (DigitalOcean Container Registry), and push the initial version for the online boutique sample application images.

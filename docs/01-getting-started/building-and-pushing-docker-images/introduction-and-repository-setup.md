## Introduction

In this section you will create the GitHub repository hosting the sample application used through this guide. It's a web-based e-commerce app (online boutique) consisting of 11 microservices of which only 9 are used by this guide. In terms of functionality, users can browse items, add them to the cart, and purchase them.

The online boutique application is a clone of the original [GoogleCloudPlatform](https://github.com/GoogleCloudPlatform/microservices-demo) project. It will be used as a demo for the Kubernetes adoption journey. The [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) project from the DigitalOcean [kubernetes-sample-apps](https://github.com/digitalocean/kubernetes-sample-apps) repository has been stripped down to focus only on the major parts required by the adoption journey.

For more information and architecture details, please visit the [GoogleCloudPlatform](https://github.com/GoogleCloudPlatform/microservices-demo) GitHub repository.

**Why not create a fork?**

There are several reasons why a fork is not appropriate to complete all steps from this guide:

1. Each PR opened on your fork will point to the upstream repository by default. You will want to have PRs opened against your repo when testing each section of the adoption journey guide, especially in the continuous integration chapter.
2. Full history of the upstream repo will be present in your fork as well. This can create lot of noise.
3. All projects from the kubernetes-sample-apps upstream are pulled in your fork as well. You only care about microservices-demo.

Next, you will start by creating your own GitHub repository hosting the online boutique demo application source code and configuration files.

## Prerequisites

To complete this section you will need:

1. A GitHub account you own. You can create one for free [here](https://github.com/join/).
2. A [Git client](https://git-scm.com/downloads/) to perform operations on your GitHub repository. Usually bundled with your Linux distribution.
3. [Wget](https://www.gnu.org/software/wget/) and unzip utilities. Usually bundled with your Linux distribution.
4. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.

## Set Up GitHub Repository for the Online Boutique Application

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

    ??? info "Click to expand `microservices-demo` repository structure"
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

11. Commit and push all changes to main branch:

    ```shell
    git add .
    git commit -m "Initial repository layout"
    git push origin
    ```

At this point your online boutique GitHub repository is prepared and ready to use through this guide. Next, a quick introduction is given for main project layout and important assets.

### Understanding Microservices Demo Project Structure

It's important to familiarize with the folder structure of the e-commerce web application used in this guide. The `microservices-demo` repository folder layout is listed below:

??? info "Click to expand `microservices-demo` project folder layout"
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

Explanations for the above layout:

- `kustomize` - main folder containing project kustomizations. Project deployment is managed via [Kustomize](https://kustomize.io/). Each environment is represented and managed via a Kustomize overlay folder - [dev](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/dev), [staging](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/staging), [prod](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/prod), etc. Overlays contain environment specific configuration over the [base](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/base) folder. The `base` contains common configuration across all environments.
- `release-scripts` - contains utility shell scripts used to create, build, tag and push project docker images.
- `src` - this is the main project folder containing source code for all application microservices. It also contains required Dockerfiles to build each component image. It is a standardized layout (except for `cartservice` component). You will find here each project unit tests as well (not all are implemented yet though).
- `tilt-resources` - Tilt [configuration profiles](https://docs.tilt.dev/tiltfile_config.html) for each environment supported by the sample application.
- `Tiltfile` - main project [Tilt](https://tilt.dev/) logic. You will learn more about Tilt in the [development section](tilt-local.md).

### Configuring DOCR Endpoint for Kustomize Overlays

Each overlay corresponds to an environment and it is defined by the `kustomization.yaml` manifest file present in the corresponding folder, such as `dev`, `staging`, `prod`. Base overlay contains common stuff across all environments.

The following listing shows the Kustomize folder layout used in this guide:

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
...
```

Above listing shows all `kustomization.yaml` manifests present in each environment subfolder (or overlay). The `kustomization.yaml` manifest file is important because it defines the differences across environments. Basically, it overrides or adds new settings over the existing ones present in the `base` subfolder. There's a `kustomization.yaml` manifest file located in the `base` subfolder as well which defines default or common settings for all project microservices.

Going forward, every environment overrides each microservice Docker image used in the project to include registry information. Based on your current setup, this setting needs to be changed accordingly.

Follow below steps to change DOCR settings for each environment:

#### Development Environment DOCR Overlay

1. Open and edit the `kustomize/dev/kustomization.yaml` file using an editor of your choice (preferably with YAML lint suppprt).  For example, you can use [VS Code](https://code.visualstudio.com/):

    ```shell
    code kustomize/dev/kustomization.yaml
    ```

2. For each application image, replace the `microservices-demo` string within each `newName` line with your own registry name:

    ??? info "Click to expand the `kustomize/dev/kustomization.yaml` images section"
        ```yaml hl_lines="4 7 10 13 16 19 22 25 28"
        ...
        images:
        - name: cartservice
          newName: registry.digitalocean.com/microservices-demo/cartservice
          newTag: v1.0.0
        - name: checkoutservice
          newName: registry.digitalocean.com/microservices-demo/checkoutservice
          newTag: v1.0.0
        - name: currencyservice
          newName: registry.digitalocean.com/microservices-demo/currencyservice
          newTag: v1.0.0
        - name: emailservice
          newName: registry.digitalocean.com/microservices-demo/emailservice
          newTag: v1.0.0
        - name: frontend
          newName: registry.digitalocean.com/microservices-demo/frontend
          newTag: v1.0.0
        - name: paymentservice
          newName: registry.digitalocean.com/microservices-demo/paymentservice
          newTag: v1.0.0
        - name: productcatalogservice
          newName: registry.digitalocean.com/microservices-demo/productcatalogservice
          newTag: v1.0.0
        - name: recommendationservice
          newName: registry.digitalocean.com/microservices-demo/recommendationservice
          newTag: v1.0.0
        - name: shippingservice
          newName: registry.digitalocean.com/microservices-demo/shippingservice
          newTag: v1.0.0
        ...
        ```

#### Staging Environment DOCR Overlay

1. Open and edit the `kustomize/staging/kustomization.yaml` file using an editor of your choice (preferably with YAML lint suppprt).  For example, you can use [VS Code](https://code.visualstudio.com/):

    ```shell
    code kustomize/staging/kustomization.yaml
    ```

2. For each application image, replace the `microservices-demo` string within each `newName` line with your own registry name:

    ??? info "Click to expand the `kustomize/staging/kustomization.yaml` images section"
        ```yaml hl_lines="4 7 10 13 16 19 22 25 28"
        ...
        images:
        - name: cartservice
          newName: registry.digitalocean.com/microservices-demo/cartservice
          newTag: v1.0.0
        - name: checkoutservice
          newName: registry.digitalocean.com/microservices-demo/checkoutservice
          newTag: v1.0.0
        - name: currencyservice
          newName: registry.digitalocean.com/microservices-demo/currencyservice
          newTag: v1.0.0
        - name: emailservice
          newName: registry.digitalocean.com/microservices-demo/emailservice
          newTag: v1.0.0
        - name: frontend
          newName: registry.digitalocean.com/microservices-demo/frontend
          newTag: v1.0.0
        - name: paymentservice
          newName: registry.digitalocean.com/microservices-demo/paymentservice
          newTag: v1.0.0
        - name: productcatalogservice
          newName: registry.digitalocean.com/microservices-demo/productcatalogservice
          newTag: v1.0.0
        - name: recommendationservice
          newName: registry.digitalocean.com/microservices-demo/recommendationservice
          newTag: v1.0.0
        - name: shippingservice
          newName: registry.digitalocean.com/microservices-demo/shippingservice
          newTag: v1.0.0
        ...
        ```

#### Production Environment DOCR Overlay

1. Open and edit the `kustomize/production/kustomization.yaml` file using an editor of your choice (preferably with YAML lint suppprt).  For example, you can use [VS Code](https://code.visualstudio.com/):

    ```shell
    code kustomize/production/kustomization.yaml
    ```

2. For each application image, replace the `microservices-demo` string within each `newName` line with your own registry name:

    ??? info "Click to expand the `kustomize/production/kustomization.yaml` images section"
        ```yaml hl_lines="4 7 10 13 16 19 22 25 28"
        ...
        images:
        - name: cartservice
          newName: registry.digitalocean.com/microservices-demo/cartservice
          newTag: v1.0.0
        - name: checkoutservice
          newName: registry.digitalocean.com/microservices-demo/checkoutservice
          newTag: v1.0.0
        - name: currencyservice
          newName: registry.digitalocean.com/microservices-demo/currencyservice
          newTag: v1.0.0
        - name: emailservice
          newName: registry.digitalocean.com/microservices-demo/emailservice
          newTag: v1.0.0
        - name: frontend
          newName: registry.digitalocean.com/microservices-demo/frontend
          newTag: v1.0.0
        - name: paymentservice
          newName: registry.digitalocean.com/microservices-demo/paymentservice
          newTag: v1.0.0
        - name: productcatalogservice
          newName: registry.digitalocean.com/microservices-demo/productcatalogservice
          newTag: v1.0.0
        - name: recommendationservice
          newName: registry.digitalocean.com/microservices-demo/recommendationservice
          newTag: v1.0.0
        - name: shippingservice
          newName: registry.digitalocean.com/microservices-demo/shippingservice
          newTag: v1.0.0
        ...
        ```

Next, it is important to set a few protection rules to avoid pushing directly to `main` branch, as well as how to enforce a set of policies related to how code is merged.

## Set Up Main Branch Protection

You should define branch protection rules to disable force pushing, prevent branches from being deleted, and optionally require status checks before merging.

1. From [GitHub](https://github.com/), navigate to the main page of your repository.
2. Under your repository name, click `Settings`.
3. In the `Code and automation` section of the sidebar, click `Branches`.
4. Next to `Branch protection rules`, click Add rule.
5. Set the `Branch name pattern` to `master`:
6. Tick the following options:
    - Require a pull request before merging.
    - Dismiss stale pull request approvals when new commits are pushed.

The online boutique demo application uses [Docker](https://www.docker.com/) technology to distribute and run all application components.

Next, you have the option to use a [classic docker build](building-and-pushing-images-using-docker.md) to distribute the application, or use [Cloud Native Buildpacks](building-and-pushing-images-using-cnb.md). Cloud Native Buildpacks simplify the process of distributing Docker applications without having to write a single Dockerfile.

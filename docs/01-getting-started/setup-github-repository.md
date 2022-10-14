## Introduction

In this section you will create a Github repository in which you will clone the sample application used throughout this adoption journey - [Online Boutique](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) application.

## Configuring the Github repository

1. Navigate to [Github](https://github.com/) and log into your account.
2. In the upper-right corner of any page, use the `+` drop-down menu, and select `New repository`.
3. Set the `Repository name` to `microservices-demo`.
4. Click on the `Create repository` button.
5. From the command line clone the newly created repository to your local machine (make sure to replace the `<>` placeholders accordingly):

    ```shell
    git clone git clone git@github.com:<YOUR_GITHUB_USERNAME>/microservices-demo.git
    ```

6. Change directory to the clone repository:

    ```shell
    cd microservices-demo
    ```

7. Run the following command to download the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) project and save it to a `.zip` file:

    ```shell
    wget https://github.com/digitalocean/kubernetes-sample-apps/archive/refs/heads/master.zip -O kubernetes-sample-apps.zip
    ```

8. Unzip the `microservices-demo` project:

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
        ```
        ├── kustomize
        │   ├── base
        │   ├── dev
        │   ├── local
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
        ├── CODE_OF_CONDUCT.md
        ├── CONTRIBUTING.md
        ├── LICENSE
        ├── README.md
        ├── Tiltfile
        └── Tiltfile-dev
        ```

11. Change the remote origin to your `microservices-demo` repository (make sure to replace the `<>` placeholders accordingly):

    ```shell
    git remote set-url origin git@github.com:<YOUR_GITHUB_USERNAME>/microservices-demo.git
    ```

12. Add, commit and push all the changes to your origin:

    ```shell
    git add .
    git commit -m "Initial repository layput"
    git push origin
    ```

## Setting branch protection rules

You should define branch protection rules to disable force pushing, prevent branches from being deleted, and optionally require status checks before merging.

1. From [Github](https://github.com/), navigate to the main page of your repository.
2. Under your repository name, click `Settings`.
3. In the `Code and automation` section of the sidebar, click `Branches`.
4. Next to `Branch protection rules`, click Add rule.
5. Set the `Branch name pattern` to `master`:
6. Tick the following options:
    - Require a pull request before merging
    - Dismiss stale pull request approvals when new commits are pushed

Next, you will learn how to create a DOCR (DigitalOcean Container Registry) and push images to it.

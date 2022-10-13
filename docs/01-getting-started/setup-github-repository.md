## Introduction

In this section you will create a Github repository in which you will clone the sample application used throughout this adoption journey - [Online Boutique](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) application.

## Configuring the Github repository

1. Navigate to [Github](https://github.com/) and log into your account.
2. In the upper-right corner of any page, use the `+` drop-down menu, and select `New repository`.
3. Set the `Repository name` to `online-boutique`.
4. Click on the `Create repository` button.
5. From the command line clone the newly created repository to your local machine (make sure to replace the `<>` placeholders accordingly):

    ```shell
    git clone git clone git@github.com:<YOUR_GITHUB_USERNAME>/online-boutique.git
    ```

6. Change directory to the clone repository:

    ```shell
    cd online-boutique
    ```

7. Clone the [sample apps](https://github.com/digitalocean/kubernetes-sample-apps) inside the `online-boutique` folder:

    ```shell
    git clone https://github.com/digitalocean/kubernetes-sample-apps
    ```

8. Change directory to the `kubernetes-sample-apps` folder:

    ```shell
    cd kubernetes-sample-apps
    ```

9. Change the remote origin to your `online-boutique` repository (make sure to replace the `<>` placeholders accordingly):

    ```shell
    git remote set-url origin git@github.com:<YOUR_GITHUB_USERNAME>/online-boutique.git
    ```

10. Remove all of the folders/files apart from the `microservices-demo` one:

    ```shell
    sudo rm -r bookinfo-example doks-example emojivoto-example game-2048-example podinfo-example .github
    ```

11. Add, commit and push all the changes to your origin:

    ```shell
    git add .
    git commit -m "Removes everything apart from microservices-demo"
    git push origin
    ```

    !!! info
        Your repository should not contain only the `microservices-demo` folder.

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

## Introduction

After setting up the CI process, the next step is to configure automated (or continuous) deployments for your environments. In some setups, continuous deployments is not desired. In the end, it all drills down to how often you want to deliver release for your project. If the release cycle and cadence of your project is more agile and you want to deliver more releases in a short period of time, then it makes sense to have such an automated setup.

In practice, this is not the only reason. You will want some environments such as the development environment to continuously reflect latest code changes of your main application repository branch. Here is where continuous deployments play an important role. Another important aspect is - how do you track each change and what is deployed where?

To answer all above questions, a new concept is introduced called [GitOps](https://www.gitops.tech/). GitOps is yet another set of methodologies and accompanying practices, allowing automated deployments and easy track of changes for all your application deployments to various environments. It relies on Git as the single source of truth. It means, you rely on the Git history feature to track all changes, and revert the system to a previous working state in case something goes bad.

One popular solution used to implement GitOps principles is [Argo CD](https://argoproj.github.io/cd/), a free and open source project very well supported by the community. Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.

**Where does Argo CD fit in?**

Argo CD sits at the very end of your CI process. It waits for changes to happen in your Git repository over it is watching. No need to create and maintain separate GitHub workflows for deploying application components to each environment. Just tell Argo about your GitHub repository, and what Kubernetes cluster to sync with. Then, let Argo CD do the heavy lifting.

**Do I need to create separate GitHub repositories and/or branches to sync each Kubernetes environment?**

The short answer is no. No, you don't have to do this. Because you already use Kustomize overlays in your project, you have full control over the deployment process to each environment. No need to create separate branches to target each environment, which is hard to maintain and not recommended.

For small projects it is often enough to use a monorepo structure where you have both application code and Kubernetes configuration manifests. In case of bigger projects, it's best to split application code and Kubernetes stuff into separate repositories. It's easier to track application vs Kubernetes changes this way.

This guides relies on a monorepo approach, but it should be relatively easy to migrate to a split repo setup because all Kubernetes manifests are kept in the [kustomize](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/kustomize/) subfolder.

**Do I need a separate Argo CD instance per environment or just one connecting all?**

You can go either one or the other. This guide is using a separate ArgoCD instance per environment. This kind of setup doesn't affect one environment or the other if one ArgoCD instance goes down, or even if one of the clusters is in a degraded state. Only the current environment where Argo operates is affected. This is called a decentralized setup. The only drawback of this configuration is that application specific resources and system specific resources operate in the same DOKS cluster which leads to additional CPU and/or memory usage.

Another kind of setup (not covered in this guide) is where you have one dedicated DOKS instance (or a dedicated node pool) to serve this purpose. This is called a centralized setup where one Argo CD instance manages all environments from a single place. Main advantage is user application is now decoupled from system apps, and more resources become available for the app you're developing. Main disadvantage is additional costs for operating a dedicated cluster. Another drawback is possible Argo CD downtime for all environments if HA is not properly configured, or if the cluster is not properly sized to handle multiple Argo projects and applications.

Following diagram depicts the Argo CD setup used in this guide for each environment (decentralized setup):

![Argo CD Decentralized Setup](argocd_main_setup.png)

It's important to understand Argo CD concepts, so please follow the official [getting started guide](https://argo-cd.readthedocs.io/en/stable/getting_started/). To keep it short, you need to know how to operate Argo [applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#applications) and [projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/). The application CRD is the most important bit of configuration dealing with connecting various sources such as Git repositories and Kubernetes clusters. On the other hand, Argo CD projects represent a logical way of grouping multiple applications related to each other.

Next, you will learn how to bootstrap Argo CD for each environment. The procedure is basically the same, so once you learn how to do it for one environment, it should be pretty straightforward to perform the same steps for the remaining ones.

## Prerequisites

To complete this section you will need:

1. A container registry already set up as explained in the [Getting Started -> Set up DOCR](setup-docr.md) section. Also, make sure the initial version (`v1.0.0`) for the demo application is already pushed to your DOCR as explained in the same chapter.
2. A DOKS cluster set up and running for each environment:
    - [Development Environment -> Set up DOKS](setup-doks-dev.md)
    - [Staging Environment -> Set up DOKS](setup-doks-staging.md)
    - [Production Environment -> Set up DOKS](setup-doks-production.md)
3. The `microservices-demo` GitHub repository already prepared as explained in the [Preparing demo application GitHub repository](preparing-demo-application.md) section.
4. [Argo CD Autopilot CLI](https://argocd-autopilot.readthedocs.io/en/stable/Installation-Guide/) installed for your distribution as explained in the official docs.
5. A [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token/) (or PAT for short) with the `repo` permissions set. It is required only once by the autopilot CLI to bootstrap Argo CD to your cluster for each environment.

## Bootstrapping Argo CD for the Development Environment

In this section you will deploy Argo CD to your `development` DOKS cluster using the autopilot CLI . Then, you will configure Argo to sync changes using the `dev` overlay folder from your `microservices-demo` GitHub repository.

The [Argo CD autopilot project](https://argocd-autopilot.readthedocs.io) aims to ease the initial bootstrapping process of your Argo instance for each environment. What is nice about this approach is that the Argo installation itself is also synced with your GitHub repo in a GitOps fashion. The autopilot CLI will first deploy Argo CD in your cluster, and then push all required manifests to your GitHub repository.

Please follow below steps to bootstrap and deploy Argo CD to your development DOKS cluster:

1. Export the GitHub personal access token via the `GIT_TOKEN` environment variable (make sure to replace the `<>` placeholders first):

    ```shell
    export GIT_TOKEN=<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE>
    ```

2. Switch Kubernetes context to your `microservices-demo-dev` cluster (notice that cluster name is prefixed using the `do-<region>-` identifier):

    ```shell
    kubectl config set-context do-nyc1-microservices-demo-dev
    ```

3. Bootstrap Argo CD for the development DOKS cluster using the autopilot CLI. You need to do this only once on a fresh cluster (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot repo bootstrap \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/dev"
    ```

    !!!note
        - Once the process finishes successfully you will receive instructions how to access the Argo CD web interface. Most important, you will get the admin user password - put it safe for later use.
        - Also, a new folder should be present in your Git repository - `argocd/dev`, containing all manifests for the `Argo CD dev` environment instance. The same folder is synced by Argo to keep itself up to date, thus following GitOps principles.

4. Check if the `Argo CD dev` instance is up and running:

    ```shell
    kubectl get deployments -n argocd
    ```

    The output looks similar to:

    ```text
    NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
    argocd-applicationset-controller   1/1     1            1           15m
    argocd-dex-server                  1/1     1            1           15m
    argocd-notifications-controller    1/1     1            1           15m
    argocd-redis                       1/1     1            1           15m
    argocd-repo-server                 1/1     1            1           15m
    argocd-server                      1/1     1            1           15m
    ```

    All Argo CD deployments must be healthy and running.

5. Create an Argo project for the `dev` environment (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot project create dev \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/dev"
    ```

    !!!tip
        It's best practice to organize your Argo applications using projects. For example, you can use Argo projects to define environments, such as in the above example.

6. Finally, create an Argo application for the `microservices-demo` project using the Kustomize `dev` overlay (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot app create microservices-demo \
        --app "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/kustomize/dev" \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/dev" \
        --project dev \
        --type kustomize
    ```

Now, check if Argo created the microservices-demo application. First, port-forward the Argo web interface:

```shell
kubectl port-forward -n argocd svc/argocd-server 8080:80
```

Open the Argo CD dashboard in your web browser using this link - [localhost:8080](https://localhost:8080/):

![Demo App Argo CD Dashboard](microservices-demo-app-dashboard.png)

If everything went well, you should see the `dev-microservices-demo` app created and synced successfully.

!!!note
    - Argo CD is using this naming convention - `<project_name>-<app_name>`, hence the `dev-microservices-demo` name for the application.
    - Please bear in mind that Argo CD is using the Git polling method by default which takes around **3 minutes** to trigger. So, changes are not propagated in an instant.

Next, click on the `dev-microservices-demo` app tile - you should see the online boutique application composition (microservices):

![Online Boutique App Composition](microservices-demo-app-composition.png)

Finally, port-forward the frontend service to check the online boutique application status:

```shell
kubectl port-forward -n microservices-demo-dev svc/frontend 9090:80
```

Open a web browser pointing to [localhost:9090](http://localhost:9090/) - you should see the online boutique application landing page.

!!!tip
    You should see the previous changes that you made in the [Set up continuous integration -> Testing the Online Boutique Application GitHub Workflows](setup-continuous-integration.md#testing-the-online-boutique-application-github-workflows) chapter applied as well. So, please go ahead and check that as well.

Next, you will perform the same steps to bootstrap Argo CD for the staging environment.

## Bootstrapping Argo CD for the Staging Environment

In this section you will deploy Argo CD to your `staging` DOKS cluster using the autopilot CLI . Then, you will configure Argo to sync changes using the `staging` overlay folder from your `microservices-demo` GitHub repository.

Please follow below steps to bootstrap and deploy Argo CD to your staging DOKS cluster:

1. Export the GitHub personal access token via the `GIT_TOKEN` environment variable, if not already (make sure to replace the `<>` placeholders first):

    ```shell
    export GIT_TOKEN=<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE>
    ```

2. Switch Kubernetes context to your `microservices-demo-staging` cluster (notice that cluster name is prefixed using the `do-<region>-` identifier):

    ```shell
    kubectl config set-context do-nyc1-microservices-demo-staging
    ```

3. Bootstrap Argo CD for the staging DOKS cluster using the autopilot CLI. You need to do this only once on a fresh cluster (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot repo bootstrap \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/staging"
    ```

    !!!note
        - Once the process finishes successfully you will receive instructions how to access the Argo CD web interface. Most important, you will get the admin user password - put it safe for later use.
        - Also, a new folder should be present in your Git repository - `argocd/staging`, containing all manifests for the `Argo CD staging` environment instance. The same folder is synced by Argo to keep itself up to date, thus following GitOps principles.

4. Check if the `Argo CD staging` instance is up and running:

    ```shell
    kubectl get deployments -n argocd
    ```

    The output looks similar to:

    ```text
    NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
    argocd-applicationset-controller   1/1     1            1           10m
    argocd-dex-server                  1/1     1            1           10m
    argocd-notifications-controller    1/1     1            1           10m
    argocd-redis                       1/1     1            1           10m
    argocd-repo-server                 1/1     1            1           10m
    argocd-server                      1/1     1            1           10m
    ```

    All Argo CD deployments must be healthy and running.

5. Create an Argo project for the `staging` environment (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot project create staging \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/staging"
    ```

    !!!tip
        It's best practice to organize your Argo applications using projects. For example, you can use Argo projects to define environments, such as in the above example.

6. Finally, create an Argo application for the `microservices-demo` project using the Kustomize `staging` overlay (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot app create microservices-demo \
        --app "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/kustomize/staging" \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/staging" \
        --project staging \
        --type kustomize
    ```

To verify the whole setup works, please use the same procedure as you already learned in the [Bootstrapping Argo CD for the Development Environment](#bootstrapping-argo-cd-for-the-development-environment) section of this chapter.

!!!note
    Please bear in mind that Argo CD is using the Git polling method by default which takes around **3 minutes** to trigger. So, changes are not propagated in an instant.

Next, you will perform the same steps to bootstrap Argo CD for the production environment.

## Bootstrapping Argo CD for the Production Environment

In this section you will deploy Argo CD to your `production` DOKS cluster using the autopilot CLI . Then, you will configure Argo to sync changes using the `prod` overlay folder from your `microservices-demo` GitHub repository.

Please follow below steps to bootstrap and deploy Argo CD to your production DOKS cluster:

1. Export the GitHub personal access token via the `GIT_TOKEN` environment variable, if not already (make sure to replace the `<>` placeholders first):

    ```shell
    export GIT_TOKEN=<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE>
    ```

2. Switch Kubernetes context to your `microservices-demo-production` cluster (notice that cluster name is prefixed using the `do-<region>-` identifier):

    ```shell
    kubectl config set-context do-nyc1-microservices-demo-production
    ```

3. Bootstrap Argo CD for the production DOKS cluster using the autopilot CLI. You need to do this only once on a fresh cluster (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot repo bootstrap \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/prod"
    ```

    !!!note
        - Once the process finishes successfully you will receive instructions how to access the Argo CD web interface. Most important, you will get the admin user password - put it safe for later use.
        - Also, a new folder should be present in your Git repository - `argocd/prod`, containing all manifests for the `Argo CD production` environment instance. The same folder is synced by Argo to keep itself up to date, thus following GitOps principles.

4. Check if the `Argo CD production` instance is up and running:

    ```shell
    kubectl get deployments -n argocd
    ```

    The output looks similar to:

    ```text
    NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
    argocd-applicationset-controller   1/1     1            1           5m
    argocd-dex-server                  1/1     1            1           5m
    argocd-notifications-controller    1/1     1            1           5m
    argocd-redis                       1/1     1            1           5m
    argocd-repo-server                 1/1     1            1           5m
    argocd-server                      1/1     1            1           5m
    ```

    All Argo CD deployments must be healthy and running.

5. Create an Argo project for the `production` environment (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot project create prod \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/prod"
    ```

    !!!tip
        It's best practice to organize your Argo applications using projects. For example, you can use Argo projects to define environments, such as in the above example.

6. Finally, create an Argo application for the `microservices-demo` project using the Kustomize `prod` overlay (make sure to replace the `<>` placeholders first):

    ```shell
    argocd-autopilot app create microservices-demo \
        --app "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/kustomize/prod" \
        --repo "github.com/<YOUR_GITHUB_USERNAME>/microservices-demo/argocd/prod" \
        --project prod \
        --type kustomize
    ```

To verify the whole setup works, please use the same procedure as you already learned in the [Bootstrapping Argo CD for the Development Environment](#bootstrapping-argo-cd-for-the-development-environment) section of this chapter.

!!!note
    Please bear in mind that Argo CD is using the Git polling method by default which takes around **3 minutes** to trigger. So, changes are not propagated in an instant.

## Testing the Final Setup

As an exercise, go ahead and make a change to one or even more microservices. Then, open a PR and check the associated workflow. Next, approve the PR and merge change into main branch. Check the main branch GitHub workflow as it progresses. When finished, check if Argo propagated the latest changes to your development DOKS cluster.

Next, you will learn how to create GitHub releases for your application and propagate (or promote) changes to upper environments. First to staging, and then after QA approval (may imply project manager decision as well) deploy to production environment as well.

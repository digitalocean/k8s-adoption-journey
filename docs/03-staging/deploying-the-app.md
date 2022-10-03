## Introduction

!!! note
        On the `development` cluster you used `Tilt` to deploy the sample application. On the `staging` environment, `kustomize` will be used to initially deploy the application and then `ArgoCD` will do the heavy lifting for future deployments.

In this section you will learn how to deploy the `online boutique` sample application using [Kustomize](https://kustomize.io/). It is tool for customizing Kubernetes configurations. It has the following features to manage application configuration files:

- generating resources from other sources
- setting cross-cutting fields for resources
- composing and customizing collections of resources

A more common use case of `Kustomize` is that you’ll need multiple variants of a common set of resources, e.g., a `development`, `staging` and `production` variant.
For this purpose, kustomize supports the idea of an `overlay` and a `base`. Both are represented by a `kustomization` file. The base declares things that the variants share in common (both resources and a common customization of those resources), and the overlays declare the differences. This is well represented in the structure of the `online boutique` sample application [repository structure](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo).

!!! info
        You will be using the `kubectl` built-in verion of `Kustomize`.

## Prerequisites

To complete this section you will need:

1. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.
2. A Kubernetes cluster (DOKS) up and running as explained in the [Set up DOKS](setup-doks.md) section.
3. Doctl utility already installed as explained in the [Installing Required Tools -> Doctl](installing-required-tools.md#installing-doctl) section.

## Deploying the application with Kustomize

1. Clone the [sample-apps-repository](https://github.com/digitalocean/kubernetes-sample-apps).

    ```shell
    git clone https://github.com/digitalocean/kubernetes-sample-apps.git
    ```

2. Change directory to the `microservices-demo` folder:

    ```shell
    cd kubernetes-sample-apps/microservices-demo
    ```

3. Deploy the Kustomization to your cluster using `kubectl`:

    ``` shell
    kubectl apply -k kustomize/staging
    ```

    !!! note
        To verify that the deployment was succesful run the `kubectl get all -n microservices-demo-staging` command.
        The application is deployed to the `staging` environment using the images built and pushed in the [Setup DOCR](setup-docr.md) section.

4. Access the web interface by port-forwarding the `frontned` service:

    ```shell
    kubectl port-forward service/frontend -n microservices-demo-staging 9090:80
    ```

5. Open a web browser and point to [localhost:9090](http://localhost:9090/). You should see the online boutique welcome page.

    !!! note
            Although you open a connection to localhost in your web browser, traffic is forwarded to the remote staging cluster by `kubectl`.

Next, you will deploy and configure the Nginx ingress controller for your staging cluster (DOKS) to expose microservices to the outside world. You will also set up [cert-manager](https://cert-manager.io/) to automatically issue valid TLS certificates for your applications.

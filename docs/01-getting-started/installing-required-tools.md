## Introduction

This section will show you how to install the required tools needed to complete this guide. You will focus on most popular tools used in the Kubernetes world. You will also install additional programs used for interacting with the DigitalOcean API, and local development enablement.

Below is a complete list of the tools used in this guide:

1. [Kubectl](https://kubernetes.io/docs/reference/kubectl/) - this the official Kubernetes client. Allows you to interact with the Kubernetes API, and to run commands against Kubernetes clusters.
2. [Helm](https://helm.sh/) - this is the package manager for Kubernetes. Behaves the same way as package managers used in Linux distributions, but for Kubernetes. Gained a lot of popularity, and it is a widely adopted solution for managing software packages installation and upgrade in Kubernetes.
3. [Doctl](https://docs.digitalocean.com/reference/doctl/) - allows you to interact with the DigitalOcean API via the command line. It supports most functionality found in the control panel. You can create, configure, and destroy DigitalOcean resources like Droplets, Kubernetes clusters, firewalls, load balancers, database clusters, domains, and more.
4. [Docker Desktop](https://www.docker.com/products/docker-desktop/) - enables you to build and share containerized applications and microservices using Docker. It has a GUI interface, and bundles a ready to run Kubernetes cluster to use for local development.
5. [Kustomize](https://kustomize.io/) - Kustomize lets you customize raw, template-free YAML files for multiple purposes, leaving the original YAML untouched and usable as is.
6. [Tilt](https://tilt.dev/) - eases local development by taking away the pain of time consuming Docker builds, watching files, and bringing environments up to date.

## Prerequisites

To complete this section, you will need:

1. [Homebrew](https://brew.sh/) if you are using a macOS system.
2. [Curl](https://curl.se/) package installed on your system.

## Installing Docker Desktop

Depending on your operating system, you can install [docker-desktop](https://docs.docker.com/desktop/) in the following ways:

=== "MacOS"

    1. Install `docker-desktop` using Homebrew:

        ```shell
        brew install --cask docker
        ```

    2. Test to ensure you installed the latest version:
    
        ```shell
        docker version
        ```

=== "Linux - Ubuntu"

    1. Update `apt` package index:

        ```shell
        sudo apt-get update
        sudo apt-get install \
            ca-certificates \
            curl \
            gnupg \
            lsb-release
        ```

    2. Add Docker's official GPG key:

        ```shell
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        ```

    3. Set up the repository:

        ```shell
        echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        ```
    
    4. Install docker desktop:
        
        ```shell
        sudo apt install docker-desktop
        ```

    5. Test to ensure you installed the latest version:
    
        ```shell
        docker version
        ```

## Installing Doctl

Depending on your operating system, you can install [doctl](https://docs.digitalocean.com/reference/doctl/) in the following ways:

=== "MacOS"

    1. Install `doctl` using Homebrew:

        ```shell
        brew install doctl
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        doctl version
        ```

=== "Linux"

    1. Download the latest `doctl` package (check [releases](https://github.com/digitalocean/doctl/releases) page):

        ```shell
        curl -LO https://github.com/digitalocean/doctl/releases/download/v1.79.0/doctl-1.79.0-linux-amd64.tar.gz
        ```
    
    2. Extract the `doctl` package:
    
        ```shell
        tar xf doctl-1.79.0-linux-amd64.tar.gz
        ```

    3. Set the executable flag, and make the `doctl` binary available in your path:

        ```shell
        chmod +x doctl
        sudo mv doctl /usr/local/bin
        ```
    
    4. Test to ensure you installed the latest version:

        ```shell
        doctl version
        ```

## Installing Kubectl

Depending on your operating system, you can install [kubectl](https://kubernetes.io/docs/reference/kubectl/) in the following ways:

=== "MacOS"

    1. Install kubectl using Homebrew:

        ```shell
        brew install kubectl
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        kubectl version --client
        ```

=== "Linux"

    1. Download the latest `kubectl` release:

        ```shell
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        ```

    2. Set the executable flag, and make the `kubectl` binary available in your path:

        ```shell
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin
        ```
    
    3. Test to ensure you installed the latest version:

        ```shell
        kubectl version --client
        ```

## Installing Helm

Depending on your operating system, you can install [helm](https://helm.sh/docs/intro/install/) in the following ways:

=== "MacOS"

    1. Install helm using Homebrew:

        ```shell
        brew install helm
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        helm version
        ```

=== "Linux"

    1. Download the latest `helm` release:

        ```shell
        curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
        sudo apt-get install apt-transport-https --yes
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
        sudo apt-get update
        sudo apt-get install helm
        ```
    
    2. Test to ensure you installed the latest version:

        ```shell
        helm version
        ```

## Installing Kustomize

Depending on your operating system, you can install [kustomize](https://kubectl.docs.kubernetes.io/installation/kustomize/) in the following ways:

=== "MacOS"

    1. Install kustomize using Homebrew:

        ```shell
        brew install kustomize
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        kustomize version 
        ```

=== "Linux"

    1. Install kustomize by running the following script:

        ```shell
        curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
        ```
    
    2. Test to ensure you installed the latest version:

        ```shell
        kustomize version
        ```

## Installing Tilt

Depending on your operating system, you can install [Tilt](https://docs.tilt.dev/install.html) in the following ways:

=== "MacOS"

    1. Install tilt using curl:

        ```shell
        brew install tilt
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        tilt version
        ```

=== "Linux"
    1. Install tilt using curl:

        ```shell
        curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        tilt version
        ```

Next, you will learn how to authenticate with the DigitalOcean API to get the most out of the tools used in this guide to provision required cloud resources.

# Installing Required Tools

This section will show you how to install the required tools to bootstrap a [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/) cluster (aka **DOKS**).

## Prerequisites

To complete this section, you will need:

1. A [DigitalOcean account](https://docs.digitalocean.com/products/getting-started/#sign-up) for accessing the `DigitalOcean` platform.
2. A [DigitalOcean personal access token](https://docs.digitalocean.com/reference/api/create-personal-access-token) for using the `DigitalOcean` API.
3. Curl package installed on your system.

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

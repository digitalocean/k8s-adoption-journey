# Installing Required Tools

This section will show you how to install the required tools to bootstrap a [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/) cluster (aka **DOKS**).

## Prerequisites

To complete this section, you will need:

1. A [DigitalOcean account](https://docs.digitalocean.com/products/getting-started/#sign-up) for accessing the `DigitalOcean` platform.
2. A [DigitalOcean personal access token](https://docs.digitalocean.com/reference/api/create-personal-access-token) for using the `DigitalOcean` API.
3. Curl package installed on your system.

## Installing Docker Desktop

Depending on your operating system, you can install [docker-desktop](https://docs.docker.com/desktop/) in the following ways:

=== "MacOS"

    1. Download the `DMG` file corresponding to your version of Mac machine and install it from [here](https://docs.docker.com/desktop/install/mac-install/)
    2. Test to ensure you installed the latest version:
    
        ```shell
            docker version
        ```

=== "Linux"

    1. Download the package file corresponding to your Linux distribution and install it from [here](https://docs.docker.com/desktop/install/linux-install/)
    2. Test to ensure you installed the latest version:
    
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

    1. Install kubectl using Homebrew:

        ```shell
        brew install helm
        ```

    2. Test to ensure you installed the latest version:

        ```shell
        helm version
        ```

=== "Linux"

    1. Download the latest `kubectl` release:

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

## Installing Tilt

Depending on your operating system, you can install [Tilt](https://docs.tilt.dev/install.html) in the following ways:

=== "MacOS"

    1. Install tilt using curl:

        ```shell
        curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
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

# Installing Required Tools

This section will show you how to install the required tools to bootstrap a [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/) cluster (aka **DOKS**).

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

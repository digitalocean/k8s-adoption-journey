## Introduction

This section will show you how to authenticate with the [DigitalOcean API](https://docs.digitalocean.com/reference/api/api-reference/). To use the API, you’ll first generate a personal access token.

A personal access token allows you to use automation tools such as [doctl](https://docs.digitalocean.com/reference/doctl/) to create and manage various DigitalOcean cloud resources, such as [Kubernetes Clusters](https://docs.digitalocean.com/products/kubernetes/), [Droplets](https://docs.digitalocean.com/products/droplets/), [Container Registries](https://docs.digitalocean.com/products/container-registry/), etc.

## Prerequisites

To complete this section, you will need:

1. A [DigitalOcean account](https://docs.digitalocean.com/products/getting-started/#sign-up) for accessing the `DigitalOcean` platform.
2. A [DigitalOcean personal access token](https://docs.digitalocean.com/reference/api/create-personal-access-token) for using the `DigitalOcean` API.
3. Doctl utility already installed as explained in the [Installing Required Tools -> Doctl](installing-required-tools.md#installing-doctl) section.

## Authenticating with the DigitalOcean API

First you will need to initialze `doctl` by running the following command:

```shell
doctl auth init
```

After entering your token `doctl` should be able to validate your token.

Test to ensure that your account is configured for `doctl` to use:

```shell
doctl auth list
```

You should see a line containing your account and the `"current"` string next to it.

For more info on this topic please see this [Kubernetes Starter Kit Authentication Section](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers/tree/main/01-setup-DOKS#step-2---authenticating-to-digitalocean-api).

Next, you will learn how to create a DigitalOcean Container Registry to store all microservices Docker images used in this guide for demonstration.

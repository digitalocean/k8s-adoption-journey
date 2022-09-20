# Authentication

This section will show you how to authenticate with the `DigitalOcean` API.
A token created in the [Installing required tools](installing-required-tools.md) allows you to authenticate doctl for use with your DigitalOcean account.

## Prerequisites

To complete this section, you will need:

1. A [DigitalOcean account](https://docs.digitalocean.com/products/getting-started/#sign-up) for accessing the `DigitalOcean` platform.
2. A [DigitalOcean personal access token](https://docs.digitalocean.com/reference/api/create-personal-access-token) for using the `DigitalOcean` API.

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

You should see a line containing your acount and the "current" string next to it.

For more info on this topic please see this [Kubernetes Starter Kit Authentication Section](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers/tree/main/01-setup-DOKS#step-2---authenticating-to-digitalocean-api).

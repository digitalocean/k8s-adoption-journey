## Introduction

This section will show you how to create a [DigitalOcean Kubernetes Cluster](https://docs.digitalocean.com/products/kubernetes/) (**DOKS**) cluster that can be used for both local and remote development, targeting the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) sample used as a reference in this guide.

## Creating a DOKS Cluster for Microservices Development

In this step, you will create a new Kubernetes cluster running on the DigitalOcean platform, using the [doctl](https://docs.digitalocean.com/reference/doctl/) utility.

Following command will create a DigitalOcean Kubernetes cluster named `microservices-demo-dev`, with a pool size of `2 nodes`, each having `2 vCPUs` and `2GB` of RAM, in the `nyc1` region:

```shell
doctl k8s cluster create microservices-demo-dev \
  --auto-upgrade=true \
  --maintenance-window "saturday=21:00" \
  --node-pool "name=basicnp;size=s-2vcpu-2gb;count=2;tag=adoption-journey;label=type=basic" \
  --region nyc1
```

!!! notes
    - The example cluster created above is using 2 nodes, each having **2vCPU/2GB** size, which amounts to **36$/month**.
    - For simplicity and consistency through all the guide, the **microservices-demo-dev** name was picked for the example cluster. You can choose any name you like, but you need to make sure the naming convention stays consistent.
    - Cluster region can be changed to one that's closest to you. Run the following command `doctl k8s options regions` to check available regions.
    - Cluster [auto upgrade](https://docs.digitalocean.com/products/kubernetes/how-to/upgrade-cluster/#automatically) is enabled (`--auto-upgrade=true`). Kubernetes clusters should be auto-upgraded to ensure that they always contain the latest security patches.

Next, you can verify the cluster details. First, fetch your `DOKS` cluster `ID`:

```shell
doctl k8s cluster list
```

Finally, check if the `kubectl` context was set to point to your `DOKS` cluster. The `doctl` utility should do this automatically:

```shell
kubectl config current-context
```

For more info on this topic please see this [Kubernetes Starter Kit DOKS Creation](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers/tree/main/01-setup-DOKS#step-3---creating-the-doks-cluster).

!!! note
    Please note that DOKS creation can also be achieved from the [Digital Ocean Cloud Console](https://docs.digitalocean.com/products/kubernetes/quickstart/).

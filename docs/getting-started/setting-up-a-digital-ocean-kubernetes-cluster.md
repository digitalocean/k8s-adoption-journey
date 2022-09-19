# Setting up a Digital Ocean Kubernetes Cluster (DOKS)

This section will show you how to create a DOKS cluster using the `doctl` CLI.

From the command line run the following:

```shell
doctl k8s cluster create <YOUR_CLUSTER_NAME> \
  --auto-upgrade=false \
  --maintenance-window "saturday=21:00" \
  --node-pool "name=basicnp;size=s-2vcpu-2gb;count=1;tag=adoption-journey;label=type=basic" \
  --region nyc1
```

!!! note
    Please replace the **`<YOUR_CLUSTER_NAME>`** placeholder with a valid name.
    This cluster is using `2vCPU/2GB` node size which amounts to 18$/month.

Next, you can verify the cluster details. First, fetch your `DOKS` cluster `ID`:

```shell
doctl k8s cluster list
```

Finally, check if the `kubectl` context was set to point to your `DOKS` cluster. The `doctl` utility should do this automatically:

```shell
kubectl config current-context
```

For more info on this topic please see this [Kubernetes Starter Kit DOKS Creation](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers/tree/main/01-setup-DOKS#step-3---creating-the-doks-cluster).

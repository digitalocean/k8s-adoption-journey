## Introduction

The goal of observability is to understand what’s happening across all these environments and among the technologies, so you can detect and resolve issues to keep your systems efficient and reliable.

Observability is a measure of how well the system’s internal states can be inferred from knowledge of its external outputs. It uses the data and insights that monitoring produces to provide a holistic understanding of your system, including its health and performance. The observability of your system, then, depends partly on how well your monitoring metrics can interpret your system's performance indicators.

## Prerequisites

1. Helm installed as explained in the [Installing required tools](installing-required-tools.md) section.
2. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.
3. A Kubernetes cluster (DOKS) up and running as explained in the [Set up DOKS](setup-doks.md) section.
4. The online boutique sample application deployed to your cluster as explained in the [Deploying the app](deploying-the-app.md) section.

## Installing the Prometheus Monitoring Stack

1. Add the `Helm` repository and list the available charts:

    ```shell
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

    helm repo update prometheus-community
    ```

2. Install the `kube-prometheus-stack`, using `Helm`:

    ```shell
    HELM_CHART_VERSION="35.5.1"

    helm install kube-prom-stack prometheus-community/kube-prometheus-stack --version "${HELM_CHART_VERSION}" \
      --namespace monitoring \
      --create-namespace \
      -f "docs/03-staging/assets/manifests/prom-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```

    !!! note
        A `specific` version for the `Helm` chart is used. In this case `35.5.1` was picked, which maps to the `0.56.3` version of the application.
        To check if the installation was successful, run the `helm ls -n monitoring` command, and confirm the deployment status.

3. Connect to `Grafana` (using default credentials: `admin/prom-operator`) - by port forwarding to local machine:

    ```shell
    kubectl --namespace monitoring port-forward svc/kube-prom-stack-grafana 3000:80
    ```

    !!! info
        You should **NOT** expose `Grafana` to `public` network (eg. you should create an ingress mapping or `LB` service).

4. Open a web browser and point to [localhost:3000](http://localhost:3000). You should see the `Grafna` login page.

    !!! info
        `Grafana` installation comes with a number of dashboards. Open a web browser on [localhost:3000](http://localhost:3000). Once in, you can go to `Dashboards -> Browse`, and choose different dashboards.

## Configuring Persistent Storage for Prometheus

In this section, you will learn how to enable `persistent storage` for `Prometheus`, so that metrics data is persisted across `server restarts`, or in case of `cluster failures`.

1. Open the `"docs/03-staging/assets/manifests/prom-stack-values-v35.5.1.yaml` file provided and uncomment the `storageSpec` section. The definition should look like this:

    ```yaml
    prometheusSpec:
      storageSpec:
        volumeClaimTemplate:
          spec:
            storageClassName: do-block-storage
            accessModes: ["ReadWriteOnce"]
            resources:
              requests:
                storage: 5Gi
    ```

2. Apply the new settings using `Helm`:

    ```shell
    HELM_CHART_VERSION="35.5.1"

    helm upgrade kube-prom-stack prometheus-community/kube-prometheus-stack --version "${HELM_CHART_VERSION}" \
      --namespace monitoring \
      -f "docs/03-staging/assets/manifests/prom-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```

    !!! note
        Check the `PVC` status by running `kubectl get pvc -n monitoring`. A new `Volume` should appear in the [Volumes](https://cloud.digitalocean.com/volumes) web page, from your `DigitalOcean` account panel.

## Configuring Persistent Storage for Grafana

In this section, you will learn how to enable `persistent storage` for `Grafana`, so that metrics data is persisted across `server restarts`, or in case of `cluster failures`.

1. Open the `"docs/03-staging/assets/manifests/prom-stack-values-v35.5.1.yaml` file provided and uncomment the `storageSpec` section. The definition should look like this:

    ```yaml
    grafana:
    ...
    persistence:
        enabled: true
        storageClassName: do-block-storage
        accessModes: ["ReadWriteOnce"]
        size: 5Gi
    ```

2. Apply the new settings using `Helm`:

    ```shell
    HELM_CHART_VERSION="35.5.1"

    helm upgrade kube-prom-stack prometheus-community/kube-prometheus-stack --version "${HELM_CHART_VERSION}" \
      --namespace monitoring \
      -f "docs/03-staging/assets/manifests/prom-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```

    !!! note
        Check the `PVC` status by running `kubectl get pvc -n monitoring`. A new `Volume` should appear in the [Volumes](https://cloud.digitalocean.com/volumes) web page, from your `DigitalOcean` account panel.

## Installing the Loki Stack

In this section you will learn about [Loki](https://github.com/grafana/helm-charts/tree/main/charts/loki-stack), which is a log `aggregation` system inspired by `Prometheus`.
`Loki` uses `Promtail` to fetch logs from all `Pods` running in your cluster. Then, logs are `aggregated` and `compressed`, and sent to the configured `storage`. Next, you can connect `Loki` data source to `Grafana` and view the logs.

1. Add the `Grafana` Helm repository and list the available charts:

    ```shell
    helm repo add grafana https://grafana.github.io/helm-charts

    helm repo update grafana
    ```

2. Intall the `Loki` stack using `Helm`:

    ```shell
        HELM_CHART_VERSION="2.6.4"

        helm install loki grafana/loki-stack --version "${HELM_CHART_VERSION}" \
        --namespace=loki-stack \
        --create-namespace \
        -f "docs/03-staging/assets/manifests/loki-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```  

    !!! note
        The above values file, enables `Loki` and `Promtail` for you, so no other input is required. `Prometheus` and `Grafana` installation is disabled, because [Installing the Prometheus Monitoring Stack](#installing-the-prometheus-monitoring-stack) took care of it already.
        The `2.6.4` Helm chart version is picked for `loki-stack`, which maps to application version `2.4.2`.
        To check if the installation was successful, run the `helm ls -n loki-stack` command, and confirm the deployment status.

## Configuring Grafana with Loki

In this section, you will add the `Loki` data source to `Grafana`. First, you need to expose the `Grafana` web interface on your local machine (default credentials: `admin/prom-operator`):

```shell
kubectl --namespace monitoring port-forward svc/kube-prom-stack-grafana 3000:80
```

Next, open a web browser on [localhost:3000](http://localhost:3000), and follow below steps:

1. Click the `Configuration` gear from the left panel.
2. Select `Data sources`.
3. Click the `Add data source` blue button.
4. Select `Loki` from the list and add `Loki` url `http://loki.loki-stack:3100`.
5. Save and test.

!!! info
    If everything goes well, a green label message will appear, saying `Data source connected and labels found.`

You can access logs from the `Explore` tab of `Grafana`. Make sure to select `Loki` as the data source. Use the `Help` button for log search cheat sheet.
    !!! info
        As an example query, to retrieve all the logs for the `microservices-demo-staging` namespace you can run: `{namespace="microservices-demo-staging"}`.

TBD

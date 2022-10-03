## Introduction

The goal of observability is to understand what’s happening across all these environments and among the technologies, so you can detect and resolve issues to keep your systems efficient and reliable.

Observability is a measure of how well the system’s internal states can be inferred from knowledge of its external outputs. It uses the data and insights that monitoring produces to provide a holistic understanding of your system, including its health and performance. The observability of your system, then, depends partly on how well your monitoring metrics can interpret your system's performance indicators.

## Prerequisites

1. Helm installed as explained in the [Installing required tools](installing-required-tools.md) section.
2. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.
3. A Kubernetes cluster (DOKS) up and running as explained in the [Set up DOKS](setup-doks.md) section.
4. The online boutique sample application deployed to your cluster as explained in the [Deploying the app](deploying-the-app.md) section.
5. A [DO Spaces](https://cloud.digitalocean.com/spaces) bucket for `Loki` storage. Please follow the official `DigitalOcean` tutorial to [create one](https://docs.digitalocean.com/products/spaces/how-to/create/). Make sure that it is set to `restrict file listing` for security reasons.

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

1. Open the `docs/03-staging/assets/manifests/prom-stack-values-v35.5.1.yaml` file provided and uncomment the `storageSpec` section. The definition should look like this:

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

## Configuring Persistent Storage for Loki

In this step, you will learn how to enable `persistent` storage for `Loki`. You're going to use the `DO Spaces` bucket created in the [Prerequisites](#prerequisites) section.

1. Open the `docs/03-staging/assets/manifests/loki-stack-values-v35.5.1.yaml` file provided and remove the comments surrounding the `schema_config` and `storage_config` keys. The definition should look like this:

    ??? note "Click to expand the `loki config`"
            loki:
              enabled: true
              config:
                schema_config:
                  configs:
                    - from: "2020-10-24"
                      store: boltdb-shipper
                      object_store: aws
                      schema: v11
                      index:
                        prefix: index_
                        period: 24h
                storage_config:
                boltdb_shipper:
                  active_index_directory: /data/loki/boltdb-shipper-active
                  cache_location: /data/loki/boltdb-shipper-cache
                  cache_ttl: 24h
                  shared_store: aws
                aws:
                  bucketnames: <YOUR_DO_SPACES_BUCKET_NAME_HERE>
                  endpoint: <YOUR_DO_SPACES_BUCKET_ENDPOINT_HERE>  # in the following format: <region>.digitaloceanspaces.com
                  region: <YOUR_DO_SPACES_BUCKET_REGION_HERE>      # short region name (e.g.: fra1)
                  access_key_id: <YOUR_DO_SPACES_ACCESS_KEY_HERE>
                  secret_access_key: <YOURDO_SPACES_SECRET_KEY_HERE>
                  s3forcepathstyle: true

2. Apply the new settings using `Helm`:

    ```shell
        HELM_CHART_VERSION="2.6.4"

        helm upgrade loki grafana/loki-stack --version "${HELM_CHART_VERSION}" \
        --namespace=loki-stack \
        -f "docs/03-staging/assets/manifests/loki-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```  

    !!! note
        Check if the main `Loki` application pod is up and running by runnging the following `kubectl` command: `kubectl get pods -n loki-stack -l app=loki`.
        If everything goes well, you should see the `DO Spaces` bucket containing the `index` and `chunks` folders (the `chunks` folder is called `fake`, which is a strange name - this is by design, when not running in `multi-tenant` mode).

## Setting up Alert Manager

Alertmanager is deployed alongside Prometheus and forms the alerting layer of the `kube-prom-stack`. It handles alerts generated by Prometheus by deduplicating, grouping, and routing them to various integrations such as email, Slack or PagerDuty.
Alerts and notifications are a critical part of your workflow. When things go wrong (e.g. any service is down, or a pod is crashing, etc.), you will want to get notifications in real time to handle critical situations as soon as possible.

To create a new alert, you need to add a new definition in the `additionalPrometheusRule`s section from the kube-prom-stack Helm values file.
You will be creating a sample alert that will trigger if the `microservices-demo-staging` namespace does not have an expected number of instances. The expected number of pods for the `online boutique` application is 10.

1. Open the `docs/03-staging/assets/manifests/prom-stack-values-v35.5.1.yaml` file provided and uncomment the `additionalPrometheusRulesMap` block. The definition should look like this:

    ```yaml
    additionalPrometheusRulesMap:
      rule-name:
        groups:
        - name: online-boutique-instance-down
          rules:
            - alert: OnlineBoutiqueInstanceDown
              expr: sum(kube_pod_owner{namespace="microservices-demo-staging"}) by (namespace) < 10
              for: 1m
              labels:
                severity: 'critical'
              annotations:
                description: ' The Number of pods from the namespace {{ $labels.namespace }} is lower than the expected 10. '
                summary: 'Pod {{ $labels.pod }} down'
    ```

2. Apply the new settings using `Helm`:

    ```shell
    HELM_CHART_VERSION="35.5.1"

    helm upgrade kube-prom-stack prometheus-community/kube-prometheus-stack --version "${HELM_CHART_VERSION}" \
      --namespace monitoring \
      -f "docs/03-staging/assets/manifests/prom-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```

    !!! info
        To check that the alert has been created successfully, first port-forward to your local machine by running this command: `kubectl --namespace monitoring port-forward service/kube-prom-stack-kube-prome-prometheus 9090:9090`. Navigate to the [Promethes Console](http://localhost:9090) click on the `Alerts` menu item and identify the `EmojivotioInstanceDown` alert. It should be visible at the bottom of the list.

## Configuring Alertmanager to Send Notifications to Slack

To complete this section you need to have administrative rights over a workspace. This will enable you to create the incoming webhook you will need in the next steps. You will also need to create a channel where you would like to receive notifications from `AlertManager`.

Steps to follow:

1. Open a web browser and navigate to `https://api.slack.com/apps` and click on the `Create New App` button.
2. In the `Create an app` window select the `From scratch` option. Then, give your application a name and select the appropriate workspace.
3. From the `Basic Information` page click on the `Incoming Webhooks` option, turn it on and click on the `Add New Webhook to Workspace` button at the bottom.
4. On the next page, use the `Search for a channel...` drop-down list to select the desired channel where you want to send notifications. When ready, click on the `Allow` button.
5. Take note of the `Webhook URL` value displayed on the page. You will be using it in the next section.

Next you will tell `Alertmanager` how to send `Slack` notifications.

1. Open the `docs/03-staging/assets/manifests/prom-stack-values-v35.5.1.yaml` file provided and uncomment the `alertmaanager.config` block. Make sure to update the `<>` placeholders accordingly. The definition should look like:

    ```yaml
    alertmanager:
      enabled: true
      config:
        global:
          resolve_timeout: 5m
          <!-- #slack_api_url: "<YOUR_SLACK_APP_INCOMING_WEBHOOK_URL_HERE>" -->
        route:
          receiver: "slack-notifications"
          repeat_interval: 12h
          routes:
            - receiver: "slack-notifications"
              matchers:
                - alertname="OnlineBoutiqueInstanceDown"
              continue: false
        receivers:
          - name: "slack-notifications"
            slack_configs:
              - channel: "#<YOUR_SLACK_CHANNEL_NAME_HERE>"
                send_resolved: true
                title: "{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}"
                text: "{{ range .Alerts }}{{ .Annotations.description }}\n{{ end }}"
    ```

2. Apply the new settings using `Helm`:

    ```shell
    HELM_CHART_VERSION="35.5.1"

    helm upgrade kube-prom-stack prometheus-community/kube-prometheus-stack --version "${HELM_CHART_VERSION}" \
      --namespace monitoring \
      -f "docs/03-staging/assets/manifests/prom-stack-values-v${HELM_CHART_VERSION}.yaml"
    ```

  !!! info
      At this point you should only receieve alerts from the matching `OnlinqBoutiqueInstanceDown` alertname. Since the `continue` is set to false `Alertmanager` will only send notifications from this alert and stop sending for others.
      Clicking on the notification name in `Slack` will open a web browser to an unreachable web page with the internal Kubernetes DNS of the `Alertmanager` pod. This is expected. For more information you can check out this [article](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
      For additional information about the configuration parameters for `Alertmanager` you can check out this [doc](https://prometheus.io/docs/alerting/latest/configuration/).
      You can also at some notification examples in this [article](https://prometheus.io/docs/alerting/latest/notification_examples/).

## Setting up Event Exporter for events retention

A Kubernetes event is an object that shows what’s happening inside a cluster, node, pod, or container. These objects are usually generated in response to changes that occur inside your K8s system. The Kubernetes API Server enables all core components to create these events. Generally, each event is accompanied by a log message as well.
Event objects are not regular log events, therefore the Kubernetes logs do not include them. Kubernetes has no builtin support to store or forward these events on the long term, and they are cleaned up after a short retention time defaulting to just 1 hour.
In this section you will learn how to configure the [Kubernetes Events Exporter](https://github.com/resmoio/kubernetes-event-exporter) and collect and perist those events using `Loki`.

1. Create the `ServiceAccount`, `ClusterRole` and `ClusterRoleBinding` using `kubectl`:

    The manifest file looks like the following:

    ??? note "Click to expand the manifest file"
            apiVersion: v1
            kind: Namespace
            metadata:
              name: event-exporter
            ---
            apiVersion: v1
            kind: ServiceAccount
            metadata:
              namespace: event-exporter
              name: event-exporter
            ---
            apiVersion: rbac.authorization.k8s.io/v1
            kind: ClusterRoleBinding
            metadata:
              name: event-exporter
            roleRef:
              apiGroup: rbac.authorization.k8s.io
              kind: ClusterRole
              name: view
            subjects:
              - kind: ServiceAccount
                namespace: event-exporter
                name: event-exporter

    ``` shell
    kubectl apply -f docs/03-staging/assets/manifests/event-exporter-roles.yaml
    ```
  
2. Create the `event exporter` config using `kubectl`:

    The manifest file for the config looks like the following:

    ??? note "Click to expand the config manifest file"
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: event-exporter-cfg
              namespace: event-exporter
            data:
              config.yaml: |
                logLevel: error
                logFormat: json
                route:
                  routes:
                    - match:
                        - receiver: "dump"
                receivers:
                  - name: "dump"
                    stdout: {}

    ``` shell
    kubectl apply -f docs/03-staging/assets/manifests/event-exporter-config.yaml
    ```

3. Finally, create the `event exporter` deployment using kubectl:

    The manifest file for the deployment looks like the following:

    ??? note "Click to expand the deployment manifest file"
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: event-exporter
              namespace: event-exporter
            spec:
              replicas: 1
              template:
                metadata:
                  labels:
                    app: event-exporter
                    version: v1
                spec:
                  serviceAccountName: event-exporter
                  containers:
                    - name: event-exporter
                      image: ghcr.io/resmoio/kubernetes-event-exporter:latest
                      imagePullPolicy: IfNotPresent
                      args:
                        - -conf=/data/config.yaml
                      volumeMounts:
                        - mountPath: /data
                          name: cfg
                  volumes:
                    - name: cfg
                      configMap:
                        name: event-exporter-cfg
              selector:
                matchLabels:
                  app: event-exporter
                  version: v1

    ``` shell
    kubectl apply -f docs/03-staging/assets/manifests/event-exporter-deployment.yaml
    ```

## Viewing events in Grafana

If the installation went well and no errors were reported you should start seeing event start to flow in Grafana.

1. Connect to `Grafana` (using default credentials: `admin/prom-operator`) by port forwarding to local machine:

    ```shell
    kubectl --namespace monitoring port-forward svc/kube-prom-stack-grafana 3000:80
    ```

2. Open a web browser on [localhost:3000](http://localhost:3000). Once in, you can go to `Explore` menu and select the `Loki` as a datasource.

3. In the `Log browser` input enter the following:

    ```json
    {app="event-exporter"}
    ```

    !!! info
        You should see events in the `Logs` section.
        Any of the fields in the `Detected fields` section of a log detail view can be used to query. For example you can perform a query using the pod name and view specific logs for a certain pod: `{app="event-exporter"} |= "shippingservice-79bdd5f858-gqm6g"`.

    ![loki kubernetes events](loki_kubernetes_events.png)

For a more in depth explanation on the `Obervability` topic you can check out the [Kubernetes Starter Kit Tutorial](https://github.com/digitalocean/Kubernetes-Starter-Kit-Developers).

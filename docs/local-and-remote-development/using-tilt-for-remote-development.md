# Using Tilt for remote development

This section will show you how to do remote development using `Tilt`.
You will install the `microservices-demo` application on your remote development environment using `Tilt`.
This section assumes that you already installed `Tilt` in the [Installing Required Tools](installing-required-tools.md) sction, [DOCR](setting-up-a-digital-ocean-container-registry.md) and [DOKS](setting-up-a-digital-ocean-kubernetes-cluster.md) configured and [tested](testing-the-setup.md).

## Prerequisites

To complete this section you will need:

1. [Ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/#quick-start) installed.
2. [Cert-manager](https://cert-manager.io/docs/installation/helm/) installed.
3. A valid domain available configured to point to DigitalOcean name servers. More information in this [article](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars). Digital Ocean is not a domain registrar so you will need to purchase that from another vendor.
4. The valid domain added to DigitalOcean. From the command line:

    ```shell
    doctl compute domain create <YOUR_DOMAIN_NAME>
    ```

    !!! info
        You will use this domain to create aditional sub-domains to use with the microservices app you will deploy in this section. The name of the domain needs to match the domain you configured to point to DigitalOcean's nameservers.
5. Create a sub-domain for your domain:

    ```shell
    LOAD_BALANCER_IP=$(doctl compute load-balancer list --format IP --no-header)

    doctl compute domain records create <YOUR_DOMAIN_NAME> --record-type "A" --record-name <YOUR_RECORD_NAME> --record-data "$LOAD_BALANCER_IP" --record-ttl "30"
    ```

## Remote development with Tilt

1. Clone the [sample-apps-repository](https://github.com/digitalocean/kubernetes-sample-apps).

    ```shell
    git clone https://github.com/digitalocean/kubernetes-sample-apps.git
    ```

2. Change directory to the `microservices-demo` folder:

    ```shell
    cd kubernetes-sample-apps/microservices-demo
    ```

3. Switch your current `Kuberenetes` config to your current config in the `Tiltfile-dev`:

    ```code
    ...
    allow_k8s_contexts("<YOUR_REMOTE_DEV_CLUSTER_CONTEXT_HERE>")
    ...
    ```

4. Edit the `pat.env` file under the `configs/do-token` and set it to your DigitalOcean access token:

    ```code
    access_token=<DO_ACCESS_TOKEN>
    ```

5. Edit the `wildcard-certificate.yaml` file under the `/kustomize/dev/frontend` folder and change all of the placeholders to the created and configured domain.

6. Edit the `wildcard-host.yaml` file under the `/kustomize/dev/frontend` folder and change all of the placeholders to the created and configured domain.

7. Edit the `wildcard-issuer.yaml` file under the `/kustomize/dev/frontend` folder and change all of the placeholders to a valid email address.

8. From the command line run the following:

    ```shell
    tilt up -f Tiltfile-dev
    ```

    You should see the following output:

    ```text
    Tilt started on http://localhost:10350/
    v0.30.7, built 2022-08-12

    (space) to open the browser
    (s) to stream logs (--stream=true)
    (t) to open legacy terminal mode (--legacy=true)
    (ctrl-c) to exit
    ```

9. Press the `Space` bar to open Tilt's UI.

    You should see the following:
    ![Tilt UI](tilt_ui.png)

    !!! note
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Titl is doing such as logs from all Kubernetes resources. This may take a few minutes.

10. Open a web browser and point to `<YOUR_RECORD_NAME>.<YOUR_DOMAIN_NAME>`. You should see the `microservices-demo` welcome page.

    You should see the following:

    ![microservices-demo landing page](microservices_demo_remote_development.png)

    !!! info
        In the above image you can see that the `frontend` service is served through a valid domain name via the `dev` subdomain. It is also using valid TLS/SSL certificates.

## Introduction

This section will show you how to do remote development using [Tilt](https://tilt.dev/). Tilt eases remote development by taking away the pain of time consuming Docker builds, watching files, and bringing environments up to date.

You will install the `microservices-demo` application on your remote development environment using `Tilt`. This section assumes that you already installed `Tilt` in the [Installing Required Tools](installing-required-tools.md) section, [DOCR](setup-docr.md), and [DOKS](setup-doks.md) configured.

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
        You will use this domain to create additional sub-domains to use with the microservices app you will deploy in this section. The name of the domain needs to match the domain you configured to point to DigitalOcean's nameservers.

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

3. Switch your current `Kubernetes` config to your current config in the `Tiltfile-dev`:

    ```code
    ...
    allow_k8s_contexts("<YOUR_REMOTE_DEV_CLUSTER_CONTEXT_HERE>")
    ...
    ```

4. Edit the `pat.env` file under the `configs/do` and set it to your DigitalOcean access token:

    ```code
    access_token=<DO_ACCESS_TOKEN>
    ```

5. Edit the `wildcard-certificate.yaml` file under the `/kustomize/dev/frontend` folder and change all of the placeholders to the created and configured domain.

6. Edit the `wildcard-host.yaml` file under the `/kustomize/dev/frontend` folder and change all of the placeholders to the created and configured domain.

7. Edit the `wildcard-issuer.yaml` file under the `/kustomize/dev/frontend` folder and change all of the placeholders to a valid email address.

8. All microservices Docker images are built on your local machine, and then pushed to your DOCR registry. A registry login is required first using `doctl`:

    ```shell
    doctl registry login
    ```

9. From the command line run the following:

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

10. Press the `Space` bar to open Tilt's UI.

    ![Tilt UI](tilt_ui.png)

    !!! note
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Tilt is doing such as logs from all Kubernetes resources. This may take a few minutes.

11. Open a web browser and point to `<YOUR_RECORD_NAME>.<YOUR_DOMAIN_NAME>`. You should see the `microservices-demo` welcome page.

    ![microservices-demo landing page](microservices_demo_remote_development.png)

    !!! info
        In the above image you can see that the `frontend` service is served through a valid domain name via the `dev` subdomain. It is also using valid TLS/SSL certificates.

## Live Updates with Tilt

Tilt has the ability to reload and rebuild resources at the right time. Every code change will require tilt to rebuild and push (if using Tilt against a remote Kubernetes cluster) docker images and roll out new versions of pods.

1. Navigate to your clone of the `kubernetes-sample-apps` (if not there already) and go to the `src/frontend/templates` folder under the `microservices-demo` folder:

    ```shell
    cd microservices-demo/src/frontend/templates
    ```

2. Next, edit the [home.html](https://raw.githubusercontent.com/digitalocean/kubernetes-sample-apps/master/microservices-demo/src/frontend/templates/home.html) file, and change some of the `h3` tags to something different:

    ```code
    ...
    <div class="col-12">
        <h3>On Sale Now</h3>
    </div>
    });
    ```

3. Navigate to `Tilt`'s detailed view on its UI. You should see that the `frontend` resource is being rebuilt. The updated `docker image` will be pushed to DOCR.
4. Open a web browser and point to `<YOUR_RECORD_NAME>.<YOUR_DOMAIN_NAME>`. You should see the `microservices-demo` welcome page updated with your changes.

    ![microservices-demo updated page](microservices_demo_updated_page.png)

    !!! info
        Due to browser cache the changes might not appear immediately and for this reason you can `hard refresh` your browser to see the changes. On modern browsers this can be achieved by pressing `Command` + `Shift` + `R` on macOS, and `Ctrl` + `Shift` + `R` for Linux systems.

## Introduction

This section will show you how to do remote development using [Tilt](https://tilt.dev/). It is very similar to the local development guide, the only difference being you will work directly on the remote Kubernetes cluster created in the [Set up DOKS](setup-doks.md) section. Application changes and reloading will happen as well on the remote development cluster.

Next, you will use Tilt to deploy the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) application on your remote Kubernetes cluster used as a development environment.

## Prerequisites

To complete this section you will need:

1. Tilt already installed and working as explained in the [Installing Required Tools](installing-required-tools.md) section.
2. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.
3. A Kubernetes cluster (DOKS) up and running as explained in the [Set up DOKS](setup-doks.md) section.

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

4. All microservices Docker images are built on your local machine, and then pushed to your DOCR registry. A registry login is required first using `doctl`:

    ```shell
    doctl registry login
    ```

5. From the command line run the following:

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

6. Press the `Space` bar to open Tilt's UI.

    ![Tilt UI](tilt_ui.png)

    !!! note
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Tilt is doing such as logs from all Kubernetes resources. This may take a few minutes.

7. Open a web browser and point to [localhost:9000](http://localhost:9000/). You should see the `microservices-demo` welcome page:

    ![microservices-demo landing page](microservices_demo_landing_page.png)

    !!! note
        Although you open a connection to localhost in your web browser, traffic is forwarded to the remote development cluster by Tilt.

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
4. Open a web browser and point to [localhost:9000](http://localhost:9000/). You should see the `microservices-demo` welcome page updated with your changes:

    ![microservices-demo updated page](microservices_demo_updated_page.png)

    !!! info
        Due to browser cache the changes might not appear immediately and for this reason you can `hard refresh` your browser to see the changes. On modern browsers this can be achieved by pressing `Command` + `Shift` + `R` on macOS, and `Ctrl` + `Shift` + `R` for Linux systems.

Next, you will learn how to deploy and configure the Nginx ingress controller for your development cluster (DOKS) to expose microservices to the outside world. You will also learn how to set up [cert-manager](https://cert-manager.io/) to automatically issue valid TLS certificates for your applications.

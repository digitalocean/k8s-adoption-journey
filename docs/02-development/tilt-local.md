## Introduction

This section will show you how to do local development using [Tilt](https://tilt.dev/). Tilt eases local development by taking away the pain of time consuming Docker builds, watching files, and bringing environments up to date.

You will install the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) application on your local environment using [Docker Desktop](https://www.docker.com/products/docker-desktop/) and Tilt.

## Prerequisites

1. Tilt already installed and working as explained in the [Installing Required Tools -> Tilt](installing-required-tools.md#installing-tilt) section.
2. Docker desktop already installed and working as explained in the [Installing Required Tools -> Docker Desktop](installing-required-tools.md#installing-docker-desktop) section.

## Local development with Tilt

1. Clone the [kubernetes-sample-apps](https://github.com/digitalocean/kubernetes-sample-apps).

    ```shell
    git clone https://github.com/digitalocean/kubernetes-sample-apps.git
    ```

2. Change directory to the `microservices-demo` folder:

    ```shell
    cd kubernetes-sample-apps/microservices-demo
    ```

3. Switch your current `Kuberenetes` config to `docker-desktop`:

    ```shell
    kubectl config use-context docker-desktop 
    ```

    !!! note
        This is required for local development as Tilt can be ran against a remote Kubernetes cluster and you can accidentally do unwanted changes to it.

4. From the command line run the following:

    ```shell
    tilt up
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

5. Press the `Space` bar to open Tilt's UI.

    You should see the following:
    ![Tilt UI](tilt_ui.png)

    !!! note
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Tilt is doing such as logs from all Kubernetes resources.

6. Open a web browser and point to [localhost:9000](http://localhost:9000/). You should see the `microservices-demo` welcome page:

    ![microservices-demo landing page](microservices_demo_landing_page.png)

## Live Updates with Tilt

Tilt has the ability to reload and rebuild resources at the right time. Every code change will require tilt to rebuild and push (if using Tilt against a remote Kubernetes cluster) docker images and roll out new versions of pods.

1. Navigate to your clone of the `kubernetes-sample-apps` (if not there already) and go to the `src/frontend/templates` folder under the `microservices-demo` folder:

    ```shell
    cd microservices-demo/src/frontend/templates
    ```

2. Next, edit the [home.html](https://raw.githubusercontent.com/digitalocean/kubernetes-sample-apps/master/microservices-demo/src/frontend/templates/home.html) file, and change one of the `h3` tags to something different:

    ```code
    ...
    <div class="col-12">
        <h3>On Sale Now</h3>
    </div>
    });
    ```

3. Navigate to `Tilt`'s detailed view on its UI. You should see that the `frontend` resource is being rebuilt.
4. Open a web browser and point to [localhost:9000](http://localhost:9000/). You should see the updated `microservices-demo` welcome page with your changes:

    ![microservices-demo updated page](microservices_demo_updated_page.png)

    !!! info
        Due to browser cache the changes might not appear immediately and for this reason you can `hard refresh` your browser to see the changes. On modern browsers this can be achieved by pressing `Command` + `Shift` + `R` on macOS, and `Ctrl` + `Shift` + `R` for Linux systems.

Next, you will learn how to perform remote development for the same set of microservices, using the Kubernetes environment created at the beginning of this chapter.

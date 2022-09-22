# Using Tilt

This section will show you how to do local development using `Tilt`.
You will install the `microservices-demo` application on your local environment using `docker-desktop` and tilt.
This section assumes that you already installed `Tilt` in the [Installing Required Tools](installing-required-tools.md) section.

## Local development with Tilt

1. Clone the [sample-apps-repository](https://github.com/digitalocean/kubernetes-sample-apps).

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
        This is required for local development as Titl can be ran against a remote Kubernetes cluster and you can accidentaly do unwanted changes to it.

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
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Titl is doing such as logs from all Kubernetes resources.

6. Open a web browser and point to [localhost:9000](http://localhost:9000/). You should see the `microservices-demo` welcome page.

    You should see the following:

    ![microservices-demo landing page](microservices_demo_landing_page.png)

## Live Updates with Tilt

Tilt has the ability to reload and rebuild resources at the right time. Every code change will require tilt to rebuild and push (if using Tilt agains a remote Kubernetes cluster) docker images and roll out new versions of pods.

1. Navigate to your clone of the `kuberentes-sample-apps` (if not there already) and go to the `src/frontend/templates` folder under the `microservices-demo` folder:

    ```shell
    cd microservices-demo/src/frontend/templates
    ```

2. Next, edit the `home.html` [file](https://raw.githubusercontent.com/digitalocean/kubernetes-sample-apps/master/microservices-demo/src/frontend/templates/home.html) and change its `h3` to something different:

    ```code
    ...
    <div class="col-12">
        <h3>On Sale Now</h3>
    </div>
    });
    ```

3. Navigate to `Tilt`'s detailed view on its UI. You should see that the `frontend` resource is being rebuilt.
4. Open a web browser and point to [localhost:9000](http://localhost:9000/). You should see the updated `microservices-demo` welcome page with your change:

    ![microservices-demo updated page](microservices_demo_updated_page.png)

    !!! info
        Due to browser cache the changes might not appear immediately and for this reason you can `hard refresh` your browser to see the changes. On modern browsers this can be achieved by pressing `Command` + `Shift` + `R` on macOS and `Ctrl` + `Shift` + `R` for Linux systems.

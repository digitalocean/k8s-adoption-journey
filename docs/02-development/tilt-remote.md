## Introduction

This section will show you how to do remote development using [Tilt](https://tilt.dev/). It is very similar to the local development guide, the only difference being you will work directly on the remote Kubernetes cluster created in the [Set up Development DOKS](setup-doks-dev.md) section. Application changes and reloading will happen on the fly on the remote development cluster as well.

Next, you will use Tilt to deploy the [online boutique](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) sample application to your development DOKS cluster.

The same approach based on Tilt [configuration profiles](https://docs.tilt.dev/tiltfile_config.html) is being used here as well. You only need to copy the environment specific configuration file (`tilt_config.json`) to your root project directory, and then run `tilt up`.

## Prerequisites

To complete this section you will need:

1. Tilt already installed and working as explained in the [Installing Required Tools](installing-required-tools.md) section.
2. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.
3. A development Kubernetes cluster (DOKS) up and running as explained in the [Set up Development DOKS](setup-doks-dev.md) section. You need to have proper permissions to create namespaces and deploy resources.
4. The `microservices-demo` GitHub repository already prepared as explained in the [Preparing demo application GitHub repository](preparing-demo-application.md) section.

## Remote development with Tilt

1. Clone your `microservices-demo` repository if you haven't already (make sure to replace the `<>` placeholders first):

    ```shell
    git clone https://github.com/<YOUR_GITHUB_ACCOUNT_USERNAME>/microservices-demo.git
    ```

2. Change directory to `microservices-demo` folder:

    ```shell
    cd microservices-demo
    ```

3. Switch current Kubernetes config to your `microservices-demo-dev` cluster. Bear in mind that the context is prefixed using the `do-<region_id>-` string (e.g. `do-nyc1-`):

    ```shell
    kubectl config use-context do-nyc1-microservices-demo-dev
    ```

4. All microservices Docker images are built on your local machine, and then pushed to your DOCR registry. A registry login is required first using `doctl`:

    ```shell
    doctl registry login
    ```

5. Within the current directory, copy the `dev profile` configuration for Tilt:

    ```shell
    cp tilt-resources/dev/tilt_config.json .
    ```

    !!! warn
        - Make sure to give a unique value for the `namespace` property in the `tilt_config.json` file to avoid overriding existing applications on the remote development cluster.
        - Tilt configuration files will be excluded from git commits by `.gitignore` settings. Each developer customizes his profile locally as desired, and should not impact other team members.

6. Bring the `microservices-demo` dev environment up using Tilt:

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

7. Press the `Space` bar to open Tilt's UI:

    ![Tilt UI](tilt_ui.png)

    !!! note
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Tilt is doing such as logs from all Kubernetes resources. This may take a few minutes.

8. Open a web browser and point to [localhost:9090](http://localhost:9090/). You should see the online boutique welcome page:

    ![online boutique landing page](microservices_demo_landing_page.png)

    !!! note
        Although you open a connection to localhost in your web browser, traffic is forwarded to the remote development cluster by Tilt.

## Live Updates with Tilt

Tilt has the ability to reload and rebuild resources at the right time. Every code change triggers Tilt to automatically rebuild local docker images, and roll out new versions of your application pods.

Follow steps below to watch Tilt doing live updates for your application:

1. Change directory to your local clone of the `microservices-demo` project directory (if not already). Then, open the `src/frontend/templates/home.html` file using a text editor of your choice (preferably with HTML lint support). For example, you can use [VS Code](https://code.visualstudio.com/):

    ```shell
    code src/frontend/templates/home.html
    ```

2. Next, change one of the `h3` tags to something different, such as:

    ```code
    ...
    <div class="col-12">
        <h3>On Sale Now</h3>
    </div>
    });
    ```

3. Navigate to `Tilt`'s detailed view using the web interface. You should see the `frontend` resource being rebuilt. The updated `docker image` will be pushed to your DOCR.
4. Finally, open a web browser and point to [localhost:9090](http://localhost:9090/). You should see the online boutique welcome page updated with your changes:

    ![online boutique updated page](microservices_demo_updated_page.png)

    !!! info
        Due to browser cache the changes might not appear immediately and for this reason you can `hard refresh` your browser to see the changes. On modern browsers this can be achieved by pressing `Command` + `Shift` + `R` on macOS, and `Ctrl` + `Shift` + `R` for Linux systems.

Next, you will learn how to deploy and configure the Nginx ingress controller for your development cluster (DOKS) to expose microservices to the outside world. You will also learn how to set up [cert-manager](https://cert-manager.io/) to automatically issue valid TLS certificates for your applications.

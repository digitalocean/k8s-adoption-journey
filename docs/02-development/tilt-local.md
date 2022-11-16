## Introduction

This section will show you how to do local development using [Tilt](https://tilt.dev/). Tilt eases local development by taking away the pain of time consuming Docker builds, watching files, and bringing environments up to date. The way Tilt works is based on a single Tiltfile present in your root project directory containing environment setup logic.

You will install the [online boutique](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) sample application on your local environment using [Docker Desktop](https://www.docker.com/products/docker-desktop/) and Tilt.

The way you will use Tilt in this guide is based on [configuration profiles](https://docs.tilt.dev/tiltfile_config.html). This approach has a major benefit - application logic is decoupled from configuration data. It means, you don't have to modify the base Tiltfile only if really required, or to add new functionality. Tilt automatically loads (if present) the configuration file (`tilt_config.json`), and sets up the environment for you.

Based on your current requirements or needs, you just pick the appropriate `tilt_config.json` file from the [tilt-resources](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo/tilt-resources/) directory, and copy it alongside main Tiltfile.

Below is an example of such setup:

```text
.
.
.
├── tilt-resources
│   ├── dev
│   │   └── tilt_config.json
│   └── local
│       └── tilt_config.json
├── Tiltfile
└── tilt_config.json
```

You need to copy only once the environment specific configuration file, and then run `tilt up` from the root directory of your project:

1. If you need a local environment setup - `cp tilt-resources/local/tilt_config.json <Tiltfile_directory>`. Then, run `tilt up`, and see it in action.
2. If you need a remote development setup - `cp tilt-resources/dev/tilt_config.json <Tiltfile_directory>`. Then, run `tilt up`, and see it in action.

## Prerequisites

To complete this section you will need:

1. Tilt already installed and working as explained in the [Installing Required Tools -> Tilt](installing-required-tools.md#installing-tilt) section.
2. Docker desktop already installed and running as explained in the [Installing Required Tools -> Docker Desktop](installing-required-tools.md#installing-docker-desktop) section.
3. The `microservices-demo` GitHub repository already prepared as explained in the [Preparing demo application GitHub repository](introduction-and-repository-setup.md) section.

## Local development with Tilt

1. Clone your `microservices-demo` repository if you haven't already (make sure to replace the `<>` placeholders first):

    ```shell
    git clone https://github.com/<YOUR_GITHUB_ACCOUNT_USERNAME>/microservices-demo.git
    ```

2. Change directory to `microservices-demo` folder:

    ```shell
    cd microservices-demo
    ```

3. Switch your current Kubernetes config to `docker-desktop`:

    ```shell
    kubectl config use-context docker-desktop 
    ```

    !!! note
        This is required for local development as Tilt can be ran against a production Kubernetes cluster for example, and you can accidentally perform unwanted changes.

4. Within the current directory, copy the `local profile` configuration for Tilt:

    ```shell
    cp tilt-resources/local/tilt_config.json .
    ```

    !!! note
        Tilt configuration files will be excluded from git commits by `.gitignore` settings. Each developer customizes his profile locally as desired, and should not impact other team members.

5. Bring the `microservices-demo` local environment up using Tilt:

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

6. Press the `Space` bar to open Tilt's UI:

    You should see the following:
    ![Tilt UI](tilt_ui.png)

    !!! note
        Please note that from the top left you can switch between `Table` and `Detail` view. `Detail` view offers a lot more information on what Tilt is doing such as logs from all Kubernetes resources.

7. Open a web browser and point to [localhost:9090](http://localhost:9090/). You should see the online boutique welcome page:

    ![online boutique landing page](microservices_demo_landing_page.png)

## Live Updates with Tilt

Tilt has the ability to reload and rebuild resources at the right time. Every code change triggers Tilt to automatically rebuild local docker images, and roll out new versions of your application pods.

Follow steps below to watch Tilt doing live updates for your application:

1. Change directory to your local clone of the `microservices-demo` project directory (if not already). Then, open the `src/frontend/templates/home.html` file using a text editor of your choice (preferably with HTML lint support). For example, you can use [VS Code](https://code.visualstudio.com/):

    ```shell
    code src/frontend/templates/home.html
    ```

2. Next, change one of the `h3` tags to something different, such as:

    ```html
    ...
    <div class="col-12">
        <h3>On Sale Now</h3>
    </div>
    });
    ```

3. Navigate to Tilt's detailed view using the web interface. You should see that the `frontend` resource is being rebuilt.
4. Finally, open a web browser and point to [localhost:9090](http://localhost:9090/). You should see the updated online boutique welcome page with your changes:

    ![online boutique updated page](microservices_demo_updated_page.png)

    !!! info
        Due to browser cache the changes might not appear immediately and for this reason you can `hard refresh` your browser to see the changes. On modern browsers this can be achieved by pressing `Command` + `Shift` + `R` on macOS, and `Ctrl` + `Shift` + `R` for Linux systems.

Next, you will learn how to perform remote development for the same set of microservices, using the Kubernetes environment created in the [Set up Development DOKS](setup-doks-dev.md) section.

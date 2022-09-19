# Testing the Setup

This section will show you how to quickly install a sample application to test that the setup works.
You will install the 2048 game application on your newly created Kubernetes cluster.

1. Clone the [sample-apps-repository](https://github.com/digitalocean/kubernetes-sample-apps).

    ```shell
    git clone https://github.com/digitalocean/kubernetes-sample-apps.git
    ```

2. Change directory to the `game-2048-example` folder.

    ```shell
    cd kubernetes-sample-apps
    ```

3. Build the `docker image`:

    ```shell
    docker build -t registry.digitalocean.com/<YOUR_DOCKER_REGISTRY_NAME_HERE>/2048-game .
    ```

4. Push the `docker image` to your `DOCR` repository:

    ```shell
    docker push registry.digitalocean.com/<YOUR_DOCKER_REGISTRY_NAME_HERE>/2048-game
    ```

    !!! note
        Please replace the **`<YOUR_REGISTRY_NAME_HERE>`** placeholder with the name of the `DOCR` you created in the [Setting up a Digital Ocean Container Registry (DOCR)](./setting-up-a-digital-ocean-container-registry.md) section.

5. Edit the game-2048 [deployment manifest](kustomize/resources/deployment.yaml) and replace the `<>` placeholders.
6. Deploy the application using the `kubectl kustomize` option (`-k` flag):

    ```shell
    kubectl apply -k game-2048-example/kustomize
    ```

7. Inspect all the resources in the `game-2048` namespace:

    ```shell
    kubectl get all -n game-2048
    ```

    You should see an output similar to the following:

    ```text
    NAME                            READY   STATUS    RESTARTS   AGE
    pod/game-2048-f96755947-dgj7z   1/1     Running   0          5m19s

    NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
    service/game-2048   ClusterIP   10.245.120.202   <none>        8080/TCP    5m21s

    NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/game-2048   1/1     1            1           5m22s

    NAME                                  DESIRED   CURRENT   READY   AGE
    replicaset.apps/game-2048-f96755947   1         1         1       5m22s
    ```

    !!! note
        Please note that you might need to wait for about a minute for everything to be ready.

8. Port-forward the `game-2048` service using kubectl:

    ```shell
    kubectl port-forward service/game-2048 -n game-2048 8080:8080
    ```

9. Open a web browser and point to [localhost:8080](http://localhost:8080/). You should see the `game-2048` welcome page.

!!! note
    If you are running an Mac with Apple chip, you will need to use `Buildx` to build a docker image for the `linux/amd64` as you may encounter issues if you try to run a docker image on an architecture that differs from the one it's been build on (arm/amd64 for example).
    Please see this [guide](https://github.com/docker/buildx#building-multi-platform-images) for more information.

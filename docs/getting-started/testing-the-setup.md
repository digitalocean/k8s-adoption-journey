# Testing the Setup

This section will show you how to quickly install a sample application to test that the setup works.
You will install the 2048 game application on your newly created Kubernetes cluster.

1. Clone the [sample-apps-repository](https://github.com/digitalocean/kubernetes-sample-apps).
2. Navigate to the `game-2048-example` folder.
3. Build the `docker image`:

    ```shell
    docker build -t registry.digitalocean.com/<YOUR_DOCKER_REGISTRY_NAME_HERE>/2048-game .
    ```

4. Push the `docker image` to your `DOCR` repository:

    ```shell
    docker push registry.digitalocean.com/<YOUR_DOCKER_REGISTRY_NAME_HERE>/2048-game
    ```

5. Edit the game-2048 [deployment manifest](kustomize/resources/deployment.yaml) and replace the `<>` placeholders.
6. Deploy the application using the `kubectl kustomize` option (`-k` flag):

    ```shell
    kubectl apply -k game-2048-example/kustomize
    ```

7. Inspect all the resources in the `game-2048` namespace:

    ```shell
    kubectl get all -n game-2048
    ```

8. Port-forward the `game-2048` service using kubectl:

    ```shell
    kubectl port-forward service/game-2048 -n game-2048 8080:8080
    ```

9. Open a web browser and point to [localhost:8080](http://localhost:8080/). You should see the `game-2048` welcome page.

!!! note
    If you are running an Mac with Apple chip, you will need to use `Buildx` to build a docker image for the `linux/amd64` as you may encounter issues if you try to run a docker image on an architecture that differs from the one it's been build on (arm/amd64 for example).
    Please see this [guide](https://github.com/docker/buildx#building-multi-platform-images) for more information.

# Testing the Setup

This section will show you how to quickly install a sample application to test that the setup works.
You will install the 2048 game application on your newly created Kubernetes cluster.

1. Clone the [sample-apps-repository](https://github.com/digitalocean/kubernetes-sample-apps)
2. Navigate to the `game-2048-example` and run the steps described in the repository's [README](https://github.com/digitalocean/kubernetes-sample-apps/blob/master/game-2048-example/README.md).

Running the instructions in the sample app repository step by step will validate that everything is working correctly. You should be able to deploy the `game-2048` application in your cluster using a docker image from your DOCR account.

**Note:**

If you are running an Mac with Apple chip, you will need to use `Buildx` to build a docker image for the `linux/amd64` as you may encounter issues if you try to run a docker image on an architecture that differs from the one it's been build on (arm/amd64 for example).
Please see this [guide](https://github.com/docker/buildx#building-multi-platform-images) for more information.

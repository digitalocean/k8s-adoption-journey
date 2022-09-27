## Introduction

In this section, you will learn how to use the Kubernetes-maintained [Nginx](https://kubernetes.github.io/ingress-nginx) Ingress Controller. Then, you're going to discover how to have `TLS` certificates automatically deployed and configured for your hosts (thus enabling `TLS` termination), and `route` traffic to your `backend` applications.

## Prerequisites

1. A container registry already set up as explained in the [Set up DOCR](setup-docr.md) section.
2. A Kubernetes cluster (DOKS) up and running as explained in the [Set up DOKS](setup-doks.md) section.
3. The microservices application deployed in your development cluster as explained in the [Tilt remote](tilt-remote.md) section.
4. A valid domain available configured to point to DigitalOcean name servers. More information in this [article](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars). Digital Ocean is not a domain registrar so you will need to purchase that from another vendor.

## Installing ingress nginx

1. Add the Ingress Nginx `Helm` repository:

    ```shell
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

    helm repo update ingress-nginx

    helm search repo ingress-nginx
    ```

2. Install the `Nginx Ingress Controller` using `Helm`:

    ```shell
    helm install ingress-nginx ingress-nginx/ingress-nginx --version 4.1.3 \
    --namespace ingress-nginx \
    --create-namespace  
    ```

    !!! note
        To check if the installation was succesfull you can run the `helm ls -n ingress-nginx` and confirm the deployment status.

3. Confiure DNS for Nginx Ingress Controller:

    ```shell
    doctl compute domain create <YOUR_DOMAIN_NAME>
    ```

    !!! info
        Please note that this domain matches the domain you purchased in the `Prerequisites` section. You will use this domain to create additional sub-domains to use with the microservices app you will deploy in this section.

4. Create an `A` record for your host:

    ```shell
    LOAD_BALANCER_IP=$(doctl compute load-balancer list --format IP --no-header)
    doctl compute domain records create <YOUR_DOMAIN_NAME> --record-type "A" --record-name <YOUR_RECORD_NAME> --record-data "$LOAD_BALANCER_IP" --record-ttl "30"
    ```

5. Add the `Jetstack` Helm repository:

    ```shell
    helm repo add jetstack https://charts.jetstack.io

    helm repo update jetstack
    ```

6. Install the `jetstack/cert-manager` chart using `Helm`:

    ```shell
    helm install cert-manager jetstack/cert-manager --version 1.8.0 \
    --namespace cert-manager \
    --create-namespace \
    --set installCRDs=true
    ```

    !!! note
        To check if the installation was succesfull you can run the `helm ls -n cert-manager` and confirm the deployment status.

7. Create a `Kubernetes Secret` for the [DigitalOcean Provider](https://cert-manager.io/docs/configuration/acme/dns01/digitalocean) that `cert-manager` is going to use to perform the `DNS-01` challenge using a `DigitalOcean API` token:

    ```shell
    DO_API_TOKEN="<YOUR_DO_API_TOKEN_HERE>"

    kubectl create secret generic "digitalocean-dns" \
        --namespace microservides-demo-dev \
        --from-literal=access-token="$DO_API_TOKEN"
    ```

    !!! note
        The secret must be created in the **same namespace** where the `Issuer` CRD is located in this case the `microservides-demo-dev` namespace.

8. Add the `Cert Manager` issuer using `kubectl` and the provided manifest file:

    ```shell
    kubectl apply -f assets/manifests/cert-manager-wildcard-issuer.yaml
    ```

    !!! info
        Make sure to replace the `<>` placeholders. Running `kubectl get issuer letsencrypt-nginx-wcard -n microservices-demo-dev` should result in the `True` value being displayed under the `READY` column.

    !!! note
        If the `Issuer` object displays a `Not Ready` state you can describe the object to get additional information using: `kubectl describe issuer letsencrypt-nginx-wcard -n microservices-demo-dev`.

9. Add the `Wildcard Certificates` using `kubectl` and the provided manifest file:

    ```shell
    kubectl apply -f assets/manifests/cert-manager-wildcard-certificate.yaml
    ```

    !!! info
    Make sure to replace the `<>` placeholders.

    To verify the certificate status run:

    ```shell
    kubectl get certificate starter-kit.online -n microservides-demo-dev
    ```

    !!! info
        This may take a few minutes to complete. If the `Certificate` object displays a `not ready state` you can run: `kubectl logs -l app=cert-manager,app.kubernetes.io/component=controller -n cert-manager`

10. Add the `Ingress Nginx` host using `kubectl` and the provided manifest file:

    ```shell
    kubectl apply -f assets/manifests/ingress-host.yaml 
    ```

    !!! info
        Make sure to replace the `<>` placeholders.

11. Open a web browser and point to `<YOUR_A_RECORD>.<YOUR_DOMAIN>`. You should see the online boutique welcome page. You should see that the connection is secure and the certificate is a valid one issued by [Let's Encrypt](https://letsencrypt.org).

    ![development environment online boutique](microservices_demo_ingress_dev.png)

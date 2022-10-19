## Introduction

In this section, you will learn how to install and configure the Kubernetes-maintained version of the [Nginx](https://kubernetes.github.io/ingress-ngin) Ingress Controller. Then, you're going to discover how to automatically issue TLS certificates for your hosts (thus enabling TLS termination), and route traffic to your backend applications.

## Prerequisites

To complete this section you will need:

1. Helm installed as explained in the [Installing required tools](installing-required-tools.md) section.
2. A Kubernetes cluster (DOKS) up and running as explained in the [Set up DOKS](setup-doks-dev.md) section.
3. The online boutique sample application deployed to your cluster as explained in the [Tilt remote development](tilt-remote.md) section.
4. A valid domain available and configured to point to DigitalOcean name servers. More information is available in this [article](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars). Digital Ocean is not a domain registrar, so you will need to purchase the domain from a well known vendor, such as GoDaddy.

## Installing the Nginx Ingress Controller

In this section you will install the community maintained version of the Nginx ingress controller. Please follow below steps to install Nginx using Helm:

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
        To check if the installation was successful, run the `helm ls -n ingress-nginx` command, and confirm the deployment status.

3. Configure DNS for Nginx Ingress Controller:

    ```shell
    doctl compute domain create <YOUR_DOMAIN_NAME>
    ```

    !!! info
        Please note that this domain matches the domain you purchased in the [Prerequisites](#prerequisites) section. You will use this domain to create additional sub-domains to use with the microservices app you will deploy in this section.

4. Create an `A` record for your host:

    ```shell
    LOAD_BALANCER_IP=$(doctl compute load-balancer list --format IP --no-header)
    doctl compute domain records create <YOUR_DOMAIN_NAME> \
        --record-type "A" --record-name <YOUR_RECORD_NAME> \
        --record-data "$LOAD_BALANCER_IP" \
        --record-ttl "30"
    ```

    !!! info
        The upper mentioned command works if you have only one LB in your DO account. If you have multiple LBs you will need to add the its IP in the command.

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
        --namespace microservices-demo-dev \
        --from-literal=access-token="$DO_API_TOKEN"
    ```

    !!! note
        The secret must be created in the **same namespace** where the `Issuer` CRD is located - in this case the `microservides-demo-dev` namespace.

8. Create an `issuer` resource for cert-manager using `kubectl` (make sure to replace the <> placeholders first):

    The `issuer` manifest file looks like the following:

    ??? note "Click to expand `issuer` manifest file"
        ```yaml
        apiVersion: cert-manager.io/v1
        kind: Issuer
        metadata:
        name: letsencrypt-nginx-wcard
        namespace: microservices-demo-dev
        spec:
        # ACME issuer configuration:
        # `email` - the email address to be associated with the ACME account (make sure it's a valid one).
        # `server` - the URL used to access the ACME server’s directory endpoint.
        # `privateKeySecretRef` - Kubernetes Secret to store the automatically generated ACME account private key.
        acme:
            email: <YOUR_EMAIL_ADDRESS>
            server: https://acme-v02.api.letsencrypt.org/directory
            privateKeySecretRef:
            name: letsencrypt-nginx-wcard-private
            # List of challenge solvers that will be used to solve ACME challenges for the matching domains.
            solvers:
            # Use the DigitalOcean DNS API to manage DNS01 challenge records.
            - dns01:
                digitalocean:
                    # Kubernetes secret that contains the DO API token .
                    # Must be in the same namespace as the Issuer CRD.
                    tokenSecretRef:
                    name: digitalocean-dns
                    key: access-token
        ```

    Apply via kubectl:

    ```shell
    kubectl apply -f docs/03-development/assets/manifests/cert-manager-wildcard-issuer.yaml
    ```

    !!! info
    Running `kubectl get issuer letsencrypt-nginx-wcard -n microservices-demo-dev` should result in the `True` value being displayed under the `READY` column.

    !!! note
        If the `Issuer` object displays a `Not Ready` state you can describe the object to get additional information using: `kubectl describe issuer letsencrypt-nginx-wcard -n microservices-demo-dev` to get more information.

9. Create the `wildcard certificates` resource using `kubectl` and the provided manifest file (make sure to replace the <> placeholders first):

    The `certificate` manifest file looks like the following:

    ??? note "Click to expland the `certificate` resource"
        ```yaml
        apiVersion: cert-manager.io/v1
        kind: Certificate
        metadata:
        name: <YOUR_DOMAIN_NAME>
        # Cert-Manager will put the resulting Secret in the same Kubernetes namespace as the Certificate.
        namespace: microservices-demo-dev
        spec:
        # Secret name to create, where the private key and certificate should be stored.
        secretName: <YOUR_DOMAIN_NAME>
        # What Issuer to use for getting the certificate.
        issuerRef:
            name: letsencrypt-nginx-wcard
            kind: Issuer
            group: cert-manager.io
        # Common name to be used on the Certificate.
        commonName: "*.<YOUR_DOMAIN_NAME>"
        # List of DNS subjectAltNames to be set on the Certificate.
        dnsNames:
            - "<YOUR_DOMAIN_NAME>"
            - "*.<YOUR_DOMAIN_NAME>"
        ```

    Apply via kubectl:

    ```shell
    kubectl apply -f docs/03-development/assets/manifests/cert-manager-wildcard-certificate.yaml
    ```

    To verify the certificate status run:

    ```shell
    kubectl get certificate <YOUR_DOMAIN_NAME> -n microservices-demo-dev
    ```

    !!! info
        This may take a few minutes to complete. If the `Certificate` object displays a `not ready state` you can run: `kubectl logs -l app=cert-manager,app.kubernetes.io/component=controller -n cert-manager`

10. Add the `Ingress Nginx` host using `kubectl` and the provided manifest file (make sure to replace the <> placeholders first):

    The `ingress host` manifest file looks like the following:

    ??? note "Click to expand the `ingress host` resource"
        ```yaml
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
        name: ingress-microservices-demo-dev
        namespace: microservices-demo-dev
        spec:
        tls:
            - hosts:
                - "*.<YOUR_DOMAIN_NAME>"
            secretName: <YOUR_DOMAIN_NAME>
        rules:
            - host: <YOUR_A_RECORD>.<YOUR_DOMAIN_NAME>
            http:
                paths:
                - path: /
                    pathType: Prefix
                    backend:
                    service:
                        name: frontend
                        port:
                        number: 80
        ingressClassName: nginx
        ```

    Apply via kubectl:

    ```shell
    kubectl apply -f docs/03-development/assets/manifests/ingress-host.yaml 
    ```

11. Open a web browser and point to `<YOUR_A_RECORD>.<YOUR_DOMAIN>`. You should see the online boutique welcome page. The connection is secure and the certificate is a valid one issued by [Let's Encrypt](https://letsencrypt.org).

    ![development environment online boutique](microservices_demo_ingress_dev.png)

Next, you will deploy the [Kubernetes Dashboard](https://github.com/kubernetes/dashboard) and [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server) to your cluster in order to visualize application and cluster related metrics, as well as corresponding logs and events.

Hands-on tutorial for going from day-1 to production on [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/).

## Welcome to Kubernetes Adoption Journey

The decision to adopt Kubernetes shouldn’t be taken lightly. It’s a complex system that requires hard work and dedication. In fact, when it comes to using Kubernetes, the best value comes from adopting a DevOps culture. Kubernetes isn’t just installing something on a virtual machine (VM), it’s a transformative way of viewing IT and enabling your teams. Automation is a direct path to becoming more productive. Kubernetes can make every aspect of your applications and tools accessible to automation, including role-based access controls, ports, databases, storage, networking, container builds, security scanning, and more. Kubernetes gives teams a well-documented and proven system that they can use to automate so that they can focus on outcomes.

Startups and small-to-medium-sized businesses (SMBs) are uniquely positioned in their journeys. Unlike enterprises, they typically don’t have dedicated departments for operations or security, and they usually run lean development teams. At the same time, SMBs are ultra-efficient, sometimes going from discovery phases to production in a matter of two or three weeks. When startups and SMBs consider adopting Kubernetes, they need to retain their ability to be flexible and pivot quickly while benefiting from the scalability and automation provided by Kubernetes. To achieve both without large and ongoing maintenance overhead, SMBs may consider the hands-free operations provided by Managed Kubernetes offerings.

In this guide, you’ll find recommendations for SMBs at any stage of the Kubernetes adoption journey. From Discovery and Development through Staging, Production, and ultimately Scale, we’ll offer a simple yet comprehensive approach to getting the most out of Kubernetes.

## Guide Overview

This guide will teach you to:

1. Install and configure **required tools** to build applications running on DigitalOcean Kubernetes.
2. Set up a [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/) development cluster (**DOKS**) for deploying and testing applications in the incipient stages of development.
3. Set up a [DigitalOcean Container Registry](https://docs.digitalocean.com/products/container-registry/) (**DOCR**) for storing application images used for deployment to each environment (dev, staging, prod).
4. Deploying a **sample application** consisting of several microservices (the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app).
5. Perform **local development** for the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app using [Tilt](https://tilt.dev/).
6. Set up a **development environment**, and perform remote development using Tilt.
7. Set up **staging** and **production** environments to build and deploy the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app to upper environments.
8. Set up **CI/CD workflows** using GitHub Actions to build and deploy the [microservices-demo](https://github.com/digitalocean/kubernetes-sample-apps/tree/master/microservices-demo) app to each environment after a code change (PR merge).
9. Set up **observability** for each environment - logging, monitoring, alerting, etc.
10. Automatically **scale application workloads** on demand.

Please proceed with the [Getting started -> Installing required tools](installing-required-tools.md) section.

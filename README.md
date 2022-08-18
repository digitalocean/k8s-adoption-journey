# k8s-adoption-journey
Hands-on tutorial for going from day-1 to production on DigitalOcean Kubernetes. Goes with "kubernetes adoption journey" document.


Sections:
1/ Setup [Cristian]
- Set up DOKS cluster, DOCR registry, Bookinfo sample app using CLI.
- Set up the client tools - kubectl, helm3, k9s, ...

2/ Development [Bogdan]
- Install tilt. Modify source code locally for a python file of the bookinfo app. Show both options where Tilt automatically updates via registry, vs. hot reload the container.

3/ CI/CD Setup [Cristian]
- Create a staging and a prod cluster.
- Install argocd.
- Create a fork of bookinfo.
- Using caching feature offered by github to optimize the build.
- Add a few sample tests as part of the bookinfo CI.
- Use github actions to update bookinfo and push to registry, and update the staging manifests.
- Configure argocd to pickup the updated image from the registry and deploy to staging.
- Create a PR for prod manifest. Approve the PR.
- Show the update failing for some reason, show how to revert to the previous version.

4/ Production 
- Set up monitoring, logging, alerting (Bogan)
- Set up velero (Cristian)

5/ Scaling [Bogdan]
- Send lots of traffic to the bookinfo app. Observe the metrics.
- Set up HPA for certain pods to address the traffic load.

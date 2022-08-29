# k8s-adoption-journey
Hands-on tutorial for going from day-1 to production on DigitalOcean Kubernetes. Goes with "kubernetes adoption journey" document.


Sections:
1/ Setup 
- Set up DOKS cluster, DOCR registry, ...
- Set up the client tools - kubectl, helm3, k9s, ...
- Install 2 apps: Bookinfo, and wordpress. We will use the wordpress site as a blog post for BookInfo App. 

2/ Development 
- Install tilt. Modify source code locally for a python file of the bookinfo app. Show both options where Tilt automatically updates via registry, vs. hot reload the container.


3/ CI/CD Setup
- Create 1 staging and 2 prod clusters.
- Install argocd.
- Set up the Git repository structure for bookinfo and wordpress to deploy to the staging and prod environments.
- Use external secrets operator - combine with a vault install on a standalone droplet. 
- Verify the argo CD is able to install the apps.
- CI pipeline
  - Use caching feature offered by github to optimize the build.
  - Add a few sample tests as part of the bookinfo CI.
  - Use github actions to update bookinfo and push to registry, and update the staging manifests.
  - Configure argocd to pickup the updated image from the registry and deploy to staging.
- Create a PR for prod manifest. Approve the PR.
- Show the update failing for some reason, show how to revert to the previous version.

4/ Production 
- Set up ingress, monitoring, logging, alerting 
- Add Snyk to CI pipeline and registry scanning. 

5/ Scaling
- Send lots of traffic to the bookinfo app. Observe the metrics.
- Set up HPA for certain pods to address the traffic load.
- TBD

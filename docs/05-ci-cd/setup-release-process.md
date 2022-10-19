!!!warning
    **NOT FINISHED YET - WORK IN PROGRESS!!!**

## Managing Application Releases

The release process is pretty straightforward, and it's based on semantic versioning:

1. `Semantic versioning` is used to distinguish between each release. First version starts at `v1.0.0`.
2. For each release the `version is increased by a single value`.
3. For each release a corresponding `git tag` is created. Using tags helps verify changes introduced by a specific version in time. Also, in case something goes bad you can rebuild the assets at that point in time.
4. A dedicated workflow runs for tag events which builds and pushes the project docker images using release tag version.

Releasing a new version for a project is a separate process, and it is usually triggered manually. GitHub offers the possibility to create and manage releases via the web interface in a very straightforward manner.

Releasing a new version for the online boutique sample application consists of:

1. Creating a new GitHub release:
   - Use tagging based on semantic versioning (e.g. v1.0.0)
   - Generate release changelog
2. Automatically trigger a release GitHub workflow which does the following:
   - Checks the latest release tag and corresponding version
   - Builds and tags images for the affected microservice(s)
   - Pushes release artifacts to registry (docker images)

## Promoting to Upper Environments

It's not best practice to immediately deploy to production after a new release was made. You will want to deploy to staging environment first, then have QA team check and approve the release. If everything is ok, then you will move forward and deploy to production.

Promoting a new release to upper environments should happen in a controlled manner via PRs, and it is described below. Why use PRs? Because you can create atomic commits, and revert the same way in case something goes bad.

I. Promoting to staging environment:

- Prerequisites:

  1. A new GitHub release for the project was made.
  2. Release artifacts already published.

- Steps:

  1. Create a new PR with Kustomize changes for the staging overlay. New release tag is included in the images section.
  2. A Kustomize validation workflow is automatically triggered.
  3. Manual review is also required.
  4. If all checks pass, PR is closed, and code merged in the main branch.
  5. ArgoCD picks the changes and deploys new application artifacts to staging environment.

II. Promoting to production environment:

- Prerequisites:

  1. A new GitHub release for the project was made.
  2. Release artifacts already published.
  3. Application was already tested and QA team approved it for staging environment.

- Steps:

  1. Create a new PR with Kustomize changes for the prod overlay. New release tag is included in the images section.
  2. A Kustomize validation workflow is automatically triggered.
  3. Manual review is also required.
  4. If all hecks pass, PR is closed, and code merged in the main branch.
  5. ArgoCD picks the changes and deploys new application artifacts to prod environment.

## Rolling Back a Release

In case something goes bad, you can immediately revert the associated PR for the respective environment. This approach ensures atomic changes and rollbacks. Next, ArgoCD will pick the changes automatically and rolls back to previous deployment.

## Other Concerns

1. Application configuration drift issues ?

    - Reasoning:
        Everything is tracked via the main branch which is constantly being developed. How can we ensure application configuration stays immutable? The affected part is Kustomize.

    - Possible solution:
        Use Git tags. Then, point ArgoCD to use a release tag.

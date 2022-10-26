## Introduction

It's not best practice to immediately deploy to production after a new release was made. You will want to deploy to staging environment first, then have QA team check and approve the release. If everything is ok, then you will move forward and deploy to production.

Promoting a new release to upper environments should happen in a controlled manner via PRs, and it is described below. Why use PRs? Because you can create atomic commits, and revert the same way in case something goes bad.

## Promoting to Staging Environment

!!! note
    This part is automated in this guide. But, if you want to disable automated deployments of project releases to staging environment, you will find required manual steps below.

**Prerequisites:**

1. A new GitHub release for the project was made.
2. Release artifacts already published.

**Steps:**

1. Create a new PR with Kustomize changes for the staging overlay. New release tag is included in the images section.
2. A Kustomize validation workflow is automatically triggered.
3. Manual review is also required.
4. If all checks pass, PR is closed, and code merged in the main branch.
5. Argo CD picks the changes, and deploys new application artifacts to staging environment.

## Promoting to Production Environment

**Prerequisites:**

1. A new GitHub release for your project is made.
2. Release artifacts already published.
3. Application was already tested and QA team approved it for staging environment.

**Steps:**

1. Create a new PR with Kustomize changes for the prod overlay. New release tag is included in the images section.
2. A Kustomize validation workflow is automatically triggered.
3. Manual review is also required.
4. If all checks pass, PR is closed, and code merged in the main branch.
5. ArgoCD picks the changes and deploys new application artifacts to prod environment.

## Rollback Releases

In case something goes bad, you can immediately revert the associated PR for the respective environment. This approach ensures atomic changes and rollbacks. Next, Argo CD picks the changes automatically and rolls back to previous deployment.

Essentially, you follow the same procedure as learned in previous chapters - e.g. [Set up continuous deployments -> Reverting bad application deployments](setup-continuous-deployments.md#reverting-bad-application-deployments).

Another approach is to use the [Argo CD application rollback](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_rollback/) feature. You should be able to revert to any previous git commit ID. It offers a fast approach to rollback application changes. Meanwhile you will work on a fix, and when ready deploy a new release.

Just bear in mind that during the rollback process changes are performed only on the Argo CD server - your Git repository remains untouched. As a consequence, the affected Argo application is not in sync anymore with latest state of your Git repository. This is something desired, until you come up with a fix (or set of fixes) for the bad release. The affected Argo application will be synced again automatically when you perform the next release.

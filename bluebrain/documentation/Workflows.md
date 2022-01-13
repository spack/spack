# Workflows

## Redeployment of a Stage

As the number of different versions of software in a stage grows, it may be
beneficial to redeploy stages into a new directory to keep the Spack
database lean and fast to query.

To redeploy a stage and all its dependents, visit our
[Deployment Jenkins Overview](https://bbpcode.epfl.ch/ci/blue/organizations/jenkins/hpc.spack-deployment/activity/),
and click the button labelled "Run".
The following dialog should appear:

![Redeployment Dialog for "Run" in Jenkins](images/redeploy.png "Redeployment Dialog")

Ensure that the following items are changed:

* The checkbox `REDEPLOY` should be checked.

  This will deploy into the specified folder (see next item), and after
  successful deployment reset the `latest` symlink to said folder.
  Future deployment runs will then use the new deployment by default.

* The date field should have `latest` replaced with an actual date like
  `2020-04-01`.

  The deployment resolves the symlink `latest` to the last redeployment.
  If this field is not set to an actual date, no new deployment will be
  created, but the latest deployment will be updated.

* Select the appropriate stage to redeploy.

  Note that the content of the earlier stages, e.g., `compilers`, `tools`,
  evolves only slowly, and redeployment should only be done infrequent.

## Updating with a new Upstream Spack

### Initial Merge

Merge the most recent release branch into our `develop`, i.e., upstream's
`release/v0.15`.  Resolve merge conflicts by consulting vanilla checkouts
of our own `develop` and upstream's release branch.

Before building the merged branch, the following steps should be taken:

* Update the compilers where necessary! This involves updating the
  following files:
  * `deploy/configs/packages.yaml` (compiler preferences at the end of the
    file)
  * `deploy/packages/compilers.yaml`
  * `deploy/packages/toolchains.yaml`

* Update the Python version, if desired. This will affect the following
  files:
  * `deploy/packages/toolchains.yaml`
  * `deploy/packages/external-libraries.yaml`
  * `deploy/packages/python-packages.yaml`

* Grep through the files in the `deploy` directory to ensure that no old
  compiler or Python versions are referenced anywhere!

* **Temporarily** modify the `deploy/Jenkinsfile` to build the right branch
  into a new directory:
  * The function `deployment_directory` can be modified to return a
    temporary deployment root.
  * The default value for the branch/`sha1` to build should be modified to
    point to the merged branch instead of `develop`.
  * The pipeline steps to check out Spack should be modified to grab the
    merged branch instead of `develop`.

### Building the Merged Deployment

Copy the mirror data for proprietary tarballs into the new deployment root.
Otherwise, the building of PGI may fail, and Intel® compilers will take a
long time to download.

Create a new Jenkins plan to build the merged branch. Customarily,
`hpc.spack-deployment-clone` may still be around; if this is not the case,
ask Core Services to clone the `hpc.spack-deployment` plan. In the
configuration of the plan, make sure that the "Pipeline" configuration
setting "Branches to build" is updated to the merged branch.

Said plan may now be triggered, any build failure should be resolved. Use
the `pull_env.sh` script to investigate failures locally, e.g. with the
following command if the merged branch is built into a directory called
`merge` under the current Jenkins plan root:

    $ eval $(spack/deploy/pull_env.sh merge compilers)

The above command will attempt to re-create an environment very similar
(*note:* **not identical**) to what `bbprelman` uses when building within
Jenkins. Within this environment, one can reproduce the commands used in
`deploy/deploy.lib` to handle the build, e.g.:

    $ spack spec -I $(<$HOME/specs.txt)

The directory created (equivalent to `${HOME}` in the modified shell)
should be deleted once investigations are concluded.

### Merging the new Deployment

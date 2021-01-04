# Deploying software on BlueBrain5

Essential software used to build and simulate our brain models is deployed
centrally on BlueBrain5, as well as some utilities to facilitate easier
software development.

Modules should be available by default, and

    $ module avail

should list both `archive` modules and an `unstable` one, which will become
the next `archive` module available at the end of the month.

If no modules are available, the following will restore the setup:

    $ . /gpfs/bbp.cscs.ch/apps/hpc/jenkins/config/modules.sh

To update the version of any of these modules, first we have to make sure
that the corresponding software is built by edit the corresponding Spack
environment:

    $ nvim spack/deploy/environments/applications.yaml

The above environment definition provides the end-user software that is
developed by BlueBrain.
Version specifications are only required if the deployed version should be
static and not change with updates to the package file.

If there are dependencies used in a broader scope/by several software
packages, consider adding them to one of the following steps in the
deployment chain (all found in `spack/deploy/environments`):

* `libraries` for general purpose libraries, and dependencies that depend
  on MPI
* `externals` for packages that are rarely changed and for which
  the dependency graph may be truncated by Spack (e.g. Spark, Python) ­
  mainly dependencies for building

Following this, the software package may have to be whitelisted
in the module definition. I.e., for the `application` modules, the software
package should be listed without version information in:

    $ nvim spack/deploy/configs/applications/modules.yaml

Under a key `whitelist`.

Changes to either file should be committed and result in a pull request on
Github.
Jenkins will build the additional software required, with all output
available in a separate directory:

    $ ls /gpfs/bbp.cscs.ch/apps/hpc/jenkins/pulls/165
    config  deploy  mirror  spack

Software packages and modules should be updated upon pull request merge and
a nightly basis.
The `config` directory contains the same configuration files as the regular
deployment and can be used instead.

# Deploying software on BlueBrain5

## Modules on BlueBrain5

Essential software used to build and simulate our brain models is deployed
centrally on BlueBrain5, as well as some utilities to facilitate easier
software development.

Modules should be available by default, and

    $ module avail

should list both `archive` modules and an `unstable` one, which will become
the next `archive` module available at the end of the month.

If no modules are available, the following will restore the setup:

    $ . /gpfs/bbp.cscs.ch/apps/bsd/config/modules.sh

## Updating deployed software versions

To update the version of any of these modules, first we have to make sure
that the corresponding software is built by edit the corresponding Spack
environment:

    $ nvim ${SPACK_ROOT}/bluebrain/deployment/environments/applications_${team}.yaml

The above environment definition provides the end-user software that is
developed by BlueBrain, split by team.
Version specifications are only required if the deployed version should be
static and not change with updates to the package file.
Please ensure that:

* If a module is required, the list `spack:modules:tcl:whitelist` contains
  the name of the package (no version information required normally)
* The package name is listed under `spack:specs` with required variants or
  special dependencies.

If there are dependencies used in a broader scope/by several software
packages, consider adding them to one of the following steps in the
deployment chain (all found in
`${SPACK_ROOT}/bluebrain/deployment/environments`):

* `libraries` for general purpose libraries, and dependencies that depend
  on MPI
* `externals` for packages that are rarely changed and for which
  the dependency graph may be truncated by Spack (e.g. Spark, Python) ­
  mainly dependencies for building

Changes to any file should be committed and result in a pull request on
Github.

## Testing pull requests for updates

Jenkins will build the additional software required, with all output
available in a separate directory:

    $ ls /gpfs/bbp.cscs.ch/apps/bsd/pulls/12345
    config  deploy  mirror  spack

Software packages and modules should be updated upon pull request merge and
a nightly basis.
The `config` directory contains the same configuration files as the regular
deployment and can be used instead.
To test the pull request, clean the environment and source the
corresponding modules:

    $ module purge     # remove anything that may pollute the shell environment
    $ unset MODULEPATH # start with a clean slate, no interference
    $ . /gpfs/bbp.cscs.ch/apps/bsd/pulls/${MY_PULL_REQUEST_NUMBER}/config/modules.sh
    $ module load unstable
    $ module load ${SOFTWARE_I_JUST_UPDATED}

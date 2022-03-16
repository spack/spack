# Setup for BlueBrain5

On BlueBrain5, installing software and creating modules requires only the
Spack module:

    $ module load spack

To modify packages and update deployment related files,
clone this repository in addition.
The following commands are a good way to get started:

    $ module load spack unstable git
    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ . spack/share/spack/setup-env.sh

To be fully independent of the module, export the system configuration
path, and make sure that this is done every time before using Spack:

    $ export SPACK_SYSTEM_CONFIG_PATH=/gpfs/bbp.cscs.ch/ssd/apps/bsd/config
    $ export SPACK_USER_CACHE_PATH=$HOME/spack_install

Note that the `git clone` should be executed in a subdirectory of the home
directory on GPFS.
The project directories are backed by a slower GPFS setup, and using a
Spack installation from the project directories will result in a big
performance penalty.

## Customizing the Software Installation Directory

By loading the provided Spack module and sourcing the local Spack
installation **afterwards**,
software and modules will be installed into `${HOME}/spack_install`.

To customise this, use the following commands:

    $ spack config add config:install_tree:root:${HOME}/my_software
    $ spack config add config:module_roots:tcl:${HOME}/my_modules

## Generating Custom Modules

To generate a module for the package `my_package`,
modify the whitelist with the following command:

    $ spack config add "modules:tcl:whitelist:[my_package]"

And use

    $ spack module tcl refresh my_package

To generate or update the module.

### Automatically Generate Modules for all Installed Software

**Note that this may have unintended consequences and is not a supported configuration**.

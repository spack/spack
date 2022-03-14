# Setup for Personal Machines

In general, when following these instructions make sure that you satisfy
the following:

1. Old configuration is backed up, i.e., `~/.spack` moved out of the way
2. Spack is not sourced **anywhere** in the shell start-up scripts
3. Use a new clone to avoid configuration changes in the old checkout

## Prerequisites

### Building software on MacOS

To install end-user software on MacOS, please defer to `brew`.

Before starting, please install XCode and `brew` and make sure that there
is a working Python on your machine, preferably from XCode or another
*stable* source.
It is recommended to rebuild a Spack-based Python for utmost independence
and to minimize potential build problems for binary Python libraries.

If issues arise to find `stdio.h` correctly building software outside the
Spack stack, e.g., `neuron`, issue the following command if using a POSIX
shell:

    $ export SDKROOT=$(xcrun --sdk macosx --show-sdk-path)

Or set it in `fish`:

    $ set -x SDKROOT (xcrun --sdk macosx --show-sdk-path)

Then install a Fortran compiler, which Spack will pick up and use in
conjunction with Apple's CLang:

    $ brew install gcc

### Building software on Ubuntu

Ubuntu / Debian have a habit of being somewhat _special_, patching upstream
projects in unexpected ways.
Consider yourself warned to not rely on system packages and defer to
Spack-installed ones when needed.

First, ensure that the essential packages to building stuff are installed:

    $ sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    $ sudo apt update
    $ sudo apt install build-essential gcc-11 g++-11 gfortran-11

If Python 3 is not your default, tell Ubuntu to use a newer one, e.g.,
Python 3.8 by setting the default `python`:

    $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

To check that we are using Python 3 as `python`:

    $ sudo update-alternatives --config python
    There is only one alternative in link group python
    (providing /usr/bin/python): /usr/bin/python3.8. Nothing to configure.

## Spack Setup

Now clone our version of Spack and find compilers and external packages:

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find
    $ spack external find

### Additional Configuration

#### Remove Flawed External Packages

Use the following commands to remove software that may be too customized to
use reliably:

    $ spack config rm packages:hdf5
    $ spack config rm packages:openmpi
    $ spack config rm packages:python
    $ spack config rm packages:sqlite

### Tuning on MacOS

Edit the resulting externals, removing any references to `brew` from the
system, the latter two as they are unfit to be used as full dependencies
with Spack:

    $ spack config edit packages

With this minimal setup, Spack should operate independent of the system and
the `brew` installation.

### Tuning on Ubuntu

You may want to purge older GCCs from `~/.spack/linux/compilers.yaml` if
Spack implies older GCC by default.

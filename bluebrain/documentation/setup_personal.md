# Setup for Personal Machines

## Building software on OS X

To install end-user software on OS X, please defer to `brew`.

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

Now clone our version of Spack and find compilers and external packages:

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find
    $ spack external find

Edit the resulting externals, removing any references to `brew`, `python`,
and `sqlite` from the system, the latter two as they are unfit to be used
as full dependencies with Spack:

    $ spack config edit packages

With this minimal setup, Spack should operate independent of the system and
the `brew` installation.
Software installed via Spack should be accessed either with `spack load` or
by using Spack's environment feature.

## Building software on Ubuntu

Use Spack on the workstations provided by the project.

### Ubuntu 18.04

We build Docker images based on Ubuntu 18.04, and the same settings can be
used to set Spack up on the desktops:

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ mkdir ~/.spack
    $ cp spack/bluebrain/sysconfig/ubuntu-18.04/*.yaml ~/.spack
    $ sed -e 's/#.*//g' spack/bluebrain/sysconfig/ubuntu-18.04/packages|xargs -r sudo apt-get install --assume-yes
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find

### Ubuntu 20.04

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ mkdir ~/.spack
    $ cp spack/bluebrain/sysconfig/ubuntu-20.04/*.yaml ~/.spack
    $ sed -e 's/#.*//g' spack/bluebrain/sysconfig/ubuntu-20.04/packages|xargs -r sudo apt-get install --assume-yes
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find

Since Ubuntu 20.04 dropped Python 2 support, we need to set Python 3 as the
default `python`:

    $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

To check that we are using Python 3 as `python`:

    $ sudo update-alternatives --config python
    There is only one alternative in link group python
    (providing /usr/bin/python): /usr/bin/python3.8. Nothing to configure.

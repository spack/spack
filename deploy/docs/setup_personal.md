# Setup for Personal Machines

## Building software on OS X

Install software on OS X, using Homebrew for binary packages.

On OS X the build process is very similar to Ubuntu. To avoid building
the whole stack from source we can likewise use another package manager to provide precompiled binaries.
To that end we have successfully used Homebrew. We also provide a skeleton 
`packages.yaml` that you should review and adapt to your needs.

Before starting, please install brew and the required packages.
If you require Python please install a version dowloaded from
Python.org, as several issues have been found with Homebrew's Python

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ mkdir ~/.spack
    $ cp spack/sysconfig/mac_osx/*.yaml ~/.spack
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find

## Building software on Ubuntu

Use Spack on the workstations provided by the project.

### Ubuntu 18.04

We build Docker images based on Ubuntu 18.04, and the same settings can be
used to set Spack up on the desktops:

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ mkdir ~/.spack
    $ cp spack/sysconfig/ubuntu-18.04/*.yaml ~/.spack
    $ sed -e 's/#.*//g' spack/sysconfig/ubuntu-18.04/packages|xargs -r sudo apt-get install --assume-yes
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find

### Ubuntu 20.04

    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ mkdir ~/.spack
    $ cp spack/sysconfig/ubuntu-20.04/*.yaml ~/.spack
    $ sed -e 's/#.*//g' spack/sysconfig/ubuntu-20.04/packages|xargs -r sudo apt-get install --assume-yes
    $ . spack/share/spack/setup-env.sh
    $ spack compiler find

Since Ubuntu 20.04 dropped Python 2 support, we need to set Python 3 as the
default `python`:

    $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

To check that we are using Python 3 as `python`:

    $ sudo update-alternatives --config python
    There is only one alternative in link group python
    (providing /usr/bin/python): /usr/bin/python3.8. Nothing to configure.

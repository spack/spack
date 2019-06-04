# The BlueBrain Spack Deployment

Official documentation [below](#-spack).
For the development documentation of the deployment stack, see
[`deploy/README.md`](deploy/README.md).

## Building software on Ubuntu 18.04

We build Docker images based on Ubuntu 18.04, and the same settings can be
used to set Spack up on the desktops:

    $ git clone https://github.com/BlueBrain/spack.git
    $ mkdir ~/.spack
    $ cp spack/sysconfig/ubuntu-18.04/*.yaml ~/.spack
    $ sed -e 's/#.*//g' spack/sysconfig/ubuntu-18.04/packages|xargs -r sudo apt-get install
    $ spack compiler find
    $ . spack/share/spack/setup-env.sh

Now to build software, i.e., MVDTool:

    $ git clone git@github.com:BlueBrain/MVDTool.git
    $ cd MVDTool
    $ spack setup mvdtool@develop
    $ cd build
    $ ../spconfig.py ..
    $ make

Alternatively, to quickly install software based on a local source
checkout:

    $ git clone git@github.com:BlueBrain/MVDTool.git
    $ cd MVDTool
    $ spack diy -y --test=root mvdtool@my-custom-version

This version of MVDTool can now be re-used by Spack to build other
software, when `^mvdtool@my-custom-version` is appended to the appropriate
spec.

## Building software on BlueBrain5

On BB5, clone this repository to get started using Spack.
The following commands are a good way to get started:

    $ git clone https://github.com/BlueBrain/spack.git
    $ . spack/share/spack/setup-env.sh
    $ spack spec -I spykfunc|head -n 15
    Input spec
    --------------------------------
     -   spykfunc

    Concretized
    --------------------------------
     -   spykfunc@0.12.0%gcc@4.8.5 arch=linux-rhel7-x86_64
     -       ^hdf5@1.10.4%gcc@4.8.5~cxx~debug~fortran+hl~mpi+pic+shared~szip~threadsafe arch=linux-rhel7-x86_64
     -           ^zlib@1.2.11%gcc@4.8.5+optimize+pic+shared arch=linux-rhel7-x86_64
     -       ^highfive@1.6%gcc@4.8.5~boost build_type=RelWithDebInfo ~mpi arch=linux-rhel7-x86_64
     -           ^cmake@3.13.0%gcc@4.8.5~doc+ncurses+openssl+ownlibs~qt arch=linux-rhel7-x86_64
     -               ^ncurses@6.1%gcc@4.8.5~symlinks~termlib arch=linux-rhel7-x86_64
     -                   ^pkgconf@1.5.4%gcc@4.8.5 arch=linux-rhel7-x86_64
     -               ^openssl@1.1.1%gcc@4.8.5+systemcerts arch=linux-rhel7-x86_64
     -                   ^perl@5.26.2%gcc@4.8.5+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-rhel7-x86_64

Here we see all the software that would be required to build one program of
the circuit building workflow.
The leading `-` sign in the output signifies that this particular piece of
software would have to be built from scratch.
To reduce the amount of time spent compiling the same software, we can
configure Spack to use centrally build packages on BB5:

    $ mkdir -p ~/.spack
    $ ln -s /gpfs/bbp.cscs.ch/apps/hpc/jenkins/config/*.yaml ~/.spack
    $ export SPACK_INSTALL_PREFIX=$HOME/software

The configuration thus set up uses the environment variable
`SPACK_INSTALL_PREFIX` as the installation directory for packages.
With the above setup, any packages installed can be found in `~/software`.
Every call to Spack reads this environment variable, temporarily changing
it is a good way to test changes.

After adding the correct setup, the dependency graph of our software to
install has changed significantly:

    $ spack spec -I spykfunc|head -n 15
    Input spec
    --------------------------------
     -   spykfunc

    Concretized
    --------------------------------
    [+]  spykfunc@0.12.0%gcc@6.4.0 arch=linux-rhel7-x86_64
    [^]      ^hdf5@1.10.4%gcc@6.4.0~cxx~debug~fortran+hl~mpi+pic+shared~szip~threadsafe arch=linux-rhel7-x86_64
    [^]          ^zlib@1.2.11%gcc@6.4.0+optimize+pic+shared arch=linux-rhel7-x86_64
    [^]      ^highfive@1.6%gcc@6.4.0~boost build_type=RelWithDebInfo ~mpi arch=linux-rhel7-x86_64
    [^]      ^jdk@1.8.0_191-b12%gcc@6.4.0 arch=linux-rhel7-x86_64
    [^]      ^mvdtool@1.4%gcc@6.4.0 build_type=RelWithDebInfo ~mpi~python arch=linux-rhel7-x86_64
    [+]          ^boost@1.68.0%gcc@6.4.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199 ~pic+program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave arch=linux-rhel7-x86_64
    [+]          ^cmake@3.13.0%gcc@6.4.0~doc+ncurses+openssl+ownlibs~qt arch=linux-rhel7-x86_64
    [^]      ^py-bb5@0.2%gcc@6.4.0 patches=22a56c05830b2e40dffbcbbc70cd2e95c006e13cb4da867f1b7e0d6292ff6618 arch=linux-rhel7-x86_64

This tells us that all required software is either installed in an upstream
database or provided as external packages in the package database (`[^]`
and `[+]`, respectively).

To see all installed packages available through the central installations
directly, use:

    $ spack find -lv|&head
    ==> 265 installed packages
    -- linux-rhel7-x86_64 / gcc@6.4.0 -------------------------------
    s26d2n5 arrow@0.11.0 build_type=Release +parquet+python
    ocjfhxp arrow@0.11.0 build_type=Release +parquet+python
    figbvwx autoconf@2.69
    py26izr automake@1.13.4
    v6f6e33 binutils@2.31.1+gold~libiberty+nls~plugins
    j4xbdil bison@3.0.5
    o4mvxg2 boost@1.68.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199 ~pic+program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave
    lnnxkhm bzip2@1.0.6+shared

These packages act like locally installed packages, only that you will not
be able to uninstall them.
Spack has access to the full dependency graph of the packages above, and
environments will be set accordingly.
The configuration of upstream package databases can be found in
`~/.spack/upsreams.yaml`.
Additional packages are installed and available as external software, where
Spack will trim the dependency tree and only consider the external package
without any sub-dependencies.
The information for external packages is stored in
`~/.spack/packages.yaml`, and can also be printed on the command line:

    $ spack config get packages|&grep -C 1 paths:|tail -n 20
    --
      util-macros:
        paths:
          util-macros@1.19.1: /gpfs/bbp.cscs.ch/apps/hpc/jenkins/deploy/tools/2018-12-19/linux-rhel7-x86_64/gcc-6.4.0/util-macros-1.19.1-et5doh3u6t
    --
      valgrind:
        paths:
          valgrind@3.13.0 +boost~mpi+only64bit+ubsan: /gpfs/bbp.cscs.ch/apps/hpc/jenkins/deploy/tools/2018-12-19/linux-rhel7-x86_64/gcc-6.4.0/valgrind-3.13.0-z5rpvffayd
    --
      xz:
        paths:
          xz@5.2: /usr
    --
      zeromq:
        paths:
          zeromq@4.2.5 +libsodium: /gpfs/bbp.cscs.ch/apps/hpc/jenkins/deploy/external-libraries/2019-01-04/linux-rhel7-x86_64/gcc-6.4.0/zeromq-4.2.5-qvzt3welbs
    --
      zlib:
        paths:
          zlib@1.2.11 +optimize+pic+shared: /gpfs/bbp.cscs.ch/apps/hpc/jenkins/deploy/external-libraries/2019-01-04/linux-rhel7-x86_64/gcc-6.4.0/zlib-1.2.11-w43e56tzqj


## Managing Centrally Built Modules and Packages

Centrally build modules can be made available by sourcing the following
script:

    $ . /gpfs/bbp.cscs.ch/apps/hpc/jenkins/config/modules.sh
    $ module avail|&tail

     /gpfs/bbp.cscs.ch/apps/hpc/jenkins/deploy/applications/2018-12-19/modules/tcl/linux-rhel7-x86_64
    functionalizer/3.11.0             py-bluepyopt/1.6.56/python2
    neurodamus/hippocampus/python3    py-bluepyopt/1.6.56/python3
    neurodamus/master/python3         py-efel/3.0.22/python2
    neurodamus/plasticity/python3     py-efel/3.0.22/python3
    neurodamus/plasticity/python3-knl spykfunc/0.12.0/python3
    parquet-converters/0.3            steps/3.3.0/python3/parallel
    py-bluepymm/0.6.38/python2        synapsetool/0.3.2/parallel
    py-bluepymm/0.6.38/python3        touchdetector/4.3.3

The output above shows the `applications` category of modules, which are
generated from centrally build packages.
To update the version of any of these modules, edit the corresponding YAML
configuration:

    $ vim spack/deploy/packages/bbp-packages.yaml

If there are dependencies used in a broader scope/by several software
packages, consider adding them to one of the following steps in the
deployment chain (all found in `spack/deploy/packages`):

* `parallel-libraries` for everything using MPI or highly performant
* `serial-libraries`, `python-packages` for general purpose libraries
* `external-libraries` for packages that are seldomly changed and for which
  the dependency graph may be truncated by Spack (e.g., Spark, Python) - mainly dependencies for building

Commit the changes and file a pull request on Github.
Jenkins will build the additional software required, with all output
available in a separate directory:

    $ ls /gpfs/bbp.cscs.ch/apps/hpc/jenkins/pulls/165
    config  deploy  mirror  spack

Software packages and modules should be updated upon pull request merge and
a nightly basis.
The `config` directory contains the same configuration files as the regular
deployment and can be used instead.

# <img src="https://cdn.rawgit.com/spack/spack/develop/share/spack/logo/spack-logo.svg" width="64" valign="middle" alt="Spack"/> Spack

[![Build Status](https://travis-ci.org/spack/spack.svg?branch=develop)](https://travis-ci.org/spack/spack)
[![codecov](https://codecov.io/gh/spack/spack/branch/develop/graph/badge.svg)](https://codecov.io/gh/spack/spack)
[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://spack.readthedocs.io)
[![Slack](https://spackpm.herokuapp.com/badge.svg)](https://spackpm.herokuapp.com)

Spack is a multi-platform package manager that builds and installs
multiple versions and configurations of software. It works on Linux,
macOS, and many supercomputers. Spack is non-destructive: installing a
new version of a package does not break existing installations, so many
configurations of the same package can coexist.

Spack offers a simple "spec" syntax that allows users to specify versions
and configuration options. Package files are written in pure Python, and
specs allow package authors to write a single script for many different
builds of the same package.  With Spack, you can build your software
*all* the ways you want to.

See the
[Feature Overview](http://spack.readthedocs.io/en/latest/features.html)
for examples and highlights.

To install spack and your first package, make sure you have Python.
Then:

    $ git clone https://github.com/spack/spack.git
    $ cd spack/bin
    $ ./spack install libelf

Documentation
----------------

[**Full documentation**](http://spack.readthedocs.io/) for Spack is
the first place to look.

Try the
[**Spack Tutorial**](http://spack.readthedocs.io/en/latest/tutorial.html),
to learn how to use spack, write packages, or deploy packages for users
at your site.

See also:
  * [Technical paper](http://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf) and
    [slides](https://tgamblin.github.io/files/Gamblin-Spack-SC15-Talk.pdf) on Spack's design and implementation.
  * [Short presentation](https://tgamblin.github.io/files/Gamblin-Spack-Lightning-Talk-BOF-SC15.pdf) from the *Getting Scientific Software Installed* BOF session at Supercomputing 2015.

Get Involved!
------------------------

Spack is an open source project.  Questions, discussion, and
contributions are welcome. Contributions can be anything from new
packages to bugfixes, or even new core features.

### Mailing list

If you are interested in contributing to spack, join the mailing list.
We're using Google Groups for this:

  * [Spack Google Group](https://groups.google.com/d/forum/spack)

### Slack channel

Spack has a Slack channel where you can chat about all things Spack:

  * [Spack on Slack](https://spackpm.slack.com)

[Sign up here](https://spackpm.herokuapp.com) to get an invitation mailed
to you.

### Twitter

You can follow [@spackpm](https://twitter.com/spackpm) on Twitter for
updates. Also, feel free to `@mention` us in in questions or comments
about your own experience with Spack.

### Contributions

Contributing to Spack is relatively easy.  Just send us a
[pull request](https://help.github.com/articles/using-pull-requests/).
When you send your request, make ``develop`` the destination branch on the
[Spack repository](https://github.com/spack/spack).

Your PR must pass Spack's unit tests and documentation tests, and must be
[PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.  We enforce
these guidelines with [Travis CI](https://travis-ci.org/spack/spack).  To
run these tests locally, and for helpful tips on git, see our
[Contribution Guide](http://spack.readthedocs.io/en/latest/contribution_guide.html).

Spack uses a rough approximation of the
[Git Flow](http://nvie.com/posts/a-successful-git-branching-model/)
branching model.  The ``develop`` branch contains the latest
contributions, and ``master`` is always tagged and points to the latest
stable release.

Authors
----------------
Many thanks go to Spack's [contributors](https://github.com/spack/spack/graphs/contributors).

Spack was created by Todd Gamblin, tgamblin@llnl.gov.

### Citing Spack

If you are referencing Spack in a publication, please cite the following paper:

 * Todd Gamblin, Matthew P. LeGendre, Michael R. Collette, Gregory L. Lee,
   Adam Moody, Bronis R. de Supinski, and W. Scott Futral.
   [**The Spack Package Manager: Bringing Order to HPC Software Chaos**](http://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf).
   In *Supercomputing 2015 (SC’15)*, Austin, Texas, November 15-20 2015. LLNL-CONF-669890.

License
----------------

Spack is distributed under the terms of both the MIT license and the
Apache License (Version 2.0). Users may choose either license, at their
option.

All new contributions must be made under both the MIT and Apache-2.0
licenses.

See [LICENSE-MIT](https://github.com/spack/spack/blob/develop/LICENSE-MIT),
[LICENSE-APACHE](https://github.com/spack/spack/blob/develop/LICENSE-APACHE),
[COPYRIGHT](https://github.com/spack/spack/blob/develop/COPYRIGHT), and
[NOTICE](https://github.com/spack/spack/blob/develop/NOTICE) for details.

`SPDX-License-Identifier: (Apache-2.0 OR MIT)`

``LLNL-CODE-647188``

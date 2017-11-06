.. _configs-tutorial:

================================
Spack Configurations Tutorial
================================

This tutorial will guide you through the configuration options for
Spack installations available through the compilers configuration file
and the packages configuration file. We will first cover the compilers
configuration file, focusing on how it can be used to extend Spack's
compiler autodetection. Then, we will cover the packages
configuration, focusing first on its use for building against external
packages and then on setting other Spack preferences. We will also
briefly cover the Spack config configuration file, which manages more
high-level Spack configuration. For all of these features we will
demonstrate how we build up a full configuration file. For some we
will then demonstrate how the configuration affects the install
command, and for others we will use the `spack spec` command to
demonstrate how the configuration changes have affected Spack's
concretization algorithm. The provided output is all from a server
running ubuntu version 16.04.

.. _configs-tutorial-scopes:

-----------------------------
Configuration Scopes in Spack
-----------------------------

Spack has 4 configuration scopes, and at each scope configuration
files can be sub-scoped generally or by platform. These scopes, in
order of decreasing priority, are:

- User configurations
- Project configurations
- System configurations
- Default configurations

Spack user configurations are stored in the user's home directory
under the `.spack/` directory. Project configurations are stored
within the Spack installation under `SPACK_ROOT/etc/`. System
configurations are stored under `/etc/spack`. Default configurations
are stored under `$SPACK_ROOT/etc/spack/defaults`. Spack contains
sensible default configurations for several platforms in the relevant
files under `$SPACK_ROOT/etc/spack/defaults/<platform>/`.

For example, compiler configuration files named `compilers.yaml` can
appear in 8 places and be used by Spack, in the following decreasing
order of precedence.

- `~/.spack/<platform>/compilers.yaml`
- `~/.spack/compilers.yaml`
- `$SPACK_ROOT/etc/<platform>/compilers.yaml`
- `$SPACK_ROOT/etc/compilers.yaml`
- `/etc/spack/<platform>/compilers.yaml`
- `/etc/spack/compilers.yaml`
- `$SPACK_ROOT/etc/defaults/<platform>/compilers.yaml`
- `$SPACK_ROOT/etc/defaults/compilers.yaml`

Spack configurations are YAML dictionaries. Every configuration file
begins with a top-level dictionary that tells Spack which
configuration set it modifies. When Spack checks it's configuration,
the configuration scopes are updated as dictionaries in increasing
order of precedence, allowing higher precedence files to override
lower. YAML dictionaries use a colon ``:`` to specify key-value
pairs. Spack extends YAML syntax slightly to allow a double-colon
``::`` to specify a key-value pair. When a double-colon is used to
specify a key-value pair, instead of adding that section Spack
replaces what was in that section with the new value. For example, a
user compilers configuration file as follows:

.. code-block:: yaml

  compilers::
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: debian6
      paths:
        cc: !!python/unicode '/path/to/cc'
        cxx: !!python/unicode '/path/to/cxx'
        f77: !!python/unicode '/path/to/f77'
        fc: !!python/unicode '/path/to/fc'
      spec: clang@6.0
      target: x86_64

ensures that no other compilers are used, as the user configuration
scope is the last scope searched and the `compilers::` line replaces
all previous configuration files information. If the same
configuration file had a single colon instead of the double colon, it
would add the clang version 6.0 compiler to whatever other compilers
were listed in other configuration files.

.. _configs-tutorial-compilers:

-------------------------------
Configuring New Spack compilers
-------------------------------

For most tasks, we can use Spack with the compilers autodetected the
first time Spack runs on a system. As we discussed in the basic
installation section, we can also tell Spack where compilers are
located using the `spack compiler add` command. However, in some
circumstances we want even more fine-grained control over the
compilers available. This section will teach you how to exercise that
control using the compilers configuration file.

We will start by opening the compilers configuration file

.. code-block:: console

  emacs -nw ~/.spack/compilers.yaml

.. code-block:: yaml

  compilers:
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: ubuntu16.04
      paths:
        cc: !!python/unicode '/usr/bin/clang'
        cxx: !!python/unicode '/usr/bin/clang++'
        f77: null
        fc: null
      spec: clang@3.8.0-2ubuntu4
      target: x86_64
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: ubuntu16.04
      paths:
        cc: !!python/unicode '/usr/bin/gcc'
        cxx: !!python/unicode '/usr/bin/g++'
        f77: !!python/unicode '/usr/bin/gfortran'
        fc: !!python/unicode '/usr/bin/gfortran'
      spec: gcc@5.4.0
      target: x86_64

This specifies one version of the gcc compiler and one version of the
clang compiler with no flang compiler. Now suppose we have a code that
we want to compile with the clang compiler for C/C++ code, but with
gfortran for fotran components. We can do this by adding another entry
to the compilers.yaml file.

.. code-block:: yaml

    - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: ubuntu16.04
      paths:
        cc: !!python/unicode '/usr/bin/clang'
        cxx: !!python/unicode '/usr/bin/clang++'
        f77: !!python/unicode '/usr/bin/gfortran'
        fc: !!python/unicode '/usr/bin/gfortran'
      spec: clang@3.8.0-gfortran
      target: x86_64

Let's talk about the sections we've changed of this compiler
entry. The biggest change we've made is to the `paths` section. This
lists the paths to the compilers to use for each
language/specification. In this case, we point to the clang compiler
for C/C++ and the gfortran compiler for both specifications of
fortran. We've also changed the `spec` entry for this compiler. The
`spec` entry is effectively the name of the compiler for Spack. It
consists of a name and a version number, separated by the `@`
sign. The name must be one of the supported compiler names in Spack
(gcc, intel, pgi, xl, xl_r, clang, nag, cce). The version number can
be an arbitrary string of alphanumeric characters, as well as `-`,
`.`, and `_`. The `target` and `operating_system` sections we leave
unchanged. These sections specify when Spack can use different
compilers, and are primarily useful for configuration files that will
be used across multiple systems.

We can verify that our new compiler worked by invoking it now

.. code-block:: console

  $ spack install hdf5 %clang@3.8.0-gfortran
  ADD BINARY CACHING OUTPUT

This new compiler also works on fortran codes

.. code-block:: console

  $ spack install zoltan %clang
  ADD BINARY CACHING OUTPUT

--------------------------
Configuring Compiler Flags
--------------------------

Some compilers may require specific compiler flags to work properly in
a particular computing environment. Spack provides configuration
options for setting compiler flags every time a specific compiler is
invoked. These flags become part of the package spec and therefore of
the build provenance. As on the command line, the flags are set
through the implicit build variables `cflags`, `cxxflags`, `cppflags`,
`fflags`, `ldflags`, and `ldlibs`.

Let's open our compilers configuration file again and add a compiler flag.

.. code-block:: yaml

    - compiler:
      environment: {}
      extra_rpaths: []
      flags:
        cppflags: -fPIC
      modules: []
      operating_system: ubuntu16.04
      paths:
        cc: !!python/unicode '/usr/bin/clang'
        cxx: !!python/unicode '/usr/bin/clang++'
        f77: !!python/unicode '/usr/bin/gfortran'
        fc: !!python/unicode '/usr/bin/gfortran'
      spec: clang@3.8.0-gfortran
      target: x86_64

We can test this out using the `spack spec` command to show how the
spec is concretized.

.. code-block:: console

  $ spack spec zoltan %clang
  Input spec
  --------------------------------
  zoltan

  Normalized
  --------------------------------
  zoltan

  Concretized
  --------------------------------
  zoltan@3.83%clang@3.8.0-gfortran cppflags="-fPIC" ~debug+fortran+mpi+shared arch=linux-ubuntu16.04-x86_64
      ^openmpi@3.0.0%clang@3.8.0-gfortran cppflags="-fPIC" ~cuda fabrics= ~java schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
          ^hwloc@1.11.7%clang@3.8.0-gfortran cppflags="-fPIC" ~cuda+libxml2~pci arch=linux-ubuntu16.04-x86_64
              ^libxml2@2.9.4%clang@3.8.0-gfortran cppflags="-fPIC" ~python arch=linux-ubuntu16.04-x86_64
                  ^pkg-config@0.29.2%clang@3.8.0-gfortran cppflags="-fPIC" +internal_glib arch=linux-ubuntu16.04-x86_64
                  ^xz@5.2.3%clang@3.8.0-gfortran cppflags="-fPIC"  arch=linux-ubuntu16.04-x86_64
                  ^zlib@1.2.11%clang@3.8.0-gfortran cppflags="-fPIC" +pic+shared arch=linux-ubuntu16.04-x86_64

We can see that ``cppflags=-fPIC`` has been added to every node in the DAG.

-------------------------------
Advanced Compiler Configuration
-------------------------------

There are three fields of the compiler configuration entry that we
have not talked about yet.

The `modules` field of the compiler is used primarily on Cray systems,
but can be useful on any system that has compilers that are only
useful when a particular module is loaded. Any modules in the
`modules` field of the compiler configuration will be loaded as part
of the build environment for packages using that compiler.

The `extra_rpaths` field of the compiler configuration is used for
compilers that do not rpath all of their dependencies by
default. Since compilers are generally installed externally to Spack,
Spack is unable to manage compiler dependencies and enforce
rpath-ing. This can lead to packages not finding link dependencies
imposed by the compiler properly. For compilers that impose link
dependencies on the resulting executables that are not rpath'd into
the executable automatically, the `extra_rpath` field of the compiler
configuration tells Spack which dependencies to rpath into every
executable created by that compiler. The executables will then be able
to find the link dependencies imposed by the compiler.

The `environment` field of the compiler configuration is used for
generally ``badly behaved`` compiler installations that require some
sort of environment variable to be set to work properly. The contents
of this field is a dictionary of environemnt variable names and values
to set before the compiler is invoked. We generally recommend avoiding
this field when possible, but it is available in particularly
pathological cases.

----------------------------------------
Configuring Package Preferences in Spack
----------------------------------------

Package preferences in Spack are managed through the `packages.yaml` configuration file. First, we will look at the default `packages.yaml` file.

.. code-block:: console

  $ emacs -nw $SPACK_ROOT/etc/spack/defaults/packages.yaml

.. code-block:: yaml

  # -------------------------------------------------------------------------
  # This file controls default concretization preferences for Spack.
  #
  # Settings here are versioned with Spack and are intended to provide
  # sensible defaults out of the box. Spack maintainers should edit this
  # file to keep it current.
  #
  # Users can override these settings by editing the following files.
  #
  # Per-spack-instance settings (overrides defaults):
  #   $SPACK_ROOT/etc/spack/packages.yaml
  #
  # Per-user settings (overrides default and site settings):
  #   ~/.spack/packages.yaml
  # -------------------------------------------------------------------------
  packages:
    all:
      compiler: [gcc, intel, pgi, clang, xl, nag]
      providers:
        awk: [gawk]
        blas: [openblas]
        daal: [intel-daal]
        elf: [elfutils]
        golang: [gcc]
        ipp: [intel-ipp]
        java: [jdk]
        lapack: [openblas]
        mkl: [intel-mkl]
        mpe: [mpe2]
        mpi: [openmpi, mpich]
        opencl: [pocl]
        openfoam: [openfoam-com, openfoam-org, foam-extend]
        pil: [py-pillow]
        scalapack: [netlib-scalapack]
        szip: [libszip, libaec]
        tbb: [intel-tbb]
        jpeg: [libjpeg-turbo, libjpeg]

This sets the default preferences for compilers and for providers for
virtual packages. To illustrate how this works, suppose we want to
change the preferences to prefer the clang compiler and to prefer
mpich over openmpi. Currently, we prefer gcc and openmpi

.. code-block:: console

  $ spack spec hdf5
  Input spec
  --------------------------------
  hdf5

  Normalized
  --------------------------------
  hdf5
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%gcc@5.4.0+cxx~debug+fortran+mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^openmpi@3.0.0%gcc@5.4.0~cuda fabrics= ~java schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
          ^hwloc@1.11.7%gcc@5.4.0~cuda+libxml2~pci arch=linux-ubuntu16.04-x86_64
              ^libxml2@2.9.4%gcc@5.4.0~python arch=linux-ubuntu16.04-x86_64
                  ^pkg-config@0.29.2%gcc@5.4.0+internal_glib arch=linux-ubuntu16.04-x86_64
                  ^xz@5.2.3%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                  ^zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64

Now we will open the packages configuration file and update our
preferences.

.. code-block:: console

  $ emacs -nw ~/.spack/packages.yaml

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]

Because of the configuration scoping we discussed earlier, this
overrides the default settings just for these two items.

.. code-block:: console

  $ spack spec hdf5
  Input spec
  --------------------------------
  hdf5

  Normalized
  --------------------------------
  hdf5
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4+cxx~debug~fortran~hl+mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^mpich@3.2%clang@3.8.0-2ubuntu4 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%clang@3.8.0-2ubuntu4+pic+shared arch=linux-ubuntu16.04-x86_64

--------------------------------
Variant Preference Configuration
--------------------------------

The packages configuration file can also set variant preferences for
packages. For example, let's change our preferences to build all
packages without static libraries. We will accomplish this by turning
off the `shared` variant on all packages that have one.

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]
      variants: ~shared

We can check the effect of this command with `spack spec hdf5` again.

.. code-block:: console

  $ spack spec hdf5
  Input spec
  --------------------------------
  hdf5

  Normalized
  --------------------------------
  hdf5
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4+cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^mpich@3.2%clang@3.8.0-2ubuntu4 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%clang@3.8.0-2ubuntu4+pic~shared arch=linux-ubuntu16.04-x86_64

So far we have only made global changes to the package preferences. As
we've seen throughout this tutorial, hdf5 builds with MPI enabled by
default in Spack. If we were working on a project that would routinely
need serial hdf5, that might get annoying quickly, having to type
`hdf5~mpi` all the time. Instead, we'll update our preferences for
hdf5.

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]
      variants: ~shared
    hdf5:
      variants: ~mpi

Now hdf5 will concretize without an MPI dependency by default.

.. code-block:: console

  $ spack spec hdf5
  Input spec
  --------------------------------
  hdf5

  Normalized
  --------------------------------
  hdf5
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4+cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%clang@3.8.0-2ubuntu4+pic~shared arch=linux-ubuntu16.04-x86_64

In general, every attribute that we can set for all packages we can
set separately for an individual package.

--------------------------
External Packages in Spack
--------------------------

The packages configuration file also controls when Spack will build
against an externally installed package. On these systems we have a
pre-installed zlib.

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]
      variants: ~shared
    hdf5:
      variants: ~mpi
    zlib:
      paths:
        zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64: /usr

Okay what's going on here? We've told Spack that we know the path to an externally installed zlib. We've also told Spack how that zlib was built by writing it out in Spec format. And we've listed the prefix into which zlib was installed.

.. code-block:: console

  $ spack spec hdf5
  Input spec
  --------------------------------
  hdf5

  Normalized
  --------------------------------
  hdf5
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4+cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%clang@3.8.0-2ubuntu4+pic~shared arch=linux-ubuntu16.04-x86_64

Note this did not use our external zlib. Why? Because Spack concretized zlib to a different Spec than the one we provided. There are two ways we could get Spack to build with our external zlib. One would be to explicitly ask for that spec. The other is to tell Spack it's not allowed to build its own zlib. We'll go with the latter.

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]
      variants: ~shared
    hdf5:
      variants: ~mpi
    zlib:
      paths:
        zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64: /usr
      buildable: False

Now Spack will be forced to choose the external zlib.

.. code-block:: console

  $ spack spec hdf5
  Input spec
  --------------------------------
  hdf5

  Normalized
  --------------------------------
  hdf5
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%gcc@5.4.0+cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64

Note that Spack now concretizes the entire DAG to use the gcc
compiler. Because we did not specify a build using the clang compiler
(only expressed a preference) Spack used the gcc compiler specified by
the zlib spec. If we want to use clang for the rest of the build, we
have to specify it.

.. code-block:: console

  $ spack spec hdf5 %clang
  Input spec
  --------------------------------
  hdf5%clang

  Normalized
  --------------------------------
  hdf5%clang
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4+cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64

This gets slightly more complicated with virtual dependencies. Suppose
we don't want to build our own MPI, but we now want a parallel version
of hdf5? Well, fortunately we have mpich installed on these systems.

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]
      variants: ~shared
    hdf5:
      variants: ~mpi
    zlib:
      paths:
        zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64: /usr
      buildable: False
    mpich:
      paths:
        mpich@3.2%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64: /usr
      buildable: False

If we concretize `hdf5+mpi` with this configuration file, we will just
build with an alternate MPI implementation.

.. code-block:: console

  $ spack spec hdf5 %clang +mpi
  Input spec
  --------------------------------
  hdf5%clang+mpi

  Normalized
  --------------------------------
  hdf5%clang+mpi
      ^mpi
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4~cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^openmpi@3.0.0%clang@3.8.0-2ubuntu4~cuda fabrics=verbs ~java schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
          ^hwloc@1.11.8%clang@3.8.0-2ubuntu4~cuda+libxml2+pci arch=linux-ubuntu16.04-x86_64
              ^libpciaccess@0.13.5%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64
                  ^libtool@2.4.6%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64
                      ^m4@1.4.18%clang@3.8.0-2ubuntu4 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00 +sigsegv arch=linux-ubuntu16.04-x86_64
                          ^libsigsegv@2.11%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64
                  ^pkg-config@0.29.2%clang@3.8.0-2ubuntu4+internal_glib arch=linux-ubuntu16.04-x86_64
                  ^util-macros@1.19.1%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64
              ^libxml2@2.9.4%clang@3.8.0-2ubuntu4~python arch=linux-ubuntu16.04-x86_64
                  ^xz@5.2.3%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64
                  ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64

We have only expressed a preference for mpich over other MPI
implementations, and Spack will happily build with one we haven't
forbid it from using. We could resolve this by requesting
`hdf5%clang+mpi^mpich` explicitly, or we can configure Spack not to
use any other MPI implementation. Since we're focused on
configurations here and the former can get tedious, we'll need to
modify our `packages.yaml` file again.

While we're at it, we can configure hdf5 to build with MPI by default
again.

.. code-block:: yaml

  packages:
    all:
      compiler: [clang, gcc, intel, pgi, xl, nag]
      providers:
        mpi: [mpich, openmpi]
      variants: ~shared
    zlib:
      paths:
        zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64: /usr
      buildable: False
    mpich:
      paths:
        mpich@3.2%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64: /usr
      buildable: False
    openmpi:
      buildable: False
    mvapich2:
      buildable: False
    intel-mpi:
      buildable: False
    spectrum-mpi:
      buildable: False
    intel-parallel-studio:
      buildable: False

Now that we have configured Spack not to build any of the possible
providers for MPI we can try again.

.. code-block:: console

  $ spack spec hdf5 %clang
  Input spec
  --------------------------------
  hdf5%clang

  Normalized
  --------------------------------
  hdf5%clang
      ^mpi
      ^zlib@1.1.2:

  Concretized
  --------------------------------
  hdf5@1.10.1%clang@3.8.0-2ubuntu4+cxx~debug~fortran~hl+mpi+pic~shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
      ^mpich@3.2%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64
      ^zlib@1.2.11%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64

Now that we have hdf5 configured to install exactly as we want it, we
can install it. We've now minimized the command line effort necessary
to get exactly the hdf5 installation we want, and we can now build
hdf5 against our external installations of zlib and mpich.

.. code-block:: console

  $ spack install hdf5 %clang
  ADD BINARY CACHING OUTPUT

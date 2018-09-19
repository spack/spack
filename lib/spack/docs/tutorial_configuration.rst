.. _configs-tutorial:

======================
Configuration Tutorial
======================

This tutorial will guide you through various configuration options
that allow you to customize Spack's behavior with respect to
software installation. We will first cover the configuration file
hierarchy. Then, we will cover configuration options for compilers,
focusing on how it can be used to extend Spack's compiler auto-detection.
Next, we will cover the packages configuration file, focusing on
how it can be used to override default build options as well as
specify external package installations to use. Finally, we will
briefly touch on the config configuration file, which manages more
high-level Spack configuration options.

For all of these features we will demonstrate how we build up a full
configuration file. For some we will then demonstrate how the
configuration affects the install command, and for others we will use
the ``spack spec`` command to demonstrate how the configuration
changes have affected Spack's concretization algorithm. The provided
output is all from a server running Ubuntu version 16.04.

.. _configs-tutorial-scopes:

--------------------
Configuration Scopes
--------------------

Depending on your use case, you may want to provide configuration
settings common to everyone on your team, or you may want to set
default behaviors specific to a single user account. Spack provides
4 configuration *scopes* to handle this customization. These scopes,
in order of decreasing priority, are:

======================   ==================================
Scope                    Directory
======================   ==================================
User configurations      ``~/.spack``
Project configurations   ``$SPACK_ROOT/etc/spack``
System configurations    ``/etc/spack``
Default configurations   ``$SPACK_ROOT/etc/spack/defaults``
======================   ==================================

Spack's default configuration settings reside in
``$SPACK_ROOT/etc/spack/defaults``. These are useful for reference,
but should never be directly edited. To override these settings,
create new configuration files in any of the higher-priority
configuration scopes.

A particular cluster may have multiple Spack installations associated
with different projects. To provide settings common to all Spack
installations, put your configuration files in ``/etc/spack``.
To provide settings specific to a particular Spack installation,
you can use the ``$SPACK_ROOT/etc/spack`` directory.

For settings specific to a particular user, you will want to add
configuration files to the ``~/.spack`` directory. When Spack first
checked for compilers on your system, you may have noticed that it
placed your compiler configuration in this directory.

Some facilities manage multiple platforms from a single shared
filesystem. In order to handle this, each of the configuration
scopes listed above has two *sub-scopes*: platform-specific and
platform-independent. For example, compiler settings can be stored
in ``compilers.yaml`` configuration files in the following locations:

- ``~/.spack/<platform>/compilers.yaml``
- ``~/.spack/compilers.yaml``
- ``$SPACK_ROOT/etc/spack/<platform>/compilers.yaml``
- ``$SPACK_ROOT/etc/spack/compilers.yaml``
- ``/etc/spack/<platform>/compilers.yaml``
- ``/etc/spack/compilers.yaml``
- ``$SPACK_ROOT/etc/defaults/<platform>/compilers.yaml``
- ``$SPACK_ROOT/etc/defaults/compilers.yaml``

These files are listed in decreasing order of precedence, so files in
``~/.spack/<platform>`` will override settings in ``~/.spack``.

Spack configurations are YAML dictionaries. Every configuration file
begins with a top-level dictionary that tells Spack which
configuration set it modifies. When Spack checks it's configuration,
the configuration scopes are updated as dictionaries in increasing
order of precedence, allowing higher precedence files to override
lower. YAML dictionaries use a colon ":" to specify key-value
pairs. Spack extends YAML syntax slightly to allow a double-colon
"::" to specify a key-value pair. When a double-colon is used to
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
       operating_system: ubuntu16.04
       paths:
         cc: /usr/bin/gcc
         cxx: /usr/bin/g++
         f77: /usr/bin/gfortran
         fc: /usr/bin/gfortran
       spec: gcc@5.4.0
       target: x86_64


ensures that no other compilers are used, as the user configuration
scope is the last scope searched and the ``compilers::`` line replaces
all previous configuration files information. If the same
configuration file had a single colon instead of the double colon, it
would add the gcc version 5.4.0 compiler to whatever other compilers
were listed in other configuration files.

.. _configs-tutorial-compilers:

----------------------
Compiler Configuration
----------------------

For most tasks, we can use Spack with the compilers auto-detected the
first time Spack runs on a system. As we discussed in the basic
installation section, we can also tell Spack where compilers are
located using the ``spack compiler add`` command. However, in some
circumstances we want even more fine-grained control over the
compilers available. This section will teach you how to exercise that
control using the compilers configuration file.

We will start by opening the compilers configuration file

.. code-block:: console

   $ spack config edit compilers


.. code-block:: yaml

   compilers:
   - compiler:
       environment: {}
       extra_rpaths: []
       flags: {}
       modules: []
       operating_system: ubuntu16.04
       paths:
         cc: /usr/bin/clang
         cxx: /usr/bin/clang++
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
         cc: /usr/bin/gcc
         cxx: /usr/bin/g++
         f77: /usr/bin/gfortran
         fc: /usr/bin/gfortran
       spec: gcc@5.4.0
       target: x86_64


This specifies one version of the gcc compiler and one version of the
clang compiler with no flang compiler. Now suppose we have a code that
we want to compile with the clang compiler for C/C++ code, but with
gfortran for Fortran components. We can do this by adding another entry
to the ``compilers.yaml`` file.

.. code-block:: yaml

   - compiler:
     environment: {}
     extra_rpaths: []
     flags: {}
     modules: []
     operating_system: ubuntu16.04
     paths:
       cc: /usr/bin/clang
       cxx: /usr/bin/clang++
       f77: /usr/bin/gfortran
       fc: /usr/bin/gfortran
     spec: clang@3.8.0-gfortran
     target: x86_64


Let's talk about the sections of this compiler entry that we've changed.
The biggest change we've made is to the ``paths`` section. This lists
the paths to the compilers to use for each language/specification.
In this case, we point to the clang compiler for C/C++ and the gfortran
compiler for both specifications of Fortran. We've also changed the
``spec`` entry for this compiler. The ``spec`` entry is effectively the
name of the compiler for Spack. It consists of a name and a version
number, separated by the ``@`` sigil. The name must be one of the supported
compiler names in Spack (gcc, intel, pgi, xl, xl_r, clang, nag, cce).
The version number can be an arbitrary string of alphanumeric characters,
as well as ``-``, ``.``, and ``_``. The ``target`` and ``operating_system``
sections we leave unchanged. These sections specify when Spack can use
different compilers, and are primarily useful for configuration files that
will be used across multiple systems.

We can verify that our new compiler works by invoking it now:

.. code-block:: console

   $ spack install zlib %clang@3.8.0-gfortran
   ...


This new compiler also works on Fortran codes:

.. code-block:: console

   $ spack install cfitsio %clang@3.8.0-gfortran
   ...


^^^^^^^^^^^^^^
Compiler Flags
^^^^^^^^^^^^^^

Some compilers may require specific compiler flags to work properly in
a particular computing environment. Spack provides configuration
options for setting compiler flags every time a specific compiler is
invoked. These flags become part of the package spec and therefore of
the build provenance. As on the command line, the flags are set
through the implicit build variables ``cflags``, ``cxxflags``, ``cppflags``,
``fflags``, ``ldflags``, and ``ldlibs``.

Let's open our compilers configuration file again and add a compiler flag.

.. code-block:: yaml

   - compiler:
     environment: {}
     extra_rpaths: []
     flags:
       cppflags: -g
     modules: []
     operating_system: ubuntu16.04
     paths:
       cc: /usr/bin/clang
       cxx: /usr/bin/clang++
       f77: /usr/bin/gfortran
       fc: /usr/bin/gfortran
     spec: clang@3.8.0-gfortran
     target: x86_64


We can test this out using the ``spack spec`` command to show how the
spec is concretized.

.. code-block:: console

   $ spack spec cfitsio %clang@3.8.0-gfortran
   Input spec
   --------------------------------
   cfitsio%clang@3.8.0-gfortran

   Normalized
   --------------------------------
   cfitsio%clang@3.8.0-gfortran

   Concretized
   --------------------------------
   cfitsio@3.410%clang@3.8.0-gfortran cppflags="-g" +bzip2+shared arch=linux-ubuntu16.04-x86_64
       ^bzip2@1.0.6%clang@3.8.0-gfortran cppflags="-g" +shared arch=linux-ubuntu16.04-x86_64


We can see that "cppflags=-g" has been added to every node in the DAG.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Advanced Compiler Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are three fields of the compiler configuration entry that we
have not talked about yet.

The ``modules`` field of the compiler is used primarily on Cray systems,
but can be useful on any system that has compilers that are only
useful when a particular module is loaded. Any modules in the
``modules`` field of the compiler configuration will be loaded as part
of the build environment for packages using that compiler.

The ``extra_rpaths`` field of the compiler configuration is used for
compilers that do not rpath all of their dependencies by
default. Since compilers are generally installed externally to Spack,
Spack is unable to manage compiler dependencies and enforce
rpath usage. This can lead to packages not finding link dependencies
imposed by the compiler properly. For compilers that impose link
dependencies on the resulting executables that are not rpath'ed into
the executable automatically, the ``extra_rpath`` field of the compiler
configuration tells Spack which dependencies to rpath into every
executable created by that compiler. The executables will then be able
to find the link dependencies imposed by the compiler. As an example,
this field can be set by

.. code-block:: yaml

   - compiler:
     ...
     extra_rpaths:
      - /apps/intel/ComposerXE2017/compilers_and_libraries_2017.5.239/linux/compiler/lib/intel64_lin
     ...


The ``environment`` field of the compiler configuration is used for
compilers that require environment variables to be set during build
time. For example, if your Intel compiler suite requires the
``INTEL_LICENSE_FILE`` environment variable to point to the proper
license server, you can set this in ``compilers.yaml`` as follows:

.. code-block:: yaml

  - compiler:
      environment:
        set:
          INTEL_LICENSE_FILE: 1713@license4
      ...


.. _configs-tutorial-package-prefs:

-------------------------------
Configuring Package Preferences
-------------------------------

Package preferences in Spack are managed through the ``packages.yaml``
configuration file. First, we will look at the default
``packages.yaml`` file.

.. code-block:: console

   $ spack config --scope defaults edit packages


.. literalinclude:: ../../../etc/spack/defaults/packages.yaml
   :language: yaml


This sets the default preferences for compilers and for providers of
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

  $ spack config edit packages


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


^^^^^^^^^^^^^^^^^^^
Variant Preferences
^^^^^^^^^^^^^^^^^^^

The packages configuration file can also set variant preferences for
package variants. For example, let's change our preferences to build all
packages without shared libraries. We will accomplish this by turning
off the ``shared`` variant on all packages that have one.

.. code-block:: yaml

   packages:
     all:
       compiler: [clang, gcc, intel, pgi, xl, nag]
       providers:
         mpi: [mpich, openmpi]
       variants: ~shared


We can check the effect of this command with ``spack spec hdf5`` again.

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
``hdf5~mpi`` all the time. Instead, we'll update our preferences for
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

^^^^^^^^^^^^^^^^^
External Packages
^^^^^^^^^^^^^^^^^

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
         zlib@1.2.8%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64: /usr


Here, we've told Spack that zlib 1.2.8 is installed on our system.
We've also told it the installation prefix where zlib can be found.
We don't know exactly which variants it was built with, but that's
okay.

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
   hdf5@1.10.1%gcc@5.4.0~cxx~debug~fortran~hl~mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
       ^zlib@1.2.8%gcc@5.4.0+optimize+pic~shared arch=linux-ubuntu16.04-x86_64


You'll notice that Spack is now using the external zlib installation,
but the compiler used to build zlib is now overriding our compiler
preference of clang. If we explicitly specify clang:

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
   hdf5@1.10.1%clang@3.8.0-2ubuntu4~cxx~debug~fortran~hl~mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
       ^zlib@1.2.11%clang@3.8.0-2ubuntu4+optimize+pic~shared arch=linux-ubuntu16.04-x86_64


Spack concretizes to both hdf5 and zlib being built with clang.
This has a side-effect of rebuilding zlib. If we want to force
Spack to use the system zlib, we have two choices. We can either
specify it on the command line, or we can tell Spack that it's
not allowed to build its own zlib. We'll go with the latter.

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
         zlib@1.2.8%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64: /usr
       buildable: False


Now Spack will be forced to choose the external zlib.

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
   hdf5@1.10.1%clang@3.8.0-2ubuntu4~cxx~debug~fortran~hl~mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
       ^zlib@1.2.8%gcc@5.4.0+optimize+pic~shared arch=linux-ubuntu16.04-x86_64


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
         zlib@1.2.8%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64: /usr
       buildable: False
     mpich:
       paths:
         mpich@3.2%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64: /usr
       buildable: False


If we concretize ``hdf5+mpi`` with this configuration file, we will just
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
                   ^zlib@1.2.8%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64


We have only expressed a preference for mpich over other MPI
implementations, and Spack will happily build with one we haven't
forbid it from using. We could resolve this by requesting
``hdf5%clang+mpi^mpich`` explicitly, or we can configure Spack not to
use any other MPI implementation. Since we're focused on
configurations here and the former can get tedious, we'll need to
modify our ``packages.yaml`` file again.

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
         zlib@1.2.8%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64: /usr
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
       ^zlib@1.2.8%gcc@5.4.0+pic+shared arch=linux-ubuntu16.04-x86_64


By configuring most of our package preferences in ``packages.yaml``,
we can cut down on the amount of work we need to do when specifying
a spec on the command line. In addition to compiler and variant
preferences, we can specify version preferences as well. Anything
that you can specify on the command line can be specified in
``packages.yaml`` with the exact same spec syntax.

.. warning::

   Make sure to delete or move the ``packages.yaml`` you have been
   editing up to this point. Otherwise, it will change the hashes
   of your packages, leading to differences in the output of later
   tutorial sections.


-----------------
High-level Config
-----------------

In addition to compiler and package settings, Spack allows customization
of several high-level settings. These settings are stored in the generic
``config.yaml`` configuration file. You can see the default settings by
running:

.. code-block:: console

   $ spack config --scope defaults edit config


.. literalinclude:: ../../../etc/spack/defaults/config.yaml
   :language: yaml


As you can see, many of the directories Spack uses can be customized.
For example, you can tell Spack to install packages to a prefix
outside of the ``$SPACK_ROOT`` hierarchy. Module files can be
written to a central location if you are using multiple Spack
instances. If you have a fast scratch filesystem, you can run builds
from this filesystem with the following ``config.yaml``:

.. code-block:: yaml

   config:
     build_stage:
       - /scratch/$user


On systems with compilers that absolutely *require* environment variables
like ``LD_LIBRARY_PATH``, it is possible to prevent Spack from cleaning
the build environment with the ``dirty`` setting:

.. code-block:: yaml

   config:
     dirty: true


However, this is strongly discouraged, as it can pull unwanted libraries
into the build.

One last setting that may be of interest to many users is the ability
to customize the parallelism of Spack builds. By default, Spack
installs all packages in parallel with the number of jobs equal to the
number of cores on the node. For example, on a node with 36 cores,
this will look like:

.. code-block:: console

   $ spack install --verbose zlib
   ==> Installing zlib
   ==> Using cached archive: ~/spack/var/spack/cache/zlib/zlib-1.2.11.tar.gz
   ==> Staging archive: ~/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb/zlib-1.2.11.tar.gz
   ==> Created stage in ~/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
   ==> No patches needed for zlib
   ==> Building zlib [Package]
   ==> Executing phase: 'install'
   ==> './configure' '--prefix=~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb'
   Checking for shared library support...
   Building shared library libz.so.1.2.11 with ~/spack/lib/spack/env/gcc/gcc.
   Checking for size_t... Yes.
   Checking for off64_t... Yes.
   Checking for fseeko... Yes.
   Checking for strerror... Yes.
   Checking for unistd.h... Yes.
   Checking for stdarg.h... Yes.
   Checking whether to use vs[n]printf() or s[n]printf()... using vs[n]printf().
   Checking for vsnprintf() in stdio.h... Yes.
   Checking for return value of vsnprintf()... Yes.
   Checking for attribute(visibility) support... Yes.
   ==> 'make' '-j36'
   ...
   ==> 'make' '-j36' 'install'
   ...


As you can see, we are building with all 36 cores on the node. If you are
on a shared login node, this can slow down the system for other users. If
you have a strict ulimit or restriction on the number of available licenses,
you may not be able to build at all with this many cores. On nodes with 64+
cores, you may not see a significant speedup of the build anyway. To limit
the number of cores our build uses, set ``build_jobs`` like so:

.. code-block:: yaml

   config:
     build_jobs: 4


If we uninstall and reinstall zlib, we see that it now uses only 4 cores:

.. code-block:: console

   $ spack install -v zlib
   ==> Installing zlib
   ==> Using cached archive: ~/spack/var/spack/cache/zlib/zlib-1.2.11.tar.gz
   ==> Staging archive: ~/spack/var/spack/stage/zlib-1.2.11-ezuwp4pa52e75v6iweawzwymmf4ahxxn/zlib-1.2.11.tar.gz
   ==> Created stage in ~/spack/var/spack/stage/zlib-1.2.11-ezuwp4pa52e75v6iweawzwymmf4ahxxn
   ==> No patches needed for zlib
   ==> Building zlib [Package]
   ==> Executing phase: 'install'
   ==> './configure' '--prefix=~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-7.2.0/zlib-1.2.11-ezuwp4pa52e75v6iweawzwymmf4ahxxn'
   Checking for shared library support...
   Building shared library libz.so.1.2.11 with ~/spack/lib/spack/env/gcc/gcc.
   Checking for size_t... Yes.
   Checking for off64_t... Yes.
   Checking for fseeko... Yes.
   Checking for strerror... Yes.
   Checking for unistd.h... Yes.
   Checking for stdarg.h... Yes.
   Checking whether to use vs[n]printf() or s[n]printf()... using vs[n]printf().
   Checking for vsnprintf() in stdio.h... Yes.
   Checking for return value of vsnprintf()... Yes.
   Checking for attribute(visibility) support... Yes.
   ==> 'make' '-j4'
   ...
   ==> 'make' '-j4' 'install'
   ...


Obviously, if you want to build everything in serial for whatever reason,
you would set ``build_jobs`` to 1.


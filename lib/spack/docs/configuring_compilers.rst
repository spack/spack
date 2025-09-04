.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Discover how to configure compilers in Spack, whether by specifying them as externals, or by installing them with Spack.

.. _compiler-config:

Configuring Compilers
=====================

Spack has the ability to build packages with multiple compilers and compiler versions.
Compilers can be made available to Spack by:

1. Specifying them as externals in ``packages.yaml``, or
2. Having them installed in the current Spack store, or
3. Having them available as binaries in a buildcache

For convenience, Spack will automatically detect compilers as externals the first time it needs them, if no compiler is available.

.. _cmd-spack-compilers:

``spack compiler list``
-----------------------

You can see which compilers are available to Spack by running ``spack compiler list``:

.. code-block:: spec

   $ spack compiler list
   ==> Available compilers
   -- gcc ubuntu20.04-x86_64 ---------------------------------------
   [e]  gcc@10.5.0  [+]  gcc@15.1.0  [+]  gcc@14.3.0

Compilers marked with an ``[e]`` are system compilers (externals), and those marked with a ``[+]`` have been installed by Spack.
Compilers from remote buildcaches are marked as ``-``, but are not shown by default.
To see them you need a specific option:

.. code-block:: console

   $ spack compiler list --remote
   ==> Available compilers
   -- gcc ubuntu20.04-x86_64 ---------------------------------------
   [e]  gcc@10.5.0  [+]  gcc@15.1.0  [+]  gcc@14.3.0

   -- gcc ubuntu20.04-x86_64 ---------------------------------------
    -   gcc@12.4.0

Any of these compilers can be used to build Spack packages.
More details on how this is done can be found in :ref:`sec-specs`.

.. _cmd-spack-compiler-find:

``spack compiler find``
-----------------------

If you do not see a compiler in the list shown by:

.. code-block:: console

   $ spack compiler list

but you want to use it with Spack, you can simply run ``spack compiler find`` with the path to where the compiler is installed.
For example:

.. code-block:: console

   $ spack compiler find /opt/intel/oneapi/compiler/2025.1/bin/
   ==> Added 1 new compiler to /home/user/.spack/packages.yaml
       intel-oneapi-compilers@2025.1.0
   ==> Compilers are defined in the following files:
       /home/user/.spack/packages.yaml

Or you can run ``spack compiler find`` with no arguments to force auto-detection.
This is useful if you do not know where compilers are installed, but you know that new compilers have been added to your ``PATH``.
For example, you might load a module, like this:

.. code-block:: console

   $ module load gcc/4.9.0
   $ spack compiler find
   ==> Added 1 new compiler to /home/user/.spack/packages.yaml
       gcc@4.9.0

This loads the environment module for gcc-4.9.0 to add it to ``PATH``, and then it adds the compiler to Spack.

.. note::

   By default, Spack does not fill in the ``modules:`` field in the ``packages.yaml`` file.
   If you are using a compiler from a module, then you should add this field manually.
   See the section on :ref:`compilers-requiring-modules`.

.. _cmd-spack-compiler-info:

``spack compiler info``
-----------------------

If you want to see additional information about specific compilers, you can run ``spack compiler info``:

.. code-block:: console

   $ spack compiler info gcc
   gcc@=8.4.0 languages='c,c++,fortran' arch=linux-ubuntu20.04-x86_64:
     prefix: /usr
     compilers:
       c: /usr/bin/gcc-8
       cxx: /usr/bin/g++-8
       fortran: /usr/bin/gfortran-8

   gcc@=9.4.0 languages='c,c++,fortran' arch=linux-ubuntu20.04-x86_64:
     prefix: /usr
     compilers:
       c: /usr/bin/gcc
       cxx: /usr/bin/g++
       fortran: /usr/bin/gfortran

   gcc@=10.5.0 languages='c,c++,fortran' arch=linux-ubuntu20.04-x86_64:
     prefix: /usr
     compilers:
       c: /usr/bin/gcc-10
       cxx: /usr/bin/g++-10
       fortran: /usr/bin/gfortran-10

This shows the details of the compilers that were detected by Spack.
Notice also that we didn't have to be too specific about the version.
We just said ``gcc``, and we got information about all the matching compilers.

Manual configuration of external compilers
------------------------------------------

If auto-detection fails, you can manually configure a compiler by editing your ``packages`` configuration.
You can do this by running:

.. code-block:: console

   $ spack config edit packages

which will open the file in :ref:`your favorite editor <controlling-the-editor>`.

Each compiler has an "external" entry in the file with ``extra_attributes``:

.. code-block:: yaml

   packages:
     gcc:
       externals:
       - spec: gcc@10.5.0 languages='c,c++,fortran'
         prefix: /usr
         extra_attributes:
           compilers:
             c: /usr/bin/gcc-10
             cxx: /usr/bin/g++-10
             fortran: /usr/bin/gfortran-10

The compiler executables are listed under ``extra_attributes:compilers``, and are keyed by language.
Once you save the file, the configured compilers will show up in the list displayed by ``spack compilers``.

You can also add compiler flags to manually configured compilers.
These flags should be specified in the ``flags`` section of the compiler specification.
The valid flags are ``cflags``, ``cxxflags``, ``fflags``, ``cppflags``, ``ldflags``, and ``ldlibs``.
For example:

.. code-block:: yaml

   packages:
     gcc:
       externals:
       - spec: gcc@10.5.0 languages='c,c++,fortran'
         prefix: /usr
         extra_attributes:
           compilers:
             c: /usr/bin/gcc-10
             cxx: /usr/bin/g++-10
             fortran: /usr/bin/gfortran-10
           flags:
             cflags: -O3 -fPIC
             cxxflags: -O3 -fPIC
             cppflags: -O3 -fPIC

These flags will be treated by Spack as if they were entered from the command line each time this compiler is used.
The compiler wrappers then inject those flags into the compiler command.
Compiler flags entered from the command line will be discussed in more detail in the following section.

Some compilers also require additional environment configuration.
Examples include Intel's oneAPI and AMD's AOCC compiler suites, which have custom scripts for loading environment variables and setting paths.
These variables should be specified in the ``environment`` section of the compiler specification.
The operations available to modify the environment are ``set``, ``unset``, ``prepend_path``, ``append_path``, and ``remove_path``.
For example:

.. code-block:: yaml

   packages:
     intel-oneapi-compilers:
       externals:
       - spec: intel-oneapi-compilers@2025.1.0
         prefix: /opt/intel/oneapi
         extra_attributes:
           compilers:
             c: /opt/intel/oneapi/compiler/2025.1/bin/icx
             cxx: /opt/intel/oneapi/compiler/2025.1/bin/icpx
             fortran: /opt/intel/oneapi/compiler/2025.1/bin/ifx
           environment:
             set:
               MKL_ROOT: "/path/to/mkl/root"
             unset: # A list of environment variables to unset
             - CC
             prepend_path: # Similar for append|remove_path
               LD_LIBRARY_PATH: /ld/paths/added/by/setvars/sh

It is also possible to specify additional ``RPATHs`` that the compiler will add to all executables generated by that compiler.
This is useful for forcing certain compilers to RPATH their own runtime libraries so that executables will run without the need to set ``LD_LIBRARY_PATH``:

.. code-block:: yaml

   packages:
     gcc:
       externals:
       - spec: gcc@4.9.3
         prefix: /opt/gcc
         extra_attributes:
           compilers:
             c: /opt/gcc/bin/gcc
             cxx: /opt/gcc/bin/g++
             fortran: /opt/gcc/bin/gfortran
           extra_rpaths:
           - /path/to/some/compiler/runtime/directory
           - /path/to/some/other/compiler/runtime/directory

.. _compilers-requiring-modules:

Compilers Requiring Modules
---------------------------

Many installed compilers will work regardless of the environment from which they are called.
However, some installed compilers require environment variables to be set in order to run.

On typical HPC clusters, these environment modifications are usually delegated to some "module" system.
In such a case, you should tell Spack which module(s) to load in order to run the chosen compiler:

.. code-block:: yaml

   packages:
     gcc:
       externals:
       - spec: gcc@10.5.0 languages='c,c++,fortran'
         prefix: /opt/compilers
         extra_attributes:
           compilers:
             c: /opt/compilers/bin/gcc-10
             cxx: /opt/compilers/bin/g++-10
             fortran: /opt/compilers/bin/gfortran-10
         modules: [gcc/10.5.0]

Some compilers require special environment settings to be loaded not just to run, but also to execute the code they build, breaking packages that need to execute code they just compiled.
If it's not possible or practical to use a better compiler, you'll need to ensure that environment settings are preserved for compilers like this (i.e., you'll need to load the module or source the compiler's shell script).

By default, Spack tries to ensure that builds are reproducible by cleaning the environment before building.
If this interferes with your compiler settings, you CAN use ``spack install --dirty`` as a workaround.
Note that this MAY interfere with package builds.

Build Your Own Compiler
-----------------------

If you require a specific compiler and version, you can have Spack build it for you.
For example:

.. code-block:: spec

   $ spack install gcc@14+binutils

Once the compiler is installed, you can start using it without additional configuration:

.. code-block:: spec

   $ spack install hdf5~mpi %gcc@14

Mixing Compilers
----------------

For more options on configuring Spack to mix different compilers for different languages, see :ref:`the toolchains configuration docs <toolchains>`.

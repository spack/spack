.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _build-settings:

===================
Build Customization
===================

Spack allows you to customize how your software is built through the
``packages.yaml`` file.  Using it, you can make Spack prefer particular
implementations of virtual dependencies (e.g., MPI or BLAS/LAPACK),
or you can make it prefer to build with particular compilers.  You can
also tell Spack to use *external* software installations already
present on your system.

At a high level, the ``packages.yaml`` file is structured like this:

.. code-block:: yaml

   packages:
     package1:
       # settings for package1
     package2:
       # settings for package2
     # ...
     all:
       # settings that apply to all packages.

So you can either set build preferences specifically for *one* package,
or you can specify that certain settings should apply to *all* packages.
The types of settings you can customize are described in detail below.

Spack's build defaults are in the default
``etc/spack/defaults/packages.yaml`` file.  You can override them in
``~/.spack/packages.yaml`` or ``etc/spack/packages.yaml``. For more
details on how this works, see :ref:`configuration-scopes`.

.. _sec-external-packages:

-----------------
External Packages
-----------------

Spack can be configured to use externally-installed
packages rather than building its own packages. This may be desirable
if machines ship with system packages, such as a customized MPI
that should be used instead of Spack building its own MPI.

External packages are configured through the ``packages.yaml`` file found
in a Spack installation's ``etc/spack/`` or a user's ``~/.spack/``
directory. Here's an example of an external configuration:

.. code-block:: yaml

   packages:
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel

This example lists three installations of OpenMPI, one built with GCC,
one built with GCC and debug information, and another built with Intel.
If Spack is asked to build a package that uses one of these MPIs as a
dependency, it will use the pre-installed OpenMPI in
the given directory. Note that the specified path is the top-level
install prefix, not the ``bin`` subdirectory.

``packages.yaml`` can also be used to specify modules to load instead
of the installation prefixes.  The following example says that module
``CMake/3.7.2`` provides cmake version 3.7.2.

.. code-block:: yaml

   cmake:
     externals:
     - spec: cmake@3.7.2
       modules:
       - CMake/3.7.2

Each ``packages.yaml`` begins with a ``packages:`` attribute, followed
by a list of package names.  To specify externals, add an ``externals:``
attribute under the package name, which lists externals.
Each external should specify a ``spec:`` string that should be as
well-defined as reasonably possible.  If a
package lacks a spec component, such as missing a compiler or
package version, then Spack will guess the missing component based
on its most-favored packages, and it may guess incorrectly.

Each package version and compiler listed in an external should
have entries in Spack's packages and compiler configuration, even
though the package and compiler may not ever be built.

The packages configuration can tell Spack to use an external location
for certain package versions, but it does not restrict Spack to using
external packages.  In the above example, since newer versions of OpenMPI
are available, Spack will choose to start building and linking with the
latest version rather than continue using the pre-installed OpenMPI versions.

To prevent this, the ``packages.yaml`` configuration also allows packages
to be flagged as non-buildable.  The previous example could be modified to
be:

.. code-block:: yaml

   packages:
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel
       buildable: False

The addition of the ``buildable`` flag tells Spack that it should never build
its own version of OpenMPI, and it will instead always rely on a pre-built
OpenMPI.  Similar to ``paths``, ``buildable`` is specified as a property under
a package name.

If an external module is specified as not buildable, then Spack will load the
external module into the build environment which can be used for linking.

The ``buildable`` does not need to be paired with external packages.
It could also be used alone to forbid packages that may be
buggy or otherwise undesirable.

Virtual packages in Spack can also be specified as not buildable, and
external implementations can be provided. In the example above,
OpenMPI is configured as not buildable, but Spack will often prefer
other MPI implementations over the externally available OpenMPI. Spack
can be configured with every MPI provider not buildable individually,
but more conveniently:

.. code-block:: yaml

   packages:
     mpi:
       buildable: False
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel

Implementations can also be listed immediately under the virtual they provide:

.. code-block:: yaml

   packages:
     mpi:
       buildable: False
         openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64: /opt/openmpi-1.4.3
         openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug: /opt/openmpi-1.4.3-debug
         openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64: /opt/openmpi-1.6.5-intel
         mpich@3.3 %clang@9.0.0 arch=linux-debian7-x86_64: /opt/mpich-3.3-intel

Spack can then use any of the listed external implementations of MPI
to satisfy a dependency, and will choose depending on the compiler and
architecture.

.. _cmd-spack-external-find:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Automatically Find External Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run the :ref:`spack external find <spack-external-find>` command
to search for system-provided packages and add them to ``packages.yaml``.
After running this command your ``packages.yaml`` may include new entries:

.. code-block:: yaml

   packages:
     cmake:
       externals:
       - spec: cmake@3.17.2
         prefix: /usr

Generally this is useful for detecting a small set of commonly-used packages;
for now this is generally limited to finding build-only dependencies.
Specific limitations include:

* Packages are not discoverable by default: For a package to be
  discoverable with ``spack external find``, it needs to add special
  logic. See :ref:`here <make-package-findable>` for more details.
* The current implementation only collects and examines executable files,
  so it is typically only useful for build/run dependencies (in some cases
  if a library package also provides an executable, it may be possible to
  extract a meaningful Spec by running the executable - for example the
  compiler wrappers in MPI implementations).
* The logic does not search through module files, it can only detect
  packages with executables defined in ``PATH``; you can help Spack locate
  externals which use module files by loading any associated modules for
  packages that you want Spack to know about before running
  ``spack external find``.
* Spack does not overwrite existing entries in the package configuration:
  If there is an external defined for a spec at any configuration scope,
  then Spack will not add a new external entry (``spack config blame packages``
  can help locate all external entries).


.. _manually-adding-external-packages:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Manually Adding External Packages in Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So far this section described external package detection and its limitations.
The paragraphs below deal with challenges arising when external packages are
found in loadable modules. When using modules, Spack will attempt to parse the
``module show`` output in order to determine all relevant settings and
variables. Reasons why this may not work automatically are

* a mismatch between module and package name,
* missing module dependencies in the ``packages.yaml`` file,
* modules whose directory structure does not match conventions, and
* the use of metamodules, i.e., modules whose only purpose is to load other
  modules.

Each following paragraph will discuss one of the bullet points above.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Module/Package Name Mismatches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For certain libraries there exist multiple implementations (e.g., MPI). When
defining an external entry for a package, make sure the package name identifies
the implementation that matches the module. For example, the package ``mpich``
can be used only for the vanilla MPICH implementation but not for Cray MPICH;
Cray MPICH has its own package called ``cray-mpich``. If the wrong module name
is picked, this can cause errors later, e.g., Spack may compute a wrong prefix.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Missing Modules Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The case of missing dependencies will be discussed based on the real-world
example of loading OpenMPI 4.0.2 with CUDA support. Shown below is the ``module
show openmpi/4.0.2`` output.

.. code-block:: console

    $ module show openmpi/4.0.2-cuda
    -------------------------------------------------------------------
    /usr/local/modulefiles/openmpi/4.0.2-cuda:

    module-whatis   {An open source Message Passing Interface implementation.}
    prereq          intel-compilers/19.0.4 pgi/20.1 pgi/19.10 gcc/10.1.0 gcc/8.3.1
    conflict        openmpi
    conflict        intel-mpi

    Available software environment(s):
    - intel-compilers/19.0.4 cuda/10.2
    - pgi/20.1 cuda/10.2
    - pgi/19.10 cuda/10.2
    - gcc/10.1.0 cuda/10.2
    - gcc/8.3.1 cuda/10.2
    - gcc/8.3.1 cuda/10.1.2
    - gcc/8.3.1 cuda/10.1.1

    If you want to use this module with another software environment,
    please contact the support team.
    -------------------------------------------------------------------

There are two things of importance to note. First, there are multiple possible
module combinations to satisfy the compiler and CUDA dependency; this example
will use ``gcc/8.3.1`` and ``cuda/10.1.2``. Second, the output does not contain
any information about environment variables or flags that are needed. The
situation changes as soon as the dependencies are satisfied.

.. code-block:: console

    $ module purge
    $ module load gcc/8.3.1
    $ module load cuda/10.1.2
    $ module show openmpi/4.0.2-cuda
    -------------------------------------------------------------------
    /usr/local/modulefiles/openmpi/4.0.2-cuda:

    module-whatis   {An open source Message Passing Interface implementation.}
    prereq          intel-compilers/19.0.4 pgi/20.1 pgi/19.10 gcc/10.1.0 gcc/8.3.1
    prereq          cuda/10.2 cuda/10.1.2 cuda/10.1.1
    conflict        openmpi
    conflict        intel-mpi
    prepend-path    CPATH /usr/local/spack_soft/openmpi/4.0.2/gcc-8.3.1-n6vcsair26tkpepojy3c2gqxtqccijq3/include
    prepend-path    LD_LIBRARY_PATH /usr/local/spack_soft/openmpi/4.0.2/gcc-8.3.1-n6vcsair26tkpepojy3c2gqxtqccijq3/lib
    prepend-path    LIBRARY_PATH /usr/local/spack_soft/openmpi/4.0.2/gcc-8.3.1-n6vcsair26tkpepojy3c2gqxtqccijq3/lib
    prepend-path    PATH /usr/local/spack_soft/openmpi/4.0.2/gcc-8.3.1-n6vcsair26tkpepojy3c2gqxtqccijq3/bin
    [snip]

This output can be parsed by Spack when building software. To obtain an entry
for this external package in the ``package.yaml`` file, you could run ``spack
external find openmpi`` after loading the dependencies to benefit from the
automatic variant detection of the OpenMPI build. Afterwards, add the module
and all of its dependencies in the ``packages.yaml`` file to arrive at the
following OpenMPI entry:

.. code-block:: yaml

    packages:
      openmpi:
        externals:
        - spec: openmpi@4.0.2+cuda+cxx+cxx_exceptions~java~memchecker+pmi~sqlite3+static~thread_multiple~wrapper-rpath
            fabrics=psm2 schedulers=slurm
          prefix: /usr/local/spack_soft/openmpi/4.0.2/gcc-8.3.1-n6vcsair26tkpepojy3c2gqxtqccijq3
          modules: [gcc/8.3.1, cuda-10.1.2, openmpi/4.0.2-cuda]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nonstandard Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once all dependencies are satisfied or if there are no dependencies, then the
prefix determined by Spack may not be correct in the presence of a nonstandard
directory structure. This is rarely the case because Spack contains
package-specific code to deal with these quirks. Before manually setting the
prefix in the ``packages.yaml`` file in addition to a list of modules, it is
strongly suggested to check the package name and the module list again. 

The files of OpenMPI on CentOS 7 use a nonstandard directory structure. For
example on x86-64, the libraries are in ``/usr/lib64/openmpi`` (on x86-64
machines) instead of ``/usr/lib64`` or ``/usr/lib``. Consider the ``module show
mpi`` output:

.. code-block:: console

    [john@c7 ~]# module show mpi
    -------------------------------------------------------------------
    /etc/modulefiles/mpi/openmpi-x86_64:

    conflict	 mpi
    prepend-path	 PATH /usr/lib64/openmpi/bin
    prepend-path	 LD_LIBRARY_PATH /usr/lib64/openmpi/lib
    prepend-path	 PYTHONPATH /usr/lib64/python2.7/site-packages/openmpi
    prepend-path	 MANPATH /usr/share/man/openmpi-x86_64
    [snip]

Given this module output, ``spack external find`` will determine
``/usr/lib64/openmpi`` as the prefix when only ``/usr`` allows Spack to
determine all required paths. This incorrect prefix can cause the error message
below when building packages::

    ==> Error: AttributeError: Query of package 'openmpi' for 'headers' failed
    	prefix : None
    	spec : openmpi@1.10.7%gcc@4.8.5~cuda+cxx_exceptions fabrics=none ~java~legacylaunchers~memchecker~pmi schedulers=none ~sqlite3~thread_multiple+vt arch=linux-centos7-x86_64
    	queried as : openmpi
    	extra parameters : []

The solution in this case is to manually edit the prefix in the
``packages.yaml`` file (here for CentOS 7):

.. code-block:: yaml

    packages:
      openmpi:
        externals:
        - spec: openmpi@1.10.7%gcc@4.8.5~cuda+cxx~cxx_exceptions~java~memchecker~pmi~sqlite3~static~thread_multiple~wrapper-rpath
          prefix: /usr
          modules: [mpi]

~~~~~~~~~~~
Metamodules
~~~~~~~~~~~

Consider the following ``module show`` output:

.. code-block:: console

    $ module show intel-all
    -------------------------------------------------------------------
    /gpfslocalsup/pub/module-rh/modulefiles/intel-all/2019.4:

    conflict        intel-all
    module          load intel-compilers/19.0.4
    module          load intel-mkl/19.0.4
    module          load intel-mpi/19.0.4
    module          load intel-vtune/19.0.4
    module          load intel-advisor/19.0.4
    module          load intel-tbb/19.0.4
    module          load intel-itac/19.0.4
    -------------------------------------------------------------------

The module ``intel-all`` is obviously a metamodule because it only loads other
modules; the module contents do not include direct manipulations of ``PATH``,
which Spack depends on to determine the package prefix. For this reason,
metamodules cannot generally be used in place of the direct package module when
defining external packages.


.. _concretization-preferences:

--------------------------
Concretization Preferences
--------------------------

Spack can be configured to prefer certain compilers, package
versions, dependencies, and variants during concretization.
The preferred configuration can be controlled via the
``~/.spack/packages.yaml`` file for user configurations, or the
``etc/spack/packages.yaml`` site configuration.

Here's an example ``packages.yaml`` file that sets preferred packages:

.. code-block:: yaml

   packages:
     opencv:
       compiler: [gcc@4.9]
       variants: +debug
     gperftools:
       version: [2.2, 2.4, 2.3]
     all:
       compiler: [gcc@4.4.7, 'gcc@4.6:', intel, clang, pgi]
       target: [sandybridge]
       providers:
         mpi: [mvapich2, mpich, openmpi]

At a high level, this example is specifying how packages should be
concretized.  The opencv package should prefer using GCC 4.9 and
be built with debug options.  The gperftools package should prefer version
2.2 over 2.4.  Every package on the system should prefer mvapich2 for
its MPI and GCC 4.4.7 (except for opencv, which overrides this by preferring GCC 4.9).
These options are used to fill in implicit defaults.  Any of them can be overwritten
on the command line if explicitly requested.

Each ``packages.yaml`` file begins with the string ``packages:`` and
package names are specified on the next level. The special string ``all``
applies settings to *all* packages. Underneath each package name is one
or more components: ``compiler``, ``variants``, ``version``,
``providers``, and ``target``.  Each component has an ordered list of
spec ``constraints``, with earlier entries in the list being preferred
over later entries.

Sometimes a package installation may have constraints that forbid
the first concretization rule, in which case Spack will use the first
legal concretization rule.  Going back to the example, if a user
requests gperftools 2.3 or later, then Spack will install version 2.4
as the 2.4 version of gperftools is preferred over 2.3.

An explicit concretization rule in the preferred section will always
take preference over unlisted concretizations.  In the above example,
xlc isn't listed in the compiler list.  Every listed compiler from
gcc to pgi will thus be preferred over the xlc compiler.

The syntax for the ``provider`` section differs slightly from other
concretization rules.  A provider lists a value that packages may
``depend_on`` (e.g, MPI) and a list of rules for fulfilling that
dependency.

.. _package_permissions:

-------------------
Package Permissions
-------------------

Spack can be configured to assign permissions to the files installed
by a package.

In the ``packages.yaml`` file under ``permissions``, the attributes
``read``, ``write``, and ``group`` control the package
permissions. These attributes can be set per-package, or for all
packages under ``all``. If permissions are set under ``all`` and for a
specific package, the package-specific settings take precedence.

The ``read`` and ``write`` attributes take one of ``user``, ``group``,
and ``world``.

.. code-block:: yaml

  packages:
    all:
      permissions:
        write: group
        group: spack
    my_app:
      permissions:
        read: group
        group: my_team

The permissions settings describe the broadest level of access to
installations of the specified packages. The execute permissions of
the file are set to the same level as read permissions for those files
that are executable. The default setting for ``read`` is ``world``,
and for ``write`` is ``user``. In the example above, installations of
``my_app`` will be installed with user and group permissions but no
world permissions, and owned by the group ``my_team``. All other
packages will be installed with user and group write privileges, and
world read privileges. Those packages will be owned by the group
``spack``.

The ``group`` attribute assigns a Unix-style group to a package. All
files installed by the package will be owned by the assigned group,
and the sticky group bit will be set on the install prefix and all
directories inside the install prefix. This will ensure that even
manually placed files within the install prefix are owned by the
assigned group. If no group is assigned, Spack will allow the OS
default behavior to go as expected.

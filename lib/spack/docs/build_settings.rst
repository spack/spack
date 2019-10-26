.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
       paths:
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7: /opt/openmpi-1.4.3
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7+debug: /opt/openmpi-1.4.3-debug
         openmpi@1.6.5%intel@10.1 arch=linux-x86_64-debian7: /opt/openmpi-1.6.5-intel

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
     modules:
       cmake@3.7.2: CMake/3.7.2

Each ``packages.yaml`` begins with a ``packages:`` token, followed
by a list of package names.  To specify externals, add a ``paths`` or ``modules``
token under the package name, which lists externals in a
``spec: /path`` or ``spec: module-name`` format.  Each spec should be as
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
       paths:
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7: /opt/openmpi-1.4.3
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7+debug: /opt/openmpi-1.4.3-debug
         openmpi@1.6.5%intel@10.1 arch=linux-x86_64-debian7: /opt/openmpi-1.6.5-intel
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

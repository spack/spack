.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _build-settings:

================================
Package Settings (packages.yaml)
================================

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

.. _concretizer-options:

----------------------
Concretizer options
----------------------

``packages.yaml`` gives the concretizer preferences for specific packages,
but you can also use ``concretizer.yaml`` to customize aspects of the
algorithm it uses to select the dependencies you install:

.. literalinclude:: _spack_root/etc/spack/defaults/concretizer.yaml
   :language: yaml

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Reuse already installed packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``reuse`` attribute controls whether Spack will prefer to use installed packages (``true``), or
whether it will do a "fresh" installation and prefer the latest settings from
``package.py`` files and ``packages.yaml`` (``false``).
You can use:

.. code-block:: console

   % spack install --reuse <spec>

to enable reuse for a single installation, and you can use:

.. code-block:: console

   spack install --fresh <spec>

to do a fresh install if ``reuse`` is enabled by default.

.. note::

   ``reuse: false`` is the current default, but ``reuse: true`` will be the default
   in the next Spack release. You will still be able to use ``spack install --fresh``
   to get the old behavior.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Selection of the target microarchitectures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The options under the ``targets`` attribute control which targets are considered during a solve.
Currently the options in this section are only configurable from the ``concretization.yaml`` file
and there are no corresponding command line arguments to enable them for a single solve.

The ``granularity`` option can take two possible values: ``microarchitectures`` and ``generic``.
If set to:

.. code-block:: yaml

   concretizer:
     targets:
       granularity: microarchitectures

Spack will consider all the microarchitectures known to ``archspec`` to label nodes for
compatibility. If instead the option is set to:

.. code-block:: yaml

   concretizer:
     targets:
       granularity: generic

Spack will consider only generic microarchitectures. For instance, when running on an
Haswell node, Spack will consider ``haswell`` as the best target in the former case and
``x86_64_v3`` as the best target in the latter case.

The ``host_compatible`` option is a Boolean option that determines whether or not the
microarchitectures considered during the solve are constrained to be compatible with the
host Spack is currently running on. For instance, if this option is set to ``true``, a
user cannot concretize for ``target=icelake`` while running on an Haswell node.

.. _package-preferences:

-------------------
Package Preferences
-------------------

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

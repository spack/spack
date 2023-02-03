.. Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

External packages are configured through the ``packages.yaml`` file.
Here's an example of an external configuration:

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

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prevent packages from being built from sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adding an external spec in ``packages.yaml`` allows Spack to use an external location,
but it does not prevent Spack from building packages from sources. In the above example,
Spack might choose for many valid reasons to start building and linking with the
latest version of OpenMPI rather than continue using the pre-installed OpenMPI versions.

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
its own version of OpenMPI from sources, and it will instead always rely on a pre-built
OpenMPI.

.. note::

   If ``concretizer:reuse`` is on (see :ref:`concretizer-options` for more information on that flag)
   pre-built specs include specs already available from a local store, an upstream store, a registered
   buildcache or specs marked as externals in ``packages.yaml``. If ``concretizer:reuse`` is off, only
   external specs in ``packages.yaml`` are included in the list of pre-built specs.

If an external module is specified as not buildable, then Spack will load the
external module into the build environment which can be used for linking.

The ``buildable`` does not need to be paired with external packages.
It could also be used alone to forbid packages that may be
buggy or otherwise undesirable.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Non-buildable virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Spack can then use any of the listed external implementations of MPI
to satisfy a dependency, and will choose depending on the compiler and
architecture.

In cases where the concretizer is configured to reuse specs, and other ``mpi`` providers
(available via stores or buildcaches) are not wanted, Spack can be configured to require
specs matching only the available externals:

.. code-block:: yaml

   packages:
     mpi:
       buildable: False
       require:
       - one_of: [
           "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64",
           "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug",
           "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         ]
     openmpi:
       externals:
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
         prefix: /opt/openmpi-1.4.3-debug
       - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
         prefix: /opt/openmpi-1.6.5-intel

This configuration prevents any spec using MPI and originating from stores or buildcaches to be reused,
unless it matches the requirements under ``packages:mpi:require``. For more information on requirements see
:ref:`package-requirements`.

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
``reuse: true`` is the default.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Selection of the target microarchitectures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The options under the ``targets`` attribute control which targets are considered during a solve.
Currently the options in this section are only configurable from the ``concretizer.yaml`` file
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

.. _package-requirements:

--------------------
Package Requirements
--------------------

Spack can be configured to always use certain compilers, package
versions, and variants during concretization through package
requirements.

Package requirements are useful when you find yourself repeatedly
specifying the same constraints on the command line, and wish that
Spack respects these constraints whether you mention them explicitly
or not. Another use case is specifying constraints that should apply
to all root specs in an environment, without having to repeat the
constraint everywhere.

Apart from that, requirements config is more flexible than constraints
on the command line, because it can specify constraints on packages
*when they occur* as a dependency. In contrast, on the command line it
is not possible to specify constraints on dependencies while also keeping
those dependencies optional.

The package requirements configuration is specified in ``packages.yaml``
keyed by package name:

.. code-block:: yaml

   packages:
     libfabric:
       require: "@1.13.2"
     openmpi:
       require:
       - any_of: ["~cuda", "%gcc"]
     mpich:
      require:
      - one_of: ["+cuda", "+rocm"]

Requirements are expressed using Spec syntax (the same as what is provided
to ``spack install``). In the simplest case, you can specify attributes
that you always want the package to have by providing a single spec to
``require``; in the above example, ``libfabric`` will always build
with version 1.13.2.

You can provide a more-relaxed constraint and allow the concretizer to
choose between a set of options using ``any_of`` or ``one_of``:

* ``any_of`` is a list of specs. One of those specs must be satisfied
  and it is also allowed for the concretized spec to match more than one.
  In the above example, that means you could build ``openmpi+cuda%gcc``,
  ``openmpi~cuda%clang`` or ``openmpi~cuda%gcc`` (in the last case,
  note that both specs in the ``any_of`` for ``openmpi`` are
  satisfied).
* ``one_of`` is also a list of specs, and the final concretized spec
  must match exactly one of them.  In the above example, that means
  you could build ``mpich+cuda`` or ``mpich+rocm`` but not
  ``mpich+cuda+rocm`` (note the current package definition for
  ``mpich`` already includes a conflict, so this is redundant but
  still demonstrates the concept).

.. note::

   For ``any_of`` and ``one_of``, the order of specs indicates a
   preference: items that appear earlier in the list are preferred
   (note that these preferences can be ignored in favor of others).

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setting default requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also set default requirements for all packages under ``all``
like this:

.. code-block:: yaml

   packages:
     all:
       require: '%clang'

which means every spec will be required to use ``clang`` as a compiler.

Note that in this case ``all`` represents a *default set of requirements* -
if there are specific package requirements, then the default requirements
under ``all`` are disregarded. For example, with a configuration like this:

.. code-block:: yaml

   packages:
     all:
       require: '%clang'
     cmake:
       require: '%gcc'

Spack requires ``cmake`` to use ``gcc`` and all other nodes (including ``cmake``
dependencies) to use ``clang``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setting requirements on virtual specs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A requirement on a virtual spec applies whenever that virtual is present in the DAG.
This can be useful for fixing which virtual provider you want to use:

.. code-block:: yaml

   packages:
     mpi:
       require: 'mvapich2 %gcc'

With the configuration above the only allowed ``mpi`` provider is ``mvapich2 %gcc``.

Requirements on the virtual spec and on the specific provider are both applied, if
present. For instance with a configuration like:

.. code-block:: yaml

   packages:
     mpi:
       require: 'mvapich2 %gcc'
     mvapich2:
       require: '~cuda'

you will use ``mvapich2~cuda %gcc`` as an ``mpi`` provider.

.. _package-preferences:

-------------------
Package Preferences
-------------------

In some cases package requirements can be too strong, and package
preferences are the better option. Package preferences do not impose
constraints on packages for particular versions or variants values,
they rather only set defaults -- the concretizer is free to change
them if it must due to other constraints. Also note that package
preferences are of lower priority than reuse of already installed
packages.

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

At a high level, this example is specifying how packages are preferably
concretized.  The opencv package should prefer using GCC 4.9 and
be built with debug options.  The gperftools package should prefer version
2.2 over 2.4.  Every package on the system should prefer mvapich2 for
its MPI and GCC 4.4.7 (except for opencv, which overrides this by preferring GCC 4.9).
These options are used to fill in implicit defaults.  Any of them can be overwritten
on the command line if explicitly requested.

Package preferences accept the follow keys or components under
the specific package (or ``all``) section: ``compiler``, ``variants``,
``version``, ``providers``, and ``target``.  Each component has an
ordered list of spec ``constraints``, with earlier entries in the
list being preferred over later entries.

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
``depends_on`` (e.g, MPI) and a list of rules for fulfilling that
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

----------------------------
Assigning Package Attributes
----------------------------

You can assign class-level attributes in the configuration:

.. code-block:: yaml

  packages:
    mpileaks:
      # Override existing attributes
      url: http://www.somewhereelse.com/mpileaks-1.0.tar.gz
      # ... or add new ones
      x: 1

Attributes set this way will be accessible to any method executed
in the package.py file (e.g. the ``install()`` method). Values for these
attributes may be any value parseable by yaml.

These can only be applied to specific packages, not "all" or
virtual packages.

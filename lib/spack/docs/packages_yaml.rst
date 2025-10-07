..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A guide to customizing package settings in Spack using the packages.yaml file, including configuring compilers, specifying external packages, package requirements, and permissions.

.. _packages-config:

Package Settings (packages.yaml)
================================

Spack allows you to customize how your software is built through the ``packages.yaml`` file.
Using it, you can make Spack prefer particular implementations of virtual dependencies (e.g., MPI or BLAS/LAPACK), or you can make it prefer to build with particular compilers.
You can also tell Spack to use *external* software installations already present on your system.

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

You can either set build preferences specifically for *one* package, or you can specify that certain settings should apply to *all* packages.
The types of settings you can customize are described in detail below.

Spack's build defaults are in the default ``etc/spack/defaults/packages.yaml`` file.
You can override them in ``~/.spack/packages.yaml`` or ``etc/spack/packages.yaml``.
For more details on how this works, see :ref:`configuration-scopes`.

.. _sec-external-packages:

External packages
-----------------

Spack can be configured to use externally-installed packages rather than building its own packages.
This may be desirable if machines ship with system packages, such as a customized MPI, which should be used instead of Spack building its own MPI.

External packages are configured through the ``packages.yaml`` file.
Here's an example of an external configuration:

.. code-block:: yaml

   packages:
     openmpi:
       externals:
       - spec: "openmpi@1.4.3~debug"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3+debug"
         prefix: /opt/openmpi-1.4.3-debug

This example lists two installations of OpenMPI, one with debug information, and one without.
If Spack is asked to build a package that uses one of these MPIs as a dependency, it will use the pre-installed OpenMPI in the given directory.
Note that the specified path is the top-level install prefix, not the ``bin`` subdirectory.

``packages.yaml`` can also be used to specify modules to load instead of the installation prefixes.
The following example says that module ``CMake/3.7.2`` provides cmake version 3.7.2.

.. code-block:: yaml

   cmake:
     externals:
     - spec: cmake@3.7.2
       modules:
       - CMake/3.7.2

Each ``packages.yaml`` begins with a ``packages:`` attribute, followed by a list of package names.
To specify externals, add an ``externals:`` attribute under the package name, which lists externals.
Each external should specify a ``spec:`` string that should be as well-defined as reasonably possible.
If a package lacks a spec component, such as missing a compiler or package version, then Spack will guess the missing component based on its most-favored packages, and it may guess incorrectly.


.. _cmd-spack-external-find:

Automatically find external packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run the :ref:`spack external find <spack-external-find>` command to search for system-provided packages and add them to ``packages.yaml``.
After running this command your ``packages.yaml`` may include new entries:

.. code-block:: yaml

   packages:
     cmake:
       externals:
       - spec: cmake@3.17.2
         prefix: /usr

Generally this is useful for detecting a small set of commonly-used packages; for now this is generally limited to finding build-only dependencies.
Specific limitations include:

* Packages are not discoverable by default: For a package to be discoverable with ``spack external find``, it needs to add special logic.
  See :ref:`here <make-package-findable>` for more details.
* The logic does not search through module files, it can only detect packages with executables defined in ``PATH``; you can help Spack locate externals which use module files by loading any associated modules for packages that you want Spack to know about before running ``spack external find``.
* Spack does not overwrite existing entries in the package configuration: If there is an external defined for a spec at any configuration scope, then Spack will not add a new external entry (``spack config blame packages`` can help locate all external entries).

Prevent packages from being built from sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adding an external spec in ``packages.yaml`` allows Spack to use an external location, but it does not prevent Spack from building packages from sources.
In the above example, Spack might choose for many valid reasons to start building and linking with the latest version of OpenMPI rather than continue using the pre-installed OpenMPI versions.

To prevent this, the ``packages.yaml`` configuration also allows packages to be flagged as non-buildable.
The previous example could be modified to be:

.. code-block:: yaml

   packages:
     openmpi:
       externals:
       - spec: "openmpi@1.4.3~debug"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3+debug"
         prefix: /opt/openmpi-1.4.3-debug
       buildable: false

The addition of the ``buildable`` flag tells Spack that it should never build its own version of OpenMPI from sources, and it will instead always rely on a pre-built OpenMPI.

.. note::

   If ``concretizer:reuse`` is on (see :ref:`concretizer-options` for more information on that flag) pre-built specs are taken from: the local store, an upstream store, a registered buildcache and externals in ``packages.yaml``.
   If ``concretizer:reuse`` is off, only external specs in ``packages.yaml`` are included in the list of pre-built specs.

If an external module is specified as not buildable, then Spack will load the external module into the build environment which can be used for linking.

The ``buildable`` attribute does not need to be paired with external packages.
It could also be used alone to forbid packages that may be buggy or otherwise undesirable.

Non-buildable virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Virtual packages in Spack can also be specified as not buildable, and external implementations can be provided.
In the example above, OpenMPI is configured as not buildable, but Spack will often prefer other MPI implementations over the externally available OpenMPI.
Spack can be configured with every MPI provider not buildable individually, but more conveniently:

.. code-block:: yaml

   packages:
     mpi:
       buildable: false
     openmpi:
       externals:
       - spec: "openmpi@1.4.3~debug"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3+debug"
         prefix: /opt/openmpi-1.4.3-debug

Spack can then use any of the listed external implementations of MPI to satisfy a dependency, and will choose among them depending on the compiler and architecture.

In cases where the concretizer is configured to reuse specs, and other ``mpi`` providers (available via stores or buildcaches) are not desirable, Spack can be configured to require specs matching only the available externals:

.. code-block:: yaml

   packages:
     mpi:
       buildable: false
       require:
       - one_of:
         - "openmpi@1.4.3~debug"
         - "openmpi@1.4.3+debug"
     openmpi:
       externals:
       - spec: "openmpi@1.4.3~debug"
         prefix: /opt/openmpi-1.4.3
       - spec: "openmpi@1.4.3+debug"
         prefix: /opt/openmpi-1.4.3-debug

This configuration prevents any spec using MPI and originating from stores or buildcaches to be reused, unless it matches the requirements under ``packages:mpi:require``.
For more information on requirements see :ref:`package-requirements`.


.. _extra-attributes-for-externals:

Extra attributes for external packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes external packages require additional attributes to be used effectively.
This information can be defined on a per-package basis and stored in the ``extra_attributes`` section of the external package configuration.
In addition to per-package information, this section can be used to define environment modifications to be performed whenever the package is used.
For example, if an external package is built without ``rpath`` support, it may require ``LD_LIBRARY_PATH`` settings to find its dependencies.
This could be configured as follows:

.. code-block:: yaml

   packages:
     mpich:
       externals:
       - spec: mpich@3.3 +hwloc
         prefix: /path/to/mpich
         extra_attributes:
           environment:
             prepend_path:
               LD_LIBRARY_PATH: /path/to/hwloc/lib64

See :ref:`configuration_environment_variables` for more information on how to configure environment modifications in Spack config files.

.. _configuring-system-compilers-as-external-packages:

Configuring system compilers as external packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Spack, compilers are treated as packages like any other.
This means that you can also configure system compilers as external packages and use them in Spack.

Spack automatically detects system compilers and configures them in ``packages.yaml`` for you.
You can also run :ref:`spack-compiler-find` to find and configure new system compilers.

When configuring compilers as external packages, you need to set a few :ref:`extra attributes <extra-attributes-for-externals>` for them to work properly.
The ``compilers`` extra attribute field is required to clarify which paths within the compiler prefix are used for which languages:

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

Other fields accepted by compilers under ``extra_attributes`` are ``flags``, ``environment``, ``extra_rpaths``, and ``implicit_rpaths``.

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
             cflags: -O3
             fflags: -g -O2
           environment:
             set:
               GCC_ROOT: /usr
             prepend_path:
               PATH: /usr/unusual_path_for_ld/bin
           implicit_rpaths:
           - /usr/lib/gcc
           extra_rpaths:
           - /usr/lib/unusual_gcc_path

The ``flags`` attribute specifies compiler flags to apply to every spec that depends on this compiler.
The accepted flag types are ``cflags``, ``cxxflags``, ``fflags``, ``cppflags``, ``ldflags``, and ``ldlibs``.
In the example above, every spec compiled with this compiler will pass the flags ``-g -O2`` to ``/usr/bin/gfortran-10`` and will pass the flag ``-O3`` to ``/usr/bin/gcc-10``.

The ``environment`` attribute specifies user environment modifications to apply before every time the compiler is invoked.
The available operations are ``set``, ``unset``, ``prepend_path``, ``append_path``, and ``remove_path``.
In the example above, Spack will set ``GCC_ROOT=/usr`` and set ``PATH=/usr/unusual_path_for_ld/bin:$PATH`` before handing control to the build system that will use this compiler.

The ``extra_rpaths`` and ``implicit_rpaths`` fields specify additional paths to pass as rpaths to the linker when using this compiler.
The ``implicit_rpaths`` field is filled in automatically by Spack when detecting compilers, and the ``extra_rpaths`` field is available for users to configure necessary rpaths that have not been detected by Spack.
In addition, paths from ``extra_rpaths`` are added as library search paths for the linker.
In the example above, both ``/usr/lib/gcc`` and ``/usr/lib/unusual_gcc_path`` would be added as rpaths to the linker, and ``-L/usr/lib/unusual_gcc_path`` would be added as well.

.. _package-requirements:
.. _package-strong-preferences:

Requirements, Preferences, and Conflicts
----------------------------------------

You can control how Spack selects versions, variants and providers during concretization using package requirements, preferences, and conflicts.

Package requirements are useful when you find yourself repeatedly specifying the same constraints on the command line or in Spack environments, and you wish that Spack respects these constraints whether you mention them explicitly or not.

Both **requirements** and **conflicts** are hard constraints that Spack must satisfy.
If they cannot be met, concretization will fail.

In contrast, **preferences** are softer constraints that Spack will satisfy if possible, but ignore if they conflict with other constraints.

Requirements, preferences and conflicts are among the highest priorities of the concretizer, and are taken into account before other factors, such as optimizing for reuse of already installed packages.

If you are looking for ways to influence Spack's concretization choices, but prefer reuse of existing installations above all else, consider using :ref:`weak package preferences <package-preferences>` instead.

.. seealso::

   FAQ: :ref:`Why does Spack pick particular versions and variants? <faq-concretizer-precedence>`


Basic Syntax and Examples
^^^^^^^^^^^^^^^^^^^^^^^^^

The package requirements, preferences and conflicts are specified in ``packages.yaml``, keyed by package name and expressed using the :doc:`spec syntax <spec_syntax>` under the ``require``, ``prefer`` and ``conflict`` attributes.

Here is a basic example that features all three types of constraints:

.. code-block:: yaml

   packages:
     cmake:
       require:
       - "@3.31:"
     libfabric:
       prefer:
       - "@2.2.0"
       conflict:
       - "fabrics=tcp"

With this configuration, Spack will:

1. always concretize ``cmake`` to version 3.31 or later,
2. prefer ``libfabric@2.2.0``, except when that version conflicts with other constraints,
3. never pick ``libfabric`` with the ``tcp`` fabric.

The ``require``, ``prefer``, and ``conflict`` attributes all accept lists of specs, even if only a single spec is specified.
The use of lists makes composition of constraints from :ref:`different configuration scopes <config-scope-precedence>` possible.
For instance, if you have the following instance-level configuration

.. code-block:: yaml
   :caption: ``$spack/etc/spack/packages.yaml``
   :name: instance-scope-preference

   packages:
     libfabric:
       prefer:
       - "%gcc"

and the following user-level configuration

.. code-block:: yaml
   :caption: ``~/.spack/packages.yaml``
   :name: user-scope-preference

   packages:
     libfabric:
       prefer:
       - "@2.2"

Spack merges configurations from different scopes by concatenating the lists for ``require``, ``prefer``, and ``conflict``.
In this case, the two separate lists are combined into one:

.. code-block:: yaml

   packages:
     libfabric:
       prefer:
       - "@2.2"
       - "%gcc"


preferring ``@2.2`` and ``%gcc`` independently.

The ability to specify multiple preferences in a list is useful, as each spec is treated as an independent preference.
For example, with ``prefer: ["@2.2", "%gcc"]``, Spack has two separate preferences for ``libfabric``: one for version ``@2.2`` and another for the ``gcc`` compiler.
If other constraints in a spec make it impossible to use ``@2.2``, Spack will still try to use ``%gcc``.

This is different from expressing the two as a single preference:

.. code-block:: yaml

   packages:
     libfabric:
       prefer:
       - "@2.2 %gcc"

Here, the preference is for the specific combination of version ``@2.2`` and dependency ``gcc``.
If that combination is not possible, the entire preference is disregarded.

.. _setting-requirements-on-virtual-specs:

Constraints on virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A requirement, preference or conflict on a virtual package applies whenever that virtual is present in the DAG.
This can be useful for choosing a particular provider for a virtual package.

.. code-block:: yaml

   packages:
     mpi:
       require: "mvapich2 %c,cxx,fortran=gcc"

With the configuration above the only allowed ``mpi`` provider is ``mvapich2`` with underlying compiler GCC.

Requirements on the virtual package and on the specific provider are both applied, if present.
For instance with a configuration like:

.. code-block:: yaml

   packages:
     mpi:
       require: "mvapich2 %c,cxx,fortran=gcc"
     mvapich2:
       require: "~cuda"

you will use ``mvapich2~cuda %c,cxx,fortran=gcc`` as an ``mpi`` provider.

A noteworthy use case for preferences on virtual packages is specifying compilers for languages, which are virtuals in Spack.

.. code-block:: yaml

   packages:
     c:
       prefer:
       - clang@20
     cxx:
       prefer:
       - clang@20
     fortran:
       prefer:
       - gcc@14

In this example, ``clang@20`` is preferred for C and C++, while ``gcc@14`` is preferred for Fortran.


Constraints on all packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can define preferences or conflicts that apply to any package under the ``all`` section of ``packages.yaml``.
At typical use case is setting the target architecture globally:

.. code-block:: yaml

   packages:
     all:
       prefer:
       - "target=zen2"

It can also be used for certain variants that are shared by many packages, such as ``cuda``:

.. code-block:: yaml

   packages:
     all:
       prefer:
       - "+cuda"

This makes the concretizer enable the ``cuda`` variant for every package that defines it, if possible.

Requirements can be set under ``all`` too, but their use cases are limited, since very few constraints can be meaningfully applied to every package.

Constraints under ``all`` are *overridden* by the corresponding settings of specific packages.
For example, if we want to prefer ``openblas@0.3:`` while generally preferring ``target=zen2`` for all packages, we have to repeat the target preference for ``openblas``:

.. code-block:: yaml

   packages:
     all:
       prefer:
       - "target=zen2"
     openblas:
       prefer:
       - "@0.3:"
       - "target=zen2"

This is because the package-specific ``prefer`` list for ``openblas`` *completely replaces* the ``prefer`` list from the ``all`` section.
The lists are not merged.
Therefore, if you want to retain a global preference like ``target`` while adding a package-specific one, you must repeat it in the package-specific section.

Conditional constraints
^^^^^^^^^^^^^^^^^^^^^^^

The ``require``, ``prefer`` and ``conflict`` attributes also accept a list of objects with ``spec`` and optionally ``when`` and ``message`` keys.
This allows for conditional requirements, preferences and conflicts that only apply when the ``when`` spec matches the concretized spec.

In the following example we require a certain compiler, but only for *older* versions of a package:

.. code-block:: yaml

   packages:
     openmpi:
       require:
       - spec: "%c,cxx,fortran=gcc"
         when: "@:4.1.4"
         message: "reason why only gcc can be used for older versions"

The ``message`` can be used to provide a custom error message if the requirement is not satisfiable.

Notice that conditional requirements give the concretizer two options:

1. either satisfy both the ``when`` condition and its associated ``spec``,
2. or ensure that the ``when`` condition is not satisfied.

The choice depends on the optimization criteria of the concretizer (see :ref:`spack-solve` for the current optimization criteria).

The second option is sometimes considered counter-intuitive, as the concretizer may choose to ignore a ``when`` condition rather than satisfy it.
For example, if an older package version is required only when using the default compiler, the concretizer may be more likely to pick a newer version with a non-default compiler, rather than an older version with the default compiler.


Choice rules in requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For more complex use cases, ``require`` also lets you define a choice between multiple specs.
This is done using the ``any_of`` or a ``one_of`` field (instead of a single ``spec`` field), which contains a list of specs.

``any_of``
""""""""""

A requirement with ``any_of`` is satisfied if the concretized spec matches *at least one* of the specs in the list.

.. code-block:: yaml

   packages:
     openmpi:
       require:
       - any_of: ["@4.1.5:", "%gcc"]
         message: "openmpi must be version 4.1.5+ or built with GCC"

In the above example, Spack must satisfy one of the following:

* Use ``openmpi`` version 4.1.5 or later
* Use the ``gcc`` compiler.

It is also allowed for the concretized spec to match more than one, for instance ``openmpi@4.1.5%gcc``.
However, a spec like ``openmpi@4.1.4%clang`` would fail, as it matches neither.
If the requirement is not satisfiable, Spack will print the custom error message:

.. code-block:: console

   $ spack spec openmpi@4.1.4%clang
   ==> Error: openmpi must be version 4.1.5+ or built with GCC

``one_of``
""""""""""

A requirement with ``one_of`` is satisfied if the concretized spec matches *exactly one* of the specs in the list.
This is useful for forcing a choice between mutually exclusive options.

.. code-block:: yaml

   packages:
     mpich:
       require:
       - one_of: ["+cuda", "+rocm"]

In this example, ``mpich`` must be built with either CUDA support or ROCm support, but not both.
A spec for ``mpich+cuda+rocm`` would fail to concretize.


.. note::

   For ``any_of`` and ``one_of``, the order of specs indicates a preference: items that appear earlier in the list are preferred (note that these preferences can be ignored in favor of others).

.. _package-preferences:

Weak Package Preferences
------------------------

Weak package preferences are low-priority hints that guide the concretizer when it has to build a new package.
They are designed to set convenient defaults without forcing unnecessary builds.

The defining rule for weak preferences is their relationship to package reuse: Spack will always prioritize reusing an already installed package (or one from a build cache) over building a new one to satisfy a weak preference.

This makes them the ideal tool for setting site-wide or personal defaults (like a preferred version or variant of a package) that should give way if a different, but still valid, version or variant is already available.
This is in direct contrast to :ref:`"strong" preferences <package-strong-preferences>`, which are treated as high-priority requests that take precedence over reuse.

.. seealso::

   FAQ: :ref:`Why does Spack pick particular versions and variants? <faq-concretizer-precedence>`

Weak preferences are set in ``packages.yaml`` using four specific attributes.
The ``version`` and ``variants`` attributes are set per-package, while ``target`` and ``providers`` are set globally under the ``all`` section.

The ``variants`` and ``version`` preferences can be set under package specific sections as follows:

.. code-block:: yaml

   packages:
     opencv:
       variants: +debug
     gperftools:
       version: [2.2, 2.4, 2.3]

In this case, the preference for ``opencv`` is to build with debug options, while ``gperftools`` prefers version 2.2 over 2.4, and 2.4 over 2.3, following the order of the list.
If the user requests ``gperftools@2.3:``, then Spack considers 2.4 the most preferred version, since 2.2 is ruled out by the version constraint.

The ``target`` and ``providers`` weak preferences can only be set globally under the ``all`` section of ``packages.yaml``:

.. code-block:: yaml

   packages:
     all:
       target: [x86_64_v3]
       providers:
         mpi: [mvapich2, mpich, openmpi]

These weak preferences override Spack's default and effectively reorder priorities when looking for the best target architecture or virtual package provider.
Each preference takes an ordered list of values, with earlier entries in the list being preferred over later entries.

In the example above all packages prefer to target the ``x86_64_v3`` microarchitecture and to use ``mvapich2`` if they depend on ``mpi``.

.. _package_permissions:

Package Permissions
-------------------

Spack can be configured to assign permissions to the files installed by a package.

In the ``packages.yaml`` file under ``permissions``, the attributes ``read``, ``write``, and ``group`` control the package permissions.
These attributes can be set per-package, or for all packages under ``all``.
If permissions are set under ``all`` and for a specific package, the package-specific settings take precedence.

The ``read`` and ``write`` attributes take one of ``user``, ``group``, and ``world``.

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

The permissions settings describe the broadest level of access to installations of the specified packages.
The execute permissions of the file are set to the same level as read permissions for those files that are executable.
The default setting for ``read`` is ``world``, and for ``write`` is ``user``.
In the example above, installations of ``my_app`` will be installed with user and group permissions but no world permissions, and owned by the group ``my_team``.
All other packages will be installed with user and group write privileges, and world read privileges.
Those packages will be owned by the group ``spack``.

The ``group`` attribute assigns a Unix-style group to a package.
All files installed by the package will be owned by the assigned group, and the sticky group bit will be set on the install prefix and all directories inside the install prefix.
This will ensure that even manually placed files within the install prefix are owned by the assigned group.
If no group is assigned, Spack will allow the OS default behavior to go as expected.

.. _assigning-package-attributes:

Assigning Package Attributes
----------------------------

You can assign class-level attributes in the configuration:

.. code-block:: yaml

   packages:
     mpileaks:
       package_attributes:
         # Override existing attributes
         url: http://www.somewhereelse.com/mpileaks-1.0.tar.gz
         # ... or add new ones
         x: 1

Attributes set this way will be accessible to any method executed in the package.py file (e.g. the ``install()`` method).
Values for these attributes may be any value parseable by yaml.

These can only be applied to specific packages, not "all" or virtual packages.

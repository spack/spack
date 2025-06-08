.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _repositories:

=================================
Package Repositories (repos.yaml)
=================================

Spack comes with thousands of built-in package recipes. As of Spack v1.0, these are hosted in a separate Git repository at `spack/spack-packages <https://github.com/spack/spack-packages>`_.

A **package repository** is a directory that Spack searches when it needs to find a package by name.
You may need to maintain packages for restricted, proprietary, or experimental software separately from the built-in repository.
Spack allows you to configure local and remote repositories using either the ``repos.yaml`` configuration file or the ``spack repo`` command.

This document describes how to set up and manage these package repositories.

---------------------------------------------
Structure of an Individual Package Repository
---------------------------------------------

An individual Spack package repository is a directory structured as follows::

  /path/to/repos/                   # the top-level dir is added to the Python search path
    spack_repo/                     # every package repository is part of the spack_repo Python module
      myrepo/                       # directory for the 'myrepo' repository (matches namespace)
        repo.yaml                   # configuration file for this package repository
        packages/                   # directory containing package directories
          hdf5/                     # directory for the hdf5 package
            package.py              # the package recipe file
          mpich/                    # directory for the mpich package
            package.py              # the package recipe file
            mpich-1.9-bugfix.patch  # example patch file
          trilinos/
            package.py
      ...

* ``repo.yaml``.
  This file contains metadata for this specific repository, for example:
  
  .. code-block:: yaml

    repo:
      namespace: myrepo
      api: v2.0

  It defines primarily:

  * ``namespace``.
    A unique identifier for this repository (e.g., ``myrepo``, ``projectx``).
    See the :ref:`Namespaces <namespaces>` section for more details.
  * ``api``.
    The version of the Spack Package API this repository adheres to (e.g., ``v2.0``).
    Spack itself defines what range of API versions it supports, and will error if it encounters a repository with an unsupported API version.

* ``packages/``.
  This directory contains subdirectories for each package in the repository.
  Each package directory contains a ``package.py`` file and any patches or other files needed to build the package.

Package repositories allow you to:

1. Maintain your own packages separately from Spack's built-in set.
2. Share your packages (e.g., by hosting them on a shared file system or in a Git repository) without committing them to the main ``spack/spack-packages`` repository.
3. Override built-in Spack packages with your own implementations.

Packages in a separate repository can also *depend on* built-in Spack packages, allowing you to leverage existing recipes without re-implementing them.

Package Names
^^^^^^^^^^^^^

Package names are defined by the directory names under ``packages/``.
In the example above, the package names are ``hdf5``, ``mpich``, and ``trilinos``.
Package names can only contain lowercase characters ``a-z``, digits ``0-9`` and hyphens ``-``.

.. note::

   Package names are **derived** from the directory names under ``packages/``.
   Package directories are required to be valid Python module names, which means they cannot contain hyphens or start with a digit.
   This means that a package named ``my-package`` would be stored in a directory named ``my_package/``, and a package named ``7zip`` would be stored in a directory named ``_7zip/`` with an underscore prefix to make it a valid Python module name.
   The mapping between package names and directory names is one-to-one.
   Use ``spack list`` to see how Spack resolves the package names from the directory names.

--------------------------------------------
Configuring Repositories with ``repos.yaml``
--------------------------------------------

Spack uses ``repos.yaml`` files found in its :ref:`configuration scopes <configuration>` (e.g., ``~/.spack/``, ``etc/spack/``) to discover and prioritize package repositories. Note that this ``repos.yaml`` (plural) configuration file is distinct from the ``repo.yaml`` (singular) file within each individual package repository.

Spack supports two main types of repository configurations:

Local Repositories (Path-based)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can point Spack to a repository on your local filesystem:

.. code-block:: yaml

  # Example: ~/.spack/repos.yaml
  repos:
    my_local_packages: /path/to/my_repository_root

Here, ``/path/to/my_repository_root`` should be the directory containing that repository's ``repo.yaml`` and ``packages/`` subdirectory.

Git-based Repositories
^^^^^^^^^^^^^^^^^^^^^^

Spack can clone and use repositories directly from Git URLs:

.. code-block:: yaml

  repos:
    my_remote_repo: https://github.com/myorg/spack-custom-pkgs.git

**Automatic Cloning.**
When Spack first encounters a Git-based repository configuration, it automatically clones it. By default, these repositories are cloned into a subdirectory within ``~/.spack/package_repos/``, named with a hash of the repository URL.

To change directories to the package repository, you can use ``spack cd --repo [name]``. To find where a repository is cloned, you can use ``spack location --repo [name]`` or ``spack repo list``. The ``name`` argument is optional; if omitted, Spack will use the first package repository in configuration order.

**Customizing Clone Location.**
The default clone location (``~/.spack/package_repos/<hashed_name>``) might not be convenient for package maintainers who want to make changes to packages. You can specify a custom local directory for Spack to clone a Git repository into, or to use if the repository is already cloned there. This is done using the ``destination`` key in ``repos.yaml`` or via the ``spack repo set --destination`` command (see :ref:`cmd-spack-repo-set-destination`).

For example, to use ``~/custom_packages_clone`` for ``my_remote_repo``:

.. code-block:: yaml

  # ~/.spack/repos.yaml
  repos:
    my_remote_repo:
      git: https://github.com/myorg/spack-custom-pkgs.git
      destination: ~/custom_packages_clone

If the ``git`` URL is defined in a lower-precedence configuration (like Spack's defaults for ``builtin``), you only need to specify the ``destination`` in your user-level ``repos.yaml``. Spack can make the configuration changes for you using ``spack repo set --destination ~/spack-packages builtin``, or you can directly edit your ``repos.yaml`` file:

.. code-block:: yaml

  # ~/.spack/repos.yaml
  repos:
    builtin:
      destination: ~/spack-packages

**Updating and pinning.**
There is currently no automatic update mechanism for Git-based repositories in Spack.
Additionally, package repositories cannot be pinned to a specific commit or branch in configuration files.
We are still gathering feedback and use cases from the community to determine the best approach for these features.
For now, we encourage users to update Git repositories manually, by navigating to the clone directory ``spack cd --repo`` or ``spack cd --repo [name]`` and using standard Git commands (e.g., ``git pull`` to get the latest changes, or ``git checkout <commit|tag>`` to switch to a specific version).

**Git repositories need a package repo index.**
A single Git repository can contain one or more Spack package repositories. To enable Spack to discover these, the root of the Git repository should contain a ``spack-repo-index.yaml`` file. This file lists the relative paths to package repository roots within the git repo.

For example, assume a Git repository at ``https://example.com/my_org/my_pkgs.git`` has the following structure::

  my_pkgs.git/
    spack-repo-index.yaml     # metadata file at the root of the Git repo
    ...
    spack_pkgs/
      spack_repo/
        my_org/
          comp_sci_packages/  # package repository for computer science packages
            repo.yaml
            packages/
              hdf5/
                package.py
              mpich/
                package.py
          physics_packages/   # package repository for physics packages
            repo.yaml
            packages/
              gromacs/
                package.py

The ``spack-repo-index.yaml`` in the root of ``https://example.com/my_org/my_pkgs.git`` should look like this:

.. code-block:: yaml

  # my_pkgs.git/spack-repo-index.yaml
  repo_index:
    paths:
    - spack_pkgs/spack_repo/my_org/comp_sci_packages
    - spack_pkgs/spack_repo/my_org/physics_packages

If ``my_pkgs.git`` is configured in ``repos.yaml`` as follows:

.. code-block:: yaml

  # ~/.spack/repos.yaml
  repos:
    example_mono_repo: https://example.com/my_org/my_pkgs.git

Spack will clone ``my_pkgs.git`` and look for ``spack-repo-index.yaml``. It will then register two separate repositories based on the paths found (e.g., ``<clone_dir>/spack_pkgs/spack_repo/my_org/comp_sci_packages`` and ``<clone_dir>/spack_pkgs/spack_repo/my_org/physics_packages``), each with its own namespace defined in its respective ``repo.yaml`` file. Thus, one ``repos.yaml`` entry for a Git mono-repo can lead to *multiple repositories* being available to Spack.

If you want only one of the package repositories from a Git mono-repo, you can override the paths in your user-level ``repos.yaml``. For example, if you only want the computer science packages:

.. code-block:: yaml
   
   # ~/.spack/repos.yaml
   repos:
     example_mono_repo:
       git: https://example.com/my_org/my_pkgs.git
       paths:
       - spack_pkgs/spack_repo/my_org/comp_sci_packages

The ``spack repo add`` command can help you set up these configurations easily.

The ``builtin`` Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack's extensive collection of built-in packages resides at `spack/spack-packages <https://github.com/spack/spack-packages>`_.
By default, Spack is configured to use this as a Git-based repository. The default configuration in ``$spack/etc/spack/defaults/repos.yaml`` looks something like this:

.. code-block:: yaml

  repos:
    builtin:
      git: https://github.com/spack/spack-packages.git

.. _namespaces:

----------
Namespaces
----------

Every repository in Spack has an associated **namespace** defined in the ``namespace:`` key of its top-level ``repo.yaml`` file.
For example, the built-in repository (from ``spack/spack-packages``) has its namespace defined as ``builtin``:

.. code-block:: yaml

  # In spack/spack-packages repository's repo.yaml
  repo:
    namespace: builtin
    api: v2.0 # Or newer

Spack records the repository namespace of each installed package. For example, if you install the ``mpich`` package from the ``builtin`` repo, Spack records its fully qualified name as ``builtin.mpich``. This accomplishes two things:

1.  You can have packages with the same name from different namespaces installed simultaneously.
2.  You can easily determine which repository a package came from after it is installed (more :ref:`below <namespace-example>`).

.. note::

   The ``namespace`` defined in the package repository's ``repo.yaml`` is the **authoritative source** for the namespace. It is *not* derived from the local configuration in ``repos.yaml``. This means that the namespace is determined by the repository maintainer, not by the user or local configuration.

Nested Namespaces for Organizations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we have already seen in the Git-based package repositories example above, you can create nested namespaces by using periods in the namespace name.
For example, a repository for packages related to computation at LLNL might have the namespace ``llnl.comp``, while one for physical and life sciences could be ``llnl.pls``.
On the file system, this requires a directory structure like this::

  /path/to/repos/
    spack_repo/
      llnl/
        comp/
          repo.yaml  # Contains namespace: llnl.comp
          packages/
            mpich/
              package.py
        pls/
          repo.yaml  # Contains namespace: llnl.pls
          packages/
            hdf5/
              package.py

Uniqueness
^^^^^^^^^^

Spack cannot ensure global uniqueness of all namespaces, but it will prevent you from registering two repositories with the same namespace *at the same time* in your current configuration. If you try to add a repository that has the same namespace as an already registered one, Spack will print a warning and may ignore the new addition or apply specific override logic depending on the configuration.

.. _namespace-example:

Namespace Example
^^^^^^^^^^^^^^^^^

Suppose LLNL maintains its own version of ``mpich`` (in a repository with namespace ``llnl.comp``), separate from Spack's built-in ``mpich`` package (namespace ``builtin``). If you've installed both, ``spack find`` alone might be ambiguous:

.. code-block:: console

  $ spack find
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  mpich@3.2  mpich@3.2

Using ``spack find -N`` displays packages with their namespaces:

.. code-block:: console

  $ spack find -N
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  builtin.mpich@3.2  llnl.comp.mpich@3.2

Now you can distinguish them.
Packages differing only by namespace will have different hashes:

.. code-block:: console

  $ spack find -lN
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  c35p3gc builtin.mpich@3.2  itoqmox llnl.comp.mpich@3.2

All Spack commands that take a package :ref:`spec <sec-specs>` also accept a fully qualified spec with a namespace, allowing you to be specific:

.. code-block:: console

  spack uninstall llnl.comp.mpich

-------------------------------------
Search Order and Overriding Packages
-------------------------------------

When Spack resolves an unqualified package name (e.g., ``mpich`` in ``spack install mpich``), it searches the configured repositories in the order they appear in the *merged* ``repos.yaml`` configuration (from highest to lowest precedence scope, and top to bottom within each file).
The first repository found that provides the package will be used.
For Git-based mono-repos, the individual repositories listed in its ``spack-repo-index.yaml`` are effectively inserted into this search order based on the mono-repo's position.

This search order allows you to override built-in packages.
If you have your own ``mpich`` in a repository ``my_custom_repo``, and ``my_custom_repo`` is listed before ``builtin`` in your ``repos.yaml``, Spack will use your version of ``mpich`` by default.

Suppose your effective (merged) ``repos.yaml`` implies the following order:
1.  ``proto`` (local repo at ``~/my_spack_repos/spack_repo/proto_repo``)
2.  ``llnl`` (local repo at ``/usr/local/repos/spack_repo/llnl_repo``)
3.  ``builtin`` (Spack's default packages from `spack/spack-packages`)

And the packages are:
  +--------------+------------------------------------------------+-----------------------------+
  | Namespace    | Source                                         | Packages                    |
  +==============+================================================+=============================+
  | ``proto``    | ``~/my_spack_repos/spack_repo/proto_repo``     | ``mpich``                   |
  +--------------+------------------------------------------------+-----------------------------+
  | ``llnl``     | ``/usr/local/repos/spack_repo/llnl_repo``      | ``hdf5``                    |
  +--------------+------------------------------------------------+-----------------------------+
  | ``builtin``  | `spack/spack-packages` (Git)                   | ``mpich``, ``hdf5``, others |
  +--------------+------------------------------------------------+-----------------------------+

If ``hdf5`` depends on ``mpich``:

* ``spack install hdf5`` will install ``llnl.hdf5 ^proto.mpich``.
  Spack finds ``hdf5`` first in ``llnl``.
  For its dependency ``mpich``, Spack searches again from the top, finding ``mpich`` first in ``proto``.

You can force a particular repository's package using a fully qualified name:

* ``spack install hdf5 ^builtin.mpich`` will install ``llnl.hdf5 ^builtin.mpich``.
* ``spack install builtin.hdf5 ^builtin.mpich`` will install ``builtin.hdf5 ^builtin.mpich``.

To see which repositories will be used for a build *before* installing, use ``spack spec -N``:

.. code-block:: console

   $ spack spec -N hdf5
   llnl.hdf5@1.10.0
       ^proto.mpich@3.2
       ^builtin.zlib@1.2.8

.. warning::

   While you *can* use a fully qualified package name in a ``depends_on`` directive within a ``package.py`` file (e.g., ``depends_on("proto.hdf5")``), this is **strongly discouraged**.
   It makes the package non-portable and tightly coupled to a specific repository configuration, hindering sharing and composition of repositories.
   A package will fail to load if the hardcoded namespace's repository is not registered.

.. _cmd-spack-repo:

--------------------------
The ``spack repo`` Command
--------------------------

Spack provides commands to manage your repository configurations.

.. _cmd-spack-repo-list:

``spack repo list``
^^^^^^^^^^^^^^^^^^^^^^

This command shows all repositories Spack currently knows about, including their namespace, API version, and resolved path (local path or clone directory for Git repos).

.. code-block:: console

  $ spack repo list
  [+] my_local           v2.0    /path/to/spack_repo/my_local_packages
  [+] comp_sci_packages  v2.0    ~/.spack/package_repos/<hash 1>/spack_pkgs/spack_repo/comp_sci_packages
  [+] physics_packages   v2.0    ~/.spack/package_repos/<hash 1>/spack_pkgs/spack_repo/physics_packages  # From the same git repo
  [+] builtin            v2.0    ~/.spack/package_repos/<hash 2>/repos/spack_repo/builtin

Spack shows a green ``[+]`` next to each repository that is available for use.
It shows a red ``[-]`` to indicate that package repositories cannot be used due to an error (e.g., unsupported API version, missing ``repo.yaml``, etc.).
It can also show just a gray ``-`` if it is a Git-based package repository that has not been cloned yet.

Note that for Git-based package repositories, ``spack repo list`` will show entries for *each* individual package repository registered via ``spack-repo-index.yaml``.
This contrasts with ``spack config get repos``, which shows the raw configuration from ``repos.yaml`` files, including just the Git URL for a mono-repo:

.. code-block:: console

   $ spack config get repos
   repos:
     my_local_packages: /path/to/spack_repo/my_local_packages
     example_mono_repo: https://example.com/my_org/my_pkgs.git # contains two package repositories
     builtin:
       git: https://github.com/spack/spack-packages.git
       # destination: /my/custom/path (if set by user)

.. _cmd-spack-repo-create:

``spack repo create``
^^^^^^^^^^^^^^^^^^^^^

To create the directory structure for a new, empty local repository:

.. code-block:: console

  $ spack repo create ~/my_spack_projects myorg.projectx
  ==> Created repo with namespace 'myorg.projectx'.
  ==> To register it with spack, run this command:
    spack repo add ~/my_spack_projects/spack_repo/myorg/projectx

This command creates the following structure::

  ~/my_spack_projects/
    spack_repo/
      myorg/
        projectx/
          repo.yaml      # Contains namespace: myorg.projectx
          packages/      # Empty directory for new package.py files

The ``<target_dir>`` is where the ``spack_repo/<namespace_parts>`` hierarchy will be created.
The ``<namespace>`` can be simple (e.g., ``myrepo``) or nested (e.g., ``myorg.projectx``), and Spack will create the corresponding directory structure.

.. _cmd-spack-repo-add:

``spack repo add``
^^^^^^^^^^^^^^^^^^

To register package repositories from local paths or a remote Git repositories with Spack:

* **For a local path:**
  Provide the path to the repository's root directory (the one containing ``repo.yaml`` and ``packages/``).

  .. code-block:: console

     $ spack repo add ~/my_spack_projects/spack_repo/myorg/projectx
     ==> Added repo to config with name 'myorg.projectx'.

* **For a Git repository:**
  Provide the Git URL.

  .. code-block:: console

     $ spack repo add --name my_pkgs https://github.com/spack/spack-packages.git ~/my_pkgs
     Cloning into '/home/user/my_pkgs'...
     ==> Added repo to config with name 'my_pkgs'.

  Notice that for Git-based package repositories, you need to specify a configuration name explicitly, which is the key used in your ``repos.yaml`` configuration file.
  The example also shows providing a custom destination path ``~/my_pkgs``.
  You can omit this if you want Spack to use the default clone location (e.g., ``~/.spack/package_repos/<hashed_name>``).

After adding, packages from this repository should appear in ``spack list`` and be installable.

.. _cmd-spack-repo-remove:

``spack repo remove``
^^^^^^^^^^^^^^^^^^^^^

To unregister a repository, use its configuration name (the key in ``repos.yaml``) or its local path.

By configuration name (e.g., ``projectx`` from the add example):

.. code-block:: console

  $ spack repo remove projectx
  ==> Removed repository 'projectx'.

By path (for a local repo):

.. code-block:: console

  $ spack repo remove ~/my_spack_projects/spack_repo/myorg/projectx
  ==> Removed repository '/home/user/my_spack_projects/spack_repo/myorg/projectx'.

This command removes the corresponding entry from your ``repos.yaml`` configuration.
It does *not* delete the local repository files or any cloned Git repositories.

.. _cmd-spack-repo-set-destination:

``spack repo set``
^^^^^^^^^^^^^^^^^^

For Git-based repositories, this command allows you to specify a custom local directory where Spack should clone the repository, or use an existing clone.
The ``<config_name>`` is the key used in your ``repos.yaml`` file for that Git repository (e.g., ``builtin``, ``my_remote_repo``).

.. code-block:: console

  $ spack repo set --destination /my/custom/path/for/spack-packages builtin
  ==> Updated repo 'builtin'

This updates your user-level ``repos.yaml``, adding or modifying the ``destination:`` key for the specified repository configuration name.

.. code-block:: yaml

  # ~/.spack/repos.yaml after the command
  repos:
    builtin:
      destination: /my/custom/path/for/spack-packages
      # The 'git:' URL is typically inherited from Spack's default configuration for 'builtin'

Spack will then use ``/my/custom/path/for/spack-packages`` for the ``builtin`` repository.
If the directory doesn't exist, Spack will clone into it.
If it exists and is a valid Git repository, Spack will use it.

--------------------------------
Repository Namespaces and Python
--------------------------------

Package repositories in Spack (from ``api: v2.0`` or newer) are structured to integrate smoothly with Python's import system.
They are effectively Python namespace packages under the top-level ``spack_repo`` namespace.

The ``api: v2.0`` repository structure ensures that packages can be imported using a standard Python module path: ``spack_repo.<namespace>.packages.<package_name>.package``.
For instance, the ``mpich`` package from the ``builtin`` repository corresponds to the Python module ``spack_repo.builtin.packages.mpich.package``.

This allows you to easily extend or subclass package classes from other repositories in your own ``package.py`` files:

.. code-block:: python

   # In your custom repository (e.g., namespace 'mycustom')
   # in a package file, e.g., mycustom_mpich/package.py

   from spack.package_base import PackageBase # Or other base class
   # Import the original Mpich class from the 'builtin' repository
   from spack_repo.builtin.packages.mpich.package import Mpich as BuiltinMpich

   class MycustomMpich(BuiltinMpich):
       # Override versions, variants, or methods from BuiltinMpich
       version("3.5-custom", sha256="...")

       # Add a new variant
       variant("custom_feature", default=False, description="Enable my custom feature")

       def install(self, spec, prefix):
           if "+custom_feature" in spec:
               # Do custom things
               pass
           super().install(spec, prefix) # Call parent install method

Spack manages Python's ``sys.path`` at runtime to make these imports discoverable across all registered repositories.
This capability is powerful for creating derivative packages or slightly modifying existing ones without copying entire package files.
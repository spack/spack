.. _repositories:

=============================
Local Package Repositories
=============================

Spack comes with over 1,000 builtin package recipes in the
``var/spack/repos/builtin/`` directory.  This is a **package
repository**, a directory that Spack searches when it needs to find a
package by name.  By default, the :ref:`cmd-spack-edit` and
:ref:`cmd-spack-create` commands modify packages in the builtin
repository.  You may need to maintain a set of packages **separate** from
the builtin repository, for private, proprietary, export-controlled, or
otherwise restricted software. Spack allows you to configure local
repositories using either the ``repos.yaml`` or the ``spack repo``
command.

A package repository is simply a directory structured like this::

  repo/
      repo.yaml
      packages/
          hdf5/
              package.py
          mpich/
              package.py
              mpich-1.9-bugfix.patch
          trilinos/
              package.py
          ...

The top-level ``repo.yaml`` file contains configuration metadata for the
repository, and the ``packages`` directory contains subdirectories for
each package in the repository.  Each package directory contains a
``package.py`` file and any patches or other files needed to build the
package.


---------------------
``repos.yaml``
---------------------

Spack finds repositories by looking at the ``repos.yaml`` configuration
file.  For more on the YAML format, and on how configuration file
precedence works in Spack, :ref:`see configuration <configuration>`.  By
default, ``repos.yaml`` looks like this:

.. code-block:: yaml

  repos:
  - $spack/var/spack/repos/builtin

The file starts with ``repos:`` and contains a single ordered list
(denoted by ``-``).  You can add a repository by inserting another
element into this list:

.. code-block:: yaml

  repos:
  - /opt/local-repo
  - $spack/var/spack/repos/builtin

When you install a package with Spack, it searches these directories in
order for an appropriate ``package.py`` file.  For example, if you type
``spack install mpich``, Spack looks first in
``/opt/local-repo/packages/mpich``, then in
``$spack/var/spack/repos/builtin/packages/mpich``, and uses the first
valid package it finds.

.. _note:

  Currently, Spack only knows how to deal with repositories in the local
  file system. Eventually we plan to support putting URLs in
  ``repos.yaml`` so that you can easily host remote package repositories,
  but that support is not implemented yet.

---------------------
Namespaces
---------------------

Every repository in Spack has an associated **namespace** defined in its
top-level ``repo.yaml`` file.  The namespace serves only to distinguish
packages from different repositories.  If you look at the contents of
``var/spack/repos/builtin/repo.yaml`` in the builtin repository, you'll
see that its namespace is ``builtin``:

.. code-block:: console

  $ cat var/spack/repos/builtin/repo.yaml
  repo:
    namespace: builtin

The namespace doesn't **have** to correspond to the repository directory
name; it's just convenient in this case.

If you make a repository for packages from your organization, you might
use your organization's name.  You can also nest namespaces using
periods.  For example, LLNL might use a namespace for its internal
repositories like ``llnl``. Packages from the Physical & Life Sciences
directorate (PLS) might use the ``llnl.pls`` namespace, and packages
created by the computation directorate might use ``llnl.comp``.

You can have packages with the same name from different namespaces
installed at once.  For example, LLNL might maintain its own version of
``mpich`` separate from Spack's builtin ``mpich`` package.  If you just
use ``spack find``, you won't see a difference between these two
packages:

.. code-block:: console

  $ spack find
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  mpich@3.2  mpich@3.2

However, if you use ``spack find -N``, Spack will display the packages
with their namespaces:

.. code-block:: console

  $ spack find -N
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  builtin.mpich@3.2  llnl.comp.mpich@3.2

As you might guess, packages that are identical save for their namespace
will still have different hashes:

.. code-block:: console

  $ spack find -lN
  ==> 2 installed packages.
  -- linux-rhel6-x86_64 / gcc@4.4.7 -------------
  c35p3gc builtin.mpich@3.2  itoqmox llnl.comp.mpich@3.2

All Spack commands that take a package :ref:`spec <sec-specs>` can also
accept a qualified spec with a namespace, so you can use the namespace to
be more specific when designating, e.g., which package to uninstall:

.. code-block:: console

  spack uninstall llnl.comp.mpich

Or, if you have your own repository registered and you want to **force**
spack to use the ``builtin`` implementation of ``mpich`` for a certain
build of ``hdf5``, you could do this:

.. code-block:: console

  spack install hdf5 +mpi ^llnl.comp.mpich

---------------------
Listing repositories
---------------------

Spack's :ref:`configuration system <configuration>` allows repository
settings to come from ``repos.yaml`` files in many locations.  If you
want to see the repositories registered as a result of all configuration
files, use ``spack repo list``.

.. _cmd-spack-repo-list:

^^^^^^^^^^^^^^^^^^^
``spack repo list``
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

  $ spack repo list
  ==> 2 package repositories.
  myrepo     /Users/gamblin2/myrepo
  builtin    /Users/gamblin2/src/spack/var/spack/repos/builtin

Each repository is listed with its associated namespace.

---------------------
Creating a repository
---------------------

To make your own repository, you don't need to construct a directory
yourself; you can use the ``spack repo create`` command.

.. _cmd-spack-repo-create:

^^^^^^^^^^^^^^^^^^^^^
``spack repo create``
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

  $ spack repo create myrepo
  ==> Created repo with namespace 'myrepo'.
  ==> To register it with spack, run this command:
    spack repo add /Users/gamblin2/myrepo

  $ ls myrepo
  packages/  repo.yaml

  $ cat myrepo/repo.yaml
  repo:
    namespace: 'myrepo'

By default, the namespace of a new repo matches its directory's name.
You can supply a custom namespace with a second argument, e.g.:

  $ spack repo create myrepo llnl.comp
  ==> Created repo with namespace 'llnl.comp'.
  ==> To register it with spack, run this command:
    spack repo add /Users/gamblin2/myrepo

  $ cat myrepo/repo.yaml
  repo:
    namespace: 'llnl.comp'

----------------------------------------
Adding and removing package repositories
----------------------------------------

.. _cmd-spack-repo-add:

^^^^^^^^^^^^^^^^^^
``spack repo add``
^^^^^^^^^^^^^^^^^^

Once your repository is created, you can register it with Spack with
``spack repo add``:

.. code-block:: console

   $ spack repo add ./myrepo
   ==> Added repo with namespace 'llnl.comp'.

   $ spack repo list
   ==> 2 package repositories.
   llnl.comp    /Users/gamblin2/myrepo
   builtin      /Users/gamblin2/src/spack/var/spack/repos/builtin

This simply adds the repo to your ``repos.yaml`` file.

Once a repository is registered like this, you should be able to see its
packages' names in the output of ``spack list``, and you should be able
to build them using ``spack install <name>`` as you would with any
builtin package.

.. _cmd-spack-repo-rm:

^^^^^^^^^^^^^^^^^
``spack repo rm``
^^^^^^^^^^^^^^^^^

You can remove an already-registered repository with ``spack repo rm``.
This will work whether you pass the repository's namespace **or** its
path.

By namespace:

.. code-block:: console

  $ spack repo rm llnl.comp
  ==> Removed repository /Users/gamblin2/myrepo with namespace 'llnl.comp'.

  $ spack repo list
  ==> 1 package repository.
  builtin    /Users/gamblin2/src/spack/var/spack/repos/builtin

By path:

.. code-block:: console

  $ spack repo rm ~/myrepo
  ==> Removed repository /Users/gamblin2/myrepo

  $ spack repo list
  ==> 1 package repository.
  builtin    /Users/gamblin2/src/spack/var/spack/repos/builtin

..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A developer reference for the lockfile format of Spack environments, describing its structure, its compatibility across releases, and its version history.

.. _lockfile-format:

Lockfile Format
===============

This document describes the lockfile format, which stores the result of concretizing an environment as JSON: the roots of the environment, and every concrete spec they depend on.
The current version of the format is |lockfile_version|, defined by :data:`spack.environment.environment.CURRENT_LOCKFILE_VERSION`.

A lockfile is found in ``<environment>/spack.lock``, next to the ``spack.yaml`` it was concretized from.

Structure
---------

This section describes the current version of the format, |lockfile_version|.
A lockfile holds the version of the format, the roots of the environment, and one node for each concrete spec:

.. code-block:: json

   {
     "_meta": {
       "file-type": "spack-lockfile",
       "lockfile-version": 8,
       "specfile-version": 6
     },
     "spack": {
       "version": "1.3.0.dev0",
       "type": "git",
       "commit": "c7c444853d"
     },
     "roots": [
       {"hash": "nic37xsihlqze3xyg3xd6pthcgqxoy6p", "spec": "zlib-ng"}
     ],
     "concrete_specs": {
       "nic37xsihlqze3xyg3xd6pthcgqxoy6p": {
         "name": "zlib-ng",
         "version": "2.3.3",
         "provided_virtuals": ["zlib-api"],
         "dependencies": [
           {
             "name": "gcc",
             "hash": "26zpexhcroz5n23vbzm5ypre7tlfus2b",
             "parameters": {"deptypes": ["build"], "virtuals": ["c", "cxx"]}
           }
         ],
         "annotations": {"original_specfile_version": 6},
         "hash": "nic37xsihlqze3xyg3xd6pthcgqxoy6p"
       }
     }
   }

To keep the example short, most keys of the node and the remaining nodes are not shown.

A lockfile is a dictionary with the following keys.
The keys of previous versions are described in :ref:`lockfile-version-history`.

``_meta``
   ``file-type`` is always ``spack-lockfile``, and ``lockfile-version`` is the version of the format.
   ``specfile-version`` is the version of the spec file format of the nodes.
   It is informational, and is not used when the lockfile is read.
``spack``
   The version of Spack that wrote the lockfile.
   ``type`` is ``git`` when Spack is run from a git repository, in which case ``commit`` is also present, and ``release`` otherwise.
``roots``
   The roots of the environment, in order.
   Each entry has ``spec``, the abstract spec that was concretized, and ``hash``, the DAG hash of the result.
   It also has ``group``, the group of the root, when the environment defines groups other than the default one.
``concrete_specs``
   One node dictionary for each node of the environment, keyed by DAG hash, as described in :ref:`specfile-format`.
   For a spliced spec, the nodes of the build spec are also included.
``include_concrete``
   The ``roots`` and ``concrete_specs`` of each included concrete environment, keyed by the path of that environment.
   It is present only when the environment includes concrete environments, and it is nested when those include others.

Compatibility
-------------

.. admonition:: A lockfile in an older version is converted only when the environment changes
   :class: warning

   Spack reads a lockfile in an older version without modifying it, and commands that do not change the roots or the concrete specs of the environment leave the file as it is.
   A command that changes them, such as ``spack concretize`` after ``spack add``, or that concretizes the roots again, writes the lockfile in the current version, after which older versions of Spack can no longer read it.

The properties below are defined in :ref:`file-formats`.

**Backward compatibility**
   Every version of Spack reads all the versions of the format up to its own.
   Lockfiles before version 4 are keyed by older hashes, and when Spack reads them it identifies each spec by its current DAG hash.

**Forward compatibility**
   None.
   Reading a version newer than the current one is an error.

**Rewrite policy**
   A lockfile is rewritten, in the current version, when a root is concretized, or when the roots, their hashes, their groups, or the included concrete environments differ from what was read.
   Lockfiles before version 4 are always rewritten on the next write, and a version 1 lockfile is copied to ``spack.lock.backup.v1`` when it is read.

The following table lists the lockfile versions that each release of Spack can read:

.. list-table:: Lockfile versions read by each release
   :header-rows: 1

   * - Spack
     - v1
     - v2
     - v3
     - v4
     - v5
     - v6
     - v7
     - v8
   * - v0.12
     - ✅
     -
     -
     -
     -
     -
     -
     -
   * - v0.13 to v0.16
     - ✅
     - ✅
     -
     -
     -
     -
     -
     -
   * - v0.17
     - ✅
     - ✅
     - ✅
     -
     -
     -
     -
     -
   * - v0.18 to v0.20
     - ✅
     - ✅
     - ✅
     - ✅
     -
     -
     -
     -
   * - v0.21 to v0.23
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     -
     -
     -
   * - v1.0 to v1.1
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     -
     -
   * - v1.2
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     -
   * - v1.3 (in development)
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅

.. _lockfile-version-history:

Version History
---------------

The version is recorded in ``_meta.lockfile-version``.
Each version of the lockfile is associated with one version of the spec file, which is used to read every node, including those in ``include_concrete``.

**Version 8** *(Spack v1.3)*
   Nodes are in spec file v6, which includes the virtuals provided by each node (`#53012 <https://github.com/spack/spack/pull/53012>`_).
   A lockfile is rewritten only when its content changes (`#53048 <https://github.com/spack/spack/pull/53048>`_).
   Up to Spack v1.2, every write of the environment rewrote the lockfile in the current version.

**Version 7** *(Spack v1.2)*
   Roots have the ``group`` key (`#51891 <https://github.com/spack/spack/pull/51891>`_).
   The roots of a lockfile in an older version are assigned to the default group when they are read.
   Nodes are in spec file v5, as in version 6.

**Version 6** *(Spack v1.0)*
   Nodes are in spec file v5, where compilers are build dependencies (`#45189 <https://github.com/spack/spack/pull/45189>`_).

**Version 5** *(Spack v0.21)*
   Nodes are in spec file v4, where virtuals are recorded on the edges of the DAG (`#34821 <https://github.com/spack/spack/pull/34821>`_).
   The ``include_concrete`` key was added in Spack v0.22, without a new version (`#33768 <https://github.com/spack/spack/pull/33768>`_).

**Version 4** *(Spack v0.18)*
   The build hash is removed (`#28504 <https://github.com/spack/spack/pull/28504>`_).
   Nodes are in spec file v3, and are keyed by the DAG hash that includes build dependencies and the package hash.
   The ``spack`` key was added in Spack v0.20, without a new version (`#32801 <https://github.com/spack/spack/pull/32801>`_).

**Version 3** *(Spack v0.17)*
   Nodes are in spec file v2 (`#22845 <https://github.com/spack/spack/pull/22845>`_, `#25879 <https://github.com/spack/spack/pull/25879>`_).
   They are keyed by build hash as in version 2, and their dependencies are referred to by ``build_hash``.
   The ``_meta.specfile-version`` key is added.

**Version 2** *(Spack v0.13)*
   Nodes are in spec file v1, as in version 1.
   They are keyed by build hash, and have a ``hash`` key with their DAG hash.
   Dependencies are referred to by DAG hash.
   Since installations are identified by the DAG hash, which at this time does not include build dependencies, a lockfile in version 2 or 3 can have several nodes with the same DAG hash.
   When Spack reads such a lockfile, it keeps the first of these nodes that is reached from the roots.

**Version 1** *(Spack v0.12)*
   Nodes are in spec file v1, and are keyed by the DAG hash, which includes only link and run dependencies.
   The nodes have no ``hash`` key.

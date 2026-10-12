..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A developer reference for the Spack Database format, describing its structure, its compatibility across releases, how an index is converted with spack reindex, and its version history.

.. _database-format:

Database Format
===============

This document describes the Database format, which stores the specs installed in an install tree as JSON, together with their prefix and whether they were installed explicitly.
The current version of the format is |db_version|, defined by ``spack.database._DB_VERSION``.

An index in the Database format is found in the following places:

* In ``<install_tree:root>/.spack-db/index.json``, for the install tree in use and for each upstream.
* In build caches, where the index lists the specs available in the build cache.

Structure
---------

This section describes the current version of the format, |db_version|.
An index has a single top-level ``database`` key, which holds the version of the format and one record for each spec:

.. code-block:: json

   {
     "database": {
       "version": "9",
       "installs": {
         "nic37xsihlqze3xyg3xd6pthcgqxoy6p": {
           "spec": {
             "name": "zlib-ng",
             "version": "2.3.3",
             "dependencies": [
               {"name": "glibc", "hash": "cyucshxqmd4krmsp7nco25trnybrdbam", "parameters": {"deptypes": ["link"], "virtuals": ["libc"]}}
             ],
             "hash": "nic37xsihlqze3xyg3xd6pthcgqxoy6p"
           },
           "ref_count": 0,
           "path": "/opt/spack/linux-alderlake/zlib-ng-2.3.3-nic37xsihlqze3xyg3xd6pthcgqxoy6p",
           "installed": true,
           "explicit": true,
           "installation_time": 1759400000.0
         }
       }
     }
   }

To keep the example short, most keys of ``spec`` and the remaining records are not shown.

The version is a string.
The records are keyed by DAG hash, and their order is not significant.
Besides the installed specs, the index has records for specs that are not installed: dependencies that have no prefix, and deprecated specs.
Each record is a dictionary with the following keys:

``spec``
   The node dictionary of the spec, as described in :ref:`specfile-format`.
   Each dependency is referred to by its DAG hash, and has a record of its own in the same index, or in the index of an upstream.
``ref_count``
   The number of records that depend on this one, plus the number of records deprecated in favor of it.
``path``
   The installation prefix, or the prefix of an external.
``installed``
   Whether the spec is installed.
``explicit``
   Whether the spec was installed explicitly, or only as a dependency.
``installation_time``
   The time of the installation, in seconds since the epoch.
``deprecated_for``
   The DAG hash of the spec that replaces this one.
   It is present only in specs deprecated with ``spack deprecate``.
``origin``
   The value ``external-db``, for externals read from an external manifest.
   It is not present in other records.

The index of a build cache has only the keys ``spec``, ``ref_count``, and ``in_buildcache`` in each record.

A JSON schema of the format is in ``lib/spack/spack/schema/database_index.py``.

Compatibility
-------------

.. admonition:: An index in an older version is converted only by ``spack reindex``
   :class: warning

   Spack reads an index in an older version without modifying it, and commands that would modify it fail with an error that requests ``spack reindex``.
   After ``spack reindex``, the versions of Spack that wrote the previous index can no longer read it.

The properties below are defined in :ref:`file-formats`.

**Backward compatibility**
   An index in version 6 or later is read in place, so commands that only read the Database, such as ``spack find``, work on it.
   An index in version 5 or earlier is an error for every command.

**Forward compatibility**
   None.
   Reading a version newer than the current one is an error.

**Rewrite policy**
   An index in an older version is never rewritten implicitly.
   Commands that modify the Database, such as ``spack install`` or ``spack uninstall``, check the version before starting any work.

.. rubric:: Converting an index with ``spack reindex``

``spack reindex`` writes a new index from the ``spec.json`` files of the installation prefixes, and keeps a copy of the previous one:

.. code-block:: console

   $ spack reindex
   ==> Created a backup copy of the DB at
     /opt/spack/.spack-db/index.json.bkp
   ==> The DB at /opt/spack/.spack-db/index.json has been reindexed to v9
     If you need to restore, replace it with the backup.

If Spack can read the previous index, the values of ``explicit``, ``installation_time``, ``origin``, and ``deprecated_for`` are copied from its records.
Otherwise, every spec found in the install tree is recorded as explicitly installed.
Specs that are in the previous index and have no prefix are kept, and are recorded as not installed.

.. rubric:: Upstreams and build caches

The index of an upstream is never written, so Spack cannot convert it.
It is read in place if it is in version 6 or later, and it is an error otherwise.

The index of a build cache follows the same rules when it is in an older version.
An index in a version newer than the current one is not used, and Spack emits a warning.

.. _database-version-history:

Version History
---------------

The version is recorded in ``database.version``.
Each version of the Database is associated with one version of the spec file, which is used to read the ``spec`` of every record.

**Version 9** *(Spack v1.3)*
   Records store spec file v6 nodes, which include the virtuals provided by each node (`#53012 <https://github.com/spack/spack/pull/53012>`_).
   An index in an older version is read in place, and writes to it are refused (`#53045 <https://github.com/spack/spack/pull/53045>`_).

**Version 8** *(Spack v1.0)*
   Records store spec file v5 nodes, where compilers are build dependencies (`#45189 <https://github.com/spack/spack/pull/45189>`_).
   An index in an older version is an error for every command, including those that only read the Database.

**Version 7** *(Spack v0.21)*
   Records store spec file v4 nodes, where virtuals are recorded on the edges of the DAG (`#34821 <https://github.com/spack/spack/pull/34821>`_).

**Version 6** *(Spack v0.17)*
   Records store spec file v2 nodes (`#22845 <https://github.com/spack/spack/pull/22845>`_).
   Spack v0.18 to v0.20 write the same version with spec file v3 nodes, which have the same structure.

**Version 5** *(Spack v0.13)*
   The version becomes an integer, and records can have the ``deprecated_for`` key (`#13410 <https://github.com/spack/spack/pull/13410>`_).
   Records store spec file v1 nodes.

**Versions 0.9 to 0.9.3** *(Spack v0.12 and earlier)*
   Version 0.9 is written by Spack v0.9, and version 0.9.2 by Spack v0.10.
   Version 0.9.3, written by Spack v0.11 and v0.12, adds externals to the Database (`#1167 <https://github.com/spack/spack/pull/1167>`_).

Up to Spack v0.23, an index in an older version was converted automatically: it was either reindexed when read, or read and rewritten in the current version on the next write.

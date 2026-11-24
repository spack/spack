..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A developer reference for the Spack spec file format, describing its structure, how the DAG hash is computed, its compatibility across releases, and its version history.

.. _specfile-format:

Spec File Format
================

This document describes the spec file format, which stores the DAG of a spec as JSON.
The current version of the format is |specfile_format_version|, defined by :data:`spack.spec.SPECFILE_FORMAT_VERSION`.

Spec files are found in the following places:

* In ``<prefix>/.spack/spec.json``, written when a spec is installed.
  ``spack reindex`` rebuilds the Database from these files.
* In build caches, where a few keys specific to build caches are added to the spec file.
* In the output of ``spack spec --json``.

The Database and the lockfile store the nodes of a spec file without the enclosing ``spec`` and ``_meta`` keys, as described in :ref:`file-formats`.

All of these files hold concrete specs, and the rest of this document describes concrete specs.

.. admonition:: Abstract specs
   :class: note

   The format can also represent abstract specs, which are written only in the entries of the concretization cache, for troubleshooting, and are not read back.
   The nodes of an abstract spec have ``"concrete": false``, and may have the keys ``abstract_hash``, ``compiler_flags``, ``propagate``, ``abstract``, ``propagated_parameters``, and ``propagated_abstract``; their dependencies may have ``when`` and ``propagation``.
   None of these keys is written for concrete specs, so they do not affect the DAG hash.

Structure
---------

This section describes the current version of the format, |specfile_format_version|.
A spec file has a single top-level ``spec`` key, which holds the version of the format and the list of nodes:

.. code-block:: json

   {
     "spec": {
       "_meta": {"version": 6},
       "nodes": [
         {
           "name": "zlib-ng",
           "version": "2.3.3",
           "arch": {"platform": "linux", "platform_os": "ubuntu24.04", "target": {"name": "alderlake"}},
           "namespace": "builtin",
           "parameters": {"build_system": "autotools", "shared": true, "cflags": []},
           "package_hash": "bnbx7ezlmmjgjyubhncgeel7lpbjrj6l4aeuhyewdeyz56l7tqsq====",
           "provided_virtuals": ["zlib-api"],
           "dependencies": [
             {
               "name": "gcc",
               "hash": "26zpexhcroz5n23vbzm5ypre7tlfus2b",
               "parameters": {"deptypes": ["build"], "virtuals": ["c", "cxx"]}
             },
             {
               "name": "glibc",
               "hash": "cyucshxqmd4krmsp7nco25trnybrdbam",
               "parameters": {"deptypes": ["link"], "virtuals": ["libc"]}
             }
           ],
           "annotations": {"original_specfile_version": 6},
           "hash": "nic37xsihlqze3xyg3xd6pthcgqxoy6p"
         }
       ]
     }
   }

To keep the example short, the features of the target, most variants, the remaining dependencies, and the remaining nodes are not shown.

The first node of the list is the root of the DAG.
The order of the remaining nodes is not significant, since nodes refer to each other by hash.
Each node is listed once, even if it can be reached through several paths.
For a spliced spec, the list also includes the nodes of the build spec.

Each node is a dictionary with the following keys.
The keys of previous versions are described in :ref:`specfile-version-history`.

``name``, ``version``, ``arch``, ``namespace``
   The identity of the node.
``parameters``
   The values of the variants, and the compiler flags.
``patches``
   The hashes of the patches applied to the node, in the order in which they are applied.
   It is present only in nodes that have patches.
``package_hash``
   The hash of the content of the ``package.py`` that the node was concretized with.
``provided_virtuals``
   The virtuals that a concrete node provides, possibly with a version, for instance ``libgfortran@5``.
   It is written only when the node provides at least one virtual.
``dependencies``
   One entry for each edge, which refers to the dependency by name and DAG hash.
   The ``parameters`` of the entry hold the dependency types, the virtuals that the dependency provides on that edge, and ``direct: true`` for direct dependencies.
``build_spec``
   The name and DAG hash of the spec that was built.
   It is present only in spliced specs.
``external``
   The path or the modules of an external, and its extra attributes.
   It is present only in externals.
``annotations``
   ``original_specfile_version`` is the version of the spec file from which the node was first read.
   Nodes first read from a spec file before v5 also have ``compiler``, the compiler that those versions stored as a node attribute.
``hash``
   The DAG hash of the node.

A JSON schema of the format is in ``lib/spack/spack/schema/spec.py``.

How the DAG Hash Is Computed
----------------------------

The DAG hash of a concrete node is computed in two steps:

1. The node dictionary, without the ``hash`` key, is serialized as JSON with no whitespace, and with the keys in the order in which they are written.
2. The SHA-1 digest of the serialization is encoded in base32, in lowercase.

This definition has the following consequences:

* The node dictionary contains the hashes of the dependencies, so the DAG hash depends on the entire sub-DAG.
* Any change to what Spack writes for a concrete node, including the order of its keys, gives a different hash to every spec concretized afterwards.

The hash stored in a spec file is never recomputed when the file is read.
Spack can therefore read a spec written with an older definition of the hash, and still find the installation it refers to.
The changes to the definition are listed in :ref:`specfile-version-history`.

.. rubric:: Spliced specs

The hash of a spliced spec is computed in the same way, except that its last 7 characters are replaced by those of the hash of its build spec.
A spliced spec is installed by relocating the binaries of its build spec to a new prefix, and relocation has to leave the end of the prefix unchanged.
The reason is that compilers save space by storing a string constant as the suffix of a longer one, so rewriting the end of a path in a binary could alter an unrelated string that shares it.
With the default layout the prefix ends with the hash, hence the two hashes have the same ending.

Compatibility
-------------

The properties below are defined in :ref:`file-formats`.

**Backward compatibility**
   Every version of Spack reads all the versions of the format up to its own.
   When reading an older version, Spack reconstructs the information that the version does not store from the package repositories.

**Forward compatibility**
   None.
   Reading a version newer than the current one is an error.

**Rewrite policy**
   Spec files are never rewritten.
   The ``spec.json`` file of an installation prefix remains in the version it was written in.
   When a node read from an older version is written to a new file, its original version is recorded in ``annotations.original_specfile_version``.

.. _specfile-version-history:

Version History
---------------

The version is recorded in ``spec._meta.version``.
Spec files in version 1 have no ``_meta`` key, and are recognized because their ``spec`` key holds a list.

**Version 6** *(Spack v1.3)*
   Concrete nodes record the virtuals they provide in ``provided_virtuals``, which is part of the DAG hash (`#53012 <https://github.com/spack/spack/pull/53012>`_).

**Version 5** *(Spack v1.0)*
   Compilers become build dependencies (`#45189 <https://github.com/spack/spack/pull/45189>`_).
   The ``compiler`` attribute of nodes is removed, ``annotations`` is added, and ``parameters.direct`` marks direct dependencies.
   From Spack v1.0 on, the DAG hash also includes test dependencies (`#49505 <https://github.com/spack/spack/pull/49505>`_).
   The ``abstract`` key was added for abstract specs before the release of Spack v1.0 (`#49756 <https://github.com/spack/spack/pull/49756>`_).
   The keys ``abstract_hash``, ``compiler_flags``, ``when``, and ``propagation`` were added later for abstract specs, without a new version (`#52788 <https://github.com/spack/spack/pull/52788>`_).
   The keys ``propagated_parameters`` and ``propagated_abstract`` were added in the same way (`#52963 <https://github.com/spack/spack/pull/52963>`_).

**Version 4** *(Spack v0.21)*
   Virtuals are recorded on the edges of the DAG (`#34821 <https://github.com/spack/spack/pull/34821>`_).
   The dependency types of each entry move to ``parameters.deptypes``, next to the new ``parameters.virtuals``.
   The ``propagate`` key was added in Spack v0.23 for abstract specs, without a new version (`#47351 <https://github.com/spack/spack/pull/47351>`_).

**Version 3** *(Spack v0.18)*
   The build hash and the full hash are removed (`#28504 <https://github.com/spack/spack/pull/28504>`_).
   The structure is the same as in version 2, and ``hash`` becomes the DAG hash that includes build dependencies and the package hash.
   In versions 1 and 2 the DAG hash includes only link and run dependencies.

**Version 2** *(Spack v0.17)*
   Installation prefixes move from ``spec.yaml`` to ``spec.json`` (`#22845 <https://github.com/spack/spack/pull/22845>`_).
   The ``_meta.version`` key is added, ``nodes`` becomes a list of dictionaries with a ``name`` key, ``dependencies`` becomes a list, and ``build_spec`` is added.

**Version 1** *(Spack v0.16 and earlier)*
   Spec files are YAML (``spec.yaml``), or JSON with the same structure.
   The ``spec`` key holds a list with one ``{<name>: <node>}`` entry for each node.
   Dependencies are a dictionary keyed by name, with the hash of the dependency and its ``type``.
   The hash of the dependency is stored under ``hash``, ``full_hash``, or ``build_hash``, depending on the version of Spack that wrote the file.

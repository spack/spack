..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A developer reference for the layout of Spack build caches, describing its structure, its compatibility across releases, and its version history.

.. _buildcache-format:

Build Cache Layout
==================

This document describes the build cache layout, which determines where binary packages, their spec files, the index, and the public keys are stored in a mirror.
The current version of the layout is |buildcache_layout_version|, defined by ``spack.url_buildcache.CURRENT_BUILD_CACHE_LAYOUT_VERSION``.

The layout is used by build caches on a filesystem and on URLs such as ``https://`` and ``s3://``.
Build caches in OCI registries do not use it.

Structure
---------

This section describes the current version of the layout, |buildcache_layout_version|.
A build cache has a directory of manifests, named after the version of the layout, and a directory of blobs:

.. code-block:: text

   <mirror>/
     v3/
       layout.json
       manifests/
         spec/
           zlib-ng/
             zlib-ng-2.3.3-nic37xsihlqze3xyg3xd6pthcgqxoy6p.spec.manifest.json
         index/
           index.manifest.json
         key/
           75BC0528114909C076E2607418010FFAD73C9B07.key.manifest.json
           keys.manifest.json
     blobs/
       sha256/
         0f/
           0f24aa6b5dd7150067349865217acd3f6a383083f9eca111d2d2fed726c88210

``layout.json`` records how the build cache is signed, and its presence indicates that the mirror has a build cache in this version of the layout.
Every other file, apart from the manifests, is stored as a blob named after its checksum.
A manifest lists the blobs that belong to one entity, which is a binary package, the index, a public key, or the index of the public keys:

.. code-block:: json

   {
     "version": 3,
     "data": [
       {
         "contentLength": 10731083,
         "mediaType": "application/vnd.spack.install.v2.tar+gzip",
         "compression": "gzip",
         "checksumAlgorithm": "sha256",
         "checksum": "0f24aa6b5dd7150067349865217acd3f6a383083f9eca111d2d2fed726c88210"
       },
       {
         "contentLength": 1000,
         "mediaType": "application/vnd.spack.spec.v6+json",
         "compression": "gzip",
         "checksumAlgorithm": "sha256",
         "checksum": "fba751c4796536737c9acbb718dad7429be1fa485f5585d450ab8b25d12ae041"
       }
     ]
   }

A manifest is a dictionary with the following keys:

``version``
   The version of the layout.
``data``
   One entry for each blob.
   ``checksumAlgorithm`` and ``checksum`` give the location of the blob, which is ``blobs/<algorithm>/<first two characters of the checksum>/<checksum>``.
   ``mediaType`` identifies the content of the blob and the version of its format.
   ``compression`` is ``gzip`` or ``none``, and ``contentLength`` is the size of the blob in bytes.

The manifest of a binary package can be signed, in which case the file is a clearsigned document that contains the JSON above.

The media types tie the layout to the other formats:

.. list-table:: Media types of the blobs
   :header-rows: 1

   * - Blob
     - Media type
     - Format
   * - Spec file
     - ``application/vnd.spack.spec.vN+json``
     - A spec file in version N, as described in :ref:`specfile-format`.
   * - Index
     - ``application/vnd.spack.db.vN+json``
     - An index in version N of the Database format, as described in :ref:`database-format`.
   * - Binary package
     - ``application/vnd.spack.install.v2.tar+gzip``
     - A tarball of the installation prefix.
   * - Public key
     - ``application/pgp-keys``
     - A public key used to verify signed manifests.
   * - Index of the public keys
     - ``application/vnd.spack.keyindex.v1+json``
     - The list of the public keys in the build cache.

The manifest of the index can list several indexes with different media types, so that versions of Spack with different Database versions can use the same build cache.

A complete description of the layout, with an example of each kind of manifest, is in :ref:`Build Cache Layout <build_cache_layout>`.
A JSON schema of the manifest is in ``lib/spack/spack/schema/url_buildcache_manifest.py``.

Compatibility
-------------

.. admonition:: A build cache can be shared by versions of Spack with different spec file and Database versions
   :class: tip

   Each version of Spack writes spec files and the index with the media type of its own versions, and reads every media type it supports.
   An older version of Spack keeps using the entries it can read, and does not use the ones pushed by a newer version.

The properties below are defined in :ref:`file-formats`.

**Backward compatibility**
   Spack reads build caches in the previous version of the layout, version 2, and emits a deprecation warning.
   Within the current layout, it reads spec files from ``spec.v5`` and indexes from ``db.v8``.

**Forward compatibility**
   None.
   A blob with a media type newer than the ones Spack supports is not used.
   A build cache in a newer version of the layout is not read, since Spack only looks in the directories of the versions it supports.

**Rewrite policy**
   A build cache is never rewritten in place.
   A build cache in version 2 of the layout is converted by ``spack buildcache migrate``, which writes the new layout next to the previous one.
   Spack no longer writes version 2.
   When Spack pushes an index, it keeps the indexes with other media types that are already listed in the manifest.

.. _buildcache-version-history:

Version History
---------------

The version is recorded in the ``version`` key of every manifest, and in the name of the directory that contains the manifests.

**Version 3** *(Spack v1.0)*
   Every file is a blob stored under its checksum, and is located through a manifest (`#48713 <https://github.com/spack/spack/pull/48713>`_).
   The manifests are in ``v3/manifests/``, and their media types include the version of the spec file and of the Database.
   ``spack buildcache migrate`` is added, and build caches in version 2 can be read but not written.
   From Spack v1.3 on, the manifest of the index keeps the indexes of other Database versions (`#53094 <https://github.com/spack/spack/pull/53094>`_).

**Version 2** *(Spack v0.22)*
   The tarball of a binary package includes the parent directories of the installation prefix (`#41773 <https://github.com/spack/spack/pull/41773>`_).
   The files are in the same places as in version 1.

**Version 1** *(Spack v0.18)*
   The signature is applied to the spec file, and the ``.spack`` file is the tarball of the installation prefix (`#30750 <https://github.com/spack/spack/pull/30750>`_).
   All the files are in ``build_cache/``, with the public keys in ``build_cache/_pgp/``.

Before version 1, the ``.spack`` file was an archive that contained the spec file, the signature, and the tarball of the installation prefix.

In versions 1 and 2 the version is recorded in the ``buildcache_layout_version`` key of each spec file.
Spec files in the current layout still have this key, with the value ``2``.

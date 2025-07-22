.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

Spack Package API v2.2
======================

This document describes the Spack Package API (:mod:`spack.package`), the stable interface for Spack package authors.
It is assumed you have already read the :doc:`Spack Packaging Guide <packaging_guide_creation>`.

The Spack Package API is the *only* module from the Spack codebase considered public API.
It re-exports essential functions and classes from various Spack modules, allowing package authors to import them directly from :mod:`spack.package` without needing to know Spack's internal structure.

Spack Package API Versioning
----------------------------

The current Package API version is |package_api_version|, defined in :attr:`spack.package_api_version`.
Notice that the Package API is versioned independently from Spack itself:

* The **minor version** is incremented when new functions or classes are exported from :mod:`spack.package`.
* The **major version** is incremented when functions or classes are removed or have breaking changes to their signatures (a rare occurrence).

This independent versioning allows package authors to utilize new Spack features without waiting for a new Spack release.

Compatibility between Spack and :doc:`package repositories <repositories>` is managed as follows:

* Package repositories declare their minimum required Package API version in their ``repo.yaml`` file using the ``api: vX.Y`` format.
* Spack checks if the declared API version falls within its supported range, specifically between :attr:`spack.min_package_api_version` and :attr:`spack.package_api_version`.

Spack version |spack_version| supports package repositories with a Package API version between |min_package_api_version| and |package_api_version|, inclusive.

Spack Package API Reference
---------------------------

.. automodule:: spack.package
   :members:
   :show-inheritance:
   :undoc-members:
   :no-value:

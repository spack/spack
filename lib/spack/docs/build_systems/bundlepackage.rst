.. Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _bundlepackage:

------
Bundle
------

``BundlePackage`` represents a set of packages that are expected to work
well together, such as a collection of commonly used software libraries.
The associated software is specified as bundle dependencies.

If it makes sense, variants and conflicts can be added to the package.
Variants could ensure that common build options are consistent across
the packages supporting them. Conflicts are used to prevent builds with
known bugs or issues. For example, if the bundle is known to only build
on ``linux`` then conflicts can be added, such as:

.. code-block:: python

    for platform in ["cray", "darwin", "windows"]:
        conflicts(f"platform={platform}", msg="Only builds on linux")


^^^^^^^^
Creation
^^^^^^^^

Be sure to specify the ``bundle`` template if you are using ``spack create``
to generate a package from the template.  For example, use the following
command to create a bundle package whose class name will be ``Mybundle``:

.. code-block:: console

    $ spack create --template bundle --name mybundle



^^^^^^
Phases
^^^^^^

The ``BundlePackage`` base class does not provide any phases by default
since the bundle does not represent a build system.


^^^
URL
^^^

The ``url`` property does not have meaning since there is no package-specific
code to fetch.


^^^^^^^
Version
^^^^^^^

At least one ``version`` must be specified in order for the package to
build.

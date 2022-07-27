.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _bundlepackage:

-------------
BundlePackage
-------------

``BundlePackage`` represents a set of packages that are expected to work well
together, such as a collection of commonly used software libraries.  The
associated software is specified as bundle dependencies.


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

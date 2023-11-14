.. Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

==========================
Frequently Asked Questions
==========================

-------------------------------------------------------
What determines what versions and variants Spack picks?
-------------------------------------------------------

This question comes up in a variety of forms:

 1. Why does Spack ignore the preferences for versions / variants
    that I set in my ``packages.yaml`` file?
 2. Why does Spack not use the default variant value from the
    ``package.py`` file?

The short answer is that Spack picks the optimal versions, variant
values, and dependencies, and the optimal choice does not always
coincide with user preferences, default values or latest package
versions.

The exact optimality criteria are complex, but in practice it is
enough to remember the following order of precedence:

1. :ref:`Package preferences <package-preferences>` set in ``packages.yaml``
   override variant defaults set in ``package.py`` files, and override the
   default version order (latest is best). Preferences are set as follows:

   .. code-block:: yaml

      packages:
        foo:
          version: [1.0, 1.1]
          variants: ~mpi

2. :ref:`Reuse concretization <concretizer-options>` set in ``concretizer.yaml``
   overrides preferences. The idea is that avoiding source builds is more important
   than building a preferred version from sources. When build caches are configured,
   specs may be reused from a remote location too. Reuse concretization is set
   as follows:

   .. code-block:: yaml

      concretizer:
        reuse: dependencies / true / false

3. :ref:`Package requirements <package-requirements>` set in ``packages.yaml`` and
   constraints from the command line as well as ``package.py`` files override all
   of the above. Requirements look like this:

   .. code-block:: yaml

      packages:
        foo:
          require:
          - "@1.2: +mpi"

In summary: requirements + constraints > reuse > preferences > defaults.
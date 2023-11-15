.. Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

==========================
Frequently Asked Questions
==========================

--------------------------------------------------------
What determines which versions and variants Spack picks?
--------------------------------------------------------

This question comes up in a variety of forms:

 1. Why does Spack ignore the preferences for versions and variants
    that I set in my ``packages.yaml`` file?
 2. Why does Spack not use the default variant value from the
    ``package.py`` file?

The short answer is that Spack always picks an optimal configuration
based on a complex set of criteria. These criteria are more nuanced
than always choosing the latest versions or default variants.

The following set of criteria (from lowest to highest precedence) explain
common cases where concretization output may seem surprising at first.

1. :ref:`Package preferences <package-preferences>` configured in ``packages.yaml``
   override variant defaults from ``package.py`` files, and influence the optimal
   ordering of versions. Preferences are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          version: [1.0, 1.1]
          variants: ~mpi

2. :ref:`Reuse concretization <concretizer-options>` configured in ``concretizer.yaml``
   overrides preferences. The idea is that avoiding source builds is more important
   than building a preferred version from sources. When build caches are configured,
   specs may be reused from a remote location too. Reuse concretization is configured
   as follows:

   .. code-block:: yaml

      concretizer:
        reuse: dependencies / true / false

3. :ref:`Package requirements <package-requirements>` configured in ``packages.yaml``,
   and constraints from the command line as well as ``package.py`` files override all
   of the above. Requirements are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          require:
          - "@1.2: +mpi"

Requirements and constraints restrict the set of possible solutions, while reuse
behavior and preferences influence what an optimal solution looks like.

.. note::

    As a rule of thumb: requirements + constraints > reuse > preferences > defaults.
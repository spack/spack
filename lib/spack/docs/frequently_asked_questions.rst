.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Answers to common Spack questions, including version and variant selection, package preferences, compiler configuration, and concretizer behavior, with practical YAML and command-line examples.

Frequently Asked Questions
==========================

This page contains answers to frequently asked questions about Spack.
If you have questions that are not answered here, feel free to ask on `Slack <https://slack.spack.io>`_ or `GitHub Discussions <https://github.com/spack/spack/discussions>`_.
If you've learned the answer to a question that you think should be here, please consider contributing to this page.

.. _faq-concretizer-precedence:

Why does Spack pick particular versions and variants?
-----------------------------------------------------

This question comes up in a variety of forms:

1. Why does Spack seem to ignore my package preferences from ``packages.yaml`` configuration?
2. Why does Spack toggle a variant instead of using the default from the ``package.py`` file?

The short answer is that Spack always picks an optimal configuration based on a complex set of criteria\ [#f1]_.
These criteria are more nuanced than always choosing the latest versions or default variants.

.. note::

    As a rule of thumb: requirements + constraints > strong preferences > reuse > preferences > defaults.

The following set of criteria (from lowest to highest precedence) explains common cases where concretization output may seem surprising at first.

1. :ref:`Package preferences <package-preferences>` configured in ``packages.yaml`` override variant defaults from ``package.py`` files, and influence the optimal ordering of versions.
   Preferences are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          version: [1.0, 1.1]
          variants: ~mpi

2. :ref:`Reuse concretization <concretizer-options>` configured in ``concretizer.yaml`` overrides preferences, since it's typically faster to reuse an existing spec than to build a preferred one from sources.
   When build caches are enabled, specs may be reused from a remote location too.
   Reuse concretization is configured as follows:

   .. code-block:: yaml

      concretizer:
        reuse: dependencies  # other options are 'true' and 'false'

3. :ref:`Strong preferences <package-strong-preferences>` configured in ``packages.yaml`` are higher priority than reuse, and can be used to strongly prefer a specific version or variant, without erroring out if it's not possible.
   Strong preferences are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          prefer:
          - "@1.1: ~mpi"

4. :ref:`Package requirements <package-requirements>` configured in ``packages.yaml``, and constraints from the command line as well as ``package.py`` files override all of the above.
   Requirements are specified as follows:

   .. code-block:: yaml

      packages:
        foo:
          require:
          - "@1.2: +mpi"
          conflict:
          - "@1.4"

Requirements and constraints restrict the set of possible solutions, while reuse behavior and preferences influence what an optimal solution looks like.

How do I use a specific compiler?
---------------------------------

When you have multiple compilers available in :ref:`spack-compiler-list`, and want to build your packages with a specific one, you have the following options:

1. Specify your compiler preferences globally for all packages in configuration files.
2. Specify them on the level of individual specs, like ``pkg %gcc@15`` or ``pkg %c,cxx=gcc@15``.

We'll explore both options in more detail.

Specific compiler for all packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use a specific compiler for all packages, it's best to use :ref:`strong preferences in packages.yaml config <setting-requirements-on-virtual-specs>`.
The following example prefers GCC 15 for all languages ``c``, ``cxx``, and ``fortran``:

.. code-block:: yaml
   :caption: Recommended: *prefer* a specific compiler
   :name: code-example-prefer-compiler

   packages:
     c:
       prefer:
       - gcc@15
     cxx:
       prefer:
       - gcc@15
     fortran:
       prefer:
       - gcc@15

You can also replace ``prefer:`` with ``require:`` if you want Spack to produce an error if the preferred compiler cannot be used.
See also :ref:`the previous FAQ entry <faq-concretizer-precedence>`.

In Spack, the languages ``c``, ``cxx`` and ``fortran`` are :ref:`virtual packages <language-dependencies>`, on which packages depend if they need a compiler for that language.
Compiler packages provide these language virtuals.
When you specify these strong preferences, Spack determines whether the package depends on any of the language virtuals, and if so, it applies the associated compiler spec when possible.

What is **not recommended** is to define ``%gcc`` as a required dependency of all packages:

.. code-block:: yaml
   :caption: Incorrect: requiring a dependency on a compiler for all packages
   :name: code-example-typical-mistake-require-compiler

   packages:
     all:
       require:
       - "%gcc@15"

This is *incorrect*, because some packages do not need a compiler at all (e.g. pure Python packages).

Specific compiler for individual specs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If different parts of your software stack need to be built with different compilers, it's best to specify compilers as dependencies of the relevant specs (whether on the command line or in Spack environments).

.. code-block:: spec
   :caption: Example of specifying different compilers for different specs
   :name: console-example-different-compilers

   $ spack install foo %gcc@15 ^bar %intel-oneapi-compilers

What this means is that ``foo`` will depend on GCC 15, while ``bar`` will depend on ``intel-oneapi-compilers``.

You can also be more specific about what compiler to use for a particular language:

.. code-block:: spec
   :caption: Example of specifying different compilers for different languages
   :name: console-example-different-languages

   $ spack install foo %c,cxx=gcc@15 %fortran=intel-oneapi-compilers

These input specs can be simplified using :doc:`toolchains_yaml`.
See also :ref:`pitfalls-without-toolchains` for common mistakes to avoid.

.. rubric:: Footnotes

.. [#f1] The exact list of criteria can be retrieved with the :ref:`spack-solve` command.

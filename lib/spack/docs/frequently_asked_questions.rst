..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

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

.. _faq-concretization-errors:

How do I debug unexpected or failing concretization?
-----------------------------------------------------

``spack install`` and ``spack concretize`` may fail with a concretization error when the solver cannot find a package configuration that satisfies all constraints.

Most of the time, the error message is structured and contains information about which requirements could not be met.
It typically identifies the conflicting constraints and the files where they are defined (e.g., a ``packages.yaml`` entry or a ``conflicts()`` directive in a ``package.py``).
If the cause is clear from the error, you can fix the offending entry directly.

If it is not obvious *why* the solver made a particular decision -- for example, why it chose a specific version or variant -- run :ref:`spack-solve` to see the full optimization breakdown:

.. code-block:: console

   $ spack solve <spec>

The output shows the optimization criteria and the weights assigned to each choice.
This makes it possible to trace which preference or requirement is driving an unexpected result.
See also :ref:`faq-concretizer-precedence` for an overview of how criteria are prioritized.

For a deeper investigation of solver internals, see :ref:`debugging-concretization` in the developer guide.

.. _faq-variant-rename:

How do I rename or remove a variant?
-------------------------------------

Abruptly removing or renaming a variant in a package breaks any spec that still uses the old name, and leaves users with an opaque error and no guidance on what to use instead.
The ``deprecated()`` directive with ``replace=`` lets you keep the old variant name working while transparently rewriting it to the new form *before the solver runs*.

**Removing a variant**

Suppose we want to remove the ``pic`` variant from ``bzip2``, and always build with ``PIC`` enabled:

.. code-block:: python

   class Bzip2(Package):
       variant("pic", default=False, description="Build with PIC")

Removing the ``variant()`` directive and replacing it with a proper ``deprecated()`` directive:

.. code-block:: python

   class Bzip2(Package):
       deprecated("pic=*", reason="maintenance", replace={"pic=*": ""})

is enough to warn users during concretization, if they still reference the ``pic`` variant explicitly in any place.

**Removing a variant with no valid replacement**

Sometimes a variant cannot be silently dropped because the corresponding configuration is no longer buildable at all.
For instance, suppose we plan to drop support for ``+guile`` in ``gmake``.

In these cases it is good practice to deprecate only the affected value first, so users get a warning during concretization while the variant is still accepted.
This gives them time to update their specs before the hard cutover:

.. code-block:: python

   class GMake(Package):
       variant("guile", default=False, description="Support GNU Guile for embedded scripting")
       deprecated("+guile", msg="Guile support will be dropped in the next release")

In the following release, the variant definition can then be removed, and the ``replace=`` argument can be added to the deprecated directive:

.. code-block:: python

   class GMake(Package):
      deprecated(
        "guile=*",
        replace={
            "+guile": None,  # error: Guile support has been removed entirely
            "~guile": "",    # no-op: package always builds without Guile now
        },
        msg="Guile is not supported anymore"
      )

At this point, any spec that requests ``gmake+guile`` will produce a hard error:

.. code-block:: console

   $ spack solve gmake+guile
   ==> Error: Deprecated variants with no replacement were found:
     - input spec: gmake+guile is deprecated with no replacement [Guile is not supported anymore]
     - in foo's recipe: gmake+guile is deprecated with no replacement [Guile is not supported anymore]

The provenance prefix tells you exactly where the offending constraint came from -- fix it there.

**Renaming a variant**

Suppose ``hdf5`` currently defines a boolean ``shared`` variant:

.. code-block:: python

   class Hdf5(Package):
       variant("shared", default=True, description="When active, builds shared libraries")

and we want to replace it with a multi-valued ``libs`` variant.
To do it, we have to remove the old ``variant()`` directive, add the new variant, and finally add ``deprecated()``:

.. code-block:: python

   class Hdf5(Package):
       variant(
           "libs",
           default="shared",
           values=("shared", "static"),
           multi=True,
           description="Build shared and/or static libraries"
       )

       deprecated("shared=*", replace={"+shared": "libs=shared", "~shared": "libs=static"})

When a user installs ``hdf5+shared``, Spack rewrites it in-memory to ``hdf5 libs=shared`` before solving and emits a deprecation warning.
The in-memory rewriting also applies automatically to ``packages.yaml`` preference and requirement entries, and to constraints in package recipes, so downstream packages do not need to be updated immediately.

See :ref:`packaging_deprecations_variants` for the full API, including how to handle multiple old variants mapping to a single new constraint.

.. rubric:: Footnotes

.. [#f1] The exact list of criteria can be retrieved with the :ref:`spack-solve` command.
         See :ref:`faq-concretization-errors` for more information.

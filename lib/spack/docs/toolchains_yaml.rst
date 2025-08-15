.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Define named compiler sets (toolchains) in Spack to easily and consistently apply compiler choices for C, C++, and Fortran across different packages.

.. _toolchains:

Toolchains (toolchains.yaml)
=============================

Toolchains let you group a set of compiler constraints under a single, user-defined name.
This allows you to reference a complex set of compiler choices for C, C++, Fortran, with a simple spec like ``%my_toolchain``.
They are defined under the ``toolchains`` section of the configuration.

.. seealso::

   The sections :ref:`language-dependencies` and :ref:`explicit-binding-virtuals` provide more background on how Spack handles languages and compilers.

Basic usage
-----------

As an example, the following configuration file defines a toolchain named ``llvm_gfortran``:

.. code-block:: yaml
   :caption: ~/.spack/toolchains.yaml

   toolchains:
     llvm_gfortran:
     - spec: cflags=-O3
     - spec: "%c=llvm"
       when: "%c"
     - spec: "%cxx=llvm"
       when: "%cxx"
     - spec: "%fortran=gcc"
       when: "%fortran"

The ``when`` clause in each entry determines if that line's ``spec`` is applied.
In this example, it means that ``llvm`` is used as a compiler for the C and C++ languages, and ``gcc`` for Fortran, *whenever the package uses those languages*.
It also adds ``cflags=-O3`` unconditionally.

The toolchain can be referenced using

.. code-block:: spec
  
   $ spack install my-package %llvm_gfortran

Toolchains are useful for two reasons:

1. **They reduce verbosity.**
   Instead of multiple constraints ``%c,cxx=clang %fortran=gcc``, you can simply write ``%llvm_gfortran``.
2. **They apply conditionally.**
   You can use ``my-package %llvm_gfortran`` even if ``my-package`` is not written in Fortran.


Pitfalls without toolchains
---------------------------

The conditional nature of toolchains is important, because it helps you avoid two common pitfalls when specifying compilers.

1. Firstly, when you specify ``my-package %gcc``, your spec is **underconstrained**: Spack has to make ``my-package`` depend on ``gcc``, but the constraint does not rule out mixed compilers, such as ``gcc`` for C and ``llvm`` for C++.

2. Secondly, when you specify ``my-package %c,cxx,fortran=gcc`` to be more explicit, your spec might be **overconstrained**.
   You not only require ``gcc`` for all languages, but *also* that ``my-package`` uses *all* these languages.
   This will cause a concretization error if ``my-package`` was written in C and C++, but not Fortran.

Toolchains and matrices
-----------------------

Toolchains can be used to simplify the construction of a list of specs using :ref:`environment-spec-matrices`, when the list includes packages with different language requirements:

.. code-block:: yaml

   specs:
   - matrix:
     - [kokkos, hdf5~cxx+fortran, py-scipy]
     - ["%llvm_gfortran"]

Note that in this case we can use a single matrix, and the user doesn't need to know exactly which package requires which language.
Without toolchains, it would be difficult to enforce compilers directly, because:

* ``kokkos`` depends on C and C++, but not Fortran
* ``hdf5~cxx+fortran`` depends on C and Fortran, but not C++
* ``py-scipy`` depends on C, C++, and Fortran

Combining toolchains
--------------------

Different toolchains can be used independently or even in the same spec.
Consider the following configuration:

.. code-block:: yaml
   :caption: ~/.spack/toolchains.yaml

   toolchains:
     llvm_gfortran:
     - spec: cflags=-O3
     - spec: "%c=llvm"
       when: "%c"
     - spec: "%cxx=llvm"
       when: "%cxx"
     - spec: "%fortran=gcc"
       when: "%fortran"
     gcc_all:
     - spec: "%c=gcc"
       when: "%c"
     - spec: "%cxx=gcc"
       when: "%cxx"
     - spec: "%fortran=gcc"
       when: "%fortran"


Now, you can use these toolchains in a single spec:

.. code-block:: spec

   $ spack install hdf5+fortran%llvm_gfortran ^mpich %gcc_all

This will result in:

* An ``hdf5`` compiled with ``llvm`` for the C/C++ components, but with its Fortran components compiled with ``gfortran``,
* Built against an MPICH installation compiled entirely with ``gcc`` for C, C++, and Fortran.

.. note::

   Toolchains are currently limited to using only direct dependencies (``%``) in their definition.
   Transitive dependencies are not allowed.

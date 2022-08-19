.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

============
Known Issues
============

This is a list of known issues in Spack. It provides ways of getting around these
problems if you encounter them.

------------------------------------------------
Spack does not seem to respect ``packages.yaml``
------------------------------------------------

.. note::

   This issue is **resolved** as of v0.19.0.dev0 commit
   `8281a0c5feabfc4fe180846d6fe95cfe53420bc5`, through the introduction of package
   requirements. See :ref:`package-requirements`.

A common problem in Spack v0.18.0 up to v0.19.0.dev0 is that package, compiler and target
preferences specified in ``packages.yaml`` do not seem to be respected. Spack picks the
"wrong" compilers and their versions, package versions and variants, and
micro-architectures.

This is however not a bug. In order to reduce the number of builds of the same
packages, the concretizer values reuse of installed packages higher than preferences
set in ``packages.yaml``. Note that ``packages.yaml`` specifies only preferences, not
hard constraints.

There are multiple workarounds:

1. Disable reuse during concretization: ``spack install --fresh <spec>`` when installing
   from the command line, or ``spack concretize --fresh --force`` when using
   environments.  
2. Turn preferences into constrains, by moving them to the input spec. For example,
   use ``spack spec zlib%gcc@12`` when you want to force GCC 12 even if ``zlib`` was
   already installed with GCC 10.

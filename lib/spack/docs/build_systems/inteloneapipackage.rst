.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _inteloneapipackage:


====================
 IntelOneapiPackage
====================


.. contents::


oneAPI packages in Spack
========================

Spack can install and use the Intel oneAPI products. You may either
use spack to install the oneAPI tools or use the `Intel
installers`_. After installation, you may use the tools directly, or
use Spack to build packages with the tools.

The Spack Python class ``IntelOneapiPackage`` is a base class that is
used by ``IntelOneapiCompilers``, ``IntelOneapiMkl``,
``IntelOneapiTbb`` and other classes to implement the oneAPI
packages. See the `Spack package list`_ for the full list of available
oneAPI packages.


Unrelated packages
------------------

The following packages use a different installer and are not discussed
here:

* ``intel-gpu-tools`` -- Test suite and low-level tools for the Linux `Direct
  Rendering Manager <https://en.wikipedia.org/wiki/Direct_Rendering_Manager>`_
* ``intel-mkl-dnn`` -- Math Kernel Library for Deep Neural Networks (``CMakePackage``)
* ``intel-xed`` -- X86 machine instructions encoder/decoder
* ``intel-tbb`` -- Standalone version of Intel Threading Building Blocks. Note that
  a TBB runtime version is included with ``intel-mkl``, and development
  versions are provided by the packages ``intel-parallel-studio`` (all
  editions) and its ``intel`` subset.

Example
=======

We start with a simple example that will be sufficient for most
users. Install the oneAPI compilers::

  spack install intel-oneapi-compilers

Add the oneAPI compilers to the set of compilers that Spack can use::

  spack compiler add `spack location -i intel-oneapi-compilers`/latest/linux/bin/intel64
  spack compiler add `spack location -i intel-oneapi-compilers`/latest/linux/bin

This adds the compilers to your ``compilers.yaml``. Verify that the
compilers are available::

  spack compiler list

The ``intel-oneapi-compilers`` package includes 2 families of
compilers:

* ``intel``: ``icc``, ``icpc``, ``ifort``. Intel's *classic*
  compilers.
* ``oneapi``: ``icx``, ``icpx``, ``ifx``. Intel's new generation of
  compilers based on LLVM.

To build the ``patchelf`` Spack package with ``icc``, do::

  spack install patchelf%intel

To build with with ``icx``, do ::

  spack install patchelf%oneapi

In addition to compilers, oneAPI contains many libraries. The ``hdf5``
package works with any compatible MPI implementation. To build
``hdf5`` with Intel oneAPI MPI do::

  spack install hdf5 +mpi ^intel-oneapi-mpi

Using an Externally Installed oneAPI
====================================

Spack can also use oneAPI tools that are manually installed with
`Intel Installers`_.  The procedures for configuring Spack to use
external compilers and libraries are different.

Compilers
---------

To use the compilers, add some information about the installation to
``compilers.yaml``. For most users, it is sufficient to do::

  spack compiler add /opt/intel/oneapi/compiler/latest/linux/bin/intel64
  spack compiler add /opt/intel/oneapi/compiler/latest/linux/bin

Adapt the paths above if you did not install the tools in the default
location. After adding the compilers, using them in Spack will be
exactly the same as if you had installed the
``intel-oneapi-compilers`` package.  Another option is to manually add
the configuration to ``compilers.yaml`` as described in :ref:`Compiler
configuration <compiler-config>`.


Libraries
---------

Configure external library packages by editing ``packages.yaml``,
following the Spack documentation under :ref:`External Packages
<sec-external-packages>`.

Similar to ``compilers.yaml``, the ``packages.yaml`` files define a
package external to Spack in terms of a Spack spec and resolve each
such spec via veither the ``paths`` or ``modules`` tokens to a
specific pre-installed package version on the system.  Since Intel
tools generally need environment variables to interoperate, which
cannot be conveyed in a mere ``paths`` specification, the ``modules``
token will be more sensible to use. It resolves the Spack-side spec to
a modulefile generated and managed outside of Spack's purview, which
Spack will load internally and transiently when the corresponding spec
is called upon to compile client packages.

Unlike compilers, Spack does not offer a command to generate an
entirely new ``packages.yaml`` entry.  You must create new entries
yourself in a text editor, though the command ``spack config
[--scope=...] edit packages`` can help with selecting the proper file.
See section :ref:`Configuration Scopes <configuration-scopes>` for an
explanation about the different files and section :ref:`Build
customization <build-settings>` for specifics and examples for
``packages.yaml`` files.


Using oneAPI Tools Installed by Spack
=====================================

Spack can be a convenient way to install and configure compilers and
libaries, even if you do not intend to build a Spack package. If you
want to build a Makefile project using Spack-installed oneAPI compilers,
then use spack to configure your environment::

  spack load intel-oneapi-compilers

And then you can build with::

  CXX=icpx make

You can also use Spack-installed libraries. For example::

  spack load intel-oneapi-mkl

Will update your environment CPATH, LIBRARY_PATH, and other
environment variables for building an application with MKL.


Selecting libraries to satisfy virtual packages
===============================================

Intel packages, whether integrated into Spack as external packages or
installed within Spack, can be called upon to satisfy the requirement
of a client package for a library that is available from different
providers.  The relevant virtual packages for Intel are ``blas``,
``lapack``, ``scalapack``, and ``mpi``.



Tips for configuring client packages to use MKL
===============================================

* To use MKL as provider for BLAS, LAPACK, or ScaLAPACK:

  The packages that provide ``mkl`` also provide the narrower
  virtual ``blas``, ``lapack``, and ``scalapack`` packages.
  See the relevant :ref:`Packaging Guide section <blas_lapack_scalapack>`
  for an introduction.
  To portably use these virtual packages, construct preprocessor and linker
  option strings in your package configuration code using the package functions
  ``.headers`` and ``.libs`` in conjunction with utility functions from the
  following classes:

  * :py:class:`llnl.util.filesystem.FileList`,
  * :py:class:`llnl.util.filesystem.HeaderList`,
  * :py:class:`llnl.util.filesystem.LibraryList`.

  .. tip::
     *Do not* use constructs like ``.prefix.include`` or ``.prefix.lib``, with
     Intel or any other implementation of ``blas``, ``lapack``, and
     ``scalapack``.

  For example, for an
  :ref:`AutotoolsPackage <autotoolspackage>`
  use ``.libs.ld_flags`` to transform the library file list into linker options
  passed to ``./configure``:

  .. code-block:: python

      def configure_args(self):
          args = []
          ...
          args.append('--with-blas=%s' % self.spec['blas'].libs.ld_flags)
          args.append('--with-lapack=%s' % self.spec['lapack'].libs.ld_flags)
          ...

  .. tip::
     Even though ``.ld_flags`` will return a string of multiple words, *do not*
     use quotes for options like ``--with-blas=...`` because Spack passes them
     to ``./configure`` without invoking a shell.

  Likewise, in a :ref:`MakefilePackage <makefilepackage>` or similar
  package that does not use AutoTools you may need to provide include
  and link options for use on command lines or in environment
  variables.  For example, to generate an option string of the form
  ``-I<dir>``, use:

  .. code-block:: python

    self.spec['blas'].headers.include_flags

  and to generate linker options (``-L<dir> -llibname ...``), use the
  same as above,

  .. code-block:: python

    self.spec['blas'].libs.ld_flags

  See :ref:`MakefilePackage <makefilepackage>` and more generally the
  :ref:`Packaging Guide <blas_lapack_scalapack>` for background and
  further examples.


.. _`Intel installers`: https://software.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top.html
.. _`Spack package list`: https://spack.readthedocs.io/en/latest/package_list.html#intel-oneapi-ccl

.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

============
Known Issues
============

This is a list of known bugs in Spack. It provides ways of getting around these
problems if you encounter them.

---------------------------------------------------
Variants are not properly forwarded to dependencies
---------------------------------------------------

**Status:** Expected to be fixed by Spack's new concretizer

Sometimes, a variant of a package can also affect how its dependencies are
built. For example, in order to build MPI support for a package, it may
require that its dependencies are also built with MPI support. In the
``package.py``, this looks like:

.. code-block:: python

   depends_on('hdf5~mpi', when='~mpi')
   depends_on('hdf5+mpi', when='+mpi')

Spack handles this situation properly for *immediate* dependencies, and
builds ``hdf5`` with the same variant you used for the package that
depends on it. However, for *indirect* dependencies (dependencies of
dependencies), Spack does not backtrack up the DAG far enough to handle
this. Users commonly run into this situation when trying to build R with
X11 support:

.. code-block:: console

   $ spack install r+X
   ...
   ==> Error: Invalid spec: 'cairo@1.14.8%gcc@6.2.1+X arch=linux-fedora25-x86_64 ^bzip2@1.0.6%gcc@6.2.1+shared arch=linux-fedora25-x86_64 ^font-util@1.3.1%gcc@6.2.1 arch=linux-fedora25-x86_64 ^fontconfig@2.12.1%gcc@6.2.1 arch=linux-fedora25-x86_64 ^freetype@2.7.1%gcc@6.2.1 arch=linux-fedora25-x86_64 ^gettext@0.19.8.1%gcc@6.2.1+bzip2+curses+git~libunistring+libxml2+tar+xz arch=linux-fedora25-x86_64 ^glib@2.53.1%gcc@6.2.1~libmount arch=linux-fedora25-x86_64 ^inputproto@2.3.2%gcc@6.2.1 arch=linux-fedora25-x86_64 ^kbproto@1.0.7%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libffi@3.2.1%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libpng@1.6.29%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libpthread-stubs@0.4%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libx11@1.6.5%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libxau@1.0.8%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libxcb@1.12%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libxdmcp@1.1.2%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libxext@1.3.3%gcc@6.2.1 arch=linux-fedora25-x86_64 ^libxml2@2.9.4%gcc@6.2.1~python arch=linux-fedora25-x86_64 ^libxrender@0.9.10%gcc@6.2.1 arch=linux-fedora25-x86_64 ^ncurses@6.0%gcc@6.2.1~symlinks arch=linux-fedora25-x86_64 ^openssl@1.0.2k%gcc@6.2.1 arch=linux-fedora25-x86_64 ^pcre@8.40%gcc@6.2.1+utf arch=linux-fedora25-x86_64 ^pixman@0.34.0%gcc@6.2.1 arch=linux-fedora25-x86_64 ^pkg-config@0.29.2%gcc@6.2.1+internal_glib arch=linux-fedora25-x86_64 ^python@2.7.13%gcc@6.2.1+shared~tk~ucs4 arch=linux-fedora25-x86_64 ^readline@7.0%gcc@6.2.1 arch=linux-fedora25-x86_64 ^renderproto@0.11.1%gcc@6.2.1 arch=linux-fedora25-x86_64 ^sqlite@3.18.0%gcc@6.2.1 arch=linux-fedora25-x86_64 ^tar^util-macros@1.19.1%gcc@6.2.1 arch=linux-fedora25-x86_64 ^xcb-proto@1.12%gcc@6.2.1 arch=linux-fedora25-x86_64 ^xextproto@7.3.0%gcc@6.2.1 arch=linux-fedora25-x86_64 ^xproto@7.0.31%gcc@6.2.1 arch=linux-fedora25-x86_64 ^xtrans@1.3.5%gcc@6.2.1 arch=linux-fedora25-x86_64 ^xz@5.2.3%gcc@6.2.1 arch=linux-fedora25-x86_64 ^zlib@1.2.11%gcc@6.2.1+pic+shared arch=linux-fedora25-x86_64'.
   Package cairo requires variant ~X, but spec asked for +X

A workaround is to explicitly activate the variants of dependencies as well:

.. code-block:: console

   $ spack install r+X ^cairo+X ^pango+X

See https://github.com/spack/spack/issues/267 and
https://github.com/spack/spack/issues/2546 for further details.

-----------------------------------------------
depends_on cannot handle recursive dependencies
-----------------------------------------------

**Status:** Not yet a work in progress

Although ``depends_on`` can handle any aspect of Spack's spec syntax,
it currently cannot handle recursive dependencies. If the ``^`` sigil
appears in a ``depends_on`` statement, the concretizer will hang.
For example, something like:

.. code-block:: python

   depends_on('mfem+cuda ^hypre+cuda', when='+cuda')


should be rewritten as:

.. code-block:: python

   depends_on('mfem+cuda', when='+cuda')
   depends_on('hypre+cuda', when='+cuda')


See https://github.com/spack/spack/issues/17660 and
https://github.com/spack/spack/issues/11160 for more details.

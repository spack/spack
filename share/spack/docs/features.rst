.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

================
Feature Overview
================

This is a high-level overview of features that make Spack different
from other `package managers
<http://en.wikipedia.org/wiki/Package_management_system>`_ and `port
systems <http://en.wikipedia.org/wiki/Ports_collection>`_.

---------------------------
Simple package installation
---------------------------

Installing the default version of a package is simple. This will install
the latest version of the ``mpileaks`` package and all of its dependencies:

.. code-block:: console

   $ spack install mpileaks

--------------------------------
Custom versions & configurations
--------------------------------

Spack allows installation to be customized.  Users can specify the
version, compile-time options, and cross-compile platform, all on the command line.

.. code-block:: console

   # Install a particular version by appending @
   $ spack install hdf5@1.14.6

   # Add special compile-time options by name
   $ spack install hdf5@1.14.6 api=v110

   # Add special boolean compile-time options with +
   $ spack install hdf5@1.14.6 +hl

   # Add compiler flags using the conventional names
   $ spack install hdf5@1.14.6 cflags="-O3 -floop-block"

   # Cross-compile for a different micro-architecture with target=
   $ spack install hdf5@1.14.6 target=icelake

Users can specify as many or as few options as they care about. Spack
will fill in the unspecified values with sensible defaults.

----------------------
Customize dependencies
----------------------

Spack allows *dependencies* of a particular installation to be customized extensively.
Users can specify both *direct* dependencies of a node, using the ``%`` sigil, or *transitive*
dependencies, using the ``^`` sigil:

.. code-block:: console

   # Install hdf5 using gcc@15.1.0 as a compiler (direct dependency of hdf5)
   $ spack install hdf5@1.14.6 %gcc@15.1.0

   # Install hdf5 using hwloc with CUDA enabled (transitive dependency)
   $ spack install hdf5@1.14.6 ^hwloc+cuda

The expression on the command line can be as simple, or as complicated, as the user need:

.. code-block:: console

   # Install hdf5 compiled with gcc@15, linked to mpich compiled with gcc@14
   $ spack install hdf5@1.14.6 %gcc@15 ^mpich %gcc@14

------------------------
Non-destructive installs
------------------------

Spack installs every unique package/dependency configuration into its
own prefix, so new installs will not break existing ones.

-------------------------------
Packages can peacefully coexist
-------------------------------

Spack avoids library misconfiguration by using ``RPATH`` to link
dependencies.  When a user links a library or runs a program, it is
tied to the dependencies it was built with, so there is no need to
manipulate ``LD_LIBRARY_PATH`` at runtime.

-------------------------
Creating packages is easy
-------------------------

To create a new package, all Spack needs is a URL for the source
archive.  The ``spack create`` command will create a boilerplate
package file, and the package authors can fill in specific build steps
in pure Python.

For example, this command:

.. code-block:: console

   $ spack create https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz

creates a simple Python file:

.. code-block:: python

   from spack.package import *


   class Libelf(AutotoolsPackage):
       """FIXME: Put a proper description of your package here."""

       # FIXME: Add a proper url for your package's homepage here.
       homepage = "https://www.example.com"
       url = "https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz"

       # FIXME: Add a list of GitHub accounts to
       # notify when the package is updated.
       # maintainers("github_user1", "github_user2")

       version("0.8.13", sha256="591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d")

       # FIXME: Add dependencies if required.
       # depends_on("foo")

       def configure_args(self):
           # FIXME: Add arguments other than --prefix
           # FIXME: If not needed delete this function
           args = []
           return args

It doesn't take much Python coding to get from there to a working
package:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/libelf/package.py
   :lines: 5-

Spack also provides wrapper functions around common commands like
``configure``, ``make``, and ``cmake`` to make writing packages
simple.

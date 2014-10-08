Feature Overview
==================

This is a high-level overview of features that make Spack different
from other `package managers
<http://en.wikipedia.org/wiki/Package_management_system>`_ and `port
systems <http://en.wikipedia.org/wiki/Ports_collection>`_.

Simple package installation
----------------------------

Installing the default version of a package is simple. This will install
the latest version of the ``mpileaks`` package and all of its dependencies:

.. code-block:: sh

   $ spack install mpileaks

Custom versions & configurations
-------------------------------------------

Spack allows installation to be customized.  Users can specify the
version, build compiler, compile-time options, and cross-compile
platform, all on the command line.

.. code-block:: sh

   # Install a particular version by appending @
   $ spack install mpileaks@1.1.2

   # Specify a compiler (and its version), with %
   $ spack install mpileaks@1.1.2 %gcc@4.7.3

   # Add special compile-time options with +
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 +debug

   # Cross-compile for a different architecture with =
   $ spack install mpileaks@1.1.2 =bgqos_0

Users can specify as many or few options as they care about.  Spack
will fill in the unspecified values with sensible defaults.


Customize dependencies
-------------------------------------

Spack allows *dependencies* of a particular installation to be
customized extensively.  Suppose that ``mpileaks`` depends indirectly
on ``libelf`` and ``libdwarf``.  Using ``^``, users can add custom
configurations for the dependencies:

.. code-block:: sh

   # Install mpileaks and link it with specific versions of libelf and libdwarf
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 +debug ^libelf@0.8.12 ^libdwarf@20130729+debug


Non-destructive installs
-------------------------------------

Spack installs every unique package/dependency configuration into its
own prefix, so new installs will not break existing ones.

Packages can peacefully coexist
-------------------------------------

Spack avoids library misconfiguration by using ``RPATH`` to link
dependencies.  When a user links a library or runs a program, it is
tied to the dependencies it was built with, so there is no need to
manipulate ``LD_LIBRARY_PATH`` at runtime.

Creating packages is easy
-------------------------------------

To create a new packages, all Spack needs is a URL for the source
archive.  The ``spack create`` command will create a boilerplate
package file, and the package authors can fill in specific build steps
in pure Python.

For example, this command:

.. code-block:: sh

   $ spack create http://www.mr511.de/software/libelf-0.8.13.tar.gz

creates a simple python file:

.. code-block:: python

   from spack import *

   class Libelf(Package):
       homepage = "http://www.example.com/"
       url      = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"

       version('0.8.13', '4136d7b4c04df68b686570afa26988ac')

       def install(self, prefix):
           configure("--prefix=%s" % prefix)
           make()
           make("install")

It doesn't take much python coding to get from there to a working
package:

.. literalinclude:: ../../../var/spack/packages/libelf/package.py
   :lines: 25-

Spack also provides wrapper functions around common commands like
``configure``, ``make``, and ``cmake`` to make writing packages
simple.

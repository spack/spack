Feature Overview
==================

This is an overview of features that make Spack different from other
`package managers <http://en.wikipedia.org/wiki/Package_management_system>`_
and `port systems <http://en.wikipedia.org/wiki/Ports_collection>`_.

Simple package installation
----------------------------

Installing packages is easy with Spack when you just want the default
version.  This installs the latest version of mpileaks and all of its
dependencies:

.. code-block:: sh

   $ spack install mpileaks

Custom versions & configurations
-------------------------------------------

If there's some aspect of your package that you want to customize, you
can do that too.

.. code-block:: sh

   # Install a particular version by appending @
   $ spack install mpileaks@1.1.2

   # Or your favorite compiler (and its version), with %
   $ spack install mpileaks@1.1.2 %gcc@4.7.3

   # Add some special compile-time options with +
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 +debug

   # Cross-compile for a different architecture with =
   $ spack install mpileaks@1.1.2 =bgqos_0

Customize dependencies
-------------------------------------

You can customize package dependencies with ``^``.  Suppose that
``mpileaks`` depends indirectly on ``libelf`` and ``libdwarf``.  Using
``^``, you can add custom configurations for the dependencies, too.

.. code-block:: sh

   # Install mpileaks and link it with specific versions of libelf and libdwarf
   $ spack install mpileaks@1.1.2 %gcc@4.7.3 +debug ^libelf@0.8.12 ^libdwarf@20130729+debug


Non-destructive installs
-------------------------------------

Spack installs every unique package configuration in its own prefix,
so you can install as many different versions and configurations as
you want.  New installs will not break existing ones.


Packages can peacefully coexist
-------------------------------------

Spack uses ``RPATH`` everywhere, so users do not need to customize
``LD_LIBRARY_PATH``.  If you use a library or run a program, it will
run the way you built it.


Creating packages is easy
-------------------------------------

To create your own packages, give spack the tarball URL.  Spack
creates all the boilerplate for you.

.. code-block:: sh

   $ spack create http://scalability.llnl.gov/mpileaks/downloads/mpileaks-1.0.tar.gz

Creates ``mpileaks.py``:

.. code-block:: python

   from spack import *

   class Mpileaks(Package):
       homepage = "http://www.example.com/"
       url      = "http://scalability.llnl.gov/mpileaks/downloads/mpileaks-1.0.tar.gz"
       md5      = "4136d7b4c04df68b686570afa26988ac"

       def install(self, prefix):
           configure("--prefix=%s" % prefix)
           make()
           make("install")

Packages are pure python, so you have complete freedom when writing
build code.  Spack also provides a number of feature that make it
easier to write packages.

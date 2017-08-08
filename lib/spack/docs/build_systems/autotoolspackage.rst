.. _autotoolspackage:

----------------
AutotoolsPackage
----------------

Autotools is a GNU build system that provides a build script generator.
By running the platform-independent ``./configure`` script that comes
with the package, you can generate a platform-dependent Makefile.

^^^^^^
Phases
^^^^^^

Spack's ``AutotoolsPackage`` comes with the following phases:

#. ``autoreconf`` - generate the configure script
#. ``configure`` - generate the Makefiles
#. ``build`` - build the package
#. ``install`` - install the package

Most of the time, the ``autoreconf`` phase will do nothing, but if the
package is missing a ``configure`` script, ``autoreconf`` will generate
one for you.

The other phases run:

.. code-block:: console

   $ ./configure --prefix=/path/to/installation/prefix
   $ make
   $ make check  # optional
   $ make install
   $ make installcheck  # optional


Of course, you may need to add a few arguments to the ``./configure``
line.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^^^^^
Finding configure flags
^^^^^^^^^^^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^^^^^^^^
Addings flags to configure
^^^^^^^^^^^^^^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configure script in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^^^^
Building out of source
^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   Watch out for fake Autotools packages!

   Autotools is a very popular build system, and many people are used to the
   classic:

   .. code-block:: console

      $ ./configure
      $ make
      $ make install


   steps to install a package. For this reason, some developers will write
   their own ``configure`` scripts that have nothing to do with Autotools.
   These packages may not accept the same flags as other Autotools packages,
   so it is better to create a custom build system. You can tell if a package
   uses Autotools by running ``./configure --help`` and comparing the output
   to other known Autotools packages. You should also look for files like:

   * ``configure.ac``
   * ``configure.in``
   * ``Makefile.am``

   Packages that don't use Autotools aren't likely to have these files.

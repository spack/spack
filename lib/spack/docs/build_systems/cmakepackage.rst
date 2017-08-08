.. _cmakepackage:

------------
CMakePackage
------------

Like Autotools, CMake is a build script generator. Designed by Kitware,
CMake is a popular up-and-coming build system. In its simplest form,
Spack's ``CMakePackage`` runs the following steps:

.. code-block:: console

   $ mkdir spack-build
   $ cd spack-build
   $ cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/installation/prefix
   $ make
   $ make test  # optional
   $ make install


A few more flags are passed to ``cmake`` by default, including flags
for setting the build type and flags for locating dependencies. Of
course, you may need to add a few arguments yourself.

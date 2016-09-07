=======================================
Using Spack for CMake-based Development
=======================================

These are instructions on how to use Spack to aid in the development
of a CMake-based project.  Spack is used to help find the dependencies
for the project, configure it at development time, and then package it
it in a way that others can install.  Using Spack for CMake-based
development consists of three parts:

#. Setting up the CMake build in your software
#. Writing the Spack Package
#. Using it from Spack.

--------------------------
Setting Up the CMake Build
--------------------------

You should follow standard CMake conventions in setting up your
software, your CMake build should NOT depend on or require Spack to
build.  See here for an example:

https://github.com/citibeth/icebin

Note that there's one exception here to the rule I mentioned above.
In ``CMakeLists.txt``, I have the following line:

.. code-block:: none

   include_directories($ENV{CMAKE_TRANSITIVE_INCLUDE_PATH})

This is a hook into Spack, and it ensures that all transitive
dependencies are included in the include path.  It's not needed if
everything is in one tree, but it is (sometimes) in the Spack world;
when running without Spack, it has no effect.

Note that this "feature" is controversial, could break with future
versions of GNU ld, and probably not the best to use.  The best
practice is that you make sure that anything you #include is listed as
a dependency in your CMakeLists.txt.

To be more specific: if you #inlcude something from package A and an
installed HEADER FILE in A #includes something from package B, then
you should also list B as a dependency in your CMake build.  If you
depend on A but header files exported by A do NOT #include things from
B, then you do NOT need to list B as a dependency --- even if linking
to A links in libB.so as well.

I also recommend that you set up your CMake build to use RPATHs
correctly.  Not only is this a good idea and nice, but it also ensures
that your package will build the same with or without ``spack
install``.

-------------------------
Writing the Spack Package
-------------------------

Now that you have a CMake build, you want to tell Spack how to
configure it.  This is done by writing a Spack package for your
software.  See here for example:

https://github.com/citibeth/spack/blob/efischer/develop/var/spack/repos/builtin/packages/icebin/package.py

You need to subclass ``CMakePackage``, as is done in this example.
This enables advanced features of Spack for helping you in configuring
your software (keep reading...).  Instead of an ``install()`` method
used when subclassing ``Package``, you write ``configure_args()``.
See here for more info on how this works:

https://github.com/LLNL/spack/pull/543/files

NOTE: if your software is not publicly available, you do not need to
set the URL or version.  Or you can set up bogus URLs and
versions... whatever causes Spack to not crash.

-------------------
Using it from Spack
-------------------

Now that you have a Spack package, you can get Spack to setup your
CMake project for you.  Use the following to setup, configure and
build your project:

.. code-block:: console

   $ cd myproject
   $ spack spconfig myproject@local
   $ mkdir build; cd build
   $ ../spconfig.py ..
   $ make
   $ make install

Everything here should look pretty familiar here from a CMake
perspective, except that ``spack spconfig`` creates the file
``spconfig.py``, which calls CMake with arguments appropriate for your
Spack configuration.  Think of it as the equivalent to running a bunch
of ``spack location -i`` commands.  You will run ``spconfig.py``
instead of running CMake directly.

If your project is publicly available (eg on GitHub), then you can
ALSO use this setup to "just install" a release version without going
through the manual configuration/build step.  Just do:

#. Put tag(s) on the version(s) in your GitHub repo you want to be release versions.

#. Set the ``url`` in your ``package.py`` to download a tarball for
   the appropriate version.  (GitHub will give you a tarball for any
   version in the repo, if you tickle it the right way).  For example:

   https://github.com/citibeth/icebin/tarball/v0.1.0

   Set up versions as appropriate in your ``package.py``.  (Manually
   download the tarball and run ``md5sum`` to determine the
   appropriate checksum for it).

#. Now you should be able to say ``spack install myproject@version``
   and things "just work."

NOTE... in order to use the features outlined in this post, you
currently need to use the following branch of Spack:

https://github.com/citibeth/spack/tree/efischer/develop

There is a pull request open on this branch (
https://github.com/LLNL/spack/pull/543 ) and we are working to get it
integrated into the main ``develop`` branch.

------------------------
Activating your Software
------------------------

Once you've built your software, you will want to load it up.  You can
use ``spack load mypackage@local`` for that in your ``.bashrc``, but
that is slow.  Try stuff like the following instead:

The following command will load the Spack-installed packages needed
for basic Python use of IceBin:

.. code-block:: console

   $ module load `spack module find tcl icebin netcdf cmake@3.5.1`
   $ module load `spack module find --dependencies tcl py-basemap py-giss`


You can speed up shell startup by turning these into ``module load`` commands.

#. Cut-n-paste the script ``make_spackenv``:

   .. code-block:: sh

      #!/bin/sh
      #
      # Generate commands to load the Spack environment

      SPACKENV=$HOME/spackenv.sh

      spack module find --shell tcl git icebin@local ibmisc netcdf cmake@3.5.1 > $SPACKENV
      spack module find --dependencies --shell tcl py-basemap py-giss >> $SPACKENV

#. Add the following to your ``.bashrc`` file:

   .. code-block:: sh

      source $HOME/spackenv.sh
      # Preferentially use your checked-out Python source
      export PYTHONPATH=$HOME/icebin/pylib:$PYTHONPATH

#. Run ``sh make_spackenv`` whenever your Spack installation changes (including right now).

-----------
Giving Back
-----------

If your software is publicly available, you should submit the
``package.py`` for it as a pull request to the main Spack GitHub
project.  This will ensure that anyone can install your software
(almost) painlessly with a simple ``spack install`` command.  See here
for how that has turned into detailed instructions that have
successfully enabled collaborators to install complex software:

https://github.com/citibeth/icebin/blob/develop/README.rst

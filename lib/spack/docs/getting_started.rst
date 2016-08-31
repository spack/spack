===============
Getting Started
===============

--------
Download
--------

Getting spack is easy.  You can clone it from the `github repository
<https://github.com/llnl/spack>`_ using this command:

.. code-block:: console

   $ git clone https://github.com/llnl/spack.git

This will create a directory called ``spack``.  We'll assume that the
full path to this directory is in the ``SPACK_ROOT`` environment
variable.  Add ``$SPACK_ROOT/bin`` to your path and you're ready to
go:

.. code-block:: console

   $ export PATH=$SPACK_ROOT/bin:$PATH
   $ spack install libelf

For a richer experience, use Spack's `shell support
<http://software.llnl.gov/spack/basic_usage.html#environment-modules>`_:

.. code-block:: console

   # For bash users
   $ export SPACK_ROOT=/path/to/spack
   $ . $SPACK_ROOT/share/spack/setup-env.sh

   # For tcsh or csh users (note you must set SPACK_ROOT)
   $ setenv SPACK_ROOT /path/to/spack
   $ source $SPACK_ROOT/share/spack/setup-env.csh

This automatically adds Spack to your ``PATH``.

------------
Installation
------------

You don't need to install Spack; it's ready to run as soon as you
clone it from git.

You may want to run it out of a prefix other than the git repository
you cloned.  The ``spack bootstrap`` command provides this
functionality.  To install spack in a new directory, simply type:

.. code-block:: console

   $ spack bootstrap /my/favorite/prefix

This will install a new spack script in ``/my/favorite/prefix/bin``,
which you can use just like you would the regular spack script.  Each
copy of spack installs packages into its own ``$PREFIX/opt``
directory.

----------------------
Compiler configuration
----------------------

Spack has the ability to build packages with multiple compilers and
compiler versions. Spack searches for compilers on your machine
automatically the first time it is run. It does this by inspecting
your ``PATH``.

.. _spack-compilers:

^^^^^^^^^^^^^^^^^^^
``spack compilers``
^^^^^^^^^^^^^^^^^^^

You can see which compilers spack has found by running ``spack
compilers`` or ``spack compiler list``:

.. code-block:: console

   $ spack compilers
   ==> Available compilers
   -- gcc ---------------------------------------------------------
       gcc@4.9.0  gcc@4.8.0  gcc@4.7.0  gcc@4.6.2  gcc@4.4.7
       gcc@4.8.2  gcc@4.7.1  gcc@4.6.3  gcc@4.6.1  gcc@4.1.2
   -- intel -------------------------------------------------------
       intel@15.0.0  intel@14.0.0  intel@13.0.0  intel@12.1.0  intel@10.0
       intel@14.0.3  intel@13.1.1  intel@12.1.5  intel@12.0.4  intel@9.1
       intel@14.0.2  intel@13.1.0  intel@12.1.3  intel@11.1
       intel@14.0.1  intel@13.0.1  intel@12.1.2  intel@10.1
   -- clang -------------------------------------------------------
       clang@3.4  clang@3.3  clang@3.2  clang@3.1
   -- pgi ---------------------------------------------------------
       pgi@14.3-0   pgi@13.2-0  pgi@12.1-0   pgi@10.9-0  pgi@8.0-1
       pgi@13.10-0  pgi@13.1-1  pgi@11.10-0  pgi@10.2-0  pgi@7.1-3
       pgi@13.6-0   pgi@12.8-0  pgi@11.1-0   pgi@9.0-4   pgi@7.0-6

Any of these compilers can be used to build Spack packages.  More on
how this is done is in :ref:`sec-specs`.

.. _spack-compiler-add:

^^^^^^^^^^^^^^^^^^^^^^
``spack compiler add``
^^^^^^^^^^^^^^^^^^^^^^

An alias for ``spack compiler find``.

.. _spack-compiler-find:

^^^^^^^^^^^^^^^^^^^^^^^
``spack compiler find``
^^^^^^^^^^^^^^^^^^^^^^^

If you do not see a compiler in this list, but you want to use it with
Spack, you can simply run ``spack compiler find`` with the path to
where the compiler is installed.  For example:

.. code-block:: console

   $ spack compiler find /usr/local/tools/ic-13.0.079
   ==> Added 1 new compiler to /Users/gamblin2/.spack/compilers.yaml
       intel@13.0.079

Or you can run ``spack compiler find`` with no arguments to force
auto-detection.  This is useful if you do not know where compilers are
installed, but you know that new compilers have been added to your
``PATH``.  For example, using dotkit, you might do this:

.. code-block:: console

   $ module load gcc-4.9.0
   $ spack compiler find
   ==> Added 1 new compiler to /Users/gamblin2/.spack/compilers.yaml
       gcc@4.9.0

This loads the environment module for gcc-4.9.0 to add it to
``PATH``, and then it adds the compiler to Spack.

.. _spack-compiler-info:

^^^^^^^^^^^^^^^^^^^^^^^
``spack compiler info``
^^^^^^^^^^^^^^^^^^^^^^^

If you want to see specifics on a particular compiler, you can run
``spack compiler info`` on it:

.. code-block:: console

   $ spack compiler info intel@15
   intel@15.0.0:
           cc  = /usr/local/bin/icc-15.0.090
           cxx = /usr/local/bin/icpc-15.0.090
           f77 = /usr/local/bin/ifort-15.0.090
           fc  = /usr/local/bin/ifort-15.0.090
           modules  = []
           operating system  = centos6

This shows which C, C++, and Fortran compilers were detected by Spack.
Notice also that we didn't have to be too specific about the
version. We just said ``intel@15``, and information about the only
matching Intel compiler was displayed.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Manual compiler configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If auto-detection fails, you can manually configure a compiler by
editing your ``~/.spack/compilers.yaml`` file.  You can do this by running
``spack config edit compilers``, which will open the file in your ``$EDITOR``.

Each compiler configuration in the file looks like this:

.. code-block:: yaml

   compilers:
   - compiler:
       modules = []
       operating_system: centos6
       paths:
         cc: /usr/local/bin/icc-15.0.024-beta
         cxx: /usr/local/bin/icpc-15.0.024-beta
         f77: /usr/local/bin/ifort-15.0.024-beta
         fc: /usr/local/bin/ifort-15.0.024-beta
       spec: intel@15.0.0:

For compilers, like ``clang``, that do not support Fortran, put
``None`` for ``f77`` and ``fc``:

.. code-block:: yaml

       paths:
         cc: /usr/bin/clang
         cxx: /usr/bin/clang++
         f77: None
         fc: None
       spec: clang@3.3svn:

Once you save the file, the configured compilers will show up in the
list displayed by ``spack compilers``.

You can also add compiler flags to manually configured compilers. The
valid flags are ``cflags``, ``cxxflags``, ``fflags``, ``cppflags``,
``ldflags``, and ``ldlibs``. For example:

.. code-block:: yaml

   compilers:
   - compiler:
       modules = []
       operating_system: OS
       paths:
         cc: /usr/local/bin/icc-15.0.024-beta
         cxx: /usr/local/bin/icpc-15.0.024-beta
         f77: /usr/local/bin/ifort-15.0.024-beta
         fc: /usr/local/bin/ifort-15.0.024-beta
       parameters:
         cppflags: -O3 -fPIC
       spec: intel@15.0.0:

These flags will be treated by spack as if they were enterred from
the command line each time this compiler is used. The compiler wrappers
then inject those flags into the compiler command. Compiler flags
enterred from the command line will be discussed in more detail in the
following section.

.. _cray-support:

-------------
Spack on Cray
-------------

Spack differs slightly when used on a Cray system. The architecture spec
can differentiate between the front-end and back-end processor and operating system.
For example, on Edison at NERSC, the back-end target processor
is "Ivy Bridge", so you can specify to use the back-end this way:

.. code-block:: console

   $ spack install zlib target=ivybridge

You can also use the operating system to build against the back-end:

.. code-block:: console

   $ spack install zlib os=CNL10

Notice that the name includes both the operating system name and the major
version number concatenated together.

Alternatively, if you want to build something for the front-end,
you can specify the front-end target processor. The processor for a login node
on Edison is "Sandy bridge" so we specify on the command line like so:

.. code-block:: console

   $ spack install zlib target=sandybridge

And the front-end operating system is:

.. code-block:: console

   $ spack install zlib os=SuSE11

^^^^^^^^^^^^^^^^^^^^^^^
Cray compiler detection
^^^^^^^^^^^^^^^^^^^^^^^

Spack can detect compilers using two methods. For the front-end, we treat
everything the same. The difference lies in back-end compiler detection.
Back-end compiler detection is made via the Tcl module avail command.
Once it detects the compiler it writes the appropriate PrgEnv and compiler
module name to compilers.yaml and sets the paths to each compiler with Cray\'s
compiler wrapper names (i.e. cc, CC, ftn). During build time, Spack will load
the correct PrgEnv and compiler module and will call appropriate wrapper.

The compilers.yaml config file will also differ. There is a
modules section that is filled with the compiler's Programming Environment
and module name. On other systems, this field is empty []:

.. code-block:: yaml

   - compiler:
       modules:
         - PrgEnv-intel
         - intel/15.0.109

As mentioned earlier, the compiler paths will look different on a Cray system.
Since most compilers are invoked using cc, CC and ftn, the paths for each
compiler are replaced with their respective Cray compiler wrapper names:

.. code-block:: yaml

     paths:
       cc: cc
       cxx: CC
       f77: ftn
       fc: ftn

As opposed to an explicit path to the compiler executable. This allows Spack
to call the Cray compiler wrappers during build time.

For more on compiler configuration, check out :ref:`compiler-config`.

Spack sets the default Cray link type to dynamic, to better match other
other platforms. Individual packages can enable static linking (which is the
default outside of Spack on cray systems) using the ``-static`` flag.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setting defaults and using Cray modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use default compilers for each PrgEnv and also be able
to load cray external modules, you will need to set up a ``packages.yaml``.

Here's an example of an external configuration for cray modules:

.. code-block:: yaml

   packages:
     mpi:
       modules:
         mpich@7.3.1%gcc@5.2.0 arch=cray_xc-haswell-CNL10: cray-mpich
         mpich@7.3.1%intel@16.0.0.109 arch=cray_xc-haswell-CNL10: cray-mpich

This tells Spack that for whatever package that depends on mpi, load the
cray-mpich module into the environment. You can then be able to use whatever
environment variables, libraries, etc, that are brought into the environment
via module load.

You can set the default compiler that Spack can use for each compiler type.
If you want to use the Cray defaults, then set them under ``all:`` in packages.yaml.
In the compiler field, set the compiler specs in your order of preference.
Whenever you build with that compiler type, Spack will concretize to that version.

Here is an example of a full packages.yaml used at NERSC

.. code-block:: yaml

   packages:
     mpi:
       modules:
         mpich@7.3.1%gcc@5.2.0 arch=cray_xc-CNL10-ivybridge: cray-mpich
         mpich@7.3.1%intel@16.0.0.109 arch=cray_xc-SuSE11-ivybridge: cray-mpich
       buildable: False
     netcdf:
       modules:
         netcdf@4.3.3.1%gcc@5.2.0 arch=cray_xc-CNL10-ivybridge: cray-netcdf
         netcdf@4.3.3.1%intel@16.0.0.109 arch=cray_xc-CNL10-ivybridge: cray-netcdf
       buildable: False
     hdf5:
       modules:
         hdf5@1.8.14%gcc@5.2.0 arch=cray_xc-CNL10-ivybridge: cray-hdf5
         hdf5@1.8.14%intel@16.0.0.109 arch=cray_xc-CNL10-ivybridge: cray-hdf5
       buildable: False
     all:
       compiler: [gcc@5.2.0, intel@16.0.0.109]

Here we tell spack that whenever we want to build with gcc use version 5.2.0 or
if we want to build with intel compilers, use version 16.0.0.109. We add a spec
for each compiler type for each cray modules. This ensures that for each
compiler on our system we can use that external module.

For more on external packages check out the section :ref:`sec-external_packages`.

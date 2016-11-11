.. _getting_started:

===============
Getting Started
===============

-------------
Prerequisites
-------------

Spack has the following minimum requirements, which must be installed
before Spack is run:

1. Python 2.6 or 2.7
2. A C/C++ compiler
3. The ``git`` and ``curl`` commands.

These requirements can be easily installed on most modern Linux systems;
on Macintosh, XCode is required.  Spack is designed to run on HPC
platforms like Cray and BlueGene/Q.  Not all packages should be expected
to work on all platforms.  A build matrix showing which packages are
working on which systems is planned but not yet available.

------------
Installation
------------

Getting Spack is easy.  You can clone it from the `github repository
<https://github.com/llnl/spack>`_ using this command:

.. code-block:: console

   $ git clone https://github.com/llnl/spack.git

This will create a directory called ``spack``.

^^^^^^^^^^^^^^^^^^^^^^^^
Add Spack to the Shell
^^^^^^^^^^^^^^^^^^^^^^^^

We'll assume that the full path to your downloaded Spack directory is
in the ``SPACK_ROOT`` environment variable.  Add ``$SPACK_ROOT/bin``
to your path and you're ready to go:

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

^^^^^^^^^^^^^^^^^
Clean Environment
^^^^^^^^^^^^^^^^^

Many packages' installs can be broken by changing environment
variables.  For example, a package might pick up the wrong build-time
dependencies (most of them not specified) depending on the setting of
``PATH``.  ``GCC`` seems to be particularly vulnerable to these issues.

Therefore, it is recommended that Spack users run with a *clean
environment*, especially for ``PATH``.  Only software that comes with
the system, or that you know you wish to use with Spack, should be
included.  This procedure will avoid many strange build errors.


^^^^^^^^^^^^^^^^^^
Check Installation
^^^^^^^^^^^^^^^^^^

With Spack installed, you should be able to run some basic Spack
commands.  For example:

.. code-block:: console

    $ spack spec netcdf
      ...
      netcdf@4.4.1%gcc@5.3.0~hdf4+mpi arch=linux-SuSE11-x86_64
          ^curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
              ^openssl@system%gcc@5.3.0 arch=linux-SuSE11-x86_64
              ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
          ^hdf5@1.10.0-patch1%gcc@5.3.0+cxx~debug+fortran+mpi+shared~szip~threadsafe arch=linux-SuSE11-x86_64
              ^openmpi@1.10.1%gcc@5.3.0~mxm~pmi~psm~psm2~slurm~sqlite3~thread_multiple~tm+verbs+vt arch=linux-SuSE11-x86_64
          ^m4@1.4.17%gcc@5.3.0+sigsegv arch=linux-SuSE11-x86_64
              ^libsigsegv@2.10%gcc@5.3.0 arch=linux-SuSE11-x86_64

^^^^^^^^^^^^^^^^^^^^^^^^^^
Optional: Alternate Prefix
^^^^^^^^^^^^^^^^^^^^^^^^^^

You may want to run Spack out of a prefix other than the git repository
you cloned.  The ``spack bootstrap`` command provides this
functionality.  To install spack in a new directory, simply type:

.. code-block:: console

   $ spack bootstrap /my/favorite/prefix

This will install a new spack script in ``/my/favorite/prefix/bin``,
which you can use just like you would the regular spack script.  Each
copy of spack installs packages into its own ``$PREFIX/opt``
directory.


^^^^^^^^^^
Next Steps
^^^^^^^^^^

In theory, Spack doesn't need any additional installation; just
download and run!  But in real life, additional steps are usually
required before Spack can work in a practical sense.  Read on...


.. _compiler-config:

----------------------
Compiler configuration
----------------------

Spack has the ability to build packages with multiple compilers and
compiler versions. Spack searches for compilers on your machine
automatically the first time it is run. It does this by inspecting
your ``PATH``.

.. _cmd-spack-compilers:

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
``PATH``.  For example, you might load a module, like this:

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
     paths:
       cc  = /usr/local/bin/icc-15.0.090
       cxx = /usr/local/bin/icpc-15.0.090
       f77 = /usr/local/bin/ifort-15.0.090
       fc  = /usr/local/bin/ifort-15.0.090
     modules = []
     operating system = centos6
   ...

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
       modules: []
       operating_system: centos6
       paths:
         cc: /usr/local/bin/icc-15.0.024-beta
         cxx: /usr/local/bin/icpc-15.0.024-beta
         f77: /usr/local/bin/ifort-15.0.024-beta
         fc: /usr/local/bin/ifort-15.0.024-beta
       spec: intel@15.0.0:

For compilers that do not support Fortran (like ``clang``), put
``None`` for ``f77`` and ``fc``:

.. code-block:: yaml

   compilers:
   - compiler:
       modules: []
       operating_system: centos6
       paths:
         cc: /usr/bin/clang
         cxx: /usr/bin/clang++
         f77: None
         fc: None
       spec: clang@3.3svn

Once you save the file, the configured compilers will show up in the
list displayed by ``spack compilers``.

You can also add compiler flags to manually configured compilers. These
flags should be specified in the ``flags`` section of the compiler
specification. The valid flags are ``cflags``, ``cxxflags``, ``fflags``,
``cppflags``, ``ldflags``, and ``ldlibs``. For example:

.. code-block:: yaml

   compilers:
   - compiler:
       modules: []
       operating_system: centos6
       paths:
         cc: /usr/bin/gcc
         cxx: /usr/bin/g++
         f77: /usr/bin/gfortran
         fc: /usr/bin/gfortran
       flags:
         cflags: -O3 -fPIC
         cxxflags: -O3 -fPIC
         cppflags: -O3 -fPIC
       spec: gcc@4.7.2

These flags will be treated by spack as if they were entered from
the command line each time this compiler is used. The compiler wrappers
then inject those flags into the compiler command. Compiler flags
entered from the command line will be discussed in more detail in the
following section.

^^^^^^^^^^^^^^^^^^^^^^^
Build Your Own Compiler
^^^^^^^^^^^^^^^^^^^^^^^

If you are particular about which compiler/version you use, you might
wish to have Spack build it for you.  For example:

.. code-block:: console

   $ spack install gcc@4.9.3

Once that has finished, you will need to add it to your
``compilers.yaml`` file.  You can then set Spack to use it by default
by adding the following to your ``packages.yaml`` file:

.. code-block:: yaml

   packages:
     all:
       compiler: [gcc@4.9.3]


.. tip::

    If you are building your own compiler, some users prefer to have a
    Spack instance just for that.  For example, create a new Spack in
    ``~/spack-tools`` and then run ``~/spack-tools/bin/spack install
    gcc@4.9.3``.  Once the compiler is built, don't build anything
    more in that Spack instance; instead, create a new "real" Spack
    instance, configure Spack to use the compiler you've just built,
    and then build your application software in the new Spack
    instance.  Following this tip makes it easy to delete all your
    Spack packages *except* the compiler.


^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compilers Requiring Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many installed compilers will work regardless of the environment they
are called with.  However, some installed compilers require
``$LD_LIBRARY_PATH`` or other environment variables to be set in order
to run; this is typical for Intel and other proprietary compilers.

In such a case, you should tell Spack which module(s) to load in order
to run the chosen compiler (If the compiler does not come with a
module file, you might consider making one by hand).  Spack will load
this module into the environment ONLY when the compiler is run, and
NOT in general for a package's ``install()`` method.  See, for
example, this ``compilers.yaml`` file:

.. code-block:: yaml

   compilers:
   - compiler:
       modules: [other/comp/gcc-5.3-sp3]
       operating_system: SuSE11
       paths:
         cc: /usr/local/other/SLES11.3/gcc/5.3.0/bin/gcc
         cxx: /usr/local/other/SLES11.3/gcc/5.3.0/bin/g++
         f77: /usr/local/other/SLES11.3/gcc/5.3.0/bin/gfortran
         fc: /usr/local/other/SLES11.3/gcc/5.3.0/bin/gfortran
       spec: gcc@5.3.0

Some compilers require special environment settings to be loaded not just
to run, but also to execute the code they build, breaking packages that
need to execute code they just compiled.  If it's not possible or
practical to use a better compiler, you'll need to ensure that
environment settings are preserved for compilers like this (i.e., you'll
need to load the module or source the compiler's shell script).

By default, Spack tries to ensure that builds are reproducible by
cleaning the environment before building.  If this interferes with your
compiler settings, you CAN use ``spack install --dirty`` as a workaround.
Note that this MAY interfere with package builds.

.. _licensed-compilers:

^^^^^^^^^^^^^^^^^^
Licensed Compilers
^^^^^^^^^^^^^^^^^^

Some proprietary compilers require licensing to use.  If you need to
use a licensed compiler (eg, PGI), the process is similar to a mix of
build your own, plus modules:

#. Create a Spack package (if it doesn't exist already) to install
   your compiler.  Follow instructions on installing :ref:`license`.

#. Once the compiler is installed, you should be able to test it by
   using Spack to load the module it just created, and running simple
   builds (eg: ``cc helloWorld.c && ./a.out``)

#. Add the newly-installed compiler to ``compilers.yaml`` as shown
   above.

.. _mixed-toolchains:

^^^^^^^^^^^^^^^^
Mixed Toolchains
^^^^^^^^^^^^^^^^

Modern compilers typically come with related compilers for C, C++ and
Fortran bundled together.  When possible, results are best if the same
compiler is used for all languages.

In some cases, this is not possible.  For example, starting with macOS El
Capitan (10.11), many packages no longer build with GCC, but XCode
provides no Fortran compilers.  The user is therefore forced to use a
mixed toolchain: XCode-provided Clang for C/C++ and GNU ``gfortran`` for
Fortran.

#. You need to make sure that command-line tools are installed. To that
   end run ``$ xcode-select --install``.

#. Run ``$ spack compiler find`` to locate Clang.

#. There are different ways to get ``gfortran`` on macOS. For example, you can
   install GCC with Spack (``$ spack install gcc``) or with Homebrew
   (``$ brew install gcc``).

#. The only thing left to do is to edit ``~/.spack/compilers.yaml`` to provide
   the path to ``gfortran``:

   .. code-block:: yaml

      compilers:
        darwin-x86_64:
          clang@7.3.0-apple:
            cc: /usr/bin/clang
            cxx: /usr/bin/clang++
            f77: /path/to/bin/gfortran
            fc: /path/to/bin/gfortran

   If you used Spack to install GCC, you can get the installation prefix by
   ``$ spack location -i gcc`` (this will only work if you have a single version
   of GCC installed). Whereas for Homebrew, GCC is installed in
   ``/usr/local/Cellar/gcc/x.y.z``.

^^^^^^^^^^^^^^^^^^^^^
Compiler Verification
^^^^^^^^^^^^^^^^^^^^^

You can verify that your compilers are configured properly by installing a
simple package.  For example:

.. code-block:: console

   $ spack install zlib%gcc@5.3.0

--------------------------------------
Vendor-Specific Compiler Configuration
--------------------------------------

With Spack, things usually "just work" with GCC.  Not so for other
compilers.  This section provides details on how to get specific
compilers working.

^^^^^^^^^^^^^^^
Intel Compilers
^^^^^^^^^^^^^^^

Intel compilers are unusual because a single Intel compiler version
can emulate multiple GCC versions.  In order to provide this
functionality, the Intel compiler needs GCC to be installed.
Therefore, the following steps are necessary to successfully use Intel
compilers:

#. Install a version of GCC that implements the desired language
   features (``spack install gcc``).

#. Tell the Intel compiler how to find that desired GCC.  This may be
   done in one of two ways:

      "By default, the compiler determines which version of ``gcc`` or ``g++``
      you have installed from the ``PATH`` environment variable.

      If you want use a version of ``gcc`` or ``g++`` other than the default
      version on your system, you need to use either the ``-gcc-name``
      or ``-gxx-name`` compiler option to specify the path to the version of
      ``gcc`` or ``g++`` that you want to use."

      -- `Intel Reference Guide <https://software.intel.com/en-us/node/522750>`_

Intel compilers may therefore be configured in one of two ways with
Spack: using modules, or using compiler flags.

""""""""""""""""""""""""""
Configuration with Modules
""""""""""""""""""""""""""

One can control which GCC is seen by the Intel compiler with modules.
A module must be loaded both for the Intel Compiler (so it will run)
and GCC (so the compiler can find the intended GCC).  The following
configuration in ``compilers.yaml`` illustrates this technique:

.. code-block:: yaml

   compilers:
   - compiler:
       modules: [gcc-4.9.3, intel-15.0.24]
       operating_system: centos7
       paths:
         cc: /opt/intel-15.0.24/bin/icc-15.0.24-beta
         cxx: /opt/intel-15.0.24/bin/icpc-15.0.24-beta
         f77: /opt/intel-15.0.24/bin/ifort-15.0.24-beta
         fc: /opt/intel-15.0.24/bin/ifort-15.0.24-beta
       spec: intel@15.0.24.4.9.3


.. note::

   The version number on the Intel compiler is a combination of
   the "native" Intel version number and the GNU compiler it is
   targeting.

""""""""""""""""""""""""""
Command Line Configuration
""""""""""""""""""""""""""

One can also control which GCC is seen by the Intel compiler by adding
flags to the ``icc`` command:

#. Identify the location of the compiler you just installed:

   .. code-block:: console

       $ spack location --install-dir gcc
       /home2/rpfische/spack2/opt/spack/linux-centos7-x86_64/gcc-4.9.3-iy4rw...

#. Set up ``compilers.yaml``, for example:

   .. code-block:: yaml

       compilers:
       - compiler:
           modules: [intel-15.0.24]
           operating_system: centos7
           paths:
             cc: /opt/intel-15.0.24/bin/icc-15.0.24-beta
             cflags: -gcc-name /home2/rpfische/spack2/opt/spack/linux-centos7-x86_64/gcc-4.9.3-iy4rw.../bin/gcc
             cxx: /opt/intel-15.0.24/bin/icpc-15.0.24-beta
             cxxflags: -gxx-name /home2/rpfische/spack2/opt/spack/linux-centos7-x86_64/gcc-4.9.3-iy4rw.../bin/g++
             f77: /opt/intel-15.0.24/bin/ifort-15.0.24-beta
             fc: /opt/intel-15.0.24/bin/ifort-15.0.24-beta
             fflags: -gcc-name /home2/rpfische/spack2/opt/spack/linux-centos7-x86_64/gcc-4.9.3-iy4rw.../bin/gcc
           spec: intel@15.0.24.4.9.3


^^^
PGI
^^^

PGI comes with two sets of compilers for C++ and Fortran,
distinguishable by their names.  "Old" compilers:

.. code-block:: yaml

    cc:  /soft/pgi/15.10/linux86-64/15.10/bin/pgcc
    cxx: /soft/pgi/15.10/linux86-64/15.10/bin/pgCC
    f77: /soft/pgi/15.10/linux86-64/15.10/bin/pgf77
    fc:  /soft/pgi/15.10/linux86-64/15.10/bin/pgf90

"New" compilers:

.. code-block:: yaml

    cc:  /soft/pgi/15.10/linux86-64/15.10/bin/pgcc
    cxx: /soft/pgi/15.10/linux86-64/15.10/bin/pgc++
    f77: /soft/pgi/15.10/linux86-64/15.10/bin/pgfortran
    fc:  /soft/pgi/15.10/linux86-64/15.10/bin/pgfortran

Older installations of PGI contains just the old compilers; whereas
newer installations contain the old and the new.  The new compiler is
considered preferable, as some packages
(``hdf``) will not build with the old compiler.

When auto-detecting a PGI compiler, there are cases where Spack will
find the old compilers, when you really want it to find the new
compilers.  It is best to check this ``compilers.yaml``; and if the old
compilers are being used, change ``pgf77`` and ``pgf90`` to
``pgfortran``.

Other issues:

* There are reports that some packages will not build with PGI,
  including ``libpciaccess`` and ``openssl``.  A workaround is to
  build these packages with another compiler and then use them as
  dependencies for PGI-build packages.  For example:

  .. code-block:: console

     $ spack install openmpi%pgi ^libpciaccess%gcc


* PGI requires a license to use; see :ref:`licensed-compilers` for more
  information on installation.

.. note::

   It is believed the problem with HDF 4 is that everything is
   compiled with the ``F77`` compiler, but at some point some Fortran
   90 code slipped in there. So compilers that can handle both FORTRAN
   77 and Fortran 90 (``gfortran``, ``pgfortran``, etc) are fine.  But
   compilers specific to one or the other (``pgf77``, ``pgf90``) won't
   work.


^^^
NAG
^^^

The Numerical Algorithms Group provides a licensed Fortran compiler. Like Clang,
this requires you to set up a :ref:`mixed-toolchains`. It is recommended to use
GCC for your C/C++ compilers.

The NAG Fortran compilers are a bit more strict than other compilers, and many
packages will fail to install with error messages like:

.. code-block:: none

   Error: mpi_comm_spawn_multiple_f90.f90: Argument 3 to MPI_COMM_SPAWN_MULTIPLE has data type DOUBLE PRECISION in reference from MPI_COMM_SPAWN_MULTIPLEN and CHARACTER in reference from MPI_COMM_SPAWN_MULTIPLEA

In order to convince the NAG compiler not to be too picky about calling conventions,
you can use ``FFLAGS=-mismatch`` and ``FCFLAGS=-mismatch``. This can be done through
the command line:

.. code-block:: console

   $ spack install openmpi fflags=\"-mismatch\"

Or it can be set permanently in your ``compilers.yaml``:

.. code-block:: yaml

   - compiler:
    modules: []
    operating_system: centos6
    paths:
      cc: /soft/spack/opt/spack/linux-x86_64/gcc-5.3.0/gcc-6.1.0-q2zosj3igepi3pjnqt74bwazmptr5gpj/bin/gcc
      cxx: /soft/spack/opt/spack/linux-x86_64/gcc-5.3.0/gcc-6.1.0-q2zosj3igepi3pjnqt74bwazmptr5gpj/bin/g++
      f77: /soft/spack/opt/spack/linux-x86_64/gcc-4.4.7/nag-6.1-jt3h5hwt5myezgqguhfsan52zcskqene/bin/nagfor
      fc: /soft/spack/opt/spack/linux-x86_64/gcc-4.4.7/nag-6.1-jt3h5hwt5myezgqguhfsan52zcskqene/bin/nagfor
    flags:
      fflags: -mismatch
    spec: nag@6.1

---------------
System Packages
---------------

Once compilers are configured, one needs to determine which
pre-installed system packages, if any, to use in builds.  This is
configured in the file ``~/.spack/packages.yaml``.  For example, to use
an OpenMPI installed in /opt/local, one would use:

.. code-block:: yaml

    packages:
        openmpi:
            paths:
                openmpi@1.10.1: /opt/local
            buildable: False

In general, Spack is easier to use and more reliable if it builds all of
its own dependencies.  However, there are two packages for which one
commonly needs to use system versions:

^^^
MPI
^^^

On supercomputers, sysadmins have already built MPI versions that take
into account the specifics of that computer's hardware.  Unless you
know how they were built and can choose the correct Spack variants,
you are unlikely to get a working MPI from Spack.  Instead, use an
appropriate pre-installed MPI.

If you choose a pre-installed MPI, you should consider using the
pre-installed compiler used to build that MPI; see above on
``compilers.yaml``.

^^^^^^^
OpenSSL
^^^^^^^

The ``openssl`` package underlies much of modern security in a modern
OS; an attacker can easily "pwn" any computer on which they can modify SSL.
Therefore, any ``openssl`` used on a system should be created in a
"trusted environment" --- for example, that of the OS vendor.

OpenSSL is also updated by the OS vendor from time to time, in
response to security problems discovered in the wider community.  It
is in everyone's best interest to use any newly updated versions as
soon as they come out.  Modern Linux installations have standard
procedures for security updates without user involvement.

Spack running at user-level is not a trusted environment, nor do Spack
users generally keep up-to-date on the latest security holes in SSL.  For
these reasons, a Spack-installed OpenSSL should likely not be trusted.

As long as the system-provided SSL works, you can use it instead.  One
can check if it works by trying to download an ``https://``.  For
example:

.. code-block:: console

    $ curl -O https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz

The recommended way to tell Spack to use the system-supplied OpenSSL is
to add the following to ``packages.yaml``.  Note that the ``@system``
"version" means "I don't care what version it is, just use what is
there."  This is reasonable for OpenSSL, which has a stable API.


.. code-block:: yaml

    packages:
        openssl:
            paths:
                openssl@system: /usr
            version: [system]
            buildable: False


^^^^^^^^^^^^^
BLAS / LAPACK
^^^^^^^^^^^^^

The recommended way to use system-supplied BLAS / LAPACK packages is
to add the following to ``packages.yaml``:

.. code-block:: yaml

    packages:
        netlib-lapack:
            paths:
                netlib-lapack@system: /usr
            version: [system]
            buildable: False
        all:
            providers:
                blas: [netlib-lapack]
                lapack: [netlib-lapack]

.. note::

   The ``@system`` "version" means "I don't care what version it is,
   just use what is there." Above we pretend that the system-provided
   Blas/Lapack is ``netlib-lapack`` only because it is the only BLAS / LAPACK
   provider which use standard names for libraries (as opposed to, for example,
   `libopenblas.so`).

   Although we specify external package in ``/usr``, Spack is smart enough not
   to add ``/usr/lib`` to RPATHs, where it could cause unrelated system
   libraries to be used instead of their Spack equivalents. ``usr/bin`` will be
   present in PATH, however it will have lower precedence compared to paths
   from other dependencies. This ensures that binaries in Spack dependencies
   are preferred over system binaries.

^^^
Git
^^^

Some Spack packages use ``git`` to download, which might not work on
some computers.  For example, the following error was
encountered on a Macintosh during ``spack install julia-master``:

.. code-block:: console

   ==> Trying to clone git repository:
     https://github.com/JuliaLang/julia.git
     on branch master
   Cloning into 'julia'...
   fatal: unable to access 'https://github.com/JuliaLang/julia.git/':
       SSL certificate problem: unable to get local issuer certificate

This problem is related to OpenSSL, and in some cases might be solved
by installing a new version of ``git`` and ``openssl``:

#. Run ``spack install git``
#. Add the output of ``spack module loads git`` to your ``.bahsrc``.

If this doesn't work, it is also possible to disable checking of SSL
certificates by using:

.. code-block:: console

   $ spack --insecure install

Using ``--insecure`` makes Spack disable SSL checking when fetching
from websites and from git.

.. warning::

   This workaround should be used ONLY as a last resort!  Wihout SSL
   certificate verification, spack and git will download from sites you
   wouldn't normally trust.  The code you download and run may then be
   compromised!  While this is not a major issue for archives that will
   be checksummed, it is especially problematic when downloading from
   name Git branches or tags, which relies entirely on trusting a
   certificate for security (no verification).

-----------------------
Utilities Configuration
-----------------------

Although Spack does not need installation *per se*, it does rely on
other packages to be available on its host system.  If those packages
are out of date or missing, then Spack will not work.  Sometimes, an
appeal to the system's package manager can fix such problems.  If not,
the solution is have Spack install the required packages, and then
have Spack use them.

For example, if ``curl`` doesn't work, one could use the following steps
to provide Spack a working ``curl``:

.. code-block:: console

    $ spack install curl
    $ spack load curl

or alternately:

.. code-block:: console

    $ spack module loads curl >>~/.bashrc

or if environment modules don't work:

.. code-block:: console

    $ export PATH=`spack location --install-dir curl`/bin:$PATH


External commands are used by Spack in two places: within core Spack,
and in the package recipes. The bootstrapping procedure for these two
cases is somewhat different, and is treated separately below.

^^^^^^^^^^^^^^^^^^^^
Core Spack Utilities
^^^^^^^^^^^^^^^^^^^^

Core Spack uses the following packages, mainly to download and unpack
source code, and to load generated environment modules: ``curl``,
``env``, ``git``, ``go``, ``hg``, ``svn``, ``tar``, ``unzip``,
``patch``, ``environment-modules``.

As long as the user's environment is set up to successfully run these
programs from outside of Spack, they should work inside of Spack as
well.  They can generally be activated as in the ``curl`` example above;
or some systems might already have an appropriate hand-built
environment module that may be loaded.  Either way works.

A few notes on specific programs in this list:

""""""""""""""""""""""""""
cURL, git, Mercurial, etc.
""""""""""""""""""""""""""

Spack depends on cURL to download tarballs, the format that most
Spack-installed packages come in.  Your system's cURL should always be
able to download unencrypted ``http://``.  However, the cURL on some
systems has problems with SSL-enabled ``https://`` URLs, due to
outdated / insecure versions of OpenSSL on those systems.  This will
prevent Spack from installing any software requiring ``https://``
until a new cURL has been installed, using the technique above.

.. warning::

   remember that if you install ``curl`` via Spack that it may rely on a
   user-space OpenSSL that is not upgraded regularly.  It may fall out of
   date faster than your system OpenSSL.

Some packages use source code control systems as their download method:
``git``, ``hg``, ``svn`` and occasionally ``go``.  If you had to install
a new ``curl``, then chances are the system-supplied version of these
other programs will also not work, because they also rely on OpenSSL.
Once ``curl`` has been installed, you can similarly install the others.


.. _InstallEnvironmentModules:

"""""""""""""""""""
Environment Modules
"""""""""""""""""""

In order to use Spack's generated environment modules, you must have
installed one of *Environment Modules* or *Lmod*.  On many Linux
distributions, this can be installed from the vendor's repository.  For
example: ``yum install environment-modules`` (Fedora/RHEL/CentOS).  If
your Linux distribution does not have Environment Modules, you can get it
with Spack:

#. Consider using system tcl (as long as your system has Tcl version 8.0 or later):

   #) Identify its location using ``which tclsh``
   #) Identify its version using ``echo 'puts $tcl_version;exit 0' | tclsh``
   #) Add to ``~/.spack/packages.yaml`` and modify as appropriate:

      .. code-block:: yaml

         packages:
             tcl:
                 paths:
                     tcl@8.5: /usr
                 version: [8.5]
                 buildable: False

#. Install with:

   .. code-block:: console

      $ spack install environment-modules

#. Activate with the following script (or apply the updates to your
   ``.bashrc`` file manually):

   .. code-block:: sh

      TMP=`tempfile`
      echo >$TMP
      MODULE_HOME=`spack location --install-dir environment-modules`
      MODULE_VERSION=`ls -1 $MODULE_HOME/Modules | head -1`
      ${MODULE_HOME}/Modules/${MODULE_VERSION}/bin/add.modules <$TMP
      cp .bashrc $TMP
      echo "MODULE_VERSION=${MODULE_VERSION}" > .bashrc
      cat $TMP >>.bashrc

This adds to your ``.bashrc`` (or similar) files, enabling Environment
Modules when you log in.  Re-load your .bashrc (or log out and in
again), and then test that the ``module`` command is found with:

.. code-block:: console

   $ module avail


^^^^^^^^^^^^^^^^^
Package Utilities
^^^^^^^^^^^^^^^^^

Spack may also encounter bootstrapping problems inside a package's
``install()`` method.  In this case, Spack will normally be running
inside a *sanitized build environment*.  This includes all of the
package's dependencies, but none of the environment Spack inherited
from the user: if you load a module or modify ``$PATH`` before
launching Spack, it will have no effect.

In this case, you will likely need to use the ``--dirty`` flag when
running ``spack install``, causing Spack to **not** sanitize the build
environment.  You are now responsible for making sure that environment
does not do strange things to Spack or its installs.

Another way to get Spack to use its own version of something is to add
that something to a package that needs it.  For example:

.. code-block:: python

   depends_on('binutils', type='build')

This is considered best practice for some common build dependencies,
such as ``autotools`` (if the ``autoreconf`` command is needed) and
``cmake`` --- ``cmake`` especially, because different packages require
a different version of CMake.

""""""""
binutils
""""""""

.. https://groups.google.com/forum/#!topic/spack/i_7l_kEEveI

Sometimes, strange error messages can happen while building a package.
For example, ``ld`` might crash.  Or one receives a message like:

.. code-block:: console

   ld: final link failed: Nonrepresentable section on output


or:

.. code-block:: console

   ld: .../_fftpackmodule.o: unrecognized relocation (0x2a) in section `.text'

These problems are often caused by an outdated ``binutils`` on your
system.  Unlike CMake or Autotools, adding ``depends_on('binutils')`` to
every package is not considered a best practice because every package
written in C/C++/Fortran would need it.  A potential workaround is to
load a recent ``binutils`` into your environment and use the ``--dirty``
flag.


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

For more on external packages check out the section :ref:`sec-external-packages`.

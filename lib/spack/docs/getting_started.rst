.. _getting_started:

===============
Getting Started
===============

-------------
Prerequisites
-------------

Spack has the following minimum requirements, which must be installed
before Spack is run:

1. Operating System: GNU/Linux or Macintosh
2. Python 2.6 or 2.7
3. A C/C++ compiler

These requirements can be easily installed on most modern Linux
systems; on Macintosh, XCode is required.

------------
Installation
------------

Getting spack is easy.  You can clone it from the `github repository
<https://github.com/llnl/spack>`_ using this command:

.. code-block:: console

   $ git clone https://github.com/llnl/spack.git

This will create a directory called ``spack``.  If you are using Spack
for a specific purpose, you might have received different instructions
on how to download Spack; if so, please follow those instructions.

^^^^^^^^^^^^^^^^^^
Add Spack to Shell
^^^^^^^^^^^^^^^^^^

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
downlad and run!  But in real life, additional steps are usually
required before Spack can work in a practical sense.  Read on...


.. _compiler-config:

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

^^^^^^^^^^^^^^^^^^^^^^^
Build Your Own Compiler
^^^^^^^^^^^^^^^^^^^^^^^

If you are particular about which compiler/version you use, you might
wish to have Spack build it for you.  For example:

.. code-block::

    spack install gcc@4.9.3

Once that has finished, you will need to add it to your
``compilers.yaml`` file.  If this is your preferred compiler, in
general future Spack builds will use it.

.. note::

    If you are building your own compiler, it can be useful to have a
    Spack instance just for that.  For example, create a new Spack in
    ``~/spack-tools`` and then run ``~/spack-tools/bin/spack install
    gcc@4.9.3``.  Once the compiler is built, don't build anything
    more in that Spack instance; instead, create a new "real" Spack
    instance, configure Spack to use the compiler you've just built,
    and then build your application software in the new Spack
    instance.

    This tip is useful because sometimes you will find yourself
    rebuilding may pacakges due to Spack updates.  Sometimes, you
    might even delete your entire Spack installation and start fresh.
    If your compiler was built in a separate Spack installation, you
    will never have to rebuild it --- as long as you wish to continue
    using that version of the compiler.


^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compilers Requiring Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many installed compilers will work regardless of the environment they
are called with.  However, some installed compilers require
``$LD_LIBRARY_PATH`` or other environment variables to be set in order
to run; Intel compilers are known for this.  In such a case, you
should tell Spack which module(s) to load in order to run the chosen
compiler.  Spack will load this module into the environment ONLY when
the compiler is run, and NOT in general for a package's ``install()``
method.  See, for example, this ``compilers.yaml`` file:

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

Some compilers require a module to be loaded not just to run, but also
to execute any code built with the compiler, breaking packages that
execute any bits of code they just compiled.  Such compilers should be
taken behind the barn and put out of their misery.  If that is not
possible or practical, the user (and anyone running code built by that
compiler) will need to load the compiler's module into their
environment.  And ``spack install --dirty`` will need to be used.

^^^^^^^^^^^^^^^^^^^^^
Compiler Verification
^^^^^^^^^^^^^^^^^^^^^

You can verify that your compilers are configured properly by installing a
simple package.  For example:

.. code-block:: sh

    spack install zlib%gcc@5.3.0


---------------
System Packages
---------------

Once compilers are configured, one needs to determine which
pre-installed system packages, if any, to use in builds.  This is
configured in the file `~/.spack/packages.yaml`.  For example, to use
an OpenMPI installed in /opt/local, one would use:

.. code-block:: yaml

    packages:
        openmpi:
            paths:
                openmpi@1.10.1: /opt/local
            buildable: False

In general, Spack is easier to use and more reliable if it builds all
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
OS; an attacker can easily "pwn" any computer on which can modify SSL.
Therefore, any `openssl` used on a system should be created in a
"trusted environment" --- for example, that of the OS vendor.

OpenSSL is also updated by the OS vendor from time to time, in
response to security problems discovered in the wider community.  It
is in everyone's best interest to use any newly updated versions as
soon as they come out.  Modern Linux installations have standard
procedures for security updates without user involvement.

Spack running at user-level is not a trusted environment, nor do Spack
users generally keep up-to-date on the latest security holes in SSL.
For these reasons, any Spack-installed OpenSSL should be considered
untrusted.

As long as the system-provided SSL works, it is better to use it.  One can check if it works by trying to download an ``https://``.  For example:

.. code-block:: sh

    curl -O https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz

As long as it works, the recommended way to tell Spack to use the
system-supplied OpenSSL is to add the following to ``packages.yaml``.
Note that the ``@system`` "version" means "I don't care what version
it is, just use what is there."  This is appropriate for OpenSSL,
which has a stable API.


.. code-block:: yaml

    packages:
        # Recommended for security reasons
        # Do not install OpenSSL as non-root user.
        openssl:
            paths:
                openssl@system: /usr
            version: [system]
            buildable: False


-----------------------
Utilities Configuration
-----------------------

Although Spack does not need installation *per se*, it does rely on
other packages to be available on its host system.  If those packages
are out of date or missing, then Spack will not work.  Sometimes, an
appeal to the system's package manager can fix such problems.  If not,
the solution is have Spack install the required packages, and then
have Spack use them.

For example, if `curl` doesn't work, one could use the following steps
to provide Spack a working `curl`:

.. code-block:: console

    $ spack install curl
    $ spack load curl

or alternately:

.. code-block:: console

    $ spack module loads curl >>~/.bashrc

or if environment modules don't work:

.. code-block:: console

    $ export PATH=`spack location -i curl`/bin:$PATH


External commands are used by Spack in two places: within core Spack,
and in the package recipes. The bootstrapping procedure for these two
cases is somewhat different, and is treated separately below.

^^^^^^^^^^^^^^^^^^^^
Core Spack Utilities
^^^^^^^^^^^^^^^^^^^^

Core Spack uses the following packages, aminly to download and unpack
source code, and to load generated environment modules: ``curl``,
``env``, ``git``, ``go``, ``hg``, ``svn``, ``tar``, ``unzip``,
``patch``, ``environment-modules``.

As long as the user's environment is set up to successfully run these
programs from outside of Spack, they should work inside of Spack as
well.  They can generally be activated as in the `curl` example above;
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

    ``curl`` depends on ``openssl`` and ``zlib``, both of which are
    downloadable from non-SSL sources.  Unfortunately, this
    Spack-built cURL should be considered untrustworthy for
    ``https://`` sources becuase it relies on an OpenSSL built in user
    space.  Luckily, Spack verifies checksums of the software it
    installs, and does not rely on a secure SSL implementation.

    If your version of ``curl`` is not trustworthy, then you should
    *not* use it outside of Spack.  Instead of putting it in your
    ``.bashrc``, you might wish to create a short shell script that
    loads the appropariate module(s) and then launches Spack.

Some packages use source code control systems as their download
method: ``git``, ``hg``, ``svn`` and occasionally ``go``.  If you had
to install a new ``curl``, then chances are the system-supplied
version of these other programs will also not work, because they also
rely on OpenSSL.  Once ``curl`` has been installed, the others should
also be installable.


.. _InstallEnvironmentModules:

"""""""""""""""""""
Environment Modules
"""""""""""""""""""

In order to use Spack's generated environment modules, you must have
installed the *Environment Modules* package.  On many Linux
distributions, this can be installed from the vendor's repository.
For example: """yum install environment-modules``
(Fedora/RHEL/CentOS).  If your Linux distribution does not have
Environment Modules, you can get it with Spack:

1. Consider using system tcl (as long as your system has Tcl version 8.0 or later):
    # Identify its location using ``which tclsh``
    # Identify its version using ``echo 'puts $tcl_version;exit 0' | tclsh``
    # Add to ``~/.spack/packages.yaml`` and modify as appropriate:

       .. code-block:: yaml

           packages:
               tcl:
                   paths:
                       tcl@8.5: /usr
                   version: [8.5]
                   buildable: False

2. Install with::
   .. code-block:: console

       $ spack install environment-modules

3. Activate with the following script (or apply the updates to your
   ``.bashrc`` file manually)::

   .. code-block:: sh

       TMP=`tempfile`
       echo >$TMP
       MODULE_HOME=`spack location -i environment-modules`
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

In this case, you will likley need to use the ``--dirty`` flag when
running ``spack install``, causing Spack to **not** santize the build
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
For exmaple, ``ld`` might crash.  Or one receives a message like:

.. code-block::

    ld: final link failed: Nonrepresentable section on output

These problems are often caused by an outdated ``binutils`` on your
system.  Unlike CMake or Autotools, adding ``depends_on('binutils')``
to every package is not considered a best practice because every
package written in C/C++/Fortran would need it.  Instead, load a
recent ``binutils`` into your environment and use the ``--dirty``
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

For more on external packages check out the section :ref:`sec-external_packages`.

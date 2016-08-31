===============
Spack Workflows
===============

The process of using Spack involves building packages, running
binaries from those packages, and developing software that depends on
those packages.  For example, one might use Spack to build the
`netcdf` package, use `spack load` to run the `ncdump` binary, and
finally, write a small C program to read/write a particular NetCDF file.

Spack supports a variety of workflows to suit a variety of situaions
and user preferences, there is no single way to do all these things.
This chapter demonstrates different workflows that have been
developed, pointing out the pros and cons of them.

-----------
Definitions
-----------

First some basic definitions.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Package, Concrete Spec, Installed Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Spack, a package is an abstract recipe to build one piece of software.
Spack packages may be used to build, in principle, any version of that
software with any set of variants.  Examples of packages include
``curl`` and ``zlib``.

A package may be *instantiated* to produce a concrete spec; one
possible realization of a particular package, out of combinatorially
many other realizations.  For example, here is a concrete spec
instantiated from ``curl``:

.. code-block:: console

    curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
        ^openssl@system%gcc@5.3.0 arch=linux-SuSE11-x86_64
        ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64

Spack's core concretization algorithm generates concrete specs by
instantiating packages from its repo, based on a set of "hints",
including user input and the ``packages.yaml`` file.  This algorithm
may be accessed at any time with the ``spack spec`` command.  For
example:

.. code-block:: console

    $ spack spec curl
      curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
          ^openssl@system%gcc@5.3.0 arch=linux-SuSE11-x86_64
          ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64

Every time Spack installs a package, that installation corresponds to
a concrete spec.  Only a vanishingly small fraction of possible
concrete specs will be installed at any one Spack site.

^^^^^^^^^^^^^^^
Consistent Sets
^^^^^^^^^^^^^^^

A set of Spack specs is said to be *consistent* if each package is
only instantiated one way within it --- that is, if two specs in the
set have the same package, then they must also have the same version,
variant, compiler, etc.  For example, the following set is consistent:

.. code-block:: console

    curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
        ^openssl@system%gcc@5.3.0 arch=linux-SuSE11-x86_64
        ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
    zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64

The following set is not consistent:

.. code-block:: console

    curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
        ^openssl@system%gcc@5.3.0 arch=linux-SuSE11-x86_64
        ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
    zlib@1.2.7%gcc@5.3.0 arch=linux-SuSE11-x86_64    

The compatibility of a set of installed packages determines what may
be done with it.  It is always possible to ``spack load`` any set of
installed packages, whether or not they are consistent, and run their
binaries from the command line.  However, a set of installed packages
can only be linked together in one binary if it is consistent.

If the user produces a series of `spack spec` or `spack load`
commands, in general there is no guarantee of consistency between
them.  Spack's concretization procedure guarantees that the results of
any *single* `spack spec` call will be consistent.  Therefore, the
best way to ensure a consistent set of specs is to create a Spack
package with dependencies, and then instantiate that package.  We will
use this technique below.

-----------------
Building Packages
-----------------

Suppose you are tasked with installing a set of software packages on a
system in order to support one application -- both a core application
program, plus software to prepare input and analyze output.  The
required software might be summed up as a series of ``spack install``
commands placed in a script.  If needed, this script can always be run
again in the future.  For example:

.. code-block:: sh

    #!/bin/sh
    spack install modele-utils
    spack install emacs
    spack install ncview
    spack install nco
    spack install modele-control
    spack install py-numpy

In most cases, this script will not correctly install software
according to your specific needs: choices need to be made for
variants, versions and virtual dependency choices may be needed.  It
*is* possible to specify these choices by extending specs on the
command line; however, the same choices must be specified repeatedly.
For example, if you wish to use ``openmpi`` to satisfy the ``mpi``
dependency, then ``^openmpi`` will have to appear on *every* ``spack
install`` line that uses MPI.  It can get repetitve fast.

Custimizing Spack installation options is easier to do in the
``~/.spack/packages.yaml`` file.  In this file, you can specify
preferred versions and variants to use for packages.  For exmaple:

.. code-block:: yaml

    packages:
        python:
            version: [3.5.1]
        modele-utils:
            version: [cmake]

        everytrace:
            version: [develop]
        eigen:
            variants: ~suitesparse
        netcdf:
            variants: +mpi

        all:
            compiler: [gcc@5.3.0]
            providers:
                mpi: [openmpi]
                blas: [openblas]
                lapack: [openblas]


This approach will work as long as you are building packages for just
one application.  

^^^^^^^^^^^^^^^^^^^^^
Multiple Applications
^^^^^^^^^^^^^^^^^^^^^

Suppose instead you're building multiple inconsistent applications.
For example, users want package A to be built with ``openmpi`` and
package B with ``mpich`` --- but still share many other lower-level
dependencies.  In this case, a single ``packages.yaml`` file will not
work.  Plans are to implement *per-project* ``packages.yaml`` files.
In the meantime, one could write shell scripts to switch
``packages.yaml`` between multiple versions as needed, using symlinks.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Combinatorial Sets of Installas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose that you are now tasked with systematically building many
incompatible versions of packages.  For example, you need to build
``petsc`` 9 times for 3 different MPI implementations on 3 different
compilers, in order to support user needs.  In this case, you will
need to either create 9 different ``packages.yaml`` files; or more
likely, create 9 different ``spack install`` command lines with the
correct options in the spec.


----------------
Loading Packages
----------------

Once Spack packages have been built, the next step is to use them.  As
with buiding packages, there are many ways to use them, depending on
the use case.

^^^^^^^^^^^^
Simple Loads
^^^^^^^^^^^^

Suppose that Spack has been used to install a set of command-line
programs, which users now wish to use.  One can in principle put a
number of ``spack load`` commands into ``.bashrc``, for example:

.. code-block::

    spack load modele-utils
    spack load emacs
    spack load ncview
    spack load nco
    spack load modele-control

Although simple load scripts like this are useful in many cases, the
have some drawbacks:

1. The set of modules loaded by them will in general not be
   consistent.  They are a decent way to load commands to be called
   from command shells.  See below for better ways to assemble a
   consistent set of packages for building application programs.

2. The ``spack spec`` and ``spack install`` commands use a
   sophisticated concretization algorithm that chooses the "best"
   among several options, taking into account ``packages.yaml`` file.
   The ``spack load`` and ``spack module loads`` commands, on the
   other thand, are not very smart: if the user-supplied spec matches
   more than one installed package, then ``spack module loads`` will
   fail. This may change in the future.  For now, the workaround is to
   be more specific on any ``spack module loads`` lines that fail.


^^^^^^^^^^^^^^^^^^^
Cached Simple Loads
^^^^^^^^^^^^^^^^^^^

Another problem with using `spack load` is, it is slow; a typical user
environment could take several seconds to load, and would not be
appropriate to put into ``.bashrc`` directly.  It is preferable to use
a series of ``spack module loads`` commands to pre-compute which
modules to load.  These can be put in a script that is run whenever
installed Spack packages change.  For example:

.. code-block:: sh
    #!/bin/sh
    #
    # Generate module load commands in ~/env/spackenv

    cat <<EOF | /bin/sh >$HOME/env/spackenv
    FIND='spack module loads --prefix linux-SuSE11-x86_64/'

    \$FIND modele-utils
    \$FIND emacs
    \$FIND ncview
    \$FIND nco
    \$FIND modele-control
    EOF

The output of this file is written in ``~/env/spackenv``:

.. code-block:: sh

    # binutils@2.25%gcc@5.3.0+gold~krellpatch~libiberty arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/binutils-2.25-gcc-5.3.0-6w5d2t4
    # python@2.7.12%gcc@5.3.0~tk~ucs4 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/python-2.7.12-gcc-5.3.0-2azoju2
    # ncview@2.1.7%gcc@5.3.0 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/ncview-2.1.7-gcc-5.3.0-uw3knq2
    # nco@4.5.5%gcc@5.3.0 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/nco-4.5.5-gcc-5.3.0-7aqmimu
    # modele-control@develop%gcc@5.3.0 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/modele-control-develop-gcc-5.3.0-7rddsij
    # zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/zlib-1.2.8-gcc-5.3.0-fe5onbi
    # curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/curl-7.50.1-gcc-5.3.0-4vlev55
    # hdf5@1.10.0-patch1%gcc@5.3.0+cxx~debug+fortran+mpi+shared~szip~threadsafe arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/hdf5-1.10.0-patch1-gcc-5.3.0-pwnsr4w
    # netcdf@4.4.1%gcc@5.3.0~hdf4+mpi arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/netcdf-4.4.1-gcc-5.3.0-rl5canv
    # netcdf-fortran@4.4.4%gcc@5.3.0 arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/netcdf-fortran-4.4.4-gcc-5.3.0-stdk2xq
    # modele-utils@cmake%gcc@5.3.0+aux+diags+ic arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/modele-utils-cmake-gcc-5.3.0-idyjul5
    # everytrace@develop%gcc@5.3.0+fortran+mpi arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/everytrace-develop-gcc-5.3.0-p5wmb25

Users may now put ``source ~/env/spackenv`` into ``.bashrc``.

.. note ::

    Some module systems put a prefix on the names of modules created
    by Spack.  For example, that prefix is ``linux-SuSE11-x86_64/`` in
    the above case.  If a prefix is not needed, you may omit the
    ``--prefix`` flag from ``spack module loads``.


^^^^^^^^^^^^^^^^^^^^^^^
Transitive Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

In the script above, each ``spack module loads`` command generates a
*single* ``module load`` line.  Transitive dependencies do not usually
need to be load, only modules the user needs in in ``$PATH``.  This is
because Spack builds binaries with RPATH.  Spack's RPATH policy has
some nice features:

 1. Modules for multiple inconsistent applications may be loaded
    simultaneously.  In the above example (Multiple Applications),
    package A and package B can coexist together in the user's $PATH,
    even though they use different MPIs.

 2. RPATH eliminates a whole class of strange errors that can happen
    in non-RPATH binaries when the wrong ``LD_LIBRARY_PATH`` is
    loaded.

 3. Recursive module systems such as LMod are not necessary.

 4. Modules are not needed at all to execute binaries.  If a path to a
    binary is known, it may be executed.  For example, the path for a
    Spack-built compiler can be given to an IDE without requiring the
    IDE to load that compiler's module.

Unfortunately, Spacks' RPATH support does not work in all case.  For example:

 1. Software comes in many forms --- not just compiled ELF binaries,
    but also as interpreted code in Python, R, JVM bytecode, etc.
    Those systems almost universally use an environment variable
    analogous to ``LD_LIBRARY_PATH`` to dynamically load libraries.

 2. Although Spack generally builds binaries with RPATH, it does not
    currently do so for compiled Python extensions (for example,
    ``py-numpy``).  Any libraries that these extensions depend on
    (``openblas`` in this case, for example) must be specified in the
    ``LD_LIBRARY_PATH``.`

 3. In some cases, Spack-generated binaries end up without a
    functional RPATH for no discernable reason.

In cases where RPATH support doesn't make things "just work," it can
be necessary to load a module's dependencies as well as the module
itself.  This is done by adding the ``--dependencies`` flag to the
``spack module loads`` command.  For example, the following line,
added to the script above, would be used to load Numpy, along with
core Python, Setup Tools and a number of other packages:

.. code-block:: sh
    \$FIND --dependencies py-numpy

^^^^^^^^^^^^^^^^^^
Extension Packages
^^^^^^^^^^^^^^^^^^

:ref:`packaging_extensions` may be used as an alternative to loading
Python packages directly.  If extensions are activated, then ``spack
load python`` will also load all the extensions activated for the
given ``python``.  However, Spack extensions have two potential
drawbacks:

1. Activated packages that involve compiled C extensions may still
   need their dependencies to be loaded manually.  For example,
   ``spack load openblas`` might be required to make ``py-numpy``
   work.

2. Extensions "break" a core feature of Spack, which is that multiple
   versions of a package can co-exist side-by-side.  For example,
   suppose you wish to run a Python in two different environments but
   the same basic Python --- one with ``py-numpy@1.7`` and one with
   ``py-numpy@1.8``.  Spack extensions will not support this potential
   debugging use case.


^^^^^^^^^^^^^^^^
Filesystem Views
^^^^^^^^^^^^^^^^

.. Maybe this is not the right location for this documentation.

The Spack installation area allows for many package installation trees
to coexist and gives the user choices as to what versions and variants
of packages to use.  To use them, the user must rely on a way to
aggregate a subset of those packages.  The section on Environment
Modules gives one good way to do that which relies on setting various
environment variables.  An alternative way to aggregate is through
**filesystem views**.

A filesystem view is a single directory tree which is the union of the
directory hierarchies of the individual package installation trees
that have been included.  The files of the view's installed packages
are brought into the view by symbolic or hard links back to their
location in the original Spack installation area.  As the view is
formed, any clashes due to a file having the exact same path in its
package installation tree are handled in a first-come-first-served
basis and a warning is printed.  Packages and their dependencies can
be both added and removed.  During removal, empty directories will be
purged.  These operations can be limited to pertain to just the
packages listed by the user or to exclude specific dependencies and
they allow for software installed outside of Spack to coexist inside
the filesystem view tree.

By its nature, a filesystem view represents a particular choice of one
set of packages among all the versions and variants that are available
in the Spack installation area.  It is thus equivalent to the
directory hiearchy that might exist under ``/usr/local``.  While this
limits a view to including only one version/variant of any package, it
provides the benefits of having a simpler and traditional layout which
may be used without any particular knowledge that its packages were
built by Spack.

Views can be used for a variety of purposes including:

* A central installation in a traditional layout, eg ``/usr/local`` maintained over time by the sysadmin.
* A self-contained installation area which may for the basis of a top-level atomic versioning scheme, eg ``/opt/pro`` vs ``/opt/dev``.
* Providing an atomic and monolithic binary distribution, eg for delivery as a single tarball.
* Producing ephemeral testing or developing environments.

^^^^^^^^^^^^^^^^^^^^^^
Using Filesystem Views
^^^^^^^^^^^^^^^^^^^^^^

A filesystem view is created and packages are linked in by the ``spack
view`` command's ``symlink`` and ``hardlink`` sub-commands.  The
``spack view remove`` command can be used to unlink some or all of the
filesystem view.

The following example creates a filesystem view based
on an installed ``cmake`` package and then removes from the view the
files in the ``cmake`` package while retaining its dependencies.

.. code-block:: console

   $ spack view --verbose symlink myview cmake@3.5.2
   ==> Linking package: "ncurses"
   ==> Linking package: "zlib"
   ==> Linking package: "openssl"
   ==> Linking package: "cmake"

   $ ls myview/
   bin  doc  etc  include  lib  share

   $ ls myview/bin/
   captoinfo  clear  cpack     ctest    infotocap        openssl  tabs  toe   tset
   ccmake     cmake  c_rehash  infocmp  ncurses6-config  reset    tic   tput

   $ spack view --verbose --dependencies false rm myview cmake@3.5.2
   ==> Removing package: "cmake"

   $ ls myview/bin/
   captoinfo  c_rehash  infotocap        openssl  tabs  toe   tset
   clear      infocmp   ncurses6-config  reset    tic   tput

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Limitations of Filesystem Views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes some limitations that should be considered in
using filesystems views.

Filesystem views are merely organizational.  The binary executable
programs, shared libraries and other build products found in a view
are mere links into the "real" Spack installation area.  If a view is
built with symbolic links it requires the Spack-installed package to
be kept in place.  Building a view with hardlinks removes this
requirement but any internal paths (eg, rpath or ``#!`` interpreter
specifications) will still require the Spack-installed package files
to be in place.

.. FIXME: reference the relocation work of Hegner and Gartung.

As described above, when a view is built only a single instance of a
file may exist in the unified filesystem tree.  If more than one
package provides a file at the same path (relative to its own root)
then it is the first package added to the view that "wins".  A warning
is printed and it is up to the user to determine if the conflict
matters.

It is up to the user to assure a consistent view is produced.  In
particular if the user excludes packages, limits the following of
dependencies or removes packages the view may become inconsistent.  In
particular, if two packages require the same sub-tree of dependencies,
removing one package (recursively) will remove its dependencies and
leave the other package broken.




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








^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Build System Configuration Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imagine a developer creating a CMake or Autotools-based project in a local
directory, which depends on libraries A-Z.  Once Spack has installed
those dependencies, one would like to run ``cmake`` with appropriate
command line and environment so CMake can find them.  The ``spack
setup`` command does this conveniently, producing a CMake
configuration that is essentially the same as how Spack *would have*
configured the project.  This can be demonstrated with a usage
example:

.. code-block:: console

   $ cd myproject
   $ spack setup myproject@local
   $ mkdir build; cd build
   $ ../spconfig.py ..
   $ make
   $ make install

Notes:

* Spack must have ``myproject/package.py`` in its repository for
  this to work.
* ``spack setup`` produces the executable script ``spconfig.py`` in
  the local directory, and also creates the module file for the
  package.  ``spconfig.py`` is normally run from the user's
  out-of-source build directory.
* The version number given to ``spack setup`` is arbitrary, just
  like ``spack diy``.  ``myproject/package.py`` does not need to
  have any valid downloadable versions listed (typical when a
  project is new).
* spconfig.py produces a CMake configuration that *does not* use the
  Spack wrappers.  Any resulting binaries *will not* use RPATH,
  unless the user has enabled it.  This is recommended for
  development purposes, not production.
* ``spconfig.py`` is human readable, and can serve as a developer
  reference of what dependencies are being used.
* ``make install`` installs the package into the Spack repository,
  where it may be used by other Spack packages.
* CMake-generated makefiles re-run CMake in some circumstances.  Use
  of ``spconfig.py`` breaks this behavior, requiring the developer
  to manually re-run ``spconfig.py`` when a ``CMakeLists.txt`` file
  has changed.

^^^^^^^^^^^^
CMakePackage
^^^^^^^^^^^^

In order to enable ``spack setup`` functionality, the author of
``myproject/package.py`` must subclass from ``CMakePackage`` instead
of the standard ``Package`` superclass.  Because CMake is
standardized, the packager does not need to tell Spack how to run
``cmake; make; make install``.  Instead the packager only needs to
create (optional) methods ``configure_args()`` and ``configure_env()``, which
provide the arguments (as a list) and extra environment variables (as
a dict) to provide to the ``cmake`` command.  Usually, these will
translate variant flags into CMake definitions.  For example:

.. code-block:: python

   def configure_args(self):
       spec = self.spec
       return [
           '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
           '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
           '-DBUILD_GRIDGEN=%s' % ('YES' if '+gridgen' in spec else 'NO'),
           '-DBUILD_COUPLER=%s' % ('YES' if '+coupler' in spec else 'NO'),
           '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO')
       ]

If needed, a packager may also override methods defined in
``StagedPackage`` (see below).

^^^^^^^^^^^^^
StagedPackage
^^^^^^^^^^^^^

``CMakePackage`` is implemented by subclassing the ``StagedPackage``
superclass, which breaks down the standard ``Package.install()``
method into several sub-stages: ``setup``, ``configure``, ``build``
and ``install``.  Details:

* Instead of implementing the standard ``install()`` method, package
  authors implement the methods for the sub-stages
  ``install_setup()``, ``install_configure()``,
  ``install_build()``, and ``install_install()``.

* The ``spack install`` command runs the sub-stages ``configure``,
  ``build`` and ``install`` in order.  (The ``setup`` stage is
  not run by default; see below).
* The ``spack setup`` command runs the sub-stages ``setup``
  and a dummy install (to create the module file).
* The sub-stage install methods take no arguments (other than
  ``self``).  The arguments ``spec`` and ``prefix`` to the standard
  ``install()`` method may be accessed via ``self.spec`` and
  ``self.prefix``.

^^^^^^^^^^^^^
GNU Autotools
^^^^^^^^^^^^^

The ``setup`` functionality is currently only available for
CMake-based packages.  Extending this functionality to GNU
Autotools-based packages would be easy (and should be done by a
developer who actively uses Autotools).  Packages that use
non-standard build systems can gain ``setup`` functionality by
subclassing ``StagedPackage`` directly.

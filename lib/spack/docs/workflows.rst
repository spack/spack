=========
Workflows
=========

The process of using Spack involves building packages, running
binaries from those packages, and developing software that depends on
those packages.  For example, one might use Spack to build the
``netcdf`` package, use ``spack load`` to run the ``ncdump`` binary, and
finally, write a small C program to read/write a particular NetCDF file.

Spack supports a variety of workflows to suit a variety of situations
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

.. command-output:: spack spec curl

Spack's core concretization algorithm generates concrete specs by
instantiating packages from its repo, based on a set of "hints",
including user input and the ``packages.yaml`` file.  This algorithm
may be accessed at any time with the ``spack spec`` command.

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
       ^openssl@1.0.2k%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
   zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64

The following set is not consistent:

.. code-block:: console

   curl@7.50.1%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^openssl@1.0.2k%gcc@5.3.0 arch=linux-SuSE11-x86_64
       ^zlib@1.2.8%gcc@5.3.0 arch=linux-SuSE11-x86_64
   zlib@1.2.7%gcc@5.3.0 arch=linux-SuSE11-x86_64

The compatibility of a set of installed packages determines what may
be done with it.  It is always possible to ``spack load`` any set of
installed packages, whether or not they are consistent, and run their
binaries from the command line.  However, a set of installed packages
can only be linked together in one binary if it is consistent.

If the user produces a series of ``spack spec`` or ``spack load``
commands, in general there is no guarantee of consistency between
them.  Spack's concretization procedure guarantees that the results of
any *single* ``spack spec`` call will be consistent.  Therefore, the
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
install`` line that uses MPI.  It can get repetitive fast.

Customizing Spack installation options is easier to do in the
``~/.spack/packages.yaml`` file.  In this file, you can specify
preferred versions and variants to use for packages.  For example:

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
Combinatorial Sets of Installs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose that you are now tasked with systematically building many
incompatible versions of packages.  For example, you need to build
``petsc`` 9 times for 3 different MPI implementations on 3 different
compilers, in order to support user needs.  In this case, you will
need to either create 9 different ``packages.yaml`` files; or more
likely, create 9 different ``spack install`` command lines with the
correct options in the spec.  Here is a real-life example of this kind
of usage:

.. code-block:: sh

   #!/bin/sh

   compilers=(
       %gcc
       %intel
       %pgi
   )

   mpis=(
       openmpi+psm~verbs
       openmpi~psm+verbs
       mvapich2+psm~mrail
       mvapich2~psm+mrail
       mpich+verbs
   )

   for compiler in "${compilers[@]}"
   do
       # Serial installs
       spack install szip           $compiler
       spack install hdf            $compiler
       spack install hdf5           $compiler
       spack install netcdf         $compiler
       spack install netcdf-fortran $compiler
       spack install ncview         $compiler

       # Parallel installs
       for mpi in "${mpis[@]}"
       do
           spack install $mpi            $compiler
           spack install hdf5~cxx+mpi    $compiler ^$mpi
           spack install parallel-netcdf $compiler ^$mpi
       done
   done

------------------------------
Running Binaries from Packages
------------------------------

Once Spack packages have been built, the next step is to use them.  As
with building packages, there are many ways to use them, depending on
the use case.

^^^^^^^^^^^^
Find and Run
^^^^^^^^^^^^

The simplest way to run a Spack binary is to find it and run it!
In many cases, nothing more is needed because Spack builds binaries
with RPATHs.  Spack installation directories may be found with ``spack
location --install-dir`` commands.  For example:

.. code-block:: console

   $ spack location --install-dir cmake
   ~/spack/opt/spack/linux-SuSE11-x86_64/gcc-5.3.0/cmake-3.6.0-7cxrynb6esss6jognj23ak55fgxkwtx7

This gives the root of the Spack package; relevant binaries may be
found within it.  For example:

.. code-block:: console

   $ CMAKE=`spack location --install-dir cmake`/bin/cmake


Standard UNIX tools can find binaries as well.  For example:

.. code-block:: console

   $ find ~/spack/opt -name cmake | grep bin
   ~/spack/opt/spack/linux-SuSE11-x86_64/gcc-5.3.0/cmake-3.6.0-7cxrynb6esss6jognj23ak55fgxkwtx7/bin/cmake

These methods are suitable, for example, for setting up build
processes or GUIs that need to know the location of particular tools.
However, other more powerful methods are generally preferred for user
environments.


^^^^^^^^^^^^^^^^^^^^^^^
Spack-Generated Modules
^^^^^^^^^^^^^^^^^^^^^^^

Suppose that Spack has been used to install a set of command-line
programs, which users now wish to use.  One can in principle put a
number of ``spack load`` commands into ``.bashrc``, for example, to
load a set of Spack-generated modules:

.. code-block:: sh

   spack load modele-utils
   spack load emacs
   spack load ncview
   spack load nco
   spack load modele-control

Although simple load scripts like this are useful in many cases, they
have some drawbacks:

1. The set of modules loaded by them will in general not be
   consistent.  They are a decent way to load commands to be called
   from command shells.  See below for better ways to assemble a
   consistent set of packages for building application programs.

2. The ``spack spec`` and ``spack install`` commands use a
   sophisticated concretization algorithm that chooses the "best"
   among several options, taking into account ``packages.yaml`` file.
   The ``spack load`` and ``spack module loads`` commands, on the
   other hand, are not very smart: if the user-supplied spec matches
   more than one installed package, then ``spack module loads`` will
   fail. This may change in the future.  For now, the workaround is to
   be more specific on any ``spack module loads`` lines that fail.


""""""""""""""""""""""
Generated Load Scripts
""""""""""""""""""""""

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


"""""""""""""""""""""""
Transitive Dependencies
"""""""""""""""""""""""

In the script above, each ``spack module loads`` command generates a
*single* ``module load`` line.  Transitive dependencies do not usually
need to be loaded, only modules the user needs in in ``$PATH``.  This is
because Spack builds binaries with RPATH.  Spack's RPATH policy has
some nice features:

#. Modules for multiple inconsistent applications may be loaded
   simultaneously.  In the above example (Multiple Applications),
   package A and package B can coexist together in the user's $PATH,
   even though they use different MPIs.

#. RPATH eliminates a whole class of strange errors that can happen
   in non-RPATH binaries when the wrong ``LD_LIBRARY_PATH`` is
   loaded.

#. Recursive module systems such as LMod are not necessary.

#. Modules are not needed at all to execute binaries.  If a path to a
   binary is known, it may be executed.  For example, the path for a
   Spack-built compiler can be given to an IDE without requiring the
   IDE to load that compiler's module.

Unfortunately, Spack's RPATH support does not work in all case.  For example:

#. Software comes in many forms --- not just compiled ELF binaries,
   but also as interpreted code in Python, R, JVM bytecode, etc.
   Those systems almost universally use an environment variable
   analogous to ``LD_LIBRARY_PATH`` to dynamically load libraries.

#. Although Spack generally builds binaries with RPATH, it does not
   currently do so for compiled Python extensions (for example,
   ``py-numpy``).  Any libraries that these extensions depend on
   (``blas`` in this case, for example) must be specified in the
   ``LD_LIBRARY_PATH``.`

#. In some cases, Spack-generated binaries end up without a
   functional RPATH for no discernible reason.

In cases where RPATH support doesn't make things "just work," it can
be necessary to load a module's dependencies as well as the module
itself.  This is done by adding the ``--dependencies`` flag to the
``spack module loads`` command.  For example, the following line,
added to the script above, would be used to load SciPy, along with
Numpy, core Python, BLAS/LAPACK and anything else needed:

.. code-block:: sh

   spack module loads --dependencies py-scipy

^^^^^^^^^^^^^^^^^^
Extension Packages
^^^^^^^^^^^^^^^^^^

:ref:`packaging_extensions` may be used as an alternative to loading
Python (and similar systems) packages directly.  If extensions are
activated, then ``spack load python`` will also load all the
extensions activated for the given ``python``.  This reduces the need
for users to load a large number of modules.

However, Spack extensions have two potential drawbacks:

#. Activated packages that involve compiled C extensions may still
   need their dependencies to be loaded manually.  For example,
   ``spack load openblas`` might be required to make ``py-numpy``
   work.

#. Extensions "break" a core feature of Spack, which is that multiple
   versions of a package can co-exist side-by-side.  For example,
   suppose you wish to run a Python package in two different
   environments but the same basic Python --- one with
   ``py-numpy@1.7`` and one with ``py-numpy@1.8``.  Spack extensions
   will not support this potential debugging use case.


^^^^^^^^^^^^^^
Dummy Packages
^^^^^^^^^^^^^^

As an alternative to a series of ``module load`` commands, one might
consider dummy packages as a way to create a *consistent* set of
packages that may be loaded as one unit.  The idea here is pretty
simple:

#. Create a package (say, ``mydummy``) with no URL and no
   ``install()`` method, just dependencies.

#. Run ``spack install mydummy`` to install.

An advantage of this method is the set of packages produced will be
consistent.  This means that you can reliably build software against
it.  A disadvantage is the set of packages will be consistent; this
means you cannot load up two applications this way if they are not
consistent with each other.

^^^^^^^^^^^^^^^^
Filesystem Views
^^^^^^^^^^^^^^^^

Filesystem views offer an alternative to environment modules, another
way to assemble packages in a useful way and load them into a user's
environment.

A filesystem view is a single directory tree that is the union of the
directory hierarchies of a number of installed packages; it is similar
to the directory hiearchy that might exist under ``/usr/local``.  The
files of the view's installed packages are brought into the view by
symbolic or hard links, referencing the original Spack installation.

When software is built and installed, absolute paths are frequently
"baked into" the software, making it non-relocatable.  This happens
not just in RPATHs, but also in shebangs, configuration files, and
assorted other locations.

Therefore, programs run out of a Spack view will typically still look
in the original Spack-installed location for shared libraries and
other resources.  This behavior is not easily changed; in general,
there is no way to know where absolute paths might be written into an
installed package, and how to relocate it.  Therefore, the original
Spack tree must be kept in place for a filesystem view to work, even
if the view is built with hardlinks.

.. FIXME: reference the relocation work of Hegner and Gartung (PR #1013)


""""""""""""""""""""""
Using Filesystem Views
""""""""""""""""""""""

A filesystem view is created, and packages are linked in, by the ``spack
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

.. note::

    If the set of packages being included in a view is inconsistent,
    then it is possible that two packages will provide the same file.  Any
    conflicts of this type are handled on a first-come-first-served basis,
    and a warning is printed.

.. note::

    When packages are removed from a view, empty directories are
    purged.

""""""""""""""""""
Fine-Grain Control
""""""""""""""""""

The ``--exclude`` and ``--dependencies`` option flags allow for
fine-grained control over which packages and dependencies do or not
get included in a view.  For example, suppose you are developing the
``appsy`` package.  You wish to build against a view of all ``appsy``
dependencies, but not ``appsy`` itself:

.. code-block:: console

   $ spack view symlink --dependencies yes --exclude appsy appsy

Alternately, you wish to create a view whose purpose is to provide
binary executables to end users.  You only need to include
applications they might want, and not those applications'
dependencies.  In this case, you might use:

.. code-block:: console

   $ spack view symlink --dependencies no cmake


"""""""""""""""""""""""
Hybrid Filesystem Views
"""""""""""""""""""""""

Although filesystem views are usually created by Spack, users are free
to add to them by other means.  For example, imagine a filesystem
view, created by Spack, that looks something like:

.. code-block:: console

   /path/to/MYVIEW/bin/programA -> /path/to/spack/.../bin/programA
   /path/to/MYVIEW/lib/libA.so -> /path/to/spack/.../lib/libA.so

Now, the user may add to this view by non-Spack means; for example, by
running a classic install script.  For example:

.. code-block:: console

   $ tar -xf B.tar.gz
   $ cd B/
   $ ./configure --prefix=/path/to/MYVIEW \
               --with-A=/path/to/MYVIEW
   $ make && make install

The result is a hybrid view:

.. code-block:: console

   /path/to/MYVIEW/bin/programA -> /path/to/spack/.../bin/programA
   /path/to/MYVIEW/bin/programB
   /path/to/MYVIEW/lib/libA.so -> /path/to/spack/.../lib/libA.so
   /path/to/MYVIEW/lib/libB.so

In this case, real files coexist, interleaved with the "view"
symlinks.  At any time one can delete ``/path/to/MYVIEW`` or use
``spack view`` to manage it surgically.  None of this will affect the
real Spack install area.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Discussion: Running Binaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modules, extension packages and filesystem views are all ways to
assemble sets of Spack packages into a useful environment.  They are
all semantically similar, in that conflicting installed packages
cannot simultaneously be loaded, activated or included in a view.

With all of these approaches, there is no guarantee that the
environment created will be consistent.  It is possible, for example,
to simultaneously load application A that uses OpenMPI and application
B that uses MPICH.  Both applications will run just fine in this
inconsistent environment because they rely on RPATHs, not the
environment, to find their dependencies.

In general, environments set up using modules vs. views will work
similarly.  Both can be used to set up ephemeral or long-lived
testing/development environments.  Operational differences between the
two approaches can make one or the other preferable in certain
environments:

* Filesystem views do not require environment module infrastructure.
  Although Spack can install ``environment-modules``, users might be
  hostile to its use.  Filesystem views offer a good solution for
  sysadmins serving users who just "want all the stuff I need in one
  place" and don't want to hear about Spack.

* Although modern build systems will find dependencies wherever they
  might be, some applications with hand-built make files expect their
  dependencies to be in one place.  One common problem is makefiles
  that assume that ``netcdf`` and ``netcdf-fortran`` are installed in
  the same tree.  Or, one might use an IDE that requires tedious
  configuration of dependency paths; and it's easier to automate that
  administration in a view-building script than in the IDE itself.
  For all these cases, a view will be preferable to other ways to
  assemble an environment.

* On systems with I-node quotas, modules might be preferable to views
  and extension packages.

* Views and activated extensions maintain state that is semantically
  equivalent to the information in a ``spack module loads`` script.
  Administrators might find things easier to maintain without the
  added "heavyweight" state of a view.

------------------------------
Developing Software with Spack
------------------------------

For any project, one needs to assemble an
environment of that application's dependencies.  You might consider
loading a series of modules or creating a filesystem view.  This
approach, while obvious, has some serious drawbacks:

1. There is no guarantee that an environment created this way will be
   consistent.  Your application could end up with dependency A
   expecting one version of MPI, and dependency B expecting another.
   The linker will not be happy...

2. Suppose you need to debug a package deep within your software DAG.
   If you build that package with a manual environment, then it
   becomes difficult to have Spack auto-build things that depend on
   it.  That could be a serious problem, depending on how deep the
   package in question is in your dependency DAG.

3. At its core, Spack is a sophisticated concretization algorithm that
   matches up packages with appropriate dependencies and creates a
   *consistent* environment for the package it's building.  Writing a
   list of ``spack load`` commands for your dependencies is at least
   as hard as writing the same list of ``depends_on()`` declarations
   in a Spack package.  But it makes no use of Spack concretization
   and is more error-prone.

4. Spack provides an automated, systematic way not just to find a
   packages's dependencies --- but also to build other packages on
   top.  Any Spack package can become a dependency for another Spack
   package, offering a powerful vision of software re-use.  If you
   build your package A outside of Spack, then your ability to use it
   as a building block for other packages in an automated way is
   diminished: other packages depending on package A will not
   be able to use Spack to fulfill that dependency.

5. If you are reading this manual, you probably love Spack.  You're
   probably going to write a Spack package for your software so
   prospective users can install it with the least amount of pain.
   Why should you go to additional work to find dependencies in your
   development environment?  Shouldn't Spack be able to help you build
   your software based on the package you've already written?

In this section, we show how Spack can be used in the software
development process to greatest effect, and how development packages
can be seamlessly integrated into the Spack ecosystem.  We will show
how this process works by example, assuming the software you are
creating is called ``mylib``.

^^^^^^^^^^^^^^^^^^^^^
Write the CMake Build
^^^^^^^^^^^^^^^^^^^^^

For now, the techniques in this section only work for CMake-based
projects, although they could be easily extended to other build
systems in the future.  We will therefore assume you are using CMake
to build your project.

The ``CMakeLists.txt`` file should be written as normal.  A few caveats:

1. Your project should produce binaries with RPATHs.  This will ensure
   that they work the same whether built manually or automatically by
   Spack.  For example:

.. code-block:: cmake

   # enable @rpath in the install name for any shared library being built
   # note: it is planned that a future version of CMake will enable this by default
   set(CMAKE_MACOSX_RPATH 1)

   # Always use full RPATH
   # http://www.cmake.org/Wiki/CMake_RPATH_handling
   # http://www.kitware.com/blog/home/post/510

   # use, i.e. don't skip the full RPATH for the build tree
   SET(CMAKE_SKIP_BUILD_RPATH  FALSE)

   # when building, don't use the install RPATH already
   # (but later on when installing)
   SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

   # add the automatically determined parts of the RPATH
   # which point to directories outside the build tree to the install RPATH
   SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

   # the RPATH to be used when installing, but only if it's not a system directory
   LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
   IF("${isSystemDir}" STREQUAL "-1")
      SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
   ENDIF("${isSystemDir}" STREQUAL "-1")


2. Spack provides a CMake variable called
   ``SPACK_TRANSITIVE_INCLUDE_PATH``, which contains the ``include/``
   directory for all of your project's transitive dependencies.  It
   can be useful if your project ``#include``s files from package B,
   which ``#include`` files from package C, but your project only
   lists project B as a dependency.  This works in traditional
   single-tree build environments, in which B and C's include files
   live in the same place.  In order to make it work with Spack as
   well, you must add the following to ``CMakeLists.txt``.  It will
   have no effect when building without Spack:

   .. code-block:: cmake

      # Include all the transitive dependencies determined by Spack.
      # If we're not running with Spack, this does nothing...
      include_directories($ENV{SPACK_TRANSITIVE_INCLUDE_PATH})

   .. note::

      Note that this feature is controversial and could break with
      future versions of GNU ld.  The best practice is to make sure
      anything you ``#include`` is listed as a dependency in your
      CMakeLists.txt (and Spack package).

.. _write-the-spack-package:

^^^^^^^^^^^^^^^^^^^^^^^
Write the Spack Package
^^^^^^^^^^^^^^^^^^^^^^^

The Spack package also needs to be written, in tandem with setting up
the build (for example, CMake).  The most important part of this task
is declaring dependencies.  Here is an example of the Spack package
for the ``mylib`` package (ellipses for brevity):

.. code-block:: python

   class Mylib(CMakePackage):
       """Misc. reusable utilities used by Myapp."""

       homepage = "https://github.com/citibeth/mylib"
       url = "https://github.com/citibeth/mylib/tarball/123"

       version('0.1.2', '3a6acd70085e25f81b63a7e96c504ef9')
       version('develop', git='https://github.com/citibeth/mylib.git',
           branch='develop')

       variant('everytrace', default=False,
               description='Report errors through Everytrace')
       ...

       extends('python')

       depends_on('eigen')
       depends_on('everytrace', when='+everytrace')
       depends_on('proj', when='+proj')
       ...
       depends_on('cmake', type='build')
       depends_on('doxygen', type='build')

       def configure_args(self):
           spec = self.spec
           return [
               '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
               '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
               ...
               '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
               '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO')]

This is a standard Spack package that can be used to install
``mylib`` in a production environment.  The list of dependencies in
the Spack package will generally be a repeat of the list of CMake
dependencies.  This package also has some features that allow it to be
used for development:

1. It subclasses ``CMakePackage`` instead of ``Package``.  This
   eliminates the need to write an ``install()`` method, which is
   defined in the superclass.  Instead, one just needs to write the
   ``configure_args()`` method.  That method should return the
   arguments needed for the ``cmake`` command (beyond the standard
   CMake arguments, which Spack will include already).  These
   arguments are typically used to turn features on/off in the build.

2. It specifies a non-checksummed version ``develop``.  Running
   ``spack install mylib@develop`` the ``@develop`` version will
   install the latest version off the develop branch.  This method of
   download is useful for the developer of a project while it is in
   active development; however, it should only be used by developers
   who control and trust the repository in question!

3. The ``url``, ``url_for_version()`` and ``homepage`` attributes are
   not used in development.  Don't worry if you don't have any, or if
   they are behind a firewall.

^^^^^^^^^^^^^^^^
Build with Spack
^^^^^^^^^^^^^^^^

Now that you have a Spack package, you can use Spack to find its
dependencies automatically.  For example:

.. code-block:: console

   $ cd mylib
   $ spack setup mylib@local

The result will be a file ``spconfig.py`` in the top-level
``mylib/`` directory.  It is a short script that calls CMake with the
dependencies and options determined by Spack --- similar to what
happens in ``spack install``, but now written out in script form.
From a developer's point of view, you can think of ``spconfig.py`` as
a stand-in for the ``cmake`` command.

.. note::

   You can invent any "version" you like for the ``spack setup``
   command.

.. note::

   Although ``spack setup`` does not build your package, it does
   create and install a module file, and mark in the database that
   your package has been installed.  This can lead to errors, of
   course, if you don't subsequently install your package.
   Also... you will need to ``spack uninstall`` before you run
   ``spack setup`` again.


You can now build your project as usual with CMake:

.. code-block:: console

   $ mkdir build; cd build
   $ ../spconfig.py ..   # Instead of cmake ..
   $ make
   $ make install

Once your ``make install`` command is complete, your package will be
installed, just as if you'd run ``spack install``.  Except you can now
edit, re-build and re-install as often as needed, without checking
into Git or downloading tarballs.

.. note::

   The build you get this way will be *almost* the same as the build
   from ``spack install``.  The only difference is, you will not be
   using Spack's compiler wrappers.  This difference has not caused
   problems in our experience, as long as your project sets
   RPATHs as shown above.  You DO use RPATHs, right?

^^^^^^^^^^^^^^^^^^^^
Build Other Software
^^^^^^^^^^^^^^^^^^^^

Now that you've built ``mylib`` with Spack, you might want to build
another package that depends on it --- for example, ``myapp``.  This
is accomplished easily enough:

.. code-block:: console

   $ spack install myapp ^mylib@local

Note that auto-built software has now been installed *on top of*
manually-built software, without breaking Spack's "web."  This
property is useful if you need to debug a package deep in the
dependency hierarchy of your application.  It is a *big* advantage of
using ``spack setup`` to build your package's environment.

If you feel your software is stable, you might wish to install it with
``spack install`` and skip the source directory.  You can just use,
for example:

.. code-block:: console

   $ spack install mylib@develop

.. _release-your-software:

^^^^^^^^^^^^^^^^^^^^^
Release Your Software
^^^^^^^^^^^^^^^^^^^^^

You are now ready to release your software as a tarball with a
numbered version, and a Spack package that can build it.  If you're
hosted on GitHub, this process will be a bit easier.

#. Put tag(s) on the version(s) in your GitHub repo you want to be
   release versions.  For example, a tag ``v0.1.0`` for version 0.1.0.

#. Set the ``url`` in your ``package.py`` to download a tarball for
   the appropriate version.  GitHub will give you a tarball for any
   commit in the repo, if you tickle it the right way.  For example:

   .. code-block:: python

      url = 'https://github.com/citibeth/mylib/tarball/v0.1.2'

#. Use Spack to determine your version's hash, and cut'n'paste it into
   your ``package.py``:

   .. code-block:: console

      $ spack checksum mylib 0.1.2
      ==> Found 1 versions of mylib
        0.1.2     https://github.com/citibeth/mylib/tarball/v0.1.2

      How many would you like to checksum? (default is 5, q to abort)
      ==> Downloading...
      ==> Trying to fetch from https://github.com/citibeth/mylib/tarball/v0.1.2
      ######################################################################## 100.0%
      ==> Checksummed new versions of mylib:
            version('0.1.2', '3a6acd70085e25f81b63a7e96c504ef9')

#. You should now be able to install released version 0.1.2 of your package with:

   .. code-block:: console

      $ spack install mylib@0.1.2

#. There is no need to remove the `develop` version from your package.
   Spack concretization will always prefer numbered version to
   non-numeric versions.  Users will only get it if they ask for it.

^^^^^^^^^^^^^^^^^^^^^^^^
Distribute Your Software
^^^^^^^^^^^^^^^^^^^^^^^^

Once you've released your software, other people will want to build
it; and you will need to tell them how.  In the past, that has meant a
few paragraphs of prose explaining which dependencies to install.  But
now you use Spack, and those instructions are written in executable
Python code.  But your software has many dependencies, and you know
Spack is the best way to install it:

#. First, you will want to fork Spack's ``develop`` branch.  Your aim
   is to provide a stable version of Spack that you KNOW will install
   your software.  If you make changes to Spack in the process, you
   will want to submit pull requests to Spack core.

#. Add your software's ``package.py`` to that fork.  You should submit
   a pull request for this as well, unless you don't want the public
   to know about your software.

#. Prepare instructions that read approximately as follows:

   #. Download Spack from your forked repo.

   #. Install Spack; see :ref:`getting_started`.

   #. Set up an appropriate ``packages.yaml`` file.  You should tell
      your users to include in this file whatever versions/variants
      are needed to make your software work correctly (assuming those
      are not already in your ``packages.yaml``).

   #. Run ``spack install mylib``.

   #. Run this script to generate the ``module load`` commands or
      filesystem view needed to use this software.

#. Be aware that your users might encounter unexpected bootstrapping
   issues on their machines, especially if they are running on older
   systems.  The :ref:`getting_started` section should cover this, but
   there could always be issues.

^^^^^^^^^^^^^^^^^^^
Other Build Systems
^^^^^^^^^^^^^^^^^^^

``spack setup`` currently only supports CMake-based builds, in
packages that subclass ``CMakePackage``.  The intent is that this
mechanism should support a wider range of build systems; for example,
GNU Autotools.  Someone well-versed in Autotools is needed to develop
this patch and test it out.

Python Distutils is another popular build system that should get
``spack setup`` support.  For non-compiled languages like Python,
``spack diy`` may be used.  Even better is to put the source directory
directly in the user's ``PYTHONPATH``.  Then, edits in source files
are immediately available to run without any install process at all!

^^^^^^^^^^
Conclusion
^^^^^^^^^^

The ``spack setup`` development workflow provides better automation,
flexibility and safety than workflows relying on environment modules
or filesystem views.  However, it has some drawbacks:

#. It currently works only with projects that use the CMake build
   system.  Support for other build systems is not hard to build, but
   will require a small amount of effort for each build system to be
   supported.  It might not work well with some IDEs.

#. It only works with packages that sub-class ``StagedPackage``.
   Currently, most Spack packages do not.  Converting them is not
   hard; but must be done on a package-by-package basis.

#. It requires that users are comfortable with Spack, as they
   integrate Spack explicitly in their workflow.  Not all users are
   willing to do this.

------------------
Upstream Bug Fixes
------------------

It is not uncommon to discover a bug in an upstream project while
trying to build with Spack.  Typically, the bug is in a package that
serves a dependency to something else.  This section describes
procedure to work around and ultimately resolve these bugs, while not
delaying the Spack user's main goal.

^^^^^^^^^^^^^^^^^
Buggy New Version
^^^^^^^^^^^^^^^^^

Sometimes, the old version of a package works fine, but a new version
is buggy.  For example, it was once found that `Adios did not build
with hdf5@1.10 <https://github.com/LLNL/spack/issues/1683>`_.  If the
old version of ``hdf5`` will work with ``adios``, the suggested
procedure is:

#. Revert ``adios`` to the old version of ``hdf5``.  Put in its
   ``adios/package.py``:

   .. code-block:: python

      # Adios does not build with HDF5 1.10
      # See: https://github.com/LLNL/spack/issues/1683
      depends_on('hdf5@:1.9')

#. Determine whether the problem is with ``hdf5`` or ``adios``, and
   report the problem to the appropriate upstream project.  In this
   case, the problem was with ``adios``.

#. Once a new version of ``adios`` comes out with the bugfix, modify
   ``adios/package.py`` to reflect it:

   .. code-block:: python

      # Adios up to v1.10.0 does not build with HDF5 1.10
      # See: https://github.com/LLNL/spack/issues/1683
      depends_on('hdf5@:1.9', when='@:1.10.0')
      depends_on('hdf5', when='@1.10.1:')

^^^^^^^^^^^^^^^^
No Version Works
^^^^^^^^^^^^^^^^

Sometimes, *no* existing versions of a dependency work for a build.
This typically happens when developing a new project: only then does
the developer notice that existing versions of a dependency are all
buggy, or the non-buggy versions are all missing a critical feature.

In the long run, the upstream project will hopefully fix the bug and
release a new version.  But that could take a while, even if a bugfix
has already been pushed to the project's repository.  In the meantime,
the Spack user needs things to work.

The solution is to create an unofficial Spack release of the project,
as soon as the bug is fixed in *some* repository.  A study of the `Git
history <https://github.com/citibeth/spack/commits/efischer/develop/var/spack/repos/builtin/packages/py-proj/package.py>`_
of ``py-proj/package.py`` is instructive here:

#. On `April 1 <https://github.com/citibeth/spack/commit/44a1d6a96706affe6ef0a11c3a780b91d21d105a>`_, an initial bugfix was identified for the PyProj project
   and a pull request submitted to PyProj.  Because the upstream
   authors had not yet fixed the bug, the ``py-proj`` Spack package
   downloads from a forked repository, set up by the package's author.
   A non-numeric version number is used to make it easy to upgrade the
   package without recomputing checksums; however, this is an
   untrusted download method and should not be distributed.  The
   package author has now become, temporarily, a maintainer of the
   upstream project:

   .. code-block:: python

      # We need the benefits of this PR
      # https://github.com/jswhit/pyproj/pull/54
      version('citibeth-latlong2',
          git='https://github.com/citibeth/pyproj.git',
          branch='latlong2')


#. By May 14, the upstream project had accepted a pull request with
   the required bugfix.  At this point, the forked repository was
   deleted.  However, the upstream project still had not released a
   new version with a bugfix.  Therefore, a Spack-only release was
   created by specifying the desired hash in the main project
   repository.  The version number ``@1.9.5.1.1`` was chosen for this
   "release" because it's a descendent of the officially released
   version ``@1.9.5.1``.  This is a trusted download method, and can
   be released to the Spack community:

   .. code-block:: python

      # This is not a tagged release of pyproj.
      # The changes in this "version" fix some bugs, especially with Python3 use.
      version('1.9.5.1.1', 'd035e4bc704d136db79b43ab371b27d2',
          url='https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f')

   .. note::

      It would have been simpler to use Spack's Git download method,
      which is also a trusted download in this case:

      .. code-block:: python

         # This is not a tagged release of pyproj.
         # The changes in this "version" fix some bugs, especially with Python3 use.
         version('1.9.5.1.1',
              git='https://github.com/jswhit/pyproj.git',
              commit='0be612cc9f972e38b50a90c946a9b353e2ab140f')

   .. note::

      In this case, the upstream project fixed the bug in its
      repository in a relatively timely manner.  If that had not been
      the case, the numbered version in this step could have been
      released from the forked repository.


#. The author of the Spack package has now become an unofficial
   release engineer for the upstream project.  Depending on the
   situation, it may be advisable to put ``preferred=True`` on the
   latest *officially released* version.

#. As of August 31, the upstream project still had not made a new
   release with the bugfix.  In the meantime, Spack-built ``py-proj``
   provides the bugfix needed by packages depending on it.  As long as
   this works, there is no particular need for the upstream project to
   make a new official release.

#. If the upstream project releases a new official version with the
   bugfix, then the unofficial ``version()`` line should be removed
   from the Spack package.

^^^^^^^
Patches
^^^^^^^

Spack's source patching mechanism provides another way to fix bugs in
upstream projects.  This has advantages and disadvantages compared to the procedures above.

Advantages:

 1. It can fix bugs in existing released versions, and (probably)
    future releases as well.

 2. It is lightweight, does not require a new fork to be set up.

Disadvantages:

 1. It is harder to develop and debug a patch, vs. a branch in a
    repository.  The user loses the automation provided by version
    control systems.

 2. Although patches of a few lines work OK, large patch files can be
    hard to create and maintain.



.. _build-systems:

=============
Build Systems
=============

This guide provides information specific to a particular build system.
It assumes knowledge of general Spack packaging capabilities and expands
on these ideas for each distinct build system that Spack supports.

For reference, the :py:mod:`Build System API docs <spack.build_systems>`
provide a list of build systems and methods/attributes that can be
overridden. If you are curious about the implementation of a particular
build system, you can view the source code by running:

.. code-block:: console

   $ spack edit --build-system autotools


This will open up the ``AutotoolsPackage`` definition in your favorite
editor. In addition, if you are working with a less common build system
like QMake, SCons, or Waf, it may be useful to see examples of other
packages. You can quickly find examples by running:

.. code-block:: console

   $ cd var/spack/repos/builtin/packages
   $ grep -l QMakePackage */package.py


You can then view these packages with ``spack edit``.

This guide is intended to supplement the Build System API docs with
examples of how to override commonly used methods. It also provides
rules of thumb and suggestions for package developers who are unfamiliar
with a particular build system.

---------------
MakefilePackage
---------------

The most primitive build system a package can use is a plain Makefile.
Makefiles are simple to write for small projects, but they usually
require you to edit the Makefile to set platform and compiler-specific
variables.

^^^^^^
Phases
^^^^^^

``MakefilePackage`` comes with 3 phases:

#. ``edit`` - edit the Makefile
#. ``build`` - build the project
#. ``install`` - install the project

By default, ``edit`` does nothing, but you can override it to replace
hard-coded Makefile variables. The ``build`` and ``install`` phases
run:

.. code-block:: console

   $ make
   $ make install


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

The main file that matters for a ``MakefilePackage`` is the Makefile.
This file will be named one of the following ways:

* GNUmakefile (only works with GNU Make)
* Makefile (most common)
* makefile

``Makefile`` is the most common name.

Some Makefiles also *include* other configuration files. Check for an
``include`` directive in the Makefile.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

Spack assumes that the operating system will have a valid ``make`` utility
installed already, so you don't need to add a dependency on ``make``.
However, if the package uses a ``GNUmakefile`` or the developers recommend
using GNU Make, you should add a dependency on ``gmake``:

.. code-block:: python

   depends_on('gmake', type='build')


^^^^^^^^^^^^^^^^^^^^^^^^^^
Types of Makefile packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

Most of the work involved in packaging software that uses Makefiles
involves overriding or replacing hard-coded variables. Many packages
make the mistake of hard-coding compilers, usually for GCC or Intel.
This is fine if you happen to be using that particular compiler, but
Spack is designed to work with *any* compiler, and you need to ensure
that this is the case.

Depending on how the Makefile is designed, there are 4 common strategies
that can be used to set or override the appropriate variables:

"""""""""""""""""""""
Environment variables
"""""""""""""""""""""

Make has multiple types of assignment operators. Some Makefiles
use ``=`` to assign variables. The only way to override these
variables is to edit the Makefile or override them on the command-line.
However, Makefiles that use ``?=`` for assignment honor environment
variables. Since Spack already sets ``CC``, ``CXX``, ``F77``, and ``FC``,
you won't need to worry about setting these variables. If there are
any other variables you need to set, you can do this in the ``edit``
method:

.. code-block:: python

   def edit(self, spec, prefix):
       env['PREFIX'] = prefix
       env['BLASLIB'] = spec['blas'].libs.ld_flags


``cbench`` is a good example of a simple package that does this, while
``esmf`` is a good example of a more complex package.

""""""""""""""""""""""
Command-line arguments
""""""""""""""""""""""

If the Makefile ignores environment variables, the next thing to try
is command-line arguments. You can do this by overriding the
``build_targets`` attribute. If you don't need access to the spec,
you can do this like so:

.. code-block:: python

   build_targets = ['CC=cc']


If you do need access to the spec, you can create a property like so:

.. code-block:: python

   @property
   def build_targets(self):
       spec = self.spec

       return [
           'CC=cc',
           'BLASLIB={0}'.format(spec['blas'].libs.ld_flags),
       ]


``cloverleaf`` is a good example of a package that uses this strategy.

"""""""""""""
Edit Makefile
"""""""""""""

Some Makefiles are just plain stubborn and will ignore command-line
variables. The only way to ensure that these packages build correctly
is to directly edit the Makefile. Spack provides a ``FileFilter`` class
and a ``filter_file`` method to help with this. For example:

.. code-block:: python

   def edit(self, spec, prefix):
       makefile = FileFilter('Makefile')

       makefile.filter('CC = gcc',  'CC = cc')
       makefile.filter('CXX = g++', 'CC = c++')


``stream`` is a good example of a package that involves editing a
Makefile to set the appropriate variables.

"""""""""""
Config file
"""""""""""

More complex packages often involve Makefiles that _include_ a
configuration file. These configuration files are primarily composed
of variables relating to the compiler, platform, and the location of
dependencies or names of libraries. Since these config files are
dependent on the compiler and platform, you will often see entire
directories of examples for common compilers and architectures. Use
these examples to help determine what possible values to use.

If the config file is long and only contains one or two variables
that need to be modified, you can use the technique above to edit
the config file. However, if you end up needing to modify most of
the variables, it may be easier to write a new file from scratch.

If each variable is independent of each other, a dictionary works
well for storing variables:

.. code-block:: python

   def edit(self, spec, prefix):
       config = {
           'CC': 'cc',
           'MAKE': 'make',
       }

       if '+blas' in spec:
           config['BLAS_LIBS'] = spec['blas'].libs.joined()

       with open('make.inc', 'w') as inc:
           for key in config:
               inc.write('{0} = {1}\n'.format(key, config[key]))


``elk`` is a good example of a package that uses a dictionary to
store configuration variables.

If the order of variables is important, it may be easier to store
them in a list:

.. code-block:: python

   def edit(self, spec, prefix):
       config = [
           'INSTALL_DIR = {0}'.format(prefix),
           'INCLUDE_DIR = $(INSTALL_DIR)/include',
           'LIBRARY_DIR = $(INSTALL_DIR)/lib',
       ]

       with open('make.inc', 'w') as inc:
           for var in config:
               inc.write('{0}\n'.format(var))


``hpl`` is a good example of a package that uses a list to store
configuration variables.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Variables to watch out for
^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a list of common variables to watch out for:

* Compilers

  This includes variables such as ``CC``, ``CXX``, ``F77``, ``F90``,
  and ``FC``, as well as variables related to MPI compiler wrappers,
  like ``MPICC`` and friends.

* Compiler flags

  This includes variables for specific compilers, like ``CFLAGS``,
  ``CXXFLAGS``, ``F77FLAGS``, ``F90FLAGS``, ``FCFLAGS``, and ``CPPFLAGS``.
  These variables are often hard-coded to contain flags specific to a
  certain compiler. If these flags don't work for every compiler,
  you may want to consider filtering them.

* Variables that enable or disable features

  This includes variables like ``MPI``, ``OPENMP``, ``PIC``, and
  ``DEBUG``. These flags often require you to create a variant
  so that you can either build with or without MPI support, for
  example. These flags are often compiler-dependent. You should
  replace them with the appropriate compiler flags, such as
  ``self.compiler.openmp_flag`` or ``self.compiler.pic_flag``.

* Platform flags

  These flags control the type of architecture that the executable
  is compiler for. Watch out for variables like ``PLAT``, ``ARCH``,

* Dependencies

  Look out for variables that sound like they could be used to
  locate dependencies, such as ``JAVA_HOME``, ``JPEG_ROOT``, or
  ``ZLIBDIR``. Also watch out for variables that control linking,
  such as ``LIBS``, ``LDFLAGS``, and ``INCLUDES``. These variables
  need to be set to the installation prefix of a dependency, or
  to the correct linker flags to link to that dependency.

* Installation prefix

  If your Makefile has an ``install`` target, it needs some way of
  knowing where to install. By default, many packages install to
  ``/usr`` or ``/usr/local``. Since many Spack users won't have
  sudo privileges, it is imperative that each package is installed
  to the proper prefix. Look for variables like ``PREFIX`` or
  ``INSTALL``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Makefiles in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not every package places their Makefile in the root of the package
tarball. If the Makefile is in a sub-directory like ``src``, you
can tell Spack where to locate it like so:

.. code-block:: python

   build_directory = 'src'


^^^^^^^^^^^^^^^^^^^
Manual installation
^^^^^^^^^^^^^^^^^^^

Not every Makefile includes an ``install`` target. If this is the
case, you can override the default ``install`` method to manually
install the package:

.. code-block:: python

   def install(self, spec, prefix):
       mkdir(prefix.bin)
       install('foo', prefix.bin)
       install_tree('lib', prefix.lib)


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

------------
QMakePackage
------------

Much like Autotools and CMake, QMake is a build script generator
designed by the developers of Qt. In its simplest form, Spack's
``QMakePackage`` runs the following steps:

.. code-block:: console

   $ qmake
   $ make
   $ make check  # optional
   $ make install


QMake does not appear to have a standardized way of specifying
the installation directory, so you may have to set environment
variables or edit ``*.pro`` files to get things working properly.

^^^^^^
Phases
^^^^^^

The ``QMakePackage`` base class comes with the following phases:

#. ``qmake`` - generate Makefiles
#. ``build`` - build the project
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ qmake
   $ make
   $ make install


Any of these phases can be overridden in your package as necessary.
There is also a ``check`` method that looks for a ``check:`` target
in the Makefile. If a ``check:`` target exists and the user runs:

.. code-block:: console

   $ spack install --run-tests <qmake-package>


Spack will run ``make check`` after the build phase.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the QMake build system can be identified by the
presence of a ``<project-name>.pro`` file. This file declares things
like build instructions and dependencies.

One thing to look for is the ``minQtVersion`` function:

.. code-block:: none

   minQtVersion(5, 6, 0)


This means that Qt 5.6.0 is the earliest release that will work.
You should specify this in a ``depends_on`` statement.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the QMake build system need a
``qt`` dependency. Since this is always the case, the ``QMakePackage``
base class already contains:

.. code-block:: python

   depends_on('qt', type='build')


If you want to specify a particular version requirement, or need to
link to the ``qt`` libraries, you can override this in your package:

.. code-block:: python

   depends_on('qt@5.6.0:')

^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to qmake
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to pass any arguments to the ``qmake`` call, you can
override the ``qmake_args`` method like so:

.. code-block:: python

   def qmake_args(self):
       return ['-recursive']


This method can be used to pass flags as well as variables.

-------------
PythonPackage
-------------

Python libraries and modules have their own special build system.

--------
RPackage
--------

Like Python, R has its own built-in build system.

-----------
PerlPackage
-----------

Much like Python and R, Perl has its own language-specific
build system.

-----------
RubyPackage
-----------

Like Python, R, and Perl, Ruby has its own build system for
installing Ruby gems.

This build system is a work-in-progress. See
https://github.com/LLNL/spack/pull/3127 for more information.

------------
SConsPackage
------------

Unlike Autotools and CMake, SCons is a general-purpose build system
that does not rely on Makefiles to build software. SCons is written
in Python, and handles all building and linking itself.

As far as build systems go, SCons is very non-uniform. It provides a
common framework for developers to write build scripts, but the build
scripts themselves can vary drastically. Some developers add subcommands
like:

.. code-block:: console

   $ scons clean
   $ scons build
   $ scons test
   $ scons install


Others don't add any subcommands. Some have configuration options that
can be specified through variables on the command line. Others don't.

^^^^^^
Phases
^^^^^^

As previously mentioned, SCons allows developers to add subcommands like
``build`` and ``install``, but by default, installation usually looks like:

.. code-block:: console

   $ scons
   $ scons install


To facilitate this, Spack provides the following phases:

#. ``build`` - build the package
#. ``install`` - install the package

Package developers often add unit tests that can be invoked with
``scons test`` or ``scons check``. Spack provides a ``test`` method
to handle this. Since we don't know which one the package developer
chose, the ``test`` method does nothing by default, but can be easily
overridden like so:

.. code-block:: python

   def test(self):
       scons('check')


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

SCons packages can be identified by their ``SConstruct`` files. These
files handle everything from setting up subcommands and command-line
options to linking and compiling.

One thing to look for is the ``EnsureSConsVersion`` function:

.. code-block:: none

   EnsureSConsVersion(2, 3, 0)


This means that SCons 2.3.0 is the earliest release that will work.
You should specify this in a ``depends_on`` statement.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the SCons build system need a
``scons`` dependency. Since this is always the case, the ``SConsPackage``
base class already contains:

.. code-block:: python

   depends_on('scons', type='build')


If you want to specify a particular version requirement, you can override
this in your package:

.. code-block:: python

   depends_on('scons@2.3.0:', type='build')


^^^^^^^^^^^^^^^^^^^^^^^^^
Finding available options
^^^^^^^^^^^^^^^^^^^^^^^^^

The first place to start when looking for a list of valid options to
build a package is ``scons --help``. Some packages like ``kahip``
don't bother overwriting the default SCons help message, so this isn't
very useful, but other packages like ``serf`` print a list of valid
command-line variables:

.. code-block:: console

   $ scons --help
   scons: Reading SConscript files ...
   Checking for GNU-compatible C compiler...yes
   scons: done reading SConscript files.

   PREFIX: Directory to install under ( /path/to/PREFIX )
       default: /usr/local
       actual: /usr/local

   LIBDIR: Directory to install architecture dependent libraries under ( /path/to/LIBDIR )
       default: $PREFIX/lib
       actual: /usr/local/lib

   APR: Path to apr-1-config, or to APR's install area ( /path/to/APR )
       default: /usr
       actual: /usr

   APU: Path to apu-1-config, or to APR's install area ( /path/to/APU )
       default: /usr
       actual: /usr

   OPENSSL: Path to OpenSSL's install area ( /path/to/OPENSSL )
       default: /usr
       actual: /usr

   ZLIB: Path to zlib's install area ( /path/to/ZLIB )
       default: /usr
       actual: /usr

   GSSAPI: Path to GSSAPI's install area ( /path/to/GSSAPI )
       default: None
       actual: None

   DEBUG: Enable debugging info and strict compile warnings (yes|no)
       default: False
       actual: False

   APR_STATIC: Enable using a static compiled APR (yes|no)
       default: False
       actual: False

   CC: Command name or path of the C compiler
       default: None
       actual: gcc

   CFLAGS: Extra flags for the C compiler (space-separated)
       default: None
       actual:

   LIBS: Extra libraries passed to the linker, e.g. "-l<library1> -l<library2>" (space separated)
       default: None
       actual: None

   LINKFLAGS: Extra flags for the linker (space-separated)
       default: None
       actual:

   CPPFLAGS: Extra flags for the C preprocessor (space separated)
       default: None
       actual: None

   Use scons -H for help about command-line options.


More advanced packages like ``cantera`` use
``scons --help`` to print a list of subcommands:

.. code-block:: console

   $ scons --help
   scons: Reading SConscript files ...

   SCons build script for Cantera

   Basic usage:
       'scons help' - print a description of user-specifiable options.

       'scons build' - Compile Cantera and the language interfaces using
                       default options.

       'scons clean' - Delete files created while building Cantera.

       '[sudo] scons install' - Install Cantera.

       '[sudo] scons uninstall' - Uninstall Cantera.

       'scons test' - Run all tests which did not previously pass or for which the
                      results may have changed.

       'scons test-reset' - Reset the passing status of all tests.

       'scons test-clean' - Delete files created while running the tests.

       'scons test-help' - List available tests.

       'scons test-NAME' - Run the test named "NAME".

       'scons <command> dump' - Dump the state of the SCons environment to the
                                screen instead of doing <command>, e.g.
                                'scons build dump'. For debugging purposes.

       'scons samples' - Compile the C++ and Fortran samples.

       'scons msi' - Build a Windows installer (.msi) for Cantera.

       'scons sphinx' - Build the Sphinx documentation

       'scons doxygen' - Build the Doxygen documentation


You'll notice that ``cantera`` provides a ``scons help`` subcommand. Running
``scons help`` prints a list of valid command-line variables.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to scons
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you know what arguments the project accepts, you can add them to
the package build phase. This is done by overriding ``build_args`` like so:

.. code-block:: python

   def build_args(self, spec, prefix):
       args = [
         'PREFIX={0}'.format(prefix),
         'ZLIB={0}'.format(spec['zlib'].prefix),
       ]

       if '+debug' in spec:
           args.append('DEBUG=yes')
       else:
           args.append('DEBUG=no')

       return args


``SConsPackage`` also provides a ``install_args`` function that you can
override to pass additional arguments to ``scons install``.

^^^^^^^^^^^^^^^^^
Compiler wrappers
^^^^^^^^^^^^^^^^^

By default, SCons builds all packages in a separate execution environment,
and doesn't pass any environment variables from the user environment.
Even changes to ``PATH`` are not propagated unless the package developer
does so.

This is particularly troublesome for Spack's compiler wrappers, which depend
on environment variables to manage dependencies and linking flags. In many
cases, SCons packages are not compatible with Spack's compiler wrappers,
and linking must be done manually.

First of all, check the list of valid options for anything relating to
environment variables. For example, ``cantera`` has the following option:

.. code-block:: none

   * env_vars: [ string ]
       Environment variables to propagate through to SCons. Either the
       string "all" or a comma separated list of variable names, e.g.
       'LD_LIBRARY_PATH,HOME'.
       - default: 'LD_LIBRARY_PATH,PYTHONPATH'


In the case of ``cantera``, using ``env_vars=all`` allows us to use
Spack's compiler wrappers. If you don't see an option related to
environment variables, try using Spack's compiler wrappers. The full
path to these wrappers are stored in ``spack_cc`` and friends. If
you pass them to the build and you see an error message like:

.. code-block:: none

   Spack compiler must be run from Spack! Input 'SPACK_PREFIX' is missing.


you'll know that the package isn't compatible with Spack's compiler
wrappers. In this case, you'll have to use the path to the actual
compilers, which are stored in ``self.compiler.cc`` and friends.
Note that this may involve passing additional flags to the build to
locate dependencies, a task normally done by the compiler wrappers.
``serf`` is an example of a package with this limitation.

----------
WafPackage
----------

Like SCons, Waf is a general-purpose build system that does not rely
on Makefiles to build software.

------------
IntelPackage
------------

Intel provides many licensed software packages, which all share the
same basic steps for configuring and installing, as well as license
management.

This build system is a work-in-progress. See
https://github.com/LLNL/spack/pull/4300 for more information.

--------------------
Custom Build Systems
--------------------

While the build systems listed above should meet your needs for the
vast majority of packages, some packages provide custom build scripts.

.. _developer_guide:

===============
Developer Guide
===============

This guide is intended for people who want to work on Spack itself.
If you just want to develop packages, see the :ref:`packaging-guide`.

It is assumed that you've read the :ref:`basic-usage` and
:ref:`packaging-guide` sections, and that you're familiar with the
concepts discussed there.  If you're not, we recommend reading those
first.

--------
Overview
--------

Spack is designed with three separate roles in mind:

#. **Users**, who need to install software *without* knowing all the
   details about how it is built.
#. **Packagers** who know how a particular software package is
   built and encode this information in package files.
#. **Developers** who work on Spack, add new features, and try to
   make the jobs of packagers and users easier.

Users could be end users installing software in their home directory,
or administrators installing software to a shared directory on a
shared machine.  Packagers could be administrators who want to
automate software builds, or application developers who want to make
their software more accessible to users.

As you might expect, there are many types of users with different
levels of sophistication, and Spack is designed to accommodate both
simple and complex use cases for packages.  A user who only knows that
he needs a certain package should be able to type something simple,
like ``spack install <package name>``, and get the package that he
wants.  If a user wants to ask for a specific version, use particular
compilers, or build several versions with different configurations,
then that should be possible with a minimal amount of additional
specification.

This gets us to the two key concepts in Spack's software design:

#. **Specs**: expressions for describing builds of software, and
#. **Packages**: Python modules that build software according to a
   spec.

A package is a template for building particular software, and a spec
as a descriptor for one or more instances of that template.  Users
express the configuration they want using a spec, and a package turns
the spec into a complete build.

The obvious difficulty with this design is that users under-specify
what they want.  To build a software package, the package object needs
a *complete* specification.  In Spack, if a spec describes only one
instance of a package, then we say it is **concrete**.  If a spec
could describes many instances, (i.e. it is under-specified in one way
or another), then we say it is **abstract**.

Spack's job is to take an *abstract* spec from the user, find a
*concrete* spec that satisfies the constraints, and hand the task of
building the software off to the package object.  The rest of this
document describes all the pieces that come together to make that
happen.

-------------------
Directory Structure
-------------------

So that you can familiarize yourself with the project, we'll start
with a high level view of Spack's directory structure:

.. code-block:: none

   spack/                  <- installation root
      bin/
         spack             <- main spack executable

      etc/
         spack/            <- Spack config files.
                              Can be overridden by files in ~/.spack.

      var/
         spack/            <- build & stage directories
             repos/            <- contains package repositories
                builtin/       <- pkg repository that comes with Spack
                   repo.yaml   <- descriptor for the builtin repository
                   packages/   <- directories under here contain packages
             cache/        <- saves resources downloaded during installs

      opt/
         spack/            <- packages are installed here

      lib/
         spack/
            docs/          <- source for this documentation
            env/           <- compiler wrappers for build environment

            external/      <- external libs included in Spack distro
            llnl/          <- some general-use libraries

            spack/         <- spack module; contains Python code
               cmd/        <- each file in here is a spack subcommand
               compilers/  <- compiler description files
               test/       <- unit test modules
               util/       <- common code

Spack is designed so that it could live within a `standard UNIX
directory hierarchy <http://linux.die.net/man/7/hier>`_, so ``lib``,
``var``, and ``opt`` all contain a ``spack`` subdirectory in case
Spack is installed alongside other software.  Most of the interesting
parts of Spack live in ``lib/spack``.

Spack has *one* directory layout and there is no install process.
Most Python programs don't look like this (they use distutils, ``setup.py``,
etc.) but we wanted to make Spack *very* easy to use.  The simple layout
spares users from the need to install Spack into a Python environment.
Many users don't have write access to a Python installation, and installing
an entire new instance of Python to bootstrap Spack would be very complicated.
Users should not have to install install a big, complicated package to
use the thing that's supposed to spare them from the details of big,
complicated packages.  The end result is that Spack works out of the
box: clone it and add ``bin`` to your PATH and you're ready to go.

--------------
Code Structure
--------------

This section gives an overview of the various Python modules in Spack,
grouped by functionality.

^^^^^^^^^^^^^^^^^^^^^^^
Package-related modules
^^^^^^^^^^^^^^^^^^^^^^^

:mod:`spack.package`
  Contains the :class:`Package <spack.package.Package>` class, which
  is the superclass for all packages in Spack.  Methods on ``Package``
  implement all phases of the :ref:`package lifecycle
  <package-lifecycle>` and manage the build process.

:mod:`spack.packages`
  Contains all of the packages in Spack and methods for managing them.
  Functions like :func:`packages.get <spack.packages.get>` and
  :func:`class_name_for_package_name
  <packages.class_name_for_package_name>` handle mapping package module
  names to class names and dynamically instantiating packages by name
  from module files.

:mod:`spack.relations`
  *Relations* are relationships between packages, like
  :func:`depends_on <spack.relations.depends_on>` and :func:`provides
  <spack.relations.provides>`.  See :ref:`dependencies` and
  :ref:`virtual-dependencies`.

:mod:`spack.multimethod`
  Implementation of the :func:`@when <spack.multimethod.when>`
  decorator, which allows :ref:`multimethods <multimethods>` in
  packages.

^^^^^^^^^^^^^^^^^^^^
Spec-related modules
^^^^^^^^^^^^^^^^^^^^

:mod:`spack.spec`
  Contains :class:`Spec <spack.spec.Spec>` and :class:`SpecParser
  <spack.spec.SpecParser>`. Also implements most of the logic for
  normalization and concretization of specs.

:mod:`spack.parse`
  Contains some base classes for implementing simple recursive descent
  parsers: :class:`Parser <spack.parse.Parser>` and :class:`Lexer
  <spack.parse.Lexer>`.  Used by :class:`SpecParser
  <spack.spec.SpecParser>`.

:mod:`spack.concretize`
  Contains :class:`DefaultConcretizer
  <spack.concretize.DefaultConcretizer>` implementation, which allows
  site administrators to change Spack's :ref:`concretization-policies`.

:mod:`spack.version`
  Implements a simple :class:`Version <spack.version.Version>` class
  with simple comparison semantics.  Also implements
  :class:`VersionRange <spack.version.VersionRange>` and
  :class:`VersionList <spack.version.VersionList>`.  All three are
  comparable with each other and offer union and intersection
  operations.  Spack uses these classes to compare versions and to
  manage version constraints on specs.  Comparison semantics are
  similar to the ``LooseVersion`` class in ``distutils`` and to the
  way RPM compares version strings.

:mod:`spack.compilers`
  Submodules contains descriptors for all valid compilers in Spack.
  This is used by the build system to set up the build environment.

  .. warning::

     Not yet implemented.  Currently has two compiler descriptions,
     but compilers aren't fully integrated with the build process
     yet.

:mod:`spack.architecture`
  :func:`architecture.sys_type <spack.architecture.sys_type>` is used
  to determine the host architecture while building.

  .. warning::

     Not yet implemented.  Should eventually have architecture
     descriptions for cross-compiling.

^^^^^^^^^^^^^^^^^
Build environment
^^^^^^^^^^^^^^^^^

:mod:`spack.stage`
  Handles creating temporary directories for builds.

:mod:`spack.compilation`
  This contains utility functions used by the compiler wrapper script,
  ``cc``.

:mod:`spack.directory_layout`
  Classes that control the way an installation directory is laid out.
  Create more implementations of this to change the hierarchy and
  naming scheme in ``$spack_prefix/opt``

^^^^^^^^^^^^^^^^^
Spack Subcommands
^^^^^^^^^^^^^^^^^

:mod:`spack.cmd`
  Each module in this package implements a Spack subcommand.  See
  :ref:`writing commands <writing-commands>` for details.

^^^^^^^^^^
Unit tests
^^^^^^^^^^

:mod:`spack.test`
  Implements Spack's test suite.  Add a module and put its name in
  the test suite in ``__init__.py`` to add more unit tests.

:mod:`spack.test.mock_packages`
  This is a fake package hierarchy used to mock up packages for
  Spack's test suite.

^^^^^^^^^^^^^
Other Modules
^^^^^^^^^^^^^

:mod:`spack.url`
  URL parsing, for deducing names and versions of packages from
  tarball URLs.

:mod:`spack.error`
  :class:`SpackError <spack.error.SpackError>`, the base class for
  Spack's exception hierarchy.

:mod:`llnl.util.tty`
  Basic output functions for all of the messages Spack writes to the
  terminal.

:mod:`llnl.util.tty.color`
  Implements a color formatting syntax used by ``spack.tty``.

:mod:`llnl.util`
  In this package are a number of utility modules for the rest of
  Spack.

------------
Spec objects
------------

---------------
Package objects
---------------

Most spack commands look something like this:

#. Parse an abstract spec (or specs) from the command line,
#. *Normalize* the spec based on information in package files,
#. *Concretize* the spec according to some customizable policies,
#. Instantiate a package based on the spec, and
#. Call methods (e.g., ``install()``) on the package object.

The information in Package files is used at all stages in this
process.

Conceptually, packages are overloaded.  They contain:

-------------
Stage objects
-------------

.. _writing-commands:

----------------
Writing commands
----------------

Adding a new command to Spack is easy. Simply add a ``<name>.py`` file to
``lib/spack/spack/cmd/``, where ``<name>`` is the name of the subcommand.
At the bare minimum, two functions are required in this file:

^^^^^^^^^^^^^^^^^^
``setup_parser()``
^^^^^^^^^^^^^^^^^^

Unless your command doesn't accept any arguments, a ``setup_parser()``
function is required to define what arguments and flags your command takes.
See the `Argparse documentation <https://docs.python.org/2.7/library/argparse.html>`_
for more details on how to add arguments.

Some commands have a set of subcommands, like ``spack compiler find`` or
``spack module refresh``. You can add subparsers to your parser to handle
this. Check out ``spack edit --command compiler`` for an example of this.

A lot of commands take the same arguments and flags. These arguments should
be defined in ``lib/spack/spack/cmd/common/arguments.py`` so that they don't
need to be redefined in multiple commands.

^^^^^^^^^^^^
``<name>()``
^^^^^^^^^^^^

In order to run your command, Spack searches for a function with the same
name as your command in ``<name>.py``. This is the main method for your
command, and can call other helper methods to handle common tasks.

Remember, before adding a new command, think to yourself whether or not this
new command is actually necessary. Sometimes, the functionality you desire
can be added to an existing command. Also remember to add unit tests for
your command. If it isn't used very frequently, changes to the rest of
Spack can cause your command to break without sufficient unit tests to
prevent this from happening.

----------
Unit tests
----------

------------
Unit testing
------------

------------------
Developer commands
------------------

.. _cmd-spack-doc:

^^^^^^^^^^^^^
``spack doc``
^^^^^^^^^^^^^

.. _cmd-spack-test:

^^^^^^^^^^^^^^
``spack test``
^^^^^^^^^^^^^^

.. _cmd-spack-url:

^^^^^^^^^^^^^
``spack url``
^^^^^^^^^^^^^

A package containing a single URL can be used to download several different
versions of the package. If you've ever wondered how this works, all of the
magic is in :mod:`spack.url`. This module contains methods for extracting
the name and version of a package from its URL. The name is used by
``spack create`` to guess the name of the package. By determining the version
from the URL, Spack can replace it with other versions to determine where to
download them from.

The regular expressions in ``parse_name_offset`` and ``parse_version_offset``
are used to extract the name and version, but they aren't perfect. In order
to debug Spack's URL parsing support, the ``spack url`` command can be used.

"""""""""""""""""""
``spack url parse``
"""""""""""""""""""

If you need to debug a single URL, you can use the following command:

.. command-output:: spack url parse http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz

You'll notice that the name and version of this URL are correctly detected,
and you can even see which regular expressions it was matched to. However,
you'll notice that when it substitutes the version number in, it doesn't
replace the ``2.2`` with ``9.9`` where we would expect ``9.9.9b`` to live.
This particular package may require a ``list_url`` or ``url_for_version``
function.

This command also accepts a ``--spider`` flag. If provided, Spack searches
for other versions of the package and prints the matching URLs.

""""""""""""""""""
``spack url list``
""""""""""""""""""

This command lists every URL in every package in Spack. If given the
``--color`` and ``--extrapolation`` flags, it also colors the part of
the string that it detected to be the name and version. The
``--incorrect-name`` and ``--incorrect-version`` flags can be used to
print URLs that were not being parsed correctly.

""""""""""""""""""
``spack url test``
""""""""""""""""""

This command attempts to parse every URL for every package in Spack
and prints a summary of how many of them are being correctly parsed.
It also prints a histogram showing which regular expressions are being
matched and how frequently:

.. command-output:: spack url test

This command is essential for anyone adding or changing the regular
expressions that parse names and versions. By running this command
before and after the change, you can make sure that your regular
expression fixes more packages than it breaks.

---------
Profiling
---------

Spack has some limited built-in support for profiling, and can report
statistics using standard Python timing tools.  To use this feature,
supply ``--profile`` to Spack on the command line, before any subcommands.

.. _spack-p:

^^^^^^^^^^^^^^^^^^^
``spack --profile``
^^^^^^^^^^^^^^^^^^^

``spack --profile`` output looks like this:

.. command-output:: spack --profile graph dyninst
   :ellipsis: 25

The bottom of the output shows the top most time consuming functions,
slowest on top.  The profiling support is from Python's built-in tool,
`cProfile
<https://docs.python.org/2/library/profile.html#module-cProfile>`_.

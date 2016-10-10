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

:mod:`spack.globals`
  Includes global settings for Spack.  the default policy classes for
  things like :ref:`temporary space <temp-space>` and
  :ref:`concretization <concretization-policies>`.

:mod:`spack.tty`
  Basic output functions for all of the messages Spack writes to the
  terminal.

:mod:`spack.color`
  Implements a color formatting syntax used by ``spack.tty``.

:mod:`spack.url`
  URL parsing, for deducing names and versions of packages from
  tarball URLs.

:mod:`spack.util`
  In this package are a number of utility modules for the rest of
  Spack.

:mod:`spack.error`
  :class:`SpackError <spack.error.SpackError>`, the base class for
  Spack's exception hierarchy.

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

----------
Unit tests
----------

------------
Unit testing
------------

------------------
Developer commands
------------------

^^^^^^^^^^^^^
``spack doc``
^^^^^^^^^^^^^

^^^^^^^^^^^^^^
``spack test``
^^^^^^^^^^^^^^

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

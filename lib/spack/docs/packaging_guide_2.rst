.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _packaging-guide-part-2:

======================================
Packaging Guide: customizing the build
======================================

In the first part of the packaging guide, we covered the basic structure of a package, how to specify dependencies, and how to define variants.
In the second part, we will cover the installation procedure, build systems, and how to customize the build process.

.. _installation_procedure:

--------------------------------------
Overview of the installation procedure
--------------------------------------

Whenever Spack installs software, it goes through a series of predefined steps:

.. image:: images/installation_pipeline.png
  :scale: 60 %
  :align: center

All these steps are influenced by the metadata in each ``package.py`` and by the current Spack configuration.
Since build systems are different from one another, the execution of the last block in the figure is further expanded in a build system specific way.
An example for ``CMake`` is, for instance:

.. image:: images/builder_phases.png
   :align: center
   :scale: 60 %

The predefined steps for each build system are called "phases".
In general, the name and order in which the phases will be executed can be obtained by either reading the API docs at :py:mod:`~.spack_repo.builtin.build_systems`, or using the ``spack info`` command:

.. code-block:: console
    :emphasize-lines: 13,14

    $ spack info --phases m4
    AutotoolsPackage:    m4
    Homepage:            https://www.gnu.org/software/m4/m4.html

    Safe versions:
        1.4.17    ftp://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz

    Variants:
        Name       Default   Description

        sigsegv    on        Build the libsigsegv dependency

    Installation Phases:
        autoreconf    configure    build    install

    Build Dependencies:
        libsigsegv

    ...

An extensive list of available build systems and phases is provided in :ref:`installation_process`.

-----------------------------
Controlling the build process
-----------------------------

As we have seen in the first part of the packaging guide, the usual workflow for creating a package is to start with ``spack create <url>``, which generates a ``package.py`` file for you with a boilerplate package class.
This typically includes a package base class (e.g. ``AutotoolsPackage`` or ``CMakePackage``), a URL, and one or more versions.
After you have added required dependencies and variants, you can start customizing the build process.
There are various ways to do this, depending on the build system and the package itself.

From simplest to most complex, the following are the most common ways to customize the build process:

1. **Implementing build system helper methods and properties**.
   Most build systems provide a set of helper methods that can be overridden to customize the build process without overriding entire phases.
   For example, for ``AutotoolsPackage`` you can specify the command line arguments for ``./configure`` by implementing ``configure_args``:

   .. code-block:: python
   
      def configure_args(self):
          # FIXME: Add arguments other than --prefix
          # FIXME: If not needed delete this function
          args = []
          return args

   Similarly for ``CMakePackage`` you can influence how ``cmake`` is invoked by implementing ``cmake_args``:

   .. code-block:: python
   
      def cmake_args(self):
          # FIXME: Add arguments other than
          # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
          # FIXME: If not needed delete this function
          args = []
          return args

   The exact methods and properties available depend on the build system you are using.

2. **Setting environment variables**.
   Some build systems require specific environment variables to be set before the build starts.
   You can set these variables by overriding the ``setup_build_environment`` method in your package class:

   .. code-block:: python
   
      def setup_build_environment(self, env):
          env.set("MY_ENV_VAR", "value")

   This is useful for setting paths or other variables that the build system needs to find dependencies or configure itself correctly.

   See :ref:`setup-environment`.

3. **Complementing the build system with pre- or post-build steps**.
   In some cases, you may need to run additional commands before or after the build system phases.
   This is useful for installing additional files missed by the build system, or for running custom scripts.

   .. code-block:: python
   
      @run_after("install")
      def install_missing_files(self):
          install_tree("extra_files", self.prefix.bin)

   See :ref:`before_after_build_phases`.

4. **Overriding entire build phases**.
   If the default implementation of a build phase does not fit your needs, you can override the entire phase.
   See :ref:`overriding-phases` for examples.

In any of the functions above, you can

1. **Make instructions dynamic**.
   Build instructions typically depend on the package's variants, version and its dependencies.
   For example, you can use

   .. code-block:: python

      if self.spec.satisfies("+variant_name"):
         ...
   
   to check if a variant is enabled, or
   
   .. code-block:: python

      self.spec["dependency_name"].prefix

   to get the prefix of a dependency.
   See :ref:`spec-objects` for more details on how to use specs in your package.
2. **Use Spack's Python Package API**.
   The ``from spack.package import *`` statement at the top of a ``package.py`` file allows you to access Spack's utilities and helper functions, such as ``which``, ``install_tree``, ``filter_file`` and others.
   See :ref:`python-package-api` for more details.


.. _installation_process:

-------------
Build systems
-------------

Every package in Spack has an associated build system.
For most packages, this will be a well-known system for which Spack provides a base class, like ``CMakePackage`` or ``AutotoolsPackage``.
Even for packages that have no formal build process (e.g., just copying files), Spack still associates them with a generic build system class.
Build systems have the following responsibilities:

1. **Define and implement the build phases**.
   Each build system defines a set of phases that are executed in a specific order.
   For example, ``AutotoolsPackage`` has the following phases: ``autoreconf``, ``configure``, ``build``, and ``install``.
   These phases are Python methods with a sensible default implementation that can be overridden by the package author.
2. **Add dependencies and variants**.
   Build systems can define dependencies and variants that are specific to the build system.
   For example, ``CMakePackage`` adds a ``cmake`` as a build dependency, and defines ``build_type`` as a variant (which maps to the ``CMAKE_BUILD_TYPE`` CMake variable).
   All build systems also define a special variant ``build_system``, which is useful in case of :ref:`multiple_build_systems`.
3. **Provide helper methods**.
   Build systems often provide helper functions and properties that the package author can use to customize the build process.
   For example ``CMakePackage`` provides the ``cmake_args`` method to specify additional arguments for the ``cmake`` command, and the ``build_targets`` property is used in ``MakefilePackage`` to specify what make targets to build (e.g., ``make lib``).

Here is a table of the most common build systems available in Spack:

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Package Class
     - Description
   * - :doc:`AutotoolsPackage <build_systems/autotoolspackage>`
     - For packages that use GNU Autotools (autoconf, automake, libtool).
   * - :doc:`CMakePackage <build_systems/cmakepackage>`
     - For packages that use CMake.
   * - :doc:`MakefilePackage <build_systems/makefilepackage>`
     - For packages that use plain Makefiles.
   * - :doc:`MesonPackage <build_systems/mesonpackage>`
     - For packages that use the Meson build system.
   * - :doc:`PythonPackage <build_systems/pythonpackage>`
     - For Python packages (setuptools, pip, etc.).
   * - :doc:`BundlePackage <build_systems/bundlepackage>`
     - For installing a collection of other packages.
   * - :doc:`Package <build_systems/custompackage>`
     - Generic package for custom builds, provides only an ``install`` phase.

All build systems are defined in the ``spack_repo.builtin.build_systems`` module, which is part of the Spack builtin package repository.
To use a particular build system, you need to import it in your ``package.py`` file, and then derive your package class from the appropriate base class:

.. code-block:: python

   from spack_repo.builtin.build_systems.cmake import CMakePackage

   class MyPkg(CMakePackage):
       pass

For a complete list of build systems and their specific helper functions and properties, see the :doc:`build_systems` documentation.


.. _spec-objects:

---------------------------------------
Configuring the build with spec objects
---------------------------------------

Whenever you implement helper functions of a build system or complement or override its build phases, you will often need to make decisions based on the package's configuration.
Spack is unique in that it allows you to write a *single* ``package.py`` for all configurations of a package.

Spack makes this easy by providing the ``self.spec`` object, which encodes the current package's configuration.
Together with Spack's **spec language**, you can easily specify conditional build instructions.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using ``self.spec.satisfies``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Variants and versions**.
If you want to pass a flag to the configure script only if the package is built with a specific variant, you can do so like this:

.. code-block:: python

   def configure_args(self):
       args = []
       if self.spec.satisfies("+foo"):  # 'foo' is enabled
           args.append("--enable-foo")
       else:
           args.append("--disable-foo")

       if self.spec.satisfies("@1.2:"):  # version 1.2 or higher
           args.append("--enable-bar")
       else:
           args.append("--disable-bar")

       return args

Notice that many build systems provide helper functions to make the above code more concise.
See :ref:`the Autotools docs <autotools_helper_functions>` and :ref:`the CMake docs <cmake_args>`.

**Dependencies**.
You can also use the ``self.spec.satisfies`` method to test whether a dependency is present or not, and whether it is built with a specific variant or version.

The ``%`` character is used to refer to direct dependencies, which is often useful when you want to test the compiler used to build the package.

.. code-block:: python

   if self.spec.satisfies("%gcc@8:"):
       args.append("--enable-profile-guided-optimization")

The ``^`` character is used to refer to runtime and build dependencies.

.. code-block:: python

   if self.spec.satisfies("^python@3.8:"):
       args.append("--min-python-version=3.8")


**Target specific configuration**.
Spack always makes the special ``platform``, ``os`` and ``target`` variants available in the spec.
These variants can be used to test the target platform, operating system and CPU microarchitecture the package.

The following example shows how we can add a configure option only if the package is built for Apple Silicon:

.. code-block:: python

   if self.spec.satisfies("platform=darwin target=aarch64:"):
       args.append("--enable-apple-silicon")

Notice that ``target=aarch64:`` is a range which matches the whole family of ``aarch64`` microarchitectures, including ``m1``, ``m2``, and so on.

You can use ranges starting at a specific microarchitecture as well, for example:

.. code-block:: python

   if self.spec.satisfies("target=haswell:"):
       args.append("--enable-haswell")

.. note::

   The ``spec`` object encodes the *target* platform, os and architecture the package is being built for.
   This is different from the *host* platform (typically accessed via ``sys.platform``) which is the platform where Spack is running.
   When writing package recipes, you should always use the ``spec`` object to query the target platform, os and architecture.

To see what targets are available in your Spack installation, you can use the following command:

.. command-output:: spack arch --known-targets

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Referring to a dependency's prefix, libraries, and headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Very often you need to inform the build system about the location of a dependency.
The most common way to do this is to pass the dependency's prefix as a configure argument.

By sub-scripting the spec, you get another ``Spec`` object that represents the dependency:

.. code-block:: python

   libxml2 = self.spec["libxml2"]

The value in the brackets needs to be a package name on which the package depends.
What is returned is itself just another ``Spec`` object, so you can do all the same things you would do with the package's own spec:

.. code-block:: python

   def configure_args(self):
       return [
           f"--with-libxml2={self.spec['libxml2'].prefix}",
       ]

Most build systems have their own logic to locate libraries and headers of dependencies, so often it is sufficient to pass the dependency's prefix to the build system.

To be more precise, you can also refer to :ref:`custom-attributes` from the dependency.
In other cases, you can be more specific and use the dependency's attributes such as ``libs`` or ``headers``.

Apart from the :ref:`prefix <prefix-objects>`, you can also access other attributes of the dependency, such as ``libs`` or ``headers``.




.. _before_after_build_phases:

-----------------------------
Before and after build phases
-----------------------------

Typically the default implementation of the build system's phases is sufficient for most packages.
However, in some cases you may need to complement th default implementation with some custom instructions.
Instead of overriding the entire phase, you can use ``@run_before`` and ``@run_after`` to run custom code before or after a specific phase:

.. code-block:: python

   class MyPackage(CMakePackage):
       ...

       variant("extras", default=False, description="Install extra files")

       @run_before("cmake")
       def run_before_cmake_is_invoked(self):
           with open("custom_file.txt", "w") as f:
               f.write("This file is created before cmake is invoked.")

       @run_after("install", when="+extras")
       def custom_post_install_phase(self):
           # install missing files not covered by the build system
           install_tree("extras", self.prefix.share.extras)

Then ``when="+extras"`` will ensure that the custom post-install phase is only run conditionally.


.. _overriding-phases:

------------------------
Overriding a build phase
------------------------

In rare cases it is necessary to override a build phase.
The most common instance is when the package does not have a well-defined build system.
For example, the installation procedure may just be copying files or running a shell script.
In that case, you can use the generic ``Package`` class, which defines only a single ``install()`` phase, to be overridden by the package author:

.. code-block:: python

   from spack.package import *
   from spack_repo.builtin.build_systems.generic import Package

   class MyPkg(Package):
       def install(self, spec: Spec, prefix: Prefix):
           # Custom install logic
           install_tree("my_files", prefix.bin)

The signature of every build phase function is the same, and has the following arguments:

``self``
    This is the package object, which extends ``CMakePackage``.
    For API docs on Package objects, see
    :py:class:`Package <spack.package_base.PackageBase>`.

``spec``
    This is the concrete spec object created by Spack from an abstract spec supplied by the user.
    It describes what should be installed.
    It will be of type :py:class:`Spec <spack.spec.Spec>`.

``prefix``
    This is where your package should install its files.
    It acts like a string, but it's actually its :ref:`own special type <prefix-objects>`.

The arguments ``spec`` and ``prefix`` are passed only for convenience, as they always correspond to ``self.spec`` and ``self.spec.prefix`` respectively.

.. _setup-environment:

--------------------------------------------
Runtime and build time environment variables
--------------------------------------------

Spack provides a few methods to help package authors set up the required environment variables for
their package. Environment variables typically depend on how the package is used: variables that
make sense during the build phase may not be needed at runtime, and vice versa. Further, sometimes
it makes sense to let a dependency set the environment variables for its dependents. To allow all
this, Spack provides four different methods that can be overridden in a package:

1. :meth:`setup_build_environment <spack.builder.BaseBuilder.setup_build_environment>`
2. :meth:`setup_run_environment <spack.package_base.PackageBase.setup_run_environment>`
3. :meth:`setup_dependent_build_environment <spack.builder.BaseBuilder.setup_dependent_build_environment>`
4. :meth:`setup_dependent_run_environment <spack.package_base.PackageBase.setup_dependent_run_environment>`

The Qt package, for instance, uses this call:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/qt/package.py
   :pyobject: Qt.setup_dependent_build_environment
   :linenos:

to set the ``QTDIR`` environment variable so that packages that depend on a particular Qt
installation will find it.

The following diagram will give you an idea when each of these methods is called in a build
context:

.. image:: images/setup_env.png
   :align: center

Notice that ``setup_dependent_run_environment`` can be called multiple times, once for each
dependent package, whereas ``setup_run_environment`` is called only once for the package itself.
This means that the former should only be used if the environment variables depend on the dependent
package, whereas the latter should be used if the environment variables depend only on the package
itself.


.. _multiple_build_systems:

----------------------
Multiple build systems
----------------------

There are cases where a package actively supports two build systems, or changes build systems
as it evolves, or needs different build systems on different platforms. Spack allows dealing with
these cases by splitting the build instructions into separate builder classes.

For instance, software that supports two build systems unconditionally should derive from
both ``*Package`` base classes, and declare the possible use of multiple build systems using
a directive:

.. code-block:: python

   class Example(CMakePackage, AutotoolsPackage):

       variant("my_feature", default=True)

       build_system("cmake", "autotools", default="cmake")

In this case the software can be built with both ``autotools`` and ``cmake``. Since the package
supports multiple build systems, it is necessary to declare which one is the default.

Additional build instructions are split into separate builder classes:

.. code-block:: python

   class CMakeBuilder(spack_repo.builtin.build_systems.cmake.CMakeBuilder):
       def cmake_args(self):
           return [
               self.define_from_variant("MY_FEATURE", "my_feature")
           ]

   class AutotoolsBuilder(spack_repo.builtin.build_systems.autotools.AutotoolsBuilder):
       def configure_args(self):
           return self.with_or_without("my-feature", variant="my_feature")

In this example, ``spack install example +feature build_system=cmake``  will
pick the ``CMakeBuilder`` and invoke ``cmake -DMY_FEATURE:BOOL=ON``.

Similarly, ``spack install example +feature build_system=autotools`` will pick
the  ``AutotoolsBuilder`` and invoke ``./configure --with-my-feature``.

Dependencies are always specified in the package class. When some dependencies
depend on the choice of the build system, it is possible to use when conditions as
usual:

.. code-block:: python

   class Example(CMakePackage, AutotoolsPackage):

       build_system("cmake", "autotools", default="cmake")

       # Runtime dependencies
       depends_on("ncurses")
       depends_on("libxml2")

       # Lowerbounds for cmake only apply when using cmake as the build system
       with when("build_system=cmake"):
           depends_on("cmake@3.18:", when="@2.0:", type="build")
           depends_on("cmake@3:", type="build")

       # Specify extra build dependencies used only in the configure script
       with when("build_system=autotools"):
           depends_on("perl", type="build")
           depends_on("pkgconfig", type="build")

Very often projects switch from one build system to another, or add support
for a new build system from a certain version, which means that the choice
of the build system typically depends on a version range. Those situations can
be handled by using conditional values in the ``build_system`` directive:

.. code-block:: python

   class Example(CMakePackage, AutotoolsPackage):

       build_system(
           conditional("cmake", when="@0.64:"),
           conditional("autotools", when="@:0.63"),
           default="cmake",
       )

In the example the directive imposes a change from ``Autotools`` to ``CMake`` going
from ``v0.63`` to ``v0.64``.

The ``build_system`` can be used as an ordinary variant, which also means that it can
be used in ``depends_on`` statements. This can be useful when a package *requires* that
its dependency has a CMake config file, meaning that the dependent can only build when the
dependency is built with CMake, and not Autotools. In that case, you can force the choice
of the build system in the dependent:

.. code-block:: python

   class Dependent(CMakePackage):

       depends_on("example build_system=cmake")

.. _environment-variables:


---------------------
Environment variables
---------------------

Spack sets a number of standard environment variables that serve two
purposes:

#. Make build systems use Spack's compiler wrappers for their builds.
#. Allow build systems to find dependencies more easily

The Compiler environment variables that Spack sets are:

  ============  ===============================
    Variable     Purpose
  ============  ===============================
    ``CC``       C compiler
    ``CXX``      C++ compiler
    ``F77``      Fortran 77 compiler
    ``FC``       Fortran 90 and above compiler
  ============  ===============================

Spack sets these variables so that they point to *compiler
wrappers*. These are covered in :ref:`their own section
<compiler-wrappers>` below.

All of these are standard variables respected by most build systems.
If your project uses ``Autotools`` or ``CMake``, then it should pick
them up automatically when you run ``configure`` or ``cmake`` in the
``install()`` function.  Many traditional builds using GNU Make and
BSD make also respect these variables, so they may work with these
systems.

If your build system does *not* automatically pick these variables up
from the environment, then you can simply pass them on the command
line or use a patch as part of your build process to get the correct
compilers into the project's build system.  There are also some file
editing commands you can use -- these are described later in the
`section on file manipulation <python-package-api_>`_.

In addition to the compiler variables, these variables are set before
entering ``install()`` so that packages can locate dependencies
easily:

=====================  ====================================================
``PATH``               Set to point to ``/bin`` directories of dependencies
``CMAKE_PREFIX_PATH``  Path to dependency prefixes for CMake
``PKG_CONFIG_PATH``    Path to any pkgconfig directories for dependencies
``PYTHONPATH``         Path to site-packages dir of any python dependencies
=====================  ====================================================

``PATH`` is set up to point to dependencies ``/bin`` directories so
that you can use tools installed by dependency packages at build time.
For example, ``$MPICH_ROOT/bin/mpicc`` is frequently used by dependencies of
``mpich``.

``CMAKE_PREFIX_PATH`` contains a colon-separated list of prefixes
where ``cmake`` will search for dependency libraries and headers.
This causes all standard CMake find commands to look in the paths of
your dependencies, so you *do not* have to manually specify arguments
like ``-DDEPENDENCY_DIR=/path/to/dependency`` to ``cmake``.  More on
this is `in the CMake documentation <http://www.cmake.org/cmake/help/v3.0/variable/CMAKE_PREFIX_PATH.html>`_.

``PKG_CONFIG_PATH`` is for packages that attempt to discover
dependencies using the GNU ``pkg-config`` tool.  It is similar to
``CMAKE_PREFIX_PATH`` in that it allows a build to automatically
discover its dependencies.

If you want to see the environment that a package will build with, or
if you want to run commands in that environment to test them out, you
can use the :ref:`cmd-spack-build-env` command, documented
below.

-----------------
Failing the build
-----------------

Sometimes you don't want a package to successfully install unless some
condition is true.  You can explicitly cause the build to fail from
``install()`` by raising an ``InstallError``, for example:

.. code-block:: python

   if spec.architecture.startswith("darwin"):
       raise InstallError("This package does not build on Mac OS X!")

.. _shell-wrappers:

-----------------------
Shell command functions
-----------------------

Recall the install method from ``libelf``:

.. literalinclude::  .spack/spack-packages/repos/spack_repo/builtin/packages/libelf/package.py
   :pyobject: Libelf.install
   :linenos:

Normally in Python, you'd have to write something like this in order
to execute shell commands:

.. code-block:: python

   import subprocess
   subprocess.check_call("configure", "--prefix={0}".format(prefix))

We've tried to make this a bit easier by providing callable wrapper
objects for some shell commands.  By default, ``configure``,
``cmake``, and ``make`` wrappers are provided, so you can call
them more naturally in your package files.

If you need other commands, you can use ``which`` to get them:

.. code-block:: python

   sed = which("sed")
   sed("s/foo/bar/", filename)

The ``which`` function will search the ``PATH`` for the application.

Callable wrappers also allow Spack to provide some special features.
For example, in Spack, ``make`` is parallel by default, and Spack
figures out the number of cores on your machine and passes an
appropriate value for ``-j<numjobs>`` when it calls ``make`` (see the
``parallel`` `package attribute <attribute_parallel>`).  In
a package file, you can supply a keyword argument, ``parallel=False``,
to the ``make`` wrapper to disable parallel make.  In the ``libelf``
package, this allows us to avoid race conditions in the library's
build system.

--------------
Compiler flags
--------------

Compiler flags set by the user through the Spec object can be passed
to the build in one of three ways. By default, the build environment
injects these flags directly into the compiler commands using Spack's
compiler wrappers. In cases where the build system requires knowledge
of the compiler flags, they can be registered with the build system by
alternatively passing them through environment variables or as build
system arguments. The flag_handler method can be used to change this
behavior.

Packages can override the flag_handler method with one of three
built-in flag_handlers. The built-in flag_handlers are named
``inject_flags``, ``env_flags``, and ``build_system_flags``. The
``inject_flags`` method is the default. The ``env_flags`` method puts
all of the flags into the environment variables that ``make`` uses as
implicit variables ("CFLAGS", "CXXFLAGS", etc.). The
``build_system_flags`` method adds the flags as
arguments to the invocation of ``configure`` or ``cmake``,
respectively.

.. warning::

   Passing compiler flags using build system arguments is only
   supported for CMake and Autotools packages. Individual packages may
   also differ in whether they properly respect these arguments.

Individual packages may also define their own ``flag_handler``
methods. The ``flag_handler`` method takes the package instance
(``self``), the name of the flag, and a list of the values of the
flag. It will be called on each of the six compiler flags supported in
Spack. It should return a triple of ``(injf, envf, bsf)`` where
``injf`` is a list of flags to inject via the Spack compiler wrappers,
``envf`` is a list of flags to set in the appropriate environment
variables, and ``bsf`` is a list of flags to pass to the build system
as arguments.

.. warning::

   Passing a non-empty list of flags to ``bsf`` for a build system
   that does not support build system arguments will result in an
   error.

Here are the definitions of the three built-in flag handlers:

.. code-block:: python

   def inject_flags(pkg, name, flags):
       return (flags, None, None)

   def env_flags(pkg, name, flags):
       return (None, flags, None)

   def build_system_flags(pkg, name, flags):
       return (None, None, flags)

.. note::

   Returning ``[]`` and ``None`` are equivalent in a ``flag_handler``
   method.

Packages can override the default behavior either by specifying one of
the built-in flag handlers,

.. code-block:: python

   flag_handler = env_flags

or by implementing the flag_handler method. Suppose for a package
``Foo`` we need to pass ``cflags``, ``cxxflags``, and ``cppflags``
through the environment, the rest of the flags through compiler
wrapper injection, and we need to add ``-lbar`` to ``ldlibs``. The
following flag handler method accomplishes that.

.. code-block:: python

   def flag_handler(self, name, flags):
       if name in ["cflags", "cxxflags", "cppflags"]:
           return (None, flags, None)
       elif name == "ldlibs":
           flags.append("-lbar")
       return (flags, None, None)

Because these methods can pass values through environment variables,
it is important not to override these variables unnecessarily
(E.g. setting ``env["CFLAGS"]``) in other package methods when using
non-default flag handlers. In the ``setup_environment`` and
``setup_dependent_environment`` methods, use the ``append_flags``
method of the ``EnvironmentModifications`` class to append values to a
list of flags whenever the flag handler is ``env_flags``. If the
package passes flags through the environment or the build system
manually (in the install method, for example), we recommend using the
default flag handler, or removing manual references and implementing a
custom flag handler method that adds the desired flags to export as
environment variables or pass to the build system. Manual flag passing
is likely to interfere with the ``env_flags`` and
``build_system_flags`` methods.

In rare circumstances such as compiling and running small unit tests, a
package developer may need to know what are the appropriate compiler
flags to enable features like ``OpenMP``, ``c++11``, ``c++14`` and
the like. To that end the compiler classes in ``spack`` implement the
following **properties**: ``openmp_flag``, ``cxx98_flag``, ``cxx11_flag``,
``cxx14_flag``, and ``cxx17_flag``, which can be accessed in a package by
``self.compiler.cxx11_flag`` and the like. Note that the implementation is
such that if a given compiler version does not support this feature, an
error will be produced. Therefore, package developers can also use these
properties to assert that a compiler supports the requested feature. This
is handy when a package supports additional variants like

.. code-block:: python

   variant("openmp", default=True, description="Enable OpenMP support.")

.. _blas_lapack_scalapack:

------------------------------------
Blas, Lapack and ScaLapack libraries
------------------------------------

Multiple packages provide implementations of ``Blas``, ``Lapack`` and ``ScaLapack``
routines.  The names of the resulting static and/or shared libraries
differ from package to package. In order to make the ``install()`` method
independent of the choice of ``Blas`` implementation, each package which
provides it implements ``@property def blas_libs(self):`` to return an object
`LibraryList <https://spack.readthedocs.io/en/latest/llnl.util.html#llnl.util.filesystem.LibraryList>`_
type which simplifies usage of a set of libraries.
The same applies to packages which provide ``Lapack`` and ``ScaLapack``.
Package developers are requested to use this interface. Common usage cases are:

1. Space separated list of full paths

.. code-block:: python

   lapack_blas = spec["lapack"].libs + spec["blas"].libs
   options.append(
      "--with-blas-lapack-lib={0}".format(lapack_blas.joined())
   )

2. Names of libraries and directories which contain them

.. code-block:: python

   blas = spec["blas"].libs
   options.extend([
     "-DBLAS_LIBRARY_NAMES={0}".format(";".join(blas.names)),
     "-DBLAS_LIBRARY_DIRS={0}".format(";".join(blas.directories))
   ])

3. Search and link flags

.. code-block:: python

   math_libs = spec["scalapack"].libs + spec["lapack"].libs + spec["blas"].libs
   options.append(
     "-DMATH_LIBS:STRING={0}".format(math_libs.ld_flags)
   )


For more information, see documentation of
`LibraryList <https://spack.readthedocs.io/en/latest/llnl.util.html#llnl.util.filesystem.LibraryList>`_
class.


.. _prefix-objects:

--------------
Prefix objects
--------------

You can find the installation directory of package in Spack by using the ``self.prefix`` attribute of the package object.
In :ref:`overriding-phases`, we saw that the ``install()`` method has a ``prefix`` argument, which is the same as ``self.prefix``.
This variable behaves like a string, but it is actually an instance of the :py:class:`Prefix <spack.util.prefix.Prefix>` class, which provides some additional functionality to make it easier to work with file paths in Spack.

In particular, you can use the ``.`` operator to join paths together, creating nested directory structures:

======================  =======================
Prefix Attribute        Location
======================  =======================
``prefix.bin``          ``$prefix/bin``
``prefix.lib64``        ``$prefix/lib64``
``prefix.share.man``    ``$prefix/share/man``
``prefix.foo.bar.baz``  ``$prefix/foo/bar/baz``
======================  =======================

Of course, this only works if your file or directory is a valid Python variable name.
If your file or directory contains dashes or dots, use ``join`` instead:

.. code-block:: python

   prefix.lib.join("libz.a")

--------------------------------
Setting package module variables
--------------------------------

Apart from modifying environment variables of the dependent package, you can also define Python
variables to be used by the dependent. This is done by implementing
:meth:`setup_dependent_package <spack.package_base.PackageBase.setup_dependent_package>`. An
example of this can be found in the ``Python`` package:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/python/package.py
   :pyobject: Python.setup_dependent_package
   :linenos:

This allows Python packages to directly use these variables:

.. code-block:: python

   def install(self, spec, prefix):
       ...
       install("script.py", python_platlib)

.. note::

   We recommend using ``setup_dependent_package`` sparingly, as it is not always clear where
   global variables are coming from when editing a ``package.py`` file.


.. _multimethods:

--------------------------
Multimethods and ``@when``
--------------------------

The ``@when`` annotation lets packages declare multiple versions of a method that will be called
depending on the package's spec.
This can be useful to handle cases where configure options are entirely different depending on the version of the package, or when the package is built for different platforms.

.. code-block:: python

   class SomePackage(Package):
       ...

       @when("@:1")
       def configure_args(self):
           return ["--old-flag"]

       @when("@2:")
       def configure_args(self):
           return ["--new-flag"]

You can write multiple ``@when`` specs that satisfy the package's spec, for example:

.. code-block:: python

   class SomePackage(Package):
       ...
       depends_on("mpi")

       def setup_mpi(self):
           # the default, called when no @when specs match
           pass

       @when("^mpi@3:")
       def setup_mpi(self):
           # this will be called when mpi is version 3 or higher
           pass

       @when("^mpi@2:")
       def setup_mpi(self):
           # this will be called when mpi is version 2 or higher
           pass

       @when("^mpi@1:")
       def setup_mpi(self):
           # this will be called when mpi is version 1 or higher
           pass

In situations like this, the first matching spec, in declaration order, will be called.
If no ``@when`` spec matches, the default method (the one without the ``@when`` decorator) will be called.

.. warning::

   The default method (without the ``@when`` decorator) should come first in the declaration order.
   If not, it will erase all ``@when`` methods that precede it in the class.
   This is a limitation of decorators in Python.

.. _compiler-wrappers:

---------------------
Compiler wrappers
---------------------

As mentioned, ``CC``, ``CXX``, ``F77``, and ``FC`` are set to point to
Spack's compiler wrappers.  These are simply called ``cc``, ``c++``,
``f77``, and ``f90``, and they live in ``$SPACK_ROOT/lib/spack/env``.

``$SPACK_ROOT/lib/spack/env`` is added first in the ``PATH``
environment variable when ``install()`` runs so that system compilers
are not picked up instead.

All of these compiler wrappers point to a single compiler wrapper
script that figures out which *real* compiler it should be building
with.  This comes either from spec `concretization
<abstract-and-concrete>`_ or from a user explicitly asking for a
particular compiler using, e.g., ``%intel`` on the command line.

In addition to invoking the right compiler, the compiler wrappers add
flags to the compile line so that dependencies can be easily found.
These flags are added for each dependency, if they exist:

* Compile-time library search paths: ``-L$dep_prefix/lib``, ``-L$dep_prefix/lib64``
* Runtime library search paths (RPATHs): ``$rpath_flag$dep_prefix/lib``, ``$rpath_flag$dep_prefix/lib64``
* Include search paths: ``-I$dep_prefix/include``

An example of this would be the ``libdwarf`` build, which has one
dependency: ``libelf``.  Every call to ``cc`` in the ``libdwarf``
build will have ``-I$LIBELF_PREFIX/include``,
``-L$LIBELF_PREFIX/lib``, and ``$rpath_flag$LIBELF_PREFIX/lib``
inserted on the command line.  This is done transparently to the
project's build system, which will just think it's using a system
where ``libelf`` is readily available.  Because of this, you **do
not** have to insert extra ``-I``, ``-L``, etc. on the command line.

Another useful consequence of this is that you often do *not* have
to add extra parameters on the ``configure`` line to get autotools to
find dependencies.  The ``libdwarf`` install method just calls
configure like this:

.. code-block:: python

   configure("--prefix=" + prefix)

Because of the ``-L`` and ``-I`` arguments, configure will
successfully find ``libdwarf.h`` and ``libdwarf.so``, without the
packager having to provide ``--with-libdwarf=/path/to/libdwarf`` on
the command line.

.. note::

    For most compilers, ``$rpath_flag`` is ``-Wl,-rpath,``. However, NAG
    passes its flags to GCC instead of passing them directly to the linker.
    Therefore, its ``$rpath_flag`` is doubly wrapped: ``-Wl,-Wl,,-rpath,``.
    ``$rpath_flag`` can be overridden on a compiler-specific basis in
    ``lib/spack/spack/compilers/$compiler.py``.

The compiler wrappers also pass the compiler flags specified by the user from
the command line (``cflags``, ``cxxflags``, ``fflags``, ``cppflags``, ``ldflags``,
and/or ``ldlibs``). They do not override the canonical autotools flags with the
same names (but in ALL-CAPS) that may be passed into the build by particularly
challenging package scripts.

---------------------
MPI support in Spack
---------------------

It is common for high-performance computing software/packages to use the
Message Passing Interface ( ``MPI``).  As a result of concretization, a
given package can be built using different implementations of MPI such as
``OpenMPI``, ``MPICH`` or ``IntelMPI``.  That is, when your package
declares that it ``depends_on("mpi")``, it can be built with any of these
``mpi`` implementations. In some scenarios, to configure a package, one
has to provide it with appropriate MPI compiler wrappers such as
``mpicc``, ``mpic++``.  However, different implementations of ``MPI`` may
have different names for those wrappers.

Spack provides an idiomatic way to use MPI compilers in your package.  To
use MPI wrappers to compile your whole build, do this in your
``install()`` method:

.. code-block:: python

   env["CC"] = spec["mpi"].mpicc
   env["CXX"] = spec["mpi"].mpicxx
   env["F77"] = spec["mpi"].mpif77
   env["FC"] = spec["mpi"].mpifc

That's all.  A longer explanation of why this works is below.

We don't try to force any particular build method on packagers.  The
decision to use MPI wrappers depends on the way the package is written,
on common practice, and on "what works".  Loosely, there are three types
of MPI builds:

  1. Some build systems work well without the wrappers and can treat MPI
     as an external library, where the person doing the build has to
     supply includes/libs/etc.  This is fairly uncommon.

  2. Others really want the wrappers and assume you're using an MPI
     "compiler" – i.e., they have no mechanism to add MPI
     includes/libraries/etc.

  3. CMake's ``FindMPI`` needs the compiler wrappers, but it uses them to
     extract ``–I`` / ``-L`` / ``-D`` arguments, then treats MPI like a
     regular library.

Note that some CMake builds fall into case 2 because they either don't
know about or don't like CMake's ``FindMPI`` support – they just assume
an MPI compiler. Also, some autotools builds fall into case 3 (e.g., `here
is an autotools version of CMake's FindMPI
<https://github.com/tgamblin/libra/blob/master/m4/lx_find_mpi.m4>`_).

Given all of this, we leave the use of the wrappers up to the packager.
Spack will support all three ways of building MPI packages.

^^^^^^^^^^^^^^^^^^^^^
Packaging Conventions
^^^^^^^^^^^^^^^^^^^^^

As mentioned above, in the ``install()`` method, ``CC``, ``CXX``,
``F77``, and ``FC`` point to Spack's wrappers around the chosen compiler.
Spack's wrappers are not the MPI compiler wrappers, though they do
automatically add ``–I``, ``–L``, and ``–Wl,-rpath`` args for
dependencies in a similar way.  The MPI wrappers are a bit different in
that they also add ``-l`` arguments for the MPI libraries, and some add
special ``-D`` arguments to trigger build options in MPI programs.

For case 1 above, you generally don't need to do more than patch your
Makefile or add configure args as you normally would.

For case 3, you don't need to do much of anything, as Spack puts the MPI
compiler wrappers in the PATH, and the build will find them and
interrogate them.

For case 2, things are a bit more complicated, as you'll need to tell the
build to use the MPI compiler wrappers instead of Spack's compiler
wrappers.  All it takes some lines like this:

.. code-block:: python

   env["CC"] = spec["mpi"].mpicc
   env["CXX"] = spec["mpi"].mpicxx
   env["F77"] = spec["mpi"].mpif77
   env["FC"] = spec["mpi"].mpifc

Or, if you pass CC, CXX, etc. directly to your build with, e.g.,
`--with-cc=<path>`, you'll want to substitute `spec["mpi"].mpicc` in
there instead, e.g.:

.. code-block:: python

   configure("--prefix=%s" % prefix,
             "--with-cc=%s" % spec["mpi"].mpicc)

Now, you may think that doing this will lose the includes, library paths,
and RPATHs that Spack's compiler wrappers get you, but we've actually set
things up so that the MPI compiler wrappers use Spack's compiler wrappers
when run from within Spack. So using the MPI wrappers should really be as
simple as the code above.

^^^^^^^^^^^^^^^^^^^^^
``spec["mpi"]``
^^^^^^^^^^^^^^^^^^^^^

Ok, so how does all this work?

If your package has a virtual dependency like ``mpi``, then referring to
``spec["mpi"]`` within ``install()`` will get you the concrete ``mpi``
implementation in your dependency DAG.  That is a spec object just like
the one passed to install, only the MPI implementations all set some
additional properties on it to help you out.  E.g., in openmpi, you'll
find this:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/openmpi/package.py
   :pyobject: Openmpi.setup_dependent_package

That code allows the ``openmpi`` package to associate an ``mpicc`` property
with the ``openmpi`` node in the DAG, so that dependents can access it.
``mvapich2`` and ``mpich`` do similar things.  So, no matter what MPI
you're using, spec["mpi"].mpicc gets you the location of the MPI
compilers. This allows us to have a fairly simple polymorphic interface
for information about virtual dependencies like MPI.

^^^^^^^^^^^^^^^^^^^^^
Wrapping wrappers
^^^^^^^^^^^^^^^^^^^^^

Spack likes to use its own compiler wrappers to make it easy to add
``RPATHs`` to builds, and to try hard to ensure that your builds use the
right dependencies.  This doesn't play nicely by default with MPI, so we
have to do a couple tricks.

  1. If we build MPI with Spack's wrappers, mpicc and friends will be
     installed with hard-coded paths to Spack's wrappers, and using them
     from outside of Spack will fail because they only work within Spack.
     To fix this, we patch mpicc and friends to use the regular
     compilers.  Look at the filter_compilers method in mpich, openmpi,
     or mvapich2 for details.

  2. We still want to use the Spack compiler wrappers when Spack is
     calling mpicc. Luckily, wrappers in all mainstream MPI
     implementations provide environment variables that allow us to
     dynamically set the compiler to be used by mpicc, mpicxx, etc.
     Denis pasted some code from this below – Spack's build environment
     sets ``MPICC``, ``MPICXX``, etc. for mpich derivatives and
     ``OMPI_CC``, ``OMPI_CXX``, etc. for OpenMPI. This makes the MPI
     compiler wrappers use the Spack compiler wrappers so that your
     dependencies still get proper RPATHs even if you use the MPI
     wrappers.

^^^^^^^^^^^^^^^^^^^^^
MPI on Cray machines
^^^^^^^^^^^^^^^^^^^^^

The Cray programming environment notably uses ITS OWN compiler wrappers,
which function like MPI wrappers.  On Cray systems, the ``CC``, ``cc``,
and ``ftn`` wrappers ARE the MPI compiler wrappers, and it's assumed that
you'll use them for all of your builds.  So on Cray we don't bother with
``mpicc``, ``mpicxx``, etc., Spack MPI implementations set
``spec["mpi"].mpicc`` to point to Spack's wrappers, which wrap the Cray
wrappers, which wrap the regular compilers and include MPI flags.  That
may seem complicated, but for packagers, that means the same code for
using MPI wrappers will work, even on a Cray:

.. code-block:: python

   env["CC"] = spec["mpi"].mpicc

This is because on Cray, ``spec["mpi"].mpicc`` is just ``spack_cc``.



.. _python-package-api:

--------------------------
Spack's Python Package API
--------------------------

Many builds are not perfect.
If a build lacks an install target, or if it does not use systems like CMake or Autotools, which have standard ways of setting compilers and options, you may need to edit files or install some files yourself to get them working with Spack.

You can do this with standard Python code, and Python has rich libraries with functions for file manipulation and filtering.
Spack also provides a number of convenience functions of its own to make your life even easier.
These functions are described in this section.

All of the functions in this section can be included by simply running:

.. code-block:: python

   from spack.package import *

This is already part of the boilerplate for packages created with ``spack create``.

.. _file-filtering:

^^^^^^^^^^^^^^^^^^^
Filtering functions
^^^^^^^^^^^^^^^^^^^

:py:func:`filter_file(regex, repl, *filenames, **kwargs) <llnl.util.filesystem.filter_file>`
  Works like ``sed`` but with Python regular expression syntax.  Takes
  a regular expression, a replacement, and a set of files.  ``repl``
  can be a raw string or a callable function.  If it is a raw string,
  it can contain ``\1``, ``\2``, etc. to refer to capture groups in
  the regular expression.  If it is a callable, it is passed the
  Python ``MatchObject`` and should return a suitable replacement
  string for the particular match.

  Examples:

  #. Filtering a Makefile to force it to use Spack's compiler wrappers:

     .. code-block:: python

        filter_file(r"^\s*CC\s*=.*",  "CC = "  + spack_cc,  "Makefile")
        filter_file(r"^\s*CXX\s*=.*", "CXX = " + spack_cxx, "Makefile")
        filter_file(r"^\s*F77\s*=.*", "F77 = " + spack_f77, "Makefile")
        filter_file(r"^\s*FC\s*=.*",  "FC = "  + spack_fc,  "Makefile")

  #. Replacing ``#!/usr/bin/perl`` with ``#!/usr/bin/env perl`` in ``bib2xhtml``:

     .. code-block:: python

        filter_file(r"#!/usr/bin/perl",
                    "#!/usr/bin/env perl", prefix.bin.bib2xhtml)

  #. Switching the compilers used by ``mpich``'s MPI wrapper scripts from
     ``cc``, etc. to the compilers used by the Spack build:

     .. code-block:: python

        filter_file("CC='cc'", "CC='%s'" % self.compiler.cc,
                    prefix.bin.mpicc)

        filter_file("CXX='c++'", "CXX='%s'" % self.compiler.cxx,
                    prefix.bin.mpicxx)

:py:func:`change_sed_delimiter(old_delim, new_delim, *filenames) <llnl.util.filesystem.change_sed_delimiter>`
    Some packages, like TAU, have a build system that can't install
    into directories with, e.g. "@" in the name, because they use
    hard-coded ``sed`` commands in their build.

    ``change_sed_delimiter`` finds all ``sed`` search/replace commands
    and changes the delimiter.  e.g., if the file contains commands
    that look like ``s///``, you can use this to change them to
    ``s@@@``.

    Example of changing ``s///`` to ``s@@@`` in TAU:

    .. code-block:: python

       change_sed_delimiter("@", ";", "configure")
       change_sed_delimiter("@", ";", "utils/FixMakefile")
       change_sed_delimiter("@", ";", "utils/FixMakefile.sed.default")

^^^^^^^^^^^^^^
File functions
^^^^^^^^^^^^^^

:py:func:`ancestor(dir, n=1) <llnl.util.filesystem.ancestor>`
  Get the n\ :sup:`th` ancestor of the directory ``dir``.

:py:func:`can_access(path) <llnl.util.filesystem.can_access>`
  True if we can read and write to the file at ``path``.  Same as
  native Python ``os.access(file_name, os.R_OK|os.W_OK)``.

:py:func:`install(src, dest) <llnl.util.filesystem.install>`
  Install a file to a particular location.  For example, install a
  header into the ``include`` directory under the install ``prefix``:

  .. code-block:: python

     install("my-header.h", prefix.include)

:py:func:`join_path(*paths) <llnl.util.filesystem.join_path>`
  An alias for ``os.path.join``. This joins paths using the OS path separator.

:py:func:`mkdirp(*paths) <llnl.util.filesystem.mkdirp>`
  Create each of the directories in ``paths``, creating any parent
  directories if they do not exist.

:py:func:`working_dir(dirname, kwargs) <llnl.util.filesystem.working_dir>`
  This is a Python `Context Manager
  <https://docs.python.org/2/library/contextlib.html>`_ that makes it
  easier to work with subdirectories in builds.  You use this with the
  Python ``with`` statement to change into a working directory, and
  when the with block is done, you change back to the original
  directory.  Think of it as a safe ``pushd`` / ``popd`` combination,
  where ``popd`` is guaranteed to be called at the end, even if
  exceptions are thrown.

  Example usage:

  #. The ``libdwarf`` build first runs ``configure`` and ``make`` in a
     subdirectory called ``libdwarf``.  It then implements the
     installation code itself.  This is natural with ``working_dir``:

     .. code-block:: python

        with working_dir("libdwarf"):
            configure("--prefix=" + prefix, "--enable-shared")
            make()
            install("libdwarf.a",  prefix.lib)

  #. Many CMake builds require that you build "out of source", that
     is, in a subdirectory.  You can handle creating and ``cd``'ing to
     the subdirectory like the LLVM package does:

     .. code-block:: python

        with working_dir("spack-build", create=True):
            cmake("..",
                  "-DLLVM_REQUIRES_RTTI=1",
                  "-DPYTHON_EXECUTABLE=/usr/bin/python",
                  "-DPYTHON_INCLUDE_DIR=/usr/include/python2.6",
                  "-DPYTHON_LIBRARY=/usr/lib64/libpython2.6.so",
                  *std_cmake_args)
            make()
            make("install")

     The ``create=True`` keyword argument causes the command to create
     the directory if it does not exist.

:py:func:`touch(path) <llnl.util.filesystem.touch>`
  Create an empty file at ``path``.



-----------------------------
Style guidelines for packages
-----------------------------

The following guidelines are provided, in the interests of making
Spack packages work in a consistent manner:

^^^^^^^^^^^^^
Variant Names
^^^^^^^^^^^^^

Spack packages with variants similar to already-existing Spack
packages should use the same name for their variants.  Standard
variant names are:

  ======= ======== ========================
  Name    Default   Description
  ======= ======== ========================
  shared   True     Build shared libraries
  mpi      True     Use MPI
  python   False    Build Python extension
  ======= ======== ========================

If specified in this table, the corresponding default should be used
when declaring a variant.

The semantics of the `shared` variant are important. When a package is
built `~shared`, the package guarantees that no shared libraries are
built. When a package is built `+shared`, the package guarantees that
shared libraries are built, but it makes no guarantee about whether
static libraries are built.

^^^^^^^^^^^^^
Version Lists
^^^^^^^^^^^^^

Spack packages should list supported versions with the newest first.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using ``home`` vs ``prefix``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``home`` and ``prefix`` are both attributes that can be queried on a
package's dependencies, often when passing configure arguments pointing to the
location of a dependency.  The difference is that while ``prefix`` is the
location on disk where a concrete package resides, ``home`` is the `logical`
location that a package resides, which may be different than ``prefix`` in
the case of virtual packages or other special circumstances.  For most use
cases inside a package, its dependency locations can be accessed via either
``self.spec["foo"].home`` or ``self.spec["foo"].prefix``.  Specific packages
that should be consumed by dependents via ``.home`` instead of ``.prefix``
should be noted in their respective documentation.

See :ref:`custom-attributes` for more details and an example implementing
a custom ``home`` attribute.

---------------------------
Packaging workflow commands
---------------------------

When you are building packages, you will likely not get things
completely right the first time.

The ``spack install`` command performs a number of tasks before it
finally installs each package.  It downloads an archive, expands it in
a temporary directory, and only then gives control to the package's
``install()`` method.  If the build doesn't go as planned, you may
want to clean up the temporary directory, or if the package isn't
downloading properly, you might want to run *only* the ``fetch`` stage
of the build.

Spack performs best-effort installation of package dependencies by default,
which means it will continue to install as many dependencies as possible
after detecting failures.  If you are trying to install a package with a
lot of dependencies where one or more may fail to build, you might want to
try the ``--fail-fast`` option to stop the installation process on the first
failure.

A typical package workflow might look like this:

.. code-block:: console

   $ spack edit mypackage
   $ spack install --fail-fast mypackage
   ... build breaks! ...
   $ spack clean mypackage
   $ spack edit mypackage
   $ spack install --fail-fast mypackage
   ... repeat clean/install until install works ...

Below are some commands that will allow you some finer-grained
control over the install process.

.. _cmd-spack-fetch:

^^^^^^^^^^^^^^^
``spack fetch``
^^^^^^^^^^^^^^^

The first step of ``spack install``.  Takes a spec and determines the
correct download URL to use for the requested package version, then
downloads the archive, checks it against an MD5 checksum, and stores
it in a staging directory if the check was successful.  The staging
directory will be located under the first writable directory in the
``build_stage`` configuration setting.

When run after the archive has already been downloaded, ``spack
fetch`` is idempotent and will not download the archive again.

.. _cmd-spack-stage:

^^^^^^^^^^^^^^^
``spack stage``
^^^^^^^^^^^^^^^

The second step in ``spack install`` after ``spack fetch``.  Expands
the downloaded archive in its temporary directory, where it will be
built by ``spack install``.  Similar to ``fetch``, if the archive has
already been expanded,  ``stage`` is idempotent.

.. _cmd-spack-patch:

^^^^^^^^^^^^^^^
``spack patch``
^^^^^^^^^^^^^^^

After staging, Spack applies patches to downloaded packages, if any
have been specified in the package file.  This command will run the
install process through the fetch, stage, and patch phases.  Spack
keeps track of whether patches have already been applied and skips
this step if they have been.  If Spack discovers that patches didn't
apply cleanly on some previous run, then it will restage the entire
package before patching.

.. _cmd-spack-restage:

^^^^^^^^^^^^^^^^^
``spack restage``
^^^^^^^^^^^^^^^^^

Restores the source code to pristine state, as it was before building.

Does this in one of two ways:

#. If the source was fetched as a tarball, deletes the entire build
   directory and re-expands the tarball.

#. If the source was checked out from a repository, this deletes the
   build directory and checks it out again.

.. _cmd-spack-clean:

^^^^^^^^^^^^^^^
``spack clean``
^^^^^^^^^^^^^^^

Cleans up Spack's temporary and cached files.  This command can be used to
recover disk space if temporary files from interrupted or failed installs
accumulate.

When called with ``--stage`` or without arguments this removes all staged
files.

The ``--downloads`` option removes :ref:`cached <caching>` downloads.

You can force the removal of all install failure tracking markers using the
``--failures`` option.  Note that ``spack install`` will automatically clear
relevant failure markings prior to performing the requested installation(s).

Long-lived caches, like the virtual package index, are removed using the
``--misc-cache`` option.

The ``--python-cache`` option removes `.pyc`, `.pyo`, and `__pycache__`
folders.

To remove all of the above, the command can be called with ``--all``.

When called with positional arguments, this command cleans up temporary files
only for a particular package. If ``fetch``, ``stage``, or ``install``
are run again after this, Spack's build process will start from scratch.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Keeping the stage directory on success
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, ``spack install`` will delete the staging area once a
package has been successfully built and installed.  Use
``--keep-stage`` to leave the build directory intact:

.. code-block:: console

   $ spack install --keep-stage <spec>

This allows you to inspect the build directory and potentially debug
the build.  You can use ``clean`` later to get rid of the
unwanted temporary files.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Keeping the install prefix on failure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, ``spack install`` will delete any partially constructed
install prefix if anything fails during ``install()``.  If you want to
keep the prefix anyway (e.g. to diagnose a bug), you can use
``--keep-prefix``:

.. code-block:: console

   $ spack install --keep-prefix <spec>

Note that this may confuse Spack into thinking that the package has
been installed properly, so you may need to use ``spack uninstall --force``
to get rid of the install prefix before you build again:

.. code-block:: console

   $ spack uninstall --force <spec>

---------------------
Graphing dependencies
---------------------

.. _cmd-spack-graph:

^^^^^^^^^^^^^^^
``spack graph``
^^^^^^^^^^^^^^^

Spack provides the ``spack graph`` command for graphing dependencies.
The command by default generates an ASCII rendering of a spec's
dependency graph.  For example:

.. command-output:: spack graph hdf5

At the top is the root package in the DAG, with dependency edges emerging
from it.  On a color terminal, the edges are colored by which dependency
they lead to.

.. command-output:: spack graph --deptype=link hdf5

The ``deptype`` argument tells Spack what types of dependencies to graph.
By default it includes link and run dependencies but not build
dependencies.  Supplying ``--deptype=link`` will show only link
dependencies.  The default is ``--deptype=all``, which is equivalent to
``--deptype=build,link,run,test``.  Options for ``deptype`` include:

* Any combination of ``build``, ``link``, ``run``, and ``test`` separated
  by commas.
* ``all`` for all types of dependencies.

You can also use ``spack graph`` to generate graphs in the widely used
`Dot <http://www.graphviz.org/doc/info/lang.html>`_ format.  For example:

.. command-output:: spack graph --dot hdf5

This graph can be provided as input to other graphing tools, such as
those in `Graphviz <http://www.graphviz.org>`_.  If you have graphviz
installed, you can write straight to PDF like this:

.. code-block:: console

   $ spack graph --dot hdf5 | dot -Tpdf > hdf5.pdf

.. _packaging-shell-support:

-------------------------
Interactive shell support
-------------------------

Spack provides some limited shell support to make life easier for
packagers.  You can enable these commands by sourcing a setup file in
the ``share/spack`` directory.  For ``bash`` or ``ksh``, run:

.. code-block:: sh

   export SPACK_ROOT=/path/to/spack
   . $SPACK_ROOT/share/spack/setup-env.sh

For ``csh`` and ``tcsh`` run:

.. code-block:: csh

   setenv SPACK_ROOT /path/to/spack
   source $SPACK_ROOT/share/spack/setup-env.csh

``spack cd`` will then be available.

.. _cmd-spack-cd:

^^^^^^^^^^^^
``spack cd``
^^^^^^^^^^^^

``spack cd`` allows you to quickly cd to pertinent directories in Spack.
Suppose you've staged a package but you want to modify it before you
build it:

.. code-block:: console

   $ spack stage libelf
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.13.tar.gz
   ######################################################################## 100.0%
   ==> Staging archive: ~/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3 arch=linux-debian7-x86_64/libelf-0.8.13.tar.gz
   ==> Created stage in ~/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3 arch=linux-debian7-x86_64.
   $ spack cd libelf
   $ pwd
   ~/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3 arch=linux-debian7-x86_64/libelf-0.8.13

``spack cd`` here changed the current working directory to the
directory containing the expanded ``libelf`` source code.  There are a
number of other places you can cd to in the spack directory hierarchy:

.. command-output:: spack cd --help

Some of these change directory into package-specific locations (stage
directory, install directory, package directory) and others change to
core spack locations.  For example, ``spack cd --module-dir`` will take you to
the main python source directory of your spack install.

.. _cmd-spack-build-env:

^^^^^^^^^^^^^^^^^^^
``spack build-env``
^^^^^^^^^^^^^^^^^^^

``spack build-env`` functions much like the standard Unix ``build-env``
command, but it takes a spec as an argument.  You can use it to see the
environment variables that will be set when a particular build runs,
for example:

.. code-block:: console

   $ spack build-env mpileaks@1.1%intel

This will display the entire environment that will be set when the
``mpileaks@1.1%intel`` build runs.

To run commands in a package's build environment, you can simply
provide them after the spec argument to ``spack build-env``:

.. code-block:: console

   $ spack cd mpileaks@1.1%intel
   $ spack build-env mpileaks@1.1%intel ./configure

This will cd to the build directory and then run ``configure`` in the
package's build environment.

.. _cmd-spack-location:

^^^^^^^^^^^^^^^^^^
``spack location``
^^^^^^^^^^^^^^^^^^

``spack location`` is the same as ``spack cd`` but it does not require
shell support.  It simply prints out the path you ask for, rather than
cd'ing to it.  In bash, this:

.. code-block:: console

   $ cd $(spack location --build-dir <spec>)

is the same as:

.. code-block:: console

   $ spack cd --build-dir <spec>

``spack location`` is intended for use in scripts or makefiles that
need to know where packages are installed.  e.g., in a makefile you
might write:

.. code-block:: makefile

   DWARF_PREFIX = $(spack location --install-dir libdwarf)
   CXXFLAGS += -I$DWARF_PREFIX/include
   CXXFLAGS += -L$DWARF_PREFIX/lib

.. _abi_compatibility:

----------------------------
Specifying ABI Compatibility
----------------------------

Packages can include ABI-compatibility information using the
``can_splice`` directive. For example, if ``Foo`` version 1.1 can
always replace version 1.0, then the package could have:

.. code-block:: python

   can_splice("foo@1.0", when="@1.1")

For virtual packages, packages can also specify ABI compatibility with
other packages providing the same virtual. For example, ``zlib-ng``
could specify:

.. code-block:: python

   can_splice("zlib@1.3.1", when="@2.2+compat")

Some packages have ABI-compatibility that is dependent on matching
variant values, either for all variants or for some set of
ABI-relevant variants. In those cases, it is not necessary to specify
the full combinatorial explosion. The ``match_variants`` keyword can
cover all single-value variants.

.. code-block:: python

   can_splice("foo@1.1", when="@1.2", match_variants=["bar"])  # any value for bar as long as they're the same
   can_splice("foo@1.2", when="@1.3", match_variants="*")  # any variant values if all single-value variants match

The concretizer will use ABI compatibility to determine automatic
splices when :ref:`automatic splicing<automatic_splicing>` is enabled.

.. note::

   The ``can_splice`` directive is experimental, and may be replaced
   by a higher-level interface in future versions of Spack.

.. _package_class_structure:

--------------------------
Package class architecture
--------------------------

.. note::

   This section aims to provide a high-level knowledge of how the package class architecture evolved
   in Spack, and provides some insights on the current design.

Packages in Spack were originally designed to support only a single build system. The overall
class structure for a package looked like:

.. image:: images/original_package_architecture.png
   :scale: 60 %
   :align: center

In this architecture the base class ``AutotoolsPackage`` was responsible for both the metadata
related to the ``autotools`` build system (e.g. dependencies or variants common to all packages
using it), and for encoding the default installation procedure.

In reality, a non-negligible number of packages are either changing their build system during the evolution of the
project, or using different build systems for different platforms. An architecture based on a single class
requires hacks or other workarounds to deal with these cases.

To support a model more adherent to reality, Spack v0.19 changed its internal design by extracting
the attributes and methods related to building a software into a separate hierarchy:

.. image:: images/builder_package_architecture.png
   :scale: 60 %
   :align: center

In this new format each ``package.py`` contains one ``*Package`` class that gathers all the metadata,
and one or more ``*Builder`` classes that encode the installation procedure. A specific builder object
is created just before the software is built, so at a time where Spack knows which build system needs
to be used for the current installation, and receives a ``package`` object during initialization.

^^^^^^^^^^^^^^^^^^^^^^^^
``build_system`` variant
^^^^^^^^^^^^^^^^^^^^^^^^

To allow imposing conditions based on the build system, each package must have a ``build_system`` variant,
which is usually inherited from base classes. This variant allows for writing metadata that is conditional
on the build system:

.. code-block:: python

   with when("build_system=cmake"):
       depends_on("cmake", type="build")

and also for selecting a specific build system from a spec literal, like in the following command:

.. code-block:: console

   $ spack install arpack-ng build_system=autotools

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compatibility with single-class format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Internally, Spack always uses builders to perform operations related to the installation of a specific software.
The builders are created in the ``spack.builder.create`` function.

.. literalinclude:: _spack_root/lib/spack/spack/builder.py
   :pyobject: create

To achieve backward compatibility with the single-class format Spack creates in this function a special
"adapter builder", if no custom builder is detected in the recipe:

.. image:: images/adapter.png
   :scale: 60 %
   :align: center

Overall the role of the adapter is to route access to attributes of methods first through the ``*Package``
hierarchy, and then back to the base class builder. This is schematically shown in the diagram above, where
the adapter role is to "emulate" a method resolution order like the one represented by the red arrows.

-----------------
Customizing Views
-----------------

.. note::

   This is advanced functionality that is rarely needed to be customized.

Spack environments manage a view of their packages, which is a single directory
that merges all installed packages through symlinks, so users can easily access them.
The methods of ``PackageViewMixin`` can be overridden to customize how packages are added
to views.
Sometimes it's impossible to get an application to work just through symlinking its executables, and patching is necessary.
For example, Python scripts in a ``bin`` directory may have a shebang that points to the Python interpreter in Python's install prefix, but it's more convenient to have the shebang point to the Python interpreter in the view, since that interpreter is aware of the Python packages in the view (the view is a virtual environment).
As a consequence, Python extension packages (those inheriting from ``PythonPackage``) override ``add_files_to_view`` in order to rewrite shebang lines.

^^^^^^^^^^^^^^^^^
Bundling software
^^^^^^^^^^^^^^^^^

If you have a collection of software expected to work well together with
no source code of its own, you can create a :ref:`BundlePackage <bundlepackage>`.
Examples where bundle packages can be useful include defining suites of
applications (e.g., `EcpProxyApps
<https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/ecp_proxy_apps/package.py>`_), commonly used libraries
(e.g., `AmdAocl <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/amd_aocl/package.py>`_),
and software development kits (e.g., `EcpDataVisSdk <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/ecp_data_vis_sdk/package.py>`_).

These versioned packages primarily consist of dependencies on the associated
software packages. They can include :ref:`variants <variants>` to ensure
common build options are consistently applied to dependencies. Known build
failures, such as not building on a platform or when certain compilers or
variants are used, can be flagged with :ref:`conflicts <packaging_conflicts>`.
Build requirements, such as only building with specific compilers, can similarly
be flagged with :ref:`requires <packaging_conflicts>`.

The ``spack create --template bundle`` command will create a skeleton
``BundlePackage`` ``package.py`` for you:

.. code-block:: console

   $ spack create --template bundle --name coolsdk

Now you can fill in the basic package documentation, version(s), and software
package dependencies along with any other relevant customizations.

.. note::

   Remember that bundle packages have no software of their own so there
   is nothing to download.

.. _handling_rpaths:

---------------
Handling RPATHs
---------------

Spack installs each package in a way that ensures that all of its
dependencies are found when it runs.  It does this using `RPATHs
<http://en.wikipedia.org/wiki/Rpath>`_.  An RPATH is a search
path, stored in a binary (an executable or library), that tells the
dynamic loader where to find its dependencies at runtime. You may be
familiar with `LD_LIBRARY_PATH
<http://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html>`_
on Linux or `DYLD_LIBRARY_PATH
<https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/dyld.3.html>`_
on Mac OS X.  RPATH is similar to these paths, in that it tells
the loader where to find libraries.  Unlike them, it is embedded in
the binary and not set in each user's environment.

RPATHs in Spack are handled in one of three ways:

#. For most packages, RPATHs are handled automatically using Spack's
   :ref:`compiler wrappers <compiler-wrappers>`.  These wrappers are
   set in standard variables like ``CC``, ``CXX``, ``F77``, and ``FC``,
   so most build systems (autotools and many gmake systems) pick them
   up and use them.
#. CMake has its own RPATH handling, and distinguishes between build and
   install RPATHs. By default, during the build it registers RPATHs to
   all libraries it links to, so that just-built executables can be run
   during the build itself. Upon installation, these RPATHs are cleared,
   unless the user defines the install RPATHs. When inheriting from
   ``CMakePackage``, Spack handles this automatically, and sets
   ``CMAKE_INSTALL_RPATH_USE_LINK_PATH`` and ``CMAKE_INSTALL_RPATH``,
   so that libraries of dependencies and the package's own libraries
   can be found at runtime.
#. If you need to modify the build to add your own RPATHs, you can
   use the ``self.rpath`` property of your package, which will
   return a list of all the RPATHs that Spack will use when it
   links.  You can see this how this is used in the :ref:`PySide
   example <pyside-patch>` above.

.. _attribute_parallel:

---------------
Parallel builds
---------------

Spack supports parallel builds on an individual package and at the
installation level.  Package-level parallelism is established by the
``--jobs`` option and its configuration and package recipe equivalents.
Installation-level parallelism is driven by the DAG(s) of the requested
package or packages.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Package-level build parallelism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Spack will invoke ``make()``, or any other similar tool,
with a ``-j <njobs>`` argument, so those builds run in parallel.
The parallelism is determined by the value of the ``build_jobs`` entry
in ``config.yaml`` (see :ref:`here <build-jobs>` for more details on
how this value is computed).

If a package does not build properly in parallel, you can override
this setting by adding ``parallel = False`` to your package.  For
example, OpenSSL's build does not work in parallel, so its package
looks like this:

.. code-block:: python
   :emphasize-lines: 8
   :linenos:

   class Openssl(Package):
       homepage = "http://www.openssl.org"
       url      = "http://www.openssl.org/source/openssl-1.0.1h.tar.gz"

       version("1.0.1h", md5="8d6d684a9430d5cc98a62a5d8fbda8cf")
       depends_on("zlib-api")

       parallel = False

You can also disable parallel builds only for specific make
invocation:

.. code-block:: python
   :emphasize-lines: 5
   :linenos:

   class Libelf(Package):
       ...

       def install(self, spec, prefix):
           make("install", parallel=False)

Note that the ``--jobs`` option works out of the box for all standard
build systems. If you are using a non-standard build system instead, you
can use the variable ``make_jobs`` to extract the number of jobs specified
by the ``--jobs`` option:

.. code-block:: python
   :emphasize-lines: 7, 11
   :linenos:

   class Xios(Package):
      ...
      def install(self, spec, prefix):
         ...
         options = [
            ...
            '--jobs', str(make_jobs),
        ]
        ...
        make_xios = Executable("./make_xios")
        make_xios(*options)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install-level build parallelism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack supports the concurrent installation of packages within a Spack
instance across multiple processes using file system locks.  This
parallelism is separate from the package-level achieved through build
systems' use of the ``-j <njobs>`` option.  With install-level parallelism,
processes coordinate the installation of the dependencies of specs
provided on the command line and as part of an environment build with
only **one process** being allowed to install a given package at a time.
Refer to :ref:`Dependencies` for more information on dependencies and
:ref:`installing-environment` for how to install an environment.

Concurrent processes may be any combination of interactive sessions and
batch jobs.  This means a ``spack install`` can be running in a terminal
window while a batch job is running ``spack install`` on the same or
overlapping dependencies without any process trying to re-do the work of
another.

For example, if you are using Slurm, you could launch an installation
of ``mpich`` using the following command:

.. code-block:: console

   $ srun -N 2 -n 8 spack install -j 4 mpich@3.3.2

This will create eight concurrent, four-job installs on two different
nodes.

Alternatively, you could run the same installs on one node by entering
the following at the command line of a bash shell:

.. code-block:: console

   $ for i in {1..12}; do nohup spack install -j 4 mpich@3.3.2 >> mpich_install.txt 2>&1 & done

.. note::

   The effective parallelism is based on the maximum number of packages
   that can be installed at the same time, which is limited by the
   number of packages with no (remaining) uninstalled dependencies.

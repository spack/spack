.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _multiplepackage:

----------------------
Multiple Build Systems
----------------------

Quite frequently, a package will change build systems from one version to the
next. For example, a small project that once used a single Makefile to build
may now require Autotools to handle the increased number of files that need to
be compiled. Or, a package that once used Autotools may switch to CMake for
Windows support. In this case, it becomes a bit more challenging to write a
single build recipe for this package in Spack.

There are several ways that this can be handled in Spack:

#. Subclass the new build system, and override phases as needed (preferred)
#. Subclass ``Package`` and implement ``install`` as needed
#. Create separate ``*-cmake``, ``*-autotools``, etc. packages for each build system
#. Rename the old package to ``*-legacy`` and create a new package
#. Move the old package to a ``legacy`` repository and create a new package
#. Drop older versions that only support the older build system

Of these options, 1 is preferred, and will be demonstrated in this
documentation. Options 3-5 have issues with concretization, so shouldn't be
used. Options 4-5 also don't support more than two build systems. Option 6 only
works if the old versions are no longer needed. Option 1 is preferred over 2
because it makes it easier to drop the old build system entirely.

The exact syntax of the package depends on which build systems you need to
support. Below are a couple of common examples.

^^^^^^^^^^^^^^^^^^^^^
Makefile -> Autotools
^^^^^^^^^^^^^^^^^^^^^

Let's say we have the following package:

.. code-block:: python

   class Foo(MakefilePackage):
       version("1.2.0", sha256="...")

       def edit(self, spec, prefix):
           filter_file("CC=", "CC=" + spack_cc, "Makefile")

       def install(self, spec, prefix):
           install_tree(".", prefix)


The package subclasses from :ref:`makefilepackage`, which has three phases:

#. ``edit`` (does nothing by default)
#. ``build`` (runs ``make`` by default)
#. ``install`` (runs ``make install`` by default)

In this case, the ``install`` phase needed to be overridden because the
Makefile did not have an install target. We also modify the Makefile to use
Spack's compiler wrappers. The default ``build`` phase is not changed.

Starting with version 1.3.0, we want to use Autotools to build instead.
:ref:`autotoolspackage` has four phases:

#. ``autoreconf`` (does not if a configure script already exists)
#. ``configure`` (runs ``./configure --prefix=...`` by default)
#. ``build`` (runs ``make`` by default)
#. ``install`` (runs ``make install`` by default)

If the only version we need to support is 1.3.0, the package would look as
simple as:

.. code-block:: python

   class Foo(AutotoolsPackage):
       version("1.3.0", sha256="...")

       def configure_args(self):
           return ["--enable-shared"]


In this case, we use the default methods for each phase and only override
``configure_args`` to specify additional flags to pass to ``./configure``.

If we wanted to write a single package that supports both versions 1.2.0 and
1.3.0, it would look something like:

.. code-block:: python

   class Foo(AutotoolsPackage):
       version("1.3.0", sha256="...")
       version("1.2.0", sha256="...", deprecated=True)

       def configure_args(self):
           return ["--enable-shared"]

       # Remove the following once version 1.2.0 is dropped
       @when("@:1.2")
       def patch(self):
           filter_file("CC=", "CC=" + spack_cc, "Makefile")

       @when("@:1.2")
       def autoreconf(self, spec, prefix):
           pass

       @when("@:1.2")
       def configure(self, spec, prefix):
           pass

       @when("@:1.2")
       def install(self, spec, prefix):
           install_tree(".", prefix)


There are a few interesting things to note here:

* We added ``deprecated=True`` to version 1.2.0. This signifies that version
  1.2.0 is deprecated and shouldn't be used. However, if a user still relies
  on version 1.2.0, it's still there and builds just fine.
* We moved the contents of the ``edit`` phase to the ``patch`` function. Since
  ``AutotoolsPackage`` doesn't have an ``edit`` phase, the only way for this
  step to be executed is to move it to the ``patch`` function, which always
  gets run.
* The ``autoreconf`` and ``configure`` phases become no-ops. Since the old
  Makefile-based build system doesn't use these, we ignore these phases when
  building ``foo@1.2.0``.
* The ``@when`` decorator is used to override these phases only for older
  versions. The default methods are used for ``foo@1.3:``.

Once a new Spack release comes out, version 1.2.0 and everything below the
comment can be safely deleted. The result is the same as if we had written a
package for version 1.3.0 from scratch.

^^^^^^^^^^^^^^^^^^
Autotools -> CMake
^^^^^^^^^^^^^^^^^^

Let's say we have the following package:

.. code-block:: python

   class Bar(AutotoolsPackage):
       version("1.2.0", sha256="...")

       def configure_args(self):
           return ["--enable-shared"]


The package subclasses from :ref:`autotoolspackage`, which has four phases:

#. ``autoreconf`` (does not if a configure script already exists)
#. ``configure`` (runs ``./configure --prefix=...`` by default)
#. ``build`` (runs ``make`` by default)
#. ``install`` (runs ``make install`` by default)

In this case, we use the default methods for each phase and only override
``configure_args`` to specify additional flags to pass to ``./configure``.

Starting with version 1.3.0, we want to use CMake to build instead.
:ref:`cmakepackage` has three phases:

#. ``cmake`` (runs ``cmake ...`` by default)
#. ``build`` (runs ``make`` by default)
#. ``install`` (runs ``make install`` by default)

If the only version we need to support is 1.3.0, the package would look as
simple as:

.. code-block:: python

   class Bar(CMakePackage):
       version("1.3.0", sha256="...")

       def cmake_args(self):
           return [self.define("BUILD_SHARED_LIBS", True)]


In this case, we use the default methods for each phase and only override
``cmake_args`` to specify additional flags to pass to ``cmake``.

If we wanted to write a single package that supports both versions 1.2.0 and
1.3.0, it would look something like:

.. code-block:: python

   class Bar(CMakePackage):
       version("1.3.0", sha256="...")
       version("1.2.0", sha256="...", deprecated=True)

       def cmake_args(self):
           return [self.define("BUILD_SHARED_LIBS", True)]

       # Remove the following once version 1.2.0 is dropped
       def configure_args(self):
           return ["--enable-shared"]

       @when("@:1.2")
       def cmake(self, spec, prefix):
           configure("--prefix=" + prefix, *self.configure_args())


There are a few interesting things to note here:

* We added ``deprecated=True`` to version 1.2.0. This signifies that version
  1.2.0 is deprecated and shouldn't be used. However, if a user still relies
  on version 1.2.0, it's still there and builds just fine.
* Since CMake and Autotools are so similar, we only need to override the
  ``cmake`` phase, we can use the default ``build`` and ``install`` phases.
* We override ``cmake`` to run ``./configure`` for older versions.
  ``configure_args`` remains the same.
* The ``@when`` decorator is used to override these phases only for older
  versions. The default methods are used for ``bar@1.3:``.

Once a new Spack release comes out, version 1.2.0 and everything below the
comment can be safely deleted. The result is the same as if we had written a
package for version 1.3.0 from scratch.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Multiple build systems for the same version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

During the transition from one build system to another, developers often
support multiple build systems at the same time. Spack can only use a single
build system for a single version. To decide which build system to use for a
particular version, take the following things into account:

1. If the developers explicitly state that one build system is preferred over
   another, use that one.
2. If one build system is considered "experimental" while another is considered
   "stable", use the stable build system.
3. Otherwise, use the newer build system.

The developer preference for which build system to use can change over time as
a newer build system becomes stable/recommended.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Dropping support for old build systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When older versions of a package don't support a newer build system, it can be
tempting to simply delete them from a package. This significantly reduces
package complexity and makes the build recipe much easier to maintain. However,
other packages or Spack users may rely on these older versions. The recommended
approach is to first support both build systems (as demonstrated above),
:ref:`deprecate <deprecate>` versions that rely on the old build system, and
remove those versions and any phases that needed to be overridden in the next
Spack release.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Three or more build systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In rare cases, a package may change build systems multiple times. For example,
a package may start with Makefiles, then switch to Autotools, then switch to
CMake. The same logic used above can be extended to any number of build systems.
For example:

.. code-block:: python

   class Baz(CMakePackage):
       version("1.4.0", sha256="...")  # CMake
       version("1.3.0", sha256="...")  # Autotools
       version("1.2.0", sha256="...")  # Makefile

       def cmake_args(self):
           return [self.define("BUILD_SHARED_LIBS", True)]

       # Remove the following once version 1.3.0 is dropped
       def configure_args(self):
           return ["--enable-shared"]

       @when("@1.3")
       def cmake(self, spec, prefix):
           configure("--prefix=" + prefix, *self.configure_args())

       # Remove the following once version 1.2.0 is dropped
       @when("@:1.2")
       def patch(self):
           filter_file("CC=", "CC=" + spack_cc, "Makefile")

       @when("@:1.2")
       def cmake(self, spec, prefix):
           pass

       @when("@:1.2")
       def install(self, spec, prefix):
           install_tree(".", prefix)


^^^^^^^^^^^^^^^^^^^
Additional examples
^^^^^^^^^^^^^^^^^^^

When writing new packages, it often helps to see examples of existing packages.
Here is an incomplete list of existing Spack packages that have changed build
systems before:

================  =====================  ================
Package           Previous Build System  New Build System
================  =====================  ================
amber             custom                 CMake
arpack-ng         Autotools              CMake
atk               Autotools              Meson
blast             None                   Autotools
dyninst           Autotools              CMake
evtgen            Autotools              CMake
fish              Autotools              CMake
gdk-pixbuf        Autotools              Meson
glib              Autotools              Meson
glog              Autotools              CMake
gmt               Autotools              CMake
gtkplus           Autotools              Meson
hpl               Makefile               Autotools
interproscan      Perl                   Maven
jasper            Autotools              CMake
kahip             SCons                  CMake
kokkos            Makefile               CMake
kokkos-kernels    Makefile               CMake
leveldb           Makefile               CMake
libdrm            Autotools              Meson
libjpeg-turbo     Autotools              CMake
mesa              Autotools              Meson
metis             None                   CMake
mpifileutils      Autotools              CMake
muparser          Autotools              CMake
mxnet             Makefile               CMake
nest              Autotools              CMake
neuron            Autotools              CMake
nsimd             CMake                  nsconfig
opennurbs         Makefile               CMake
optional-lite     None                   CMake
plasma            Makefile               CMake
preseq            Makefile               Autotools
protobuf          Autotools              CMake
py-pygobject      Autotools              Python
singularity       Autotools              Makefile
span-lite         None                   CMake
ssht              Makefile               CMake
string-view-lite  None                   CMake
superlu           Makefile               CMake
superlu-dist      Makefile               CMake
uncrustify        Autotools              CMake
================  =====================  ================

Packages that support multiple build systems can be a bit confusing to write.
Don't hesitate to open an issue or draft pull request and ask for advice from
other Spack developers!

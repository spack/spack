.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _cheatsheet:


Spack (packaging) cheat sheet
=============================

-  How to change filename extension for source archive:


   .. code:: python

        def url_for_version(self, version):
            url = self.url.rsplit("/", 1)[0]
            if version >= Version("0.2.3"):
                url += "/pathos-{0}.tar.gz"
            else:
                url += "/pathos-{0}.zip"

            url = url.format(version)
            return url

   -  Alternatively, pass ``extension=`` kwarg to ``version(...)`` - this is an unexpected side-effect and can break when Spack updates


-  Some Python packages require ``setuptools`` in runtime - one can
   ``grep`` the installed package for ``setuptools`` and
   ``pkg_resources``
-  Check if package is taken from system: ``self.spec[...].external``
-  Copy additional file to build area:

.. code:: python

   @run_before("configure")
   def copy_gsl_m4(self):
       if self.spec.satisfies("@2.6.2:"):
           copy(join_path(os.path.dirname(__file__), "gsl.m4"), "m4/gsl.m4")

-  Manual installation of some files:

.. code:: python

   install(
       join_path(self.stage.source_path,
           "Contrib", "AlpGen", "AlpGenHandler.so"),
       join_path(prefix.lib, "Herwig++", "AlpGenHandler.so"))

-  Full manual installation:

.. code:: python

   def install(self, spec, prefix):
       def install_dir(dirname):
           install_tree(dirname, join_path(prefix, dirname))

       install_dir("bin")
       install_dir("etc")
       install_dir("include")
       install_dir("lib")
       install_dir("libexec")
       install_dir("sbin")
       install_dir("share")

   # Or just
   def install(self, spec, prefix):
       install_tree(".", prefix)

-  Run code after unpacking but before patching (e.g. flatten the
   directory structure):

.. code:: python

   def do_stage(self, mirror_only=False):
       super(Charybdis, self).do_stage(mirror_only)
       dn = os.listdir(self.stage.source_path)[0]
       for fn in os.listdir(join_path(self.stage.source_path, dn)):
           shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
       shutil.rmtree(join_path(self.stage.source_path, dn))

-  Common signatures:

.. code:: python

   def edit(self, spec, prefix):
       pass

   def patch(self):
       pass

   @run_before()
   def foo(self):
       pass

   @run_after()
   def bar(self):
       pass

   def setup_build_environment(self, env):
       pass

-  Common paths

.. code:: python

   self.stage.source_path # this is where the source code is
   self.stage.path # this is one directory up - i.e. common staging area

-  If Spack complains about patch hash, do ``spack clean -m``
-  (Recommended) way to control which libraries (shared or static) are
   built in autotools-based packages:a

.. code:: python

       variant("libs", default="shared,static", values=("shared", "static"),
               multi=True, description="Build shared libs, static libs or both")
       # ...
       def configure_args(self):
           args += self.enable_or_disable("libs")

-  Setting ``PYTHON_LIBRARY`` and ``PYTHON_INCLUDE_DIR`` (not a generic
   way, the dependency needs to define ``def libs`` and
   ``def headers``):

.. code:: python

       self.define("PYTHON_LIBRARY", self.spec["python"].libs[0]),
       self.define("PYTHON_INCLUDE_DIR", self.spec["python"].headers.directories[0])

-  Passing ``CFLAGS`` etc to AutotoolsPackage (or CMakePackage, or a few
   other high level build systems that support that):

.. code:: python

       def flag_handler(self, name, flags):
           flags = list(flags)
           if name == "cxxflags":
               flags.append("-std=c++" + self.spec.variants["cxxstd"].value)

           return (None, None, flags)

Multi-buildsystem (since Spack v0.19.0)
---------------------------------------

How-to multi-buildsystem: 

1. Use new ``build_system`` directive:

.. code:: python

       build_system(
           conditional("autotools", when=:1.5.3"),
           conditional("cmake", when="@1.5.90:"),
           default="cmake",
       )

2. Add buildsystem dependencies:

.. code:: python

       with when("build_system=autotools"):
           depends_on("autoconf", type="build")
           depends_on("automake", type="build")
           depends_on("libtool", type="build")

       with when("build_system=cmake"):
           depends_on("cmake", type="build", when="@1.5.90:")

3. (optional) Customize build:

.. code:: python

   class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
       def cmake_args(self):
           args = [
               self.define_from_variant("ENABLE_SHARED", "shared"),
               self.define_from_variant("ENABLE_STATIC", "static"),
               self.define_from_variant("WITH_JPEG8", "jpeg8"),
           ]

           return args


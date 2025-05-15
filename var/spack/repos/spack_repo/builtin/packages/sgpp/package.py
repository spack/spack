# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems.python import PythonPipBuilder
from spack_repo.builtin.build_systems.scons import SConsPackage

from spack.package import *

from ..boost.package import Boost


class Sgpp(SConsPackage):
    """SGpp is a library and framework for sparse grids in different flavors.
    SGpp supports both hierarchical spatially-adaptive sparse grids and the
    dimensionally-adaptive sparse grid combination technique."""

    homepage = "https://sgpp.sparsegrids.org"
    url = "https://github.com/SGpp/SGpp/archive/v3.2.0.tar.gz"
    git = "https://github.com/SGpp/SGpp.git"

    maintainers("G-071", "leiterrl", "pfluegdk")

    version("master", branch="master")
    version("3.4.0", sha256="450d4002850b0a48c561abe221b634261ca44eee111ca605c3e80797182f40b3")
    version("3.3.0", sha256="ca4d5b79f315b425ce69b04940c141451a76848bf1bd7b96067217304c68e2d4")
    version("3.2.0", sha256="dab83587fd447f92ed8546eacaac6b8cbe65b8db5e860218c0fa2e42f776962d")

    # Note: Older versions of SGpp required Python 2 (and offered Python 2 bindings) and have
    # thus been removed from this list as Spack now requires Python 3.
    # The last spack release with support for Python 2 is v0.19 - there, the spack package
    # still supports SGpp versions 3.1.0 and 3.0.0 if required.

    # Patches with bugfixes that are necessary to build old SGpp versions
    # with spack. Patches are submitted upstream, but need to applied
    # for versions too old to include them as they will not be
    # backported for old releases:

    # Patch that ensures libraries will actually
    # be copied into prefix/lib upon installation
    # (otherwise it would be prefix/lib/sgpp)
    # Fixed in SGpp in PR https://github.com/SGpp/SGpp/pull/222
    patch("directory.patch", when="@1.0.0:3.2.0")
    # Fix faulty setup.py introduced in 3.2.0
    # Fixed in SGpp in version 3.3.0
    patch("fix-setup-py.patch", when="@3.2.0")
    # Fix compilation issue with opencl introduced in 3.2.0
    # Fixed in SGpp in PR https://github.com/SGpp/SGpp/pull/219
    patch("ocl.patch", when="@3.2.0+opencl")
    # Fixes compilation with AVX512 and datadriven
    # Fixed in SGpp in PR https://github.com/SGpp/SGpp/pull/229
    patch("avx512_datadriven_compilation.patch", when="@:3.3.0+datadriven")
    # The distutils deprecation warning in python 3.10/3.11 caused the sgpp build system
    # to complain about missing headers (due to a path check not working anymore)
    # See issue https://github.com/SGpp/SGpp/issues/263 and https://github.com/SGpp/SGpp/pull/266
    patch("disable_disutils_deprecation_warning.patch", when="@:3.4.0 ^python@3.10:3.11")
    # SGpp does not contain aarch64 support as of 3.4.0. To make it work still, this patch adds
    # simple build system support for it.
    patch("for_aarch64.patch", when="@:3.4.0 target=aarch64:")
    # SGpp will default to the system paths when linking boost without the patch
    # This may work (depending on the boost versions in question) but we should use the boost
    # from spack. This patch allows to correctly pass the spack's boost path to SGpp
    # Fixed in SGpp PR https://github.com/SGpp/SGpp/pull/273
    patch("set_boost_lib_path_internally.patch", when="@3.3.0:3.4.0")

    variant("debug", default=False, description="Build debug version instead of release version")
    variant(
        "doc",
        default=False,
        description="Build sgpp documentation (doxygen / pydoc)",
        when="@3.4.0:",
    )
    variant("python", default=True, description="Provide Python bindings for SGpp")
    variant("optimization", default=True, description="Builds the optimization module of SGpp")
    variant("pde", default=True, description="Builds the datadriven module of SGpp")
    variant("quadrature", default=True, description="Builds the datadriven module of SGpp")
    variant("datadriven", default=False, description="Builds the datadriven module of SGpp")
    variant("misc", default=False, description="Builds the misc module of SGpp")
    variant("combigrid", default=False, description="Builds the combigrid module of SGpp")
    variant("solver", default=True, description="Builds the solver module of SGpp")
    variant(
        "opencl", default=False, description="Enables support for OpenCL accelerated operations"
    )
    variant("mpi", default=False, description="Enables support for MPI-distributed operations")
    variant(
        "eigen", default=False, description="Enables Eigen support", when="@3.4.0: +optimization"
    )
    variant(
        "dakota", default=False, description="Enables Dakota support", when="@3.4.0: +combigrid"
    )
    variant(
        "visualization",
        default=False,
        description="Build with visualization support",
        when="+python",
    )

    # Mandatory dependencies
    depends_on("cxx", type="build")  # generated
    depends_on("scons@3:", type="build")
    depends_on("zlib-api", type="link")
    depends_on("doxygen+graphviz", when="+doc", type="build")
    depends_on("eigen", when="+eigen", type=("build", "run"))
    depends_on("dakota", when="+dakota", type=("build", "run"))
    # Python dependencies
    extends("python", when="+python")
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("swig@3:", when="+python", type="build")
    depends_on("py-numpy@1.17:", when="+python", type=("build", "run"))
    depends_on("py-pandas@1.1:", when="+python+visualization", type=("build", "run"))
    depends_on("py-matplotlib@3:", when="+python+visualization", type=("build", "run"))
    depends_on("py-scipy@1.5:", when="+python", type=("build", "run"))
    # OpenCL dependency
    depends_on("opencl@1.1:", when="+opencl", type=("build", "run"))
    # MPI dependency
    depends_on("mpi", when="+mpi", type=("build", "run"))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=("build", "run", "test"))

    # Compiler with C++11 support is required
    conflicts("%gcc@:4.8.4", msg="Compiler with c++11 support is required!")
    conflicts("%apple-clang@:3.9", msg="Compiler with c++11 support is required!")
    conflicts("%clang@:3.2", msg="Compiler with c++11 support is required!")
    conflicts("%intel@:14", msg="Compiler with c++11 support is required!")
    # Solver python bindings are actually using the pde module at one point:
    conflicts("-pde", when="+python+solver")
    # some modules depend on each other (notably datadriven and misc)
    conflicts("+pde", when="-solver")
    # Datadriven module requirements
    conflicts("+datadriven", when="-solver")
    conflicts("+datadriven", when="-optimization")
    conflicts("+datadriven", when="-pde")
    # Misc module requirements
    conflicts("+misc", when="-datadriven")
    conflicts("+misc", when="-solver")
    conflicts("+misc", when="-optimization")
    conflicts("+misc", when="-pde")
    # Combigrid module requirements (for 3.2.0 or older)
    # newer combigrids have no dependencies
    conflicts("+combigrid", when="@1.0.0:3.2.0~optimization")
    conflicts("+combigrid", when="@1.0.0:3.2.0~pde")
    conflicts("+combigrid", when="@1.0.0:3.2.0~solver")
    conflicts("+combigrid", when="@1.0.0:3.2.0~quadrature")
    # Conflicts due the changes in the respective frameworks
    # Fixed in newer SGpp versions, but 3.4.0 or older versions do not work
    conflicts("^python@3.12:", when="@:3.4.0+python")
    conflicts("^py-numpy@2:", when="@:3.4.0+python")
    conflicts("^py-pandas@1.4:", when="@:3.4.0+python")
    conflicts("^py-matplotlib@3.6:", when="@:3.4.0+python")
    conflicts("^swig@4.1:", when="@:3.4.0+python")

    def build_args(self, spec, prefix):
        # Testing parameters
        if self.run_tests:
            self.args = [
                "COMPILE_BOOST_TESTS=1",
                "RUN_BOOST_TESTS=1",
                "COMPILE_BOOST_PERFORMANCE_TESTS=1",
                "RUN_BOOST_PERFORMANCE_TESTS=1",
            ]
            if "+python" in spec:
                self.args.append("RUN_PYTHON_TESTS=1")
                if spec.satisfies("@3.3.0:"):
                    self.args.append("RUN_PYTHON_EXAMPLES=1")
            if spec.satisfies("@1.0.0:3.2.0"):  # argument was renamed after 3.2.0
                self.args.append("RUN_CPPLINT=1")
            else:
                self.args.append("RUN_CPP_EXAMPLES=1")
                self.args.append("CHECK_STYLE=1")
        else:
            self.args = [
                "COMPILE_BOOST_TESTS=0",
                "RUN_BOOST_TESTS=0",
                "COMPILE_BOOST_PERFORMANCE_TESTS=0",
                "RUN_BOOST_PERFORMANCE_TESTS=0",
                "RUN_PYTHON_TESTS=0",
            ]
            if spec.satisfies("@1.0.0:3.2.0"):  # argument was renamed after 3.2.0
                self.args.append("RUN_CPPLINT=0")
            else:
                self.args.append("RUN_PYTHON_EXAMPLES=0")
                self.args.append("RUN_CPP_EXAMPLES=0")
                self.args.append("CHECK_STYLE=0")

        # Debug build or not
        self.args.append("OPT={0}".format("0" if "+debug" in spec else "1"))

        # Install direction
        self.args.append("PREFIX={0}".format(prefix))

        # Generate swig bindings?
        self.args.append("SG_PYTHON={0}".format("1" if "+python" in spec else "0"))

        # Java bindings are now deprecated within SGpp
        self.args.append("SG_JAVA=0")

        # Which modules to build?
        self.args.append("SG_OPTIMIZATION={0}".format("1" if "+optimization" in spec else "0"))
        self.args.append("SG_QUADRATURE={0}".format("1" if "+quadrature" in spec else "0"))
        self.args.append("SG_PDE={0}".format("1" if "+pde" in spec else "0"))
        self.args.append("SG_DATADRIVEN={0}".format("1" if "+datadriven" in spec else "0"))
        self.args.append("SG_COMBIGRID={0}".format("1" if "+combigrid" in spec else "0"))
        self.args.append("SG_SOLVER={0}".format("1" if "+solver" in spec else "0"))
        self.args.append("SG_MISC={0}".format("1" if "+misc" in spec else "0"))

        # SIMD scons parameter (pick according to simd spec)
        if "avx512" in self.spec.target:
            self.args.append("ARCH=avx512")
        elif "avx2" in self.spec.target:
            self.args.append("ARCH=avx2")
        elif "avx" in self.spec.target:
            self.args.append("ARCH=avx")
        elif "fma4" in self.spec.target:
            self.args.append("ARCH=fma4")
        elif "sse42" in self.spec.target:
            self.args.append("ARCH=sse42")
        elif "sse3" in self.spec.target:
            self.args.append("ARCH=sse3")
        elif "target=aarch64:" in spec:
            self.args.append("ARCH=aarch64")

        # OpenCL Flags
        self.args.append("USE_OCL={0}".format("1" if "+opencl" in spec else "0"))

        # Get the mpicxx compiler from the Spack spec
        # (makes certain we use the one from spack):
        if "+mpi" in spec:
            self.args.append("CXX={0}".format(self.spec["mpi"].mpicxx))
        else:
            self.args.append("CXX={0}".format(self.compiler.cxx))

        # Include PYDOC when building the documentation
        self.args.append("PYDOC={0}".format("1" if "+doc +python" in spec else "0"))

        # For some libraries, SGpp expects the path to be explicitly passed to scons (either using
        # CPPPATH and LIBPATH or using depency-specific variables (BOOST_LIBRARY_PATH).
        # Here, we set those paths and associated flags the dependencies where SGpp expects them
        # to be passed manually via CPPPATH/LIBPATH (Eigen, Dakota, ...):
        custom_cpppath = ""
        custom_libpath = ""
        path_separator = ";" if sys.platform == "win32" else ":"
        if "+eigen" in spec:
            self.args.append("USE_EIGEN=1")
            custom_cpppath += "{0}{1}".format(self.spec["eigen"].prefix.include, path_separator)
        if "+dakota" in spec:
            self.args.append("USE_DAKOTA=1")
            custom_cpppath += "{0}{1}".format(self.spec["dakota"].prefix.include, path_separator)
            # Simply using spec["dakota"].libs.directories[0] does not work because spack will look
            # for a libdakota library file which does not exist. However, we can use find_libraries
            # and manually specify an existing library
            # name within dakota to find the correct lib directory:
            custom_libpath += "{0}{1}".format(
                find_libraries(
                    "libdakota_src", root=self.spec["dakota"].prefix, shared=True, recursive=True
                ).directories[0],
                path_separator,
            )
        # Add combined paths to CPPPATH/LIBPATH
        if custom_cpppath:
            self.args.append("CPPPATH={0}".format(custom_cpppath))
        if custom_libpath:
            self.args.append("LIBPATH={0}".format(custom_libpath))
        # Manually set Boost location to the spack one (otherwise SGpp will try to look for
        # Boost within the System install directory first)
        self.args.append("BOOST_INCLUDE_PATH={0}".format(self.spec["boost"].prefix.include))
        self.args.append("BOOST_LIBRARY_PATH={0}".format(self.spec["boost"].libs.directories[0]))

        # Parallel builds do not seem to work without this:
        self.args.append("-j{0}".format(make_jobs))

        return self.args

    @run_after("build")
    def build_docs(self):
        # Run Doxygen Step after build but before install
        if "+doc" in self.spec:
            args = self.args
            scons("doxygen", *args)

    def install_args(self, spec, prefix):
        # SGpp expects the same args for the install and build commands
        return self.args

    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
        # Install docs
        if "+doc" in self.spec:
            install_tree("doc", self.prefix.doc)

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nmodl(CMakePackage):
    """Code Generation Framework For NEURON MODeling Language"""

    homepage = "https://github.com/BlueBrain/nmodl.git"
    url = "https://github.com/BlueBrain/nmodl.git"
    git = "https://github.com/BlueBrain/nmodl.git"

    version("develop", branch="master", submodules=True)
    version("llvm", branch="llvm", submodules=True)
    version("0.7.a3", commit="2fb037e1f8d60d522ba16bd968c69a318ce5a827")
    version("0.7.a2", commit="6f6db3b6f25e066db46d8a5fc85a1697363b995c")
    version("0.7.a1", commit="2ce4a2b91dfcfe6356b6a5003c4e99b8711564ee")
    version("0.6.0", tag="0.6")
    version("0.5.0", tag="0.5")
    version("0.4.0", tag="0.4")

    variant("legacy-unit", default=False, description="Enable legacy units")
    variant("python", default=False, description="Enable python bindings")
    variant("llvm", default=False, description="Enable llvm codegen")
    variant("llvm_cuda", default=False, description="Enable llvm codegen with CUDA backend")

    # Build with `ninja` instead of `make`
    generator("ninja")
    depends_on("ninja", type="build")
    depends_on("llvm", when="+llvm")
    depends_on("cuda", when="+llvm_cuda")

    depends_on("bison@3.0.5:", type="build")
    depends_on("catch2@2", when="@:0.6.1")
    depends_on("catch2@3:", when="@0.6.1:")
    depends_on("cli11")
    depends_on("cmake@3.17.0:", type="build")
    depends_on("flex@2.6:", type="build")
    # Need +pic when building Python bindings as in that case we link fmt into a shared
    # library
    depends_on("fmt", when="~python")
    depends_on("fmt+pic", when="+python")
    depends_on("fmt@8.0:8", when="@:0.4 ~python")
    depends_on("fmt+pic@8.0:8", when="@:0.4 +python")
    depends_on("fmt@8:", when="@0.5: ~python")
    depends_on("fmt+pic@8:", when="@0.5: +python")
    depends_on("nlohmann-json")
    depends_on("python@3.6.0:")
    depends_on("py-jinja2@2.10:", type=("build", "run"))
    depends_on("py-pybind11", type=("build", "link", "run"))
    depends_on("py-pytest@4.0.0:", type=("build", "run"))
    depends_on("py-sympy@1.3:", type=("build", "run"))
    depends_on("py-pyyaml@3.13:", type=("build", "run"))
    depends_on("spdlog")
    depends_on("py-find-libpython", type=("run",))

    def cmake_args(self):
        # Do not use the cli11, fmt, pybind11 and spdlog submodule, use the one from
        # the Spack dependency graph.
        options = [
            "-DNMODL_3RDPARTY_USE_CATCH2=OFF",
            "-DNMODL_3RDPARTY_USE_CLI11=OFF",
            "-DNMODL_3RDPARTY_USE_FMT=OFF",
            "-DNMODL_3RDPARTY_USE_JSON=OFF",
            "-DNMODL_3RDPARTY_USE_PYBIND11=OFF",
            "-DNMODL_3RDPARTY_USE_SPDLOG=OFF",
            # This recipe is used in CI pipelines that run the tests directly from
            # the build directory and not via Spack's --test=X option. Setting this
            # aims to override the implicit CMake argument that Spack injects.
            self.define("BUILD_TESTING", True),
            self.define("PYTHON_EXECUTABLE", python.command),
            self.define_from_variant("NMODL_ENABLE_PYTHON_BINDINGS", "python"),
            self.define_from_variant("NMODL_ENABLE_LEGACY_UNITS", "legacy-unit"),
            self.define_from_variant("NMODL_ENABLE_LLVM", "llvm"),
            self.define_from_variant("NMODL_ENABLE_LLVM_CUDA", "llvm_cuda"),
        ]
        return options

    def setup_build_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.lib)

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.lib)

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
    version("0.5.c", commit="c3b0736")
    version("0.5.b", commit="243453d")
    version("0.5.a", commit="94cba1c")
    version("0.4.0", tag="0.4")

    variant("legacy-unit", default=True, description="Enable legacy units")
    variant("python", default=False, description="Enable python bindings")
    variant("llvm", default=False, description="Enable llvm codegen")
    variant(
        "llvm_cuda", default=False, description="Enable llvm codegen with CUDA backend"
    )

    # Build with `ninja` instead of `make`
    generator = "Ninja"
    depends_on("ninja", type="build")
    depends_on("llvm", when="+llvm")
    depends_on("cuda", when="+llvm_cuda")

    depends_on("bison@3.0.5:", type="build")
    depends_on("catch2@2")
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

    def cmake_args(self):
        spec = self.spec

        # Do not use the cli11, fmt, pybind11 and spdlog submodule, use the one from
        # the Spack dependency graph.
        options = [
            "-DNMODL_3RDPARTY_USE_CATCH2=OFF",
            "-DNMODL_3RDPARTY_USE_CLI11=OFF",
            "-DNMODL_3RDPARTY_USE_FMT=OFF",
            "-DNMODL_3RDPARTY_USE_JSON=OFF",
            "-DNMODL_3RDPARTY_USE_PYBIND11=OFF",
            "-DNMODL_3RDPARTY_USE_SPDLOG=OFF",
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

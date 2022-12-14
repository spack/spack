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

    # 0.3.1 > 0.3.0.20220110 > 0.3.0 > 0.3b > 0.3 to Spack
    version("develop", branch="master", submodules=True)
    version("llvm", branch="llvm", submodules=True)
    version("0.5.a", commit="94cba1c")
    version("0.4.0", tag="0.4")
    # This is the merge commit of #875, which allows catch2 etc. to be dependencies
    version("0.3.0.20220531", commit="d63a061ee01b1fd6b14971644bb7fa3efeee20b0")
    # For deployment; nmodl@0.3.0%nvhpc@21.11 doesn't build with eigen/intrinsics errors
    version("0.3.0.20220110", commit="9e0a6f260ac2e6fad068a39ea3bdf7aa7a6f4ee0")
    version("0.3.0", tag="0.3")
    version("0.3b", commit="c30ea06", submodules=True)
    version("0.3a", commit="86fc52d", submodules=True)
    version("0.2", tag="0.2", submodules=True)

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

    conflicts(
        "+llvm",
        when="@0.2:0.3.0.20220531",
        msg="cannot enable LLVM backend outside of llvm version",
    )
    conflicts(
        "+llvm_cuda",
        when="@0.2:0.3.0.20220531",
        msg="cannot enable CUDA LLVM backend outside of llvm version",
    )

    # 0.3b includes #270 and #318 so should work with bison 3.6+
    depends_on("bison@3.0:3.4.99", when="@:0.3a", type="build")
    depends_on("bison@3.0.5:", when="@0.3b:", type="build")
    depends_on("catch2@2", when="@0.3.0.20220531:")
    depends_on("cli11", when="@0.3.0.20220531:")
    depends_on("cmake@3.17.0:", when="@llvm", type="build")
    depends_on("cmake@3.15.0:", when="@0.3.0.20220110:", type="build")
    depends_on("cmake@3.3.0:", when="@:0.3", type="build")
    depends_on("flex@2.6:", type="build")
    # Need +pic when building Python bindings as in that case we link fmt into a shared
    # library
    depends_on("fmt", when="@0.3.0.20220531: ~python")
    depends_on("fmt+pic", when="@0.3.0.20220531: +python")
    depends_on("nlohmann-json", when="@0.3.0.20220531:")
    depends_on("python@3.6.0:")
    depends_on("py-jinja2@2.10:")
    depends_on("py-pybind11", when="@0.3.0.20220531:")
    depends_on("py-pytest@4.0.0:")
    depends_on("py-sympy@1.3:")
    depends_on("py-pyyaml@3.13:")
    depends_on("spdlog", when="@0.3.0.20220531:")

    def cmake_args(self):
        spec = self.spec
        options = []

        if spec.satisfies("@0.3.0.20220531:"):
            # Do not use the cli11, fmt, pybind11 and spdlog submodule, use the one from
            # the Spack dependency graph.
            options += [
                "-DNMODL_3RDPARTY_USE_CATCH2=OFF",
                "-DNMODL_3RDPARTY_USE_CLI11=OFF",
                "-DNMODL_3RDPARTY_USE_FMT=OFF",
                "-DNMODL_3RDPARTY_USE_JSON=OFF",
                "-DNMODL_3RDPARTY_USE_PYBIND11=OFF",
                "-DNMODL_3RDPARTY_USE_SPDLOG=OFF",
            ]

        if "+python" in spec:
            options.append("-DNMODL_ENABLE_PYTHON_BINDINGS=ON")
        else:
            options.append("-DNMODL_ENABLE_PYTHON_BINDINGS=OFF")

        if "+legacy-unit" in spec:
            options.append("-DNMODL_ENABLE_LEGACY_UNITS=ON")

        if "+llvm" in spec:
            options.append("-DNMODL_ENABLE_LLVM=ON")
        else:
            options.append("-DNMODL_ENABLE_LLVM=OFF")

        if "+llvm_cuda" in spec:
            options.append("-DNMODL_ENABLE_LLVM_CUDA=ON")

        return options

    def setup_build_environment(self, env):
        if "@:0.3b" in self.spec:
            env.prepend_path("PYTHONPATH", self.prefix.lib.python)
        else:
            env.prepend_path("PYTHONPATH", self.prefix.lib)

    def setup_run_environment(self, env):
        if "@:0.3b" in self.spec:
            env.prepend_path("PYTHONPATH", self.prefix.lib.python)
        else:
            env.prepend_path("PYTHONPATH", self.prefix.lib)

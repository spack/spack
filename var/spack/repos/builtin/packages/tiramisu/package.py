# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs
from spack.package import *


class Tiramisu(CMakePackage, PythonExtension):
    """Tiramisu is a polyhedral compiler for dense and sparse deep learning
    and data parallel algorithms.It provides a simple C++ API for expressing
    algorithms and how these algorithms should be optimized by the compiler."""

    homepage = "http://tiramisu-compiler.org"
    url = "https://github.com/Tiramisu-Compiler/tiramisu"
    git = "https://github.com/Tiramisu-Compiler/tiramisu.git"

    maintainers = ["wraith1995"]

    generator = "Ninja"

    version("master", branch="master")
    version("2023-2-3", commit="73a9cec72e08d4dfe5e8c66da33139008124a4fa")

    variant("python", default=True, description="Install python bindings.")
    variant("cuda", default=False, description="Enable Cuda Code Generation.")
    extends("python", when="+python")
    variant(
        "debug",
        default="0",
        description="Set the debug level.",
        multi=False,
        values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
    )

    depends_on("cmake@3.5:", type="build")
    depends_on("ninja", type="build")

    depends_on("halide@14.0.0", type=("build", "link", "run"))
    depends_on("isl", type=("build", "link", "run"))
    depends_on("cuda", when="+cuda", type=("build", "link", "run"))

    depends_on("python@3.8:", type=("build", "link", "run"), when="+python")
    depends_on("py-pybind11@2.6.2:", type=("build", "link", "run"), when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-cython", type=("run"), when="+python")

    def cmake_args(self):
        spec = self.spec
        llvmdir = spec["llvm"].prefix.bin
        args = [
            self.define("HALIDE_LIB_DIRECTORY", spec["halide"].prefix.lib),
            self.define("LLVM_CONFIG_BIN", llvmdir),
            self.define("HALIDE_SOURCE_DIRECTORY", spec["halide"].prefix),
            self.define("ISL_INCLUDE_DIRECTORY", spec["isl"].prefix.include),
            self.define("ISL_LIB_DIRECTORY", spec["isl"].prefix.lib),
            self.define_from_variant("DEBUG_LEVEL", "debug"),
            self.define_from_variant("WITH_PYTHON_BINDINGS", "python"),
            self.define_from_variant("USE_GPU", "cuda"),
            self.define("PYBIND11_USE_FETCHCONTENT", False),
            self.define("USE_FLEXNLP", False),
        ]
        if "+python" in spec:
            args += [
                self.define("Tiramisu_INSTALL_PYTHONDIR", python_platlib),
                self.define("Python3_EXECUTABLE", spec["python"].command.path),
            ]
        return args

    def build(self, pkg, spec):
        """Make the build targets"""
        cmake = Executable(self.spec["cmake"].prefix.bin.cmake)
        with fs.working_dir(self.build_directory):
            cmake(*(["--build", ".", "--target", "tiramisu", "--verbose"]))
            if "+python" in self.spec:
                cmake(*(["--build", ".", "--target", "Tiramisu_Python", "--verbose"]))

    def install(self, pkg, spec, prefix=None):
        """Make the install targets"""
        cmake = Executable(self.spec["cmake"].prefix.bin.cmake)
        with fs.working_dir(self.build_directory):
            cmake(*["--install", ".", "--verbose"])

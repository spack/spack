# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Halide(CMakePackage, PythonExtension):
    """Halide is a programming language designed to make it easier to write
    high-performance image and array processing code on modern machines."""

    homepage = "https://halide-lang.org/"
    url = "https://github.com/halide/Halide/archive/refs/tags/v14.0.0.tar.gz"
    git = "https://github.com/halide/Halide.git"
    maintainers = ["wraith1995"]
    version("main", branch="main")
    version("14.0.0", sha256="f9fc9765217cbd10e3a3e3883a60fc8f2dbbeaac634b45c789577a8a87999a01")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Release", "Debug", "RelWithDebInfo"),
    )
    generator = "Ninja"
    variant("python", default=False, description="Install python bindings")
    variant("tutorials", default=False, description="Install the Halide Tutorials.")
    variant("utils", default=False, description="Install the Halide Utilities.")
    variant("tests", default=False, description="Build and Run Halide Tests and Apps.")
    extends("python", when="+python")

    _targets = " targets=arm,x86,nvptx,aarch64,hexagon,webassembly "
    depends_on("cmake@3.22:", type="build")
    depends_on("ninja", type="build")
    depends_on(
        "llvm@14.0.0:14+clang+lld" + _targets + " build_type=Release",
        type=("link", "run"),
    )
    depends_on("libjpeg", type=("build", "link", "run"))
    depends_on("libpng", type=("build", "link", "run"))

    depends_on("python@3.8:", type=("build", "link", "run"), when="+python")
    # See https://github.com/halide/Halide/blob/main/requirements.txt
    depends_on("py-pybind11@2.6.2", type="build", when="+python")
    depends_on("py-setuptools@43:", type="build", when="+python")
    depends_on("py-scikit-build", type="build", when="+python")
    depends_on("py-wheel", type="build", when="+python")

    depends_on("py-imageio", type=("build", "run"), when="+python")
    depends_on("pil", type=("build", "run"), when="+python")
    depends_on("py-scipy", type=("build", "run"), when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")

    def cmake_args(self):
        spec = self.spec
        llvm_config = Executable(spec["llvm"].prefix.bin.join("llvm-config"))
        llvmdir = llvm_config("--cmakedir", output=str)
        args = [
            self.define("Python3_EXECUTABLE", spec["python"].command.path),
            self.define("PYBIND11_USE_FETCHCONTENT", False),
            self.define("LLVM_DIR", llvmdir),
            self.define_from_variant("WITH_TESTS", "tests"),
            self.define_from_variant("WITH_TUTORIALS", "tutorials"),
            self.define_from_variant("WITH_UTILS", "utils"),
            self.define_from_variant("WITH_PYTHON_BINDINGS", "python"),
            self.define("WITH_WABT", False),
        ]
        if "+python" in spec:
            args += [
                self.define(
                    "Halide_INSTALL_PYTHONDIR",
                    python_platlib,
                )
            ]
        return args

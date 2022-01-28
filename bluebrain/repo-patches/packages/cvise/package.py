# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Cvise(CMakePackage):
    """C-Vise is a super-parallel Python port of the C-Reduce. The port is
    fully compatible to the C-Reduce and uses the same efficient LLVM-based
    C/C++ reduction tool named clang_delta.

    C-Vise is a tool that takes a large C, C++ or OpenCL program that has a
    property of interest (such as triggering a compiler bug) and automatically
    produces a much smaller C/C++ or OpenCL program that has the same property.
    It is intended for use by people who discover and report bugs in compilers
    and other tools that process C/C++ or OpenCL code."""

    homepage = "https://github.com/marxin/cvise"
    url = "https://github.com/marxin/cvise"
    git = "https://github.com/marxin/cvise"
    maintainers = ["olupton"]

    version("develop", branch="master")
    version("2.4.0", tag="v2.4.0")
    version("2.3.0", tag="v2.3.0")

    depends_on("cmake", type="build")
    depends_on("colordiff", type=("build", "run"))
    depends_on("flex")
    depends_on("libxml2")
    depends_on("llvm@9.0.0:")
    depends_on("ncurses")  # this is an llvm dependency really
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-pebble", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pytest")
    depends_on("unifdef", type=("build", "run"))
    depends_on("zlib")

    def cmake_args(self):
        return ["-DPYTHON_EXECUTABLE=" + self.spec["python"].command.path]

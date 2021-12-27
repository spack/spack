# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lfortran(CMakePackage):
    """
    LFortran is a modern open-source (BSD licensed) interactive Fortran
    compiler built on top of LLVM. It can execute user’s code interactively
    to allow exploratory work (much like Python, MATLAB or Julia) as well as
    compile to binaries with the goal to run user’s code on modern
    architectures such as multi-core CPUs and GPUs.
    """

    homepage = "https://lfortran.org/"
    url = "https://lfortran.github.io/tarballs/release/lfortran-0.14.0.tar.gz"
    git = "https://gitlab.com/lfortran/lfortran.git"

    version("0.14.0", "fc3c1d592c56ae2636065ec0228db747f154f65a0867f6311bc8091efd5c13a7")

    variant("llvm", default=True, description="Build with LLVM backend")
    variant("xeus", default=False, description="Build with Jupyter kernel support")

    conflicts("%llvm@12:", when="+llvm")
    conflicts("%xeus@2:", when="+xeus")

    depends_on("zlib")
    depends_on("llvm", when="+llvm")
    depends_on("xeus", when="+xeus")
    depends_on("xtl", when="+xeus")
    depends_on("cppzmq", when="+xeus")
    depends_on("nlohmann-json", when="+xeus")
    depends_on("cmake", type="build")

    def cmake_args(self):
        args = [
            "-DWITH_LLVM={0}".format(str("+llvm" in self.spec).upper()),
            "-DWITH_XEUS={0}".format(str("+xeus" in self.spec).upper()),
        ]
        return args

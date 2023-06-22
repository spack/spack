# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lfortran(CMakePackage):
    """Modern interactive LLVM-based Fortran compiler"""

    homepage = "https://lfortran.org"
    url = "https://lfortran.github.io/tarballs/release/lfortran-0.19.0.tar.gz"
    git = "https://github.com/lfortran/lfortran.git"
    maintainers = ["certik"]

    # The build process uses 'git describe --tags' to get the package version
    version("main", branch="main", get_full_repo=True)
    version("0.19.0", sha256="d496f61d7133b624deb3562677c0cbf98e747262babd4ac010dbd3ab4303d805")

    variant("llvm", default=True, description="Build with LLVM support")
    variant("stacktrace", default=True, description="Build with stacktrace support")

    depends_on("python@3:", type="build", when="@main")
    depends_on("cmake", type="build")
    depends_on("llvm@11:15", type=("build", "run"), when="+llvm")
    depends_on("zlib", type="build")
    depends_on("re2c", type="build", when="@main")
    depends_on("bison@:3.4", type="build", when="@main")
    depends_on("binutils@2.38:", type="build", when="platform=linux")

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_LLVM", "llvm"),
            self.define_from_variant("WITH_STACKTRACE", "stacktrace"),
        ]

        if self.spec.satisfies("@main"):
            args.append("-DLFORTRAN_BUILD_ALL=yes")

        return args

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Highway(CMakePackage):
    """Performance-portable, length-agnostic SIMD with runtime dispatch."""

    homepage = "https://github.com/google/highway"
    url = "https://github.com/google/highway/archive/refs/tags/1.0.0.tar.gz"

    version("1.0.0", sha256="ab4f5f864932268356f9f6aa86f612fa4430a7db3c8de0391076750197e876b8")

    depends_on("cmake@3.10:", type="build")
    depends_on("googletest", type="test")

    def cmake_args(self):
        args = []
        if self.run_tests:
            args.append(self.define("HWY_SYSTEM_GTEST", True))
        return args

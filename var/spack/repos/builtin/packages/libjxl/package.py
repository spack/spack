# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjxl(CMakePackage):
    """JPEG XL image format reference implementation."""

    homepage = "https://github.com/libjxl/libjxl"
    url = "https://github.com/libjxl/libjxl/archive/refs/tags/v0.6.1.tar.gz"
    git = "https://github.com/libjxl/libjxl.git"

    version("main", branch="main", submodules=True)
    version("0.7.0", tag="v0.7.0", submodules=True)
    version("0.6.1", tag="v0.6.1", submodules=True)

    depends_on("cmake@3.10:", type="build")
    depends_on("brotli")
    depends_on("highway")

    # Only needed at test time, but unfortunately "test" doesn't cause the dep to be added
    # by Spack's compiler wrappers. Solution of adding "link" means that dependency is now
    # always required...
    depends_on("googletest+gmock", type=("link", "test"))

    # https://github.com/libjxl/libjxl/pull/582
    conflicts("%clang", when="@0.6")
    conflicts("%apple-clang", when="@0.6")

    def cmake_args(self):
        args = [
            self.define("JPEGXL_FORCE_SYSTEM_BROTLI", True),
            self.define("JPEGXL_FORCE_SYSTEM_HWY", True),
        ]

        if self.run_tests:
            args.append(self.define("JPEGXL_FORCE_SYSTEM_GTEST", True))

        return args

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ZlibNg(CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"

    version("2.0.6", sha256="8258b75a72303b661a238047cb348203d88d9dddf85d480ed885f375916fcab6")
    version("2.0.0", sha256="86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8")

    variant("compat", default=False, description="Enable compatibility API")
    variant("opt", default=True, description="Enable optimizations")

    depends_on("cmake@3.5.1:", type="build")

    @property
    def libs(self):
        name = "libz" if "+compat" in self.spec else "libz-ng"
        return find_libraries([name], root=self.prefix, recursive=True)

    def cmake_args(self):
        args = [
            self.define_from_variant("ZLIB_COMPAT", "compat"),
            self.define_from_variant("WITH_OPTIM", "opt"),
            self.define("ZLIB_ENABLE_TESTS", False),
        ]

        return args

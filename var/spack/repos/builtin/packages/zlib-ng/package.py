# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ZlibNg(CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"

    version(
        "2.1.0-beta1", sha256="7331c2f0697342e47d219448b9ac45a409862c5a0c5ff4a68d702155e8e2b5e8"
    )
    version(
        "2.0.7",
        sha256="6c0853bb27738b811f2b4d4af095323c3d5ce36ceed6b50e5f773204fb8f7200",
        preferred=True,
    )
    version(
        "2.0.0",
        sha256="86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8",
        preferred=True,
    )

    variant("compat", default=True, description="Enable compatibility API")
    variant("opt", default=True, description="Enable optimizations")

    depends_on("cmake@3.5.1:", type="build")
    depends_on("cmake@3.14.0:", type="build", when="@2.1.0:")

    patch("pull-1484.patch", when="@2.1.0-beta1")

    def cmake_args(self):
        args = [
            self.define_from_variant("ZLIB_COMPAT", "compat"),
            self.define_from_variant("WITH_OPTIM", "opt"),
        ]

        return args

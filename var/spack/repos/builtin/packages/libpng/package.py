# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class Libpng(CMakePackage):
    """libpng is the official PNG reference library."""

    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url = "https://prdownloads.sourceforge.net/libpng/libpng-1.6.37.tar.xz"
    git = "https://github.com/glennrp/libpng.git"

    maintainers("AlexanderRichert-NOAA")

    version("1.6.39", sha256="1f4696ce70b4ee5f85f1e1623dc1229b210029fa4b7aee573df3e2ba7b036937")
    version("1.6.37", sha256="505e70834d35383537b6491e7ae8641f1a4bed1876dbfe361201fc80868d88ca")
    # From http://www.libpng.org/pub/png/libpng.html (2019-04-15)
    #     libpng versions 1.6.36 and earlier have a use-after-free bug in the
    #     simplified libpng API png_image_free(). It has been assigned ID
    #     CVE-2019-7317. The vulnerability is fixed in version 1.6.37,
    #     released on 15 April 2019.

    # Required for qt@3
    version("1.5.30", sha256="7d76275fad2ede4b7d87c5fd46e6f488d2a16b5a69dc968ffa840ab39ba756ed")
    version("1.2.57", sha256="0f4620e11fa283fedafb474427c8e96bf149511a1804bdc47350963ae5cf54d8")

    depends_on("zlib@1.0.4:")  # 1.2.5 or later recommended

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("CMAKE_CXX_FLAGS", self.spec["zlib"].headers.include_flags),
            self.define("ZLIB_ROOT", self.spec["zlib"].prefix),
            self.define("PNG_SHARED", "shared" in self.spec.variants["libs"].value),
            self.define("PNG_STATIC", "static" in self.spec.variants["libs"].value),
        ]
        if self.spec.satisfies("platform=darwin target=aarch64:"):
            args.append("-DPNG_ARM_NEON=off")
        return args

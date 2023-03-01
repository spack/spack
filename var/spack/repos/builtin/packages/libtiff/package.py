# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.cmake import CMakeBuilder
from spack.package import *

VARIANTS = [
    # Internal codecs
    "ccitt",
    "packbits",
    "lzw",
    "thunder",
    "next",
    "logluv",
    # External codecs
    "zlib",
    "libdeflate",
    "pixarlog",
    "jpeg",
    "old-jpeg",
    "jpeg12",
    "jbig",
    "lerc",
    "lzma",
    "zstd",
    "webp",
]


class Libtiff(CMakePackage, AutotoolsPackage):
    """LibTIFF - Tag Image File Format (TIFF) Library and Utilities."""

    homepage = "http://www.simplesystems.org/libtiff/"
    url = "https://download.osgeo.org/libtiff/tiff-4.1.0.tar.gz"

    maintainers("adamjstewart")

    version("4.4.0", sha256="917223b37538959aca3b790d2d73aa6e626b688e02dcda272aec24c2f498abed")
    version("4.3.0", sha256="0e46e5acb087ce7d1ac53cf4f56a09b221537fc86dfc5daaad1c2e89e1b37ac8")
    version("4.2.0", sha256="eb0484e568ead8fa23b513e9b0041df7e327f4ee2d22db5a533929dfc19633cb")
    version("4.1.0", sha256="5d29f32517dadb6dbcd1255ea5bbc93a2b54b94fbf83653b4d65c7d6775b8634")
    version("4.0.10", sha256="2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4")
    version("4.0.9", sha256="6e7bdeec2c310734e734d19aae3a71ebe37a4d842e0e23dbb1b8921c0026cfcd")
    version("4.0.8", sha256="59d7a5a8ccd92059913f246877db95a2918e6c04fb9d43fd74e5c3390dac2910")
    version("4.0.7", sha256="9f43a2cfb9589e5cecaa66e16bf87f814c945f22df7ba600d63aac4632c4f019")
    version("4.0.6", sha256="4d57a50907b510e3049a4bba0d7888930fdfc16ce49f1bf693e5b6247370d68c")
    version("4.0.5", sha256="e25eaa83ed7fab43ddd278b9b14d91a406a4b674cedc776adb95535f897f309c")
    version("4.0.4", sha256="8cb1d90c96f61cdfc0bcf036acc251c9dbe6320334da941c7a83cfe1576ef890")
    version("3.9.7", sha256="f5d64dd4ce61c55f5e9f6dc3920fbe5a41e02c2e607da7117a35eb5c320cef6a")

    # Internal codecs
    variant("ccitt", default=True, description="support for CCITT Group 3 & 4 algorithms")
    variant("packbits", default=True, description="support for Macintosh PackBits algorithm")
    variant("lzw", default=True, description="support for LZW algorithm")
    variant("thunder", default=True, description="support for ThunderScan 4-bit RLE algorithm")
    variant("next", default=True, description="support for NeXT 2-bit RLE algorithm")
    variant("logluv", default=True, description="support for LogLuv high dynamic range algorithm")

    # External codecs
    variant("zlib", default=True, description="use zlib")
    variant("libdeflate", default=False, description="use libdeflate", when="@4.2:")
    variant("pixarlog", default=False, description="support for Pixar log-format algorithm")
    variant("jpeg", default=True, description="use libjpeg")
    variant("old-jpeg", default=False, description="support for Old JPEG compression")
    variant("jpeg12", default=False, description="enable libjpeg 8/12-bit dual mode", when="@4:")
    variant("jbig", default=False, description="use ISO JBIG compression")
    variant("lerc", default=False, description="use libLerc", when="@4.3:")
    variant("lzma", default=False, description="use liblzma", when="@4:")
    variant("zstd", default=False, description="use libzstd", when="@4.0.10:")
    variant("webp", default=False, description="use libwebp", when="@4.0.10:")

    build_system(conditional("cmake", when="@4.0.5:"), "autotools", default="cmake")

    with when("build_system=cmake"):
        depends_on("cmake@3.9:", when="@4.3:", type="build")
        depends_on("cmake@2.8.11:", when="@4.0.10:4.2", type="build")
        depends_on("cmake@2.8.9:", when="@4.0.6:4.0.9", type="build")
        depends_on("cmake@3:", when="@4.0.5", type="build")

    depends_on("zlib", when="+zlib")
    depends_on("zlib", when="+pixarlog")
    depends_on("jpeg@5:", when="+jpeg")
    depends_on("jbigkit", when="+jbig")
    depends_on("lerc", when="+lerc")
    depends_on("xz", when="+lzma")
    depends_on("zstd@1:", when="+zstd")
    depends_on("libwebp", when="+webp")

    conflicts("+libdeflate", when="~zlib")
    conflicts("+jpeg12", when="~jpeg")
    conflicts("+lerc", when="~zlib")

    # 4.3.0 contains a bug that breaks the build on case-sensitive filesystems when
    # using a C++20-capable compiler (commonly the case on macOS). Not an easy way to
    # check for this, so add a conflict for macOS overall. For more details, see:
    # https://gitlab.com/libtiff/libtiff/-/merge_requests/243
    conflicts("platform=darwin", when="@4.3.0")

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc@:20.11"):
            filter_file(
                'vl_cv_prog_cc_warnings="-Wall -W"', 'vl_cv_prog_cc_warnings="-Wall"', "configure"
            )


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        args = [self.define_from_variant(var) for var in VARIANTS]

        # Remove empty strings
        args = [arg for arg in args if arg]

        return args


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        args = []
        for var in VARIANTS:
            args.extend(self.enable_or_disable(var))

        return args

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class Freetype(AutotoolsPackage, CMakePackage):
    """FreeType is a freely available software library to render fonts.
    It is written in C, designed to be small, efficient, highly customizable,
    and portable while capable of producing high-quality output (glyph images)
    of most vector and bitmap font formats."""

    homepage = "https://www.freetype.org/index.html"
    url = "https://download.savannah.gnu.org/releases/freetype/freetype-2.10.1.tar.gz"

    maintainers("michaelkuhn")

    version("2.11.1", sha256="f8db94d307e9c54961b39a1cc799a67d46681480696ed72ecf78d4473770f09b")
    version("2.11.0", sha256="a45c6b403413abd5706f3582f04c8339d26397c4304b78fa552f2215df64101f")
    version("2.10.4", sha256="5eab795ebb23ac77001cfb68b7d4d50b5d6c7469247b0b01b2c953269f658dac")
    version("2.10.2", sha256="e09aa914e4f7a5d723ac381420949c55c0b90b15744adce5d1406046022186ab")
    version("2.10.1", sha256="3a60d391fd579440561bf0e7f31af2222bc610ad6ce4d9d7bd2165bca8669110")
    version("2.10.0", sha256="955e17244e9b38adb0c98df66abb50467312e6bb70eac07e49ce6bd1a20e809a")
    version("2.9.1", sha256="ec391504e55498adceb30baceebd147a6e963f636eb617424bcfc47a169898ce")
    version("2.7.1", sha256="162ef25aa64480b1189cdb261228e6c5c44f212aac4b4621e28cf2157efb59f5")
    version("2.7", sha256="7b657d5f872b0ab56461f3bd310bd1c5ec64619bd15f0d8e08282d494d9cfea4")
    version("2.5.3", sha256="41217f800d3f40d78ef4eb99d6a35fd85235b64f81bc56e4812d7672fca7b806")

    build_system("cmake", "autotools", default="autotools")

    depends_on("bzip2")
    depends_on("libpng")
    for plat in ["linux", "darwin", "cray"]:
        depends_on("pkgconfig", type="build", when="platform=%s" % plat)

    conflicts(
        "%intel",
        when="@2.8:2.10.2",
        msg="freetype-2.8 to 2.10.2 cannot be built with icc (does not "
        "support __builtin_shuffle)",
    )

    variant("shared", default=True, description="Build shared libraries")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    requires("+pic", when="+shared build_system=autotools")

    patch("windows.patch", when="@2.9.1")

    @property
    def headers(self):
        headers = find_headers("*", self.prefix.include, recursive=True)
        headers.directories = [self.prefix.include.freetype2]
        return headers


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        args = [
            "--with-brotli=no",
            "--with-bzip2=yes",
            "--with-harfbuzz=no",
            "--with-png=yes",
            "--with-zlib=no",
        ]
        if self.spec.satisfies("@2.9.1:"):
            args.append("--enable-freetype-config")
        args.extend(self.enable_or_disable("shared"))
        args.extend(self.with_or_without("pic"))
        return args


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        return [
            self.define("FT_DISABLE_ZLIB", True),
            self.define("FT_DISABLE_BROTLI", True),
            self.define("FT_DISABLE_HARFBUZZ", True),
            self.define("FT_REQUIRE_PNG", True),
            self.define("FT_REQUIRE_BZIP2", True),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

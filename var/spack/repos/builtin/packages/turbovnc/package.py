# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Turbovnc(CMakePackage):
    """A VNC server tuned to provide peak 3D performance"""

    homepage = "https://turbovnc.org/"
    url = "https://github.com/TurboVNC/turbovnc/archive/refs/tags/3.1.1.tar.gz"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("3.1.1", sha256="834392e985cf29a6d7d3b21b6b95b8249c1390f2c4bbf716e03945ca9384bbc8")
    version("3.1", sha256="218eaf769c29763d4e6062978b8f2fb5538dc2b232b77d3f094591fe63ddbf65")
    version("3.0.3", sha256="3a3e1bce1d6d41b33b52c51c8546c849db1226f42255f4cef306e7bd9e1cced4")
    version("3.0.2", sha256="af1d1dbd63e4f2eb3c5c6c7f5fdeea31875c5e720d2d9a41c3a49a7c5736e67b")
    version("3.0.1", sha256="f0bd45e4e6f8cb8a52b5ccdef70fbc28ba8776591554c166db113eedc914dd86")

    generator("ninja")

    variant("viewer", default=True, description="Build VNC viewer")
    variant("server", default=True, description="Build VNC server")
    variant("libs", default=True, description="Build with spack-provided core libs")
    variant("openssl", default=True, description="Build with spack-provided openssl")
    variant("java", default=True, description="Build with spack-provided java")
    variant("web", default=True, description="Build with noVNC support", when="+server")
    #    variant("X", default=False, description="Build with spack-provided X")

    with default_args(type="build"):
        depends_on("ninja")
        depends_on("cmake@2.8.12:")
        depends_on("cmake@3.12:", when="+web")
        depends_on("gettext")
        depends_on("perl-extutils-makemaker")
        depends_on("pkgconfig")

    depends_on("libjpeg-turbo@1.2:")
    depends_on("linux-pam")

    depends_on("openjdk@11:", when="+java")
    depends_on("openssl", when="+openssl")

    with when("+libs"):
        depends_on("zlib-api")
        depends_on("bzip2")
        depends_on("freetype")

    depends_on("xkbcomp")
    depends_on("xkeyboard-config")

    depends_on("libcap")
    depends_on("krb5")

    depends_on("libx11")
    depends_on("libxau")
    depends_on("libxcb")
    depends_on("libxext")
    depends_on("libxfixes")
    depends_on("libxi")
    depends_on("libxt")

    depends_on("fontconfig")
    depends_on("font-util")
    depends_on("libxft")
    depends_on("libxfont2")
    depends_on("pixman")

    depends_on("libice")
    depends_on("libsm")
    depends_on("xz")
    depends_on("lua")
    depends_on("python")
    depends_on("python@3:", when="+web")

    with default_args(type="run"):
        depends_on("xauth")

    def cmake_args(self):
        spec = self.spec
        jpeg = spec["libjpeg-turbo"]
        fontutil = spec["font-util"]
        xkbcomp = spec["xkbcomp"]
        xkbbase = spec["xkeyboard-config"]

        # Required flags for Spack build
        args = [
            # Turbo JPEG is required
            f"-DTJPEG_INCLUDE_DIR={jpeg.home.include}",
            f"-DTJPEG_LIBRARY=-L{jpeg.home.lib} -lturbojpeg",
        ]

        args += [
            # Look for Java
            self.define_from_variant("TVNC_INCLUDEJRE", "java"),
            self.define_from_variant("TVNC_SYSTEMLIBS", "libs"),
            self.define_from_variant("TVNC_DLOPENSSL", "openssl"),
            self.define_from_variant("TVNC_BUILDWEBSERVER", "web"),
        ]

        # This is all of the Xorg stuff that needs to be sorted out
        args += [
            "-DTVNC_SYSTEMX11=0",  # Not ready to debug this YET
            "-DTVNC_STATIC_XORG_PATHS=0",  # TODO: Investigate
        ]

        # Keyboard configuration (Xvnc wont start if this is wrong)
        args += [
            # We need to tell TurboVNC where xkbcomp is
            f"-DXKB_BIN_DIRECTORY={xkbcomp.home.bin}",
            # We also need to tell it where to find the xkb rules
            f"-DXKB_BASE_DIRECTORY={xkbbase.home.share.X11.xkb}",
            # And where what the default rules should be
            "-DXKB_DFLT_RULES=base",
        ]

        # Misc X configuration
        args += [
            #f"-DXORG_FONT_PATH={fontutil.home.share.fonts.X11}",
            #f"-DFONT_ENCODINGS_DIRECTORY={fontutil.home.share.fonts.X11.encodings}",
            # Don't know what actually provides these yet
            # f"-DXORG_DRI_DRIVER_PATH={}",  # dri was struggling to build in xorg-server
            # f"-DXORG_REGISTRY_PATH={}",    # This needs protocols.txt from dix?
        ]
        return args

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

    variant("novnc", default=True, description="Build with noVNC support")

    with default_args(type="build"):
        depends_on("ninja")
        depends_on("cmake@2.8.12:")
        depends_on("cmake@3.12:", when="+novnc")
        depends_on("gettext")
        depends_on("perl-extutils-makemaker")
    
    depends_on("libjpeg-turbo@1.2:")
    depends_on("linux-pam")
    depends_on("openjdk@11:")

    depends_on("libcap")

    depends_on("openssl")
    depends_on("krb5")

    depends_on("libx11")
    depends_on("libxau")
    depends_on("libxcb")
    depends_on("libxext")
    depends_on("libxfixes")
    depends_on("libxi")
    dpendds_on("libxkbcommon")
    depends_on("libxt")
    depends_on("xproto")

    depends_on("libice")
    depends_on("libsm")
    depends_on("zlib-api")
    depends_on("xz")
    depends_on("lua")
    depends_on("python")
    depends_on("python@3:", when="+novnc")

    with default_args(type="run"):
        depends_on("xauth")
        depends_on("xkeyboard-config")

    def cmake_args(self):
        spec = self.spec
        jpeg = spec["libjpeg-turbo"]
        ssl = spec["openssl"]
        xkb = spec["libxkbcommon"]
        args = [
            f"-DTVNC_INCLUDEJRE=1",
            f"-DTJPEG_INCLUDE_DIR={jpeg.home.include}",
            f"-DTJPEG_LIBRARY=-L{jpeg.home.lib} -lturbojpeg",
            f"-DTVNC_DLOPENSSL={ssl.home.libs.search_flags}",
            f"-DXKB_BASE_DIRECTORY={xkb.home.share}",
            f"-DXKB_BIN_DIRECTORY={xkb.home.bin}",
            # TODO
#            f"-DTVNC_STATIC_XORG_PATHS={}",
#            f"-DTVNC_SYSTEMLIBS={}",
#            f"-DTVNC_SYSTEMX11={}",
#            f"-DXORG_DRI_DRIVER_PATH={}",
#            f"-DXORG_FONT_PATH={}",
#            f"-DXORG_REGISTRY_PATH={}",
        ]
        return args

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libwmf(AutotoolsPackage):
    """libwmf is a library for reading vector images in Microsft's
    native Windows Metafile Format (WMF)"""

    homepage = "https://github.com/caolanm/libwmf"
    url = "https://github.com/caolanm/libwmf/archive/refs/tags/v0.2.12.tar.gz"

    maintainers("benkirk")

    parallel = False

    version("0.2.12", sha256="464ff63605d7eaf61a4a12dbd420f7a41a4d854675d8caf37729f5bc744820e2")
    version("0.2.11", sha256="e2a2664afd5abc71a42be7ad3c200f64de2b8889bf088eac1d32e205ce843803")

    depends_on("pkgconfig", type="build")
    depends_on("expat")
    depends_on("freetype")
    depends_on("gdk-pixbuf")
    depends_on("ghostscript-fonts")
    depends_on("libxml2")
    depends_on("libpng")
    depends_on("libjpeg")
    depends_on("zlib")

    def configure_args(self):
        args = ["--disable-static"]
        return args

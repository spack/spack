# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxdmcp(AutotoolsPackage, XorgPackage):
    """libXdmcp - X Display Manager Control Protocol library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXdmcp"
    xorg_mirror_path = "lib/libXdmcp-1.1.2.tar.gz"

    version("1.1.4", sha256="55041a8ff8992ab02777478c4b19c249c0f8399f05a752cb4a1a868a9a0ccb9a")
    version("1.1.2", sha256="6f7c7e491a23035a26284d247779174dedc67e34e93cc3548b648ffdb6fc57c0")

    depends_on("xproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
    depends_on("libbsd", when="platform=linux")
    depends_on("libbsd", when="platform=cray")

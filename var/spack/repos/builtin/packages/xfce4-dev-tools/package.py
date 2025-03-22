# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfce4DevTools(AutotoolsPackage):
    """Autoconf macros and scripts to augment XFCE4 app and library build systems"""

    homepage = "https://docs.xfce.org/xfce/xfce4-dev-tools/start"
    url = "https://archive.xfce.org/src/xfce/xfce4-dev-tools/4.20/xfce4-dev-tools-4.20.0.tar.bz2"

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teaguesterling")

    version("4.20.0", sha256="1fba39a08a0ecc771eaa3a3b6e4272a4f0b9e7c67d0f66e780cd6090cd4466aa")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("libxslt", type="build")
    depends_on("meson", type="build")

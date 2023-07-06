# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xkbutils(AutotoolsPackage, XorgPackage):
    """xkbutils is a collection of small utilities utilizing the XKeyboard
    (XKB) extension to the X11 protocol."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xkbutils"
    xorg_mirror_path = "app/xkbutils-1.0.4.tar.gz"

    version("1.0.5", sha256="b87072f0d7e75f56ee04455e1feab92bb5847aee4534b18c2e08b926150279ff")
    version("1.0.4", sha256="cf31303cbdd6a86c34cab46f4b6e0c7acd2e84578593b334a146142894529bca")

    depends_on("libxaw")
    depends_on("libxt")
    depends_on("libx11")

    depends_on("xproto@7.0.17:")
    depends_on("inputproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

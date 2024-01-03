# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxdamage(AutotoolsPackage, XorgPackage):
    """This package contains the library for the X Damage extension."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXdamage"
    xorg_mirror_path = "lib/libXdamage-1.1.4.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.6", sha256="2afcc139eb6eb926ffe344494b1fc023da25def42874496e6e6d3aa8acef8595")
    version("1.1.5", sha256="630ec53abb8c2d6dac5cd9f06c1f73ffb4a3167f8118fdebd77afd639dbc2019")
    version("1.1.4", sha256="4bb3e9d917f5f593df2277d452926ee6ad96de7b7cd1017cbcf4579fe5d3442b")

    depends_on("libxfixes")
    depends_on("libx11")

    depends_on("damageproto@1.1:")
    depends_on("fixesproto")
    depends_on("xextproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

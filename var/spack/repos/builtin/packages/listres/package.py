# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Listres(AutotoolsPackage, XorgPackage):
    """The listres program generates a list of X resources for a widget
    in an X client written using a toolkit based on libXt."""

    homepage = "https://cgit.freedesktop.org/xorg/app/listres"
    xorg_mirror_path = "app/listres-1.0.3.tar.gz"

    version("1.0.5", sha256="ed068e63dfb6e42cfbcea568d161e53e1d120d99da9aa16c1f822803ebb38504")
    version("1.0.3", sha256="87d5698b8aa4d841e45e6556932c9914210cbd8b10003d664b31185b087981be")

    depends_on("libxaw")
    depends_on("libxt")
    depends_on("libxmu")

    depends_on("xproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

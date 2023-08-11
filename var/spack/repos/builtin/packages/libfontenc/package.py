# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfontenc(AutotoolsPackage, XorgPackage):
    """libfontenc - font encoding library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libfontenc"
    xorg_mirror_path = "lib/libfontenc-1.1.3.tar.gz"

    version("1.1.7", sha256="5e5f210329823f08f97bfe9fd5b4105070c789bc5aef88ce01d86d8203d4aa9f")
    version("1.1.3", sha256="6fba26760ca8d5045f2b52ddf641c12cedc19ee30939c6478162b7db8b6220fb")

    depends_on("zlib-api")

    depends_on("xproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Xorgproto(MesonPackage):
    """X Window System unified protocol definitions replacing standalone protos"""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xorgproto"
    url = "https://gitlab.freedesktop.org/xorg/proto/xorgproto/-/archive/xorgproto-2024.1/xorgproto-xorgproto-2024.1.tar.bz2"

    maintainers("teaguesterling")

    license("OTHER", checked_by="teaguesterling")

    version("2024.1", sha256="3959b2d17d86dd9d165dc24d26f372ca64f27127cd381739366ba8383a6cd51a")

    depends_on("meson@0.56:")
    depends_on("util-macros", type="build")


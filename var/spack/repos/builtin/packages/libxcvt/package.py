# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libxcvt(MesonPackage):
    """Implementation of the VESA CVT standard timing modelines generator."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcvt"
    url = "https://gitlab.freedesktop.org/xorg/lib/libxcvt/-/archive/libxcvt-0.1.2/libxcvt-libxcvt-0.1.2.tar.bz2"

    license("MIT", checked_by="teaguesterling")

    version("0.1.2", sha256="590e5a6da87ace7aa7857026b207a2c4d378620035441e20ea97efedd15d6d4a")


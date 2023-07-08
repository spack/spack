# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libde265(CMakePackage):
    """libde265 is an open source implementation of the h.265 video codec.

    It is written from scratch and has a plain C API to enable
    a simple integration into other software."""

    homepage = "https://www.libde265.org"
    url = "https://github.com/strukturag/libde265/archive/refs/tags/v1.0.9.tar.gz"

    maintainers("benkirk")

    version("1.0.9", sha256="153554f407718a75f1e0ae197d35b43147ce282118a54f894554dbe27c32163d")

    depends_on("cmake@3.13:", type="build")

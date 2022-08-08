# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjxl(CMakePackage):
    """JPEG XL image format reference implementation."""

    homepage = "https://github.com/libjxl/libjxl"
    url = "https://github.com/libjxl/libjxl/archive/refs/tags/v0.6.1.tar.gz"
    git = "https://github.com/libjxl/libjxl.git"

    version("main", branch="main", submodules=True)
    version("0.6.1", tag="v0.6.1", submodules=True)

    depends_on("cmake@3.10:", type="build")
    # TODO: is it possible to use external installations of these?
    # depends_on("highway")
    # depends_on("lodepng")
    # depends_on("sjpeg")
    # depends_on("googletest+gmock", type="test")

    # https://github.com/libjxl/libjxl/pull/582
    conflicts("%clang", when="@0.6")
    conflicts("%apple-clang", when="@0.6")

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qb3(CMakePackage):
    """QB3: Fast and Efficient Raster Compression."""

    homepage = "https://github.com/lucianpls/QB3"
    git = "https://github.com/lucianpls/QB3.git"

    version("master", branch="master")

    depends_on("cmake@3.5:", type="build")
    depends_on("libicd")

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libicd(CMakePackage):
    """Image codec library."""

    homepage = "https://github.com/lucianpls/libicd"
    git = "https://github.com/lucianpls/libicd.git"

    version("main", branch="main")

    depends_on("cmake@3.5:", type="build")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("lerc")

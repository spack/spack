# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qb3(CMakePackage):
    """QB3: Fast and Efficient Raster Compression."""

    homepage = "https://github.com/lucianpls/QB3"
    git = "https://github.com/lucianpls/QB3.git"

    license("Apache-2.0")

    version("master", branch="master")

    depends_on("cmake@3.5:", type="build")
    depends_on("libicd")

    @property
    def libs(self):
        # Override because libs have different case than Spack package name
        name = "libQB3*"
        return find_libraries(name, root=self.prefix, shared=True, recursive=True)

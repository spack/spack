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
        # We expect libraries to be in either lib64 or lib directory
        # Try lib64 first
        root = self.prefix.lib64
        liblist = find_libraries(name, root=root, shared=True, recursive=False)
        if liblist:
            # Found libs in lib64, so return those
            return liblist
        else:
            # Did not find libs in lib64, so try lib w/out 64 suffix
            root = self.prefix.lib
            liblist = find_libraries(name, root=root, shared=True, recursive=False)
            return liblist

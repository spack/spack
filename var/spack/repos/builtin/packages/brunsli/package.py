# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brunsli(CMakePackage):
    """Brunsli is a lossless JPEG repacking library."""

    homepage = "https://github.com/google/brunsli"
    git = "https://github.com/google/brunsli.git"

    version("0.1", tag="v0.1", submodules=True)

    depends_on("cmake@3.1:", type="build")

    @property
    def libs(self):
        return find_libraries(
            ["libbrunslidec-c", "libbrunslienc-c"], root=self.prefix, recursive=True
        )

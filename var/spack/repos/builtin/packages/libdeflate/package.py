# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdeflate(MakefilePackage):
    """Heavily optimized library for DEFLATE/zlib/gzip compression and decompression"""

    homepage = "https://github.com/ebiggers/libdeflate"
    url = "https://github.com/ebiggers/libdeflate/archive/v1.7.tar.gz"

    maintainers("dorton21")

    version("1.10", sha256="5c1f75c285cd87202226f4de49985dcb75732f527eefba2b3ddd70a8865f2533")
    version("1.7", sha256="a5e6a0a9ab69f40f0f59332106532ca76918977a974e7004977a9498e3f11350")

    depends_on("zlib")
    depends_on("gzip")

    def patch(self):
        filter_file(r"\/usr\/local", self.prefix, "Makefile")

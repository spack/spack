# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdeflate(MakefilePackage, CMakePackage):
    """Heavily optimized library for DEFLATE/zlib/gzip compression and decompression"""

    homepage = "https://github.com/ebiggers/libdeflate"
    url = "https://github.com/ebiggers/libdeflate/archive/v1.7.tar.gz"

    maintainers("dorton21")

    version("1.18", sha256="225d982bcaf553221c76726358d2ea139bb34913180b20823c782cede060affd")
    version("1.10", sha256="5c1f75c285cd87202226f4de49985dcb75732f527eefba2b3ddd70a8865f2533")
    version("1.7", sha256="a5e6a0a9ab69f40f0f59332106532ca76918977a974e7004977a9498e3f11350")

    build_system(conditional("makefile", when="@:1.14"), conditional("cmake", when="@1.15:"))

    depends_on("zlib")
    depends_on("gzip")

    with when("build_system=cmake"):
        depends_on("cmake@3.7:", type="build")

    @when("@:1.14")
    def patch(self):
        filter_file(r"\/usr\/local", self.prefix, "Makefile")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    pass


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    pass

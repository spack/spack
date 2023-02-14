# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cernlib(CMakePackage):
    """CERN Library"""

    homepage = "https://cernlib.web.cern.ch"
    url = "https://cernlib.web.cern.ch/cernlib/download/2022_source/tar/cernlib-2022.11.08.0-free.tar.gz"

    maintainers("andriish")

    version(
        "2022.11.08.0-free",
        sha256="733d148415ef78012ff81f21922d3bf641be7514b0242348dd0200cf1b003e46",
    )

    depends_on("freetype")
    depends_on("motif")
    depends_on("libnsl")
    depends_on("libx11")
    depends_on("libxaw")
    depends_on("libxt")
    depends_on("libxcrypt")

    depends_on("openssl", when="os=linux")

    @when("@2022.11.08.0-free")
    def patch(self):
        filter_file("crypto", "crypt", "packlib/CMakeLists.txt")

    def cmake_args(self):
        args = ["-DCERNLIB_BUILD_SHARED:BOOL=ON"]
        return args

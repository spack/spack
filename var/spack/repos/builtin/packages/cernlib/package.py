# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cernlib(CMakePackage):
    """CERN Library"""

    homepage = "https://cernlib.web.cern.ch"
    url = "https://cernlib.web.cern.ch/download/2023_source/tar/cernlib-2023.08.14.0-free.tar.gz"

    maintainers("andriish")

    version(
        "2023.08.14.0-free",
        sha256="7006475d9c38254cb94ce75e556a319fea3b3155087780ea522003103771474e",
    )

    variant("shared", default=True, description="Build shared libraries")

    depends_on("freetype")
    depends_on("motif")
    depends_on("libnsl")
    depends_on("libx11")
    depends_on("libxaw")
    depends_on("libxt")
    depends_on("libxcrypt")

    depends_on("openssl", when="platform=linux")

    @when("@2023.08.14.0-free")
    def patch(self):
        filter_file("crypto", "crypt", "packlib/CMakeLists.txt")

    def cmake_args(self):
        args = [self.define_from_variant("CERNLIB_BUILD_SHARED", "shared")]
        return args

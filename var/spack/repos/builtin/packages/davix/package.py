# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Davix(CMakePackage):
    """High-performance file management over WebDAV/HTTP."""

    homepage = "https://davix.web.cern.ch/davix/docs/devel/index.html"
    url = "https://github.com/cern-fts/davix/releases/download/R_0_8_1/davix-0.8.1.tar.gz"

    maintainers("gartung", "greenc-FNAL", "marcmengel", "vitodb")

    version("0.8.1", sha256="3f42f4eadaf560ab80984535ffa096d3e88287d631960b2193e84cf29a5fe3a6")
    version("0.8.0", sha256="2f108da0408a83fb5b9f0c68150d360ba733e4b3a0fe298d45b0d32d28ab7124")
    version("0.7.6", sha256="a2e7fdff29f7ba247a3bcdb08ab1db6d6ed745de2d3971b46526986caf360673")
    version("0.7.5", sha256="d920ca976846875d83af4dc50c99280bb3741fcf8351d5733453e70fa5fe6fc8")
    version("0.7.3", sha256="cd46276e72c6a0da1e2ad30eb66ec509a4c023687767c62a66713fa8c23d328a")
    version("0.6.9", sha256="fbd97eb5fdf82ca48770d06bf8e2805b35f23255478aa381a9d25a49eb98e348")
    version("0.6.8", sha256="e1820f4cc3fc44858ae97197a3922cce2a1130ff553b080ba19e06eb8383ddf7")

    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("pkgconfig", type="build")
    depends_on("libxml2")
    depends_on("uuid")
    depends_on("openssl")

    variant("thirdparty", default=False)
    depends_on("gsoap", when="+thirdparty")

    def cmake_args(self):
        cmake_args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", variant="cxxstd"),
            self.define_from_variant("ENABLE_THIRD_PARTY_COPY", variant="thirdparty"),
        ]

        if "darwin" in self.spec.architecture:
            cmake_args.append("-DCMAKE_MACOSX_RPATH=ON")
        return cmake_args

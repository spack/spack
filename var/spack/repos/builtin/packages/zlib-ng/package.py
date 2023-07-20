# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class ZlibNg(AutotoolsPackage, CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"

    version("2.1.2", sha256="383560d6b00697c04e8878e26c0187b480971a8bce90ffd26a5a7b0f7ecf1a33")
    version("2.0.7", sha256="6c0853bb27738b811f2b4d4af095323c3d5ce36ceed6b50e5f773204fb8f7200")
    version("2.0.0", sha256="86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8")

    variant("compat", default=True, description="Enable compatibility API")
    variant("opt", default=True, description="Enable optimizations")

    # Default to autotools, since cmake would result in circular dependencies if it's not
    # reused.
    build_system("autotools", "cmake", default="autotools")

    with when("build_system=cmake"):
        depends_on("cmake@3.5.1:", type="build")
        depends_on("cmake@3.14.0:", type="build", when="@2.1.0:")


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []
        if self.spec.satisfies("+compat"):
            args.append("--zlib-compat")
        if self.spec.satisfies("~opt"):
            args.append("--without-optimizations")
        return args


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define_from_variant("ZLIB_COMPAT", "compat"),
            self.define_from_variant("WITH_OPTIM", "opt"),
        ]

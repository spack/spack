# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmetatensor(CMakePackage):
    """Self-describing sparse tensor data format for atomistic machine learning and beyond."""

    homepage = "https://docs.metatensor.org"
    url = "https://github.com/metatensor/metatensor/releases/download/metatensor-core-v0.1.14/metatensor-core-cxx-0.1.14.tar.gz"
    git = "https://github.com/metatensor/metatensor.git"

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.1.14", sha256="dc6cdd9cf0113e2f012ecf68b81cc7cfc71bef3d2020b41574de8fa403dba646")
    version("0.1.13", sha256="c735b1050357b2873e2e07ee1e263fc9d45faf07f5ea63b65e70869ca423adb5")

    variant("shared", default=True, description="Build shared library version")

    generator("ninja")

    depends_on("cmake", type="build")
    depends_on("ninja", type="build")
    depends_on("rust@1.74.0:", type="build")

    depends_on("cxx", type="test")
    depends_on("cmake", type="test")
    depends_on("ninja", type="test")

    def cmake_args(self):
        args = [
            "-DMETATENSOR_INSTALL_BOTH_STATIC_SHARED=OFF",  # For now
            self.define("CMAKE_BUILD_TYPE", "Release"),
        ]
        return args

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsolv(CMakePackage):
    """Library for solving packages and reading repositories."""

    homepage = "https://en.opensuse.org/OpenSUSE:Libzypp_satsolver"
    url = "https://github.com/opensuse/libsolv"

    maintainers = ["charmoniumQ"]

    version("0.7.22", sha256="968aef452b5493751fa0168cd58745a77c755e202a43fe8d549d791eb16034d5")

    variant("shared", default=True, description="Build shared libraries, otherwise build static")

    depends_on("expat", type="build")
    depends_on("zlib+shared", type="run", when="+shared")
    depends_on("zlib~shared", type="build", when="~shared")

    def url_for_version(self, version):
        return f"{self.url}/archive/refs/tags/{version}.tar.gz"

    def cmake_args(self):
        if "+shared" in self.spec:
            return [
                "-DENABLE_STATIC=OFF",
                "-DDISABLE_DYNAMIC=OFF",
            ]
        else:
            return [
                "-DENABLE_STATIC=ON",
                "-DDISABLE_DYNAMIC=ON",
            ]

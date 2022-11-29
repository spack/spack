# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libreproc(CMakePackage):
    """A cross-platform process library"""

    url = "https://github.com/DaanDeMeyer/reproc"

    maintainers = ["charmoniumQ"]

    version("14.2.4", sha256="55c780f7faa5c8cabd83ebbb84b68e5e0e09732de70a129f6b3c801e905415dd")

    variant("cxx", default=False, description="Build reproc C++ bindings")
    variant("shared", default=True, description="Build shared libraries, otherwise static")

    depends_on("cmake@3.14:", type="build")
    depends_on("zlib+shared", type="run", when="+shared")
    depends_on("zlib~shared", type="build", when="~shared")

    def url_for_version(self, version):
        return f"{self.url}/archive/refs/tags/v{version}.tar.gz"

    def cmake_args(self):
        return [
            self.define_from_variant("REPROC++", "cxx"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsolv(CMakePackage):
    """Library for solving packages and reading repositories."""

    homepage = "https://en.opensuse.org/OpenSUSE:Libzypp_satsolver"
    url = "https://github.com/opensuse/libsolv/archive/0.7.22.tar.gz"

    maintainers("charmoniumQ")

    version("0.7.22", sha256="968aef452b5493751fa0168cd58745a77c755e202a43fe8d549d791eb16034d5")

    variant("shared", default=True, description="Build shared libraries")
    variant("conda", default=False, description="Include solv/conda.h")

    depends_on("expat", type="link")
    depends_on("zlib+shared", type="link", when="+shared")
    depends_on("zlib~shared", type="link", when="~shared")

    def cmake_args(self):
        return [
            self.define("ENABLE_STATIC", "~shared" in self.spec),
            self.define("DISABLE_DYNAMIC", "~shared" in self.spec),
            self.define_from_variant("ENABLE_CONDA", "conda"),
        ]

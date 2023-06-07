# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mold(CMakePackage):
    """mold: A Modern Linker"""

    homepage = "https://github.com/rui314/mold"
    url = "https://github.com/rui314/mold/archive/refs/tags/v1.11.0.tar.gz"

    maintainers("jabcross")

    version("1.11.0", sha256="99318eced81b09a77e4c657011076cc8ec3d4b6867bd324b8677974545bc4d6f")
    version("1.7.1", sha256="e155f647c4c8555697f2d9544ba2f93a67023c4fff21b5b56aa3157700e14364")

    depends_on("mimalloc")
    depends_on("openssl")
    depends_on("tbb")
    depends_on("zlib")

    def cmake_args(self):
        args = []
        args.append(self.define("MOLD_USE_SYSTEM_MIMALLOC", True))

        return args

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mold(CMakePackage):
    """mold: A Modern Linker"""

    homepage = "https://github.com/rui314/mold"
    url = "https://github.com/rui314/mold/archive/refs/tags/v1.11.0.tar.gz"

    maintainers("jabcross")

    license("MIT")

    version("2.1.0", sha256="a32bec1282671b18ea4691855aed925ea2f348dfef89cb7689cd81273ea0c5df")
    version("2.0.0", sha256="2ae8a22db09cbff626df74c945079fa29c1e5f60bbe02502dcf69191cf43527b")
    version("1.11.0", sha256="99318eced81b09a77e4c657011076cc8ec3d4b6867bd324b8677974545bc4d6f")
    version("1.7.1", sha256="fa2558664db79a1e20f09162578632fa856b3cde966fbcb23084c352b827dfa9")

    depends_on("mimalloc")
    depends_on("zlib-api")
    depends_on("openssl")
    depends_on("tbb")

    def cmake_args(self):
        args = []
        args.append(self.define("MOLD_USE_SYSTEM_MIMALLOC", True))

        return args

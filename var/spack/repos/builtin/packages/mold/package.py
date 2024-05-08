# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mold(CMakePackage):
    """mold: A Modern Linker"""

    homepage = "https://github.com/rui314/mold"
    url = "https://github.com/rui314/mold/archive/refs/tags/v1.11.0.tar.gz"

    maintainers("msimberg")

    license("MIT")

    version("2.31.0", sha256="3dc3af83a5d22a4b29971bfad17261851d426961c665480e2ca294e5c74aa1e5")
    version("2.30.0", sha256="6e5178ccafe828fdb4ba0dd841d083ff6004d3cb41e56485143eb64c716345fd")
    version("2.4.1", sha256="c9853d007d6a1b4f3e36b7314346751f4cc91bc43c76e30db51709b53b44dd68")
    version("2.4.0", sha256="be65f3d785d32ece7b3204ecaa57810847fdd25c232cf704cbfff2dafb1ac107")
    version("2.3.0", sha256="6cfc1af0214f993be1b0ae4a2f0278d32b7fc48155c15b2d03758f6d81e7250b")
    version("2.2.0", sha256="78ddddaaa004e50f8d92a13d8e792a46a1b37745fab48d39ad16aeb5a776e7c6")
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

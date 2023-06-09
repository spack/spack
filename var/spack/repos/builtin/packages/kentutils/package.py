# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities"""

    homepage = "https://github.com/ucscGenomeBrowser/kent-core"
    url = "https://github.com/ucscGenomeBrowser/kent-core/archive/refs/tags/v449.tar.gz"

    version("449", sha256="640e7997e9ce220d6ab465e944bf11e678a9e3858ec6b346b024dc6f44e84713")
    version(
        "302.1",
        commit="d8376c5d52a161f2267346ed3dc94b5dce74c2f9",
        git="https://github.com/ENCODE-DCC/kentUtils.git",
    )

    depends_on("libpng")
    depends_on("openssl")
    depends_on("libuuid")
    depends_on("mariadb")

    conflicts("%cce", when="@302.1")
    conflicts("%apple-clang", when="@302.1")
    conflicts("%clang", when="@302.1")
    conflicts("%intel", when="@302.1")
    conflicts("%nag", when="@302.1")
    conflicts("%pgi", when="@302.1")
    conflicts("%xl", when="@302.1")
    conflicts("%xl_r", when="@302.1")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class KentCore(MakefilePackage):
    """Open source UCSC Genome Browser source code: converters, tools, and libraries."""

    homepage = "https://github.com/ucscGenomeBrowser/kent-core"
    url = "https://github.com/ucscGenomeBrowser/kent-core/archive/refs/tags/v465.tar.gz"

    maintainers("teaguesterling")

    license("MIT", checked_by="teaguesterling")

    version("465", sha256="4ca31f7246aace1a4ab7bab6ef63bde3146d8f964b6f3e4fb7a594eebab3c52c")

    variant("mysql", default=False, description="Force mysql instead of mariadb")

    depends_on("libpng")
    depends_on("libuuid")
    depends_on("mysql-connector-c", when="+mysql")
    depends_on("mariadb-c-client", when="~mysql")

    def install(self, spec, prefix):
        super().install(spec, prefix)
        mkdirp(prefix.bin)
        install_tree("bin", prefix.bin)

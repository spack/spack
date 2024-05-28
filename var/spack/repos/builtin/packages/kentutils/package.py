# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities"""

    homepage = "https://genome.cse.ucsc.edu/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v453.src.tgz"

    version("465", sha256="eef17b1f3182d1d9dc99b5c73a6b0468d5d3bd80470f25d3f7706cc1372e04b0")
    version("460", sha256="b955e56ee880074521ef1ab1371491f47e66dc6fdd93b05328386dd675a635fa")
    # This version isn't present in the archive any more
    # Might be worth changing url to: https://github.com/ucscGenomeBrowser/kent-core/tags/...
    version(
        "459", 
        sha256="0b6e89a183e6385c713cf010a7aeead9da6626d8d2f78c363a4f1bc56ccccebb",
        deprecated=True,
    )

    depends_on("libpng")
    depends_on("openssl")
    depends_on("libuuid")
    depends_on("mariadb")
    depends_on("zlib-api")
    depends_on("freetype")
    depends_on("libiconv")

    def flag_handler(self, name, flags):
        if name == "ldflags":
            flags.append(f'{self.spec["libiconv"].libs.ld_flags}')
        return (flags, None, None)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)

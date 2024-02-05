# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities"""

    homepage = "https://genome.cse.ucsc.edu/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v453.src.tgz"

    version("459", sha256="0b6e89a183e6385c713cf010a7aeead9da6626d8d2f78c363a4f1bc56ccccebb")
    # The above archive only goes back to v305. v302 is left for now but deprecated. Suggest
    # this is dropped next time the package is updated (v302 is from 2014!) and the list of
    # conflicts removed.
    version(
        "302.1",
        commit="d8376c5d52a161f2267346ed3dc94b5dce74c2f9",
        git="https://github.com/ENCODE-DCC/kentUtils.git",
        deprecated=True,
    )

    depends_on("libpng")
    depends_on("openssl")
    depends_on("libuuid")
    depends_on("mariadb")
    depends_on("zlib-api")
    depends_on("freetype")
    depends_on("libiconv")

    requires("%gcc", when="@302.1")

    def setup_build_environment(self, env):
        # Builds fall over without this being manually specified
        env.append_flags("LDFLAGS", f'{self.spec["libiconv"].libs.ld_flags}')

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)

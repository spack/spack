# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities"""

    homepage = "https://genome.cse.ucsc.edu/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v453.src.tgz"

    version("453", sha256="f48fc1aa370bc3f0b874effd3087f97ecd0c65c8e3fd5ec9d9300d897006f72e")
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
    depends_on("zlib-ng")
    depends_on("freetype")
    depends_on("iconv")
    # depends_on("util-linux")

    conflicts("%cce", when="@302.1")
    conflicts("%apple-clang", when="@302.1")
    conflicts("%clang", when="@302.1")
    conflicts("%intel", when="@302.1")
    conflicts("%nag", when="@302.1")
    conflicts("%pgi", when="@302.1")
    conflicts("%xl", when="@302.1")
    conflicts("%xl_r", when="@302.1")

    def setup_build_environment(self, env):
        env.append_flags("CFLAGS", "-I{}".format(self.spec["iconv"].prefix.lib))

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sam2p(Package):
    """A raster to PostScript/PDF image conversion program"""

    homepage = "https://github.com/pts/sam2p"
    url = "https://github.com/pts/sam2p/archive/v0.49.4.tar.gz"
    git = homepage

    maintainers = ["robertu94"]

    version("master", branch="master")

    def install(self, spec, prefix):
        compile_sh = Executable("./compile.sh")
        compile_sh()
        mkdirp(prefix.bin)
        install("sam2p", prefix.bin)

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sam2p(Package):
    """A raster to PostScript/PDF image conversn program"""

    homepage = "https://github.com/pts/sam2p"
    url      = "https://github.com/pts/sam2p/archive/v0.49.4.tar.gz"
    git      = homepage

    version('master', branch='master')


    def install(self, spec, prefix):
        compile_sh = Executable("./compile.sh")
        compile_sh()
        mkdirp(prefix.bin)
        install("sam2p", prefix.bin)

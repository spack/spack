# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fermi(MakefilePackage):
    """A WGS de novo assembler based on the FMD-index for large genomes."""

    homepage = "https://github.com/lh3/fermi"
    url      = "https://github.com/downloads/lh3/fermi/fermi-1.1.tar.bz2"

    version('1.1', 'd5f006315652b6f18070b31474ca5ebb')

    depends_on('zlib')
    depends_on('perl', type='run')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('fermi', prefix.bin)
        install('run-fermi.pl', prefix.bin)

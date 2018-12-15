# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flash(MakefilePackage):
    """FLASH (Fast Length Adjustment of SHort reads) is a very
    fast and accurate software tool to merge paired-end reads
    from next-generation sequencing experiments."""

    homepage = "https://ccb.jhu.edu/software/FLASH/"
    url      = "https://sourceforge.net/projects/flashpage/files/FLASH-1.2.11.tar.gz"

    version('1.2.11', 'e4d355023a766afaaab2d62f912b605c')

    depends_on('zlib')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('flash', prefix.bin)

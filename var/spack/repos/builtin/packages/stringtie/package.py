# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Stringtie(MakefilePackage):
    """StringTie is a fast and highly efficient assembler of RNA-Seq alignments
       into potential transcripts."""

    homepage = "https://ccb.jhu.edu/software/stringtie"
    url      = "https://github.com/gpertea/stringtie/archive/v1.3.3b.tar.gz"

    version('1.3.4d', '0134c0adc264efd31a1df4301b33bfcf3b3fe96bd3990ce3df90819bad9af968')
    version('1.3.4a', '2a191ef6512242a3a5778cf7718bb6af')
    version('1.3.3b', '11a43260b18e4272182380e922445d88')

    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('stringtie', prefix.bin)

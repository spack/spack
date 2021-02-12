# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Phantompeakqualtools(RPackage):
    """This package computes informative enrichment and quality measures for
       ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data."""

    homepage = "https://github.com/kundajelab/phantompeakqualtools"
    url      = "https://github.com/kundajelab/phantompeakqualtools/archive/1.2.tar.gz"

    version('1.2.2',   sha256='b31263b64aefe97bdc4d7fae138f515a7d7a60cd05031d38dd89a10f9ee10cd1')
    version('1.2.1.1', sha256='4b1445fcbe361cc86dc64f9df9def73bb6830cb961fa8372ea8545b86440e829')
    version('1.2.1',   sha256='48705856c8179a08c26801444e88c7360abbedc97fba4624d3d62314a011777b')
    version('1.2', sha256='86cbcca80b65f150b1cdbea673d8a47caba88c2db6b3b567a80f2c797c9a1668')

    depends_on('awk')
    depends_on('samtools')
    depends_on('r', type=('build', 'run'))
    depends_on('r-phantompeakqualtools', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('run_spp.R', prefix.bin)

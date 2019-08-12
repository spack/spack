# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Phantompeakqualtools(RPackage):
    """This package computes informative enrichment and quality measures for
       ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data."""

    homepage = "https://github.com/kundajelab/phantompeakqualtools"
    url      = "https://github.com/kundajelab/phantompeakqualtools/archive/1.2.tar.gz"

    version('1.2', 'e94943a42132b9ff2886f006ab34c121')

    depends_on('awk')
    depends_on('samtools')
    depends_on('r', type=('build', 'run'))
    depends_on('r-phantompeakqualtools', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('run_spp.R', prefix.bin)

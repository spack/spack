# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cleaveland4(Package):
    """CleaveLand4: Analysis of degradome data to find sliced miRNA and siRNA
       targets"""

    homepage = "https://github.com/MikeAxtell/CleaveLand4"
    url      = "https://github.com/MikeAxtell/CleaveLand4/archive/v4.4.tar.gz"

    version('4.4', 'cf62a1de715a612fc8bd5a62364e69db')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-math-cdf', type=('build', 'run'))
    depends_on('bowtie')
    depends_on('viennarna')
    depends_on('r', type=('build', 'run'))
    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('CleaveLand4.pl', prefix.bin)
        with working_dir('GSTAr_v1-0'):
            install('GSTAr.pl', prefix.bin)

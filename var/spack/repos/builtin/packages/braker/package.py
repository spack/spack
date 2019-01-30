# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Braker(Package):
    """BRAKER is a pipeline for unsupervised RNA-Seq-based genome annotation
       that combines the advantages of GeneMark-ET and AUGUSTUS"""

    homepage = "http://exon.gatech.edu/braker1.html"
    url      = "http://bioinf.uni-greifswald.de/augustus/binaries/BRAKER_v2.1.0.tar.gz"
    list_url = "http://bioinf.uni-greifswald.de/augustus/binaries/old"

    version('2.1.0', '5f974abcceb9f96a11668fa20a6f6a56')
    version('1.11', '297efe4cabdd239b710ac2c45d81f6a5',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/BRAKER1_v1.11.tar.gz')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-scalar-util-numeric', type=('build', 'run'))
    depends_on('perl-parallel-forkmanager', type=('build', 'run'))
    depends_on('perl-file-which', type=('build', 'run'))
    depends_on('augustus@3.2.3')
    depends_on('genemark-et')
    depends_on('bamtools')
    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install('braker.pl', prefix.bin)
        install('filterGenemark.pl', prefix.bin)
        install('filterIntronsFindStrand.pl', prefix.bin)
        install('helpMod.pm', prefix.lib)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix.lib)

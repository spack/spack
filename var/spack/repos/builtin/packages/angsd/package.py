# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Angsd(MakefilePackage):
    """Angsd is a program for analysing NGS data. The software can handle a
       number of different input types from mapped reads to imputed genotype
       probabilities. Most methods take genotype uncertainty into account
       instead of basing the analysis on called genotypes. This is especially
       useful for low and medium depth data."""

    homepage = "https://github.com/ANGSD/angsd"
    url      = "https://github.com/ANGSD/angsd/archive/0.919.tar.gz"

    version('0.921', sha256='8892d279ce1804f9e17fe2fc65a47e5498e78fc1c1cb84d2ca2527fd5c198772')
    version('0.919', sha256='c2ea718ca5a5427109f4c3415e963dcb4da9afa1b856034e25c59c003d21822a')

    depends_on('htslib')
    conflicts('^htslib@1.6:', when='@0.919')

    def setup_run_environment(self, env):
        env.set('R_LIBS', self.prefix.R)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('angsd', join_path(prefix.bin))
        install_tree('R', prefix.R)
        install_tree('RES', prefix.RES)
        install_tree('scripts', prefix.scripts)

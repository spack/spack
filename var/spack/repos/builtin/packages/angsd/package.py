# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
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

    version('0.921', '3702db035396db602c7f74728b1a5a1f')
    version('0.919', '79d342f49c24ac00d35934f2617048d4')

    depends_on('htslib')
    conflicts('^htslib@1.6:', when='@0.919')

    def setup_environment(self, spack_env, run_env):
        run_env.set('R_LIBS', prefix.R)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('angsd', join_path(prefix.bin))
        install_tree('R', prefix.R)
        install_tree('RES', prefix.RES)
        install_tree('scripts', prefix.scripts)

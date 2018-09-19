##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

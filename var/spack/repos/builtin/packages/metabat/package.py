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


class Metabat(SConsPackage):
    """MetaBAT, an efficient tool for accurately reconstructing single
    genomes from complex microbial communities."""

    homepage = "https://bitbucket.org/berkeleylab/metabat"
    url      = "https://bitbucket.org/berkeleylab/metabat/get/v2.12.1.tar.gz"

    version('2.12.1', 'c032f47a8b24e58a5a9fefe52cb6e0f8')

    depends_on('boost@1.55.0:', type=('build', 'run'))
    depends_on('perl', type='run')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)

    def install_args(self, spec, prefix):
        return ["PREFIX={0}".format(prefix)]

    @run_after('build')
    def fix_perl_scripts(self):
        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl',
                    'aggregateBinDepths.pl')

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl',
                    'aggregateContigOverlapsByBin.pl')

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


class Beast1(Package):
    """BEAST is a cross-platform program for Bayesian
       analysis of molecular sequences using MCMC."""

    homepage = "http://beast.community/"
    url      = "https://github.com/beast-dev/beast-mcmc/releases/download/v1.8.4/BEASTv1.8.4.tgz"

    version('1.10.0', 'bcf2f2c074319360ec8a2ebad57d2e57', 
            url='https://github.com/beast-dev/beast-mcmc/releases/download/v1.10.0/BEAST_v1.10.0.tgz')
    version('1.8.4', 'cb8752340c1f77a22d39ca4fe09687b0')

    variant('beagle', default=True, description='Build with libbeagle support')

    depends_on('java', type='run')
    depends_on('libbeagle', type=('build', 'link', 'run'), when="+beagle")

    def setup_environment(self, spack_env, run_env):
        run_env.set('BEAST1', self.prefix)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('examples', prefix.examples)
        install_tree('images', prefix.images)
        install_tree('lib', prefix.lib)
        install_tree('doc', prefix.doc)

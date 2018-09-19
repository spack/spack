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


class RPhantompeakqualtools(RPackage):
    """Computes informative enrichment and quality measures for
       ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data. This is a modified version
       of r-spp to be used in conjunction with the phantompeakqualtools
       package."""

    homepage = "https://github.com/kundajelab/phantompeakqualtools"
    url      = "https://github.com/kundajelab/phantompeakqualtools/raw/master/spp_1.14.tar.gz"

    version('1.14', '4de207d570999170c1bf45bcba8c6d2d')

    depends_on('boost@1.41.0:')
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
    depends_on('r-snowfall', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))

    conflicts('%gcc@6:')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)

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


class Talass(CMakePackage):
    """TALASS: Topological Analysis of Large-Scale Simulations
    This package compiles the talass tool chain thar implements
    various topological algorithms to analyze large scale data.
    The package is organized hierarchical FileFormat < Statistics
    < StreamingTopology and any of the subsets can be build stand-
    alone."""

    homepage = "http://www.cedmav.org/research/project/16-talass.html"
    git      = "git@bitbucket.org:cedmav/talass.git"

    version('2018-09-21', commit='bf7da9bb54a026d8cb575b5be28b9c88095cb307')

    # The default precision and index space sizes
    variant('precision', default='32', values=('32', '64'),
            description='Precision of the function values')
    variant('global', default='32', values=('16', '32', '64'),
            description='Number of bits used for the global index space')
    variant('local', default='32', values=('16', '32', '64'),
            description='Number of bits used for the local index space')

    root_cmakelists_dir = 'StreamingTopology'

    def cmake_args(self):
        variants = self.spec.variants

        args = []

        if int(variants['local'].value) > int(variants['global'].value):
            raise InstallError('The global index space (%d bits) must be at least as large\
 as the local index space (% bits)' % (variants['global'].value,
                                       variants['local'].value))

        if variants['precision'].value == '32':
            args.append('-DFUNCTION_TYPE=float')
        elif variants['precision'].value == '64':
            args.append('-DFUNCTION_TYPE=double')

        # Set global index space
        args.append('-DGLOBAL_INDEX_TYPE=uint{0}_t'.format(
            variants['global'].value))

        # Set local index space
        args.append('-DLOCAL_INDEX_TYPE=uint{0}_t'.format(
            variants['local'].value))

        # Deal with the PROJECT_INSTALL_PREFIX to enable Talass super builds
        args.append('-DPROJECT_INSTALL_PREFIX=%s' % self.prefix)

        return args

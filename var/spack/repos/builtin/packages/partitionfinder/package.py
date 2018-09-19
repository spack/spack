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


class Partitionfinder(Package):
    """PartitionFinder is free open source software to select best-fit
       partitioning schemes and models of molecular evolution for
       phylogenetic analyses."""

    homepage = "https://github.com/brettc/partitionfinder"
    url      = "https://github.com/brettc/partitionfinder/archive/v2.1.1.tar.gz"

    version('2.1.1', 'b1b6539f93146c69b967cf92459ae28a')

    depends_on('python@2.7.10:2.999', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pytables', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('partfinder', prefix.partfinder)
        install_tree('timings', prefix.timings)
        install('PartitionFinderMorphology.py', prefix.bin)
        install('PartitionFinderProtein.py', prefix.bin)
        install('PartitionFinder.py', prefix.bin)

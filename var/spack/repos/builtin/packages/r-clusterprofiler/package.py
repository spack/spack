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


class RClusterprofiler(RPackage):
    """This package implements methods to analyze and visualize functional
    profiles (GO and KEGG) of gene and gene clusters."""

    homepage = "https://www.bioconductor.org/packages/clusterProfiler/"
    git      = "https://git.bioconductor.org/packages/clusterProfiler.git"

    version('3.4.4', commit='b86b00e8405fe130e439362651a5567736e2d9d7')

    depends_on('r@3.4.0:3.4.9', when='@3.4.4')
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-rvcheck', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-gosemsim', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-dose', type=('build', 'run'))

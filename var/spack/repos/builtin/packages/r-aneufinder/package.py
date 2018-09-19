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


class RAneufinder(RPackage):
    """This package implements functions for CNV calling, plotting,
    export and analysis from whole-genome single cell sequencing data."""

    homepage = "https://www.bioconductor.org/packages/AneuFinder/"
    git      = "https://git.bioconductor.org/packages/AneuFinder.git"

    version('1.4.0', commit='e5bdf4d5e4f84ee5680986826ffed636ed853b8e')

    depends_on('r@3.4.0:3.4.9', when='@1.4.0')
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-aneufinderdata', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-bamsignals', type=('build', 'run'))
    depends_on('r-dnacopy', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-ggdendro', type=('build', 'run'))
    depends_on('r-reordercluster', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))

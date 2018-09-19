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


class RPhyloseq(RPackage):
    """phyloseq provides a set of classes and tools to facilitate the import,
    storage, analysis, and graphical display of microbiome census data."""

    homepage = "https://www.bioconductor.org/packages/phyloseq/"
    git      = "https://git.bioconductor.org/packages/phyloseq.git"

    version('1.20.0', commit='107d1d5e3437a6e33982c06a548d3cc91df2a7e0')

    depends_on('r@3.4.0:3.4.9', when='@1.20.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-biomformat', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))

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


class RAdegenet(RPackage):
    """Toolset for the exploration of genetic and genomic data. Adegenet
    provides formal (S4) classes for storing and handling various genetic
    data, including genetic markers with varying ploidy and hierarchical
    population structure ('genind' class), alleles counts by populations
    ('genpop'), and genome-wide SNP data ('genlight'). It also implements
    original multivariate methods (DAPC, sPCA), graphics, statistical tests,
    simulation tools, distance and similarity measures, and several spatial
    methods. A range of both empirical and simulated datasets is also provided
    to illustrate various methods."""

    homepage = "https://github.com/thibautjombart/adegenet/wiki"
    url      = "https://cran.r-project.org/src/contrib/adegenet_2.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/adegenet"

    version('2.0.1', 'ecb1220ce7c9affaba2987bc7f38adda')

    depends_on('r@2.14:')
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-seqinr', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-dplyr@0.4.1:', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))

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


class RGosemsim(RPackage):
    """The semantic comparisons of Gene Ontology (GO) annotations provide
    quantitative ways to compute similarities between genes and gene
    groups, and have became important basis for many bioinformatics
    analysis approaches. GOSemSim is an R package for semantic similarity
    computation among GO terms, sets of GO terms, gene products and gene
    clusters. GOSemSim implemented five methods proposed by Resnik,
    Schlicker, Jiang, Lin and Wang respectively."""

    homepage = "https://www.bioconductor.org/packages/GOSemSim/"
    git      = "https://git.bioconductor.org/packages/GOSemSim.git"

    version('2.2.0', commit='247434790e6c8cf99e5643f569390362b8c87c52')

    depends_on('r@3.4.0:3.4.9', when='@2.2.0')
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))

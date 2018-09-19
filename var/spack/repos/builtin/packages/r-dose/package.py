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


class RDose(RPackage):
    """This package implements five methods proposed by Resnik, Schlicker,
    Jiang, Lin and Wang respectively for measuring semantic similarities
    among DO terms and gene products. Enrichment analyses including
    hypergeometric model and gene set enrichment analysis are also
    implemented for discovering disease associations of high-throughput
    biological data."""

    homepage = "https://www.bioconductor.org/packages/DOSE/"
    git      = "https://git.bioconductor.org/packages/DOSE.git"

    version('3.2.0', commit='71f563fc39d02dfdf65184c94e0890a63b96b86b')

    depends_on('r@3.4.0:3.4.9', when='@3.2.0')
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-gosemsim', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-fgsea', type=('build', 'run'))
    depends_on('r-do-db', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))

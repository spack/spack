# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

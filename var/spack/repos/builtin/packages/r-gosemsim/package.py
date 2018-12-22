# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

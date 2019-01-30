# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAbaenrichment(RPackage):
    """The package ABAEnrichment is designed to test for enrichment
    of user defined candidate genes in the set of expressed genes in
    different human brain regions. The core function 'aba_enrich'
    integrates the expression of the candidate gene set (averaged
    across donors) and the structural information of the brain using
    an ontology, both provided by the Allen Brain Atlas project.
    'aba_enrich' interfaces the ontology enrichment software FUNC to
    perform the statistical analyses. Additional functions provided
    in this package like 'get_expression' and 'plot_expression'
    facilitate exploring the expression data. From version 1.3.5
    onwards genomic regions can be provided as input, too; and from
    version 1.5.9 onwards the function 'get_annotated_genes' offers
    an easy way to obtain annotations of genes to enriched or
    user-defined brain regions."""

    homepage = "https://bioconductor.org/packages/ABAEnrichment/"
    git      = "https://git.bioconductor.org/packages/ABAEnrichment.git"

    version('1.6.0', commit='d2a0467dcb7aa6e103e3b83dccd6510b0e142ac1')

    depends_on('r@3.4.0:3.4.9', when='@1.6.0')
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-abadata', type=('build', 'run'))

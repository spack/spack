# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAcde(RPackage):
    """This package provides a multivariate inferential analysis method
    for detecting differentially expressed genes in gene expression data.
    It uses artificial components, close to the data's principal
    components but with an exact interpretation in terms of differential
    genetic expression, to identify differentially expressed genes while
    controlling the false discovery rate (FDR). The methods on this
    package are described in the vignette or in the article
    'Multivariate Method for Inferential Identification of
    Differentially Expressed Genes in Gene Expression Experiments' by
    J. P. Acosta, L. Lopez-Kleine and S. Restrepo
    (2015, pending publication)."""

    homepage = "https://www.bioconductor.org/packages/acde/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/acde_1.6.0.tar.gz"

    version('1.6.0', 'e92ce91f75bab3bb1d79995bec1b42cc')

    depends_on('r-boot', type=('build', 'run'))

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAbadata(RPackage):
    """Provides the data for the gene expression enrichment analysis
    conducted in the package 'ABAEnrichment'. The package includes three
    datasets which are derived from the Allen Brain Atlas: (1) Gene
    expression data from Human Brain (adults) averaged across donors,
    (2) Gene expression data from the Developing Human Brain pooled into
    five age categories and averaged across donors and (3) a developmental
    effect score based on the Developing Human Brain expression data.
    All datasets are restricted to protein coding genes."""

    homepage = "https://bioconductor.org/packages/ABAData/"
    url      = "https://bioconductor.org/packages/release/data/experiment/src/contrib/ABAData_1.6.0.tar.gz"

    version('1.6.0', '9adfb9fbb39ad05cf72852a229476fb7')

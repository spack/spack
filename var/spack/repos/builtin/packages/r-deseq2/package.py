# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDeseq2(RPackage):
    """Differential gene expression analysis based on the negative binomial
       distribution

       Estimate variance-mean dependence in count data from high-throughput
       sequencing assays and test for differential expression based on a model
       using the negative binomial distribution."""

    homepage = "https://bioconductor.org/packages/DESeq2"
    git      = "https://git.bioconductor.org/packages/DESeq2.git"

    version('1.24.0', commit='3ce7fbbebac526b726a6f85178063d02eb0314bf')
    version('1.22.2', commit='3c6a89b61add635d6d468c7fa00192314f8ca4ce')
    version('1.20.0', commit='7e88ea5c5e68473824ce0af6e10f19e22374cb7c')
    version('1.18.1', commit='ef65091d46436af68915124b752f5e1cc55e93a7')
    version('1.16.1', commit='f41d9df2de25fb57054480e50bc208447a6d82fb')

    depends_on('r@3.6.0:3.6.9', when='@1.24.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.22.2', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.20.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.18.1', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.1', type=('build', 'run'))

    depends_on('r-rcpp', when='@1.16.1:', type=('build', 'run'))
    depends_on('r-rcpparmadillo', when='@1.16.1:', type=('build', 'run'))

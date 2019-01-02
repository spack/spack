# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDeseq2(RPackage):
    """Estimate variance-mean dependence in count data from
    high-throughput sequencing assays and test for differential
    expression based on a model using the negative binomial
    distribution."""

    homepage = "https://www.bioconductor.org/packages/DESeq2/"
    git      = "https://git.bioconductor.org/packages/DESeq2.git"

    version('1.20.0', commit='7e88ea5c5e68473824ce0af6e10f19e22374cb7c')
    version('1.18.1', commit='ef65091d46436af68915124b752f5e1cc55e93a7')
    version('1.16.1', commit='0a815574382704a08ef8b906eceb0296f81cded5')

    depends_on("r-rcpparmadillo", type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-geneplotter', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.1:1.19', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.20.0', type=('build', 'run'))

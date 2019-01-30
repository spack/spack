# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSummarizedexperiment(RPackage):
    """The SummarizedExperiment container contains one or more assays, each
       represented by a matrix-like object of numeric or other mode. The rows
       typically represent genomic ranges of interest and the columns
       represent samples."""

    homepage = "https://bioconductor.org/packages/SummarizedExperiment/"
    git      = "https://git.bioconductor.org/packages/SummarizedExperiment.git"

    version('1.10.0', commit='7ad2e991c8285bfc4b2e15b29d94cc86d07f8f2b')
    version('1.8.1', commit='9d8a29aa9c78bbc7dcc6472537e13fc0d11dc1f7')
    version('1.6.5', commit='ec69cd5cfbccaef148a9f6abdfb3e22e888695d0')

    depends_on('r-genomicranges@1.27.22:', when='@1.6.5', type=('build', 'run'))
    depends_on('r-genomicranges@1.29.14:', when='@1.8.1', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.17:', when='@1.10.0', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-delayedarray@0.1.9:', when='@1.6.5', type=('build', 'run'))
    depends_on('r-delayedarray@0.3.20:', when='@1.8.1:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.10.0', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.16:', when='@1.10.0', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.10.0', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.3:', when='@1.6.5:', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.6.5:1.9.9', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.10.0', type=('build', 'run'))

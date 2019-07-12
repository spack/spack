# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDeseq(RPackage):
    """Differential gene expression analysis based on the negative binomial
       distribution

       Estimate variance-mean dependence in count data from high-throughput
       sequencing assays and test for differential expression based on a model
       using the negative binomial distribution"""

    homepage = "https://bioconductor.org/packages/DESeq"
    git      = "https://git.bioconductor.org/packages/DESeq.git"

    version('1.36.0', commit='db4af67b49d3bd8c321d19efbe9415cd2e4ddb7e')
    version('1.34.1', commit='e86f1b03a30bc02de4bfd4a0759af2f65cb48c62')
    version('1.32.0', commit='e3d623b815b53d79eae7cdd09d097cc6098d28c9')
    version('1.30.0', commit='90c93d991dd980d538c13b0361d3345f9546794e')
    version('1.28.0', commit='738371466e6ccf00179fd35b617c8ba0e1e91630')

    depends_on('r@3.6.0:3.6.9', when='@1.36.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.34.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.32.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.30.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.0', type=('build', 'run'))

    depends_on('r-biobase@2.21.7:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.7.5:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-genefilter', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-geneplotter', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-lattice', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-locfit', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-mass', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', when='@1.28.0:', type=('build', 'run'))

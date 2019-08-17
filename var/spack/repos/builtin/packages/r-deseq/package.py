# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDeseq(RPackage):
    """Estimate variance-mean dependence in count data from
    high-throughput sequencing assays and test for differential
    expression based on a model using the negative binomial
    distribution."""

    homepage = "https://www.bioconductor.org/packages/DESeq/"
    git      = "https://git.bioconductor.org/packages/DESeq.git"

    version('1.28.0', commit='738371466e6ccf00179fd35b617c8ba0e1e91630')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-geneplotter', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))

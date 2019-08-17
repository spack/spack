# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSseq(RPackage):
    """Shrinkage estimation of dispersion in Negative Binomial models for
       RNA-seq experiments with small sample size"""

    homepage = "https://www.bioconductor.org/packages/sSeq/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/sSeq_1.20.0.tar.gz"

    version('1.20.0', sha256='0fddcb238a6c401987843debe5b46dc03c22a1ee04df670f0d502e86a4f2144f')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))

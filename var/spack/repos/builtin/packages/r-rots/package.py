# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRots(RPackage):
    """Calculates the Reproducibility-Optimized Test Statistic (ROTS)
       for differential testing in omics data."""

    homepage = "https://bioconductor.org/packages/release/bioc/html/ROTS.html"
    git      = "https://git.bioconductor.org/packages/ROTS.git"

    version('1.8.0', commit='02e3c6455bb1afe7c4cc59ad6d4d8bae7b01428b')

    depends_on('r@3.5.0:3.5.9', when='@1.8.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))

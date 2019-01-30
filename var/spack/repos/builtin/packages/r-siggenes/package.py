# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSiggenes(RPackage):
    """Identification of differentially expressed genes and estimation of the
       False Discovery Rate (FDR) using both the Significance Analysis of
       Microarrays (SAM) and the Empirical Bayes Analyses of Microarrays
       (EBAM)."""

    homepage = "http://bioconductor.org/packages/siggenes/"
    git      = "https://git.bioconductor.org/packages/siggenes.git"

    version('1.50.0', commit='b1818f26e1449005ffd971df6bda8da0303080bc')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.50.0')

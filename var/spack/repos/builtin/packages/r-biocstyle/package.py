# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiocstyle(RPackage):
    """Provides standard formatting styles for Bioconductor PDF and HTML
    documents. Package vignettes illustrate use and functionality."""

    homepage = "https://www.bioconductor.org/packages/BiocStyle/"
    git      = "https://git.bioconductor.org/packages/BiocStyle.git"

    version('2.4.1', commit='ef10764b68ac23a3a7a8ec3b6a6436187309c138')

    depends_on('r-bookdown', type=('build', 'run'))
    depends_on('r-knitr@1.12:', type=('build', 'run'))
    depends_on('r-rmarkdown@1.2:', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.4.1')

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSva(RPackage):
    """Surrogate Variable Analysis."""

    homepage = "https://www.bioconductor.org/packages/sva/"
    git      = "https://git.bioconductor.org/packages/sva.git"

    version('3.24.4', commit='ed2ebb6e33374dc9ec50e6ea97cc1d9aef836c73')

    depends_on('r@3.4.0:3.4.9', when='@3.24.4')
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))

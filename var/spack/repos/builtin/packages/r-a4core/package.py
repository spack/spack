# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4core(RPackage):
    """Automated Affymetrix Array Analysis Core Package."""

    homepage = "https://www.bioconductor.org/packages/a4Core/"
    git      = "https://git.bioconductor.org/packages/a4Core.git"

    version('1.24.0', commit='c871faa3e1ab6be38a9ea3018816cf31b58b0ed3')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))

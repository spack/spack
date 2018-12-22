# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMulttest(RPackage):
    """Resampling-based multiple hypothesis testing"""

    homepage = "https://www.bioconductor.org/packages/multtest/"
    git      = "https://git.bioconductor.org/packages/multtest.git"

    version('2.32.0', commit='c5e890dfbffcc3a3f107303a24b6085614312f4a')

    depends_on('r@3.4.0:3.4.9', when='@2.32.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))

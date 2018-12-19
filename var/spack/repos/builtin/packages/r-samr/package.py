# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSamr(RPackage):
    """Significance Analysis of Microarrays."""

    homepage = "https://cran.r-project.org/package=samr"
    url      = "https://cran.rstudio.com/src/contrib/samr_2.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/samr"
    version('2.0', 'e8f50b8b25069d03d42c2c61c72b0da0')

    depends_on('r-impute', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))

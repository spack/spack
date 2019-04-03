# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRhmmer(RPackage):
    """rhmmer: Utilities Parsing 'HMMER' Results"""

    homepage = "https://cran.r-project.org/package=rhmmer"
    url      = "https://cran.r-project.org/src/contrib/rhmmer_0.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rhmmer/"

    version('0.1.0', sha256='5022cefc9ba335160c1ad8d1b614610ae0ad48287c9fdbaf8f8966149358e520')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-testthat', type=('build', 'run'))
    depends_on('r-covr', type=('build', 'run'))

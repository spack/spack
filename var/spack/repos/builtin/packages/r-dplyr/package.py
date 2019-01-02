# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDplyr(RPackage):
    """A fast, consistent tool for working with data frame like objects, both
    in memory and out of memory."""

    homepage = "https://cran.r-project.org/package=dplyr"
    url      = "https://cran.r-project.org/src/contrib/dplyr_0.7.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dplyr"

    version('0.7.5', sha256='2fbd8f316a59670076d43a0fe854654621941ee5f621ea5f0185a3f5daafda50')
    version('0.7.4', '9edee9b2db9831c2438054d0d2c1647d')
    version('0.7.3', 'f9760b796917747e9dcd927ebb531c7d')
    version('0.5.0', '1fcafcacca70806eea2e6d465cdb94ef')

    depends_on('r-tidyselect@0.2.3', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-bindr@0.1.1', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-bindrcpp', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))

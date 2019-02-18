# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTibble(RPackage):
    """Provides a 'tbl_df' class that offers better checking and printing
    capabilities than traditional data frames."""

    homepage = "https://github.com/tidyverse/tibble"
    url      = "https://cran.rstudio.com/src/contrib/tibble_1.3.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tibble"
    version('1.3.4', '298e81546f999fb0968625698511b8d3')
    version('1.2', 'bdbc3d67aa16860741add6d6ec20ea13')
    version('1.1', '2fe9f806109d0b7fadafb1ffafea4cb8')

    depends_on('r@3.1.2:')

    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-lazyeval@0.1.10:', type=('build', 'run'), when='@:1.3.0')
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'), when='@1.3.1:')

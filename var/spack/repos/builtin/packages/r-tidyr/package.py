# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTidyr(RPackage):
    """An evolution of 'reshape2'. It's designed specifically for data tidying
    (not general reshaping or aggregating) and works well with 'dplyr' data
    pipelines."""

    homepage = "https://github.com/hadley/tidyr"
    url      = "https://cran.r-project.org/src/contrib/tidyr_0.7.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tidyr"

    version('0.7.2', '42d723bf04c5c1c59e27a8be14f3a6b6')
    version('0.5.1', '3cadc869510c054ed93d374ab44120bd')

    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-dplyr@0.7.0:', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-tidyselect', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RModelr(RPackage):
    """Functions for modelling that help you seamlessly integrate modelling
       into a pipeline of data manipulation and visualisation."""

    homepage = "https://github.com/hadley/modelr"
    url      = "https://cran.r-project.org/src/contrib/modelr_0.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/modelr"

    version('0.1.1', 'ce5fd088fb7850228ab1e34d241a975d')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-broom', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))

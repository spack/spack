# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPurrr(RPackage):
    """A complete and consistent functional programming toolkit for R."""

    homepage = "http://purrr.tidyverse.org/"
    url      = "https://cran.r-project.org/src/contrib/purrr_0.2.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/purrr"

    version('0.2.4', 'd9a11e6c14771beb3ebe8f4771a552f3')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))

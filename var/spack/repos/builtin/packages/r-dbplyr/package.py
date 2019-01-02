# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDbplyr(RPackage):
    """A 'dplyr' back end for databases that allows you to work with remote
       database tables as if they are in-memory data frames. Basic features
       works with any database that has a 'DBI' back end; more advanced
       features require 'SQL' translation to be provided by the package
       author."""

    homepage = "https://github.com/tidyverse/dbplyr"
    url      = "https://cran.r-project.org/src/contrib/dbplyr_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dbplyr"

    version('1.1.0', 'a66a08d1046e3e44bfe17e65ce72a1d0')

    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))

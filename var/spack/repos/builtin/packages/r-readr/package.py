# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReadr(RPackage):
    """The goal of 'readr' is to provide a fast and friendly way to read
       rectangular data (like 'csv', 'tsv', and 'fwf'). It is designed to
       flexibly parse many types of data found in the wild, while still cleanly
       failing when data unexpectedly changes."""

    homepage = "https://cran.rstudio.com/web/packages/readr/index.html"
    url      = "https://cran.rstudio.com/src/contrib/readr_1.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/readr/"

    version('1.1.1', 'cffb6669664f6a0f6fe172542e64cb47')

    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-hms', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))

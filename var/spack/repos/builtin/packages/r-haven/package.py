# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHaven(RPackage):
    """Import foreign statistical formats into R via the embedded 'ReadStat' C
       library, <https://github.com/WizardMac/ReadStat>."""

    homepage = "http://haven.tidyverse.org/"
    url      = "https://cran.r-project.org/src/contrib/haven_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/haven"

    version('1.1.0', '8edd4b7683f8c36b5bb68582ac1b8733')

    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-hms', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-forcats', type=('build', 'run'))

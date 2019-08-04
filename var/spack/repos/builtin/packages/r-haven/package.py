# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHaven(RPackage):
    """Import foreign statistical formats into R via the embedded 'ReadStat' C
       library, <https://github.com/WizardMac/ReadStat>."""

    homepage = "http://haven.tidyverse.org/"
    url      = "https://cloud.r-project.org/src/contrib/haven_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/haven"

    version('2.1.1', sha256='90bcb4e7f24960e7aa3e15c06b95cd897f08de149cec43fd8ba110b14526068a')
    version('2.1.0', sha256='c0a1cf1b039549fb3ad833f9644ed3f142790236ad755d2ee7bd3d8109e3ae74')
    version('1.1.0', '8edd4b7683f8c36b5bb68582ac1b8733')

    depends_on('r@3.2:')
    depends_on('r-rcpp@0.11.4:', type=('build', 'run'))
    depends_on('r-readr@0.1.0:', type=('build', 'run'))
    depends_on('r-hms', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-forcats', type=('build', 'run'))

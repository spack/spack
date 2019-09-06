# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMco(RPackage):
    """Functions for multiple criteria optimization using genetic algorithms
       and related test problems"""

    homepage = "https://github.com/cran/mco"
    url      = "https://cloud.r-project.org/src/contrib/mco_1.0-15.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mco"

    version('1.0-15.1', '1768dea61d0561d71be2bbc6ac3dccfa')
    version('1.0-15', '0b444e085c59d919611224e86b5637f8')

    depends_on('r@3.0.0:', type=('build', 'run'))

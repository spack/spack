# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RViridis(RPackage):
    """viridis: Default Color Maps from 'matplotlib'"""

    homepage = "https://github.com/sjmgarnier/viridis"
    url      = "https://cran.r-project.org/src/contrib/viridis_0.4.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/viridis"

    version('0.4.0', 'f874384cbedf459f6c309ddb40b354ea')

    depends_on('r@2.1.0:')
    depends_on('r-viridislite@0.2.0:', type=('build', 'run'))
    depends_on('r-ggplot2@1.0.1:', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))

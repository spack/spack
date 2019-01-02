# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFactominer(RPackage):
    """FactoMineR: Multivariate Exploratory Data Analysis and Data Mining"""

    homepage = "http://factominer.free.fr"
    url      = "https://cran.r-project.org/src/contrib/FactoMineR_1.35.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/FactoMineR"

    version('1.35', 'bef076181ce942016114dd7a6f5c2348')

    depends_on('r@3.3.0:')
    depends_on('r-car', type=('build', 'run'))
    # depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-ellipse', type=('build', 'run'))
    depends_on('r-flashclust', type=('build', 'run'))
    # depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-leaps', type=('build', 'run'))
    # depends_on('r-mass', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))

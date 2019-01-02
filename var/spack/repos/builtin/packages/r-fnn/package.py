# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFnn(RPackage):
    """Cover-tree and kd-tree fast k-nearest neighbor search algorithms and
    related applications including KNN classification, regression and
    information measures are implemented."""

    homepage = "https://cran.r-project.org/web/packages/FNN/index.html"
    url      = "https://cran.r-project.org/src/contrib/FNN_1.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/FNN"

    version('1.1',   '8ba8f5b8be271785593e13eae7b8c393')
    version('1.0',   'e9a47dc69d1ba55165be0877b8443fe0')
    version('0.6-4', '1c105df9763ceb7b13989cdbcb542fcc')
    version('0.6-3', 'f0f0184e50f9f30a36ed5cff24d6cff2')
    version('0.6-2', '20648ba934ea32b1b00dafb75e1a830c')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-chemometrics', type=('build', 'run'))

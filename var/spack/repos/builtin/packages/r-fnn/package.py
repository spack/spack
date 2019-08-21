# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFnn(RPackage):
    """Cover-tree and kd-tree fast k-nearest neighbor search algorithms and
    related applications including KNN classification, regression and
    information measures are implemented."""

    homepage = "https://cloud.r-project.org/package=FNN"
    url      = "https://cloud.r-project.org/src/contrib/FNN_1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/FNN"

    version('1.1.3', sha256='de763a25c9cfbd19d144586b9ed158135ec49cf7b812938954be54eb2dc59432')
    version('1.1.2.2', sha256='b51a60fbbeff58c48cc90c2023c48972d5082d68efd02284c17ccd9820986326')
    version('1.1',   '8ba8f5b8be271785593e13eae7b8c393')
    version('1.0',   'e9a47dc69d1ba55165be0877b8443fe0')
    version('0.6-4', '1c105df9763ceb7b13989cdbcb542fcc')
    version('0.6-3', 'f0f0184e50f9f30a36ed5cff24d6cff2')
    version('0.6-2', '20648ba934ea32b1b00dafb75e1a830c')

    depends_on('r@3.0.0:', type=('build', 'run'))

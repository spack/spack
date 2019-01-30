# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIrlba(RPackage):
    """Fast and memory efficient methods for truncated singular and eigenvalue
    decompositions and principal component analysis of large sparse or dense
    matrices."""

    homepage = "https://cran.r-project.org/web/packages/irlba/index.html"
    url      = "https://cran.r-project.org/src/contrib/irlba_2.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/irlba"

    version('2.1.2', '290940abf6662ed10c0c5a8db1bc6e88')
    version('2.0.0', '557674cf8b68fea5b9f231058c324d26')

    depends_on('r-matrix', type=('build', 'run'))

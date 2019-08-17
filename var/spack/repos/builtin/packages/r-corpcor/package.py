# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCorpcor(RPackage):
    """Efficient Estimation of Covariance and (Partial) Correlation"""

    homepage = "https://cran.r-project.org/package=corpcor"
    url      = "https://cran.r-project.org/src/contrib/corpcor_1.6.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/corpcor"

    version('1.6.9', '7f447d9f389e5d7dedb5fe5baedca925')

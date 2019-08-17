# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCorpcor(RPackage):
    """Efficient Estimation of Covariance and (Partial) Correlation"""

    homepage = "https://cloud.r-project.org/package=corpcor"
    url      = "https://cloud.r-project.org/src/contrib/corpcor_1.6.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/corpcor"

    version('1.6.9', '7f447d9f389e5d7dedb5fe5baedca925')

    depends_on('r@3.0.2:', type=('build', 'run'))

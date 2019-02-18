# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLars(RPackage):
    """Efficient procedures for fitting an entire lasso sequence with the cost
    of a single least squares fit."""

    homepage = "https://cran.r-project.org/web/packages/lars/index.html"
    url      = "https://cran.r-project.org/src/contrib/lars_1.2.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/lars"

    version('1.2',   '2571bae325f6cba1ad0202ea61695b8c')
    version('1.1',   'e94f6902aade09b13ec25ba2381384e5')
    version('0.9-8', 'e6f9fffab2d83898f6d3d811f04d177f')

    depends_on('r@2.10:', type=('build', 'run'))

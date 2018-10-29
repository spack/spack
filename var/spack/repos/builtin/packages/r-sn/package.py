# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSn(RPackage):
    """Build and manipulate probability distributions of the skew-normal
    family and some related ones, notably the skew-t family, and provide
    related statistical methods for data fitting and diagnostics, in the
    univariate and the multivariate case."""

    homepage = "https://cran.r-project.org/web/packages/sn/index.html"
    url      = "https://cran.r-project.org/src/contrib/sn_1.5-0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/sn"

    version('1.5-0', 'a3349773be950199d7f4c17954be56d1')
    version('1.4-0', 'cfa604317ea54224b06abd1cec179375')
    version('1.3-0', '84d02ba2ab5ca6f3644626013e7ce36d')
    version('1.2-4', 'bf3a47b05016326e910fdb4cc4967e4d')
    version('1.2-3', '290ae511d974a6beb4c3c79c0106858f')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))

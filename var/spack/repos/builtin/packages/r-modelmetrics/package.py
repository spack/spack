# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RModelmetrics(RPackage):
    """Collection of metrics for evaluating models written in C++ using
    'Rcpp'."""

    homepage = "https://cran.r-project.org/package=ModelMetrics"
    url      = "https://cran.r-project.org/src/contrib/ModelMetrics_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ModelMetrics"

    version('1.1.0', 'd43175001f0531b8810d2802d76b7b44')

    depends_on('r@3.2.2:')

    depends_on('r-rcpp', type=('build', 'run'))

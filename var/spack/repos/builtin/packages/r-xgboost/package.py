# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RXgboost(RPackage):
    """Extreme Gradient Boosting, which is an efficient implementation of
    gradient boosting framework. This package is its R interface. The package
    includes efficient linear model solver and tree learning algorithms. The
    package can automatically do parallel computation on a single machine which
    could be more than 10 times faster than existing gradient boosting
    packages. It supports various objective functions, including regression,
    classification and ranking. The package is made to be extensible, so that
    users are also allowed to define their own objectives easily."""

    homepage = "https://github.com/dmlc/xgboost"
    url      = "https://cran.r-project.org/src/contrib/xgboost_0.6-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/xgboost"

    version('0.6-4', '86e517e3ce39f8a01de796920f6b425e')
    version('0.4-4', 'c24d3076058101a71de4b8af8806697c')

    depends_on('r@3.3.0:')

    depends_on('r-matrix@1.1-0:', type=('build', 'run'))
    depends_on('r-data-table@1.9.6:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-stringi@0.5.2:', type=('build', 'run'))

    # This is not listed as required, but installation fails without it
    # ERROR: dependency 'stringr' is not available for package 'xgboost'
    depends_on('r-stringr', type=('build', 'run'))

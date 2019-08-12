# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcpparmadillo(RPackage):
    """'Rcpp' Integration for the 'Armadillo' Templated Linear
    Algebra Library."""

    homepage = "https://cran.r-project.org/package=RcppArmadillo"
    url      = "https://cran.r-project.org/src/contrib/RcppArmadillo_0.8.100.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RcppArmadillo"

    version('0.8.100.1.0', 'a79c0ee967f502702414bc3c80c88f56')

    depends_on('r-rcpp', type=('build', 'run'))

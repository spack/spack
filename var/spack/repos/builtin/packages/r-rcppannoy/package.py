# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcppannoy(RPackage):
    """RcppAnnoy: 'Rcpp' Bindings for 'Annoy', a Library for Approximate
       NearestNeighbors"""

    homepage = "https://cran.r-project.org/package=RcppAnnoy"
    url      = "https://cran.r-project.org/src/contrib/RcppAnnoy_0.0.12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RcppAnnoy"

    version('0.0.12', sha256='8f736cbbb4a32c80cb08ba4e81df633846d725f27867e983af2012966eac0eac')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rcpp@0.11.3:', type=('build', 'run'))

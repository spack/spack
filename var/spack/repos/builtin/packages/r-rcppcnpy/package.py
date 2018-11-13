# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcppcnpy(RPackage):
    """Rcpp bindings for NumPy files."""

    homepage = "https://github.com/eddelbuettel/rcppcnpy"
    url      = "https://cran.r-project.org/src/contrib/RcppCNPy_0.2.9.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/RcppCNPy"

    version('0.2.9', '7f63354d15928b6716830c2975b3baf0')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('cnpy')
    depends_on('r-rcpp', type=('build', 'run'))

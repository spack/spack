# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcppcctz(RPackage):
    """'Rcpp' Access to the 'CCTZ' timezone library is provided. 'CCTZ' is a
       C++ library for translating between absolute and civil times using the
       rules of a time zone. The 'CCTZ' source code, released under the
       Apache 2.0 License, is included in this package. See
       <https://github.com/google/cctz> for more details."""

    homepage = "https://github.com/eddelbuettel/rcppcctz"
    url      = "https://cran.r-project.org/src/contrib/RcppCCTZ_0.2.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RcppCCTZ"

    version('0.2.3', '7635014a1cc696a3f00a7619fb5d7008')

    depends_on('r-rcpp', type=('build', 'run'))

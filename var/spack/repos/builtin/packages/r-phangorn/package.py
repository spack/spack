# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPhangorn(RPackage):
    """Package contains methods for estimation of phylogenetic trees and
       networks using Maximum Likelihood, Maximum Parsimony, distance methods
       and Hadamard conjugation. Allows to compare trees, models selection and
       offers visualizations for trees and split networks."""

    homepage = "https://cran.r-project.org/package=phangorn"
    url      = "https://cran.r-project.org/src/contrib/phangorn_2.3.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/phangorn"

    version('2.3.1', '85e7309900d061432508ab6f7e3e627e')

    depends_on('r-ape@5.0:', type=('build', 'run'))
    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-igraph@1.0:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-fastmatch', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))

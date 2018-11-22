# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBayesm(RPackage):
    """Bayesian Inference for Marketing/Micro-Econometrics"""

    homepage = "https://cran.r-project.org/web/packages/bayesm/index.html"
    url      = "https://cran.r-project.org/src/contrib/bayesm_3.1-0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/bayesm"

    version('3.1-0.1', '34998382cafd3e7972d8a03245eac768')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLearnbayes(RPackage):
    """LearnBayes contains a collection of functions helpful in learning the
    basic tenets of Bayesian statistical inference. It contains functions for
    summarizing basic one and two parameter posterior distributions and
    predictive distributions. It contains MCMC algorithms for summarizing
    posterior distributions defined by the user. It also contains functions
    for regression models, hierarchical models, Bayesian tests, and
    illustrations of Gibbs sampling."""

    homepage = "https://CRAN.R-project.org/package=LearnBayes"
    url      = "https://cran.r-project.org/src/contrib/LearnBayes_2.15.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/LearnBayes"

    version('2.15', '213713664707bc79fd6d3a109555ef76')

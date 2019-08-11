# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://cloud.r-project.org/package=LearnBayes"
    url      = "https://cloud.r-project.org/src/contrib/LearnBayes_2.15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/LearnBayes"

    version('2.15.1', sha256='9b110858456523ca0b2a63f22013c4e1fbda6674b9d84dc1f4de8bffc5260532')
    version('2.15', '213713664707bc79fd6d3a109555ef76')

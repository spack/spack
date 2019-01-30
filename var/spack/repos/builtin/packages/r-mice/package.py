# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMice(RPackage):
    """Multiple imputation using Fully Conditional Specification (FCS)
    implemented by the MICE algorithm as described in Van Buuren and
    Groothuis-Oudshoorn (2011) <doi:10.18637/jss.v045.i03>.

    Each variable has its own imputation model. Built-in imputation models are
    provided for continuous data (predictive mean matching, normal), binary
    data (logistic regression), unordered categorical data (polytomous logistic
    regression) and ordered categorical data (proportional odds). MICE can
    also impute continuous two-level data (normal model, pan, second-level
    variables). Passive imputation can be used to maintain consistency between
    variables. Various diagnostic plots are available to inspect the quality
    of the imputations."""

    homepage = "https://cran.r-project.org/package=mice"
    url      = "https://cran.r-project.org/src/contrib/mice_3.0.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mice"

    version('3.0.0', 'fb54a29679536c474c756cca4538d7e3')

    depends_on('r-broom', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mitml', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))

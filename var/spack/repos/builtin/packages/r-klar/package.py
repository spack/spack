# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RKlar(RPackage):
    """Miscellaneous functions for classification and visualization, e.g.
    regularized discriminant analysis, sknn() kernel-density naive Bayes, an
    interface to 'svmlight' and stepclass() wrapper variable selection for
    supervised classification, partimat() visualization of classification rules
    and shardsplot() of cluster results as well as kmodes() clustering for
    categorical data, corclust() variable clustering, variable extraction from
    different variable clustering models and weight of evidence
    preprocessing."""

    homepage = "https://cloud.r-project.org/package=klaR"
    url      = "https://cloud.r-project.org/src/contrib/klaR_0.6-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/klaR"

    version('0.6-15', sha256='5bfe5bc643f8a64b222317732c26e9f93be297cdc318a869f15cc9ab0d9e0fae')

    depends_on('r@2.10.0:',    type=('build', 'run'))
    depends_on('r-mass',       type=('build', 'run'))
    depends_on('r-combinat',  type=('build', 'run'))
    depends_on('r-questionr', type=('build', 'run'))

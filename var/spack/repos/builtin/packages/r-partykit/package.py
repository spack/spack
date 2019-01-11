# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RPartykit(RPackage):
    """A toolkit with infrastructure for representing, summarizing, and
    visualizing tree-structured regression and classification models. This
    unified infrastructure can be used for reading/coercing tree models from
    different sources ('rpart', 'RWeka', 'PMML') yielding objects that share
    functionality for print()/plot()/predict() methods. Furthermore, new and
    improved reimplementations of conditional inference trees (ctree()) and
    model-based recursive partitioning (mob()) from the 'party' package are
    provided based on the new infrastructure."""

    homepage = "http://partykit.r-forge.r-project.org/partykit"
    url      = "https://cran.r-project.org/src/contrib/partykit_1.1-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/partykit"

    version('1.1-1', '8fcb31d73ec1b8cd3bcd9789639a9277')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-formula', type=('build', 'run'))

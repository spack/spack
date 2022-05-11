# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDistributional(RPackage):
    """Functions for Base Types and Core R and 'Tidyverse' Features.

    Vectorised distribution objects with tools for manipulating, visualising,
    and using probability distributions. Designed to allow model prediction
    outputs to return distributions rather than their parameters, allowing
    users to directly interact with predictive distributions in a data-oriented
    workflow. In addition to providing generic replacements for p/d/q/r
    functions, other useful statistics can be computed including means,
    variances, intervals, and highest density regions."""

    cran = "distributional"

    version('0.3.0', sha256='fab36c7346617d8f2ca4b3cd0e3c9da93cb2f95fb7f102a3ae88670e694751d6')
    version('0.2.2', sha256='028e5a91aabe3a676eb7b7f3dc907f7f34735a123fe0d9adcabc03476504435f')

    depends_on('r-vctrs@0.3.0:', type=('build', 'run'))
    depends_on('r-rlang@0.4.5:', type=('build', 'run'))
    depends_on('r-generics', type=('build', 'run'))
    depends_on('r-ellipsis', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-farver', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-lifecycle', type=('build', 'run'))

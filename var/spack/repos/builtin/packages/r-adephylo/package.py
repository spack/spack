# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RAdephylo(RPackage):
    """Exploratory Analyses for the Phylogenetic Comparative Method.

    Multivariate tools to analyze comparative data, i.e. a phylogeny and some
    traits measured for each taxa."""

    cran = "adephylo"

    version('1.1-11', sha256='154bf2645eac4493b85877933b9445442524ca4891aefe4e80c294c398cff61a')

    depends_on('r-ade4@1.7-10:', type=('build', 'run'))
    depends_on('r-phylobase', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-adegenet', type=('build', 'run'))

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RScuttle(RPackage):
    """Single-Cell RNA-Seq Analysis Utilities.

    Provides basic utility functions for performing single-cell analyses,
    focusing on simple normalization, quality control and data transformations.
    Also provides some helper functions to assist development of other
    packages."""

    bioc = "scuttle"

    version('1.4.0', commit='b335263dd56bb859b5dd3ea27ee00dffa0215313')
    version('1.0.4', commit='a827e2759d80e6c3510e2f8fd4bd680274206d9f')

    depends_on('r-singlecellexperiment', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-delayedarray', type=('build', 'run'))
    depends_on('r-delayedmatrixstats', type=('build', 'run'))
    depends_on('r-beachmat', type=('build', 'run'))

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RYaimpute(RPackage):
    """Nearest Neighbor Observation Imputation and Evaluation Tools.

    Performs nearest neighbor-based imputation using one or more alternative
    approaches to processing multivariate data. These include methods based on
    canonical correlation analysis, canonical correspondence analysis, and a
    multivariate adaptation of the random forest classification and regression
    techniques of Leo Breiman and Adele Cutler. Additional methods are also
    offered. The package includes functions for comparing the results from
    running alternative techniques, detecting imputation targets that are
    notably distant from reference observations, detecting and correcting for
    bias, bootstrapping and building ensemble imputations, and mapping
    results."""

    cran = "yaImpute"

    version('1.0-32', sha256='08eee5d851b80aad9c7c80f9531aadd50d60e4b16b3a80657a50212269cd73ff')

    depends_on('r@3.0:', type=('build', 'run'))

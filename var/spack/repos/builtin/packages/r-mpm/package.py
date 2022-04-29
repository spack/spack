# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RMpm(RPackage):
    """Multivariate Projection Methods.

    Exploratory graphical analysis of multivariate data, specifically gene
    expression data with different projection methods: principal component
    analysis, correspondence analysis, spectral map analysis."""

    cran = "mpm"

    version('1.0-22', sha256='d3ba4053cd57a189cb65c5fa20e6a4152374aead8c985254cb6e550e36e23272')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))

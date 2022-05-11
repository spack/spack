# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RAdespatial(RPackage):
    """Multivariate Multiscale Spatial Analysis.

    Tools for the multiscale spatial analysis of multivariate data. Several
    methods are based on the use of a spatial weighting matrix and its
    eigenvector decomposition (Moran's Eigenvectors Maps, MEM). Several
    approaches are described in the review Dray et al (2012)
    <doi:10.1890/11-1183.1>."""

    cran = "adespatial"

    version('0.3-14', sha256='a2ef7549c1ed7a23651716c633b25eaff468af8ccbf2e9fcd164e485984cbfbf')
    version('0.3-8', sha256='e3fd3209ce3f0a862a0794187e8c884f1697c87c96e569a2f51f252e00022906')

    depends_on('r-ade4@1.7-13:', type=('build', 'run'))
    depends_on('r-adegraphics', type=('build', 'run'))
    depends_on('r-adephylo', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))

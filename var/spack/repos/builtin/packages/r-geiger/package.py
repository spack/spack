# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeiger(RPackage):
    """Methods for fitting macroevolutionary models to phylogenetic trees."""

    homepage = "https://cran.r-project.org/package=geiger"
    url      = "https://cran.r-project.org/src/contrib/geiger_2.0.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/geiger"

    version('2.0.6', 'e5e1a407ea56805227d0f91bf6d95afc')

    depends_on('r-ape@3.0:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-subplex', type=('build', 'run'))
    depends_on('r-desolve@1.7:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rcpp@0.9.0:', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-ncbit', type=('build', 'run')) 
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))

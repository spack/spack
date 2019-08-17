# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpdep(RPackage):
    """A collection of functions to create spatial weights matrix objects from
    polygon contiguities, from point patterns by distance and tessellations,
    for summarizing these objects, and for permitting their use in spatial
    data analysis, including regional aggregation by minimum spanning tree;
    a collection of tests for spatial autocorrelation, including global
    Moran's I, APLE, Geary's C, Hubert/Mantel general cross product statistic,
    Empirical Bayes estimates and AssunasReis Index, Getis/Ord G and
    multicoloured join count statistics, local Moran's I and Getis/Ord G,
    saddlepoint approximations and exact tests for global and local Moran's I;
    and functions for estimating spatial simultaneous autoregressive (SAR) lag
    and error models, impact measures for lag models, weighted and unweighted
    SAR and CAR spatial regression models, semi-parametric and Moran
    eigenvector spatial filtering, GM SAR error models, and generalized spatial
    two stage least squares models."""

    homepage = "https://r-forge.r-project.org/projects/spdep"
    url      = "https://cran.r-project.org/src/contrib/spdep_0.6-13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/spdep"

    version('0.6-13', 'bfc68b3016b4894b152ecec4b86f85d1')

    depends_on('r@3.0:')
    depends_on('r-sp@1.0:', type=('build', 'run'))
    depends_on('r-learnbayes', type=('build', 'run'))
    depends_on('r-deldir', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-gmodels', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))

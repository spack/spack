##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

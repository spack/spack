# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDtw(RPackage):
    """A comprehensive implementation of dynamic time warping (DTW) algorithms
    in R. DTW computes the optimal (least cumulative distance) alignment
    between points of two time series."""

    homepage = "https://cran.r-project.org/web/packages/dtw/index.html"
    url      = "https://cran.r-project.org/src/contrib/dtw_1.18-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dtw"

    version('1.18-1', '5e9995a198a62f28045c29461265d536')
    version('1.17-1', 'e8be988fe528acd6b44afdf5aa06b745')
    version('1.16',   '260bd22d9db429394eb39739db4a4686')
    version('1.15',   'd3b6fdb0b866ff2e5b178c37bcfc7c55')
    version('1.14-3', 'a7b878e8dda7a61df22356d0a81540c5')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-proxy', type=('build', 'run'))

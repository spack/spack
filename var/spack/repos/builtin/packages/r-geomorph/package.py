# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeomorph(RPackage):
    """Geometric Morphometric Analyses of 2D/3D Landmark Data.

    Read, manipulate, and digitize landmark data, generate shape variables via
    Procrustes analysis for points, curves and surfaces, perform shape
    analyses, and provide graphical depictions of shapes and patterns of shape
    variation."""

    cran = "geomorph"

    version('4.0.1', sha256='9d54fba96dd8b8f2dcc8d0e4c427f6232bed1934da41f25084c16ec0b2c71117')
    version('3.3.2', sha256='5f1d17cb98c54e40c4bbc650f7ccb5cb26e8d63934f810644facc69e91c1b7b7')
    version('3.1.2', sha256='29cf1c484f756cb44808cfdbc20137a6fbc4bd0c5c6f98c6c3f397c5aebda8f1')
    version('3.1.1', sha256='8eb222011433100860b308beef6f02ade7c421785f575ab4461ee25e38dfa1bd')
    version('3.0.7', sha256='68f8942e1a5bc3f0298c9f5b8f69c4702c8e12ecb2275d740fda4d04d66d38e1')
    version('3.0.5', sha256='7a3a587b253770a5e7e70536234dee13e6a073f1fdf1d644ae4f11d2eb95b104')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', type=('build', 'run'), when='@3.3.2:')
    depends_on('r-rrpp', type=('build', 'run'), when='@3.0.7:')
    depends_on('r-rrpp@1.0.0:', type=('build', 'run'), when='@4.0.1:')
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'), when='@:3.1.1,4.0.1:')
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'), when='@4.0.1:')

    depends_on('r-geiger', type=('build', 'run'), when='@:3.1.1')

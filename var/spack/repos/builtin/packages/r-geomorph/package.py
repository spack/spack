# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeomorph(RPackage):
    """Read, manipulate, and digitize landmark data, generate shape variables
       via Procrustes analysis for points, curves and surfaces, perform shape
       analyses, and provide graphical depictions of shapes and patterns of
       shape variation."""

    homepage = "https://cran.r-project.org/package=geomorph"
    url      = "https://cran.r-project.org/src/contrib/geomorph_3.0.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/geomorph"

    version('3.0.7', '68f8942e1a5bc3f0298c9f5b8f69c4702c8e12ecb2275d740fda4d04d66d38e1')
    version('3.0.5', '240e69fe260ca3ef4d84b4281d61396c')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-geiger', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rrpp', type=('build', 'run'), when='@3.0.7:')

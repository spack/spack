# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RS2(RPackage):
    """Spherical Geometry Operators Using the S2 Geometry Library.

    Provides R bindings for Google's s2 library for geometric calculations on
    the sphere. High-performance constructors and exporters provide high
    compatibility with existing spatial packages, transformers construct new
    geometries from existing geometries, predicates provide a means to select
    geometries based on spatial relationships, and accessors extract
    information about geometries."""

    cran = "s2"

    version('1.0.7', sha256='2010c1c6ae29938ec9cd153a8b2c06a333ea4d647932369b2fc7d0c68d6d9e3f')
    version('1.0.4', sha256='3c274ebae33aa5473f94afb3066c6f388aced17ff3b5f6add9edcc9af22b985e')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-wk', type=('build', 'run'))
    depends_on('r-wk@0.5.0:', type=('build', 'run'), when='@1.0.7:')
    depends_on('openssl@1.0.1:', when='@1.0.7:')

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RGeometries(RPackage):
    """Convert Between R Objects and Geometric Structures.

    Geometry shapes in 'R' are typically represented by matrices (points,
    lines), with more complex shapes being lists of matrices (polygons).
    'Geometries' will convert various 'R' objects into these shapes. Conversion
    functions are available at both the 'R' level, and through 'Rcpp'."""

    cran = "geometries"

    version('0.2.0', sha256='8cf5094f3c2458fef5d755799c766afd27c66cd1c292574a6ab532d608360314')

    depends_on('r-rcpp', type=('build', 'run'))

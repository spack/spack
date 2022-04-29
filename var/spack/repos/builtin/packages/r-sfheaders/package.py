# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RSfheaders(RPackage):
    """Converts Between R Objects and Simple Feature Objects.

    Converts between R and Simple Feature 'sf' objects, without depending on
    the Simple Feature library. Conversion functions are available at both the
    R level, and through 'Rcpp'."""

    cran = "sfheaders"

    version('0.4.0', sha256='86bcd61018a0491fc8a1e7fb0422c918296287b82be299a79ccee8fcb515e045')

    depends_on('r-geometries@0.2.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))

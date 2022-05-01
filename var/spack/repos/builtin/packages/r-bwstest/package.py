# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBwstest(RPackage):
    """Baumgartner Weiss Schindler Test of Equal Distributions.

    Performs the 'Baumgartner-Weiss-Schindler' two-sample test of equal
    probability distributions, <doi:10.2307/2533862>. Also performs similar
    rank-based tests for equal probability distributions due to Neuhauser
    <doi:10.1080/10485250108832874> and Murakami
    <doi:10.1080/00949655.2010.551516>."""

    cran = "BWStest"

    version('0.2.2', sha256='faff1dd698f1673a6befacb94d14281077d4c19be035a0a3bf85d77c1dfd5509')

    depends_on('r-memoise', type=('build', 'run'))
    depends_on('r-rcpp@0.12.3:', type=('build', 'run'))

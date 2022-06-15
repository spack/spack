# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVipor(RPackage):
    """Plot Categorical Data Using Quasirandom Noise and Density Estimates.

    Generate a violin point plot, a combination of a violin/histogram plot and
    a scatter plot by offsetting points within a category based on their
    density using quasirandom noise."""

    cran = "vipor"

    version('0.4.5', sha256='7d19251ac37639d6a0fed2d30f1af4e578785677df5e53dcdb2a22771a604f84')
    version('0.4.4', sha256='5abfd7869dae42ae2e4f52206c23433a43b485b1220685e445877ee5864a3f5c')

    depends_on('r@3.0.0:', type=('build', 'run'))

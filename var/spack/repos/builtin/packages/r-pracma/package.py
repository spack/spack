# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPracma(RPackage):
    """Practical Numerical Math Functions.

    Provides a large number of functions from numerical analysis and linear
    algebra, numerical optimization, differential equations, time series, plus
    some well-known special mathematical functions. Uses 'MATLAB' function
    names where appropriate to simplify porting."""

    cran = "pracma"

    version('2.3.6', sha256='17ac83fd48c9155e00dc3f0433f95723505dc73d046860afd9001866d699b8de')
    version('2.2.9', sha256='0cea0ff5e88643df121e07b9aebfe57084c61e11801680039752f371fe87bf1e')

    depends_on('r@3.1.0:', type=('build', 'run'))

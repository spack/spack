# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RUrca(RPackage):
    """Unit Root and Cointegration Tests for Time Series Data.

    Unit root and cointegration tests encountered in applied econometric
    analysis are implemented."""

    cran = "urca"

    version('1.3-0', sha256='621cc82398e25b58b4a16edf000ed0a1484d9a0bc458f734e97b6f371cc76aaa')

    depends_on('r@2.0.0:', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))

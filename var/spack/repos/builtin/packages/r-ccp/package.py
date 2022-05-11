# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RCcp(RPackage):
    """Significance Tests for Canonical Correlation Analysis (CCA).

    Significance tests for canonical correlation analysis, including asymptotic
    tests and a Monte Carlo method"""

    cran = 'CCP'

    version('1.1', sha256='9d21cda05221f1a458fe2938cd5ff0e89711ef058865d25f9894a275c7805d1e')

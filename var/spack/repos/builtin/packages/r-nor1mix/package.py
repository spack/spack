# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RNor1mix(RPackage):
    """Normal aka Gaussian (1-d) Mixture Models (S3 Classes and Methods).

    One dimensional Normal Mixture Models Classes, for, e.g., density
    estimation or clustering algorithms research and teaching; providing the
    widely used Marron-Wand densities. Efficient random number generation and
    graphics; now fitting to data by ML (Maximum Likelihood) or EM
    estimation."""

    cran = "nor1mix"

    version('1.3-0', sha256='9ce4ee92f889a4a4041b5ea1ff09396780785a9f12ac46f40647f74a37e327a0')
    version('1.2-3', sha256='435e6519e832ef5229c51ccb2619640e6b50dfc7470f70f0c938d18a114273af')

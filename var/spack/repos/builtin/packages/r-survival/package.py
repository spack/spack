# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSurvival(RPackage):
    """Contains the core survival analysis routines, including definition of
    Surv objects, Kaplan-Meier and Aalen-Johansen (multi-state) curves, Cox
    models, and parametric accelerated failure time models."""

    homepage = "https://cloud.r-project.org/package=survival"
    url      = "https://cloud.r-project.org/src/contrib/survival_2.41-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/survival"

    version('2.44-1.1', sha256='55b151e15fcd24ccb3acf60331c9a7ad82bc10f3841ab3be9bc2a37e9ee751b9')
    version('2.44-1', sha256='82c44afa41fe4504295855f1da4a5940c3289dfd61bc664bf211bb67c051a909')
    version('2.41-3', '6edb8093d1177775685dc26f3ce78d73')
    version('2.40-1', 'a2474b656cd723791268e3114481b8a7')
    version('2.39-5', 'a3cc6b5762e8c5c0bb9e64a276710be2')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))

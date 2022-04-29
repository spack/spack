# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Crtm(CMakePackage):
    """The Community Radiative Transfer Model (CRTM) package.
    The CRTM is composed of four important modules for gaseous transmittance,
    surface emission and reflection, cloud and aerosol absorption and
    scattering, and a solver for a radiative transfer."""

    homepage = "https://www.jcsda.org/jcsda-project-community-radiative-transfer-model"
    url      = "https://github.com/NOAA-EMC/EMC_crtm/archive/refs/tags/v2.3.0.tar.gz"

    maintainers = ['t-brown', 'edwardhartnett', 'kgerheiser', 'Hang-Lei-NOAA']

    version('2.3.0', sha256='3e2c87ae5498c33dd98f9ede5c39e33ee7f298c7317b12adeb552e3a572700ce')

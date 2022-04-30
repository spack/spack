# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Crtm(CMakePackage):
    """The Community Radiative Transfer Model (CRTM) package.
    The CRTM is composed of four important modules for gaseous transmittance,
    surface emission and reflection, cloud and aerosol absorption and
    scattering, and a solver for a radiative transfer."""

    homepage = "https://www.jcsda.org/jcsda-project-community-radiative-transfer-model"
    git = 'https://github.com/JCSDA/crtm.git'

    maintainers = ['t-brown', 'edwardhartnett', 'kgerheiser', 'Hang-Lei-NOAA']

    depends_on('netcdf-fortran', when='@2.4.0:')

    # ecbuild release v2.4.0 is broken
    # add ecbuild dependency for next release with fix
    # depends_on('ecbuild', when='@2.4.0:', type=('build'))

    # REL-2.4.0_emc (v2.4.0 ecbuild does not work)
    version('2.4.0', commit='a831626', skip_git_lfs=True)
    # Uses the tip of REL-2.3.0_emc branch
    version('2.3.0', commit='99760e6', skip_git_lfs=True)

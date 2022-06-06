# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class UfsWeatherModelEnv(BundlePackage):
    """Development environment for ufs-weathermodel-bundle"""

    homepage = "https://github.com/ufs-community/ufs-weather-model"
    git      = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers = ['kgerheiser', 'climbfuji']

    version('main')
    version('1.0.0', preferred=True)

    variant('debug', default=False, description='Build a debug version of certain dependencies (ESMF, MAPL)')

    with when('@main'):
        depends_on('base-env', type='run')

        depends_on('fms@2022.01', type='run')
        depends_on('bacio',       type='run')
        depends_on('crtm',        type='run')
        depends_on('g2',          type='run')
        depends_on('g2tmpl',      type='run')
        depends_on('ip',          type='run')
        depends_on('sp',          type='run')
        depends_on('w3nco',       type='run')

        depends_on('esmf~debug', type='run', when='~debug')
        depends_on('esmf+debug', type='run', when='+debug')
        depends_on('mapl~debug', type='run', when='~debug')
        depends_on('mapl+debug', type='run', when='+debug')

    with when('@1.0.0'):
        depends_on('base-env@1.0.0', type='run')

        depends_on('fms@2022.01',   type='run')
        depends_on('bacio@2.4.1',   type='run')
        depends_on('crtm@2.3.0',    type='run')
        depends_on('g2@3.4.5',      type='run')
        depends_on('g2tmpl@1.10.0', type='run')
        depends_on('ip@3.3.3',      type='run')
        depends_on('sp@2.3.3',      type='run')
        depends_on('w3nco@2.4.1',   type='run')

        depends_on('esmf8.3.0b09~debug', type='run', when='~debug')
        depends_on('esmf8.3.0b09+debug', type='run', when='+debug')
        depends_on('mapl@2.11.0~debug',  type='run', when='~debug')
        depends_on('mapl@2.11.0+debug',  type='run', when='+debug')

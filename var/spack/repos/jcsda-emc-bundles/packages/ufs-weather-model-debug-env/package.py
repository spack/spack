# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class UfsWeatherModelDebugEnv(BundlePackage):
    """Development environment for ufs-weathermodel-bundle"""

    homepage = "https://github.com/ufs-community/ufs-weather-model"
    git      = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers = ['kgerheiser', 'climbfuji']

    version('main', branch='main')

    depends_on('esmf+debug', type='run')
    depends_on('mapl+debug', type='run')

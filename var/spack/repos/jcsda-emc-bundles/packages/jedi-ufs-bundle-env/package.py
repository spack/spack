# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUfsBundleEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    # DH* TODO - we should rename this to just ufs-bundle to match the other bundles
    homepage = "https://github.com/JCSDA/ufs-jedi-bundle"
    git      = "https://github.com/JCSDA/ufs-jedi-bundle.git"

    maintainers = ['climbfuji', 'mark-a-potts']

    version('main', branch='main')

    depends_on('base-env', type='run')
    depends_on('jedi-base-env', type='run')

    depends_on('ufs-weather-model-env', type='run')

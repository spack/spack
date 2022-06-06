# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUfsEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    # DH* TODO - we should rename this to just ufs-bundle to match the other bundles
    homepage = "https://github.com/JCSDA/ufs-jedi-bundle"
    git      = "https://github.com/JCSDA/ufs-jedi-bundle.git"

    maintainers = ['climbfuji', 'mark-a-potts']

    version('main')
    version('1.0.0', preferred=True)

    with when('@main'):
        depends_on('base-env',                    type='run')
        depends_on('jedi-base-env',               type='run')
        depends_on('ufs-weather-model-env',       type='run')

    with when('@1.0.0'):
        depends_on('base-env@1.0.0',              type='run')
        depends_on('jedi-base-env@1.0.0',         type='run')
        # DH* TODO UPDATE
        depends_on('ufs-weather-model-env@1.0.0', type='run')

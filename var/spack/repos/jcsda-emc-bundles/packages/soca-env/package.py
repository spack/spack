# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class SocaEnv(BundlePackage):
    """Development environment for soca-bundle"""

    homepage = "https://github.com/JCSDA/soca"
    git      = "https://github.com/JCSDA/soca.git"

    maintainers = ['climbfuji', 'travissluka']

    version('main', branch='main')
    version('1.0.0', preferred=True)

    with when('@main'):
        depends_on('base-env',            type='run')
        depends_on('jedi-base-env',       type='run')
        depends_on('nco',                 type='run')

    with when('@1.0.0'):
        depends_on('base-env@1.0.0',      type='run')
        depends_on('jedi-base-env@1.0.0', type='run')
        depends_on('nco@5.0.6',           type='run')

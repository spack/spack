# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class SocaBundleEnv(BundlePackage):
    """Development environment for soca-bundle"""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/soca"
    git      = "https://github.com/JCSDA-internal/soca.git"

    maintainers = ['climbfuji', 'travissluka' ]

    version('main', branch='main')

    depends_on('base-env', type='run')
    depends_on('jedi-base-env', type='run')

    depends_on('nco', type='run')

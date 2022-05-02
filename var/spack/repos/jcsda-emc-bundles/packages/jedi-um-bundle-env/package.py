# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUmBundleEnv(BundlePackage):
    """Development environment for um-bundle"""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/um-bundle"
    git      = "https://github.com/JCSDA-internal/um-bundle.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')

    depends_on('base-env', type='run')
    depends_on('jedi-base-env', type='run')

    depends_on('shumlib', type='run')
    depends_on('fiat', type='run')
    depends_on('ectrans', type='run')

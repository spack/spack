# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediFv3BundleEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    homepage = "https://github.com/JCSDA-internal/fv3-bundle"
    git      = "https://github.com/JCSDA-internal/fv3-bundle.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')

    depends_on('base-env', type='run')
    depends_on('jedi-base-env', type='run')

    depends_on('fms-jcsda@release-stable')

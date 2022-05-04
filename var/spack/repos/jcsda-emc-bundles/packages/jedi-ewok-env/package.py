# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediEwokEnv(BundlePackage):
    """Development environment for ewok"""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/ewok"
    git      = "https://github.com/JCSDA-internal/ewok.git"

    maintainers = ['climbfuji', '@ericlingerfelt']

    version('main', branch='main')

    depends_on('base-env', type='run')
    depends_on('jedi-base-env', type='run')

    depends_on('py-boto3', type='run')
    depends_on('py-cartopy', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('py-ruamel-yaml', type='run')
    depends_on('py-ruamel-yaml-clib', type='run')

    depends_on('ecflow', type='run')

    conflicts('%gcc platform=darwin', msg='jedi-ewok-env does ' + \
        'not build with gcc (11?) on macOS (12), use apple-clang')

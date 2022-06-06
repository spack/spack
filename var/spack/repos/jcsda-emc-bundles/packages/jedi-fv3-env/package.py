# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediFv3Env(BundlePackage):
    """Development environment for fv3-bundle"""

    homepage = "https://github.com/JCSDA/fv3-bundle"
    git      = "https://github.com/JCSDA/fv3-bundle.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main')
    version('1.0.0', preferred=True)

    with when('@main'):
        depends_on('base-env',          type='run')
        depends_on('fms@release-jcsda', type='run')
        depends_on('jedi-base-env',     type='run')

    with when('@1.0.0'):
        depends_on('base-env@1.0.0',      type='run')
        depends_on('fms@release-jcsda',   type='run')
        depends_on('jedi-base-env@1.0.0', type='run')

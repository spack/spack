# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUmBundleEnv(BundlePackage):
    """Development environment for um-bundle"""

    # Note. Internal only, but this repo was being frozen
    # in May 2022 and won't be developed any further.
    homepage = "https://github.com/JCSDA-internal/um-bundle"
    git      = "https://github.com/JCSDA-internal/um-bundle.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')
    version('1.0.0', preferred=True)

    with when('@main'):
        depends_on('base-env',                 type='run')
        depends_on('ectrans',                  type='run')
        depends_on('fiat',                     type='run')
        depends_on('jedi-base-env',            type='run')
        depends_on('shumlib',                  type='run')

    with when('@1.0.0'):
        depends_on('base-env@1.0.0',           type='run')
        depends_on('ectrans@1.0.0',            type='run')
        depends_on('fiat@1.0.0',               type='run')
        depends_on('jedi-base-env@1.0.0',      type='run')
        depends_on('shumlib@macos_clang_port', type='run')

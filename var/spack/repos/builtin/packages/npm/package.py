# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Npm(AutotoolsPackage):
    """npm: A package manager for javascript."""

    homepage = "https://github.com/npm/npm"
    # base http://www.npmjs.com/
    url      = "https://registry.npmjs.org/npm/-/npm-3.10.5.tgz"

    version('3.10.9', 'ec1eb22b466ce87cdd0b90182acce07f')
    version('3.10.5', '46002413f4a71de9b0da5b506bf1d992')

    depends_on('node-js', type=('build', 'run'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdir(npm_config_cache_dir)
        run_env.set('npm_config_cache', npm_config_cache_dir)
        spack_env.set('npm_config_cache', npm_config_cache_dir)

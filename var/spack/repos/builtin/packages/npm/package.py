# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('3.10.9', sha256='fb0871b1aebf4b74717a72289fade356aedca83ee54e7386e38cb51874501dd6')
    version('3.10.5', sha256='ff019769e186152098841c1fa6325e5a79f7903a45f13bd0046a4dc8e63f845f')

    depends_on('node-js', type=('build', 'run'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdir(npm_config_cache_dir)
        run_env.set('npm_config_cache', npm_config_cache_dir)
        spack_env.set('npm_config_cache', npm_config_cache_dir)

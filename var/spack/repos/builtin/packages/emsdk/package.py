# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack import *


class Emsdk(Package):
    """Emscripten SDK"""

    homepage = "https://emscripten.org"
    git      = "https://github.com/emscripten-core/emsdk.git"

    version('main')
    version('3.1.8',  tag='3.1.8')
    version('2.0.34', tag='2.0.34')
    version('1.40.1', tag='1.40.1')

    depends_on('python@3')
    depends_on('cmake', type='test')

    # TODO: use our own llvm and node instead by overriding NODE_JS and LLVM_ROOT in the
    # generated .emscripten file? See
    # https://emscripten.org/docs/getting_started/downloads.html#linux

    phases = ['install']

    def install(self, spec, prefix):
        # See https://emscripten.org/docs/getting_started/downloads.html#emsdk-install-targets.
        if str(self.version) == 'main':
            version_arg = 'latest'
        else:
            version_arg = str(self.version)

        emsdk_script = Executable('./emsdk')
        emsdk_script('install', version_arg)
        emsdk_script('activate', version_arg)

        install_tree('.', prefix)

    def setup_run_environment(self, env):
        """Parse the output of the environment setup script from the emscripten SDK."""
        sh = which('sh')
        with working_dir(self.prefix):
            sh_output = sh('./emsdk_env.sh', output=str, error=str)

        env_pairs_yet = False
        for line in sh_output.splitlines():
            if not env_pairs_yet:
                if line == 'Setting environment variables:':
                    env_pairs_yet = True
                continue
            (env_var, var_value) = re.match(r'^([A-Z_]+) = (.*)$', line).groups()
            env.set(env_var, var_value)

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from spack import *


class Emsdk(Package):
    """Emscripten SDK"""

    homepage = "https://emscripten.org"
    git      = "https://github.com/emscripten-core/emsdk.git"

    version('latest', branch='main')
    version('3.1.8',  tag='3.1.8')
    version('2.0.34', tag='2.0.34')
    version('1.40.1', tag='1.40.1')

    depends_on('python@3')
    depends_on('node-js')
    depends_on('llvm+lld+clang targets=webassembly')
    depends_on('cmake', type='test')

    # TODO: use our own llvm and node instead by overriding NODE_JS and LLVM_ROOT in the
    # generated .emscripten file? See
    # https://emscripten.org/docs/getting_started/downloads.html#linux

    phases = ['install']

    def _patch_line_regex(self, varname):
        return re.compile(r'^{} = (.*)$'.format(varname),
                          flags=re.MULTILINE)

    def _patch_line_replacement(self, varname, path):
        return "{} = '{}'".format(varname, path)

    def _patch_emscripten_config_line(self, varname, path, file_contents):
        regex = self._patch_line_regex(varname)
        replacement = self._patch_line_replacement(varname, path)
        return regex.sub(replacement, file_contents)

    def _patch_emscripten_config(self, file_contents):
        # Use the path to the actual `node` executable.
        node_path = str(which('node'))
        file_contents = self._patch_emscripten_config_line(
            'NODE_JS', node_path, file_contents,
        )
        # Use the directory containing the `lld` binary.
        lld_path = os.path.dirname(str(which('lld')))
        file_contents = self._patch_emscripten_config_line(
            'LLVM_ROOT', lld_path, file_contents,
        )
        return file_contents

    def install(self, spec, prefix):
        # See https://emscripten.org/docs/getting_started/downloads.html#emsdk-install-targets.
        if str(self.version) == 'main':
            version_arg = 'latest'
        else:
            version_arg = str(self.version)

        emsdk_script = Executable('./emsdk')
        emsdk_script('update')
        emsdk_script('install', version_arg)
        emsdk_script('activate', version_arg)

        # Patch .emscripten to point to our versions of node and llvm.
        emscripten_config_path = '.emscripten'
        assert os.path.isfile(emscripten_config_path), emscripten_config_path
        with open(emscripten_config_path, 'r') as f:
            emscripten_config = f.read()
        emscripten_config = self._patch_emscripten_config(emscripten_config)
        with open(emscripten_config_path, 'w') as f:
            f.write(emscripten_config)

        install_tree('.', prefix)

    _set_env_var_line = re.compile(r'^([A-Z_]+) = (.*)$', flags=re.MULTILINE)
    _clear_env_var_line = re.compile(r'^Clearing existing environment variable: (.*)$',
                                     flags=re.MULTILINE)

    def setup_run_environment(self, env):
        """Parse the output of the environment setup script from the emscripten SDK."""
        sh = which('sh')
        with working_dir(self.prefix):
            sh_output = sh('./emsdk_env.sh', output=str, error=str)

        for m in self._set_env_var_line.finditer(sh_output):
            (env_var, env_value) = m.groups()
            env.set(env_var, env_value)

        for m in self._clear_env_var_line.finditer(sh_output):
            (var_to_unset,) = m.groups()
            env.unset(var_to_unset)

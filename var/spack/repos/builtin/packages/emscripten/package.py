# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
from textwrap import dedent

from spack import *


class Emscripten(Package):
    """An LLVM-to-WebAssembly Compiler"""

    homepage = "https://emscripten.org"
    git      = "https://github.com/emscripten-core/emscripten.git"
    url      = "https://github.com/emscripten-core/emscripten/archive/refs/tags/3.0.0.tar.gz"

    version('3.0.0', sha256='c5524755b785d8f4b83eb3214fdd3ac4b2e1b1a4644df4c63f06e5968f48f90e')

    variant('create-standard-executables', default=True,
            description='Apply some patches to executable-type output files in order to make them executable by default.')

    # Need f-strings to run emcc, so 3.7+.
    depends_on('python@3.7:')
    depends_on('npm', type='build')
    depends_on('llvm@14:+lld+clang+multiple-definitions targets=webassembly')
    depends_on('openjdk')

    # Each version of emscripten has an single specific binaryen version they are
    # compatible with.
    depends_on('binaryen')

    depends_on('binaryen@101', when='@3.0.0')

    with when('+create-standard-executables'):
        # Ensure the output has a hashbang and is marked executable with chmod.
        patch('executable-result.patch')
        # Ensure the output has access to node raw fs APIs.
        patch('force-fs.patch')
        # Ensure that executables have sufficient initial memory, and can grow the
        # memory at runtime.
        patch('initial-memory.patch')

    executables = ('^{}$'.format(re.escape(exe)) for exe in [
        'emscons',
        'embuilder',
        'emprofile',
        'emconfigure',
        'em++',
        'emcc',
        'emnm',
        'emrun',
        'em-config',
        'emcmake',
        'emdump',
        'emranlib',
        'emar',
        'emsize',
        'emdwp',
        'emmake',
    ])

    _description = 'Emscripten gcc/clang-like replacement + linker emulating GNU ld'
    _version_pattern = re.compile(
        r'^emcc \({}\) ([0-9]+\.[0-9]+\.[0-9]+(?:\-git)?)$'.format(
            re.escape(_description)),
        flags=re.MULTILINE,
    )

    @classmethod
    def determine_version(cls, exe_path):
        try:
            exe = Executable(exe_path)
            output = exe('--version', output=str, error=str)
            m = cls._version_pattern.search(output)
            if m is None:
                return None
            (v,) = m.groups()
            return Version(v)
        except spack.util.executable.ProcessError:
            pass

        return None

    def install(self, spec, prefix):
        npm = which('npm')
        npm('install')

        with open('.emscripten', 'w') as f:
            f.write(dedent("""\
            NODE_JS = '{node_js}'
            LLVM_ROOT = '{llvm}'
            BINARYEN_ROOT = '{binaryen}'
            EMSCRIPTEN_ROOT = '{emscripten}'
            JAVA = '{java}'
            COMPILER_ENGINE = NODE_JS
            JS_ENGINES = [NODE_JS]
            """.format(
                node_js=str(which('node')),
                llvm=os.path.dirname(str(which('wasm-ld'))),
                binaryen=str(self.spec['binaryen'].prefix),
                emscripten=str(prefix),
                java=str(which('java')),
            )))

        install_tree('.', str(prefix))

    def setup_run_environment(self, env):
        # Tools like emcc are at the prefix root instead of /bin, and they don't seem to
        # like being symlinked into /bin.
        env.prepend_path('PATH', self.prefix)

    _check_description = 'shared:INFO: (Emscripten: Running sanity checks)'
    _check_line = re.compile(
        r'^{}$'.format(re.escape(_check_description)),
        flags=re.MULTILINE,
    )

    def test(self):
        self.run_test(
            'emcc',
            options=['--check'],
            expected=[self._version_pattern, self._check_line],
            installed=True,
            purpose='test: validating emscripten installation',
            skip_missing=False,
        )

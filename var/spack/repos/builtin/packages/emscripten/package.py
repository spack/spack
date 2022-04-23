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

    version('latest', branch='main')
    version('3.0.0', sha256='c5524755b785d8f4b83eb3214fdd3ac4b2e1b1a4644df4c63f06e5968f48f90e')

    executables = ['emcc', 'em\+\+', 'emconfigure', 'emcmake']

    # Need f-strings to run emcc, so 3.7+.
    depends_on('python@3.7:')
    depends_on('npm', type='build')
    depends_on('llvm@14:+lld+clang targets=webassembly')
    depends_on('binaryen')
    depends_on('openjdk')

    phases = ['install', 'test']

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
                llvm=os.path.dirname(str(which('lld'))),
                binaryen=str(self.spec['binaryen'].prefix),
                emscripten=str(prefix),
                java=str(which('java')),
            )))

        install_tree('.', str(prefix))

    def setup_run_environment(self, env):
        # Tools like emcc are at the prefix root instead of /bin, and they don't seem to
        # like being symlinked into /bin.
        env.prepend_path('PATH', self.prefix)

    def test(self):
        self.run_test(
            'emcc',
            options=['--check'],
            expected=[self._version_pattern],
            installed=True,
            purpose='test: validating emscripten installation',
            skip_missing=False,
        )

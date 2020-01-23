# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack import *


class Libsigsegv(AutotoolsPackage, GNUMirrorPackage):
    """GNU libsigsegv is a library for handling page faults in user mode."""

    homepage = "https://www.gnu.org/software/libsigsegv/"
    gnu_mirror_path = "libsigsegv/libsigsegv-2.12.tar.gz"

    version('2.12', sha256='3ae1af359eebaa4ffc5896a1aee3568c052c99879316a1ab57f8fe1789c390b6')
    version('2.11', sha256='dd7c2eb2ef6c47189406d562c1dc0f96f2fc808036834d596075d58377e37a18')
    version('2.10', sha256='8460a4a3dd4954c3d96d7a4f5dd5bc4d9b76f5754196aa245287553b26d2199a')

    patch('patch.new_config_guess', when='@2.10')

    test_requires_compiler = True

    def configure_args(self):
        return ['--enable-shared']

    def _do_smoke_test(self, cc):
        prog = './data/smoke_test'

        tty.msg("  ..compiling smoke_test.c")
        output = cc(
            '-I{0}'.format(self.prefix.include),
            '{0}.c'.format(prog),
            '-o',
            prog,
            '-L{0}'.format(self.prefix.lib),
            '-lsigsegv',
            '-Wl,-R{0}'.format(self.prefix.lib),
            output=str.split,
            error=str.split)
        assert len(output) == 0

        tty.msg("  running smoke_test")
        smoke_test = Executable(prog)
        assert smoke_test is not None
        output = smoke_test(output=str.split, error=str.split)
        with open('./data/smoke_test.out', 'r') as fd:
            assert output == fd.read()

    def _do_sigsegv1(self, cc):
        # Note the compilation options and order are from an actual install
        # on a specific linux machine, which used gcc.
        # TODO: Are relative paths acceptable?
        prog = './data/sigsegv1'
        includes = '-I./data'
        opts = '-g -O2'

        # <comp> -DHAVE_CONFIG_H -I./data -g -O2 -c -o sigsegv1.o sigsegv1.c
        tty.msg('  compiling sigsegv1')
        output = cc(
            '-DHAVE_CONFIG_H',
            '-I./data',
            '-I{0}'.format(self.prefix.include),
            '-g',
            '-O2',
            '-c',
            '-o',
            '{0}.o'.format(prog),
            '{0}.c'.format(prog),
            output=str.split,
            error=str.split)
        assert len(output) == 0


        # <comp> -g -O2 -o sigsegv1 sigsegv1.o  <install>/lib/libsigsegv.so \
        #    -lc -Wl,-rpath -Wl,<install>/lib
        tty.msg('  linking sigsegv1')
        output = cc(
            '-g',
            '-O2',
            '-o',
            prog,
            '{0}.o'.format(prog),
            '{0}/libsigsegv.so'.format(self.prefix.lib),
            '-lc',
            '-Wl,-rpath',
            '-Wl,{0}'.format(self.prefix.lib),
            output=str.split,
            error=str.split)
        assert len(output) == 0

        tty.msg("  running sigsegv1")
        sigsegv1 = Executable(prog)
        assert sigsegv1 is not None
        output = sigsegv1(output=str.split, error=str.split)
        assert output == "Test passed.\n"

    def test(self):
        compilers = spack.compilers.compilers_for_spec(
            self.spec.compiler, self.spec.architecture)
        compiler = compilers[0].cc
        cc = Executable(compilers[0].cc)
        assert cc is not None
        assert os.path.dirname(cc.path) == os.path.dirname(compiler)

        tty.msg('test: Building and running smoke test')
        self._do_smoke_test(cc)

        # TODO: Compile and run sigsegv1
        self._do_sigsegv1(cc)

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

    # TODO: Remove once this function is lifted to the package level
    def _run_test(self, exe, options, expected, status):
        """Run the test and confirm obtain the expected results

        Args:
            exe (str): the name of the executable
            options (list of str): list of options to pass to the runner
            expected (list of str): list of expected output strings
            status (int or None): the expected process status if int or None
                if the test is expected to succeed
        """
        result = 'fail with status {0}'.format(status) if status else 'succeed'
        tty.msg('test: {0}: expect to {1}' .format(exe, result))
        runner = which(exe)
        assert runner is not None

        try:
            output = runner(*options, output=str.split, error=str.split)
            assert not status, 'Expected execution to fail'
        except ProcessError as err:
            output = str(err)
            status_msg = 'exited with status {0}'.format(status)
            expected_msg = 'Expected \'{0}\' in \'{1}\''.format(
                status_msg, err.message)
            assert status_msg in output, expected_msg

        for check in expected:
            assert check in output

    def _do_smoke_test(self, cc):
        prog = 'data/smoke_test'

        options = [
            '-I{0}'.format(self.prefix.include),
            '{0}.c'.format(prog),
            '-o',
            prog,
            '-L{0}'.format(self.prefix.lib),
            '-lsigsegv',
            '-Wl,-R{0}'.format(self.prefix.lib)]
        self._run_test('cc', options, [], None)

        with open('./data/smoke_test.out', 'r') as fd:
            expected = fd.read()
        self._run_test(prog, options, expected, None)

    def _do_sigsegv1(self, cc):
        # Note the compilation options and order are from an actual install
        # on a specific linux machine, which used gcc.
        prog = 'data/sigsegv1'

        options = [
            '-DHAVE_CONFIG_H',
            '-I./data',
            '-I{0}'.format(self.prefix.include),
            '-o',
            prog,
            '-lc',
            '-L{0}'.format(self.prefix.lib),
            '-lsigsegv',
            '{0}.c'.format(prog)]
        self._run_test('cc', options, [], None)

        self._run_test(prog, [], ["Test passed."], None)

    def test(self):
        tty.msg('test: Ensuring use of installed cc')
        cc = which('cc')
        assert cc is not None

        # Run the basic smoke test
        self._do_smoke_test(cc)

        # Run the sigsegv1 test taken from the test suite
        self._do_sigsegv1(cc)

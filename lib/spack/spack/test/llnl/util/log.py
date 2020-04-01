# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import pytest

from llnl.util.tty.log import log_output
from spack.util.executable import which


def test_log_python_output_with_python_stream(capsys, tmpdir):
    # pytest's DontReadFromInput object does not like what we do here, so
    # disable capsys or things hang.
    with tmpdir.as_cwd():
        with capsys.disabled():
            with log_output('foo.txt'):
                print('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        assert capsys.readouterr() == ('', '')


def test_log_python_output_with_fd_stream(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt'):
            print('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        # Coverage is cluttering stderr during tests
        assert capfd.readouterr()[0] == ''


def test_log_python_output_and_echo_output(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                print('echo')
            print('logged')

        # Coverage is cluttering stderr during tests
        assert capfd.readouterr()[0] == 'echo\n'

        with open('foo.txt') as f:
            assert f.read() == 'echo\nlogged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_output(capsys, tmpdir):
    echo = which('echo')

    # pytest seems to interfere here, so we need to use capsys.disabled()
    # TODO: figure out why this is and whether it means we're doing
    # sometihng wrong with OUR redirects.  Seems like it should work even
    # with capsys enabled.
    with tmpdir.as_cwd():
        with capsys.disabled():
            with log_output('foo.txt'):
                echo('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_and_echo_output(capfd, tmpdir):
    echo = which('echo')

    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                echo('echo')
            print('logged')

        # Coverage is cluttering stderr during tests
        assert capfd.readouterr()[0] == 'echo\n'

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest
from six.moves import cPickle

from spack.main import SpackCommand

build_env = SpackCommand('build-env')


@pytest.mark.parametrize('pkg', [
    ('zlib',),
    ('zlib', '--')
])
@pytest.mark.usefixtures('config', 'mock_packages')
def test_it_just_runs(pkg):
    build_env(*pkg)


def test_error_when_multiple_specs_are_given(config, mock_packages):
    output = build_env('libelf libdwarf', fail_on_error=False)
    assert 'only takes one spec' in output


@pytest.mark.parametrize('args', [
    ('--', '/bin/sh', '-c', 'echo test'),
    ('--',),
    (),
])
@pytest.mark.usefixtures('config', 'mock_packages')
def test_build_env_requires_a_spec(args):
    output = build_env(*args, fail_on_error=False)
    assert 'requires a spec' in output


_out_file = 'env.out'


def test_dump(config, tmpdir, mock_packages):
    with tmpdir.as_cwd():
        build_env('--dump', _out_file, 'zlib')
        with open(_out_file) as f:
            assert(any(line.startswith('PATH=') for line in f.readlines()))


def test_pickle(config, tmpdir, mock_packages):
    with tmpdir.as_cwd():
        build_env('--pickle', _out_file, 'zlib')
        environment = cPickle.load(open(_out_file, 'rb'))
        assert(type(environment) == dict)
        assert('PATH' in environment)


def test_tty_preserves_SHELL_and_DISPLAY(
    config, working_env, mock_packages, monkeypatch
):
    os.environ['TERM'] = 'X'
    os.environ['DISPLAY'] = 'Y'
    out = build_env('--tty', 'zlib')
    assert 'TERM=X' in out
    assert 'DISPLAY=Y' in out

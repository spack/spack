# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
from six.moves import cPickle

from spack.main import SpackCommand

build_env = SpackCommand('build-env')


@pytest.mark.parametrize('pkg', [
    ('zlib',),
    ('zlib', '--')
])
@pytest.mark.usefixtures('config')
def test_it_just_runs(pkg):
    build_env(*pkg)


@pytest.mark.usefixtures('config')
def test_error_when_multiple_specs_are_given():
    output = build_env('libelf libdwarf', fail_on_error=False)
    assert 'only takes one spec' in output


@pytest.mark.parametrize('args', [
    ('--', '/bin/bash', '-c', 'echo test'),
    ('--',),
    (),
])
@pytest.mark.usefixtures('config')
def test_build_env_requires_a_spec(args):
    output = build_env(*args, fail_on_error=False)
    assert 'requires a spec' in output


_out_file = 'env.out'


@pytest.mark.usefixtures('config')
def test_dump(tmpdir):
    with tmpdir.as_cwd():
        build_env('--dump', _out_file, 'zlib')
        with open(_out_file) as f:
            assert(any(line.startswith('PATH=') for line in f.readlines()))


@pytest.mark.usefixtures('config')
def test_pickle(tmpdir):
    with tmpdir.as_cwd():
        build_env('--pickle', _out_file, 'zlib')
        environment = cPickle.load(open(_out_file, 'rb'))
        assert(type(environment) == dict)
        assert('PATH' in environment)

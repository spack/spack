# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from six.moves import cPickle
import pytest

from spack.main import SpackCommand, SpackCommandError

info = SpackCommand('build-env')


@pytest.mark.parametrize('pkg', [
    ('zlib',),
    ('zlib', '--')
])
@pytest.mark.usefixtures('config')
def test_it_just_runs(pkg):
    info(*pkg)


@pytest.mark.parametrize('pkg,error_cls', [
    ('zlib libszip', SpackCommandError),
    ('', IndexError)
])
@pytest.mark.usefixtures('config')
def test_it_just_fails(pkg, error_cls):
    with pytest.raises(error_cls):
        info(pkg)


_out_file = 'env.out'


@pytest.mark.usefixtures('config')
def test_dump(tmpdir):
    with tmpdir.as_cwd():
        info('--dump', _out_file, 'zlib')
        with open(_out_file) as f:
            assert(any(line.startswith('PATH=') for line in f.readlines()))


@pytest.mark.usefixtures('config')
def test_pickle(tmpdir):
    with tmpdir.as_cwd():
        info('--pickle', _out_file, 'zlib')
        environment = cPickle.load(open(_out_file, 'rb'))
        assert(type(environment) == dict)
        assert('PATH' in environment)

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
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


@pytest.fixture
def _test_file_cleaner():
    """Ensure test creates a file; clean up after test.
    """
    if os.path.exists(_out_file):
        os.remove(_out_file)

    yield

    assert(os.path.exists(_out_file))
    os.remove(_out_file)


@pytest.mark.parametrize('pkg', [
    ('--dump', _out_file, 'zlib'),
    ('--pickle', _out_file, 'zlib')
])
@pytest.mark.usefixtures('config', '_test_file_cleaner')
def test_pickle_dump(pkg):
    info(*pkg)

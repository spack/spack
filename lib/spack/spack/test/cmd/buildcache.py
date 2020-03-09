# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import platform

import pytest

import spack.main
import spack.binary_distribution

buildcache = spack.main.SpackCommand('buildcache')
install = spack.main.SpackCommand('install')


@pytest.fixture()
def mock_get_specs(database, monkeypatch):
    specs = database.query_local()
    monkeypatch.setattr(
        spack.binary_distribution, 'get_specs', lambda x, y: specs
    )


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
@pytest.mark.db
def test_buildcache_preview_just_runs(database):
    buildcache('preview', 'mpileaks')


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
@pytest.mark.db
@pytest.mark.regression('13757')
def test_buildcache_list_duplicates(mock_get_specs, capsys):
    with capsys.disabled():
        output = buildcache('list', 'mpileaks', '@2.3')

    assert output.count('mpileaks') == 3


def test_buildcache_create_fail_on_perm_denied(
        install_mockery, mock_fetch, monkeypatch, tmpdir):
    """Ensure that buildcache create fails on permission denied error."""
    install('trivial-install-test-package')

    tmpdir.chmod(0)
    with pytest.raises(OSError) as error:
        buildcache('create', '-d', str(tmpdir),
                   '--unsigned', 'trivial-install-test-package')
    assert error.value.errno == errno.EACCES
    tmpdir.chmod(0o700)

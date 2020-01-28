# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.repo

from spack.installer import \
    _hms, \
    ExternalPackageError, InstallLockError, UpstreamPackageError, \
    PackageInstaller


@pytest.mark.parametrize('sec,result', [
    (86400, "24h"),
    (3600, "1h"),
    (60, "1m"),
    (1.802, "1.80s"),
    (3723.456, "1h 2m 3.46s")])
def test_hms(sec, result):
    assert _hms(sec) == result


def test_constructor_errors(install_mockery):
    # Ensure installer requires a package
    with pytest.raises(ValueError, match='must be a package'):
        PackageInstaller('abc')

    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='Can only install concrete'):
        PackageInstaller(pkg)


def test_external_pkg_error():
    try:
        raise ExternalPackageError('test external', long_msg='a long message')
    except Exception as exc:
        assert exc.__class__.__name__ == 'ExternalPackageError'
        assert exc.message == 'test external'
        assert exc.long_message == 'a long message'


def test_install_lock_error():
    msg = 'test install lock'
    with pytest.raises(InstallLockError, match=msg):
        raise InstallLockError(msg)


def test_upstream_package_error():
    msg = 'test upstream package'
    with pytest.raises(UpstreamPackageError, match=msg):
        raise UpstreamPackageError(msg)

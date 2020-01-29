# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.installer as inst
import spack.repo
import spack.spec


@pytest.mark.parametrize('sec,result', [
    (86400, "24h"),
    (3600, "1h"),
    (60, "1m"),
    (1.802, "1.80s"),
    (3723.456, "1h 2m 3.46s")])
def test_hms(sec, result):
    assert inst._hms(sec) == result


def test_install_msg():
    name = 'some-package'
    pid = 123456
    expected = "{0}: Installing {1}".format(pid, name)
    assert inst.install_msg(name, pid) == expected


def dest_install_from_cache_errors(install_mockery, capsys):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Check with cache-only
    with pytest.raises(SystemExit):
        inst._install_from_cache(spec.package, True, True)

    captured = str(capsys.readouterr())
    assert 'No binary' in captured
    assert 'found when cache-only specified' in captured
    assert not spec.package.installed_from_binary_cache

    # Check when don't expect to install only from binary cache
    assert not inst._install_from_cache(spec.package, False, True)
    assert not spec.package.installed_from_binary_cache


def test_installer_init_errors(install_mockery):
    with pytest.raises(ValueError, match='must be a package'):
        inst.PackageInstaller('abc')

    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='Can only install concrete'):
        inst.PackageInstaller(pkg)


def test_installer_strings(install_mockery):
    """Tests of installer repr and str for coverage purposes."""
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    installer = inst.PackageInstaller(spec.package)

    # Cover __repr__
    irep = installer.__repr__()
    assert irep.startswith(installer.__class__.__name__)
    assert "installed=" in irep
    assert "failed=" in irep

    # Cover __str__
    istr = str(installer)
    assert "#tasks=0" in istr
    assert "installed (0)" in istr
    assert "failed (0)" in istr


def test_installer_last_phase_error(install_mockery, capsys):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    with pytest.raises(SystemExit):
        installer = inst.PackageInstaller(spec.package)
        installer.install(stop_at='badphase')

    captured = capsys.readouterr()
    assert 'is not an allowed phase' in str(captured)


def test_installer_ensure_ready_errors(install_mockery):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    installer = inst.PackageInstaller(spec.package)
    assert installer

    fmt = r'cannot be installed locally.*{0}'
    # Force an external package error
    path, module = spec.external_path, spec.external_module
    spec.external_path = '/actual/external/path/not/checked'
    spec.external_module = 'unchecked_module'
    msg = fmt.format('is external')
    with pytest.raises(inst.ExternalPackageError, match=msg):
        installer._ensure_install_ready(spec.package)

    # Force an upstream package error
    spec.external_path, spec.external_module = path, module
    spec.package._installed_upstream = True
    msg = fmt.format('is upstream')
    with pytest.raises(inst.UpstreamPackageError, match=msg):
        installer._ensure_install_ready(spec.package)

    # Force an install lock error, which should occur naturally since
    # we are calling an internal method prior to any lock-related setup
    spec.package._installed_upstream = False
    assert len(installer.locks) == 0
    with pytest.raises(inst.InstallLockError, match=fmt.format('not locked')):
        installer._ensure_install_ready(spec.package)

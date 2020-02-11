# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.compilers
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
    """Test to ensure cover _install_from_cache errors."""
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


def test_install_from_cache_ok(install_mockery, monkeypatch):
    """Test to ensure cover _install_from_cache to the return."""
    def _installed(pkg, explicit):
        return True

    def _post_hook(spec):
        pass

    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    monkeypatch.setattr(spack.installer, '_try_install_from_binary_cache',
                        _installed)
    monkeypatch.setattr(spack.hooks, 'post_install', _post_hook)

    assert inst._install_from_cache(spec.package, True, True)


def test_process_external_package_module(install_mockery, monkeypatch, capfd):
    """Test to simply cover the external module message path."""
    def _no_rec(spec):
        return None

    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Ensure take the external module path WITHOUT any changes to the database
    monkeypatch.setattr(spack.store.db, 'get_record', _no_rec)

    spec.external_path = '/actual/external/path/not/checked'
    spec.external_module = 'unchecked_module'
    inst._process_external_package(spec.package, False)

    out = capfd.readouterr()[0]
    assert 'has external module in {0}'.format(spec.external_module) in out
    assert 'is actually installed in {0}'.format(spec.external_path) in out


def test_installer_init_errors(install_mockery):
    """Test to ensure cover installer constructor errors."""
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
    """Test to cover last phase error."""
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    with pytest.raises(SystemExit):
        installer = inst.PackageInstaller(spec.package)
        installer.install(stop_at='badphase')

    captured = capsys.readouterr()
    assert 'is not an allowed phase' in str(captured)


def test_installer_ensure_ready_errors(install_mockery):
    """Test to cover _ensure_ready errors."""
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


def test_package_id(install_mockery):
    """Test to cover package_id functionality."""
    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, matches='spec is not concretized'):
        inst.package_id(pkg)

    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    assert pkg.name in inst.package_id(pkg)


def test_fake_install(install_mockery):
    """Test to cover fake install basics."""
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    inst._do_fake_install(pkg)
    assert os.path.isdir(pkg.prefix.lib)


def test_packages_needed_to_bootstrap_compiler(install_mockery, monkeypatch):
    """Test to cover most of _packages_needed_to_boostrap_compiler."""
    # TODO: More work is needed to go beyond the dependency check
    def _no_compilers(pkg, arch_spec):
        return []

    # Test path where no compiler packages returned
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    packages = inst._packages_needed_to_bootstrap_compiler(spec.package)
    assert not packages

    # Test up to the dependency check
    monkeypatch.setattr(spack.compilers, 'compilers_for_spec', _no_compilers)
    with pytest.raises(spack.repo.UnknownPackageError, matches='not found'):
        inst._packages_needed_to_bootstrap_compiler(spec.package)


def test_dump_packages_deps(install_mockery, tmpdir):
    """Test to add coverage to dump_packages."""
    spec = spack.spec.Spec('simple-inheritance').concretized()
    with tmpdir.as_cwd():
        inst.dump_packages(spec, '.')


def test_add_bootstrap_compilers(install_mockery, monkeypatch):
    """Test to cover _add_bootstrap_compilers."""
    def _pkgs(pkg):
        spec = spack.spec.Spec('mpi').concretized()
        return [(spec.package, True)]

    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    installer = inst.PackageInstaller(spec.package)
    assert len(installer.build_tasks) == 0

    monkeypatch.setattr(spack.installer,
                        '_packages_needed_to_bootstrap_compiler', _pkgs)
    installer._add_bootstrap_compilers(spec.package)

    ids = list(installer.build_tasks)
    assert len(ids) == 1
    task = installer.build_tasks[ids[0]]
    assert task.compiler


def test_prepare_for_install_on_installed(install_mockery, monkeypatch):
    """Test of _prepare_for_install's early return for installed task path."""
    def _noop(installer, pkg):
        pass

    spec = spack.spec.Spec('dependent-install')
    spec.concretize()
    assert spec.concrete
    installer = inst.PackageInstaller(spec.package)

    task = inst.BuildTask(spec.package, False, 0, 0, inst.STATUS_ADDED, [])
    installer.installed.add(task.pkg_id)

    monkeypatch.setattr(inst.PackageInstaller, '_ensure_install_ready', _noop)
    installer._prepare_for_install(task, True, True, False)

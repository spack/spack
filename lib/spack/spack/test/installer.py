# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import llnl.util.tty as tty

import spack.binary_distribution
import spack.compilers
import spack.directory_layout as dl
import spack.installer as inst
import spack.util.lock as lk
import spack.repo
import spack.spec


def _noop(*args, **kwargs):
    """Generic monkeypatch no-op routine."""
    pass


def _none(*args, **kwargs):
    """Generic monkeypatch function that always returns None."""
    return None


def _true(*args, **kwargs):
    """Generic monkeypatch function that always returns True."""
    return True


def create_build_task(pkg):
    """
    Create a built task for the given (concretized) package

    Args:
        pkg (PackageBase): concretized package associated with the task

    Return:
        (BuildTask) A basic package build task
    """
    return inst.BuildTask(pkg, False, 0, 0, inst.STATUS_ADDED, [])


def create_installer(spec_name):
    """
    Create an installer for the named spec

    Args:
        spec_name (str):  Name of the explicit install spec

    Return:
        spec (Spec): concretized spec
        installer (PackageInstaller): the associated package installer
    """
    spec = spack.spec.Spec(spec_name)
    spec.concretize()
    assert spec.concrete
    return spec, inst.PackageInstaller(spec.package)


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


def test_install_from_cache_errors(install_mockery, capsys):
    """Test to ensure cover _install_from_cache errors."""
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Check with cache-only
    with pytest.raises(SystemExit):
        inst._install_from_cache(spec.package, True, True, False)

    captured = str(capsys.readouterr())
    assert 'No binary' in captured
    assert 'found when cache-only specified' in captured
    assert not spec.package.installed_from_binary_cache

    # Check when don't expect to install only from binary cache
    assert not inst._install_from_cache(spec.package, False, True, False)
    assert not spec.package.installed_from_binary_cache


def test_install_from_cache_ok(install_mockery, monkeypatch):
    """Test to ensure cover _install_from_cache to the return."""
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    monkeypatch.setattr(inst, '_try_install_from_binary_cache', _true)
    monkeypatch.setattr(spack.hooks, 'post_install', _noop)

    assert inst._install_from_cache(spec.package, True, True, False)


def test_process_external_package_module(install_mockery, monkeypatch, capfd):
    """Test to simply cover the external module message path."""
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Ensure take the external module path WITHOUT any changes to the database
    monkeypatch.setattr(spack.database.Database, 'get_record', _none)

    spec.external_path = '/actual/external/path/not/checked'
    spec.external_module = 'unchecked_module'
    inst._process_external_package(spec.package, False)

    out = capfd.readouterr()[0]
    assert 'has external module in {0}'.format(spec.external_module) in out
    assert 'is actually installed in {0}'.format(spec.external_path) in out


def test_process_binary_cache_tarball_none(install_mockery, monkeypatch,
                                           capfd):
    """Tests to cover _process_binary_cache_tarball when no tarball."""
    monkeypatch.setattr(spack.binary_distribution, 'download_tarball', _none)

    pkg = spack.repo.get('trivial-install-test-package')
    assert not inst._process_binary_cache_tarball(pkg, None, False, False)

    assert 'exists in binary cache but' in capfd.readouterr()[0]


def test_process_binary_cache_tarball_tar(install_mockery, monkeypatch, capfd):
    """Tests to cover _process_binary_cache_tarball with a tar file."""
    def _spec(spec):
        return spec

    # Skip binary distribution functionality since assume tested elsewhere
    monkeypatch.setattr(spack.binary_distribution, 'download_tarball', _spec)
    monkeypatch.setattr(spack.binary_distribution, 'extract_tarball', _noop)

    # Skip database updates
    monkeypatch.setattr(spack.database.Database, 'add', _noop)

    spec = spack.spec.Spec('a').concretized()
    assert inst._process_binary_cache_tarball(spec.package, spec, False, False)

    assert 'Installing a from binary cache' in capfd.readouterr()[0]


def test_installer_init_errors(install_mockery):
    """Test to ensure cover installer constructor errors."""
    with pytest.raises(ValueError, match='must be a package'):
        inst.PackageInstaller('abc')

    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='Can only install concrete'):
        inst.PackageInstaller(pkg)


def test_installer_strings(install_mockery):
    """Tests of installer repr and str for coverage purposes."""
    spec, installer = create_installer('trivial-install-test-package')

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
    spec, installer = create_installer('trivial-install-test-package')

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


def test_ensure_locked_have(install_mockery, tmpdir):
    """Test to cover _ensure_locked when already have lock."""
    spec, installer = create_installer('trivial-install-test-package')

    with tmpdir.as_cwd():
        lock = lk.Lock('./test', default_timeout=1e-9, desc='test')
        lock_type = 'read'
        tpl = (lock_type, lock)
        installer.locks[installer.pkg_id] = tpl
        assert installer._ensure_locked(lock_type, spec.package) == tpl


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

    spec, installer = create_installer('trivial-install-test-package')

    monkeypatch.setattr(inst, '_packages_needed_to_bootstrap_compiler', _pkgs)
    installer._add_bootstrap_compilers(spec.package)

    ids = list(installer.build_tasks)
    assert len(ids) == 1
    task = installer.build_tasks[ids[0]]
    assert task.compiler


def test_prepare_for_install_on_installed(install_mockery, monkeypatch):
    """Test of _prepare_for_install's early return for installed task path."""
    spec, installer = create_installer('dependent-install')
    task = create_build_task(spec.package)
    installer.installed.add(task.pkg_id)

    monkeypatch.setattr(inst.PackageInstaller, '_ensure_install_ready', _noop)
    installer._prepare_for_install(task, True, True, False)


def test_installer_init_queue(install_mockery):
    """Test of installer queue functions."""
    with spack.config.override('config:install_missing_compilers', True):
        spec, installer = create_installer('dependent-install')
        installer._init_queue(True, True)

        ids = list(installer.build_tasks)
        assert len(ids) == 2
        assert 'dependency-install' in ids
        assert 'dependent-install' in ids


def test_install_task_use_cache(install_mockery, monkeypatch):
    """Test _install_task to cover use_cache path."""
    spec, installer = create_installer('trivial-install-test-package')
    task = create_build_task(spec.package)

    monkeypatch.setattr(inst, '_install_from_cache', _true)
    installer._install_task(task)
    assert spec.package.name in installer.installed


def test_release_lock_write_n_exception(install_mockery, tmpdir, capsys):
    """Test _release_lock for supposed write lock with exception."""
    spec, installer = create_installer('trivial-install-test-package')

    pkg_id = 'test'
    with tmpdir.as_cwd():
        lock = lk.Lock('./test', default_timeout=1e-9, desc='test')
        installer.locks[pkg_id] = ('write', lock)
        assert lock._writes == 0

        installer._release_lock(pkg_id)
        out = str(capsys.readouterr()[1])
        msg = 'exception when releasing write lock for {0}'.format(pkg_id)
        assert msg in out


def test_requeue_task(install_mockery, capfd):
    """Test to ensure cover _requeue_task."""
    spec, installer = create_installer('a')
    task = create_build_task(spec.package)

    installer._requeue_task(task)

    ids = list(installer.build_tasks)
    assert len(ids) == 1
    qtask = installer.build_tasks[ids[0]]
    assert qtask.status == inst.STATUS_INSTALLING

    out = capfd.readouterr()[0]
    assert 'Installing a in progress by another process' in out


def test_cleanup_all_tasks(install_mockery, monkeypatch):
    """Test to ensure cover _cleanup_all_tasks."""
    def _mktask(pkg):
        return create_build_task(pkg)

    def _rmtask(installer, pkg_id):
        raise RuntimeError('Raise an exception to test except path')

    spec, installer = create_installer('a')

    # Cover task removal happy path
    installer.build_tasks['a'] = _mktask(spec.package)
    installer._cleanup_all_tasks()
    assert len(installer.build_tasks) == 0

    # Cover task removal exception path
    installer.build_tasks['a'] = _mktask(spec.package)
    monkeypatch.setattr(inst.PackageInstaller, '_remove_task', _rmtask)
    installer._cleanup_all_tasks()
    assert len(installer.build_tasks) == 1


def test_cleanup_failed(install_mockery, tmpdir, monkeypatch, capsys):
    """Test to increase coverage of _cleanup_failed."""
    msg = 'Fake release_write exception'

    def _raise_except(lock):
        raise RuntimeError(msg)

    spec, installer = create_installer('trivial-install-test-package')

    monkeypatch.setattr(lk.Lock, 'release_write', _raise_except)
    pkg_id = 'test'
    with tmpdir.as_cwd():
        lock = lk.Lock('./test', default_timeout=1e-9, desc='test')
        installer.failed[pkg_id] = lock

        installer._cleanup_failed(pkg_id)
        out = str(capsys.readouterr()[1])
        assert 'exception when removing failure mark' in out
        assert msg in out


def test_update_failed_no_mark(install_mockery):
    """Test of _update_failed sans mark and dependent build tasks."""
    spec, installer = create_installer('dependent-install')
    task = create_build_task(spec.package)

    installer._update_failed(task)
    assert installer.failed['dependent-install'] is None


def test_install_uninstalled_deps(install_mockery, monkeypatch, capsys):
    """Test install with uninstalled dependencies."""
    spec, installer = create_installer('dependent-install')

    # Skip the actual installation and any status updates
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _noop)
    monkeypatch.setattr(inst.PackageInstaller, '_update_installed', _noop)
    monkeypatch.setattr(inst.PackageInstaller, '_update_failed', _noop)

    msg = 'Cannot proceed with dependent-install'
    with pytest.raises(spack.installer.InstallError, matches=msg):
        installer.install()

    out = str(capsys.readouterr())
    assert 'Detected uninstalled dependencies for' in out


def test_install_failed(install_mockery, monkeypatch, capsys):
    """Test install with failed install."""
    spec, installer = create_installer('b')

    # Make sure the package is identified as failed
    monkeypatch.setattr(spack.database.Database, 'prefix_failed', _true)

    # Skip the actual installation though it should never get there
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _noop)

    msg = 'Installation of b failed'
    with pytest.raises(spack.installer.InstallError, matches=msg):
        installer.install()

    out = str(capsys.readouterr())
    assert 'Warning: b failed to install' in out


def test_install_lock_failures(install_mockery, monkeypatch, capfd):
    """Cover basic install lock failure handling in a single pass."""
    def _requeued(installer, task):
        tty.msg('requeued {0}' .format(task.pkg.spec.name))

    def _not_locked(installer, lock_type, pkg):
        tty.msg('{0} locked {1}' .format(lock_type, pkg.spec.name))
        return lock_type, None

    spec, installer = create_installer('b')

    # Ensure never acquire a lock
    monkeypatch.setattr(inst.PackageInstaller, '_ensure_locked', _not_locked)

    # Ensure don't continually requeue the task
    monkeypatch.setattr(inst.PackageInstaller, '_requeue_task', _requeued)

    # Skip the actual installation though should never reach it
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _noop)

    installer.install()
    out = capfd.readouterr()[0]
    expected = ['write locked', 'read locked', 'requeued']
    for exp, ln in zip(expected, out.split('\n')):
        assert exp in ln


def test_install_lock_installed_requeue(install_mockery, monkeypatch, capfd):
    """Cover basic install handling for installed package."""
    def _install(installer, task, **kwargs):
        tty.msg('{0} installing'.format(task.pkg.spec.name))

    def _not_locked(installer, lock_type, pkg):
        tty.msg('{0} locked {1}' .format(lock_type, pkg.spec.name))
        return lock_type, None

    def _prep(installer, task, keep_prefix, keep_stage, restage):
        installer.installed.add('b')
        tty.msg('{0} is installed' .format(task.pkg.spec.name))

        # also do not allow the package to be locked again
        monkeypatch.setattr(inst.PackageInstaller, '_ensure_locked',
                            _not_locked)

    def _requeued(installer, task):
        tty.msg('requeued {0}' .format(task.pkg.spec.name))

    # Skip the actual installation though should never reach it
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _install)

    # Flag the package as installed
    monkeypatch.setattr(inst.PackageInstaller, '_prepare_for_install', _prep)

    # Ensure don't continually requeue the task
    monkeypatch.setattr(inst.PackageInstaller, '_requeue_task', _requeued)

    spec, installer = create_installer('b')

    installer.install()
    assert 'b' not in installer.installed

    out = capfd.readouterr()[0]
    expected = ['is installed', 'read locked', 'requeued']
    for exp, ln in zip(expected, out.split('\n')):
        assert exp in ln


def test_install_read_locked_requeue(install_mockery, monkeypatch, capfd):
    """Cover basic read lock handling for uninstalled package with requeue."""
    orig_fn = inst.PackageInstaller._ensure_locked

    def _install(installer, task, **kwargs):
        tty.msg('{0} installing'.format(task.pkg.spec.name))

    def _read(installer, lock_type, pkg):
        tty.msg('{0}->read locked {1}' .format(lock_type, pkg.spec.name))
        return orig_fn(installer, 'read', pkg)

    def _prep(installer, task, keep_prefix, keep_stage, restage):
        tty.msg('preparing {0}' .format(task.pkg.spec.name))
        assert task.pkg.spec.name not in installer.installed

    def _requeued(installer, task):
        tty.msg('requeued {0}' .format(task.pkg.spec.name))

    # Force a read lock
    monkeypatch.setattr(inst.PackageInstaller, '_ensure_locked', _read)

    # Skip the actual installation though should never reach it
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _install)

    # Flag the package as installed
    monkeypatch.setattr(inst.PackageInstaller, '_prepare_for_install', _prep)

    # Ensure don't continually requeue the task
    monkeypatch.setattr(inst.PackageInstaller, '_requeue_task', _requeued)

    spec, installer = create_installer('b')

    installer.install()
    assert 'b' not in installer.installed

    out = capfd.readouterr()[0]
    expected = ['write->read locked', 'preparing', 'requeued']
    for exp, ln in zip(expected, out.split('\n')):
        assert exp in ln


def test_install_dir_exists(install_mockery, monkeypatch, capfd):
    """Cover capture of install directory exists error."""
    err = 'Mock directory exists error'

    def _install(installer, task, **kwargs):
        raise dl.InstallDirectoryAlreadyExistsError(err)

    # Skip the actual installation though should never reach it
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _install)

    spec, installer = create_installer('b')

    with pytest.raises(dl.InstallDirectoryAlreadyExistsError, matches=err):
        installer.install()

    assert 'b' in installer.installed

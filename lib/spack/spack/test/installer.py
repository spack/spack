# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import py
import pytest

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import llnl.util.lock as ulk

import spack.binary_distribution
import spack.compilers
import spack.directory_layout as dl
import spack.installer as inst
import spack.package_perms as spp
import spack.repo
import spack.spec
import spack.store
import spack.util.lock as lk


def _mock_repo(root, namespace):
    """Create an empty repository at the specified root

    Args:
        root (str): path to the mock repository root
        namespace (str):  mock repo's namespace
    """
    repodir = py.path.local(root) if isinstance(root, str) else root
    repodir.ensure(spack.repo.packages_dir_name, dir=True)
    yaml = repodir.join('repo.yaml')
    yaml.write("""
repo:
   namespace: {0}
""".format(namespace))


def _noop(*args, **kwargs):
    """Generic monkeypatch no-op routine."""
    pass


def _none(*args, **kwargs):
    """Generic monkeypatch function that always returns None."""
    return None


def _not_locked(installer, lock_type, pkg):
    """Generic monkeypatch function for _ensure_locked to return no lock"""
    tty.msg('{0} locked {1}' .format(lock_type, pkg.spec.name))
    return lock_type, None


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
    """Tests of _process_binary_cache_tarball when no tarball."""
    monkeypatch.setattr(spack.binary_distribution, 'download_tarball', _none)

    pkg = spack.repo.get('trivial-install-test-package')
    assert not inst._process_binary_cache_tarball(pkg, None, False, False)

    assert 'exists in binary cache but' in capfd.readouterr()[0]


def test_process_binary_cache_tarball_tar(install_mockery, monkeypatch, capfd):
    """Tests of _process_binary_cache_tarball with a tar file."""
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


def test_try_install_from_binary_cache(install_mockery, mock_packages,
                                       monkeypatch, capsys):
    """Tests SystemExit path for_try_install_from_binary_cache."""
    def _spec(spec, force):
        spec = spack.spec.Spec('mpi').concretized()
        return {spec: None}

    spec = spack.spec.Spec('mpich')
    spec.concretize()

    monkeypatch.setattr(spack.binary_distribution, 'get_spec', _spec)

    with pytest.raises(SystemExit):
        inst._try_install_from_binary_cache(spec.package, False, False)

    captured = capsys.readouterr()
    assert 'add a spack mirror to allow download' in str(captured)


def test_installer_init_errors(install_mockery):
    """Test to ensure cover installer constructor errors."""
    with pytest.raises(ValueError, match='must be a package'):
        inst.PackageInstaller('abc')

    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='Can only install concrete'):
        inst.PackageInstaller(pkg)


def test_installer_repr(install_mockery):
    spec, installer = create_installer('trivial-install-test-package')

    irep = installer.__repr__()
    assert irep.startswith(installer.__class__.__name__)
    assert "installed=" in irep
    assert "failed=" in irep


def test_installer_str(install_mockery):
    spec, installer = create_installer('trivial-install-test-package')

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


def test_ensure_locked_err(install_mockery, monkeypatch, tmpdir, capsys):
    """Test _ensure_locked when a non-lock exception is raised."""
    mock_err_msg = 'Mock exception error'

    def _raise(lock, timeout):
        raise RuntimeError(mock_err_msg)

    spec, installer = create_installer('trivial-install-test-package')

    monkeypatch.setattr(ulk.Lock, 'acquire_read', _raise)
    with tmpdir.as_cwd():
        with pytest.raises(RuntimeError):
            installer._ensure_locked('read', spec.package)

        out = str(capsys.readouterr()[1])
        assert 'Failed to acquire a read lock' in out
        assert mock_err_msg in out


def test_ensure_locked_have(install_mockery, tmpdir, capsys):
    """Test _ensure_locked when already have lock."""
    spec, installer = create_installer('trivial-install-test-package')

    with tmpdir.as_cwd():
        # Test "downgrade" of a read lock (to a read lock)
        lock = lk.Lock('./test', default_timeout=1e-9, desc='test')
        lock_type = 'read'
        tpl = (lock_type, lock)
        installer.locks[installer.pkg_id] = tpl
        assert installer._ensure_locked(lock_type, spec.package) == tpl

        # Test "upgrade" of a read lock without read count to a write
        lock_type = 'write'
        err = 'Cannot upgrade lock'
        with pytest.raises(ulk.LockUpgradeError, match=err):
            installer._ensure_locked(lock_type, spec.package)

        out = str(capsys.readouterr()[1])
        assert 'Failed to upgrade to a write lock' in out
        assert 'exception when releasing read lock' in out

        # Test "upgrade" of the read lock *with* read count to a write
        lock._reads = 1
        tpl = (lock_type, lock)
        assert installer._ensure_locked(lock_type, spec.package) == tpl

        # Test "downgrade" of the write lock to a read lock
        lock_type = 'read'
        tpl = (lock_type, lock)
        assert installer._ensure_locked(lock_type, spec.package) == tpl


@pytest.mark.parametrize('lock_type,reads,writes', [
    ('read', 1, 0),
    ('write', 0, 1)])
def test_ensure_locked_new_lock(
        install_mockery, tmpdir, lock_type, reads, writes):
    pkg_id = 'a'
    spec, installer = create_installer(pkg_id)
    with tmpdir.as_cwd():
        ltype, lock = installer._ensure_locked(lock_type, spec.package)
        assert ltype == lock_type
        assert lock is not None
        assert lock._reads == reads
        assert lock._writes == writes


def test_ensure_locked_new_warn(install_mockery, monkeypatch, tmpdir, capsys):
    orig_pl = spack.database.Database.prefix_lock

    def _pl(db, spec, timeout):
        lock = orig_pl(db, spec, timeout)
        lock.default_timeout = 1e-9 if timeout is None else None
        return lock

    pkg_id = 'a'
    spec, installer = create_installer(pkg_id)

    monkeypatch.setattr(spack.database.Database, 'prefix_lock', _pl)

    lock_type = 'read'
    ltype, lock = installer._ensure_locked(lock_type, spec.package)
    assert ltype == lock_type
    assert lock is not None

    out = str(capsys.readouterr()[1])
    assert 'Expected prefix lock timeout' in out


def test_package_id_err(install_mockery):
    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='spec is not concretized'):
        inst.package_id(pkg)


def test_package_id_ok(install_mockery):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    assert pkg.name in inst.package_id(pkg)


def test_fake_install(install_mockery):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    pkg = spec.package
    inst._do_fake_install(pkg)
    assert os.path.isdir(pkg.prefix.lib)


def test_packages_needed_to_bootstrap_compiler_none(install_mockery):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    packages = inst._packages_needed_to_bootstrap_compiler(spec.package)
    assert not packages


def test_packages_needed_to_bootstrap_compiler_packages(install_mockery,
                                                        monkeypatch):
    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()

    def _conc_spec(compiler):
        return spack.spec.Spec('a').concretized()

    # Ensure we can get past functions that are precluding obtaining
    # packages.
    monkeypatch.setattr(spack.compilers, 'compilers_for_spec', _none)
    monkeypatch.setattr(spack.compilers, 'pkg_spec_for_compiler', _conc_spec)
    monkeypatch.setattr(spack.spec.Spec, 'concretize', _noop)

    packages = inst._packages_needed_to_bootstrap_compiler(spec.package)
    assert packages


def test_dump_packages_deps_ok(install_mockery, tmpdir, mock_repo_path):
    """Test happy path for dump_packages with dependencies."""

    spec_name = 'simple-inheritance'
    spec = spack.spec.Spec(spec_name).concretized()
    inst.dump_packages(spec, str(tmpdir))

    repo = mock_repo_path.repos[0]
    dest_pkg = repo.filename_for_package_name(spec_name)
    assert os.path.isfile(dest_pkg)


def test_dump_packages_deps_errs(install_mockery, tmpdir, monkeypatch, capsys):
    """Test error paths for dump_packages with dependencies."""
    orig_bpp = spack.store.layout.build_packages_path
    orig_dirname = spack.repo.Repo.dirname_for_package_name
    repo_err_msg = "Mock dirname_for_package_name"

    def bpp_path(spec):
        # Perform the original function
        source = orig_bpp(spec)
        # Mock the required directory structure for the repository
        _mock_repo(os.path.join(source, spec.namespace), spec.namespace)
        return source

    def _repoerr(repo, name):
        if name == 'cmake':
            raise spack.repo.RepoError(repo_err_msg)
        else:
            return orig_dirname(repo, name)

    # Now mock the creation of the required directory structure to cover
    # the try-except block
    monkeypatch.setattr(spack.store.layout, 'build_packages_path', bpp_path)

    spec = spack.spec.Spec('simple-inheritance').concretized()
    path = str(tmpdir)

    # The call to install_tree will raise the exception since not mocking
    # creation of dependency package files within *install* directories.
    with pytest.raises(IOError, match=path):
        inst.dump_packages(spec, path)

    # Now try the error path, which requires the mock directory structure
    # above
    monkeypatch.setattr(spack.repo.Repo, 'dirname_for_package_name', _repoerr)
    with pytest.raises(spack.repo.RepoError, match=repo_err_msg):
        inst.dump_packages(spec, path)

    out = str(capsys.readouterr()[1])
    assert "Couldn't copy in provenance for cmake" in out


def test_check_deps_status_install_failure(install_mockery, monkeypatch):
    spec, installer = create_installer('a')

    # Make sure the package is identified as failed
    monkeypatch.setattr(spack.database.Database, 'prefix_failed', _true)

    with pytest.raises(inst.InstallError, match='install failure'):
        installer._check_deps_status()


def test_check_deps_status_write_locked(install_mockery, monkeypatch):
    spec, installer = create_installer('a')

    # Ensure the lock is not acquired
    monkeypatch.setattr(inst.PackageInstaller, '_ensure_locked', _not_locked)

    with pytest.raises(inst.InstallError, match='write locked by another'):
        installer._check_deps_status()


def test_check_deps_status_external(install_mockery, monkeypatch):
    spec, installer = create_installer('a')

    # Mock the known dependent, b, as external so assumed to be installed
    monkeypatch.setattr(spack.spec.Spec, 'external', True)
    installer._check_deps_status()
    assert 'b' in installer.installed


def test_check_deps_status_upstream(install_mockery, monkeypatch):
    spec, installer = create_installer('a')

    # Mock the known dependent, b, as installed upstream
    monkeypatch.setattr(spack.package.PackageBase, 'installed_upstream', True)
    installer._check_deps_status()
    assert 'b' in installer.installed


def test_add_bootstrap_compilers(install_mockery, monkeypatch):
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
    spec, installer = create_installer('trivial-install-test-package')
    task = create_build_task(spec.package)

    monkeypatch.setattr(inst, '_install_from_cache', _true)
    installer._install_task(task)
    assert spec.package.name in installer.installed


def test_install_task_add_compiler(install_mockery, monkeypatch, capfd):
    config_msg = 'mock add_compilers_to_config'

    def _add(_compilers):
        tty.msg(config_msg)

    spec, installer = create_installer('a')
    task = create_build_task(spec.package)
    task.compiler = True

    # Preclude any meaningful side-effects
    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', _true)
    monkeypatch.setattr(inst.PackageInstaller, '_setup_install_dir', _noop)
    monkeypatch.setattr(spack.build_environment, 'fork', _noop)
    monkeypatch.setattr(spack.database.Database, 'add', _noop)
    monkeypatch.setattr(spack.compilers, 'add_compilers_to_config', _add)

    installer._install_task(task)

    out = capfd.readouterr()[0]
    assert config_msg in out


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


def test_setup_install_dir_grp(install_mockery, monkeypatch, capfd):
    """Test _setup_install_dir's group change."""
    mock_group = 'mockgroup'
    mock_chgrp_msg = 'Changing group for {0} to {1}'

    def _get_group(spec):
        return mock_group

    def _chgrp(path, group):
        tty.msg(mock_chgrp_msg.format(path, group))

    monkeypatch.setattr(spp, 'get_package_group', _get_group)
    monkeypatch.setattr(fs, 'chgrp', _chgrp)

    spec, installer = create_installer('trivial-install-test-package')

    fs.touchp(spec.prefix)
    metadatadir = spack.store.layout.metadata_path(spec)
    # Should fail with a "not a directory" error
    with pytest.raises(OSError, match=metadatadir):
        installer._setup_install_dir(spec.package)

    out = str(capfd.readouterr()[0])

    expected_msg = mock_chgrp_msg.format(spec.prefix, mock_group)
    assert expected_msg in out


def test_cleanup_failed_err(install_mockery, tmpdir, monkeypatch, capsys):
    """Test _cleanup_failed exception path."""
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


def test_update_failed_no_dependent_task(install_mockery):
    """Test _update_failed with missing dependent build tasks."""
    spec, installer = create_installer('dependent-install')

    for dep in spec.traverse(root=False):
        task = create_build_task(dep.package)
        installer._update_failed(task, mark=False)
        assert installer.failed[task.pkg_id] is None


def test_install_uninstalled_deps(install_mockery, monkeypatch, capsys):
    """Test install with uninstalled dependencies."""
    spec, installer = create_installer('dependent-install')

    # Skip the actual installation and any status updates
    monkeypatch.setattr(inst.PackageInstaller, '_install_task', _noop)
    monkeypatch.setattr(inst.PackageInstaller, '_update_installed', _noop)
    monkeypatch.setattr(inst.PackageInstaller, '_update_failed', _noop)

    msg = 'Cannot proceed with dependent-install'
    with pytest.raises(spack.installer.InstallError, match=msg):
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
    with pytest.raises(spack.installer.InstallError, match=msg):
        installer.install()

    out = str(capsys.readouterr())
    assert 'Warning: b failed to install' in out


def test_install_lock_failures(install_mockery, monkeypatch, capfd):
    """Cover basic install lock failure handling in a single pass."""
    def _requeued(installer, task):
        tty.msg('requeued {0}' .format(task.pkg.spec.name))

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

    with pytest.raises(dl.InstallDirectoryAlreadyExistsError, match=err):
        installer.install()

    assert 'b' in installer.installed


def test_install_skip_patch(install_mockery, mock_fetch):
    """Test the path skip_patch install path."""
    spec, installer = create_installer('b')

    installer.install(fake=False, skip_patch=True)

    assert 'b' in installer.installed

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import shutil
import sys

import py
import pytest

import llnl.util.filesystem as fs
import llnl.util.lock as ulk
import llnl.util.tty as tty

import spack.binary_distribution
import spack.compilers
import spack.concretize
import spack.config
import spack.database
import spack.installer as inst
import spack.package_base
import spack.package_prefs as prefs
import spack.repo
import spack.spec
import spack.store
import spack.util.lock as lk
import spack.version


def _mock_repo(root, namespace):
    """Create an empty repository at the specified root

    Args:
        root (str): path to the mock repository root
        namespace (str):  mock repo's namespace
    """
    repodir = py.path.local(root) if isinstance(root, str) else root
    repodir.ensure(spack.repo.packages_dir_name, dir=True)
    yaml = repodir.join("repo.yaml")
    yaml.write(
        """
repo:
   namespace: {0}
""".format(
            namespace
        )
    )


def _noop(*args, **kwargs):
    """Generic monkeypatch no-op routine."""
    pass


def _none(*args, **kwargs):
    """Generic monkeypatch function that always returns None."""
    return None


def _not_locked(installer, lock_type, pkg):
    """Generic monkeypatch function for _ensure_locked to return no lock"""
    tty.msg("{0} locked {1}".format(lock_type, pkg.spec.name))
    return lock_type, None


def _true(*args, **kwargs):
    """Generic monkeypatch function that always returns True."""
    return True


def create_build_task(pkg, install_args={}):
    """
    Create a built task for the given (concretized) package

    Args:
        pkg (spack.package_base.PackageBase): concretized package associated with
                                              the task
        install_args (dict): dictionary of kwargs (or install args)

    Return:
        (BuildTask) A basic package build task
    """
    request = inst.BuildRequest(pkg, install_args)
    return inst.BuildTask(pkg, request, False, 0, 0, inst.STATUS_ADDED, [])


def create_installer(installer_args):
    """
    Create an installer using the concretized spec for each arg

    Args:
        installer_args (list): the list of (spec name, kwargs) tuples

    Return:
        spack.installer.PackageInstaller: the associated package installer
    """
    const_arg = [(spec.package, kwargs) for spec, kwargs in installer_args]
    return inst.PackageInstaller(const_arg)


def installer_args(spec_names, kwargs={}):
    """Return a the installer argument with each spec paired with kwargs

    Args:
        spec_names (list): list of spec names
        kwargs (dict or None): install arguments to apply to all of the specs

    Returns:
        list: list of (spec, kwargs), the installer constructor argument
    """
    arg = []
    for name in spec_names:
        spec = spack.spec.Spec(name)
        spec.concretize()
        assert spec.concrete
        arg.append((spec, kwargs))
    return arg


@pytest.mark.parametrize(
    "sec,result",
    [(86400, "24h"), (3600, "1h"), (60, "1m"), (1.802, "1.80s"), (3723.456, "1h 2m 3.46s")],
)
def test_hms(sec, result):
    assert inst._hms(sec) == result


def test_get_dependent_ids(install_mockery, mock_packages):
    # Concretize the parent package, which handle dependency too
    spec = spack.spec.Spec("a")
    spec.concretize()
    assert spec.concrete

    pkg_id = inst.package_id(spec.package)

    # Grab the sole dependency of 'a', which is 'b'
    dep = spec.dependencies()[0]

    # Ensure the parent package is a dependent of the dependency package
    assert pkg_id in inst.get_dependent_ids(dep)


def test_install_msg(monkeypatch):
    """Test results of call to install_msg based on debug level."""
    name = "some-package"
    pid = 123456
    install_msg = "Installing {0}".format(name)

    monkeypatch.setattr(tty, "_debug", 0)
    assert inst.install_msg(name, pid, None) == install_msg

    install_status = inst.InstallStatus(1)
    expected = "{0} [0/1]".format(install_msg)
    assert inst.install_msg(name, pid, install_status) == expected

    monkeypatch.setattr(tty, "_debug", 1)
    assert inst.install_msg(name, pid, None) == install_msg

    # Expect the PID to be added at debug level 2
    monkeypatch.setattr(tty, "_debug", 2)
    expected = "{0}: {1}".format(pid, install_msg)
    assert inst.install_msg(name, pid, None) == expected


def test_install_from_cache_errors(install_mockery, capsys):
    """Test to ensure cover _install_from_cache errors."""
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()
    assert spec.concrete

    # Check with cache-only
    with pytest.raises(SystemExit):
        inst._install_from_cache(spec.package, True, True, False)

    captured = str(capsys.readouterr())
    assert "No binary" in captured
    assert "found when cache-only specified" in captured
    assert not spec.package.installed_from_binary_cache

    # Check when don't expect to install only from binary cache
    assert not inst._install_from_cache(spec.package, False, True, False)
    assert not spec.package.installed_from_binary_cache


def test_install_from_cache_ok(install_mockery, monkeypatch):
    """Test to ensure cover _install_from_cache to the return."""
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()
    monkeypatch.setattr(inst, "_try_install_from_binary_cache", _true)
    monkeypatch.setattr(spack.hooks, "post_install", _noop)

    assert inst._install_from_cache(spec.package, True, True, False)


def test_process_external_package_module(install_mockery, monkeypatch, capfd):
    """Test to simply cover the external module message path."""
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()
    assert spec.concrete

    # Ensure take the external module path WITHOUT any changes to the database
    monkeypatch.setattr(spack.database.Database, "get_record", _none)

    spec.external_path = "/actual/external/path/not/checked"
    spec.external_modules = ["unchecked_module"]
    inst._process_external_package(spec.package, False)

    out = capfd.readouterr()[0]
    assert "has external module in {0}".format(spec.external_modules) in out


def test_process_binary_cache_tarball_tar(install_mockery, monkeypatch, capfd):
    """Tests of _process_binary_cache_tarball with a tar file."""

    def _spec(spec, unsigned=False, mirrors_for_spec=None):
        return spec

    # Skip binary distribution functionality since assume tested elsewhere
    monkeypatch.setattr(spack.binary_distribution, "download_tarball", _spec)
    monkeypatch.setattr(spack.binary_distribution, "extract_tarball", _noop)

    # Skip database updates
    monkeypatch.setattr(spack.database.Database, "add", _noop)

    spec = spack.spec.Spec("a").concretized()
    assert inst._process_binary_cache_tarball(spec.package, explicit=False, unsigned=False)

    out = capfd.readouterr()[0]
    assert "Extracting a" in out
    assert "from binary cache" in out


def test_try_install_from_binary_cache(install_mockery, mock_packages, monkeypatch):
    """Test return false when no match exists in the mirror"""
    spec = spack.spec.Spec("mpich")
    spec.concretize()
    result = inst._try_install_from_binary_cache(spec.package, False, False)
    assert not result


def test_installer_repr(install_mockery):
    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)

    irep = installer.__repr__()
    assert irep.startswith(installer.__class__.__name__)
    assert "installed=" in irep
    assert "failed=" in irep


def test_installer_str(install_mockery):
    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)

    istr = str(installer)
    assert "#tasks=0" in istr
    assert "installed (0)" in istr
    assert "failed (0)" in istr


def test_installer_prune_built_build_deps(install_mockery, monkeypatch, tmpdir):
    r"""
    Ensure that build dependencies of installed deps are pruned
    from installer package queues.

               (a)
              /   \
             /     \
           (b)     (c) <--- is installed already so we should
              \   / | \     prune (f) from this install since
               \ /  |  \    it is *only* needed to build (b)
               (d) (e) (f)

    Thus since (c) is already installed our build_pq dag should
    only include four packages. [(a), (b), (c), (d), (e)]
    """

    @property
    def _mock_installed(self):
        return self.name in ["c"]

    # Mock the installed property to say that (b) is installed
    monkeypatch.setattr(spack.spec.Spec, "installed", _mock_installed)

    # Create mock repository with packages (a), (b), (c), (d), and (e)
    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("mock-repo"))

    builder.add_package("a", dependencies=[("b", "build", None), ("c", "build", None)])
    builder.add_package("b", dependencies=[("d", "build", None)])
    builder.add_package(
        "c", dependencies=[("d", "build", None), ("e", "all", None), ("f", "build", None)]
    )
    builder.add_package("d")
    builder.add_package("e")
    builder.add_package("f")

    with spack.repo.use_repositories(builder.root):
        const_arg = installer_args(["a"], {})
        installer = create_installer(const_arg)

        installer._init_queue()

        # Assert that (c) is not in the build_pq
        result = set([task.pkg_id[0] for _, task in installer.build_pq])
        expected = set(["a", "b", "c", "d", "e"])
        assert result == expected


def test_check_before_phase_error(install_mockery):
    s = spack.spec.Spec("trivial-install-test-package").concretized()
    s.package.stop_before_phase = "beforephase"
    with pytest.raises(inst.BadInstallPhase) as exc_info:
        inst._check_last_phase(s.package)

    err = str(exc_info.value)
    assert "is not a valid phase" in err
    assert s.package.stop_before_phase in err


def test_check_last_phase_error(install_mockery):
    s = spack.spec.Spec("trivial-install-test-package").concretized()
    s.package.stop_before_phase = None
    s.package.last_phase = "badphase"
    with pytest.raises(inst.BadInstallPhase) as exc_info:
        inst._check_last_phase(s.package)

    err = str(exc_info.value)
    assert "is not a valid phase" in err
    assert s.package.last_phase in err


def test_installer_ensure_ready_errors(install_mockery, monkeypatch):
    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec

    fmt = r"cannot be installed locally.*{0}"
    # Force an external package error
    path, modules = spec.external_path, spec.external_modules
    spec.external_path = "/actual/external/path/not/checked"
    spec.external_modules = ["unchecked_module"]
    msg = fmt.format("is external")
    with pytest.raises(inst.ExternalPackageError, match=msg):
        installer._ensure_install_ready(spec.package)

    # Force an upstream package error
    spec.external_path, spec.external_modules = path, modules
    monkeypatch.setattr(spack.spec.Spec, "installed_upstream", True)
    msg = fmt.format("is upstream")
    with pytest.raises(inst.UpstreamPackageError, match=msg):
        installer._ensure_install_ready(spec.package)

    # Force an install lock error, which should occur naturally since
    # we are calling an internal method prior to any lock-related setup
    monkeypatch.setattr(spack.spec.Spec, "installed_upstream", False)
    assert len(installer.locks) == 0
    with pytest.raises(inst.InstallLockError, match=fmt.format("not locked")):
        installer._ensure_install_ready(spec.package)


def test_ensure_locked_err(install_mockery, monkeypatch, tmpdir, capsys):
    """Test _ensure_locked when a non-lock exception is raised."""
    mock_err_msg = "Mock exception error"

    def _raise(lock, timeout=None):
        raise RuntimeError(mock_err_msg)

    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec

    monkeypatch.setattr(ulk.Lock, "acquire_read", _raise)
    with tmpdir.as_cwd():
        with pytest.raises(RuntimeError):
            installer._ensure_locked("read", spec.package)

        out = str(capsys.readouterr()[1])
        assert "Failed to acquire a read lock" in out
        assert mock_err_msg in out


def test_ensure_locked_have(install_mockery, tmpdir, capsys):
    """Test _ensure_locked when already have lock."""
    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec
    pkg_id = inst.package_id(spec.package)

    with tmpdir.as_cwd():
        # Test "downgrade" of a read lock (to a read lock)
        lock = lk.Lock("./test", default_timeout=1e-9, desc="test")
        lock_type = "read"
        tpl = (lock_type, lock)
        installer.locks[pkg_id] = tpl
        assert installer._ensure_locked(lock_type, spec.package) == tpl

        # Test "upgrade" of a read lock without read count to a write
        lock_type = "write"
        err = "Cannot upgrade lock"
        with pytest.raises(ulk.LockUpgradeError, match=err):
            installer._ensure_locked(lock_type, spec.package)

        out = str(capsys.readouterr()[1])
        assert "Failed to upgrade to a write lock" in out
        assert "exception when releasing read lock" in out

        # Test "upgrade" of the read lock *with* read count to a write
        lock._reads = 1
        tpl = (lock_type, lock)
        assert installer._ensure_locked(lock_type, spec.package) == tpl

        # Test "downgrade" of the write lock to a read lock
        lock_type = "read"
        tpl = (lock_type, lock)
        assert installer._ensure_locked(lock_type, spec.package) == tpl


@pytest.mark.parametrize("lock_type,reads,writes", [("read", 1, 0), ("write", 0, 1)])
def test_ensure_locked_new_lock(install_mockery, tmpdir, lock_type, reads, writes):
    pkg_id = "a"
    const_arg = installer_args([pkg_id], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec
    with tmpdir.as_cwd():
        ltype, lock = installer._ensure_locked(lock_type, spec.package)
        assert ltype == lock_type
        assert lock is not None
        assert lock._reads == reads
        assert lock._writes == writes


def test_ensure_locked_new_warn(install_mockery, monkeypatch, tmpdir, capsys):
    orig_pl = spack.database.SpecLocker.lock

    def _pl(db, spec, timeout):
        lock = orig_pl(db, spec, timeout)
        lock.default_timeout = 1e-9 if timeout is None else None
        return lock

    pkg_id = "a"
    const_arg = installer_args([pkg_id], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec

    monkeypatch.setattr(spack.database.SpecLocker, "lock", _pl)

    lock_type = "read"
    ltype, lock = installer._ensure_locked(lock_type, spec.package)
    assert ltype == lock_type
    assert lock is not None

    out = str(capsys.readouterr()[1])
    assert "Expected prefix lock timeout" in out


def test_package_id_err(install_mockery):
    s = spack.spec.Spec("trivial-install-test-package")
    pkg_cls = spack.repo.PATH.get_pkg_class(s.name)
    with pytest.raises(ValueError, match="spec is not concretized"):
        inst.package_id(pkg_cls(s))


def test_package_id_ok(install_mockery):
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    assert pkg.name in inst.package_id(pkg)


def test_fake_install(install_mockery):
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()
    assert spec.concrete

    pkg = spec.package
    inst._do_fake_install(pkg)
    assert os.path.isdir(pkg.prefix.lib)


def test_packages_needed_to_bootstrap_compiler_none(install_mockery):
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()
    assert spec.concrete

    packages = inst._packages_needed_to_bootstrap_compiler(
        spec.compiler, spec.architecture, [spec.package]
    )
    assert not packages


@pytest.mark.xfail(reason="fails when assuming Spec.package can only be called on concrete specs")
def test_packages_needed_to_bootstrap_compiler_packages(install_mockery, monkeypatch):
    spec = spack.spec.Spec("trivial-install-test-package")
    spec.concretize()

    def _conc_spec(compiler):
        return spack.spec.Spec("a").concretized()

    # Ensure we can get past functions that are precluding obtaining
    # packages.
    monkeypatch.setattr(spack.compilers, "compilers_for_spec", _none)
    monkeypatch.setattr(spack.compilers, "pkg_spec_for_compiler", _conc_spec)
    monkeypatch.setattr(spack.spec.Spec, "concretize", _noop)

    packages = inst._packages_needed_to_bootstrap_compiler(
        spec.compiler, spec.architecture, [spec.package]
    )
    assert packages


def test_update_tasks_for_compiler_packages_as_compiler(mock_packages, config, monkeypatch):
    spec = spack.spec.Spec("trivial-install-test-package").concretized()
    installer = inst.PackageInstaller([(spec.package, {})])

    # Add a task to the queue
    installer._add_init_task(spec.package, installer.build_requests[0], False, {})

    # monkeypatch to make the list of compilers be what we test
    def fake_package_list(compiler, architecture, pkgs):
        return [(spec.package, True)]

    monkeypatch.setattr(inst, "_packages_needed_to_bootstrap_compiler", fake_package_list)

    installer._add_bootstrap_compilers("fake", "fake", "fake", None, {})

    # Check that the only task is now a compiler task
    assert len(installer.build_pq) == 1
    assert installer.build_pq[0][1].compiler


def test_bootstrapping_compilers_with_different_names_from_spec(
    install_mockery, mutable_config, mock_fetch, archspec_host_is_spack_test_host
):
    with spack.config.override("config:install_missing_compilers", True):
        with spack.concretize.disable_compiler_existence_check():
            spec = spack.spec.Spec("trivial-install-test-package%oneapi@=22.2.0").concretized()
            spec.package.do_install()

            assert (
                spack.spec.CompilerSpec("oneapi@=22.2.0") in spack.compilers.all_compiler_specs()
            )


def test_dump_packages_deps_ok(install_mockery, tmpdir, mock_packages):
    """Test happy path for dump_packages with dependencies."""

    spec_name = "simple-inheritance"
    spec = spack.spec.Spec(spec_name).concretized()
    inst.dump_packages(spec, str(tmpdir))

    repo = mock_packages.repos[0]
    dest_pkg = repo.filename_for_package_name(spec_name)
    assert os.path.isfile(dest_pkg)


def test_dump_packages_deps_errs(install_mockery, tmpdir, monkeypatch, capsys):
    """Test error paths for dump_packages with dependencies."""
    orig_bpp = spack.store.STORE.layout.build_packages_path
    orig_dirname = spack.repo.Repo.dirname_for_package_name
    repo_err_msg = "Mock dirname_for_package_name"

    def bpp_path(spec):
        # Perform the original function
        source = orig_bpp(spec)
        # Mock the required directory structure for the repository
        _mock_repo(os.path.join(source, spec.namespace), spec.namespace)
        return source

    def _repoerr(repo, name):
        if name == "cmake":
            raise spack.repo.RepoError(repo_err_msg)
        else:
            return orig_dirname(repo, name)

    # Now mock the creation of the required directory structure to cover
    # the try-except block
    monkeypatch.setattr(spack.store.STORE.layout, "build_packages_path", bpp_path)

    spec = spack.spec.Spec("simple-inheritance").concretized()
    path = str(tmpdir)

    # The call to install_tree will raise the exception since not mocking
    # creation of dependency package files within *install* directories.
    with pytest.raises(IOError, match=path if sys.platform != "win32" else ""):
        inst.dump_packages(spec, path)

    # Now try the error path, which requires the mock directory structure
    # above
    monkeypatch.setattr(spack.repo.Repo, "dirname_for_package_name", _repoerr)
    with pytest.raises(spack.repo.RepoError, match=repo_err_msg):
        inst.dump_packages(spec, path)

    out = str(capsys.readouterr()[1])
    assert "Couldn't copy in provenance for cmake" in out


def test_clear_failures_success(tmpdir):
    """Test the clear_failures happy path."""
    failures = spack.database.FailureTracker(str(tmpdir), default_timeout=0.1)

    spec = spack.spec.Spec("a")
    spec._mark_concrete()

    # Set up a test prefix failure lock
    failures.mark(spec)
    assert failures.has_failed(spec)

    # Now clear failure tracking
    failures.clear_all()

    # Ensure there are no cached failure locks or failure marks
    assert len(failures.locker.locks) == 0
    assert len(os.listdir(failures.dir)) == 0

    # Ensure the core directory and failure lock file still exist
    assert os.path.isdir(failures.dir)

    # Locks on windows are a no-op
    if sys.platform != "win32":
        assert os.path.isfile(failures.locker.lock_path)


@pytest.mark.xfail(sys.platform == "win32", reason="chmod does not prevent removal on Win")
def test_clear_failures_errs(tmpdir, capsys):
    """Test the clear_failures exception paths."""
    failures = spack.database.FailureTracker(str(tmpdir), default_timeout=0.1)
    spec = spack.spec.Spec("a")
    spec._mark_concrete()
    failures.mark(spec)

    # Make the file marker not writeable, so that clearing_failures fails
    failures.dir.chmod(0o000)

    # Clear failure tracking
    failures.clear_all()

    # Ensure expected warning generated
    out = str(capsys.readouterr()[1])
    assert "Unable to remove failure" in out
    failures.dir.chmod(0o750)


def test_combine_phase_logs(tmpdir):
    """Write temporary files, and assert that combine phase logs works
    to combine them into one file. We aren't currently using this function,
    but it's available when the logs are refactored to be written separately.
    """
    log_files = ["configure-out.txt", "install-out.txt", "build-out.txt"]
    phase_log_files = []

    # Create and write to dummy phase log files
    for log_file in log_files:
        phase_log_file = os.path.join(str(tmpdir), log_file)
        with open(phase_log_file, "w") as plf:
            plf.write("Output from %s\n" % log_file)
        phase_log_files.append(phase_log_file)

    # This is the output log we will combine them into
    combined_log = os.path.join(str(tmpdir), "combined-out.txt")
    inst.combine_phase_logs(phase_log_files, combined_log)
    with open(combined_log, "r") as log_file:
        out = log_file.read()

    # Ensure each phase log file is represented
    for log_file in log_files:
        assert "Output from %s\n" % log_file in out


def test_combine_phase_logs_does_not_care_about_encoding(tmpdir):
    # this is invalid utf-8 at a minimum
    data = b"\x00\xF4\xBF\x00\xBF\xBF"
    input = [str(tmpdir.join("a")), str(tmpdir.join("b"))]
    output = str(tmpdir.join("c"))

    for path in input:
        with open(path, "wb") as f:
            f.write(data)

    inst.combine_phase_logs(input, output)

    with open(output, "rb") as f:
        assert f.read() == data * 2


def test_check_deps_status_install_failure(install_mockery):
    """Tests that checking the dependency status on a request to install
    'a' fails, if we mark the dependency as failed.
    """
    s = spack.spec.Spec("a").concretized()
    for dep in s.traverse(root=False):
        spack.store.STORE.failure_tracker.mark(dep)

    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]

    with pytest.raises(inst.InstallError, match="install failure"):
        installer._check_deps_status(request)


def test_check_deps_status_write_locked(install_mockery, monkeypatch):
    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]

    # Ensure the lock is not acquired
    monkeypatch.setattr(inst.PackageInstaller, "_ensure_locked", _not_locked)

    with pytest.raises(inst.InstallError, match="write locked by another"):
        installer._check_deps_status(request)


def test_check_deps_status_external(install_mockery, monkeypatch):
    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]

    # Mock the known dependent, b, as external so assumed to be installed
    monkeypatch.setattr(spack.spec.Spec, "external", True)
    installer._check_deps_status(request)

    # exotic architectures will add dependencies on gnuconfig, which we want to ignore
    installed = [x for x in installer.installed if not x.startswith("gnuconfig")]
    assert installed[0].startswith("b")


def test_check_deps_status_upstream(install_mockery, monkeypatch):
    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]

    # Mock the known dependent, b, as installed upstream
    monkeypatch.setattr(spack.spec.Spec, "installed_upstream", True)
    installer._check_deps_status(request)

    # exotic architectures will add dependencies on gnuconfig, which we want to ignore
    installed = [x for x in installer.installed if not x.startswith("gnuconfig")]
    assert installed[0].startswith("b")


def test_add_bootstrap_compilers(install_mockery, monkeypatch):
    from collections import defaultdict

    def _pkgs(compiler, architecture, pkgs):
        spec = spack.spec.Spec("mpi").concretized()
        return [(spec.package, True)]

    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]
    all_deps = defaultdict(set)

    monkeypatch.setattr(inst, "_packages_needed_to_bootstrap_compiler", _pkgs)
    installer._add_bootstrap_compilers("fake", "fake", [request.pkg], request, all_deps)

    ids = list(installer.build_tasks)
    assert len(ids) == 1
    task = installer.build_tasks[ids[0]]
    assert task.compiler


def test_prepare_for_install_on_installed(install_mockery, monkeypatch):
    """Test of _prepare_for_install's early return for installed task path."""
    const_arg = installer_args(["dependent-install"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]

    install_args = {"keep_prefix": True, "keep_stage": True, "restage": False}
    task = create_build_task(request.pkg, install_args)
    installer.installed.add(task.pkg_id)

    monkeypatch.setattr(inst.PackageInstaller, "_ensure_install_ready", _noop)
    installer._prepare_for_install(task)


def test_installer_init_requests(install_mockery):
    """Test of installer initial requests."""
    spec_name = "dependent-install"
    with spack.config.override("config:install_missing_compilers", True):
        const_arg = installer_args([spec_name], {})
        installer = create_installer(const_arg)

        # There is only one explicit request in this case
        assert len(installer.build_requests) == 1
        request = installer.build_requests[0]
        assert request.pkg.name == spec_name


def test_install_task_use_cache(install_mockery, monkeypatch):
    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)
    request = installer.build_requests[0]
    task = create_build_task(request.pkg)

    monkeypatch.setattr(inst, "_install_from_cache", _true)
    installer._install_task(task, None)
    assert request.pkg_id in installer.installed


def test_install_task_add_compiler(install_mockery, monkeypatch, capfd):
    config_msg = "mock add_compilers_to_config"

    def _add(_compilers):
        tty.msg(config_msg)

    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    task = create_build_task(installer.build_requests[0].pkg)
    task.compiler = True

    # Preclude any meaningful side-effects
    monkeypatch.setattr(spack.package_base.PackageBase, "unit_test_check", _true)
    monkeypatch.setattr(inst.PackageInstaller, "_setup_install_dir", _noop)
    monkeypatch.setattr(spack.build_environment, "start_build_process", _noop)
    monkeypatch.setattr(spack.database.Database, "add", _noop)
    monkeypatch.setattr(spack.compilers, "add_compilers_to_config", _add)

    installer._install_task(task, None)

    out = capfd.readouterr()[0]
    assert config_msg in out


def test_release_lock_write_n_exception(install_mockery, tmpdir, capsys):
    """Test _release_lock for supposed write lock with exception."""
    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)

    pkg_id = "test"
    with tmpdir.as_cwd():
        lock = lk.Lock("./test", default_timeout=1e-9, desc="test")
        installer.locks[pkg_id] = ("write", lock)
        assert lock._writes == 0

        installer._release_lock(pkg_id)
        out = str(capsys.readouterr()[1])
        msg = "exception when releasing write lock for {0}".format(pkg_id)
        assert msg in out


@pytest.mark.parametrize("installed", [True, False])
def test_push_task_skip_processed(install_mockery, installed):
    """Test to ensure skip re-queueing a processed package."""
    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    assert len(list(installer.build_tasks)) == 0

    # Mark the package as installed OR failed
    task = create_build_task(installer.build_requests[0].pkg)
    if installed:
        installer.installed.add(task.pkg_id)
    else:
        installer.failed[task.pkg_id] = None

    installer._push_task(task)

    assert len(list(installer.build_tasks)) == 0


def test_requeue_task(install_mockery, capfd):
    """Test to ensure cover _requeue_task."""
    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    task = create_build_task(installer.build_requests[0].pkg)

    # temporarily set tty debug messages on so we can test output
    current_debug_level = tty.debug_level()
    tty.set_debug(1)
    installer._requeue_task(task, None)
    tty.set_debug(current_debug_level)

    ids = list(installer.build_tasks)
    assert len(ids) == 1
    qtask = installer.build_tasks[ids[0]]
    assert qtask.status == inst.STATUS_INSTALLING
    assert qtask.sequence > task.sequence
    assert qtask.attempts == task.attempts + 1

    out = capfd.readouterr()[1]
    assert "Installing a" in out
    assert " in progress by another process" in out


def test_cleanup_all_tasks(install_mockery, monkeypatch):
    """Test to ensure cover _cleanup_all_tasks."""

    def _mktask(pkg):
        return create_build_task(pkg)

    def _rmtask(installer, pkg_id):
        raise RuntimeError("Raise an exception to test except path")

    const_arg = installer_args(["a"], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec

    # Cover task removal happy path
    installer.build_tasks["a"] = _mktask(spec.package)
    installer._cleanup_all_tasks()
    assert len(installer.build_tasks) == 0

    # Cover task removal exception path
    installer.build_tasks["a"] = _mktask(spec.package)
    monkeypatch.setattr(inst.PackageInstaller, "_remove_task", _rmtask)
    installer._cleanup_all_tasks()
    assert len(installer.build_tasks) == 1


def test_setup_install_dir_grp(install_mockery, monkeypatch, capfd):
    """Test _setup_install_dir's group change."""
    mock_group = "mockgroup"
    mock_chgrp_msg = "Changing group for {0} to {1}"

    def _get_group(spec):
        return mock_group

    def _chgrp(path, group, follow_symlinks=True):
        tty.msg(mock_chgrp_msg.format(path, group))

    monkeypatch.setattr(prefs, "get_package_group", _get_group)
    monkeypatch.setattr(fs, "chgrp", _chgrp)

    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec

    fs.touchp(spec.prefix)
    metadatadir = spack.store.STORE.layout.metadata_path(spec)
    # Regex matching with Windows style paths typically fails
    # so we skip the match check here
    if sys.platform == "win32":
        metadatadir = None
    # Should fail with a "not a directory" error
    with pytest.raises(OSError, match=metadatadir):
        installer._setup_install_dir(spec.package)

    out = str(capfd.readouterr()[0])

    expected_msg = mock_chgrp_msg.format(spec.prefix, mock_group)
    assert expected_msg in out


def test_cleanup_failed_err(install_mockery, tmpdir, monkeypatch, capsys):
    """Test _cleanup_failed exception path."""
    msg = "Fake release_write exception"

    def _raise_except(lock):
        raise RuntimeError(msg)

    const_arg = installer_args(["trivial-install-test-package"], {})
    installer = create_installer(const_arg)

    monkeypatch.setattr(lk.Lock, "release_write", _raise_except)
    pkg_id = "test"
    with tmpdir.as_cwd():
        lock = lk.Lock("./test", default_timeout=1e-9, desc="test")
        installer.failed[pkg_id] = lock

        installer._cleanup_failed(pkg_id)
        out = str(capsys.readouterr()[1])
        assert "exception when removing failure tracking" in out
        assert msg in out


def test_update_failed_no_dependent_task(install_mockery):
    """Test _update_failed with missing dependent build tasks."""
    const_arg = installer_args(["dependent-install"], {})
    installer = create_installer(const_arg)
    spec = installer.build_requests[0].pkg.spec

    for dep in spec.traverse(root=False):
        task = create_build_task(dep.package)
        installer._update_failed(task, mark=False)
        assert installer.failed[task.pkg_id] is None


def test_install_uninstalled_deps(install_mockery, monkeypatch, capsys):
    """Test install with uninstalled dependencies."""
    const_arg = installer_args(["dependent-install"], {})
    installer = create_installer(const_arg)

    # Skip the actual installation and any status updates
    monkeypatch.setattr(inst.PackageInstaller, "_install_task", _noop)
    monkeypatch.setattr(inst.PackageInstaller, "_update_installed", _noop)
    monkeypatch.setattr(inst.PackageInstaller, "_update_failed", _noop)

    msg = "Cannot proceed with dependent-install"
    with pytest.raises(inst.InstallError, match=msg):
        installer.install()

    out = str(capsys.readouterr())
    assert "Detected uninstalled dependencies for" in out


def test_install_failed(install_mockery, monkeypatch, capsys):
    """Test install with failed install."""
    const_arg = installer_args(["b"], {})
    installer = create_installer(const_arg)

    # Make sure the package is identified as failed
    monkeypatch.setattr(spack.database.FailureTracker, "has_failed", _true)

    with pytest.raises(inst.InstallError, match="request failed"):
        installer.install()

    out = str(capsys.readouterr())
    assert installer.build_requests[0].pkg_id in out
    assert "failed to install" in out


def test_install_failed_not_fast(install_mockery, monkeypatch, capsys):
    """Test install with failed install."""
    const_arg = installer_args(["a"], {"fail_fast": False})
    installer = create_installer(const_arg)

    # Make sure the package is identified as failed
    monkeypatch.setattr(spack.database.FailureTracker, "has_failed", _true)

    with pytest.raises(inst.InstallError, match="request failed"):
        installer.install()

    out = str(capsys.readouterr())
    assert "failed to install" in out
    assert "Skipping build of a" in out


def test_install_fail_on_interrupt(install_mockery, monkeypatch):
    """Test ctrl-c interrupted install."""
    spec_name = "a"
    err_msg = "mock keyboard interrupt for {0}".format(spec_name)

    def _interrupt(installer, task, install_status, **kwargs):
        if task.pkg.name == spec_name:
            raise KeyboardInterrupt(err_msg)
        else:
            installer.installed.add(task.pkg.name)

    const_arg = installer_args([spec_name], {})
    installer = create_installer(const_arg)

    # Raise a KeyboardInterrupt error to trigger early termination
    monkeypatch.setattr(inst.PackageInstaller, "_install_task", _interrupt)

    with pytest.raises(KeyboardInterrupt, match=err_msg):
        installer.install()

    assert "b" in installer.installed  # ensure dependency of a is 'installed'
    assert spec_name not in installer.installed


def test_install_fail_single(install_mockery, monkeypatch):
    """Test expected results for failure of single package."""
    spec_name = "a"
    err_msg = "mock internal package build error for {0}".format(spec_name)

    class MyBuildException(Exception):
        pass

    def _install(installer, task, install_status, **kwargs):
        if task.pkg.name == spec_name:
            raise MyBuildException(err_msg)
        else:
            installer.installed.add(task.pkg.name)

    const_arg = installer_args([spec_name], {})
    installer = create_installer(const_arg)

    # Raise a KeyboardInterrupt error to trigger early termination
    monkeypatch.setattr(inst.PackageInstaller, "_install_task", _install)

    with pytest.raises(MyBuildException, match=err_msg):
        installer.install()

    assert "b" in installer.installed  # ensure dependency of a is 'installed'
    assert spec_name not in installer.installed


def test_install_fail_multi(install_mockery, monkeypatch):
    """Test expected results for failure of multiple packages."""
    spec_name = "c"
    err_msg = "mock internal package build error"

    class MyBuildException(Exception):
        pass

    def _install(installer, task, install_status, **kwargs):
        if task.pkg.name == spec_name:
            raise MyBuildException(err_msg)
        else:
            installer.installed.add(task.pkg.name)

    const_arg = installer_args([spec_name, "a"], {})
    installer = create_installer(const_arg)

    # Raise a KeyboardInterrupt error to trigger early termination
    monkeypatch.setattr(inst.PackageInstaller, "_install_task", _install)

    with pytest.raises(inst.InstallError, match="Installation request failed"):
        installer.install()

    assert "a" in installer.installed  # ensure the the second spec installed
    assert spec_name not in installer.installed


def test_install_fail_fast_on_detect(install_mockery, monkeypatch, capsys):
    """Test fail_fast install when an install failure is detected."""
    const_arg = installer_args(["b"], {"fail_fast": False})
    const_arg.extend(installer_args(["c"], {"fail_fast": True}))
    installer = create_installer(const_arg)
    pkg_ids = [inst.package_id(spec.package) for spec, _ in const_arg]

    # Make sure all packages are identified as failed
    #
    # This will prevent b from installing, which will cause the build of a
    # to be skipped.
    monkeypatch.setattr(spack.database.FailureTracker, "has_failed", _true)

    with pytest.raises(inst.InstallError, match="after first install failure"):
        installer.install()

    assert pkg_ids[0] in installer.failed, "Expected b to be marked as failed"
    assert pkg_ids[1] not in installer.failed, "Expected no attempt to install c"

    out = capsys.readouterr()[1]
    assert "{0} failed to install".format(pkg_ids[0]) in out


def _test_install_fail_fast_on_except_patch(installer, **kwargs):
    """Helper for test_install_fail_fast_on_except."""
    # This is a module-scope function and not a local function because it
    # needs to be pickleable.
    raise RuntimeError("mock patch failure")


@pytest.mark.disable_clean_stage_check
def test_install_fail_fast_on_except(install_mockery, monkeypatch, capsys):
    """Test fail_fast install when an install failure results from an error."""
    const_arg = installer_args(["a"], {"fail_fast": True})
    installer = create_installer(const_arg)

    # Raise a non-KeyboardInterrupt exception to trigger fast failure.
    #
    # This will prevent b from installing, which will cause the build of a
    # to be skipped.
    monkeypatch.setattr(
        spack.package_base.PackageBase, "do_patch", _test_install_fail_fast_on_except_patch
    )

    with pytest.raises(inst.InstallError, match="mock patch failure"):
        installer.install()

    out = str(capsys.readouterr())
    assert "Skipping build of a" in out


def test_install_lock_failures(install_mockery, monkeypatch, capfd):
    """Cover basic install lock failure handling in a single pass."""

    def _requeued(installer, task, install_status):
        tty.msg("requeued {0}".format(task.pkg.spec.name))

    const_arg = installer_args(["b"], {})
    installer = create_installer(const_arg)

    # Ensure never acquire a lock
    monkeypatch.setattr(inst.PackageInstaller, "_ensure_locked", _not_locked)

    # Ensure don't continually requeue the task
    monkeypatch.setattr(inst.PackageInstaller, "_requeue_task", _requeued)

    with pytest.raises(inst.InstallError, match="request failed"):
        installer.install()

    out = capfd.readouterr()[0]
    expected = ["write locked", "read locked", "requeued"]
    for exp, ln in zip(expected, out.split("\n")):
        assert exp in ln


def test_install_lock_installed_requeue(install_mockery, monkeypatch, capfd):
    """Cover basic install handling for installed package."""
    const_arg = installer_args(["b"], {})
    b, _ = const_arg[0]
    installer = create_installer(const_arg)
    b_pkg_id = inst.package_id(b.package)

    def _prep(installer, task):
        installer.installed.add(b_pkg_id)
        tty.msg("{0} is installed".format(b_pkg_id))

        # also do not allow the package to be locked again
        monkeypatch.setattr(inst.PackageInstaller, "_ensure_locked", _not_locked)

    def _requeued(installer, task, install_status):
        tty.msg("requeued {0}".format(inst.package_id(task.pkg)))

    # Flag the package as installed
    monkeypatch.setattr(inst.PackageInstaller, "_prepare_for_install", _prep)

    # Ensure don't continually requeue the task
    monkeypatch.setattr(inst.PackageInstaller, "_requeue_task", _requeued)

    with pytest.raises(inst.InstallError, match="request failed"):
        installer.install()

    assert b_pkg_id not in installer.installed

    out = capfd.readouterr()[0]
    expected = ["is installed", "read locked", "requeued"]
    for exp, ln in zip(expected, out.split("\n")):
        assert exp in ln


def test_install_read_locked_requeue(install_mockery, monkeypatch, capfd):
    """Cover basic read lock handling for uninstalled package with requeue."""
    orig_fn = inst.PackageInstaller._ensure_locked

    def _read(installer, lock_type, pkg):
        tty.msg("{0}->read locked {1}".format(lock_type, pkg.spec.name))
        return orig_fn(installer, "read", pkg)

    def _prep(installer, task):
        tty.msg("preparing {0}".format(task.pkg.spec.name))
        assert task.pkg.spec.name not in installer.installed

    def _requeued(installer, task, install_status):
        tty.msg("requeued {0}".format(task.pkg.spec.name))

    # Force a read lock
    monkeypatch.setattr(inst.PackageInstaller, "_ensure_locked", _read)

    # Flag the package as installed
    monkeypatch.setattr(inst.PackageInstaller, "_prepare_for_install", _prep)

    # Ensure don't continually requeue the task
    monkeypatch.setattr(inst.PackageInstaller, "_requeue_task", _requeued)

    const_arg = installer_args(["b"], {})
    installer = create_installer(const_arg)

    with pytest.raises(inst.InstallError, match="request failed"):
        installer.install()

    assert "b" not in installer.installed

    out = capfd.readouterr()[0]
    expected = ["write->read locked", "preparing", "requeued"]
    for exp, ln in zip(expected, out.split("\n")):
        assert exp in ln


def test_install_skip_patch(install_mockery, mock_fetch):
    """Test the path skip_patch install path."""
    spec_name = "b"
    const_arg = installer_args([spec_name], {"fake": False, "skip_patch": True})
    installer = create_installer(const_arg)

    installer.install()

    spec, install_args = const_arg[0]
    assert inst.package_id(spec.package) in installer.installed


def test_install_implicit(install_mockery, mock_fetch):
    """Test the path skip_patch install path."""
    spec_name = "trivial-install-test-package"
    const_arg = installer_args([spec_name], {"fake": False})
    installer = create_installer(const_arg)
    pkg = installer.build_requests[0].pkg
    assert not create_build_task(pkg, {"explicit": False}).explicit
    assert create_build_task(pkg, {"explicit": True}).explicit
    assert create_build_task(pkg).explicit


def test_overwrite_install_backup_success(temporary_store, config, mock_packages, tmpdir):
    """
    When doing an overwrite install that fails, Spack should restore the backup
    of the original prefix, and leave the original spec marked installed.
    """
    # Get a build task. TODO: refactor this to avoid calling internal methods
    const_arg = installer_args(["b"])
    installer = create_installer(const_arg)
    installer._init_queue()
    task = installer._pop_task()

    # Make sure the install prefix exists with some trivial file
    installed_file = os.path.join(task.pkg.prefix, "some_file")
    fs.touchp(installed_file)

    class InstallerThatWipesThePrefixDir:
        def _install_task(self, task, install_status):
            shutil.rmtree(task.pkg.prefix, ignore_errors=True)
            fs.mkdirp(task.pkg.prefix)
            raise Exception("Some fatal install error")

    class FakeDatabase:
        called = False

        def remove(self, spec):
            self.called = True

    fake_installer = InstallerThatWipesThePrefixDir()
    fake_db = FakeDatabase()
    overwrite_install = inst.OverwriteInstall(fake_installer, fake_db, task, None)

    # Installation should throw the installation exception, not the backup
    # failure.
    with pytest.raises(Exception, match="Some fatal install error"):
        overwrite_install.install()

    # Make sure the package is not marked uninstalled and the original dir
    # is back.
    assert not fake_db.called
    assert os.path.exists(installed_file)


def test_overwrite_install_backup_failure(temporary_store, config, mock_packages, tmpdir):
    """
    When doing an overwrite install that fails, Spack should try to recover the
    original prefix. If that fails, the spec is lost, and it should be removed
    from the database.
    """

    class InstallerThatAccidentallyDeletesTheBackupDir:
        def _install_task(self, task, install_status):
            # Remove the backup directory, which is at the same level as the prefix,
            # starting with .backup
            backup_glob = os.path.join(
                os.path.dirname(os.path.normpath(task.pkg.prefix)), ".backup*"
            )
            for backup in glob.iglob(backup_glob):
                shutil.rmtree(backup)
            raise Exception("Some fatal install error")

    class FakeDatabase:
        called = False

        def remove(self, spec):
            self.called = True

    # Get a build task. TODO: refactor this to avoid calling internal methods
    const_arg = installer_args(["b"])
    installer = create_installer(const_arg)
    installer._init_queue()
    task = installer._pop_task()

    # Make sure the install prefix exists
    installed_file = os.path.join(task.pkg.prefix, "some_file")
    fs.touchp(installed_file)

    fake_installer = InstallerThatAccidentallyDeletesTheBackupDir()
    fake_db = FakeDatabase()
    overwrite_install = inst.OverwriteInstall(fake_installer, fake_db, task, None)

    # Installation should throw the installation exception, not the backup
    # failure.
    with pytest.raises(Exception, match="Some fatal install error"):
        overwrite_install.install()

    # Make sure that `remove` was called on the database after an unsuccessful
    # attempt to restore the backup.
    assert fake_db.called


def test_term_status_line():
    # Smoke test for TermStatusLine; to actually test output it would be great
    # to pass a StringIO instance, but we use tty.msg() internally which does not
    # accept that. `with log_output(buf)` doesn't really work because it trims output
    # and we actually want to test for escape sequences etc.
    x = inst.TermStatusLine(enabled=True)
    x.add("a")
    x.add("b")
    x.clear()


@pytest.mark.parametrize(
    "explicit_args,is_explicit",
    [({"explicit": False}, False), ({"explicit": True}, True), ({}, True)],
)
def test_single_external_implicit_install(install_mockery, explicit_args, is_explicit):
    pkg = "trivial-install-test-package"
    s = spack.spec.Spec(pkg).concretized()
    s.external_path = "/usr"
    create_installer([(s, explicit_args)]).install()
    assert spack.store.STORE.db.get_record(pkg).explicit == is_explicit


@pytest.mark.parametrize("run_tests", [True, False])
def test_print_install_test_log_skipped(install_mockery, mock_packages, capfd, run_tests):
    """Confirm printing of install log skipped if not run/no failures."""
    name = "trivial-install-test-package"
    s = spack.spec.Spec(name).concretized()
    pkg = s.package

    pkg.run_tests = run_tests
    spack.installer.print_install_test_log(pkg)
    out = capfd.readouterr()[0]
    assert out == ""


def test_print_install_test_log_failures(
    tmpdir, install_mockery, mock_packages, ensure_debug, capfd
):
    """Confirm expected outputs when there are test failures."""
    name = "trivial-install-test-package"
    s = spack.spec.Spec(name).concretized()
    pkg = s.package

    # Missing test log is an error
    pkg.run_tests = True
    pkg.tester.test_log_file = str(tmpdir.join("test-log.txt"))
    pkg.tester.add_failure(AssertionError("test"), "test-failure")
    spack.installer.print_install_test_log(pkg)
    err = capfd.readouterr()[1]
    assert "no test log file" in err

    # Having test log results in path being output
    fs.touch(pkg.tester.test_log_file)
    spack.installer.print_install_test_log(pkg)
    out = capfd.readouterr()[0]
    assert "See test results at" in out

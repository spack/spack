# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest
import shutil

from llnl.util.filesystem import mkdirp, touch, working_dir

from spack.package import InstallError, PackageBase, PackageStillNeededError
import spack.patch
import spack.repo
import spack.store
from spack.spec import Spec
from spack.package import _spack_build_envfile, _spack_build_logfile


def test_install_and_uninstall(install_mockery, mock_fetch, monkeypatch):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Get the package
    pkg = spec.package

    def find_nothing(*args):
        raise spack.repo.UnknownPackageError(
            'Repo package access is disabled for test')

    try:
        pkg.do_install()

        spec._package = None
        monkeypatch.setattr(spack.repo, 'get', find_nothing)
        with pytest.raises(spack.repo.UnknownPackageError):
            spec.package

        pkg.do_uninstall()
    except Exception:
        pkg.remove_prefix()
        raise


def mock_remove_prefix(*args):
    raise MockInstallError(
        "Intentional error",
        "Mock remove_prefix method intentionally fails")


class RemovePrefixChecker(object):
    def __init__(self, wrapped_rm_prefix):
        self.removed = False
        self.wrapped_rm_prefix = wrapped_rm_prefix

    def remove_prefix(self):
        self.removed = True
        self.wrapped_rm_prefix()


class MockStage(object):
    def __init__(self, wrapped_stage):
        self.wrapped_stage = wrapped_stage
        self.test_destroyed = False

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.destroy()

    def destroy(self):
        self.test_destroyed = True
        self.wrapped_stage.destroy()

    def create(self):
        self.wrapped_stage.create()

    def __getattr__(self, attr):
        return getattr(self.wrapped_stage, attr)


def test_partial_install_delete_prefix_and_stage(install_mockery, mock_fetch):
    spec = Spec('canfail').concretized()
    pkg = spack.repo.get(spec)
    remove_prefix = spack.package.Package.remove_prefix
    instance_rm_prefix = pkg.remove_prefix

    try:
        pkg.succeed = False
        spack.package.Package.remove_prefix = mock_remove_prefix
        with pytest.raises(MockInstallError):
            pkg.do_install()
        assert os.path.isdir(pkg.prefix)
        rm_prefix_checker = RemovePrefixChecker(instance_rm_prefix)
        spack.package.Package.remove_prefix = rm_prefix_checker.remove_prefix

        pkg.succeed = True
        pkg.stage = MockStage(pkg.stage)

        pkg.do_install(restage=True)
        assert rm_prefix_checker.removed
        assert pkg.stage.test_destroyed
        assert pkg.installed

    finally:
        spack.package.Package.remove_prefix = remove_prefix


def test_dont_add_patches_to_installed_package(install_mockery, mock_fetch):
    dependency = Spec('dependency-install')
    dependency.concretize()
    dependency.package.do_install()

    dependency_hash = dependency.dag_hash()
    dependent = Spec('dependent-install ^/' + dependency_hash)
    dependent.concretize()

    dependency.package.patches['dependency-install'] = [
        spack.patch.UrlPatch(
            dependent.package, 'file://fake.patch', sha256='unused-hash')]

    assert dependent['dependency-install'] == dependency


def test_installed_dependency_request_conflicts(
        install_mockery, mock_fetch, mutable_mock_packages):
    dependency = Spec('dependency-install')
    dependency.concretize()
    dependency.package.do_install()

    dependency_hash = dependency.dag_hash()
    dependent = Spec(
        'conflicting-dependent ^/' + dependency_hash)
    with pytest.raises(spack.spec.UnsatisfiableSpecError):
        dependent.concretize()


def test_installed_upstream_external(
        tmpdir_factory, install_mockery, mock_fetch, gen_mock_layout):
    """Check that when a dependency package is recorded as installed in
       an upstream database that it is not reinstalled.
    """
    mock_db_root = str(tmpdir_factory.mktemp('mock_db_root'))
    prepared_db = spack.database.Database(mock_db_root)

    upstream_layout = gen_mock_layout('/a/')

    dependency = spack.spec.Spec('externaltool')
    dependency.concretize()
    prepared_db.add(dependency, upstream_layout)

    try:
        original_db = spack.store.db
        downstream_db_root = str(
            tmpdir_factory.mktemp('mock_downstream_db_root'))
        spack.store.db = spack.database.Database(
            downstream_db_root, upstream_dbs=[prepared_db])
        dependent = spack.spec.Spec('externaltest')
        dependent.concretize()

        new_dependency = dependent['externaltool']
        assert new_dependency.external
        assert new_dependency.prefix == '/path/to/external_tool'

        dependent.package.do_install()

        assert not os.path.exists(new_dependency.prefix)
        assert os.path.exists(dependent.prefix)
    finally:
        spack.store.db = original_db


def test_installed_upstream(tmpdir_factory, install_mockery, mock_fetch,
                            gen_mock_layout):
    """Check that when a dependency package is recorded as installed in
       an upstream database that it is not reinstalled.
    """
    mock_db_root = str(tmpdir_factory.mktemp('mock_db_root'))
    prepared_db = spack.database.Database(mock_db_root)

    upstream_layout = gen_mock_layout('/a/')

    dependency = spack.spec.Spec('dependency-install')
    dependency.concretize()
    prepared_db.add(dependency, upstream_layout)

    try:
        original_db = spack.store.db
        downstream_db_root = str(
            tmpdir_factory.mktemp('mock_downstream_db_root'))
        spack.store.db = spack.database.Database(
            downstream_db_root, upstream_dbs=[prepared_db])
        dependent = spack.spec.Spec('dependent-install')
        dependent.concretize()

        new_dependency = dependent['dependency-install']
        assert new_dependency.package.installed_upstream
        assert (new_dependency.prefix ==
                upstream_layout.path_for_spec(dependency))

        dependent.package.do_install()

        assert not os.path.exists(new_dependency.prefix)
        assert os.path.exists(dependent.prefix)
    finally:
        spack.store.db = original_db


@pytest.mark.disable_clean_stage_check
def test_partial_install_keep_prefix(install_mockery, mock_fetch):
    spec = Spec('canfail').concretized()
    pkg = spack.repo.get(spec)

    # Normally the stage should start unset, but other tests set it
    pkg._stage = None
    remove_prefix = spack.package.Package.remove_prefix
    try:
        # If remove_prefix is called at any point in this test, that is an
        # error
        pkg.succeed = False  # make the build fail
        spack.package.Package.remove_prefix = mock_remove_prefix
        with pytest.raises(spack.build_environment.ChildError):
            pkg.do_install(keep_prefix=True)
        assert os.path.exists(pkg.prefix)

        pkg.succeed = True   # make the build succeed
        pkg.stage = MockStage(pkg.stage)
        pkg.do_install(keep_prefix=True)
        assert pkg.installed
        assert not pkg.stage.test_destroyed

    finally:
        spack.package.Package.remove_prefix = remove_prefix


def test_second_install_no_overwrite_first(install_mockery, mock_fetch):
    spec = Spec('canfail').concretized()
    pkg = spack.repo.get(spec)
    remove_prefix = spack.package.Package.remove_prefix
    try:
        spack.package.Package.remove_prefix = mock_remove_prefix

        pkg.succeed = True
        pkg.do_install()
        assert pkg.installed

        # If Package.install is called after this point, it will fail
        pkg.succeed = False
        pkg.do_install()

    finally:
        spack.package.Package.remove_prefix = remove_prefix


def test_store(install_mockery, mock_fetch):
    spec = Spec('cmake-client').concretized()
    pkg = spec.package
    pkg.do_install()


@pytest.mark.disable_clean_stage_check
def test_failing_build(install_mockery, mock_fetch):
    spec = Spec('failing-build').concretized()
    pkg = spec.package

    with pytest.raises(spack.build_environment.ChildError):
        pkg.do_install()


class MockInstallError(spack.error.SpackError):
    pass


def test_uninstall_by_spec_errors(mutable_database):
    """Test exceptional cases with the uninstall command."""

    # Try to uninstall a spec that has not been installed
    rec = mutable_database.get_record('zmpi')
    with pytest.raises(InstallError, matches="not installed"):
        PackageBase.uninstall_by_spec(rec.spec)

    # Try an unforced uninstall of a spec with dependencies
    rec = mutable_database.get_record('mpich')

    with pytest.raises(PackageStillNeededError, matches="cannot uninstall"):
        PackageBase.uninstall_by_spec(rec.spec)


def test_pkg_build_paths(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package').concretized()

    log_path = spec.package.log_path
    assert log_path.endswith(_spack_build_logfile)

    env_path = spec.package.env_path
    assert env_path.endswith(_spack_build_envfile)

    # Backward compatibility checks
    log_dir = os.path.dirname(log_path)
    mkdirp(log_dir)
    with working_dir(log_dir):
        # Start with the older of the previous log filenames
        older_log = 'spack-build.out'
        touch(older_log)
        assert spec.package.log_path.endswith(older_log)

        # Now check the newer log filename
        last_log = 'spack-build.txt'
        os.rename(older_log, last_log)
        assert spec.package.log_path.endswith(last_log)

        # Check the old environment file
        last_env = 'spack-build.env'
        os.rename(last_log, last_env)
        assert spec.package.env_path.endswith(last_env)

    # Cleanup
    shutil.rmtree(log_dir)


def test_pkg_install_paths(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package').concretized()

    log_path = os.path.join(spec.prefix, '.spack', _spack_build_logfile)
    assert spec.package.install_log_path == log_path

    env_path = os.path.join(spec.prefix, '.spack', _spack_build_envfile)
    assert spec.package.install_env_path == env_path

    # Backward compatibility checks
    log_dir = os.path.dirname(log_path)
    mkdirp(log_dir)
    with working_dir(log_dir):
        # Start with the older of the previous install log filenames
        older_log = 'build.out'
        touch(older_log)
        assert spec.package.install_log_path.endswith(older_log)

        # Now check the newer install log filename
        last_log = 'build.txt'
        os.rename(older_log, last_log)
        assert spec.package.install_log_path.endswith(last_log)

        # Check the old install environment file
        last_env = 'build.env'
        os.rename(last_log, last_env)
        assert spec.package.install_env_path.endswith(last_env)

    # Cleanup
    shutil.rmtree(log_dir)


def test_pkg_install_log(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package').concretized()

    # Attempt installing log without the build log file
    with pytest.raises(IOError, match="No such file or directory"):
        spec.package.log()

    # Set up mock build files and try again
    log_path = spec.package.log_path
    log_dir = os.path.dirname(log_path)
    mkdirp(log_dir)
    with working_dir(log_dir):
        touch(log_path)
        touch(spec.package.env_path)

    install_path = os.path.dirname(spec.package.install_log_path)
    mkdirp(install_path)

    spec.package.log()

    assert os.path.exists(spec.package.install_log_path)
    assert os.path.exists(spec.package.install_env_path)

    # Cleanup
    shutil.rmtree(log_dir)


def test_unconcretized_install(install_mockery, mock_fetch, mock_packages):
    """Test attempts to perform install phases with unconcretized spec."""
    spec = Spec('trivial-install-test-package')

    with pytest.raises(ValueError, match="only install concrete packages"):
        spec.package.do_install()

    with pytest.raises(ValueError, match="fetch concrete packages"):
        spec.package.do_fetch()

    with pytest.raises(ValueError, match="stage concrete packages"):
        spec.package.do_stage()

    with pytest.raises(ValueError, match="patch concrete packages"):
        spec.package.do_patch()

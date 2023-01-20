# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

import pytest

import llnl.util.filesystem as fs

import spack.error
import spack.patch
import spack.repo
import spack.store
import spack.util.spack_json as sjson
from spack.package_base import (
    InstallError,
    PackageBase,
    PackageStillNeededError,
    _spack_build_envfile,
    _spack_build_logfile,
    _spack_configure_argsfile,
)
from spack.spec import Spec


def find_nothing(*args):
    raise spack.repo.UnknownPackageError("Repo package access is disabled for test")


def test_install_and_uninstall(install_mockery, mock_fetch, monkeypatch):
    spec = Spec("trivial-install-test-package").concretized()

    spec.package.do_install()
    assert spec.installed

    spec.package.do_uninstall()
    assert not spec.installed


@pytest.mark.regression("11870")
def test_uninstall_non_existing_package(install_mockery, mock_fetch, monkeypatch):
    """Ensure that we can uninstall a package that has been deleted from the repo"""
    spec = Spec("trivial-install-test-package").concretized()

    spec.package.do_install()
    assert spec.installed

    # Mock deletion of the package
    spec._package = None
    monkeypatch.setattr(spack.repo.path, "get", find_nothing)
    with pytest.raises(spack.repo.UnknownPackageError):
        spec.package

    # Ensure we can uninstall it
    PackageBase.uninstall_by_spec(spec)
    assert not spec.installed


def test_pkg_attributes(install_mockery, mock_fetch, monkeypatch):
    # Get a basic concrete spec for the dummy package.
    spec = Spec("attributes-foo-app ^attributes-foo")
    spec.concretize()
    assert spec.concrete

    pkg = spec.package
    pkg.do_install()
    foo = "attributes-foo"
    assert spec["bar"].prefix == spec[foo].prefix
    assert spec["baz"].prefix == spec[foo].prefix

    assert spec[foo].home == spec[foo].prefix
    assert spec["bar"].home == spec[foo].home
    assert spec["baz"].home == spec[foo].prefix.baz

    foo_headers = spec[foo].headers
    # assert foo_headers.basenames == ['foo.h']
    assert foo_headers.directories == [spec[foo].home.include]
    bar_headers = spec["bar"].headers
    # assert bar_headers.basenames == ['bar.h']
    assert bar_headers.directories == [spec["bar"].home.include]
    baz_headers = spec["baz"].headers
    # assert baz_headers.basenames == ['baz.h']
    assert baz_headers.directories == [spec["baz"].home.include]

    lib_suffix = ".so"
    if sys.platform == "win32":
        lib_suffix = ".dll"
    elif sys.platform == "darwin":
        lib_suffix = ".dylib"

    foo_libs = spec[foo].libs
    assert foo_libs.basenames == ["libFoo" + lib_suffix]
    assert foo_libs.directories == [spec[foo].home.lib64]
    bar_libs = spec["bar"].libs
    assert bar_libs.basenames == ["libFooBar" + lib_suffix]
    assert bar_libs.directories == [spec["bar"].home.lib64]
    baz_libs = spec["baz"].libs
    assert baz_libs.basenames == ["libFooBaz" + lib_suffix]
    assert baz_libs.directories == [spec["baz"].home.lib]


def mock_remove_prefix(*args):
    raise MockInstallError("Intentional error", "Mock remove_prefix method intentionally fails")


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
        if attr == "wrapped_stage":
            # This attribute may not be defined at some point during unpickling
            raise AttributeError()
        return getattr(self.wrapped_stage, attr)


def test_partial_install_delete_prefix_and_stage(install_mockery, mock_fetch, working_env):
    s = Spec("canfail").concretized()

    instance_rm_prefix = s.package.remove_prefix

    try:
        s.package.remove_prefix = mock_remove_prefix
        with pytest.raises(MockInstallError):
            s.package.do_install()
        assert os.path.isdir(s.package.prefix)
        rm_prefix_checker = RemovePrefixChecker(instance_rm_prefix)
        s.package.remove_prefix = rm_prefix_checker.remove_prefix

        # must clear failure markings for the package before re-installing it
        spack.store.db.clear_failure(s, True)

        s.package.set_install_succeed()
        s.package.stage = MockStage(s.package.stage)

        s.package.do_install(restage=True)
        assert rm_prefix_checker.removed
        assert s.package.stage.test_destroyed
        assert s.package.spec.installed

    finally:
        s.package.remove_prefix = instance_rm_prefix


@pytest.mark.disable_clean_stage_check
def test_failing_overwrite_install_should_keep_previous_installation(
    mock_fetch, install_mockery, working_env
):
    """
    Make sure that whenever `spack install --overwrite` fails, spack restores
    the original install prefix instead of cleaning it.
    """
    # Do a successful install
    s = Spec("canfail").concretized()
    s.package.set_install_succeed()

    # Do a failing overwrite install
    s.package.do_install()
    s.package.set_install_fail()
    kwargs = {"overwrite": [s.dag_hash()]}

    with pytest.raises(Exception):
        s.package.do_install(**kwargs)

    assert s.package.spec.installed
    assert os.path.exists(s.prefix)


def test_dont_add_patches_to_installed_package(install_mockery, mock_fetch, monkeypatch):
    dependency = Spec("dependency-install")
    dependency.concretize()
    dependency.package.do_install()

    dependency_hash = dependency.dag_hash()
    dependent = Spec("dependent-install ^/" + dependency_hash)
    dependent.concretize()

    monkeypatch.setitem(
        dependency.package.patches,
        "dependency-install",
        [spack.patch.UrlPatch(dependent.package, "file://fake.patch", sha256="unused-hash")],
    )

    assert dependent["dependency-install"] == dependency


def test_installed_dependency_request_conflicts(install_mockery, mock_fetch, mutable_mock_repo):
    dependency = Spec("dependency-install")
    dependency.concretize()
    dependency.package.do_install()

    dependency_hash = dependency.dag_hash()
    dependent = Spec("conflicting-dependent ^/" + dependency_hash)
    with pytest.raises(spack.error.UnsatisfiableSpecError):
        dependent.concretize()


def test_install_dependency_symlinks_pkg(install_mockery, mock_fetch, mutable_mock_repo):
    """Test dependency flattening/symlinks mock package."""
    spec = Spec("flatten-deps")
    spec.concretize()
    pkg = spec.package
    pkg.do_install()

    # Ensure dependency directory exists after the installation.
    dependency_dir = os.path.join(pkg.prefix, "dependency-install")
    assert os.path.isdir(dependency_dir)


def test_install_times(install_mockery, mock_fetch, mutable_mock_repo):
    """Test install times added."""
    spec = Spec("dev-build-test-install-phases").concretized()
    spec.package.do_install()

    # Ensure dependency directory exists after the installation.
    install_times = os.path.join(spec.package.prefix, ".spack", "install_times.json")
    assert os.path.isfile(install_times)

    # Ensure the phases are included
    with open(install_times, "r") as timefile:
        times = sjson.load(timefile.read())

    # The order should be maintained
    phases = [x["name"] for x in times["phases"]]
    assert phases == ["stage", "one", "two", "three", "install"]
    assert all(isinstance(x["seconds"], float) for x in times["phases"])


def test_flatten_deps(install_mockery, mock_fetch, mutable_mock_repo):
    """Explicitly test the flattening code for coverage purposes."""
    # Unfortunately, executing the 'flatten-deps' spec's installation does
    # not affect code coverage results, so be explicit here.
    spec = Spec("dependent-install")
    spec.concretize()
    pkg = spec.package
    pkg.do_install()

    # Demonstrate that the directory does not appear under the spec
    # prior to the flatten operation.
    dependency_name = "dependency-install"
    assert dependency_name not in os.listdir(pkg.prefix)

    # Flatten the dependencies and ensure the dependency directory is there.
    spack.package_base.flatten_dependencies(spec, pkg.prefix)

    dependency_dir = os.path.join(pkg.prefix, dependency_name)
    assert os.path.isdir(dependency_dir)


@pytest.fixture()
def install_upstream(tmpdir_factory, gen_mock_layout, install_mockery):
    """Provides a function that installs a specified set of specs to an
    upstream database. The function returns a store which points to the
    upstream, as well as the upstream layout (for verifying that dependent
    installs are using the upstream installs).
    """
    mock_db_root = str(tmpdir_factory.mktemp("mock_db_root"))
    prepared_db = spack.database.Database(mock_db_root)
    upstream_layout = gen_mock_layout("/a/")

    def _install_upstream(*specs):
        for spec_str in specs:
            s = spack.spec.Spec(spec_str).concretized()
            prepared_db.add(s, upstream_layout)

        downstream_root = str(tmpdir_factory.mktemp("mock_downstream_db_root"))
        db_for_test = spack.database.Database(downstream_root, upstream_dbs=[prepared_db])
        store = spack.store.Store(downstream_root)
        store.db = db_for_test
        return store, upstream_layout

    return _install_upstream


def test_installed_upstream_external(install_upstream, mock_fetch):
    """Check that when a dependency package is recorded as installed in
    an upstream database that it is not reinstalled.
    """
    s, _ = install_upstream("externaltool")
    with spack.store.use_store(s):
        dependent = spack.spec.Spec("externaltest")
        dependent.concretize()

        new_dependency = dependent["externaltool"]
        assert new_dependency.external
        assert new_dependency.prefix == os.path.sep + os.path.join("path", "to", "external_tool")

        dependent.package.do_install()

        assert not os.path.exists(new_dependency.prefix)
        assert os.path.exists(dependent.prefix)


def test_installed_upstream(install_upstream, mock_fetch):
    """Check that when a dependency package is recorded as installed in
    an upstream database that it is not reinstalled.
    """
    s, upstream_layout = install_upstream("dependency-install")
    with spack.store.use_store(s):
        dependency = spack.spec.Spec("dependency-install").concretized()
        dependent = spack.spec.Spec("dependent-install").concretized()

        new_dependency = dependent["dependency-install"]
        assert new_dependency.installed_upstream
        assert new_dependency.prefix == upstream_layout.path_for_spec(dependency)

        dependent.package.do_install()

        assert not os.path.exists(new_dependency.prefix)
        assert os.path.exists(dependent.prefix)


@pytest.mark.disable_clean_stage_check
def test_partial_install_keep_prefix(install_mockery, mock_fetch, monkeypatch, working_env):
    s = Spec("canfail").concretized()

    # If remove_prefix is called at any point in this test, that is an error
    monkeypatch.setattr(spack.package_base.PackageBase, "remove_prefix", mock_remove_prefix)
    with pytest.raises(spack.build_environment.ChildError):
        s.package.do_install(keep_prefix=True)
    assert os.path.exists(s.package.prefix)

    # must clear failure markings for the package before re-installing it
    spack.store.db.clear_failure(s, True)

    s.package.set_install_succeed()
    s.package.stage = MockStage(s.package.stage)
    s.package.do_install(keep_prefix=True)
    assert s.package.spec.installed
    assert not s.package.stage.test_destroyed


def test_second_install_no_overwrite_first(install_mockery, mock_fetch, monkeypatch):
    s = Spec("canfail").concretized()
    monkeypatch.setattr(spack.package_base.PackageBase, "remove_prefix", mock_remove_prefix)

    s.package.set_install_succeed()
    s.package.do_install()
    assert s.package.spec.installed

    # If Package.install is called after this point, it will fail
    s.package.set_install_fail()
    s.package.do_install()


def test_install_prefix_collision_fails(config, mock_fetch, mock_packages, tmpdir):
    """
    Test that different specs with coinciding install prefixes will fail
    to install.
    """
    projections = {"all": "all-specs-project-to-this-prefix"}
    store = spack.store.Store(str(tmpdir), projections=projections)
    with spack.store.use_store(store):
        with spack.config.override("config:checksum", False):
            pkg_a = Spec("libelf@0.8.13").concretized().package
            pkg_b = Spec("libelf@0.8.12").concretized().package
            pkg_a.do_install()

            with pytest.raises(InstallError, match="Install prefix collision"):
                pkg_b.do_install()


def test_store(install_mockery, mock_fetch):
    spec = Spec("cmake-client").concretized()
    pkg = spec.package
    pkg.do_install()


@pytest.mark.disable_clean_stage_check
def test_failing_build(install_mockery, mock_fetch, capfd):
    spec = Spec("failing-build").concretized()
    pkg = spec.package

    with pytest.raises(spack.build_environment.ChildError, match="Expected failure"):
        pkg.do_install()


class MockInstallError(spack.error.SpackError):
    pass


def test_uninstall_by_spec_errors(mutable_database):
    """Test exceptional cases with the uninstall command."""

    # Try to uninstall a spec that has not been installed
    spec = Spec("dependent-install")
    spec.concretize()
    with pytest.raises(InstallError, match="is not installed"):
        PackageBase.uninstall_by_spec(spec)

    # Try an unforced uninstall of a spec with dependencies
    rec = mutable_database.get_record("mpich")
    with pytest.raises(PackageStillNeededError, match="Cannot uninstall"):
        PackageBase.uninstall_by_spec(rec.spec)


@pytest.mark.disable_clean_stage_check
def test_nosource_pkg_install(install_mockery, mock_fetch, mock_packages, capfd, ensure_debug):
    """Test install phases with the nosource package."""
    spec = Spec("nosource").concretized()
    pkg = spec.package

    # Make sure install works even though there is no associated code.
    pkg.do_install()
    out = capfd.readouterr()
    assert "Installing dependency-install" in out[0]

    # Make sure a warning for missing code is issued
    assert "Missing a source id for nosource" in out[1]


@pytest.mark.disable_clean_stage_check
def test_nosource_bundle_pkg_install(
    install_mockery, mock_fetch, mock_packages, capfd, ensure_debug
):
    """Test install phases with the nosource-bundle package."""
    spec = Spec("nosource-bundle").concretized()
    pkg = spec.package

    # Make sure install works even though there is no associated code.
    pkg.do_install()
    out = capfd.readouterr()
    assert "Installing dependency-install" in out[0]

    # Make sure a warning for missing code is *not* issued
    assert "Missing a source id for nosource" not in out[1]


def test_nosource_pkg_install_post_install(install_mockery, mock_fetch, mock_packages):
    """Test install phases with the nosource package with post-install."""
    spec = Spec("nosource-install").concretized()
    pkg = spec.package

    # Make sure both the install and post-install package methods work.
    pkg.do_install()

    # Ensure the file created in the package's `install` method exists.
    install_txt = os.path.join(spec.prefix, "install.txt")
    assert os.path.isfile(install_txt)

    # Ensure the file created in the package's `post-install` method exists.
    post_install_txt = os.path.join(spec.prefix, "post-install.txt")
    assert os.path.isfile(post_install_txt)


def test_pkg_build_paths(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec("trivial-install-test-package").concretized()

    log_path = spec.package.log_path
    assert log_path.endswith(_spack_build_logfile)

    env_path = spec.package.env_path
    assert env_path.endswith(_spack_build_envfile)

    # Backward compatibility checks
    log_dir = os.path.dirname(log_path)
    fs.mkdirp(log_dir)
    with fs.working_dir(log_dir):
        # Start with the older of the previous log filenames
        older_log = "spack-build.out"
        fs.touch(older_log)
        assert spec.package.log_path.endswith(older_log)

        # Now check the newer log filename
        last_log = "spack-build.txt"
        fs.rename(older_log, last_log)
        assert spec.package.log_path.endswith(last_log)

        # Check the old environment file
        last_env = "spack-build.env"
        fs.rename(last_log, last_env)
        assert spec.package.env_path.endswith(last_env)

    # Cleanup
    shutil.rmtree(log_dir)


def test_pkg_install_paths(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec("trivial-install-test-package").concretized()

    log_path = os.path.join(spec.prefix, ".spack", _spack_build_logfile)
    assert spec.package.install_log_path == log_path

    env_path = os.path.join(spec.prefix, ".spack", _spack_build_envfile)
    assert spec.package.install_env_path == env_path

    args_path = os.path.join(spec.prefix, ".spack", _spack_configure_argsfile)
    assert spec.package.install_configure_args_path == args_path

    # Backward compatibility checks
    log_dir = os.path.dirname(log_path)
    fs.mkdirp(log_dir)
    with fs.working_dir(log_dir):
        # Start with the older of the previous install log filenames
        older_log = "build.out"
        fs.touch(older_log)
        assert spec.package.install_log_path.endswith(older_log)

        # Now check the newer install log filename
        last_log = "build.txt"
        fs.rename(older_log, last_log)
        assert spec.package.install_log_path.endswith(last_log)

        # Check the old install environment file
        last_env = "build.env"
        fs.rename(last_log, last_env)
        assert spec.package.install_env_path.endswith(last_env)

    # Cleanup
    shutil.rmtree(log_dir)


def test_log_install_without_build_files(install_mockery):
    """Test the installer log function when no build files are present."""
    # Get a basic concrete spec for the trivial install package.
    spec = Spec("trivial-install-test-package").concretized()

    # Attempt installing log without the build log file
    with pytest.raises(IOError, match="No such file or directory"):
        spack.installer.log(spec.package)


def test_log_install_with_build_files(install_mockery, monkeypatch):
    """Test the installer's log function when have build files."""
    config_log = "config.log"

    # Retain the original function for use in the monkey patch that is used
    # to raise an exception under the desired condition for test coverage.
    orig_install_fn = fs.install

    def _install(src, dest):
        orig_install_fn(src, dest)
        if src.endswith(config_log):
            raise Exception("Mock log install error")

    monkeypatch.setattr(fs, "install", _install)

    spec = Spec("trivial-install-test-package").concretized()

    # Set up mock build files and try again to include archive failure
    log_path = spec.package.log_path
    log_dir = os.path.dirname(log_path)
    fs.mkdirp(log_dir)
    with fs.working_dir(log_dir):
        fs.touch(log_path)
        fs.touch(spec.package.env_path)
        fs.touch(spec.package.env_mods_path)
        fs.touch(spec.package.configure_args_path)

    install_path = os.path.dirname(spec.package.install_log_path)
    fs.mkdirp(install_path)

    source = spec.package.stage.source_path
    config = os.path.join(source, "config.log")
    fs.touchp(config)
    monkeypatch.setattr(
        type(spec.package), "archive_files", ["missing", "..", config], raising=False
    )

    spack.installer.log(spec.package)

    assert os.path.exists(spec.package.install_log_path)
    assert os.path.exists(spec.package.install_env_path)
    assert os.path.exists(spec.package.install_configure_args_path)

    archive_dir = os.path.join(install_path, "archived-files")
    source_dir = os.path.dirname(source)
    rel_config = os.path.relpath(config, source_dir)

    assert os.path.exists(os.path.join(archive_dir, rel_config))
    assert not os.path.exists(os.path.join(archive_dir, "missing"))

    expected_errs = ["OUTSIDE SOURCE PATH", "FAILED TO ARCHIVE"]  # for '..'  # for rel_config
    with open(os.path.join(archive_dir, "errors.txt"), "r") as fd:
        for ln, expected in zip(fd, expected_errs):
            assert expected in ln

    # Cleanup
    shutil.rmtree(log_dir)


def test_unconcretized_install(install_mockery, mock_fetch, mock_packages):
    """Test attempts to perform install phases with unconcretized spec."""
    spec = Spec("trivial-install-test-package")
    pkg_cls = spack.repo.path.get_pkg_class(spec.name)

    with pytest.raises(ValueError, match="must have a concrete spec"):
        pkg_cls(spec).do_install()

    with pytest.raises(ValueError, match="only patch concrete packages"):
        pkg_cls(spec).do_patch()


def test_install_error():
    try:
        msg = "test install error"
        long_msg = "this is the long version of test install error"
        raise InstallError(msg, long_msg=long_msg)
    except Exception as exc:
        assert exc.__class__.__name__ == "InstallError"
        assert exc.message == msg
        assert exc.long_message == long_msg


@pytest.mark.disable_clean_stage_check
def test_empty_install_sanity_check_prefix(
    monkeypatch, install_mockery, mock_fetch, mock_packages
):
    """Test empty install triggers sanity_check_prefix."""
    spec = Spec("failing-empty-install").concretized()
    with pytest.raises(spack.build_environment.ChildError, match="Nothing was installed"):
        spec.package.do_install()

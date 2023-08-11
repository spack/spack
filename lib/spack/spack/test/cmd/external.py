# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import sys

import pytest

from llnl.util.filesystem import getuid, touch

import spack
import spack.detection
import spack.detection.path
from spack.main import SpackCommand
from spack.spec import Spec


@pytest.fixture
def executables_found(monkeypatch):
    def _factory(result):
        def _mock_search(path_hints=None):
            return result

        monkeypatch.setattr(spack.detection.path, "executables_in_path", _mock_search)

    return _factory


@pytest.fixture
def _platform_executables(monkeypatch):
    def _win_exe_ext():
        return ".bat"

    monkeypatch.setattr(spack.util.path, "win_exe_ext", _win_exe_ext)


def define_plat_exe(exe):
    if sys.platform == "win32":
        exe += ".bat"
    return exe


def test_find_external_single_package(mock_executable, executables_found, _platform_executables):
    pkgs_to_check = [spack.repo.PATH.get_pkg_class("cmake")]
    cmake_path = mock_executable("cmake", output="echo cmake version 1.foo")
    executables_found({str(cmake_path): define_plat_exe("cmake")})

    pkg_to_entries = spack.detection.by_executable(pkgs_to_check)

    pkg, entries = next(iter(pkg_to_entries.items()))
    single_entry = next(iter(entries))

    assert single_entry.spec == Spec("cmake@1.foo")


def test_find_external_two_instances_same_package(
    mock_executable, executables_found, _platform_executables
):
    pkgs_to_check = [spack.repo.PATH.get_pkg_class("cmake")]

    # Each of these cmake instances is created in a different prefix
    # In Windows, quoted strings are echo'd with quotes includes
    # we need to avoid that for proper regex.
    cmake_path1 = mock_executable(
        "cmake", output="echo cmake version 1.foo", subdir=("base1", "bin")
    )
    cmake_path2 = mock_executable(
        "cmake", output="echo cmake version 3.17.2", subdir=("base2", "bin")
    )
    cmake_exe = define_plat_exe("cmake")
    executables_found({str(cmake_path1): cmake_exe, str(cmake_path2): cmake_exe})

    pkg_to_entries = spack.detection.by_executable(pkgs_to_check)

    pkg, entries = next(iter(pkg_to_entries.items()))
    spec_to_path = dict((e.spec, e.prefix) for e in entries)
    assert spec_to_path[Spec("cmake@1.foo")] == (
        spack.detection.executable_prefix(os.path.dirname(cmake_path1))
    )
    assert spec_to_path[Spec("cmake@3.17.2")] == (
        spack.detection.executable_prefix(os.path.dirname(cmake_path2))
    )


def test_find_external_update_config(mutable_config):
    entries = [
        spack.detection.DetectedPackage(Spec.from_detection("cmake@1.foo"), "/x/y1/"),
        spack.detection.DetectedPackage(Spec.from_detection("cmake@3.17.2"), "/x/y2/"),
    ]
    pkg_to_entries = {"cmake": entries}

    scope = spack.config.default_modify_scope("packages")
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get("packages")
    cmake_cfg = pkgs_cfg["cmake"]
    cmake_externals = cmake_cfg["externals"]

    assert {"spec": "cmake@1.foo", "prefix": "/x/y1/"} in cmake_externals
    assert {"spec": "cmake@3.17.2", "prefix": "/x/y2/"} in cmake_externals


def test_get_executables(working_env, mock_executable):
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    path_to_exe = spack.detection.executables_in_path([os.path.dirname(cmake_path1)])
    cmake_exe = define_plat_exe("cmake")
    assert path_to_exe[str(cmake_path1)] == cmake_exe


external = SpackCommand("external")


def test_find_external_cmd(mutable_config, working_env, mock_executable, _platform_executables):
    """Test invoking 'spack external find' with additional package arguments,
    which restricts the set of packages that Spack looks for.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    prefix = os.path.dirname(os.path.dirname(cmake_path1))

    os.environ["PATH"] = os.pathsep.join([os.path.dirname(cmake_path1)])
    external("find", "cmake")

    pkgs_cfg = spack.config.get("packages")
    cmake_cfg = pkgs_cfg["cmake"]
    cmake_externals = cmake_cfg["externals"]

    assert {"spec": "cmake@1.foo", "prefix": prefix} in cmake_externals


def test_find_external_cmd_not_buildable(mutable_config, working_env, mock_executable):
    """When the user invokes 'spack external find --not-buildable', the config
    for any package where Spack finds an external version should be marked as
    not buildable.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(cmake_path1)])
    external("find", "--not-buildable", "cmake")
    pkgs_cfg = spack.config.get("packages")
    assert not pkgs_cfg["cmake"]["buildable"]


def test_find_external_cmd_full_repo(
    mutable_config, working_env, mock_executable, mutable_mock_repo, _platform_executables
):
    """Test invoking 'spack external find' with no additional arguments, which
    iterates through each package in the repository.
    """
    exe_path1 = mock_executable("find-externals1-exe", output="echo find-externals1 version 1.foo")
    prefix = os.path.dirname(os.path.dirname(exe_path1))
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(exe_path1)])
    external("find", "--all")

    pkgs_cfg = spack.config.get("packages")
    pkg_cfg = pkgs_cfg["find-externals1"]
    pkg_externals = pkg_cfg["externals"]

    assert {"spec": "find-externals1@1.foo", "prefix": prefix} in pkg_externals


def test_find_external_cmd_exclude(
    mutable_config, working_env, mock_executable, mutable_mock_repo, _platform_executables
):
    """Test invoking 'spack external find --all --exclude', to ensure arbitary
    external packages can be ignored.
    """
    exe_path1 = mock_executable("find-externals1-exe", output="echo find-externals1 version 1.foo")
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(exe_path1)])
    external("find", "--all", "--exclude=find-externals1")

    pkgs_cfg = spack.config.get("packages")

    assert "find-externals1" not in pkgs_cfg.keys()


def test_find_external_no_manifest(
    mutable_config,
    working_env,
    mock_executable,
    mutable_mock_repo,
    _platform_executables,
    monkeypatch,
):
    """The user runs 'spack external find'; the default path for storing
    manifest files does not exist. Ensure that the command does not
    fail.
    """
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(
        spack.cray_manifest, "default_path", os.path.join("a", "path", "that", "doesnt", "exist")
    )
    external("find")


def test_find_external_empty_default_manifest_dir(
    mutable_config,
    working_env,
    mock_executable,
    mutable_mock_repo,
    _platform_executables,
    tmpdir,
    monkeypatch,
):
    """The user runs 'spack external find'; the default path for storing
    manifest files exists but is empty. Ensure that the command does not
    fail.
    """
    empty_manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", empty_manifest_dir)
    external("find")


@pytest.mark.skipif(sys.platform == "win32", reason="Can't chmod on Windows")
@pytest.mark.skipif(getuid() == 0, reason="user is root")
def test_find_external_manifest_with_bad_permissions(
    mutable_config,
    working_env,
    mock_executable,
    mutable_mock_repo,
    _platform_executables,
    tmpdir,
    monkeypatch,
):
    """The user runs 'spack external find'; the default path for storing
    manifest files exists but with insufficient permissions. Check that
    the command does not fail.
    """
    test_manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    test_manifest_file_path = os.path.join(test_manifest_dir, "badperms.json")
    touch(test_manifest_file_path)
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", test_manifest_dir)
    try:
        os.chmod(test_manifest_file_path, 0)
        output = external("find")
        assert "insufficient permissions" in output
        assert "Skipping manifest and continuing" in output
    finally:
        os.chmod(test_manifest_file_path, 0o700)


def test_find_external_manifest_failure(mutable_config, mutable_mock_repo, tmpdir, monkeypatch):
    """The user runs 'spack external find'; the manifest parsing fails with
    some exception. Ensure that the command still succeeds (i.e. moves on
    to other external detection mechanisms).
    """
    # First, create an empty manifest file (without a file to read, the
    # manifest parsing is skipped)
    test_manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    test_manifest_file_path = os.path.join(test_manifest_dir, "test.json")
    touch(test_manifest_file_path)

    def fail():
        raise Exception()

    monkeypatch.setattr(spack.cmd.external, "_collect_and_consume_cray_manifest_files", fail)
    monkeypatch.setenv("PATH", "")
    output = external("find")
    assert "Skipping manifest and continuing" in output


def test_find_external_nonempty_default_manifest_dir(
    mutable_database,
    mutable_mock_repo,
    _platform_executables,
    tmpdir,
    monkeypatch,
    directory_with_manifest,
):
    """The user runs 'spack external find'; the default manifest directory
    contains a manifest file. Ensure that the specs are read.
    """
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", str(directory_with_manifest))
    external("find")
    specs = spack.store.STORE.db.query("hwloc")
    assert any(x.dag_hash() == "hwlocfakehashaaa" for x in specs)


def test_find_external_merge(mutable_config, mutable_mock_repo):
    """Check that 'spack find external' doesn't overwrite an existing spec
    entry in packages.yaml.
    """
    pkgs_cfg_init = {
        "find-externals1": {
            "externals": [{"spec": "find-externals1@1.1", "prefix": "/preexisting-prefix/"}],
            "buildable": False,
        }
    }

    mutable_config.update_config("packages", pkgs_cfg_init)
    entries = [
        spack.detection.DetectedPackage(Spec.from_detection("find-externals1@1.1"), "/x/y1/"),
        spack.detection.DetectedPackage(Spec.from_detection("find-externals1@1.2"), "/x/y2/"),
    ]
    pkg_to_entries = {"find-externals1": entries}
    scope = spack.config.default_modify_scope("packages")
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get("packages")
    pkg_cfg = pkgs_cfg["find-externals1"]
    pkg_externals = pkg_cfg["externals"]

    assert {"spec": "find-externals1@1.1", "prefix": "/preexisting-prefix/"} in pkg_externals
    assert {"spec": "find-externals1@1.2", "prefix": "/x/y2/"} in pkg_externals


def test_list_detectable_packages(mutable_config, mutable_mock_repo):
    external("list")
    assert external.returncode == 0


def test_packages_yaml_format(mock_executable, mutable_config, monkeypatch, _platform_executables):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable("gcc", output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv("PATH", prefix)

    # Find the external spec
    external("find", "gcc")

    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get("packages")
    assert "gcc" in packages_yaml
    assert "externals" in packages_yaml["gcc"]
    externals = packages_yaml["gcc"]["externals"]
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc["spec"] == "gcc@4.2.1 languages=c"
    assert external_gcc["prefix"] == os.path.dirname(prefix)
    assert "extra_attributes" in external_gcc
    extra_attributes = external_gcc["extra_attributes"]
    assert "prefix" not in extra_attributes
    assert extra_attributes["compilers"]["c"] == str(gcc_exe)


def test_overriding_prefix(mock_executable, mutable_config, monkeypatch, _platform_executables):
    # Prepare an environment to detect a fake gcc that
    # override its external prefix
    gcc_exe = mock_executable("gcc", output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv("PATH", prefix)

    @classmethod
    def _determine_variants(cls, exes, version_str):
        return "languages=c", {"prefix": "/opt/gcc/bin", "compilers": {"c": exes[0]}}

    gcc_cls = spack.repo.PATH.get_pkg_class("gcc")
    monkeypatch.setattr(gcc_cls, "determine_variants", _determine_variants)

    # Find the external spec
    external("find", "gcc")

    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get("packages")
    assert "gcc" in packages_yaml
    assert "externals" in packages_yaml["gcc"]
    externals = packages_yaml["gcc"]["externals"]
    assert len(externals) == 1
    assert externals[0]["prefix"] == os.path.sep + os.path.join("opt", "gcc", "bin")


def test_new_entries_are_reported_correctly(
    mock_executable, mutable_config, monkeypatch, _platform_executables
):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable("gcc", output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv("PATH", prefix)

    # The first run will find and add the external gcc
    output = external("find", "gcc")
    assert "The following specs have been" in output

    # The second run should report that no new external
    # has been found
    output = external("find", "gcc")
    assert "No new external packages detected" in output


@pytest.mark.parametrize("command_args", [("-t", "build-tools"), ("-t", "build-tools", "cmake")])
def test_use_tags_for_detection(command_args, mock_executable, mutable_config, monkeypatch):
    # Prepare an environment to detect a fake cmake
    cmake_exe = mock_executable("cmake", output="echo cmake version 3.19.1")
    prefix = os.path.dirname(cmake_exe)
    monkeypatch.setenv("PATH", prefix)

    openssl_exe = mock_executable("openssl", output="OpenSSL 2.8.3")
    prefix = os.path.dirname(openssl_exe)
    monkeypatch.setenv("PATH", prefix)

    # Test that we detect specs
    output = external("find", *command_args)
    assert "The following specs have been" in output
    assert "cmake" in output
    assert "openssl" not in output


@pytest.mark.regression("38733")
@pytest.mark.skipif(sys.platform == "win32", reason="the test uses bash scripts")
def test_failures_in_scanning_do_not_result_in_an_error(
    mock_executable, monkeypatch, mutable_config
):
    """Tests that scanning paths with wrong permissions, won't cause `external find` to error."""
    cmake_exe1 = mock_executable(
        "cmake", output="echo cmake version 3.19.1", subdir=("first", "bin")
    )
    cmake_exe2 = mock_executable(
        "cmake", output="echo cmake version 3.23.3", subdir=("second", "bin")
    )

    # Remove access from the first directory executable
    cmake_exe1.parent.chmod(0o600)

    value = os.pathsep.join([str(cmake_exe1.parent), str(cmake_exe2.parent)])
    monkeypatch.setenv("PATH", value)

    output = external("find", "cmake")
    assert external.returncode == 0
    assert "The following specs have been" in output
    assert "cmake" in output
    assert "3.23.3" in output
    assert "3.19.1" not in output

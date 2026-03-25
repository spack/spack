# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib
import sys

import pytest

import spack.cmd.external
import spack.config
import spack.cray_manifest
import spack.detection
import spack.detection.path
import spack.repo
from spack.compilers.config import CompilerFactory
from spack.llnl.util.filesystem import getuid, touch
from spack.main import SpackCommand
from spack.spec import Spec

pytestmark = [pytest.mark.usefixtures("mock_packages")]


@pytest.fixture
def executables_found(monkeypatch):
    def _factory(result):
        def _mock_search(path_hints=None):
            return result

        monkeypatch.setattr(spack.detection.path, "executables_in_path", _mock_search)

    return _factory


def define_plat_exe(exe):
    if sys.platform == "win32":
        exe += ".bat"
    return exe


def test_find_external_update_config(mutable_config):
    entries = [
        Spec.from_detection("cmake@1.foo", external_path="/x/y1"),
        Spec.from_detection("cmake@3.17.2", external_path="/x/y2"),
    ]
    pkg_to_entries = {"cmake": entries}

    scope = spack.config.default_modify_scope("packages")
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get("packages")
    cmake_cfg = pkgs_cfg["cmake"]
    cmake_externals = cmake_cfg["externals"]

    assert {"spec": "cmake@1.foo", "prefix": "/x/y1"} in cmake_externals
    assert {"spec": "cmake@3.17.2", "prefix": "/x/y2"} in cmake_externals


def test_get_executables(working_env, mock_executable):
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    path_to_exe = spack.detection.executables_in_path([os.path.dirname(cmake_path1)])
    cmake_exe = define_plat_exe("cmake")
    assert path_to_exe[str(cmake_path1)] == cmake_exe


external = SpackCommand("external")


# TODO: this test should be made to work, but in the meantime it is
# causing intermittent (spurious) CI failures on all PRs
@pytest.mark.not_on_windows("Test fails intermittently on Windows")
def test_find_external_cmd_not_buildable(
    mutable_config, working_env, mock_executable, monkeypatch
):
    """When the user invokes 'spack external find --not-buildable', the config
    for any package where Spack finds an external version should be marked as
    not buildable.
    """
    version = "1.foo"

    @classmethod
    def _determine_version(cls, exe):
        return version

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    monkeypatch.setattr(cmake_cls, "determine_version", _determine_version)

    cmake_path = mock_executable("cmake", output=f"echo cmake version {version}")
    os.environ["PATH"] = str(cmake_path.parent)
    external("find", "--not-buildable", "cmake")
    pkgs_cfg = spack.config.get("packages")
    assert "cmake" in pkgs_cfg
    assert not pkgs_cfg["cmake"]["buildable"]


@pytest.mark.parametrize(
    "names,tags,exclude,expected",
    [
        # find -all
        (
            None,
            ["detectable"],
            [],
            [
                "builtin_mock.cmake",
                "builtin_mock.find-externals1",
                "builtin_mock.gcc",
                "builtin_mock.intel-oneapi-compilers",
                "builtin_mock.llvm",
                "builtin_mock.mpich",
                "builtin_mock.mpileaks",
            ],
        ),
        # find --all --exclude find-externals1
        (
            None,
            ["detectable"],
            ["builtin_mock.find-externals1"],
            [
                "builtin_mock.cmake",
                "builtin_mock.gcc",
                "builtin_mock.intel-oneapi-compilers",
                "builtin_mock.llvm",
                "builtin_mock.mpich",
                "builtin_mock.mpileaks",
            ],
        ),
        (
            None,
            ["detectable"],
            ["find-externals1"],
            [
                "builtin_mock.cmake",
                "builtin_mock.gcc",
                "builtin_mock.intel-oneapi-compilers",
                "builtin_mock.llvm",
                "builtin_mock.mpich",
                "builtin_mock.mpileaks",
            ],
        ),
        # find hwloc (and mock hwloc is not detectable)
        (["hwloc"], ["detectable"], [], []),
    ],
)
def test_package_selection(names, tags, exclude, expected):
    """Tests various cases of selecting packages"""
    # In the mock repo we only have 'find-externals1' that is detectable
    result = spack.detection.packages_to_search_for(names=names, tags=tags, exclude=exclude)
    assert set(result) == set(expected)


def test_find_external_no_manifest(mutable_config, working_env, monkeypatch):
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
    mutable_config, working_env, tmp_path: pathlib.Path, monkeypatch
):
    """The user runs 'spack external find'; the default path for storing
    manifest files exists but is empty. Ensure that the command does not
    fail.
    """
    empty_manifest_dir = str(tmp_path / "manifest_dir")
    (tmp_path / "manifest_dir").mkdir()
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", empty_manifest_dir)
    external("find")


@pytest.mark.not_on_windows("Can't chmod on Windows")
@pytest.mark.skipif(getuid() == 0, reason="user is root")
def test_find_external_manifest_with_bad_permissions(
    mutable_config, working_env, tmp_path: pathlib.Path, monkeypatch
):
    """The user runs 'spack external find'; the default path for storing
    manifest files exists but with insufficient permissions. Check that
    the command does not fail.
    """
    test_manifest_dir = str(tmp_path / "manifest_dir")
    (tmp_path / "manifest_dir").mkdir()
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


def test_find_external_manifest_failure(mutable_config, tmp_path: pathlib.Path, monkeypatch):
    """The user runs 'spack external find'; the manifest parsing fails with
    some exception. Ensure that the command still succeeds (i.e. moves on
    to other external detection mechanisms).
    """
    # First, create an empty manifest file (without a file to read, the
    # manifest parsing is skipped)
    test_manifest_dir = str(tmp_path / "manifest_dir")
    (tmp_path / "manifest_dir").mkdir()
    test_manifest_file_path = os.path.join(test_manifest_dir, "test.json")
    touch(test_manifest_file_path)

    def fail():
        raise Exception()

    monkeypatch.setattr(spack.cmd.external, "_collect_and_consume_cray_manifest_files", fail)
    monkeypatch.setenv("PATH", "")
    output = external("find")
    assert "Skipping manifest and continuing" in output


def test_find_external_merge(mutable_config):
    """Checks that 'spack find external' doesn't overwrite an existing spec in packages.yaml."""
    pkgs_cfg_init = {
        "find-externals1": {
            "externals": [{"spec": "find-externals1@1.1", "prefix": "/preexisting-prefix"}],
            "buildable": False,
        }
    }

    mutable_config.update_config("packages", pkgs_cfg_init)
    entries = [
        Spec.from_detection("find-externals1@1.1", external_path="/x/y1"),
        Spec.from_detection("find-externals1@1.2", external_path="/x/y2"),
    ]
    pkg_to_entries = {"find-externals1": entries}
    scope = spack.config.default_modify_scope("packages")
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get("packages")
    pkg_cfg = pkgs_cfg["find-externals1"]
    pkg_externals = pkg_cfg["externals"]

    assert {"spec": "find-externals1@1.1", "prefix": "/preexisting-prefix"} in pkg_externals
    assert {"spec": "find-externals1@1.2", "prefix": "/x/y2"} in pkg_externals


def test_list_detectable_packages(mutable_config):
    external("list")
    assert external.returncode == 0


def test_overriding_prefix(mock_executable, mutable_config, monkeypatch):
    gcc_exe = mock_executable("gcc", output="echo 4.2.1")
    search_dir = gcc_exe.parent

    @classmethod
    def _determine_variants(cls, exes, version_str):
        return "languages=c", {"prefix": "/opt/gcc/bin", "compilers": {"c": exes[0]}}

    gcc_cls = spack.repo.PATH.get_pkg_class("gcc")
    monkeypatch.setattr(gcc_cls, "determine_variants", _determine_variants)

    finder = spack.detection.path.ExecutablesFinder()
    detected_specs = finder.find(
        pkg_name="gcc", initial_guess=[str(search_dir)], repository=spack.repo.PATH
    )

    assert len(detected_specs) == 1

    gcc = detected_specs[0]
    assert gcc.name == "gcc"
    assert gcc.external_path == os.path.sep + os.path.join("opt", "gcc", "bin")


@pytest.mark.not_on_windows("Fails spuriously on Windows")
def test_new_entries_are_reported_correctly(mock_executable, mutable_config, monkeypatch):
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
@pytest.mark.not_on_windows("the test uses bash scripts")
def test_use_tags_for_detection(command_args, mock_executable, mutable_config, monkeypatch):
    versions = {"cmake": "3.19.1", "openssl": "2.8.3"}

    @classmethod
    def _determine_version(cls, exe):
        return versions[os.path.basename(exe)]

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    monkeypatch.setattr(cmake_cls, "determine_version", _determine_version)

    # Prepare an environment to detect a fake cmake
    cmake_exe = mock_executable("cmake", output=f"echo cmake version {versions['cmake']}")
    prefix = os.path.dirname(cmake_exe)
    monkeypatch.setenv("PATH", prefix)

    openssl_exe = mock_executable("openssl", output=f"OpenSSL {versions['openssl']}")
    prefix = os.path.dirname(openssl_exe)
    monkeypatch.setenv("PATH", prefix)

    # Test that we detect specs
    output = external("find", *command_args)
    assert "The following specs have been" in output
    assert "cmake" in output
    assert "openssl" not in output


@pytest.mark.regression("38733")
@pytest.mark.not_on_windows("the test uses bash scripts")
def test_failures_in_scanning_do_not_result_in_an_error(
    mock_executable, monkeypatch, mutable_config
):
    """Tests that scanning paths with wrong permissions, won't cause `external find` to error."""
    versions = {"first": "3.19.1", "second": "3.23.3"}

    @classmethod
    def _determine_version(cls, exe):
        bin_parent = os.path.dirname(exe).split(os.sep)[-2]
        return versions[bin_parent]

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    monkeypatch.setattr(cmake_cls, "determine_version", _determine_version)

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
    for vers in versions.values():
        assert vers in output


@pytest.fixture()
def mock_detection(monkeypatch):

    def _detect(pkg_cls, *, version, dependencies=None):
        @classmethod
        def _version(cls, exe):
            return version

        monkeypatch.setattr(pkg_cls, "determine_version", _version, raising=False)

        if dependencies is not None:

            @classmethod
            def _deps(cls, spec):
                return dependencies

            monkeypatch.setattr(pkg_cls, "determine_dependencies", _deps, raising=False)

    return _detect


@pytest.mark.not_on_windows("the test uses bash scripts")
def test_find_external_wires_dependencies(mock_executable, mutable_config, mock_detection):
    """Tests that deps are written to packages.yaml when ``spack external find`` is called"""
    mpileaks_version, mpich_version = "2.3", "4.0.2"

    mpileaks_cls = spack.repo.PATH.get_pkg_class("mpileaks")
    mock_detection(mpileaks_cls, version=mpileaks_version, dependencies=[f"mpich@{mpich_version}"])
    mpileaks_exe = mock_executable("mpileaks", output=f"echo mpileaks version {mpileaks_version}")

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mpich_exe = mock_executable("mpichversion", output=f"echo MPICH Version: {mpich_version}")
    mock_detection(mpich_cls, version=mpich_version)

    external(
        "find",
        "--path",
        str(mpileaks_exe.parent),
        "--path",
        str(mpich_exe.parent),
        "mpileaks",
        "mpich",
    )

    packages_yaml = mutable_config.get_config("packages")
    mpileaks_entry = packages_yaml["mpileaks"]["externals"][0]
    mpich_entry = packages_yaml["mpich"]["externals"][0]

    # Both entries must have an ID
    assert "id" in mpileaks_entry and "id" in mpich_entry

    # mpileaks must list mpich as a dependency.
    assert "dependencies" in mpileaks_entry and len(mpileaks_entry["dependencies"]) == 1
    assert mpileaks_entry["dependencies"][0]["id"] == mpich_entry["id"]

    # mpich is a leaf: no dependencies field.
    assert "dependencies" not in mpich_entry


@pytest.mark.not_on_windows("the test uses bash scripts")
def test_find_external_augments_preexisting_entry(mock_executable, mutable_config, mock_detection):
    """Tests that preexisting packages.yaml entries get an id added when they appear as a
    dependency.
    """
    mpileaks_version, mpich_version = "2.3", "4.0.2"
    mpich_prefix = "/opt/mpich"

    # Seed packages.yaml with mpich already present (no id).
    mutable_config.set(
        "packages",
        {"mpich": {"externals": [{"spec": f"mpich@{mpich_version}", "prefix": mpich_prefix}]}},
    )

    mpileaks_cls = spack.repo.PATH.get_pkg_class("mpileaks")
    mock_detection(mpileaks_cls, version=mpileaks_version, dependencies=["mpich@4.0.2"])
    mpileaks_exe = mock_executable("mpileaks", output=f"echo mpileaks version {mpileaks_version}")

    external("find", "--path", str(mpileaks_exe.parent), "mpileaks")

    packages_yaml = mutable_config.get_config("packages")
    mpileaks_entry = packages_yaml["mpileaks"]["externals"][0]
    mpich_entry = packages_yaml["mpich"]["externals"][0]

    # mpileaks must be wired up with id and dependency.
    assert "id" in mpileaks_entry and "dependencies" in mpileaks_entry
    assert mpileaks_entry["dependencies"][0]["id"] == mpich_entry["id"]

    # The preexisting mpich entry must have received an id.
    assert "id" in mpich_entry


@pytest.mark.not_on_windows("the test uses bash scripts")
def test_find_external_no_dependencies_no_id(mock_executable, mutable_config, mock_detection):
    """Tests that packages that are not dependencies get no id or dependencies in YAML"""
    cmake_version = "3.27.5"

    cmake_cls = spack.repo.PATH.get_pkg_class("cmake")
    mock_detection(cmake_cls, version=cmake_version)
    cmake_exe = mock_executable("cmake", output=f"echo cmake version {cmake_version}")

    external("find", "--path", str(cmake_exe.parent), "cmake")

    packages_yaml = mutable_config.get_config("packages")
    cmake_entry = packages_yaml["cmake"]["externals"][0]
    assert "id" not in cmake_entry
    assert "dependencies" not in cmake_entry


@pytest.mark.not_on_windows("the test uses bash scripts")
def test_find_external_idempotent(mock_executable, mutable_config, mock_detection):
    """Running external find twice with determine_dependencies produces stable config."""
    mpileaks_version, mpich_version = "2.3", "4.0.2"

    mpileaks_cls = spack.repo.PATH.get_pkg_class("mpileaks")
    mock_detection(mpileaks_cls, version=mpileaks_version, dependencies=[f"mpich@{mpich_version}"])
    mpileaks_exe = mock_executable("mpileaks", output=f"echo mpileaks version {mpileaks_version}")

    mpich_cls = spack.repo.PATH.get_pkg_class("mpich")
    mpich_exe = mock_executable("mpichversion", output=f"echo MPICH Version: {mpich_version}")
    mock_detection(mpich_cls, version=mpich_version)

    find_args = [
        "find",
        "--path",
        str(mpileaks_exe.parent),
        "--path",
        str(mpich_exe.parent),
        "cmake",
        "mpich",
    ]

    external(*find_args)
    packages_yaml_first = mutable_config.deepcopy_as_builtin("packages")

    external(*find_args)
    packages_yaml_second = mutable_config.get_config("packages")

    assert packages_yaml_first == packages_yaml_second


def test_detect_virtuals(mock_executable, mutable_config, monkeypatch):
    """Test whether external find --not-buildable sets virtuals as non-buildable (unless user
    config sets them to buildable)"""
    version = "4.0.2"

    @classmethod
    def _determine_version(cls, exe):
        return version

    cmake_cls = spack.repo.PATH.get_pkg_class("mpich")
    monkeypatch.setattr(cmake_cls, "determine_version", _determine_version)

    mpich = mock_executable("mpichversion", output=f"echo MPICH Version:    {version}")
    prefix = os.path.dirname(mpich)
    external("find", "--path", prefix, "--not-buildable", "mpich")

    # Check that mpich was correctly detected
    mpich = mutable_config.get("packages:mpich")
    assert mpich["buildable"] is False
    assert Spec(mpich["externals"][0]["spec"]).satisfies(f"mpich@{version}")

    # Check that the virtual package mpi was marked as non-buildable
    assert mutable_config.get("packages:mpi:buildable") is False

    # Delete the mpich entry, and set mpi explicitly to buildable
    mutable_config.set("packages:mpich", {})
    mutable_config.set("packages:mpi:buildable", True)

    # Run the detection again
    external("find", "--path", prefix, "--not-buildable", "mpich")

    # Check that the mpi:buildable entry was not overwritten
    assert mutable_config.get("packages:mpi:buildable") is True


def test_from_packages_yaml_compiler_with_non_compiler_dependency(mutable_config):
    """Tests that we can read compiler dependencies (e.g. binutils) when retrieving compilers."""
    binutils_id = "binutils-test-uuid"
    gcc_id = "gcc-test-uuid"
    mutable_config.set(
        "packages",
        {
            "gcc": {
                "externals": [
                    {
                        "spec": "gcc@14.1.0",
                        "prefix": "/usr/local/gcc-14",
                        "id": gcc_id,
                        "extra_attributes": {"compilers": {"c": "/usr/local/gcc-14/bin/gcc"}},
                        "dependencies": [{"id": binutils_id}],
                    }
                ]
            },
            "binutils": {
                "externals": [{"spec": "binutils@2.42", "prefix": "/usr", "id": binutils_id}]
            },
        },
    )
    # Must not raise ExternalDependencyError
    compilers = CompilerFactory.from_packages_yaml(mutable_config)
    assert any(c.satisfies("gcc@14.1.0") for c in compilers)


def test_from_packages_yaml_malformed_non_compiler_entry_is_skipped(mutable_config):
    """Tests that a non-compiler entry with a malformed spec (no concrete version) must not prevent
    reading compilers.
    """
    mutable_config.set(
        "packages",
        {
            "gcc": {
                "externals": [
                    {
                        "spec": "gcc@14.1.0",
                        "prefix": "/usr/local/gcc-14",
                        "extra_attributes": {"compilers": {"c": "/usr/local/gcc-14/bin/gcc"}},
                    }
                ]
            },
            # No version — ExternalSpecError("doesn't have a concrete version") inside the parser.
            "binutils": {"externals": [{"spec": "binutils", "prefix": "/usr"}]},
        },
    )
    # Must not raise; the malformed binutils entry must be silently skipped with a warning.
    with pytest.warns(UserWarning, match="concrete version"):
        compilers = CompilerFactory.from_packages_yaml(spack.config.CONFIG)
    assert any(c.satisfies("gcc@14.1.0") for c in compilers)

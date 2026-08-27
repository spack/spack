# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import sys

import pytest

import spack.bootstrap
import spack.bootstrap._common
import spack.bootstrap.clingo
import spack.bootstrap.config
import spack.bootstrap.core
import spack.bootstrap.status
import spack.compilers.config
import spack.config
import spack.environment
import spack.store
import spack.util.executable
import spack.util.prefix

from .conftest import _true


@pytest.fixture
def active_mock_environment(mutable_config, mutable_mock_env_path):
    with spack.environment.create("bootstrap-test") as env:
        yield env


@pytest.mark.regression("22294")
def test_store_is_restored_correctly_after_bootstrap(mutable_config, tmp_path: pathlib.Path):
    """Tests that the store is correctly swapped during bootstrapping, and restored afterward."""
    user_path = str(tmp_path / "store")
    with spack.store.use_store(user_path):
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.store.STORE.root == spack.bootstrap.config.store_path()
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path


@pytest.mark.regression("38963")
def test_store_padding_length_is_zero_during_bootstrapping(mutable_config, tmp_path: pathlib.Path):
    """Tests that, even though padded length is set in user config, the bootstrap store maintains
    a padded length of zero.
    """
    user_path = str(tmp_path / "store")
    with spack.store.use_store(user_path, extra_data={"padded_length": 512}):
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 512
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.store.STORE.root == spack.bootstrap.config.store_path()
            assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 512


@pytest.mark.regression("38963")
def test_install_tree_customization_is_respected(mutable_config, tmp_path: pathlib.Path):
    """Tests that a custom user store is respected when we exit the bootstrapping
    environment.
    """
    spack.store.reinitialize()
    store_dir = tmp_path / "store"
    spack.config.CONFIG.set("config:install_tree:root", str(store_dir))
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.store.STORE.root == spack.bootstrap.config.store_path()
        assert (
            spack.config.CONFIG.get("config:install_tree:root")
            == spack.bootstrap.config.store_path()
        )
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0
    assert spack.config.CONFIG.get("config:install_tree:root") == str(store_dir)
    assert spack.store.STORE.root == str(store_dir)


@pytest.mark.parametrize(
    "config_value,expected",
    [
        # Absolute path without expansion
        ("/opt/spack/bootstrap", "/opt/spack/bootstrap/store"),
        # Path with placeholder
        ("$spack/opt/bootstrap", "$spack/opt/bootstrap/store"),
    ],
)
def test_store_path_customization(config_value, expected, mutable_config):
    # Set the current configuration to a specific value
    spack.config.set("bootstrap:root", config_value)

    # Check the store path
    current = spack.bootstrap.config.store_path()
    assert current == spack.config.canonicalize_path(expected)


def test_raising_exception_if_bootstrap_disabled(mutable_config):
    # Disable bootstrapping in config.yaml
    spack.config.set("bootstrap:enable", False)

    # Check the correct exception is raised
    with pytest.raises(RuntimeError, match="bootstrapping is currently disabled"):
        spack.bootstrap.config.store_path()


def test_raising_exception_module_importable(config, monkeypatch):
    monkeypatch.setattr(spack.bootstrap.core, "source_is_enabled", _true)
    with pytest.raises(ImportError, match='cannot bootstrap the "asdf" Python module'):
        spack.bootstrap.core.ensure_module_importable_or_raise("asdf")


def test_raising_exception_executables_in_path(config, monkeypatch):
    monkeypatch.setattr(spack.bootstrap.core, "source_is_enabled", _true)
    with pytest.raises(RuntimeError, match="cannot bootstrap any of the asdf, fdsa executables"):
        spack.bootstrap.core.ensure_executables_in_path_or_raise(["asdf", "fdsa"], "python")


@pytest.mark.regression("25603")
def test_bootstrap_deactivates_environments(active_mock_environment):
    assert spack.environment.active_environment() == active_mock_environment
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.environment.active_environment() is None
    assert spack.environment.active_environment() == active_mock_environment


@pytest.mark.regression("25805")
def test_bootstrap_disables_modulefile_generation(mutable_config):
    # Be sure to enable both lmod and tcl in modules.yaml
    spack.config.set("modules:default:enable", ["tcl", "lmod"])

    assert "tcl" in spack.config.get("modules:default:enable")
    assert "lmod" in spack.config.get("modules:default:enable")
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert "tcl" not in spack.config.get("modules:default:enable")
        assert "lmod" not in spack.config.get("modules:default:enable")
    assert "tcl" in spack.config.get("modules:default:enable")
    assert "lmod" in spack.config.get("modules:default:enable")


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_no_environment(no_packages_yaml, mock_packages):
    assert not spack.compilers.config.all_compilers(init_config=False)
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.clingo._add_compilers_if_missing()
        assert spack.compilers.config.all_compilers(init_config=False)
    assert not spack.compilers.config.all_compilers(init_config=False)


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_environment_active(
    no_packages_yaml, active_mock_environment, mock_packages
):
    assert not spack.compilers.config.all_compilers(init_config=False)
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.clingo._add_compilers_if_missing()
        assert spack.compilers.config.all_compilers(init_config=False)
    assert not spack.compilers.config.all_compilers(init_config=False)


@pytest.mark.regression("26189")
def test_config_yaml_is_preserved_during_bootstrap(mutable_config):
    expected_dir = "/tmp/test"
    spack.config.set("config:test_stage", expected_dir, scope="command_line")

    assert spack.config.get("config:test_stage") == expected_dir
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.config.get("config:test_stage") == expected_dir
    assert spack.config.get("config:test_stage") == expected_dir


@pytest.mark.regression("26548")
def test_bootstrap_custom_store_in_environment(mutable_config, tmp_path: pathlib.Path):
    # Test that the custom store in an environment is taken into account
    # during bootstrapping
    spack_yaml = tmp_path / "spack.yaml"
    install_root = tmp_path / "store"
    spack_yaml.write_text(
        """
spack:
  specs:
  - libelf
  config:
    install_tree:
      root: {0}
""".format(install_root)
    )
    with spack.environment.Environment(str(tmp_path)):
        assert spack.environment.active_environment()
        assert spack.config.get("config:install_tree:root") == str(install_root)
        # Don't trigger evaluation here
        with spack.bootstrap.ensure_bootstrap_configuration():
            pass
        assert str(spack.store.STORE.root) == str(install_root)


def test_nested_use_of_context_manager(mutable_config):
    """Test nested use of the context manager"""
    user_config = spack.config.CONFIG
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.config.CONFIG != user_config
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.config.CONFIG != user_config
    assert spack.config.CONFIG == user_config


@pytest.mark.parametrize("expected_missing", [False, True])
def test_status_function_find_files(
    mutable_config, mock_executable, tmp_path: pathlib.Path, monkeypatch, expected_missing
):
    if not expected_missing:
        mock_executable("foo", "echo Hello WWorld!")

    monkeypatch.setattr(
        spack.bootstrap.status,
        "_optional_requirements",
        lambda: [spack.bootstrap.status._required_system_executable("foo", "NOT FOUND")],
    )
    monkeypatch.setenv("PATH", str(tmp_path / "bin"))

    _, missing = spack.bootstrap.status_message("optional")
    assert missing is expected_missing


@pytest.mark.parametrize(
    "gpg_in_path,gpg_in_store,expected_missing",
    [
        (True, False, False),  # gpg exists in PATH
        (False, True, False),  # gpg exists in bootstrap store
        (False, False, True),  # gpg is missing
    ],
)
def test_gpg_status_check(
    mutable_config,
    mock_executable,
    tmp_path: pathlib.Path,
    monkeypatch,
    gpg_in_path,
    gpg_in_store,
    expected_missing,
):
    """Test that gpg/gpg2 status is detected whether it's in PATH or in the bootstrap store."""
    # Set up mock PATH with or without gpg
    path_dir = tmp_path / "bin"
    path_dir.mkdir(exist_ok=True)
    monkeypatch.setenv("PATH", str(path_dir))

    if gpg_in_path:
        mock_executable("gpg2", "echo GPG 2.3.4")

    # Mock the bootstrap store function
    def mock_executables_in_store(exes, query_spec, query_info=None):
        if not gpg_in_store:
            return False

        # Simulate found gpg in bootstrap store
        if query_info is not None:
            query_info["spec"] = "gnupg@2.5.12"
            query_info["command"] = spack.util.executable.Executable("gpg")
        return True

    monkeypatch.setattr(spack.bootstrap.status, "_executables_in_store", mock_executables_in_store)

    # Call only the buildcache requirements function directly to isolate the test
    requirements = spack.bootstrap.status._buildcache_requirements()

    # Find the gpg entry by examining the calls made to set up requirements
    # We know the first entry in requirements is the gpg entry because of how
    # _buildcache_requirements is structured:
    # Make sure we're not out of bounds
    assert len(requirements) >= 1, "No gpg requirement found"

    # Check that the gpg requirement matches our expectations
    gpg_req = requirements[0]
    assert gpg_req[0] is not expected_missing


@pytest.mark.regression("31042")
def test_source_is_disabled(mutable_config):
    # Get the configuration dictionary of the current bootstrapping source
    conf = next(iter(spack.bootstrap.core.bootstrapping_sources()))

    # The source is not explicitly enabled or disabled, so the following should return False
    assert not spack.bootstrap.core.source_is_enabled(conf)

    # Try to explicitly disable the source and verify that the behavior is the same as above
    spack.config.add("bootstrap:trusted:{0}:{1}".format(conf["name"], False))
    assert not spack.bootstrap.core.source_is_enabled(conf)


@pytest.mark.regression("45247")
def test_use_store_does_not_try_writing_outside_root(
    tmp_path: pathlib.Path, monkeypatch, mutable_config
):
    """Tests that when we use the 'use_store' context manager, there is no attempt at creating
    a Store outside the given root.
    """
    initial_store = mutable_config.get("config:install_tree:root")
    user_store = tmp_path / "store"

    fn = spack.store.Store.__init__

    def _checked_init(self, root, *args, **kwargs):
        fn(self, root, *args, **kwargs)
        assert self.root == str(user_store)

    monkeypatch.setattr(spack.store.Store, "__init__", _checked_init)

    spack.store.reinitialize()
    with spack.store.use_store(user_store):
        assert spack.config.CONFIG.get("config:install_tree:root") == str(user_store)
    assert spack.config.CONFIG.get("config:install_tree:root") == initial_store


def _make_executable(directory: pathlib.Path, name: str) -> pathlib.Path:
    """Create a runnable stub called ``name`` in ``directory``.

    On Windows ``which_string`` appends the executable suffixes itself, so the file on
    disk is ``name.bat``; elsewhere the name is used verbatim and the mode bit is what
    makes it findable.
    """
    directory.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        executable = directory / f"{name}.bat"
        executable.write_text("@ECHO OFF\n")
    else:
        executable = directory / name
        executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    return executable


class _InstalledSpec:
    """Stand-in for a concrete spec in the store. Only ``prefix`` is ever consulted."""

    def __init__(self, prefix: pathlib.Path):
        self.prefix = spack.util.prefix.Prefix(str(prefix))


@pytest.fixture()
def store_containing(monkeypatch):
    """Report the given prefixes as installed specs matching any query."""

    def _factory(*prefixes: pathlib.Path):
        specs = [_InstalledSpec(p) for p in prefixes]

        class _DB:
            def query(self, query_spec, installed=True):
                return list(specs)

        class _Store:
            db = _DB()

        monkeypatch.setattr(spack.store, "STORE", _Store())
        return specs

    return _factory


@pytest.fixture()
def isolated_path(monkeypatch):
    """``_executables_in_store`` prepends to PATH on success; keep that out of the
    surrounding session.

    Deliberately not autouse: the other tests in this module run real compiler detection
    and executable lookups against the inherited PATH, so narrowing it for them would
    make them fail for reasons that have nothing to do with what they cover.
    """
    monkeypatch.setenv("PATH", os.defpath)


def test_executables_in_store_finds_executable_in_bin(tmp_path, store_containing, isolated_path):
    prefix = tmp_path / "pkg"
    _make_executable(prefix / "bin", "cl")
    store_containing(prefix)
    query_info = {}

    found = spack.bootstrap._common._executables_in_store(["cl"], "compiler-wrapper", query_info)

    assert found is True
    assert query_info["command"] is not None
    assert query_info["spec"].prefix == str(prefix)
    assert str(prefix / "bin") in os.environ["PATH"]


@pytest.mark.parametrize("make_bin", [True, False], ids=["empty-bin", "no-bin"])
def test_executables_in_store_rejects_spec_without_the_executable(
    tmp_path, store_containing, isolated_path, make_bin
):
    """A spec can satisfy the query and still not ship the binary we asked for, whether
    or not it has a bin directory at all. Claiming success there makes the
    ``required=True`` lookup that follows raise instead of letting the caller fall back
    to actually bootstrapping."""
    prefix = tmp_path / "pkg"
    (prefix / "bin" if make_bin else prefix).mkdir(parents=True)
    store_containing(prefix)
    query_info = {}

    found = spack.bootstrap._common._executables_in_store(["cl"], "compiler-wrapper", query_info)

    assert found is False
    assert query_info == {}


def test_executables_in_store_falls_through_to_a_spec_that_has_it(tmp_path, store_containing):
    """Several installed specs can match the query; the first one without the binary
    must not short circuit the search."""
    empty = tmp_path / "empty"
    (empty / "bin").mkdir(parents=True)
    provider = tmp_path / "provider"
    _make_executable(provider / "bin", "cl")
    store_containing(empty, provider)
    query_info = {}

    found = spack.bootstrap._common._executables_in_store(["cl"], "compiler-wrapper", query_info)

    assert found is True
    assert query_info["spec"].prefix == str(provider)


def test_executables_in_store_accepts_any_of_the_alternatives(tmp_path, store_containing):
    """The executables are alternates, so the search exits on the first one present."""
    prefix = tmp_path / "pkg"
    _make_executable(prefix / "bin", "cl")
    store_containing(prefix)

    assert spack.bootstrap._common._executables_in_store(["nope", "cl"], "compiler-wrapper")


def test_executables_in_store_without_installed_specs(store_containing):
    store_containing()

    assert spack.bootstrap._common._executables_in_store(["cl"], "compiler-wrapper") is False


@pytest.mark.only_windows("prefix/bin is a less common idiom on Windows")
def test_executables_in_store_searches_below_prefix_on_windows(
    tmp_path, store_containing, isolated_path
):
    """Windows packages routinely put binaries somewhere other than prefix/bin, so the
    whole prefix is searched rather than just that one directory."""
    prefix = tmp_path / "pkg"
    tools = prefix / "Library" / "tools"
    _make_executable(tools, "relocate")
    store_containing(prefix)
    query_info = {}

    found = spack.bootstrap._common._executables_in_store(
        ["relocate"], "compiler-wrapper", query_info
    )

    assert found is True
    assert str(tools) in os.environ["PATH"]
    assert query_info["spec"].prefix == str(prefix)

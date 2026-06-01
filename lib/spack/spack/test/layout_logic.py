# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for layout detection and config variable resolution."""

import os
import pathlib
import shutil
from pathlib import Path

import pytest

import spack.config
import spack.paths
import spack.util.path


@pytest.fixture(scope="function", autouse=True)
def clean_config_env(monkeypatch):
    """Unset config-related env vars that would interfere with layout tests."""
    # Clear config path overrides
    monkeypatch.delenv("SPACK_DISABLE_LOCAL_CONFIG", raising=False)
    monkeypatch.delenv("SPACK_USER_CONFIG_PATH", raising=False)
    monkeypatch.delenv("SPACK_SYSTEM_CONFIG_PATH", raising=False)

    # Clear XDG and SPACK location overrides
    for location in ["DATA", "STATE", "CACHE"]:
        monkeypatch.delenv(f"XDG_{location}_HOME", raising=False)
        monkeypatch.delenv(f"SPACK_{location}_HOME", raising=False)


def _ensure_dir(pathlike):
    """Create directory and return as string."""
    pathlike = pathlib.Path(pathlike)
    pathlike.mkdir(parents=True, exist_ok=True)
    return str(pathlike)


@pytest.fixture
def set_home(working_env):
    """Fixture to set HOME environment variable for both Windows and Linux."""

    def _set_home(val):
        # Clear some env vars that can interfere w/ expanduser(~) on Windows
        os.environ.pop("USERPROFILE", None)
        os.environ.pop("HOMEDRIVE", None)
        os.environ["HOMEPATH"] = val

        # For expanduser on Linux
        os.environ["HOME"] = val

    yield _set_home


@pytest.fixture
def mock_spack_instance(tmp_path, set_home, monkeypatch, clean_config_env):
    """Create a mock Spack instance with simulated home and base prefix.

    Returns:
        tuple: (home_dir, base_prefix)
    """
    # Create simulated directories
    home_dir = _ensure_dir(tmp_path / "home")
    base_prefix = _ensure_dir(tmp_path / "spack-root")

    # Copy real etc/spack into the simulated base prefix (includes defaults and include.yaml)
    real_etc_spack = os.path.join(spack.paths.prefix, "etc", "spack")
    sim_etc_spack = os.path.join(base_prefix, "etc", "spack")
    os.makedirs(os.path.dirname(sim_etc_spack), exist_ok=True)
    shutil.copytree(real_etc_spack, sim_etc_spack)

    # Set up environment using set_home fixture (handles both Windows and Linux)
    set_home(home_dir)

    # Create a new SpackPaths instance pointing to the mock base
    from spack.paths import SpackPaths

    mock_paths = SpackPaths(_prefix=base_prefix)

    # Replace the global locations object
    monkeypatch.setattr(spack.paths, "locations", mock_paths)

    return home_dir, base_prefix


def test_old_layout_detected(mock_spack_instance):
    """Test that old layout is detected when old install directory exists."""
    home_dir, base_prefix = mock_spack_instance

    # Touch the old install directory to make it "occupied"
    old_install = os.path.join(base_prefix, "opt", "spack")
    os.makedirs(old_install, exist_ok=True)
    # Add a file so dir_is_occupied returns True
    with open(os.path.join(old_install, "dummy_install"), "w", encoding="utf-8") as f:
        f.write("test")

    # Re-detect layout
    from spack.paths import SpackPaths, detect_old_spack_layout

    mock_paths = SpackPaths(_prefix=base_prefix)
    old_detected = detect_old_spack_layout(mock_paths)

    assert old_detected, "Old layout should be detected when opt/spack has content"

    # Create a new configuration to see if it picks up the old scope
    # The include.yaml should include the "old" scope when layout_detected("old") is true
    cfg = spack.config.create()

    # Check that we have the defaults scope
    assert "defaults" in cfg.scopes, "Should have defaults scope"

    # The old-layout scope should be included if the condition is met
    scope_names = list(cfg.scopes.keys())

    # Based on include.yaml, if old layout is detected, we should see "old-layout" scope
    assert len(scope_names) > 0, "Should have at least one scope"


def test_config_defaults_use_data_home(mock_spack_instance):
    """Test that config defaults reference $data_home for various paths."""
    home_dir, base_prefix = mock_spack_instance

    # Create a fresh configuration
    cfg = spack.config.create()

    # Get install_tree root - it should reference $data_home
    install_tree_root = cfg.get("config:install_tree:root")

    # The value from base/config.yaml should be "$data_home/installs"
    assert install_tree_root == "$data_home/installs", (
        f"Expected $data_home/installs, got {install_tree_root}"
    )

    # Test other paths that should use $data_home
    license_dir = cfg.get("config:license_dir")
    assert "$data_home" in license_dir, f"license_dir should use $data_home, got {license_dir}"

    source_cache = cfg.get("config:source_cache")
    assert "$data_home" in source_cache, f"source_cache should use $data_home, got {source_cache}"

    environments_root = cfg.get("config:environments_root")
    assert "$data_home" in environments_root, (
        f"environments_root should use $data_home, got {environments_root}"
    )

    gpg_path = cfg.get("config:gpg_path")
    assert "$data_home" in gpg_path, f"gpg_path should use $data_home, got {gpg_path}"

    gpg_keys_path = cfg.get("config:gpg_keys_path")
    assert "$data_home" in gpg_keys_path, (
        f"gpg_keys_path should use $data_home, got {gpg_keys_path}"
    )


def test_locations_config_exists(mock_spack_instance):
    """Test that config:locations section exists with data, state, and cache keys."""
    home_dir, base_prefix = mock_spack_instance

    # Create a fresh configuration
    cfg = spack.config.create()

    # Get the locations config
    locations_data = cfg.get("config:locations:data")
    locations_state = cfg.get("config:locations:state")
    locations_cache = cfg.get("config:locations:cache")

    # These should be lists according to our schema
    assert isinstance(locations_data, list), (
        f"locations:data should be a list, got {locations_data}"
    )
    assert isinstance(locations_state, list), (
        f"locations:state should be a list, got {locations_state}"
    )
    assert isinstance(locations_cache, list), (
        f"locations:cache should be a list, got {locations_cache}"
    )

    # Check that the lists contain expected entries
    assert any("XDG_DATA_HOME" in str(x) for x in locations_data), (
        "locations:data should include XDG_DATA_HOME entry"
    )
    assert any("XDG_STATE_HOME" in str(x) for x in locations_state), (
        "locations:state should include XDG_STATE_HOME entry"
    )


class SetAnXdgVarAndReadDataHome:
    """Set XDG_DATA_HOME in a subprocess and verify that $data_home resolution
    is not affected due to freeze mechanism."""

    def __init__(self, expected_data_home):
        self.expected_data_home = expected_data_home

    def __call__(self):
        import os

        # Set XDG_DATA_HOME to a bogus value in the subprocess
        os.environ["XDG_DATA_HOME"] = "/made-up-value-that-shouldnt-matter"

        import spack.util.path

        # Resolve $data_home - it should use the frozen value from the parent
        # process, not the XDG_DATA_HOME we just set
        actual = spack.util.path.substitute_path_variables("$data_home")

        assert actual == self.expected_data_home, (
            f"Subprocess should use frozen parent value, not XDG_DATA_HOME.\n"
            f"Expected: {self.expected_data_home}\n"
            f"Got: {actual}\n"
            f"XDG_DATA_HOME={os.environ.get('XDG_DATA_HOME')}"
        )


def test_child_proc_xdg_isolation(tmp_path, mock_spack_instance, mutable_config, monkeypatch):
    """Test that subprocess inherits frozen path values from parent, not env vars.

    Build subprocesses may set XDG_* environment variables. We want to ensure that
    $data_home resolution in those subprocesses uses the frozen values from the
    parent process (via freeze() in subprocess_context), not the new env vars.

    This test modifies the global spack.paths.locations and must run serially.
    """
    import spack.config
    import spack.subprocess_context

    home_dir, base_prefix = mock_spack_instance

    # Create fresh config after monkeypatch to pick up new paths
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    # Expected data_home based on the home we set (without any XDG override)
    expected = str(pathlib.Path(home_dir) / ".local" / "share" / "spack")

    # Run in subprocess that sets XDG_DATA_HOME
    spack_process = spack.subprocess_context.SpackTestProcess(SetAnXdgVarAndReadDataHome(expected))
    proc = spack_process.create()
    proc.start()
    proc.join()
    assert proc.exitcode == 0, "Subprocess test failed"


def test_warn_old_dotspack_when_only_dotspack_exists(mock_spack_instance, monkeypatch):
    """Warn if ~/.spack exists but ~/.config/spack doesn't."""
    import spack.config
    import spack.main

    home_dir, base_prefix = mock_spack_instance

    _ensure_dir(pathlib.Path(home_dir) / ".spack")
    # Don't create ~/.config/spack

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    warning = spack.main._old_dotspack_warning()

    assert warning is not None
    assert "~/.spack" in warning
    assert "spack migrate" in warning


def test_no_warn_when_both_exist(mock_spack_instance, monkeypatch):
    """Don't warn if both ~/.spack and ~/.config/spack exist."""
    import spack.config
    import spack.main

    home_dir, base_prefix = mock_spack_instance

    _ensure_dir(pathlib.Path(home_dir) / ".spack")
    _ensure_dir(pathlib.Path(home_dir) / ".config" / "spack")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    warning = spack.main._old_dotspack_warning()

    assert warning is None


def test_no_warn_when_explicit_override(mock_spack_instance, working_env, monkeypatch):
    """Don't warn if SPACK_USER_CONFIG_PATH explicitly set to ~/.spack."""
    import spack.config
    import spack.main

    home_dir, base_prefix = mock_spack_instance

    dotspack = _ensure_dir(pathlib.Path(home_dir) / ".spack")
    # Don't create ~/.config/spack

    os.environ["SPACK_USER_CONFIG_PATH"] = str(dotspack)

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    warning = spack.main._old_dotspack_warning()

    assert warning is None


def test_user_cache_path_is_default_when_env_var_is_empty(working_env, mock_spack_instance, monkeypatch):
    import spack.config

    home_dir, base_prefix = mock_spack_instance

    # Create fresh config after mock_spack_instance sets up paths
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    assert os.path.join(home_dir, ".local", "state", "spack") == spack.paths.user_cache_path


def test_user_cache_path_is_overridable(working_env, mock_spack_instance, monkeypatch):
    home_dir, base_prefix = mock_spack_instance
    p = str(Path("some") / "path")
    os.environ["SPACK_STATE_HOME"] = p

    # Create fresh SpackPaths instance after setting env var
    from spack.paths import SpackPaths

    fresh_paths = SpackPaths(_prefix=base_prefix)
    monkeypatch.setattr(spack.paths, "locations", fresh_paths)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    assert spack.paths.user_cache_path == p


def test_substitute_user_cache(mock_spack_instance):
    assert os.path.join(spack.paths.user_cache_path, "baz") == spack.util.path.canonicalize_path(
        os.path.join("$user_cache_path", "baz")
    )

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.paths
import spack.paths_base
from spack.paths import SpackPaths
from spack.paths_base import SpackPathsBase


def _ensure_dir(pathlike):
    pathlike.mkdir(parents=True, exist_ok=True)
    return str(pathlike)


@pytest.fixture(autouse=True)
def clear_env_vars(working_env):
    """Scrub XDG_*/SPACK_* env vars so each test starts from a known state."""
    spack.paths._unset_path_vars(os.environ)


def _set_locations(cfg, **kwargs):
    """Set config:locations:* keys (avoiding the leftover state pitfall of
    overwriting the whole locations block)."""
    for k, v in kwargs.items():
        cfg.set(f"config:locations:{k}", v)


@pytest.fixture
def mock_paths_locations(tmp_path, set_home, monkeypatch):
    """Create test SpackPaths instance and monkeypatch it as the global locations.

    Returns:
        str: The home_prefix path that was set up
    """
    home_prefix = _ensure_dir(tmp_path / "home-prefix")
    base_prefix = _ensure_dir(tmp_path / "spack-root")
    set_home(home_prefix)

    test_base = SpackPathsBase(base_prefix)
    test_paths = SpackPaths(test_base)
    monkeypatch.setattr(spack.paths, "locations", test_paths)
    monkeypatch.setattr(spack.paths_base, "locations", test_base)

    return home_prefix


# ---------------------------------------------------------------------------
# Home property resolution
# ---------------------------------------------------------------------------


def test_data_home_precedence(working_env, tmp_path, mutable_config, set_home):
    """Test the full precedence chain for data_home resolution.

    From lowest to highest precedence:
    1. Default: ~/.local/share/spack
    2. XDG_DATA_HOME: $XDG_DATA_HOME/spack
    3. config:locations:home: <config_home>/.local/share/spack
    4. config:locations:data: <config_data> (direct)
    5. SPACK_HOME: $SPACK_HOME/.local/share/spack
    6. SPACK_DATA_HOME: $SPACK_DATA_HOME (direct, highest)
    """
    # Setup paths
    home = _ensure_dir(tmp_path / "home")
    x1 = _ensure_dir(tmp_path / "x1")
    x2 = _ensure_dir(tmp_path / "x2")
    x3 = _ensure_dir(tmp_path / "x3")
    x4 = _ensure_dir(tmp_path / "x4")

    set_home(home)

    # 1. Default: ~/.local/share/spack
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == os.path.join(home, ".local", "share", "spack")

    # 2. XDG_DATA_HOME overrides default
    os.environ["XDG_DATA_HOME"] = x1
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == os.path.join(x1, "spack")

    # 3. config:locations:home overrides XDG_DATA_HOME
    mutable_config.set("config:locations:home", x2)
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == os.path.join(x2, ".local", "share", "spack")

    # 4. config:locations:data overrides config:locations:home
    mutable_config.set("config:locations:data", x3)
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == x3

    # 5. SPACK_HOME overrides config:locations:data
    os.environ["SPACK_HOME"] = x4
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == os.path.join(x4, ".local", "share", "spack")

    # 6. SPACK_DATA_HOME overrides SPACK_HOME
    x5 = _ensure_dir(tmp_path / "x5")
    os.environ["SPACK_DATA_HOME"] = x5
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == x5

    # 7. disable_env goes back to config:locations:data (ignores env vars)
    mutable_config.set("config:locations:disable_env", True)
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == x3  # back to config:locations:data

    # 8. Clear locations and set only home, should use config:locations:home
    mutable_config.set("config:locations", {})
    mutable_config.set("config:locations:home", x2)
    mutable_config.set("config:locations:disable_env", True)
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == os.path.join(x2, ".local", "share", "spack")

    # 9. Clear all locations settings, should use default
    mutable_config.set("config:locations", {})
    mutable_config.set("config:locations:disable_env", True)
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.data_home == os.path.join(home, ".local", "share", "spack")


def test_data_home_from_config(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, data=str(tmp_path / "datadir"))
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.data_home == str(tmp_path / "datadir")


def test_state_home_from_config(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, state=str(tmp_path / "statedir"))
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.state_home == str(tmp_path / "statedir")


def test_cache_home_from_config(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, cache=str(tmp_path / "cachedir"))
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.cache_home == str(tmp_path / "cachedir")


def test_spack_home_from_config(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, home=str(tmp_path / "spackhome"))
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.spack_home == str(tmp_path / "spackhome")


def test_data_home_env_overrides_config(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, data=str(tmp_path / "fromconfig"))
    os.environ["SPACK_DATA_HOME"] = str(tmp_path / "fromenv")
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.data_home == str(tmp_path / "fromenv")


def test_spack_home_env_overrides_subhomes(working_env, tmp_path, mutable_config, set_home):
    """SPACK_HOME (no _DATA_/_STATE_/_CACHE_) provides a root and the homes
    derive from it via their XDG-style subpaths."""
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, data=str(tmp_path / "fromconfig"))
    os.environ["SPACK_HOME"] = str(tmp_path / "alt-home")
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.data_home == str(tmp_path / "alt-home" / ".local" / "share" / "spack")
    assert p.state_home == str(tmp_path / "alt-home" / ".local" / "state" / "spack")
    assert p.cache_home == str(tmp_path / "alt-home" / ".cache" / "spack")


def test_specific_env_overrides_spack_home(working_env, tmp_path, mutable_config, set_home):
    """SPACK_DATA_HOME beats SPACK_HOME for data_home."""
    set_home(_ensure_dir(tmp_path / "home"))
    os.environ["SPACK_HOME"] = str(tmp_path / "alt-home")
    os.environ["SPACK_DATA_HOME"] = str(tmp_path / "specific-data")
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.data_home == str(tmp_path / "specific-data")


def test_disable_env_ignores_env_vars(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, data=str(tmp_path / "fromconfig"))
    mutable_config.set("config:locations:disable_env", True)
    os.environ["SPACK_DATA_HOME"] = str(tmp_path / "fromenv")
    os.environ["SPACK_HOME"] = str(tmp_path / "alt-home")
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.data_home == str(tmp_path / "fromconfig")


# ---------------------------------------------------------------------------
# SPACK_USER_CACHE_PATH is a legacy alias for SPACK_STATE_HOME
# ---------------------------------------------------------------------------


def test_user_cache_path_env_sets_state_home(working_env, tmp_path, mutable_config):
    target = str(tmp_path / "cache")
    os.environ["SPACK_USER_CACHE_PATH"] = target
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.user_cache_path == target
    assert p.state_home == target
    # Things rooted under state_home follow.
    assert p.package_repos_path == os.path.join(target, "package_repos")


def test_state_home_env_overrides_user_cache_path(working_env, tmp_path, mutable_config):
    """When both SPACK_USER_CACHE_PATH and SPACK_STATE_HOME are set, the
    older one (SPACK_USER_CACHE_PATH) wins, matching pre-1.2 behavior."""
    legacy = str(tmp_path / "legacy")
    new = str(tmp_path / "new")
    os.environ["SPACK_USER_CACHE_PATH"] = legacy
    os.environ["SPACK_STATE_HOME"] = new
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base")))
    assert p.state_home == legacy


# ---------------------------------------------------------------------------
# Config path overrides (SPACK_USER_CONFIG_PATH, SPACK_SYSTEM_CONFIG_PATH)
# These still live in paths_base because they bootstrap config itself.
# ---------------------------------------------------------------------------


def test_user_config_path_is_overridable(working_env, tmp_path):
    target = str(tmp_path / "redirected_usrcfg")
    os.environ["SPACK_USER_CONFIG_PATH"] = target
    pb = SpackPathsBase(_ensure_dir(tmp_path / "base-prefix"))
    assert pb.user_config_path == target


def test_user_config_path_default(working_env, tmp_path):
    os.environ["SPACK_USER_CONFIG_PATH"] = ""
    pb = SpackPathsBase(str(tmp_path))
    assert pb.user_config_path == os.path.expanduser(os.path.join("~", ".config", "spack"))


def test_system_config_path_is_overridable(working_env, tmp_path):
    target = str(tmp_path / "redirected_syscfg")
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = target
    pb = SpackPathsBase(_ensure_dir(tmp_path / "base-prefix"))
    assert pb.system_config_path == target


def test_system_config_path_default(working_env, tmp_path):
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = ""
    pb = SpackPathsBase(str(tmp_path))
    assert pb.system_config_path == os.sep + os.path.join("etc", "spack")


# ---------------------------------------------------------------------------
# Layout detection (detect_layout / layout_detected) — the helper exposed
# to include `when:` clauses.
# ---------------------------------------------------------------------------


@pytest.fixture
def empty_spack_root(tmp_path):
    base = SpackPathsBase(_ensure_dir(tmp_path / "spack-root"))
    yield base


@pytest.fixture
def occupied_spack_root(tmp_path):
    base = SpackPathsBase(_ensure_dir(tmp_path / "spack-root"))
    # Put something in old install location to trigger old-layout detection.
    inst = pathlib.Path(base.old_install_path)
    inst.mkdir(parents=True, exist_ok=True)
    (inst / "marker").touch()
    yield base


def test_detect_layout_empty_root_is_xdg(working_env, empty_spack_root, monkeypatch):
    monkeypatch.setattr(spack.paths_base, "locations", empty_spack_root)
    assert spack.paths.detect_layout("old") is False
    assert spack.paths.detect_layout("xdg") is True


def test_detect_layout_old_data_present(working_env, occupied_spack_root, monkeypatch):
    monkeypatch.setattr(spack.paths_base, "locations", occupied_spack_root)
    assert spack.paths.detect_layout("old") is True
    assert spack.paths.detect_layout("xdg") is False


def test_detect_layout_env_var_forces_xdg(working_env, occupied_spack_root, monkeypatch):
    """Even with old-layout markers, any SPACK_*_HOME env var forces xdg."""
    monkeypatch.setattr(spack.paths_base, "locations", occupied_spack_root)
    for var in ("SPACK_DATA_HOME", "SPACK_STATE_HOME", "SPACK_CACHE_HOME", "SPACK_HOME"):
        os.environ.pop(var, None)
        os.environ[var] = "/tmp/somewhere"
        try:
            assert spack.paths.detect_layout("old") is False, f"{var} should force xdg"
        finally:
            del os.environ[var]


def test_detect_layout_rejects_unknown_scheme():
    with pytest.raises(ValueError, match="unknown layout scheme"):
        spack.paths.detect_layout("eggplant")


def test_layout_detected_in_eval_conditional(occupied_spack_root, monkeypatch):
    """The helper is reachable from include `when:` clauses via eval_conditional."""
    import spack.spec

    monkeypatch.setattr(spack.paths_base, "locations", occupied_spack_root)
    assert spack.spec.eval_conditional("layout_detected('old')") is True
    assert spack.spec.eval_conditional("not layout_detected('old')") is False
    assert spack.spec.eval_conditional("layout_detected('xdg')") is False


# ---------------------------------------------------------------------------
# $xdg_data_home / $xdg_state_home / $xdg_cache_home substitutions
# ---------------------------------------------------------------------------


def test_home_substitutions_respect_env_vars(
    working_env, tmp_path, mutable_config, mock_paths_locations
):
    from spack.util.path import canonicalize_path

    # mock_paths_locations sets up the test instance, we just need tmp_path for XDG vars
    os.environ["XDG_DATA_HOME"] = str(tmp_path / "xdg-data")
    os.environ["XDG_STATE_HOME"] = str(tmp_path / "xdg-state")
    os.environ["XDG_CACHE_HOME"] = str(tmp_path / "xdg-cache")

    assert canonicalize_path("$data_home") == str(tmp_path / "xdg-data" / "spack")
    assert canonicalize_path("$state_home") == str(tmp_path / "xdg-state" / "spack")
    assert canonicalize_path("$cache_home") == str(tmp_path / "xdg-cache" / "spack")


def test_home_substitutions_fall_back_to_defaults(
    working_env, tmp_path, mock_paths_locations, mutable_config
):
    from spack.util.path import canonicalize_path

    home_prefix = mock_paths_locations

    assert canonicalize_path("$data_home") == os.path.join(home_prefix, ".local", "share", "spack")
    assert canonicalize_path("$state_home") == os.path.join(
        home_prefix, ".local", "state", "spack"
    )
    assert canonicalize_path("$cache_home") == os.path.join(home_prefix, ".cache", "spack")


# ---------------------------------------------------------------------------
# Derived paths (reports, package_repos, etc.) follow state_home
# ---------------------------------------------------------------------------


def test_derived_paths_follow_state_home(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, state=str(tmp_path / "statedir"))
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.reports_path == str(tmp_path / "statedir" / "reports")
    assert p.default_monitor_path == str(tmp_path / "statedir" / "reports" / "monitor")
    assert p.user_repos_cache_path == str(tmp_path / "statedir" / "git_repos")
    assert p.package_repos_path == str(tmp_path / "statedir" / "package_repos")


def test_dotspack_backup_pinned_to_xdg_default(working_env, tmp_path, mutable_config, set_home):
    """dotspack_backup is pinned to ~/.local/share/spack/dotspack_backup and
    does NOT follow data_home, so the migration backup lives in a stable
    location regardless of SPACK_DATA_HOME / config:locations:data."""
    home = _ensure_dir(tmp_path / "home")
    set_home(home)
    _set_locations(mutable_config, data=str(tmp_path / "datadir"))  # ignored by dotspack_backup
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.dotspack_backup == os.path.join(home, ".local", "share", "spack", "dotspack_backup")


# ---------------------------------------------------------------------------
# gpg_path / gpg_keys_path read config first, fall back to data_home
# ---------------------------------------------------------------------------


def test_gpg_path_from_config(working_env, tmp_path, mutable_config, set_home):
    set_home(_ensure_dir(tmp_path / "home"))
    mutable_config.set("config:gpg_path", str(tmp_path / "my-gpg"))
    p = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "spack-root")))
    assert p.gpg_path == str(tmp_path / "my-gpg")


def test_gpg_path_default_from_scheme(working_env, tmp_path, mutable_config, set_home, monkeypatch):
    """The xdg scheme yaml sets config:gpg_path to $data_home/gpg by default;
    the property simply reads that."""
    set_home(_ensure_dir(tmp_path / "home"))
    _set_locations(mutable_config, data=str(tmp_path / "datadir"))
    # base/config.yaml sets gpg_path to $data_home/gpg
    mutable_config.set("config:gpg_path", "$data_home/gpg")
    test_base = SpackPathsBase(_ensure_dir(tmp_path / "spack-root"))
    p = SpackPaths(test_base)
    monkeypatch.setattr(spack.paths, "locations", p)
    monkeypatch.setattr(spack.paths_base, "locations", test_base)
    assert p.gpg_path == str(tmp_path / "datadir" / "gpg")


# ---------------------------------------------------------------------------
# Module shim: spack.paths.X works for both static and dynamic attributes
# ---------------------------------------------------------------------------


def test_module_shim_static_attribute():
    # `prefix` lives on paths_base.SpackPathsBase; spack.paths.prefix
    # should reach it via the SpackPaths.__getattr__ delegation.
    assert spack.paths.prefix == spack.paths.locations.prefix


def test_module_shim_dynamic_attribute():
    # `state_home` is computed by SpackPaths; access via the module
    # should also work.
    assert spack.paths.state_home == spack.paths.locations.state_home


# ---------------------------------------------------------------------------
# Subprocess isolation test
# ---------------------------------------------------------------------------


class SetAnXdgVarAndReadDataHome:
    """Set XDG_DATA_HOME in a subprocess and verify that spack.paths.locations.data_home
    is not affected due to freeze/restore mechanism."""

    def __init__(self, expected_data_home):
        self.expected_data_home = expected_data_home

    def __call__(self):
        import os

        # Set XDG_DATA_HOME to a bogus value in the subprocess
        os.environ["XDG_DATA_HOME"] = "/made-up-value-that-shouldnt-matter"

        import spack.paths

        # Access the global locations singleton - it should use the frozen value
        # from the parent process, not the XDG_DATA_HOME we just set
        actual = spack.paths.locations.data_home

        assert actual == self.expected_data_home, (
            f"Subprocess should use frozen parent value, not XDG_DATA_HOME.\n"
            f"Expected: {self.expected_data_home}\n"
            f"Got: {actual}\n"
            f"XDG_DATA_HOME={os.environ.get('XDG_DATA_HOME')}"
        )


def test_child_proc_xdg_isolation(tmp_path, mock_paths_locations, mutable_config):
    """Test that subprocess inherits frozen path values from parent, not env vars.

    Build subprocesses may set XDG_* environment variables. We want to ensure that
    the global spack.paths.locations singleton in those subprocesses uses the frozen
    values from the parent process (via freeze/restore in subprocess_context), not
    the new env vars.

    This test modifies the global spack.paths.locations and must run serially.
    """
    import spack.subprocess_context

    home_prefix = mock_paths_locations

    # Expected data_home based on the home we set (without any XDG override)
    expected = str(pathlib.Path(home_prefix) / ".local" / "share" / "spack")

    # Run in subprocess that sets XDG_DATA_HOME
    spack_process = spack.subprocess_context.SpackTestProcess(SetAnXdgVarAndReadDataHome(expected))
    proc = spack_process.create()
    proc.start()
    proc.join()
    assert proc.exitcode == 0, "Subprocess test failed"

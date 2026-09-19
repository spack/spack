# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for layout detection and config variable resolution."""

import os
import pathlib
from pathlib import Path

import pytest

import spack.config
import spack.paths
import spack.util.spack_yaml as syaml


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
    assert any("XDG_CACHE_HOME" in str(x) for x in locations_cache), (
        "locations:cache should include XDG_CACHE_HOME entry"
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

        import spack.config

        # Resolve $data_home - it should use the frozen value from the parent
        # process, not the XDG_DATA_HOME we just set
        actual = spack.config.substitute_path_variables("$data_home")

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


def test_user_cache_path_is_default_when_env_var_is_empty(
    working_env, mock_spack_instance, monkeypatch
):
    import spack.config

    home_dir, base_prefix = mock_spack_instance

    # Create fresh config after mock_spack_instance sets up paths
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    assert os.path.join(home_dir, ".local", "state", "spack") == spack.paths.user_cache_path


@pytest.mark.parametrize(
    "env_var", ["SPACK_STATE_HOME", "SPACK_USER_CACHE_PATH", "XDG_STATE_HOME"]
)
def test_user_cache_path_is_overridable(working_env, mock_spack_instance, monkeypatch, env_var):
    home_dir, base_prefix = mock_spack_instance
    p = str(Path("some") / "path")

    # For XDG_STATE_HOME, append /spack since that's the convention
    if env_var == "XDG_STATE_HOME":
        os.environ[env_var] = p
        expected = os.path.join(p, "spack")
    else:
        os.environ[env_var] = p
        expected = p

    # Create fresh SpackPaths instance after setting env var
    from spack.paths import SpackPaths

    fresh_paths = SpackPaths(_prefix=base_prefix)
    monkeypatch.setattr(spack.paths, "locations", fresh_paths)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    assert spack.paths.user_cache_path == expected


def test_substitute_user_cache(mock_spack_instance):
    assert os.path.join(spack.paths.user_cache_path, "baz") == spack.config.canonicalize_path(
        os.path.join("$user_cache_path", "baz")
    )


def test_auto_migration_copies_user_config(mock_spack_instance, monkeypatch):
    """Auto-migration copies configuration from ~/.spack to ~/.config/spack."""
    home_dir, base_prefix = mock_spack_instance
    old_config = pathlib.Path(home_dir) / ".spack"
    old_config.mkdir()
    (old_config / "config.yaml").write_text("config:\n  build_jobs: 3\n", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate(is_isolate_command=False)

    new_config = pathlib.Path(home_dir) / ".config" / "spack" / "config.yaml"
    assert new_config.read_text(encoding="utf-8") == "config:\n  build_jobs: 3\n"


def test_config_path_migration_applies_all_path_rewrite_rules(tmp_path):
    """Config migration applies the four path-handling scenarios.

    Absolute paths outside ``include:`` remain unchanged, absolute paths inside
    ``include:`` are rewritten, relative paths outside ``include:`` become
    absolute, and relative paths inside ``include:`` remain relative.
    """
    old_config_dir = tmp_path / ".spack"
    new_config_dir = tmp_path / ".config" / "spack"
    old_config_dir.mkdir(parents=True)

    absolute_included = old_config_dir / "included-absolute"
    absolute_included.mkdir()
    relative_included = old_config_dir / "included-relative.yaml"
    relative_included.write_text("packages: {}\n", encoding="utf-8")
    absolute_external = tmp_path / "external"
    absolute_external.mkdir()
    relative_local = old_config_dir / "local.yaml"
    relative_local.write_text("config: {}\n", encoding="utf-8")

    config_path = old_config_dir / "config.yaml"
    config_path.write_text(
        syaml.dump(
            {
                "config": {
                    # Absolute paths outside include sections are unchanged.
                    "source_cache": str(absolute_external),
                    # Relative paths outside include sections become absolute.
                    "repos": "local.yaml",
                },
                "include": [
                    # Absolute paths under the old config root are rewritten.
                    {"path": str(absolute_included)},
                    # Relative include paths remain relative.
                    {"path": "included-relative.yaml"},
                ],
            }
        ),
        encoding="utf-8",
    )

    migrated, _ = spack.config.process_config_file_paths(
        str(config_path), str(old_config_dir), str(new_config_dir)
    )

    assert migrated is not None
    assert migrated["config"]["source_cache"] == str(absolute_external)
    assert migrated["config"]["repos"] == str(relative_local)
    assert migrated["include"][0]["path"] == str(new_config_dir / "included-absolute")
    assert migrated["include"][1]["path"] == "included-relative.yaml"


def test_auto_migration_gpg_failure_records_old_path(mock_spack_instance, monkeypatch, capsys):
    """A GPG destination collision keeps the old path in generated config."""
    home_dir, base_prefix = mock_spack_instance
    old_gpg = pathlib.Path(base_prefix) / "opt" / "spack" / "gpg"
    old_gpg.mkdir(parents=True)
    (old_gpg / "private-keys-v1.d").mkdir()
    (old_gpg / "private-keys-v1.d" / "key.key").write_text("key", encoding="utf-8")

    data_home = pathlib.Path(home_dir) / ".local" / "share" / "spack"
    destination = data_home / "gpg"
    destination.mkdir(parents=True)
    (destination / "existing-key").write_text("existing", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate(is_isolate_command=False)

    layout_config = pathlib.Path(spack.config._layout_scope_path()) / "config.yaml"
    assert str(old_gpg) in layout_config.read_text(encoding="utf-8")
    assert (old_gpg / "private-keys-v1.d" / "key.key").exists()
    assert (destination / "existing-key").exists()
    assert "GPG data (kept in its old location)" in capsys.readouterr().err


def test_auto_migration_moves_licenses_and_environments_to_shared_data(
    mock_spack_instance, monkeypatch, capsys
):
    """Successful migration copies resources before backing up their sources."""
    home_dir, base_prefix = mock_spack_instance
    old_licenses = pathlib.Path(base_prefix) / "etc" / "spack" / "licenses"
    old_licenses.mkdir(parents=True)
    (old_licenses / "license.dat").write_text("license", encoding="utf-8")
    old_env = pathlib.Path(base_prefix) / "var" / "spack" / "environments" / "demo"
    old_env.mkdir(parents=True)
    (old_env / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate(is_isolate_command=False)

    data_home = pathlib.Path(home_dir) / ".local" / "share" / "spack"
    assert (data_home / "licenses" / "license.dat").read_text(encoding="utf-8") == "license"
    assert (data_home / "environments" / "demo" / "spack.yaml").exists()
    backup = pathlib.Path(base_prefix) / ".migration-backup"
    assert (backup / "licenses" / "license.dat").exists()
    assert (backup / "environments" / "demo" / "spack.yaml").exists()
    assert not (old_licenses / "license.dat").exists()
    assert not old_env.exists()
    assert "spack migrate undo" in capsys.readouterr().err


def test_auto_migration_collision_preserves_source_and_destination(
    mock_spack_instance, monkeypatch
):
    """A license collision leaves the old resource usable and records its path."""
    home_dir, base_prefix = mock_spack_instance
    old_licenses = pathlib.Path(base_prefix) / "etc" / "spack" / "licenses"
    old_licenses.mkdir(parents=True)
    (old_licenses / "license.dat").write_text("old", encoding="utf-8")
    data_home = pathlib.Path(home_dir) / ".local" / "share" / "spack"
    destination = data_home / "licenses"
    destination.mkdir(parents=True)
    (destination / "license.dat").write_text("new", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate(is_isolate_command=False)

    assert (old_licenses / "license.dat").read_text(encoding="utf-8") == "old"
    assert (destination / "license.dat").read_text(encoding="utf-8") == "new"
    layout = pathlib.Path(spack.config._layout_scope_path()) / "config.yaml"
    assert str(old_licenses) in layout.read_text(encoding="utf-8")
    assert not (
        pathlib.Path(base_prefix) / ".migration-backup" / "licenses" / "license.dat"
    ).exists()


def test_auto_migration_is_not_repeated_after_layout_scope(mock_spack_instance, monkeypatch):
    """A completed layout scope prevents a later startup from migrating again.

    Fresh instances do not need a generated layout scope: auto-migration is
    bypassed when no old resources are detected.
    """
    home_dir, base_prefix = mock_spack_instance
    old_licenses = pathlib.Path(base_prefix) / "etc" / "spack" / "licenses"
    old_licenses.mkdir(parents=True)
    (old_licenses / "license.dat").write_text("license", encoding="utf-8")
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    spack.config._do_migrate(is_isolate_command=False)
    assert not spack.config._should_auto_migrate()
    backup = pathlib.Path(base_prefix) / ".migration-backup" / "licenses" / "license.dat"
    backup_mtime = backup.stat().st_mtime_ns

    spack.config._do_migrate(is_isolate_command=False)
    assert backup.stat().st_mtime_ns == backup_mtime

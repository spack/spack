# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for layout detection and config variable resolution."""

import os
import pathlib
import shutil
import sys
from pathlib import Path

import pytest

import spack.config
import spack.paths
import spack.util.spack_yaml as syaml


def test_config_defaults_use_data_home(mock_spack_instance, monkeypatch):
    """Test that config defaults reference $data_home for various paths."""
    home_dir, base_prefix = mock_spack_instance

    # Create a fresh configuration and install it globally
    cfg = spack.config.create()
    monkeypatch.setattr(spack.config, "CONFIG", cfg)

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


def test_data_home_resolves_to_mock_home(mock_spack_instance, monkeypatch):
    """Test that $data_home resolves to the correct directory under mock home."""
    home_dir, base_prefix = mock_spack_instance

    # Create fresh config after mock_spack_instance sets up paths
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    # Resolve $data_home - should point to mock home, not real home
    resolved_data_home = spack.config.canonicalize_path("$data_home")
    expected_data_home = os.path.join(home_dir, ".local", "share", "spack")

    assert resolved_data_home == expected_data_home, (
        f"$data_home should resolve to subdirectory of mock home.\n"
        f"Expected: {expected_data_home}\n"
        f"Got: {resolved_data_home}"
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
    result = spack.config._do_migrate_home()

    # Check if migration happened
    assert result["user_config"] is True, "User config migration should have succeeded"

    new_config = pathlib.Path(home_dir) / ".config" / "spack" / "config.yaml"
    assert new_config.exists(), f"New config should exist at {new_config}"
    assert new_config.read_text(encoding="utf-8") == "config:\n  build_jobs: 3\n"


def test_config_path_migration_applies_all_path_rewrite_rules(tmp_path):
    """Config migration applies the four path-handling scenarios.

    Absolute paths outside ``include:`` remain unchanged, absolute paths inside
    ``include:`` are rewritten, relative paths outside ``include:`` become
    absolute, and relative paths inside ``include:`` remain relative if they
    point inside the config directory, or become absolute if they point outside.
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

    # Relative include that points outside the config dir
    shared_cfg = tmp_path / "shared-cfg"
    shared_cfg.mkdir()

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
                    # Relative include paths pointing inside stay relative.
                    {"path": "included-relative.yaml"},
                    # Relative include paths pointing outside become absolute.
                    {"path": "../shared-cfg"},
                ],
            }
        ),
        encoding="utf-8",
    )

    migrated = spack.config.process_config_file_paths(
        str(config_path), str(old_config_dir), str(new_config_dir)
    )

    assert migrated is not None
    assert migrated["config"]["source_cache"] == str(absolute_external)
    assert migrated["config"]["repos"] == str(relative_local)
    assert migrated["include"][0]["path"] == str(new_config_dir / "included-absolute")
    assert migrated["include"][1]["path"] == "included-relative.yaml"
    assert migrated["include"][2]["path"] == str(shared_cfg)


def test_env_path_migration_applies_all_path_rewrite_rules(tmp_path):
    """Environment migration applies the four path-handling scenarios.

    1. Absolute path inside old env: rewrite to new env location
    2. Relative path pointing outside env: make absolute (preserve target)
    3. Relative path staying inside env: keep relative (works in new location)
    4. Absolute path outside env: unchanged
    """
    old_envs = tmp_path / "old_envs"
    new_envs = tmp_path / "new_envs"
    old_envs.mkdir()
    new_envs.mkdir()

    old_env = old_envs / "myenv"
    old_env.mkdir()

    # Create test paths
    local_file = old_env / "local.yaml"
    local_file.write_text("packages: {}\n", encoding="utf-8")

    subdir = old_env / "subdir"
    subdir.mkdir()
    subdir_file = subdir / "nested.yaml"
    subdir_file.write_text("config: {}\n", encoding="utf-8")

    # Shared config outside the environment
    shared_cfg = old_envs / "shared.yaml"
    shared_cfg.write_text("packages: {}\n", encoding="utf-8")

    external_dir = tmp_path / "external"
    external_dir.mkdir()

    # Create spack.yaml with all path scenarios
    spack_yaml = old_env / "spack.yaml"
    spack_yaml.write_text(
        syaml.dump(
            {
                "spack": {
                    "specs": ["zlib"],
                    "config": {
                        # Rule 1: Absolute path inside env → rewrite to new location
                        "source_cache": str(local_file),
                        # Rule 4: Absolute path outside env → unchanged
                        "misc_cache": str(external_dir),
                    },
                    "include": [
                        # Rule 2: Relative path pointing outside env → make absolute
                        "../shared.yaml",
                        # Rule 3: Relative path inside env → keep relative
                        "local.yaml",
                    ],
                }
            }
        ),
        encoding="utf-8",
    )

    # Copy to staging (simulating what _migrate_environments does)
    staging = new_envs / ".spack-env-myenv-staging"
    shutil.copytree(old_env, staging)

    # Process the file (this is what happens during migration)
    staging_yaml = staging / "spack.yaml"
    migrated = spack.config.process_env_file_paths(str(staging_yaml), str(old_env), str(staging))

    assert migrated is not None

    # Rule 1: Absolute path inside old env gets rewritten to new location
    assert migrated["spack"]["config"]["source_cache"] == str(staging / "local.yaml")

    # Rule 4: Absolute path outside env stays unchanged
    assert migrated["spack"]["config"]["misc_cache"] == str(external_dir)

    # Rule 2: Relative path outside env becomes absolute (preserves original target)
    assert migrated["spack"]["include"][0] == str(shared_cfg)

    # Rule 3: Relative path inside env stays relative
    assert migrated["spack"]["include"][1] == "local.yaml"


@pytest.mark.parametrize("conflict", ["environments", "gpg"])
def test_auto_migration_old_spack_internal_resources(mock_spack_instance, monkeypatch, conflict):
    """Test migration of resources previously stored in ``$spack``.

    Migration is component-wise: configuration points to old locations for
    components that fail to migrate and to new locations for successful
    migrations.
    """
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    old_envs = pathlib.Path(spack.paths.old_envs_path)
    old_env = old_envs / "foo"
    old_env.mkdir(parents=True)
    (old_env / "old.yaml").write_text("old: environment\n", encoding="utf-8")

    old_gpg = pathlib.Path(spack.paths.old_gpg_path)
    old_gpg.mkdir(parents=True)
    (old_gpg / "old-keyring-file").write_text("old", encoding="utf-8")
    old_gpg_keys = pathlib.Path(spack.paths.old_gpg_keys_path)
    old_gpg_keys.mkdir(parents=True)
    (old_gpg_keys / "old-public-key").write_text("old", encoding="utf-8")

    data_home = pathlib.Path(spack.config.canonicalize_path("$data_home"))
    new_envs = data_home / "environments"
    new_env = new_envs / "foo"
    new_gpg = data_home / "gpg"
    new_gpg_keys = data_home / "gpg-keys"

    if conflict == "environments":
        new_env.mkdir(parents=True)
        (new_env / "new.yaml").write_text("new: environment\n", encoding="utf-8")
    else:
        new_gpg.mkdir(parents=True)
        (new_gpg / "new-keyring-file").write_text("new", encoding="utf-8")

    spack.config._do_migrate_spack_prefix()
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    config = spack.config.CONFIG
    if conflict == "environments":
        assert (new_env / "new.yaml").read_text(encoding="utf-8") == "new: environment\n"
        assert not (new_env / "old.yaml").exists()
        assert spack.config.canonicalize_path(config.get("config:environments_root")) == str(
            old_envs
        )

        assert (new_gpg / "old-keyring-file").read_text(encoding="utf-8") == "old"
        assert (new_gpg_keys / "old-public-key").read_text(encoding="utf-8") == "old"
        assert spack.config.canonicalize_path(config.get("config:gpg_path")) == str(new_gpg)
        assert spack.config.canonicalize_path(config.get("config:gpg_keys_path")) == str(
            new_gpg_keys
        )
    else:
        assert (new_gpg / "new-keyring-file").read_text(encoding="utf-8") == "new"
        assert not (new_gpg / "old-keyring-file").exists()
        assert not new_gpg_keys.exists()
        assert spack.config.canonicalize_path(config.get("config:gpg_path")) == str(old_gpg)
        assert spack.config.canonicalize_path(config.get("config:gpg_keys_path")) == str(
            old_gpg_keys
        )

        assert (new_env / "old.yaml").read_text(encoding="utf-8") == "old: environment\n"
        assert spack.config.canonicalize_path(config.get("config:environments_root")) == str(
            new_envs
        )


def test_auto_migration_copies_package_repositories(mock_spack_instance, monkeypatch):
    """Automatic migration recursively copies the legacy package repository tree."""
    home_dir, _ = mock_spack_instance
    old_repos = pathlib.Path(home_dir) / ".spack" / "package_repos"
    (old_repos / "first" / "nested").mkdir(parents=True)
    (old_repos / "first" / "root.txt").write_text("first root", encoding="utf-8")
    (old_repos / "first" / "nested" / "nested.txt").write_text("nested", encoding="utf-8")
    (old_repos / "second").mkdir()
    (old_repos / "second" / "root.txt").write_text("second root", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate_home()

    new_repos = pathlib.Path(spack.paths.package_repos_path)
    assert (new_repos / "first" / "root.txt").read_text(encoding="utf-8") == "first root"
    assert (new_repos / "first" / "nested" / "nested.txt").read_text(encoding="utf-8") == (
        "nested"
    )
    assert (new_repos / "second" / "root.txt").read_text(encoding="utf-8") == "second root"
    assert (old_repos / "first" / "root.txt").exists()
    assert (old_repos / "second" / "root.txt").exists()
    if sys.platform != "win32":
        assert (new_repos.parent / ".spack-package-repos-migration-lock").exists()
    assert not (new_repos.parent / ".package-repos-migration").exists()


def test_auto_migration_skips_existing_package_repository_destination(
    mock_spack_instance, monkeypatch
):
    """An existing package repository destination is never overwritten."""
    home_dir, _ = mock_spack_instance
    old_repo = pathlib.Path(home_dir) / ".spack" / "package_repos" / "abc1234"
    old_repo.mkdir(parents=True)
    (old_repo / "source").write_text("old", encoding="utf-8")

    (old_repo.parent / "second").mkdir()

    new_repos = pathlib.Path(spack.paths.package_repos_path)
    new_repo = new_repos / "abc1234"
    new_repo.mkdir(parents=True)
    (new_repo / "source").write_text("new", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate_home()

    assert (new_repo / "source").read_text(encoding="utf-8") == "new"
    assert not (new_repos / "second").exists()
    assert (old_repo / "source").read_text(encoding="utf-8") == "old"


def test_config_migration_skips_unparseable_yaml(mock_spack_instance, monkeypatch):
    """Test that config migration skips YAML files that can't be parsed."""
    home_dir, base_prefix = mock_spack_instance
    old_config = pathlib.Path(home_dir) / ".spack"
    old_config.mkdir(parents=True, exist_ok=True)

    # Create a valid config file
    (old_config / "packages.yaml").write_text(
        "packages:\n  all:\n    target: [x86_64]\n", encoding="utf-8"
    )

    # Create an unparseable YAML file (like in a backup directory)
    backup_dir = old_config / "backup"
    backup_dir.mkdir()
    (backup_dir / "broken.yaml").write_text("packages: [unclosed\n", encoding="utf-8")

    # Migration should succeed, skipping the broken file
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    result = spack.config._do_migrate_home()

    # Should have migrated successfully (skipping the broken file)
    assert result["user_config"] is True

    # Valid config should be migrated
    new_config = pathlib.Path(home_dir) / ".config" / "spack"
    assert (new_config / "packages.yaml").exists()

    # Broken file should not be migrated
    assert not (new_config / "backup" / "broken.yaml").exists()


def test_migrated_environments_accessible(mock_spack_instance, monkeypatch):
    """Test that migrated environments are accessible via spack env list."""
    import spack.environment.environment as ev

    home_dir, base_prefix = mock_spack_instance
    old_envs = pathlib.Path(spack.paths.old_envs_path)
    old_envs.mkdir(parents=True)

    # Create old environments with spack.yaml files
    # test-env-1 has a shared config file
    env1_dir = old_envs / "test-env-1"
    env1_dir.mkdir()
    (env1_dir / "common.yaml").write_text(
        "packages:\n  all:\n    compiler: [gcc]\n", encoding="utf-8"
    )
    (env1_dir / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    # test-env-2 includes from test-env-1 with both relative and absolute paths
    env2_dir = old_envs / "test-env-2"
    env2_dir.mkdir()
    abs_include = str(env1_dir / "common.yaml")
    (env2_dir / "spack.yaml").write_text(
        f"spack:\n  specs: []\n  include:\n  - ../test-env-1/common.yaml\n  - {abs_include}\n",
        encoding="utf-8",
    )

    # Create fresh config and run migration
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate_spack_prefix()

    # Reload config to pick up layout scope (which may point to old environments_root if conflict)
    # or the default new location
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    # spack env list should find the environments in the new location
    env_names = ev.all_environment_names()
    assert "test-env-1" in env_names
    assert "test-env-2" in env_names

    # Verify they're in the new location (copied, old location still exists)
    new_envs = pathlib.Path(spack.config.canonicalize_path("$data_home")) / "environments"
    assert (new_envs / "test-env-1" / "spack.yaml").exists()
    assert (new_envs / "test-env-2" / "spack.yaml").exists()

    # Old location still exists (migration copies, doesn't move)
    assert old_envs.exists()
    assert (old_envs / "test-env-1" / "spack.yaml").exists()

    # Verify sibling environment references were rewritten to new location
    env2_yaml = new_envs / "test-env-2" / "spack.yaml"
    with open(env2_yaml, "r", encoding="utf-8") as f:
        env2_data = syaml.load(f)

    # Both relative and absolute includes should point to new location of test-env-1
    expected_include = str(new_envs / "test-env-1" / "common.yaml")
    assert env2_data["spack"]["include"][0] == expected_include  # was relative
    assert env2_data["spack"]["include"][1] == expected_include  # was absolute


def test_auto_migration_with_no_old_resources(mock_spack_instance, monkeypatch):
    """When no old resources exist in $spack, migration doesn't touch the spack prefix.

    Verifies that:
    - No files are written to $spack when no old resources exist
    - No locks are attempted in $spack (not even temporarily)
    - .migration-done marker is NOT created
    - _do_migrate_home is still called to check $HOME
    - No layout scope is created
    """
    import spack.util.lock

    home_dir, base_prefix = mock_spack_instance

    # Don't create any old resources - this is a fresh instance
    # No old licenses, no old envs, no old gpg, no old installs

    # Track what files exist in spack prefix before migration
    spack_prefix = pathlib.Path(base_prefix)
    files_before = set()
    for item in spack_prefix.rglob("*"):
        if item.is_file():
            files_before.add(item)

    # Track if locks were attempted
    lock_attempts = []
    original_lock = spack.util.lock.Lock

    class TrackingLock:
        def __init__(self, path, *args, **kwargs):
            lock_attempts.append(path)
            self._inner = original_lock(path, *args, **kwargs)

        def acquire_write(self):
            return self._inner.acquire_write()

        def release_write(self):
            return self._inner.release_write()

    monkeypatch.setattr(spack.util.lock, "Lock", TrackingLock)

    home_migrate_called = []
    original_migrate_home = spack.config._do_migrate_home

    def track_home_migrate():
        home_migrate_called.append(True)
        return original_migrate_home()

    monkeypatch.setattr(spack.config, "_do_migrate_home", track_home_migrate)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    spack.config._perform_auto_migration_at_module_load()

    assert home_migrate_called, "_do_migrate_home should be called even with no old resources"

    files_after = set()
    for item in spack_prefix.rglob("*"):
        if item.is_file():
            files_after.add(item)

    # Verify no new files were written to spack prefix (this includes the layout
    # scope, as well as .migration-done).
    new_files = files_after - files_before
    assert not new_files, (
        f"No files should be written to spack prefix when no old resources exist.\n"
        f"New files: {[str(f.relative_to(spack_prefix)) for f in new_files]}"
    )

    # Verify no locks were attempted in spack prefix
    spack_lock_attempts = [p for p in lock_attempts if str(spack_prefix) in str(p)]
    assert not spack_lock_attempts, (
        f"No locks should be attempted in spack prefix when no old resources exist.\n"
        f"Lock attempts: {spack_lock_attempts}"
    )


def test_migrate_with_staging_skips_occupied_destination(tmp_path, monkeypatch):
    """An occupied destination is not modified or locked."""
    import spack.util.lock

    old_path = tmp_path / "old"
    old_path.mkdir()
    (old_path / "old-file").write_text("old", encoding="utf-8")

    new_path = tmp_path / "new"
    new_path.mkdir()
    existing = new_path / "existing-file"
    existing.write_text("new", encoding="utf-8")

    def unexpected_lock(*args, **kwargs):
        raise AssertionError("migration should not create a lock for an occupied destination")

    def unexpected_staging(*args, **kwargs):
        raise AssertionError("migration should not stage files for an occupied destination")

    monkeypatch.setattr(spack.util.lock, "Lock", unexpected_lock)

    result = spack.config._migrate_with_staging(
        old_path=str(old_path),
        new_path=str(new_path),
        prepare_staging_callback=unexpected_staging,
        lock_name=".test-lock",
        staging_name=".test-staging",
        description="test resource",
    )

    assert not result
    assert existing.read_text(encoding="utf-8") == "new"
    assert set(new_path.iterdir()) == {existing}


def test_layout_scope_fallback_for_old_installs(mock_spack_instance, monkeypatch):
    """When old installs exist, layout scope retains install_tree at old location.

    Verifies that auto-migration creates a layout scope pointing install_tree:root
    to the old location when installs are detected.
    """
    home_dir, base_prefix = mock_spack_instance

    # Create old install directory with content
    old_installs = pathlib.Path(base_prefix) / "opt" / "spack"
    old_installs.mkdir(parents=True, exist_ok=True)
    (old_installs / "dummy-package").mkdir()
    (old_installs / "dummy-package" / ".spack").mkdir()
    (old_installs / "dummy-package" / ".spack" / "spec.json").write_text(
        '{"name": "dummy"}', encoding="utf-8"
    )

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    # Trigger migration
    spack.config._perform_auto_migration_at_module_load()

    # Reload config to pick up layout scope
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    # Verify install_tree:root points to old location via config.get
    install_tree_root = spack.config.CONFIG.get("config:install_tree:root")
    resolved = spack.config.canonicalize_path(install_tree_root)
    expected = str(old_installs)
    assert resolved == expected, (
        f"install_tree:root should point to old installs location.\n"
        f"Expected: {expected}\n"
        f"Got: {resolved}"
    )


def test_migrate_with_staging_handles_lock_permission_error(tmp_path, monkeypatch):
    """Test that _migrate_with_staging handles lock acquisition failures gracefully
    (reports a failed migration).
    """
    import spack.util.lock

    old_path = tmp_path / "old"
    old_path.mkdir()
    (old_path / "file.txt").write_text("content", encoding="utf-8")

    new_path = tmp_path / "new"

    # Mock Lock to raise PermissionError on acquire_write
    class MockLock:
        def __init__(self, *args, **kwargs):
            self.write_acquired = False

        def acquire_write(self):
            raise PermissionError("Cannot create lock file")

        def release_write(self):
            # This should not be called if acquire failed
            raise AssertionError("release_write should not be called when acquire failed")

    monkeypatch.setattr(spack.util.lock, "Lock", MockLock)

    def prepare_staging(old, staging, new):
        shutil.copytree(old, staging)

    # This should return False due to permission error, but not crash
    result = spack.config._migrate_with_staging(
        old_path=str(old_path),
        new_path=str(new_path),
        prepare_staging_callback=prepare_staging,
        lock_name=".test-lock",
        staging_name=".test-staging",
        description="test resource",
    )

    # Migration should fail gracefully
    assert result is False, "Migration should return False when lock acquisition fails"

    # New path should not have been created
    assert not new_path.exists(), "New path should not exist after failed migration"

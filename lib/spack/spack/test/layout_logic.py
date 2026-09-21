# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for layout detection and config variable resolution."""

import os
import pathlib
import sys
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


class MigrationResources:
    """Create and inspect the old resources used by migration tests."""

    def __init__(self, home_dir, base_prefix):
        self.base_prefix = pathlib.Path(base_prefix)
        # Calculate expected data_home directly from test paths (XDG default)
        # rather than using config which may still have old singleton state
        home_dir_path = pathlib.Path(home_dir)
        self.data_home = home_dir_path / ".local" / "share" / "spack"
        self.old_gpg = pathlib.Path(spack.paths.old_gpg_path)
        self.old_licenses = pathlib.Path(spack.paths.old_licenses_path)
        self.old_envs = pathlib.Path(spack.paths.old_envs_path)

        (self.old_gpg / "private-keys-v1.d").mkdir(parents=True)
        (self.old_gpg / "private-keys-v1.d" / "key").write_text("old", encoding="utf-8")
        self.old_licenses.mkdir(parents=True)
        for name in ("license-1", "license-2"):
            (self.old_licenses / name).write_text("old", encoding="utf-8")
        for name in ("env-1", "env-2"):
            env = self.old_envs / name
            env.mkdir(parents=True)
            (env / "spack.yaml").write_text("old", encoding="utf-8")
        view = self.old_envs / "env-1" / "view"
        view.mkdir()
        (view / ".spack-view").write_text("view", encoding="utf-8")
        (view / "should-not-copy").write_text("view", encoding="utf-8")

    @staticmethod
    def contains_text(root, text):
        """Check if text exists in root (file or directory of files)."""
        root = pathlib.Path(root)
        if root.is_file():
            return text in root.read_text(encoding="utf-8")
        return any(
            text in path.read_text(encoding="utf-8") for path in root.rglob("*") if path.is_file()
        )

    def assert_migrations(self, expected_migrations, conflicts):
        all_resources = {
            "gpg",
            "envs/env-1",
            "envs/env-2",
            "licenses/license-1",
            "licenses/license-2",
        }
        conflicts = set(conflicts)
        overrides = set(expected_migrations)
        expected_migrations = {resource for resource in all_resources if resource not in conflicts}
        if any(resource.startswith("envs/") for resource in conflicts):
            expected_migrations.difference_update(
                resource for resource in all_resources if resource.startswith("envs/")
            )
        if any(resource.startswith("licenses/") for resource in conflicts):
            expected_migrations.difference_update(
                resource for resource in all_resources if resource.startswith("licenses/")
            )
        expected_migrations.update(
            resource[1:] for resource in overrides if resource.startswith("+")
        )
        expected_migrations.difference_update(
            resource[1:] for resource in overrides if resource.startswith("-")
        )
        backup = self.base_prefix / ".migration-backup"
        for resource in (
            "gpg",
            "envs/env-1",
            "envs/env-2",
            "licenses/license-1",
            "licenses/license-2",
        ):
            migrated = resource in expected_migrations
            if resource == "gpg":
                destination = self.data_home / "gpg"
                source = self.old_gpg
                backup_path = backup / "gpg"
                marker = destination / "private-keys-v1.d" / "key"
            elif resource.startswith("envs/"):
                name = resource.split("/", 1)[1]
                destination = self.data_home / "environments" / name
                source = self.old_envs / name
                backup_path = backup / "environments" / name
                marker = destination / "spack.yaml"
            else:
                name = resource.split("/", 1)[1]
                destination = self.data_home / "licenses" / name
                source = self.old_licenses / name
                # License backup: individual file in backup directory
                backup_path = backup / "licenses" / name
                marker = destination

            if migrated:
                assert destination.exists()
                assert marker.read_text(encoding="utf-8") == "old"
                assert backup_path.exists()
                # For licenses, backup is a file - read directly
                # For GPG/envs, backup is a directory - check it contains "old"
                if resource.startswith("licenses/"):
                    assert backup_path.read_text(encoding="utf-8") == "old"
                else:
                    assert self.contains_text(backup_path, "old")
                assert not source.exists()
                if resource == "envs/env-1":
                    assert not (destination / "view").exists()
            else:
                assert source.exists()
                assert self.contains_text(source, "old")
                assert not backup_path.exists()

                # When not migrated due to conflicts (not custom config),
                # config should explicitly point to old location.
                # Check this only once per resource type to avoid redundant checks.
                if resource in conflicts:
                    if resource == "gpg":
                        config = spack.config.CONFIG
                        gpg_path = config.get("config:gpg_path")
                        assert str(self.old_gpg) == spack.config.canonicalize_path(gpg_path)
                    elif resource == "envs/env-1":
                        config = spack.config.CONFIG
                        envs_root = config.get("config:environments_root")
                        assert str(self.old_envs) == spack.config.canonicalize_path(envs_root)
                    elif resource == "licenses/license-1":
                        config = spack.config.CONFIG
                        license_dir = config.get("config:license_dir")
                        assert str(self.old_licenses) == spack.config.canonicalize_path(license_dir)

            if resource in conflicts:
                assert destination.exists()
                assert self.contains_text(destination, "new")
                assert not self.contains_text(destination, "old")

    def add_conflicts(self, conflicts):
        for resource in conflicts:
            if resource == "gpg":
                destination = self.data_home / "gpg"
                destination.mkdir(parents=True)
                (destination / "existing").write_text("new", encoding="utf-8")
            elif resource.startswith("envs/"):
                name = resource.split("/", 1)[1]
                destination = self.data_home / "environments" / name
                destination.mkdir(parents=True)
                (destination / "spack.yaml").write_text("new", encoding="utf-8")
            elif resource.startswith("licenses/"):
                name = resource.split("/", 1)[1]
                destination = self.data_home / "licenses"
                destination.mkdir(parents=True)
                (destination / name).write_text("new", encoding="utf-8")


@pytest.fixture
def migration_resources(mock_spack_instance):
    """Provide simulated old GPG, environment, and license resources."""
    return MigrationResources(*mock_spack_instance)


@pytest.mark.parametrize(
    "config_vars, conflicts, expected_migrations",
    [
        ((), (), ("gpg", "envs/env-1", "envs/env-2", "licenses/license-1", "licenses/license-2")),
        (
            (),
            ("gpg", "envs/env-1", "licenses/license-1"),
            ("-gpg", "-envs/env-1", "-licenses/license-1"),
        ),
        ((("config:gpg_path", "$spack/opt/spack/gpg"),), (), ("-gpg",)),
        (
            (("config:license_dir", "$spack/opt/licenses"),),
            (),
            ("-licenses/license-1", "-licenses/license-2"),
        ),
    ],
)
def test_auto_migration_old_spack_internal_resources(
    migration_resources, config_vars, conflicts, expected_migrations, mutable_config, monkeypatch
):
    """Migration handles GPG, environments, licenses, conflicts, and views."""
    resources = migration_resources
    resources.add_conflicts(conflicts)

    # Create fresh config after mock_spack_instance has set up test paths
    test_config = spack.config.create()
    for path, value in config_vars:
        test_config.set(path, value)
    monkeypatch.setattr(spack.config, "CONFIG", test_config)

    # Run migration which creates layout scope
    spack.config._do_migrate(is_isolate_command=False)

    # Reinitialize config to pick up newly created layout scope
    test_config = spack.config.create()
    monkeypatch.setattr(spack.config, "CONFIG", test_config)

    resources.assert_migrations(expected_migrations, conflicts)


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
    spack.config._do_migrate(is_isolate_command=False)

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
    spack.config._do_migrate(is_isolate_command=False)

    assert (new_repo / "source").read_text(encoding="utf-8") == "new"
    assert not (new_repos / "second").exists()
    assert (old_repo / "source").read_text(encoding="utf-8") == "old"


def test_auto_migration_skips_package_repositories_for_isolation(mock_spack_instance, monkeypatch):
    """Isolation leaves legacy package repositories in place."""
    home_dir, base_prefix = mock_spack_instance
    old_repos = pathlib.Path(home_dir) / ".spack" / "package_repos"
    old_repos.mkdir(parents=True)
    (old_repos / "abc1234" / "repo.yaml").parent.mkdir()
    (old_repos / "abc1234" / "repo.yaml").write_text("repo", encoding="utf-8")
    target = pathlib.Path(home_dir) / "isolated"
    config_path = target / "config.yaml"

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.config._do_migrate(
        is_isolate_command=True, config_path=str(config_path), isolate_target=str(target)
    )

    assert (old_repos / "abc1234" / "repo.yaml").exists()
    assert not (target / "package_repos").exists()


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

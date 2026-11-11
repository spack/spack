# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for layout detection and config variable resolution."""

import contextlib
import io
import os
import pathlib
import shutil
import sys

import pytest

import spack.config
import spack.error
import spack.migrate
import spack.paths
import spack.util.lang
import spack.util.lock
import spack.util.spack_yaml as syaml
from spack.util.filesystem import getuid


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

    This test patches the global spack.paths and must run serially.
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

    # Create fresh config after mock_spack_instance sets up paths. The autouse
    # mock_user_cache_path fixture patches user_cache_path(); bypass it to test the
    # real resolution.
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    assert os.path.join(home_dir, ".cache", "spack") == spack.config._resolve_location_var("cache")


@pytest.mark.parametrize(
    "env_var", ["SPACK_CACHE_HOME", "SPACK_USER_CACHE_PATH", "XDG_CACHE_HOME"]
)
def test_user_cache_path_is_overridable(working_env, mock_spack_instance, monkeypatch, env_var):
    home_dir, base_prefix = mock_spack_instance
    # Use absolute path - relative paths in config:locations are now rejected
    p = os.path.join(home_dir, "some", "path")

    # For XDG_CACHE_HOME, append /spack since that's the convention
    if env_var == "XDG_CACHE_HOME":
        os.environ[env_var] = p
        expected = os.path.join(p, "spack")
    else:
        os.environ[env_var] = p
        expected = p

    # Create fresh config after setting the env var. The autouse mock_user_cache_path
    # fixture patches user_cache_path(); bypass it to test the real resolution.
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    assert spack.config._resolve_location_var("cache") == expected


def test_substitute_user_cache(mock_spack_instance):
    assert os.path.join(spack.config.user_cache_path(), "baz") == spack.config.canonicalize_path(
        os.path.join("$user_cache_path", "baz")
    )


def test_migration_copies_user_config(mock_spack_instance, monkeypatch):
    """Migration copies configuration from ~/.spack to ~/.config/spack."""
    home_dir, base_prefix = mock_spack_instance
    old_config = pathlib.Path(home_dir) / ".spack"
    old_config.mkdir()
    (old_config / "config.yaml").write_text("config:\n  build_jobs: 3\n", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    result = spack.migrate.migrate_home()

    # Check if migration happened
    assert result["user_config"] is True, "User config migration should have succeeded"

    new_config = pathlib.Path(home_dir) / ".config" / "spack" / "config.yaml"
    assert new_config.exists(), f"New config should exist at {new_config}"
    assert new_config.read_text(encoding="utf-8") == "config:\n  build_jobs: 3\n"


def test_migration_skips_user_config_when_spack_user_config_path_set(
    mock_spack_instance, monkeypatch
):
    """Migration skips user config if SPACK_USER_CONFIG_PATH is set."""
    home_dir, base_prefix = mock_spack_instance
    old_config = pathlib.Path(home_dir) / ".spack"
    old_config.mkdir()
    (old_config / "config.yaml").write_text("config:\n  build_jobs: 3\n", encoding="utf-8")

    # Set SPACK_USER_CONFIG_PATH to indicate user has explicit override
    custom_path = pathlib.Path(home_dir) / "custom_config"
    custom_path.mkdir()
    monkeypatch.setenv("SPACK_USER_CONFIG_PATH", str(custom_path))

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    result = spack.migrate.migrate_home()

    # Migration should be skipped
    assert result["user_config"] is False, "User config migration should be skipped"

    # Default location should not have migrated files
    default_config = pathlib.Path(home_dir) / ".config" / "spack" / "config.yaml"
    assert not default_config.exists(), "Config should not be migrated to default location"

    # Custom path should remain empty (no migration)
    assert not list(custom_path.iterdir()), "Custom config path should remain empty"

    # Old config should still exist (not moved)
    assert (old_config / "config.yaml").exists(), "Old config should remain untouched"


def test_config_path_migration_relative_paths_in_known_keys(tmp_path):
    """Relative paths in the keys that name on-disk state (repos, mirrors, includes,
    environments_root, license_dir) are made absolute against the OLD config dir, because
    the data they name stays in ~/.spack. Every other string is left alone.
    """
    old = tmp_path / ".spack"
    new = tmp_path / ".config" / "spack"
    old.mkdir(parents=True)

    config_path = old / "config.yaml"
    config_path.write_text(
        syaml.dump(
            {
                "config": {
                    "environments_root": "envs",
                    "license_dir": "licenses",
                    # absolute path into ~/.spack that is NOT an old default: untouched
                    "source_cache": str(old / "my-sources"),
                    # not a path-valued key that we track, it's trivially regenerable
                    "misc_cache": "$cache_home/x",
                },
                "repos": {
                    "plain": "myrepo/spack_repo/plain",
                    "dest": {"git": "https://example.com/r.git", "destination": "clones/dest"},
                    "already_abs": str(tmp_path / "elsewhere" / "spack_repo" / "abs"),
                    "variable": "$spack/var/spack/repos/spack_repo/builtin_mock",
                },
                "mirrors": {
                    "relmir": "mirror",
                    "urlmir": "file://mirror2",  # a URL, not a relative path
                    "dictmir": {"fetch": "fetchmir", "push": {"url": "pushmir"}},
                    "remote": "https://mirror.example.com/",
                },
                "modules": {"default": {"tcl": {"projections": {"zlib": "../leafs/{name}"}}}},
                "include": [
                    "included-relative.yaml",
                    {"path": "../shared-cfg", "optional": True},
                    str(old / "abs-include.yaml"),
                ],
            }
        ),
        encoding="utf-8",
    )

    migrated = spack.migrate.process_config_file_paths(str(config_path), str(old), str(new))

    assert migrated is not None
    cfg = migrated["config"]
    assert cfg["environments_root"] == str(old / "envs")
    assert cfg["license_dir"] == str(old / "licenses")
    assert cfg["source_cache"] == str(old / "my-sources")
    assert cfg["misc_cache"] == "$cache_home/x"

    repos = migrated["repos"]
    assert repos["plain"] == str(old / "myrepo" / "spack_repo" / "plain")
    assert repos["dest"]["destination"] == str(old / "clones" / "dest")
    assert repos["already_abs"] == str(tmp_path / "elsewhere" / "spack_repo" / "abs")
    assert repos["variable"] == "$spack/var/spack/repos/spack_repo/builtin_mock"

    mirrors = migrated["mirrors"]
    assert mirrors["relmir"] == str(old / "mirror")
    assert mirrors["urlmir"] == "file://mirror2"
    assert mirrors["dictmir"]["fetch"] == str(old / "fetchmir")
    assert mirrors["dictmir"]["push"]["url"] == str(old / "pushmir")
    assert mirrors["remote"] == "https://mirror.example.com/"

    # a projection is not a path
    assert migrated["modules"]["default"]["tcl"]["projections"]["zlib"] == "../leafs/{name}"

    inc = migrated["include"]
    assert inc[0] == str(old / "included-relative.yaml")
    assert inc[1]["path"] == str((tmp_path / "shared-cfg").resolve()) or inc[1]["path"] == str(
        tmp_path / "shared-cfg"
    )
    assert inc[1]["optional"] is True
    assert inc[2] == str(old / "abs-include.yaml")


def test_config_migration_copies_only_yaml(mock_spack_instance, capsys):
    """Only configuration files are copied from ~/.spack; data the user keeps there (install
    trees, repos, mirrors, caches, and anything uncopyable) stays where it is and is
    reached through the rewritten references."""
    home_dir, _ = mock_spack_instance
    old = pathlib.Path(home_dir) / ".spack"
    old.mkdir()
    (old / "config.yaml").write_text(
        "config:\n  environments_root: envs\n  install_tree:\n    root: store\n", encoding="utf-8"
    )
    (old / "repos.yaml").write_text("repos:\n  mine: myrepo\n", encoding="utf-8")
    # nested config in a platform dir
    (old / "linux").mkdir()
    (old / "linux" / "packages.yaml").write_text("packages: {}\n", encoding="utf-8")
    # data of every kind that must NOT be copied
    (old / "store" / ".spack-db").mkdir(parents=True)
    (old / "store" / ".spack-db" / "index.json").write_text("{}", encoding="utf-8")
    (old / "myrepo" / "packages").mkdir(parents=True)
    (old / "myrepo" / "repo.yaml").write_text("repo:\n  namespace: mine\n", encoding="utf-8")
    (old / "envs" / "e1").mkdir(parents=True)
    (old / "envs" / "e1" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    (old / "srccache").mkdir()
    (old / "srccache" / "big.tar.gz").write_bytes(b"\0" * 4096)
    (old / "README").write_text("notes\n", encoding="utf-8")
    # the directories Spack itself wrote into ~/.spack hold YAML of their own (an installed
    # Python package, a staged source tree, a not-YAML "*.yaml") and links; none is config
    pkg = old / "bootstrap" / "store" / "linux" / "clingo-1.0-abc" / "lib"
    (pkg / "site").mkdir(parents=True)
    (pkg / "site" / "cfg.yaml").write_text("a: 1\n", encoding="utf-8")
    (pkg.parent / "lib64").symlink_to("lib")
    src = old / "stage" / "spack-stage-foo-1.0-abc" / "spack-src"
    (src / ".github").mkdir(parents=True)
    (src / ".github" / "ci.yml").write_text("on: push\n", encoding="utf-8")
    (src / "environment.yaml").write_text("- not: [valid\n", encoding="utf-8")
    for data_dir in ("cache", "git_repos", "package_repos", "reports", "test"):
        (old / data_dir / "x").mkdir(parents=True)
        (old / data_dir / "x" / "index.yaml").write_text("b: 2\n", encoding="utf-8")
    (old / "dangling").symlink_to(old / "nowhere")
    # Make sure a read-only directory doesn't error
    ro = old / "ro"
    ro.mkdir()
    (ro / "f").write_text("x", encoding="utf-8")
    ro.chmod(0o555)
    # a directory alias stays a link, so it keeps tracking v2
    (old / "v2").mkdir()
    (old / "v2" / "x.yaml").write_text("config: {}\n", encoding="utf-8")
    (old / "current").symlink_to("v2")
    # a yaml that is a link outside the config dir stays a link to that content
    outside_dir = pathlib.Path(home_dir) / "other" / "spack"
    outside_dir.mkdir(parents=True)
    (outside_dir / "mirrors.yaml").write_text("mirrors: {}\n", encoding="utf-8")
    (old / "mirrors.yaml").symlink_to("../other/spack/mirrors.yaml")
    # a directory link into dotfiles, relative: must be made absolute to still resolve
    (old / "shared").symlink_to("../other/spack")
    # an absolute link into ~/.spack itself: still valid, left alone
    (old / "alias.yaml").symlink_to(old / "config.yaml")

    try:
        result = spack.migrate.migrate_home()
    finally:
        ro.chmod(0o755)

    assert result["user_config"] is True
    new = pathlib.Path(spack.migrate.migration_config_home())
    regular = sorted(
        str(p.relative_to(new)) for p in new.rglob("*") if p.is_file() and not p.is_symlink()
    )
    assert regular == ["config.yaml", "linux/packages.yaml", "repos.yaml", "v2/x.yaml"]
    assert not list(new.parent.glob(".spack-*"))  # lock and staging are gone
    links = {str(p.relative_to(new)): os.readlink(p) for p in new.rglob("*") if p.is_symlink()}
    assert links == {
        # relative, stays inside: verbatim
        "current": "v2",
        # relative, leaves ~/.spack: made absolute so it still resolves
        "mirrors.yaml": str(outside_dir / "mirrors.yaml"),
        "shared": str(outside_dir),
        # absolute into ~/.spack: left alone, the target is still there
        "alias.yaml": str(old / "config.yaml"),
    }
    for link in links:
        assert (new / link).exists(), f"{link} dangles"
    # editing the linked-to file is seen through the link: it is live, not a copy
    (outside_dir / "mirrors.yaml").write_text("mirrors:\n  m: file:///x\n", encoding="utf-8")
    assert "file:///x" in (new / "mirrors.yaml").read_text(encoding="utf-8")
    # the references point back at ~/.spack
    cfg = syaml.load((new / "config.yaml").read_text(encoding="utf-8"))
    assert cfg["config"]["environments_root"] == str(old / "envs")
    assert cfg["config"]["install_tree"]["root"] == "store"  # not a relative-path key: untouched
    repos = syaml.load((new / "repos.yaml").read_text(encoding="utf-8"))
    assert repos["repos"]["mine"] == str(old / "myrepo")
    # nothing about uncopyable data was warned, since none of it was attempted
    assert "Not copying" not in capsys.readouterr().err


def test_config_path_migration_rewrites_old_defaults(tmp_path):
    """An absolute path that spells out the Spack 1.2 default for its own config key (e.g.
    ``bootstrap:root: ~/.spack/bootstrap``, as written by ``spack bootstrap root --set``) is
    rewritten to that key's new default. The same path under any other key, or any other
    path under ~/.spack, moves with the config like everything else that was copied.
    """
    old = tmp_path / "dot-spack"
    new = tmp_path / "config-spack"
    old.mkdir()
    new.mkdir()

    config_path = new / "config.yaml"
    config_path.write_text(
        syaml.dump(
            {
                "bootstrap": {"root": str(old / "bootstrap")},
                "config": {
                    "misc_cache": str(old / "cache"),
                    "test_stage": str(old / "test"),
                    "build_stage": ["$tempdir/$user/spack-stage", str(old / "stage")],
                    # the same directories under keys they are NOT the default for
                    "source_cache": str(old / "cache"),
                    "template_dirs": [str(old / "bootstrap"), str(old / "stage" / "sub")],
                    # a sub-path of a default is not the default
                    "extensions": [str(old / "bootstrap" / "store")],
                },
            }
        ),
        encoding="utf-8",
    )

    migrated = spack.migrate.process_config_file_paths(str(config_path), str(old), str(new))

    assert migrated is not None
    # old default for its own key -> new default
    assert migrated["bootstrap"]["root"] == "$state_home/bootstrap"
    assert migrated["config"]["misc_cache"] == "$cache_home/$spack_instance_id/cache"
    assert migrated["config"]["test_stage"] == "$state_home/test-stage"
    assert migrated["config"]["build_stage"][1] == "$state_home/stage"
    # same directory under a different key -> a user choice, left alone (~/.spack is retained)
    assert migrated["config"]["source_cache"] == str(old / "cache")
    assert migrated["config"]["template_dirs"][0] == str(old / "bootstrap")
    assert migrated["config"]["template_dirs"][1] == str(old / "stage" / "sub")
    # sub-path of a default -> also left alone
    assert migrated["config"]["extensions"][0] == str(old / "bootstrap" / "store")
    # variable-form values are not touched
    assert migrated["config"]["build_stage"][0] == "$tempdir/$user/spack-stage"


@pytest.mark.parametrize(
    "instance_dir,expected_is_default",
    [
        ("y6pldc2", True),
        ("abc2345", True),
        ("toolong1", False),
        ("UPPER22", False),
        ("y6pldc", False),
    ],
)
def test_config_path_migration_instance_misc_cache(tmp_path, instance_dir, expected_is_default):
    """``~/.spack/<spack_instance_id>/cache`` (the paths.py fallback for misc_cache) counts as
    the old default only when the directory name is a 7-character base32 instance id."""
    old = tmp_path / "dot-spack"
    new = tmp_path / "config-spack"
    old.mkdir()
    new.mkdir()
    config_path = new / "config.yaml"
    config_path.write_text(
        syaml.dump({"config": {"misc_cache": str(old / instance_dir / "cache")}}), encoding="utf-8"
    )

    migrated = spack.migrate.process_config_file_paths(str(config_path), str(old), str(new))

    if expected_is_default:
        assert migrated is not None
        assert migrated["config"]["misc_cache"] == "$cache_home/$spack_instance_id/cache"
    else:
        # not a default: a user choice into ~/.spack, left alone -> nothing to rewrite
        assert migrated is None


def test_config_path_migration_override_key(tmp_path):
    """``key::`` override syntax is still recognised as the same config key."""
    old = tmp_path / "dot-spack"
    new = tmp_path / "config-spack"
    old.mkdir()
    new.mkdir()
    config_path = new / "config.yaml"
    config_path.write_text(f"config:\n  misc_cache:: {old}/cache\n", encoding="utf-8")

    migrated = spack.migrate.process_config_file_paths(str(config_path), str(old), str(new))

    assert migrated is not None
    assert migrated["config"]["misc_cache:"] == "$cache_home/$spack_instance_id/cache"


def test_env_path_migration_applies_all_path_rewrite_rules(tmp_path):
    """Environment migration applies the path-handling scenarios.

    1. Absolute path inside old env: rewrite to new env location
    2. Relative path staying inside env: keep relative (works in new location)
    3. Absolute path outside env and outside envs root: unchanged
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
                        # Rule 3: Absolute path outside env and envs root → unchanged
                        "misc_cache": str(external_dir),
                    },
                    "include": [
                        # Rule 2: Relative path inside env → keep relative
                        "local.yaml"
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
    migrated = spack.migrate.process_env_file_paths(str(staging_yaml), str(old_env), str(staging))

    assert migrated is not None

    # Rule 1: Absolute path inside old env gets rewritten to new location
    assert migrated["spack"]["config"]["source_cache"] == str(staging / "local.yaml")

    # Rule 3: Absolute path outside env and envs root stays unchanged
    assert migrated["spack"]["config"]["misc_cache"] == str(external_dir)

    # Rule 2: Relative path inside env stays relative
    assert migrated["spack"]["include"][0] == "local.yaml"


@pytest.mark.parametrize(
    "path_factory,expected_error",
    [
        (lambda old_envs: "../shared.yaml", "relative path.*outside the environment"),
        (lambda old_envs: "./../shared.yaml", "relative path.*outside the environment"),
        (lambda old_envs: "sub/../../shared.yaml", "relative path.*outside the environment"),
        (
            lambda old_envs: str(old_envs / "sibling/config.yaml"),
            "absolute path.*sibling location.*environments root",
        ),
        (
            lambda old_envs: "$env/../shared.yaml",
            r"contains \$env/\.\. which would reference outside",
        ),
        (
            lambda old_envs: "${env}/../shared.yaml",
            r"contains \$env/\.\. which would reference outside",
        ),
        (
            lambda old_envs: "$env/sub/../../shared.yaml",
            r"contains \$env/\.\. which would reference outside",
        ),
        (
            lambda old_envs: "$env//../shared.yaml",
            r"contains \$env/\.\. which would reference outside",
        ),
    ],
)
def test_env_migration_blocks_external_references(tmp_path, path_factory, expected_error):
    """Environment migration blocks if there are external path references."""
    old_envs = tmp_path / "old_envs"
    old_envs.mkdir()
    old_env = old_envs / "myenv"
    old_env.mkdir()

    include_path = path_factory(old_envs)

    spack_yaml = old_env / "spack.yaml"
    spack_yaml.write_text(
        syaml.dump({"spack": {"specs": ["zlib"], "include": [include_path]}}), encoding="utf-8"
    )

    staging = tmp_path / "staging"
    shutil.copytree(old_env, staging)

    with pytest.raises(spack.error.SpackError, match=expected_error):
        spack.migrate.process_env_file_paths(
            str(staging / "spack.yaml"),
            str(old_env),
            str(staging),
            str(old_envs),
            tmp_path / "new",
        )


@pytest.mark.parametrize(
    "path", ["$env/sub/../shared.yaml", "${env}/a/b/../../c.yaml", "$env/./x.yaml", "$env"]
)
def test_env_migration_allows_env_relative_paths_that_stay_inside(path):
    """``..`` under ``$env`` is fine as long as it never climbs above the environment."""
    spack.migrate._check_for_escaping_env_variables({"spack": {"include": [path]}}, "spack.yaml")


def test_env_migration_resolves_relative_paths_from_the_included_file(tmp_path):
    """``conf/main.yaml`` including ``../extra.yaml`` stays inside the env and is kept; the
    same spelling climbing above the env is refused. Absolute paths into the env are rewritten
    to the final destination, not the staging directory the file is read from."""
    old_envs = tmp_path / "old"
    new_envs = tmp_path / "new"
    for name, main_include in (("site", "../extra.yaml"), ("bad", "../../shared.yaml")):
        env = old_envs / name
        (env / "conf").mkdir(parents=True)
        (env / "spack.yaml").write_text(
            f"spack:\n  specs: []\n  include: [conf/main.yaml, {env / 'conf' / 'abs.yaml'}]\n",
            encoding="utf-8",
        )
        (env / "conf" / "main.yaml").write_text(f"include: [{main_include}]\n", encoding="utf-8")
        (env / "conf" / "abs.yaml").write_text("config: {}\n", encoding="utf-8")
        (env / "extra.yaml").write_text("config: {}\n", encoding="utf-8")

    ok, _ = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    assert not ok  # "bad" blocks

    shutil.rmtree(old_envs / "bad")
    ok, _ = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    assert ok
    site = new_envs / "site"
    assert (site / "conf" / "main.yaml").read_text(
        encoding="utf-8"
    ) == "include: [../extra.yaml]\n"
    assert str(site / "conf" / "abs.yaml") in (site / "spack.yaml").read_text(encoding="utf-8")
    assert "staging" not in (site / "spack.yaml").read_text(encoding="utf-8")


@pytest.mark.not_on_windows("permission bits do not apply on Windows")
@pytest.mark.skipif(getuid() == 0, reason="root ignores permission bits")
def test_migrate_with_staging_warns_when_lock_cannot_be_created(tmp_path, capsys):
    """An unwritable destination parent fails the lock; the user is told, the resource is
    retained, and nothing is raised for the prefix-migration handler to misreport."""
    old = tmp_path / "old"
    old.mkdir()
    (old / "file").write_text("x", encoding="utf-8")
    parent = tmp_path / "ro"
    parent.mkdir()
    parent.chmod(0o500)
    try:
        result = spack.migrate.migrate_with_staging(
            old_path=str(old),
            new_path=str(parent / "new"),
            prepare_staging_callback=lambda o, s, n: shutil.copytree(o, s),
            lock_name=".test-lock",
            staging_name=".test-staging",
            description="test resource",
            verify_destination_callback=spack.migrate.can_migrate_to_location,
        )
    finally:
        parent.chmod(0o700)

    assert result is False
    assert f"Cannot migrate test resource to {parent / 'new'}" in capsys.readouterr().err


@pytest.mark.not_on_windows("permission bits do not apply on Windows")
@pytest.mark.skipif(getuid() == 0, reason="root ignores permission bits")
def test_env_migration_unwritable_data_home_is_retained_not_fatal(tmp_path, capsys):
    """A read-only environments destination is reported for what it is and the environments
    are retained, instead of surfacing as a "spack prefix is not writable" error."""
    old_envs = tmp_path / "old"
    (old_envs / "e").mkdir(parents=True)
    (old_envs / "e" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    new_envs = tmp_path / "new"
    new_envs.mkdir()
    new_envs.chmod(0o500)
    try:
        ok, _ = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    finally:
        new_envs.chmod(0o700)

    assert not ok
    assert f"Cannot migrate environments to {new_envs}" in capsys.readouterr().err


#: Managed environments may be nested (``team/proj``); a nested one must migrate exactly like
#: a top-level one, so the environment tests run both ways.
nested = pytest.mark.parametrize("nested", ["", "team"], ids=["top-level", "nested"])


@pytest.mark.not_on_windows("permission bits do not apply on Windows")
@pytest.mark.skipif(getuid() == 0, reason="root ignores permission bits")
@nested
def test_env_migration_rollback_removes_read_only_copies(tmp_path, nested):
    """When one environment blocks migration, copies already made are removed even if they
    contain read-only directories (copied permissions), and so is the failed staging dir.
    A leftover without a marker would otherwise block every later attempt."""
    old_envs = tmp_path / "old" / nested
    new_envs = tmp_path / "new"
    good = old_envs / "a"
    (good / "ro").mkdir(parents=True)
    (good / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    (good / "ro" / "x.yaml").write_text("config: {}\n", encoding="utf-8")
    (good / "ro").chmod(0o500)
    bad = old_envs / "b"
    (bad / "ro").mkdir(parents=True)
    (bad / "spack.yaml").write_text(
        "spack:\n  specs: []\n  include: [../../shared.yaml]\n", encoding="utf-8"
    )
    (bad / "ro").chmod(0o500)
    try:
        ok, _ = spack.migrate._migrate_environments(str(tmp_path / "old"), str(new_envs))
    finally:
        (good / "ro").chmod(0o700)
        (bad / "ro").chmod(0o700)

    assert not ok
    # nothing is left, not even the parent of a rolled-back nested environment
    assert [p.name for p in new_envs.iterdir() if p.name != ".lock"] == []


def test_env_migration_rewrites_paths_spelled_through_a_symlinked_prefix(tmp_path):
    """``~/spack -> /clone``: an include written as ``~/spack/var/.../own/jobs.yaml`` is
    inside the env being moved and must be rewritten; the same spelling into a sibling env
    is refused."""
    clone = tmp_path / "clone"
    link = tmp_path / "spack-link"
    old_envs = clone / "var" / "spack" / "environments"
    old_envs.mkdir(parents=True)
    link.symlink_to(clone)
    linked_envs = link / "var" / "spack" / "environments"
    for name, target in (("own", "own"), ("sib", "own")):
        (old_envs / name).mkdir()
        (old_envs / name / "jobs.yaml").write_text("config:\n  build_jobs: 7\n", encoding="utf-8")
        (old_envs / name / "spack.yaml").write_text(
            f"spack:\n  specs: []\n  include: [{linked_envs / target / 'jobs.yaml'}]\n",
            encoding="utf-8",
        )
    new_envs = tmp_path / "new"

    ok, _ = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    assert not ok  # sib refers into own

    shutil.rmtree(old_envs / "sib")
    ok, _ = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    assert ok
    manifest = (new_envs / "own" / "spack.yaml").read_text(encoding="utf-8")
    assert str(new_envs / "own" / "jobs.yaml") in manifest
    assert "spack-link" not in manifest


def test_env_migration_copies_unparseable_yaml_verbatim(tmp_path):
    """A ``*.yaml`` file that is not YAML (a Jinja template, say) is not Spack config; it
    is copied as it is and does not block the environment."""
    old_envs = tmp_path / "old"
    env = old_envs / "myenv"
    env.mkdir(parents=True)
    (env / "spack.yaml").write_text("spack:\n  specs: [zlib]\n", encoding="utf-8")
    template = "{% if gpu %}\nspack:\n  specs: [cuda]\n{% endif %}\n"
    (env / "template.yaml").write_text(template, encoding="utf-8")

    ok, _ = spack.migrate._migrate_environments(str(old_envs), str(tmp_path / "new"))

    assert ok
    assert (tmp_path / "new" / "myenv" / "template.yaml").read_text(encoding="utf-8") == template


def test_env_migration_keeps_relative_paths_that_stay_inside(tmp_path):
    """A relative path with ``..`` that resolves inside the env is neither refused nor
    rewritten (rule 2), while a non-path string containing ``..`` is left alone."""
    old_env = tmp_path / "old" / "myenv"
    (old_env / "sub").mkdir(parents=True)
    (old_env / "spack.yaml").write_text(
        syaml.dump({"spack": {"specs": ["zlib"], "include": ["sub/../local.yaml"]}}),
        encoding="utf-8",
    )
    staging = tmp_path / "staging"
    shutil.copytree(old_env, staging)
    result = spack.migrate.process_env_file_paths(
        str(staging / "spack.yaml"),
        str(old_env),
        str(staging),
        str(old_env.parent),
        tmp_path / "new",
    )
    assert result is None


@pytest.mark.parametrize("conflict", ["environments", "gpg"])
def test_migration_old_spack_internal_resources(mock_spack_instance, monkeypatch, conflict):
    """Test migration of resources previously stored in ``$spack``.

    Migration is component-wise: configuration points to old locations for
    components that fail to migrate and to new locations for successful
    migrations.
    """
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    old_envs = pathlib.Path(spack.paths.old_envs_path)
    for name in ("bar", "foo"):
        old_env = old_envs / name
        old_env.mkdir(parents=True)
        (old_env / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
        (old_env / "old.yaml").write_text("old: environment\n", encoding="utf-8")

    old_gpg = pathlib.Path(spack.paths.old_gpg_path)
    old_gpg.mkdir(parents=True)
    (old_gpg / "old-keyring-file").write_text("old", encoding="utf-8")
    old_gpg_keys = pathlib.Path(spack.paths.old_gpg_keys_path)
    old_gpg_keys.mkdir(parents=True)
    (old_gpg_keys / "old-public-key").write_text("old", encoding="utf-8")

    data_home = pathlib.Path(spack.config.canonicalize_path("$data_home"))
    new_envs = data_home / "environments"
    conflicting_env = new_envs / "foo"
    free_env = new_envs / "bar"
    new_gpg = data_home / "gpg"
    new_gpg_keys = data_home / "gpg-keys"

    if conflict == "environments":
        conflicting_env.mkdir(parents=True)
        (conflicting_env / "new.yaml").write_text("new: environment\n", encoding="utf-8")
    else:
        new_gpg.mkdir(parents=True)
        (new_gpg / "new-keyring-file").write_text("new", encoding="utf-8")

    spack.migrate.migrate_spack_prefix(spack.migrate.detect_old_resources())
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    config = spack.config.CONFIG
    if conflict == "environments":
        assert (conflicting_env / "new.yaml").read_text(encoding="utf-8") == "new: environment\n"
        assert not (conflicting_env / "old.yaml").exists()
        assert not free_env.exists()
        assert spack.config.canonicalize_path(config.get("config:environments_root")) == str(
            old_envs
        )

        assert (new_gpg / "old-keyring-file").read_text(encoding="utf-8") == "old"
        assert (new_gpg_keys / "old-public-key").read_text(encoding="utf-8") == "old"
        assert not list(data_home.glob(".*gpg*"))  # locks and staging are gone
        assert spack.config.canonicalize_path(config.get("config:gpg_path")) == str(new_gpg)
        assert spack.config.canonicalize_path(config.get("config:gpg_keys_path")) == str(
            new_gpg_keys
        )
    else:
        assert (new_gpg / "new-keyring-file").read_text(encoding="utf-8") == "new"
        assert not (new_gpg / "old-keyring-file").exists()
        # the keys dir is migrated before the keyring; public keys left behind are harmless
        assert (new_gpg_keys / "old-public-key").read_text(encoding="utf-8") == "old"
        assert spack.config.canonicalize_path(config.get("config:gpg_path")) == str(old_gpg)
        assert spack.config.canonicalize_path(config.get("config:gpg_keys_path")) == str(
            old_gpg_keys
        )

        assert (conflicting_env / "old.yaml").read_text(encoding="utf-8") == "old: environment\n"
        assert (free_env / "old.yaml").read_text(encoding="utf-8") == "old: environment\n"
        assert spack.config.canonicalize_path(config.get("config:environments_root")) == str(
            new_envs
        )


@pytest.mark.skipif(sys.platform == "win32", reason="unix domain sockets")
def test_gpg_migration_skips_transient_files(tmp_path):
    """A live GnuPG home holds agent sockets, lock files, an RNG seed and keyring backups.
    Sockets cannot be copied and used to fail the whole migration; the rest must not be
    carried over (a stale lock would block gpg in the new home). Key material is copied,
    symlinks are preserved rather than followed.
    """
    import socket
    import tempfile

    # AF_UNIX socket paths are limited to ~100 bytes; pytest's tmp_path is too deep on macOS
    # (the same reason GnuPG has --create-socketdir), so put the GPG home somewhere short.
    old = pathlib.Path(tempfile.mkdtemp(prefix="gpg-")) / "gpg"
    old.mkdir()
    (old / "pubring.kbx").write_bytes(b"keyring")
    (old / "trustdb.gpg").write_bytes(b"trust")
    (old / "private-keys-v1.d").mkdir()
    (old / "private-keys-v1.d" / "deadbeef.key").write_bytes(b"secret")
    (old / "openpgp-revocs.d").mkdir()
    (old / "openpgp-revocs.d" / "deadbeef.rev").write_bytes(b"revoke")
    # transient
    (old / "pubring.kbx~").write_bytes(b"backup")
    (old / "random_seed").write_bytes(b"seed")
    (old / "pubring.kbx.lock").write_text("1234@host\n", encoding="utf-8")
    (old / "trustdb.gpg.lock").write_text("1234@host\n", encoding="utf-8")
    sockets = []
    for name in ("S.gpg-agent", "S.gpg-agent.extra", "S.dirmngr"):
        sock = socket.socket(socket.AF_UNIX)
        sock.bind(str(old / name))
        sockets.append(sock)
    # a symlinked keyring component must stay a symlink, not become a copy; a relative one
    # leaving the directory is made absolute so it still resolves from the new location
    shared = tmp_path / "shared-trustdb.gpg"
    shared.write_bytes(b"shared")
    (old / "trustdb-link.gpg").symlink_to(shared)
    (old / "trustdb-rel.gpg").symlink_to(os.path.relpath(shared, old))

    new = tmp_path / "new-gpg"
    try:
        migrated = spack.migrate.migrate_with_staging(
            old_path=str(old),
            new_path=str(new),
            prepare_staging_callback=spack.migrate._make_gpg_stager(".migration-test"),
            lock_name=".gpg-test.lock",
            staging_name=".gpg-test-staging",
            description="GPG home",
            verify_destination_callback=spack.migrate.can_migrate_to_location,
        )
    finally:
        for sock in sockets:
            sock.close()
        shutil.rmtree(old.parent, ignore_errors=True)

    assert migrated is True
    assert (new / "pubring.kbx").read_bytes() == b"keyring"
    assert (new / "trustdb.gpg").read_bytes() == b"trust"
    assert (new / "private-keys-v1.d" / "deadbeef.key").read_bytes() == b"secret"
    assert (new / "openpgp-revocs.d" / "deadbeef.rev").read_bytes() == b"revoke"
    assert (new / ".migration-test").exists()
    assert (new / "trustdb-link.gpg").is_symlink()
    assert (new / "trustdb-rel.gpg").is_symlink()
    assert (new / "trustdb-rel.gpg").read_bytes() == b"shared"
    assert os.stat(new).st_mode & 0o777 == 0o700

    for transient in (
        "pubring.kbx~",
        "random_seed",
        "pubring.kbx.lock",
        "trustdb.gpg.lock",
        "S.gpg-agent",
        "S.gpg-agent.extra",
        "S.dirmngr",
    ):
        assert not (new / transient).exists(), f"{transient} should not have been copied"


def test_migration_copies_package_repositories(mock_spack_instance, monkeypatch):
    """Migration recursively copies each legacy package repository clone."""
    home_dir, _ = mock_spack_instance
    old_repos = pathlib.Path(home_dir) / ".spack" / "package_repos"
    (old_repos / "first" / "nested").mkdir(parents=True)
    (old_repos / "first" / "root.txt").write_text("first root", encoding="utf-8")
    (old_repos / "first" / "nested" / "nested.txt").write_text("nested", encoding="utf-8")
    (old_repos / "second").mkdir()
    (old_repos / "second" / "root.txt").write_text("second root", encoding="utf-8")

    result = spack.migrate.migrate_home()

    assert result["package_repos"] is True
    new_repos = pathlib.Path(spack.migrate.migration_data_home()) / "package_repos"
    # ... and that is where a freshly built config will look for them
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    assert pathlib.Path(spack.config.package_repos_path()) == new_repos
    assert (new_repos / "first" / "root.txt").read_text(encoding="utf-8") == "first root"
    assert (new_repos / "first" / "nested" / "nested.txt").read_text(encoding="utf-8") == (
        "nested"
    )
    assert (new_repos / "second" / "root.txt").read_text(encoding="utf-8") == "second root"
    assert (old_repos / "first" / "root.txt").exists()
    assert (old_repos / "second" / "root.txt").exists()
    # neither the staging directories nor the lock are left behind
    assert not any(p.name.startswith(".") for p in new_repos.iterdir())

    # Second run: nothing left to copy, nothing reported as migrated
    assert spack.migrate.migrate_home()["package_repos"] is False


def test_migration_merges_package_repositories(mock_spack_instance, capsys):
    """Clones are keyed by the hash of their remote URL and the destination is shared by
    every Spack instance on the machine, so a destination that already holds some clones
    (from a fresh checkout, or another migration) must not block the rest: existing
    clones are left alone, missing ones are copied.
    """
    home_dir, _ = mock_spack_instance
    old_repos = pathlib.Path(home_dir) / ".spack" / "package_repos"
    old_present = old_repos / "abc1234"
    old_present.mkdir(parents=True)
    (old_present / "source").write_text("old", encoding="utf-8")
    old_missing = old_repos / "k7m2x3q"
    old_missing.mkdir()
    (old_missing / "source").write_text("site repo with local edits", encoding="utf-8")
    # a stray file in the old root is not a clone and is ignored
    (old_repos / "package-repository.lock").write_text("", encoding="utf-8")

    # migration resolves its destination from the environment, not from config
    new_repos = pathlib.Path(spack.migrate.migration_data_home()) / "package_repos"
    new_present = new_repos / "abc1234"
    new_present.mkdir(parents=True)
    (new_present / "source").write_text("new", encoding="utf-8")

    result = spack.migrate.migrate_home()

    assert result["package_repos"] is True
    # existing clone untouched
    assert (new_present / "source").read_text(encoding="utf-8") == "new"
    # missing clone copied
    assert (new_repos / "k7m2x3q" / "source").read_text(encoding="utf-8") == (
        "site repo with local edits"
    )
    assert not (new_repos / "package-repository.lock").exists()
    # old clones retained
    assert (old_present / "source").read_text(encoding="utf-8") == "old"
    # no warning: every clone is accounted for
    assert "could not be copied" not in capsys.readouterr().err


def test_migration_warns_about_package_repositories_it_cannot_copy(mock_spack_instance, capsys):
    """A clone that cannot be copied is named in a warning, with what the user can do
    about it, instead of being silently abandoned."""
    home_dir, _ = mock_spack_instance
    old_repos = pathlib.Path(home_dir) / ".spack" / "package_repos"
    old_repo = old_repos / "k7m2x3q"
    old_repo.mkdir(parents=True)
    (old_repo / "source").write_text("x", encoding="utf-8")

    new_repos = pathlib.Path(spack.migrate.migration_data_home()) / "package_repos"
    new_repos.mkdir(parents=True)
    # a file where the clone should go: the copy cannot proceed
    (new_repos / "k7m2x3q").write_text("in the way", encoding="utf-8")

    result = spack.migrate.migrate_home()

    assert result["package_repos"] is False
    err = capsys.readouterr().err
    assert "could not be copied" in err
    assert str(old_repo) in err
    assert "repos:<name>:destination" in err
    assert (new_repos / "k7m2x3q").read_text(encoding="utf-8") == "in the way"


@pytest.mark.parametrize("error", ["permission", "timeout"])
def test_migration_names_dot_spack_when_its_clone_lock_cannot_be_taken(
    mock_spack_instance, monkeypatch, capsys, ensure_debug, error
):
    """The clone lock an older Spack holds lives in ``~/.spack``; failing to take it must
    be reported as that, not as a problem with the destination, which is where
    migrate_with_staging keeps its own lock."""
    home_dir, _ = mock_spack_instance
    old_repos = pathlib.Path(home_dir) / ".spack" / "package_repos"
    (old_repos / "k7m2x3q").mkdir(parents=True)
    (old_repos / "k7m2x3q" / "source").write_text("x", encoding="utf-8")
    new_repos = pathlib.Path(spack.migrate.migration_data_home()) / "package_repos"

    def cannot_lock(self, *args, **kwargs):
        if error == "permission":
            raise spack.util.lock.LockPermissionError("no permission")
        raise spack.util.lock.LockTimeoutError(spack.util.lock.LockType.READ, "x", 1.0, 1)

    monkeypatch.setattr(spack.util.lock.ReadTransaction, "__enter__", cannot_lock)

    assert spack.migrate.migrate_home()["package_repos"] is False
    err = capsys.readouterr().err
    assert f"could not take the clone lock in {pathlib.Path(home_dir) / '.spack'}" in err
    assert "could not be copied" in err and str(old_repos / "k7m2x3q") in err
    assert not (new_repos / "k7m2x3q").exists()


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
    result = spack.migrate.migrate_home()

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
    env1_dir = old_envs / "test-env-1"
    env1_dir.mkdir()
    (env1_dir / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    # test-env-2 is a simple env with no external references
    env2_dir = old_envs / "test-env-2"
    env2_dir.mkdir()
    (env2_dir / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    # Create fresh config and run migration
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.migrate.migrate_spack_prefix(spack.migrate.detect_old_resources())

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


@nested
def test_env_migration_drops_old_layout_view_links(tmp_path, nested):
    """Views are not copied. Spack < 1.3 built a view rooted at ``<env>/<name>`` in the
    container ``<env>/._<name>/<hash>`` with an absolute symlink ``<env>/<name>`` to it. Link
    and container are left behind as a pair; anything else at the env root is kept.
    """
    old_envs = tmp_path / "old" / nested
    new_envs = tmp_path / "new" / nested

    def make_env(name, link_name=None, target=None, make_target=True):
        env = old_envs / name
        env.mkdir(parents=True)
        (env / "spack.yaml").write_text("spack:\n  specs: [zlib]\n", encoding="utf-8")
        if link_name:
            if os.path.isabs(target):
                target = str(env / target.lstrip(os.sep))
            if make_target:
                (env / target / "bin").mkdir(parents=True)
                (env / target / "bin" / "tool").write_text("x", encoding="utf-8")
            (env / link_name).symlink_to(target)
        return env

    def copied(name):
        return {p.name for p in (new_envs / name).iterdir() if not p.name.startswith(".migration")}

    make_env("default", "view", "/._view/abc123")  # view: <env>/view
    make_env("custom", "myview", "/._myview/abc123")  # view: {x: {root: <env>/myview}}
    make_env("relative", "view", "._view/abc123")
    make_env("dangling", "view", "/._view/abc123", make_target=False)
    (old_envs / "dangling" / "._view").mkdir()  # hash dir already removed, container remains
    # root-level link into something that merely starts with ._ is not a view
    make_env("other", "link", "._viewer")
    # a container with no partner link is not recognized, and is copied
    orphan = make_env("orphan")
    (orphan / "._view" / "abc123").mkdir(parents=True)

    ok, differing = spack.migrate._migrate_environments(
        str(tmp_path / "old"), str(tmp_path / "new")
    )

    assert ok and differing == []
    for name, link_name in (
        ("default", "view"),
        ("custom", "myview"),
        ("relative", "view"),
        ("dangling", "view"),
    ):
        assert copied(name) == {"spack.yaml"}, f"{name}: {copied(name)}"
        # the source is untouched
        assert (old_envs / name / link_name).is_symlink()
        assert (old_envs / name / f"._{link_name}").is_dir()
    assert copied("other") == {"spack.yaml", "link", "._viewer"}
    assert (new_envs / "other" / "link").is_symlink()
    assert copied("orphan") == {"spack.yaml", "._view"}


@nested
def test_remigration_keeps_previously_migrated_env_and_warns_if_manifests_differ(
    mock_spack_instance, capsys, nested
):
    """An environment that was already migrated from this prefix is not copied again.
    If its manifest in ``$spack`` now differs from the copy, the copy is kept, the user is
    told, and the environment is not reported as migrated.
    """
    old_root = pathlib.Path(spack.paths.old_envs_path)
    new_root = pathlib.Path(spack.migrate.migration_data_home()) / "environments"
    old_envs, new_envs = old_root / nested, new_root / nested
    for name in ("same", "changed", "abs-path"):
        (old_envs / name).mkdir(parents=True)
    (old_envs / "same" / "spack.yaml").write_text("spack:\n  specs: [zlib]\n", encoding="utf-8")
    (old_envs / "changed" / "spack.yaml").write_text(
        "spack:\n  specs: [zlib@1.2]\n", encoding="utf-8"
    )
    # an absolute path into the env itself is rewritten on copy; that must not count as a
    # difference
    (old_envs / "abs-path" / "spack.yaml").write_text(
        f"spack:\n  specs: [zlib]\n  view: {old_envs / 'abs-path' / 'myview'}\n", encoding="utf-8"
    )

    ok, differing = spack.migrate._migrate_environments(str(old_root), str(new_root))
    assert ok and differing == []
    assert (new_envs / "abs-path" / "spack.yaml").read_text(encoding="utf-8") == (
        f"spack:\n  specs: [zlib]\n  view: {new_envs / 'abs-path' / 'myview'}\n"
    )
    capsys.readouterr()

    # The $spack copy of one env changes (e.g. after `spack migrate undo`, or a re-clone)
    (old_envs / "changed" / "spack.yaml").write_text(
        "spack:\n  specs: [zlib@1.3]\n", encoding="utf-8"
    )
    # ... and the user edits the migrated copy of another; both count as "differ"
    (new_envs / "same" / "spack.yaml").write_text(
        "spack:\n  specs: [zlib, bzip2]\n", encoding="utf-8"
    )

    ok, differing = spack.migrate._migrate_environments(str(old_root), str(new_root))

    assert ok
    assert sorted(differing) == [os.path.join(nested, "changed"), os.path.join(nested, "same")]
    # copies are kept as they are
    assert (new_envs / "changed" / "spack.yaml").read_text(encoding="utf-8") == (
        "spack:\n  specs: [zlib@1.2]\n"
    )
    assert (new_envs / "same" / "spack.yaml").read_text(encoding="utf-8") == (
        "spack:\n  specs: [zlib, bzip2]\n"
    )
    err = capsys.readouterr().err
    for name in ("changed", "same"):
        assert f"Attempted to migrate environment {old_envs / name} to {new_envs / name}" in err
    assert "previously migrated and the environment manifests differ" in err
    assert "Manually transfer any changes" in err
    assert "abs-path" not in err


def test_remigration_summary_excludes_envs_with_differing_manifests(
    mock_spack_instance, monkeypatch, capsys
):
    old_envs = pathlib.Path(spack.paths.old_envs_path)
    (old_envs / "foo").mkdir(parents=True)
    (old_envs / "foo" / "spack.yaml").write_text("spack:\n  specs: [zlib]\n", encoding="utf-8")
    (old_envs / "bar").mkdir()
    (old_envs / "bar" / "spack.yaml").write_text("spack:\n  specs: [zlib]\n", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    spack.migrate.migrate_spack_prefix(spack.migrate.detect_old_resources())
    assert "Migrated: environments." in capsys.readouterr().err

    (old_envs / "foo" / "spack.yaml").write_text("spack:\n  specs: [zlib@2]\n", encoding="utf-8")
    spack.migrate.migrate_spack_prefix(spack.migrate.detect_old_resources())

    err = capsys.readouterr().err
    assert "Migrated: environments (except foo: previously migrated, manifests differ" in err


@pytest.mark.parametrize(
    "var,func",
    [
        ("SPACK_DATA_HOME", spack.migrate.migration_data_home),
        ("XDG_DATA_HOME", spack.migrate.migration_data_home),
        ("XDG_CONFIG_HOME", spack.migrate.migration_config_home),
    ],
)
def test_migration_home_vars_expand_tilde_and_reject_relative(monkeypatch, var, func):
    """``~`` in the XDG/SPACK home variables is expanded; a relative value is a hard error
    rather than a copy into the current working directory."""
    suffix = "" if var == "SPACK_DATA_HOME" else os.sep + "spack"
    monkeypatch.setenv(var, "~/mine")
    assert func() == os.path.join(os.path.expanduser("~"), "mine") + suffix

    monkeypatch.setenv(var, "relative/dir")
    with pytest.raises(SystemExit):
        func()


@contextlib.contextmanager
def _yielding(value):
    """Stand-in for ``open_controlling_terminal`` that yields ``value``
    (``contextlib.nullcontext`` needs Python 3.7)."""
    yield value


@pytest.mark.parametrize(
    "value,approved",
    [("1", True), ("true", True), ("TRUE", True), ("0", False), ("no", False), ("", False)],
)
def test_automigrate_yes_requires_a_true_value(monkeypatch, value, approved):
    """``SPACK_AUTOMIGRATE_YES=0`` must not approve."""
    monkeypatch.setenv("SPACK_AUTOMIGRATE_YES", value)
    monkeypatch.setattr(spack.util.lang, "open_controlling_terminal", lambda: _yielding(None))
    resources = {"environments": True, "gpg_keys": False, "licenses": False, "installs": False}
    assert spack.migrate._prompt_for_prefix_migration(resources, timeout=1) is approved


def test_prefix_migration_prompt_needs_controlling_terminal(monkeypatch):
    """Without a controlling terminal the prompt is skipped and migration declined, no
    matter what stdin/stderr are. With one, the question goes to the terminal, not stderr."""
    monkeypatch.delenv("SPACK_AUTOMIGRATE_YES", raising=False)
    resources = {"environments": True, "gpg_keys": False, "licenses": False, "installs": False}

    monkeypatch.setattr(spack.util.lang, "open_controlling_terminal", lambda: _yielding(None))
    assert spack.migrate._prompt_for_prefix_migration(resources, timeout=1) is False

    # nothing eligible: no terminal needed, no prompt
    installs_only = {"environments": False, "gpg_keys": False, "licenses": False, "installs": True}
    assert spack.migrate._prompt_for_prefix_migration(installs_only, timeout=1) is False

    terminal = io.StringIO()
    monkeypatch.setattr(spack.util.lang, "open_controlling_terminal", lambda: _yielding(terminal))
    monkeypatch.setattr(spack.util.lang, "readline_with_timeout", lambda *a, **kw: "y")
    assert spack.migrate._prompt_for_prefix_migration(resources, timeout=1) is True
    assert "legacy internal layout" in terminal.getvalue()

    monkeypatch.setattr(spack.util.lang, "readline_with_timeout", lambda *a, **kw: None)
    assert spack.migrate._prompt_for_prefix_migration(resources, timeout=1) is False
    assert "No response received" in terminal.getvalue()


def test_symlinked_resource_root_is_migrated_as_a_symlink(tmp_path):
    """A resource whose root is a symlink (licenses -> site store, an env -> a checkout) is
    migrated by re-creating the link: a copy would freeze the data. A second migration finds
    the link and counts the resource as migrated; a destination that is anything else is
    refused."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "intel.lic").write_text("site", encoding="utf-8")
    (site / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    # licenses; an empty destination directory is replaced by the link
    src = tmp_path / "licenses"
    src.symlink_to(site)
    dst = tmp_path / "new" / "licenses"
    dst.mkdir(parents=True)
    assert spack.migrate._migrate_licenses(str(src), str(dst))
    assert dst.is_symlink() and dst.resolve() == site.resolve()
    (site / "later.lic").write_text("x", encoding="utf-8")
    assert (dst / "later.lic").exists()
    # already in place: still migrated (e.g. `spack migrate use-new-layout` after `undo`)
    assert spack.migrate._migrate_licenses(str(src), str(dst))
    assert dst.is_symlink()

    # an environment, through migrate_with_staging and the marker verifier
    old_envs = tmp_path / "old-envs"
    old_envs.mkdir()
    (old_envs / "linked").symlink_to(site)
    new_envs = tmp_path / "new-envs"
    for _ in range(2):
        ok, differing = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
        assert ok and differing == []
        assert (new_envs / "linked").is_symlink()
        assert (new_envs / "linked").resolve() == site.resolve()

    # destination occupied by something that is not that link
    (tmp_path / "new" / "other").mkdir()
    (tmp_path / "new" / "other" / "x.lic").write_text("x", encoding="utf-8")
    assert not spack.migrate._migrate_licenses(str(src), str(tmp_path / "new" / "other"))
    assert not (tmp_path / "new" / "other").is_symlink()


@nested
def test_symlinked_env_into_the_envs_root_follows_its_target(tmp_path, nested):
    """``prod -> myenv`` among the environments is an alias for a sibling that is migrated
    too; the alias is re-created relative so it reads the migrated copy. A link to somewhere
    outside stays absolute. Both are recognized on a re-run. A link to something that is
    not an environment is not environment data and is left behind."""
    old_envs = tmp_path / "old" / nested
    new_envs = tmp_path / "new" / nested
    checkout = tmp_path / "checkout"
    for env in (old_envs / "myenv" / "sub", old_envs / "notes", checkout):
        env.mkdir(parents=True)
    for env in (old_envs / "myenv", old_envs / "myenv" / "sub", checkout):
        (env / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    (old_envs / "prod").symlink_to("myenv")
    (old_envs / "prod2").symlink_to(old_envs / "myenv")
    (old_envs / "deep").symlink_to(old_envs / "myenv" / "sub")
    (old_envs / "external").symlink_to(checkout)
    (old_envs / "junk").symlink_to("notes")
    (old_envs / "junk2").symlink_to(tmp_path)

    for _ in range(2):
        ok, differing = spack.migrate._migrate_environments(
            str(tmp_path / "old"), str(tmp_path / "new")
        )
        assert ok and differing == []

    assert os.readlink(new_envs / "prod") == "myenv"
    assert os.readlink(new_envs / "prod2") == "myenv"
    assert os.readlink(new_envs / "deep") == os.path.join("myenv", "sub")
    assert (new_envs / "deep").resolve() == (new_envs / "myenv" / "sub").resolve()
    assert os.path.isabs(os.readlink(new_envs / "external"))
    assert (new_envs / "external").resolve() == checkout.resolve()
    assert not (new_envs / "notes").exists()
    assert not (new_envs / "junk").is_symlink() and not (new_envs / "junk2").is_symlink()


def test_nested_env_discovery(tmp_path):
    """Only what applies to nested environments alone: a subtree with no manifest is not
    environment data, a link to an ancestor of an environment is an alias and follows it,
    and a destination that is already an environment above a nested one is refused."""
    old_envs = tmp_path / "old"
    new_envs = tmp_path / "new"
    (old_envs / "team" / "proj").mkdir(parents=True)
    (old_envs / "team" / "proj" / "spack.yaml").write_text(
        "spack:\n  specs: []\n", encoding="utf-8"
    )
    (old_envs / "junk" / "sub").mkdir(parents=True)
    (old_envs / "junk" / "sub" / "README").write_text("", encoding="utf-8")
    (old_envs / "all").symlink_to("team")

    assert spack.migrate._find_environments(str(old_envs)) == ["all", os.path.join("team", "proj")]

    ok, differing = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    assert ok and differing == []
    assert not (new_envs / "junk").exists()
    assert os.readlink(new_envs / "all") == "team"

    (new_envs / "team" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    shutil.rmtree(new_envs / "team" / "proj")
    ok, _ = spack.migrate._migrate_environments(str(old_envs), str(new_envs))
    assert not ok
    assert {p.name for p in (new_envs / "team").iterdir()} == {"spack.yaml"}


def test_symlinked_dot_spack_is_migrated_once_and_quietly_after(tmp_path, monkeypatch, capsys):
    """``~/.spack -> ~/dotfiles/spack``: the first run links ``~/.config/spack`` to the same
    place, says so, and lists any spelled-out Spack 1.2 defaults in the linked files without
    touching them; later runs find the link and say nothing. An empty ``~/.config/spack``
    (created by hand, or by a tool like stow) is replaced by the link rather than being
    reported as a permissions problem."""
    monkeypatch.setenv("HOME", str(tmp_path))
    for var in ("SPACK_CONFIG_HOME", "SPACK_USER_CONFIG_PATH", "SPACK_DISABLE_LOCAL_CONFIG"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)

    dotfiles = tmp_path / "dotfiles" / "spack"
    dotfiles.mkdir(parents=True)
    (dotfiles / "config.yaml").write_text("config:\n  build_jobs: 7\n", encoding="utf-8")
    (tmp_path / ".spack").symlink_to(dotfiles)
    new = tmp_path / ".config" / "spack"
    new.mkdir(parents=True)

    # a spelled-out Spack 1.2 default is reported, not rewritten: the file is the user's
    (dotfiles / "bootstrap.yaml").write_text(
        f"bootstrap:\n  root: {tmp_path / '.spack' / 'bootstrap'}\n", encoding="utf-8"
    )
    # a non-default path under ~/.spack, and a relative one, are not Spack's business
    (dotfiles / "repos.yaml").write_text(
        f"repos:\n  a: myrepo\n  b: {tmp_path / '.spack' / 'other'}\n", encoding="utf-8"
    )
    before = {p.name: p.read_text(encoding="utf-8") for p in dotfiles.iterdir()}

    assert spack.migrate._migrate_user_config() is True
    assert new.is_symlink() and new.resolve() == dotfiles.resolve()
    err = capsys.readouterr().err
    assert "bootstrap:root" in err and "$state_home/bootstrap" in err
    assert "repos" not in err
    assert {p.name: p.read_text(encoding="utf-8") for p in dotfiles.iterdir()} == before

    assert spack.migrate._migrate_user_config() is False
    assert capsys.readouterr().err == ""
    assert new.is_symlink()


def test_symlinked_dot_spack_leaves_populated_config_home_alone(tmp_path, monkeypatch, capsys):
    """``~/.spack -> ~/dotfiles/spack`` while ``~/.config/spack`` already holds files: the
    user has configuration in the new place, so nothing is linked and nothing is fatal, just
    as for a populated destination when ``~/.spack`` is a directory."""
    monkeypatch.setenv("HOME", str(tmp_path))
    for var in ("SPACK_CONFIG_HOME", "SPACK_USER_CONFIG_PATH", "SPACK_DISABLE_LOCAL_CONFIG"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)

    dotfiles = tmp_path / "dotfiles" / "spack"
    dotfiles.mkdir(parents=True)
    (dotfiles / "config.yaml").write_text("config:\n  build_jobs: 7\n", encoding="utf-8")
    (tmp_path / ".spack").symlink_to(dotfiles)
    new = tmp_path / ".config" / "spack"
    new.mkdir(parents=True)
    (new / "packages.yaml").write_text("packages: {}\n", encoding="utf-8")

    assert spack.migrate._migrate_user_config() is False
    assert capsys.readouterr().err == ""
    assert not new.is_symlink()
    assert sorted(p.name for p in new.iterdir()) == ["packages.yaml"]


def test_license_migration_recognizes_its_own_repointed_links(tmp_path):
    """An absolute symlink into the license dir is repointed into the new dir on copy; a
    later run must see that as the same link, not as a conflict, while a link to a
    different file is still one."""
    src = tmp_path / "licenses"
    dst = tmp_path / "new" / "licenses"
    (src / "intel").mkdir(parents=True)
    (src / "intel" / "license.lic").write_text("key", encoding="utf-8")
    (src / "current.lic").symlink_to(src / "intel" / "license.lic")

    assert spack.migrate._migrate_licenses(str(src), str(dst))
    assert (dst / "current.lic").resolve() == (dst / "intel" / "license.lic").resolve()
    assert spack.migrate._migrate_licenses(str(src), str(dst))  # re-run: same link
    assert spack.migrate._migrate_licenses(str(src), str(dst))

    (dst / "intel" / "other.lic").write_text("x", encoding="utf-8")
    (dst / "current.lic").unlink()
    (dst / "current.lic").symlink_to(dst / "intel" / "other.lic")
    assert not spack.migrate._migrate_licenses(str(src), str(dst))


def test_license_migration_compares_bytes_and_leaves_user_links_alone(tmp_path, capsys):
    """Existing destination entries are compared byte-for-byte and like-for-like (a file never
    matches a symlink), and a mismatch says what differs; links the user already had in the
    destination are not rewritten, while copied links leaving the license dir are made
    absolute."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "intel.lic").write_text("key", encoding="utf-8")
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    # byte difference that decode(errors="replace") would hide
    (src / "a.lic").write_bytes(b"key\xff")
    (dst / "a.lic").write_bytes(b"key\xfe")
    assert not spack.migrate._migrate_licenses(str(src), str(dst))
    err = capsys.readouterr().err
    assert f"a.lic already exists at {dst}" in err
    assert "both are files, but their contents differ" in err
    assert "spack migrate use-new-layout" in err
    (dst / "a.lic").write_bytes(b"key\xff")

    # same content, but a file in the source and a link in the destination
    (src / "b.lic").write_text("key", encoding="utf-8")
    (dst / "b.lic").symlink_to(site / "intel.lic")
    assert not spack.migrate._migrate_licenses(str(src), str(dst))
    assert "a file vs. a symlink" in capsys.readouterr().err
    (dst / "b.lic").unlink()

    (src / "out.lic").symlink_to(os.path.join("..", "site", "intel.lic"))
    (dst / "mine.lic").symlink_to(os.path.join("..", "site", "intel.lic"))
    assert spack.migrate._migrate_licenses(str(src), str(dst))
    assert os.readlink(dst / "mine.lic") == os.path.join("..", "site", "intel.lic")
    assert os.path.isabs(os.readlink(dst / "out.lic"))
    assert (dst / "b.lic").read_text(encoding="utf-8") == "key"


def test_gpg_migration_keys_dir_goes_before_the_keyring(tmp_path):
    """The keys directory (public keys) is migrated before the home (secret keys). If another
    instance owns the keys destination, nothing is published; if it owns the home
    destination, only public keys have been published, and a later run picks up where it
    left off."""
    old_home = tmp_path / "old" / "gpg"
    old_keys = tmp_path / "old" / "gpg-keys"
    old_home.mkdir(parents=True)
    old_keys.mkdir()
    (old_home / "pubring.kbx").write_bytes(b"secret")
    (old_keys / "key.pub").write_bytes(b"pub")
    new_home = tmp_path / "new" / "gpg"
    new_keys = tmp_path / "new" / "gpg-keys"
    args = (str(old_home), str(new_home), str(old_keys), str(new_keys))

    new_keys.mkdir(parents=True)
    (new_keys / ".migration-other").write_text("another instance\n", encoding="utf-8")
    assert not spack.migrate._migrate_gpg(*args)
    assert not new_home.exists()

    shutil.rmtree(new_keys)
    new_home.mkdir(parents=True)
    (new_home / ".migration-other").write_text("another instance\n", encoding="utf-8")
    assert not spack.migrate._migrate_gpg(*args)
    assert (new_keys / "key.pub").read_bytes() == b"pub"
    assert not (new_home / "pubring.kbx").exists()

    shutil.rmtree(new_home)
    assert spack.migrate._migrate_gpg(*args)
    assert (new_home / "pubring.kbx").read_bytes() == b"secret"
    assert spack.migrate._migrate_gpg(*args)  # idempotent


def test_detect_old_installs_ignores_the_database(mock_spack_instance):
    """Only installed prefixes make ``opt/spack`` an install tree. ``.spack-db/`` alone does
    not, whatever it holds: a read-only command on a fresh clone creates it, and
    ``uninstall --all`` leaves it behind with an index recording nothing."""
    _, base_prefix = mock_spack_instance
    db = pathlib.Path(base_prefix) / "opt" / "spack" / ".spack-db"
    db.mkdir(parents=True)
    (db / "lock").touch()
    (db / "index.json").write_text('{"database": {"installs": {"abc": {}}}}', encoding="utf-8")
    assert spack.migrate.detect_old_resources()["installs"] is False

    (db.parent / "zlib-1.3-abc").mkdir()
    assert spack.migrate.detect_old_resources()["installs"] is True

    pathlib.Path(spack.paths.old_envs_path).mkdir(parents=True)
    (pathlib.Path(spack.paths.old_envs_path) / ".lock").touch()  # likewise, the root lock
    assert spack.migrate.detect_old_resources()["environments"] is False


def test_migration_with_no_old_resources(mock_spack_instance, monkeypatch):
    """When no old resources exist in $spack, migration doesn't touch the spack prefix.

    Verifies that:
    - No files are written to $spack when no old resources exist
    - No locks are attempted in $spack (not even temporarily)
    - .migration-done marker is NOT created
    - migrate_home is still called to check $HOME
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
    original_migrate_home = spack.migrate.migrate_home

    def track_home_migrate():
        home_migrate_called.append(True)
        return original_migrate_home()

    monkeypatch.setattr(spack.migrate, "migrate_home", track_home_migrate)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    spack.migrate.perform_migration()

    assert home_migrate_called, "migrate_home should be called even with no old resources"

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

    result = spack.migrate.migrate_with_staging(
        old_path=str(old_path),
        new_path=str(new_path),
        prepare_staging_callback=unexpected_staging,
        lock_name=".test-lock",
        staging_name=".test-staging",
        description="test resource",
        verify_destination_callback=spack.migrate.can_migrate_to_location,
    )

    assert not result
    assert existing.read_text(encoding="utf-8") == "new"
    assert set(new_path.iterdir()) == {existing}


def test_layout_scope_fallback_for_old_installs(mock_spack_instance, monkeypatch):
    """When old installs exist, layout scope retains install_tree at old location.

    Verifies that migration creates a layout scope pointing install_tree:root
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
    spack.migrate.perform_migration()

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
    """Test that migrate_with_staging handles lock acquisition failures gracefully
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
    result = spack.migrate.migrate_with_staging(
        old_path=str(old_path),
        new_path=str(new_path),
        prepare_staging_callback=prepare_staging,
        lock_name=".test-lock",
        staging_name=".test-staging",
        description="test resource",
        verify_destination_callback=spack.migrate.can_migrate_to_location,
    )

    # Migration should fail gracefully
    assert result is False, "Migration should return False when lock acquisition fails"

    # New path should not have been created
    assert not new_path.exists(), "New path should not exist after failed migration"

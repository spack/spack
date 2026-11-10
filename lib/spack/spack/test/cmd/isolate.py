# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from pathlib import Path

import pytest

import spack
import spack.config
import spack.main
import spack.migrate
import spack.paths

sp_isolate = spack.main.SpackCommand("isolate")
sp_config = spack.main.SpackCommand("config")


@pytest.fixture
def isolate_paths(mock_spack_instance):
    """Provide common path setup for isolate tests."""
    home_dir, base_prefix = mock_spack_instance
    base_prefix = Path(base_prefix)
    etc_spack = base_prefix / "etc" / "spack"
    isolate_scope_path = etc_spack / "isolate"
    return home_dir, base_prefix, etc_spack, isolate_scope_path


@pytest.mark.parametrize("use_self", [False, True])
def test_isolate_user_overrides_layout(isolate_paths, tmp_path, use_self):
    """User scope in isolation should have higher priority than layout scope.

    This is like test_isolate_added_config but this test simulates a pre-existing
    layout scope.
    """
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    # Create a layout scope with a config value
    layout_dir = etc_spack / "layout"
    layout_dir.mkdir()
    (layout_dir / "config.yaml").write_text(
        "config:\n  install_tree:\n    root: /from-layout-scope\n", encoding="utf-8"
    )
    layout_config = layout_dir / "config.yaml"

    if use_self:
        sp_isolate("--self")
        user_config = isolate_scope_path / "user" / "config.yaml"
    else:
        isolated_path = tmp_path / "test-isolation"
        sp_isolate("--path", str(isolated_path))
        user_config = isolated_path / "config.yaml"

    # Reload config to pick up the isolate scope
    spack.config.CONFIG = spack.config.create()

    # Record initial contents
    initial_layout_content = layout_config.read_text(encoding="utf-8")
    initial_user_content = (
        user_config.read_text(encoding="utf-8") if user_config.exists() else None
    )

    # Use spack config add to set a value (should go to user scope)
    sp_config("add", "config:install_tree:root:/from-config-add")

    # Assert that user_config changed and layout_config didn't
    final_user_content = user_config.read_text(encoding="utf-8")
    assert final_user_content != initial_user_content, "user config should have changed"
    assert "/from-config-add" in final_user_content, "new value should be in user config"

    final_layout_content = layout_config.read_text(encoding="utf-8")
    assert final_layout_content == initial_layout_content, "layout config should not have changed"

    # Assert that config API retrieves the value we set (user overrides layout)
    # Need to reload config to pick up the change made by config add
    spack.config.CONFIG = spack.config.create()
    retrieved_value = spack.config.CONFIG.get("config:install_tree:root")
    assert retrieved_value == "/from-config-add", (
        f"Expected /from-config-add, got {retrieved_value}"
    )


def test_isolate_redirection(isolate_paths, tmp_path):
    """Check that `spack isolate` sets up all future writes to go to
    the selected isolation target.
    """
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    isolated_path = tmp_path / "test-isolation"
    sp_isolate("--path", str(isolated_path))

    assert isolate_scope_path.exists()
    assert isolated_path.exists()
    assert not (isolate_scope_path / "bootstrap.yaml").exists()
    assert not (isolate_scope_path / "config.yaml").exists()
    assert (isolate_scope_path / "include.yaml").exists()
    assert (isolated_path / "config.yaml").exists()

    cfg = spack.config.create()
    spack.config.CONFIG = cfg
    for location in ("data", "state", "cache"):
        assert cfg.get(f"config:locations:{location}")[0] == str(isolated_path)

    # Isolation does not invent module roots. New module output requires an
    # explicit module-root configuration, while old module trees are retained.
    assert cfg.get("modules:default:roots:tcl") is None
    assert cfg.get("modules:default:roots:lmod") is None

    with open(isolate_scope_path / "include.yaml", encoding="utf-8") as f:
        include_text = f.read()
    assert "layout" in include_text
    assert "SPACK_DISABLE_LOCAL_CONFIG" not in include_text


def test_isolate_added_config(isolate_paths, tmp_path):
    """Test that config added after isolate goes to the isolated path."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    isolated_path = tmp_path / "test-isolation"
    sp_isolate("--path", str(isolated_path))

    # Verify isolate scope was created
    assert isolate_scope_path.exists()
    assert (isolate_scope_path / "include.yaml").exists()

    # Reload config to pick up the isolate scope
    spack.config.CONFIG = spack.config.create()

    # Add config and verify it goes to isolated path
    sp_config("add", "config:build_jobs:42")

    config_file = isolated_path / "config.yaml"
    assert config_file.exists()

    with open(config_file, encoding="utf-8") as f:
        text = f.read().strip()
    assert "build_jobs: 42" in text
    assert "locations:" in text
    assert "data:" in text
    assert "state:" in text
    assert "cache:" in text


def test_overwrite_replaces_old_isolate_config(isolate_paths, tmp_path):
    """An old isolate scope is replaced by the current include override."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths
    isolate_scope_path.mkdir(parents=True)
    (isolate_scope_path / "include.yaml").write_text(
        "include:\n  - name: user\n    path: old-target\n", encoding="utf-8"
    )
    (isolate_scope_path / "bootstrap.yaml").write_text("bootstrap: {}\n", encoding="utf-8")
    old_target = tmp_path / "old-target"
    old_target.mkdir()
    new_target = tmp_path / "new-target"
    sp_isolate("--overwrite", "--path", str(new_target))
    include_text = (isolate_scope_path / "include.yaml").read_text(encoding="utf-8")
    assert "new-target" in include_text
    assert "layout" in include_text
    assert not (isolate_scope_path / "bootstrap.yaml").exists()


def test_isolate_keeps_existing_resources_in_place(isolate_paths, tmp_path):
    """Some pre-1.3 artifacts like installs, licenses, etc. were stored in the
    Spack prefix: check that `spack isolate` continues to use those.
    """
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths
    old_licenses = etc_spack / "licenses"
    old_licenses.mkdir()
    (old_licenses / "license.dat").write_text("license", encoding="utf-8")
    old_install = base_prefix / "opt" / "spack" / "pkg"
    old_install.mkdir(parents=True)
    (old_install / "metadata").write_text("installed", encoding="utf-8")

    target = tmp_path / "new-isolation"
    sp_isolate("--path", str(target))

    assert (old_licenses / "license.dat").read_text(encoding="utf-8") == "license"
    assert (old_install / "metadata").read_text(encoding="utf-8") == "installed"
    cfg = spack.config.create()
    spack.config.CONFIG = cfg
    assert spack.config.canonicalize_path(cfg.get("config:license_dir")) == str(old_licenses)
    assert cfg.get("config:locations:data")[0] == str(target)

    # This should be a noop: make sure no exceptions are raised
    spack.migrate.perform_migration()


def test_isolate_reuse_old_target(isolate_paths, tmp_path):
    """Reuse an old target after restoring tracked include.yaml before pulling.

    This test applies to any old isolation target. If the target came from
    the old ``spack isolate --self`` command, it is also the old isolate
    scope, so this compatibility path only makes sense when the user restored
    ``etc/spack/include.yaml`` before pulling the new Spack. Running the old
    ``spack isolate --undo`` before the pull would remove that target and its
    configuration, leaving nothing for ``--reuse-old`` to reuse.
    """
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths
    target = tmp_path / "old-isolation"
    target.mkdir()
    config_path = target / "config.yaml"
    repos_path = target / "repos.yaml"
    bootstrap_path = target / "bootstrap.yaml"
    config_text = """config:
  'build_stage:':
  - $tempdir/$user/spack-stage
  - {target}/stage
  'test_stage:': {target}/test-stage
  'misc_cache:': {target}/cache
""".format(target=target)
    repos_text = """repos:
  builtin:
    git: https://github.com/spack/spack-packages.git
    destination: {target}/repos/builtin
""".format(target=target)
    bootstrap_text = """bootstrap:
  root: {target}/bootstrap
""".format(target=target)
    config_path.write_text(config_text, encoding="utf-8")
    repos_path.write_text(repos_text, encoding="utf-8")
    bootstrap_path.write_text(bootstrap_text, encoding="utf-8")
    (target / "user-settings.yaml").write_text("config:\n  debug: true\n", encoding="utf-8")

    # Older isolate wrote these files into etc/spack/isolate. Preserve a copy
    # there too to ensure --reuse-old does not discard user configuration.
    isolate_scope_path.mkdir(parents=True)
    old_scope_files = {
        "config.yaml": config_text,
        "repos.yaml": repos_text,
        "bootstrap.yaml": bootstrap_text,
    }
    for name, contents in old_scope_files.items():
        (isolate_scope_path / name).write_text(contents, encoding="utf-8")

    sp_isolate("--path", str(target), "--reuse-old")

    assert config_path.read_text(encoding="utf-8") == config_text
    assert repos_path.read_text(encoding="utf-8") == repos_text
    assert bootstrap_path.read_text(encoding="utf-8") == bootstrap_text
    for name, contents in old_scope_files.items():
        assert (isolate_scope_path / name).read_text(encoding="utf-8") == contents
    assert (target / "user-settings.yaml").read_text(encoding="utf-8") == (
        "config:\n  debug: true\n"
    )
    include_text = (isolate_scope_path / "include.yaml").read_text(encoding="utf-8")
    assert str(target) in include_text
    assert "layout" in include_text


@pytest.mark.parametrize("args", [["--self"], ["--path", "isolate"]])
def test_isolate_reuse_old_self_target(isolate_paths, tmp_path, args):
    """Check ``spack isolate --reuse-old`` with ``--self``, or with a ``--path``
    that is effectively the same as if they had used ``--self``."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths
    isolate_scope_path.mkdir(parents=True)
    existing_files = {
        "config.yaml": "config:\n  build_jobs: 3\n",
        "repos.yaml": "repos:\n  builtin:\n    destination: /shared/builtin\n",
        "bootstrap.yaml": "bootstrap:\n  root: /shared/bootstrap\n",
    }
    for name, contents in existing_files.items():
        (isolate_scope_path / name).write_text(contents, encoding="utf-8")

    old_install = base_prefix / "opt" / "spack"
    old_install_bin = old_install / "bin"
    old_install_bin.mkdir(parents=True)
    (old_install_bin / "spack").write_text("old install", encoding="utf-8")

    command_args = ["--reuse-old"] + args
    if args == ["--path", "isolate"]:
        command_args[2] = str(isolate_scope_path)
    sp_isolate(*command_args)

    for name, contents in existing_files.items():
        assert (isolate_scope_path / name).read_text(encoding="utf-8") == contents
    include_text = (isolate_scope_path / "include.yaml").read_text(encoding="utf-8")
    assert "user" in include_text
    assert "layout" in include_text
    assert (isolate_scope_path / "user").is_dir()

    cfg = spack.config.create()
    # Config in the old isolate scope is preserved
    assert cfg.get("config:build_jobs") == 3
    # With --self, data goes to .isolate at spack root, not etc/spack/isolate
    expected_data_location = (
        str(base_prefix / ".isolate") if args == ["--self"] else str(isolate_scope_path)
    )
    assert cfg.get("config:locations:data")[0] == expected_data_location
    # ... and old install dir is used
    assert spack.config.canonicalize_path(cfg.get("config:install_tree:root")) == str(old_install)
    # ... and new isolation user redirect scope is available (and is highest-precedence
    # scope for writing)
    assert cfg.highest_precedence_scope().name == "user"
    assert cfg.highest_precedence_scope().path == str(isolate_scope_path / "user")


def test_isolate_path_self_target_requires_reuse(isolate_paths):
    """An existing self target is not reused implicitly through --path."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths
    isolate_scope_path.mkdir(parents=True)
    with pytest.raises(Exception):
        sp_isolate("--path", str(isolate_scope_path))


def test_isolate_rejects_reuse_and_overwrite_together(isolate_paths):
    """Reuse and overwrite express contradictory target handling."""
    with pytest.raises(spack.main.SpackCommandError):
        sp_isolate("--self", "--reuse-old", "--overwrite")


def test_self_isolate(isolate_paths, tmp_path):
    """`spack isolate --self` should setup highest-priority write scope
    inside the Spack prefix."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    sp_isolate("--self")
    assert isolate_scope_path.exists()
    assert not (isolate_scope_path / "bootstrap.yaml").exists()
    assert (isolate_scope_path / "user" / "config.yaml").exists()
    assert (isolate_scope_path / "include.yaml").exists()

    # Reload config to pick up isolate scope
    spack.config.CONFIG = spack.config.create()

    sp_config("add", "packages:gcc:buildable:false")
    # Config goes to redirected user scope
    new_config_path = isolate_scope_path / "user" / "packages.yaml"
    assert new_config_path.exists()
    with open(new_config_path, encoding="utf-8") as f:
        text = f.read().strip()
    expected_text = """\
packages:
  gcc:
    buildable: false"""
    assert text == expected_text


def test_isolate_overwrite_self(isolate_paths, tmp_path):
    """Test --self --overwrite clears previous isolate config."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    sp_isolate("--self")
    with pytest.raises(Exception):
        sp_isolate("--self")

    # Config goes to redirected user scope
    new_concr_config_path = isolate_scope_path / "user" / "concretizer.yaml"
    new_pkgs_config_path = isolate_scope_path / "user" / "packages.yaml"

    # Reload and add config
    spack.config.CONFIG = spack.config.create()
    sp_config("add", "concretizer:reuse:false")
    assert new_concr_config_path.exists()
    with open(new_concr_config_path, encoding="utf-8") as f:
        text = f.read().strip()
    expected_text = """\
concretizer:
  reuse: false"""
    assert text == expected_text

    # Overwrite and verify old config is gone
    sp_isolate("--self", "--overwrite")
    spack.config.CONFIG = spack.config.create()
    sp_config("add", "packages:gcc:buildable:false")
    assert not new_concr_config_path.exists()
    assert new_pkgs_config_path.exists()
    with open(new_pkgs_config_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    expected_text = """\
packages:
  gcc:
    buildable: false"""
    assert text == expected_text


def test_isolate_undo(isolate_paths, tmp_path):
    """Test that --undo removes the isolate scope."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    isolated_path = tmp_path / "test-isolation"
    sp_isolate("--path", str(isolated_path))
    assert isolate_scope_path.exists()

    sp_isolate("--undo")
    assert not isolate_scope_path.exists()


def test_isolate_undo_preserves_data(isolate_paths, tmp_path):
    """Test that --undo with --self removes config but preserves data (installs)."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    # Use --self so data goes to self_isolation_prefix
    sp_isolate("--self")
    assert isolate_scope_path.exists()

    # Create a fake install in the data location
    data_location = Path(spack.paths.self_isolation_prefix)
    fake_install = data_location / "linux-ubuntu22.04-x86_64" / "gcc-11.2.0" / "zlib-1.2.13"
    fake_install_bin = fake_install / "bin"
    fake_install_bin.mkdir(parents=True)
    (fake_install_bin / "zlib").write_text("fake install", encoding="utf-8")

    # Undo should remove config but keep data
    sp_isolate("--undo")
    assert not isolate_scope_path.exists(), "Config scope should be removed"
    assert data_location.exists(), "Data location should be preserved"
    assert (fake_install / "bin" / "zlib").exists(), "Installs should be preserved"


@pytest.mark.parametrize("use_self", [False, True])
def test_isolate_after_migration_keeps_retained_resources(isolate_paths, tmp_path, use_self):
    """After a migration decision, `spack isolate` must keep reading the layout scope.

    The migration records paths to retained old resources (always the install tree;
    environments/GPG/licenses only if their copy failed) in ``$spack/etc/spack/layout``.
    Isolation replaces the standard include list, so it must include that scope itself,
    and must not re-derive old resource paths (which would re-pin successfully migrated
    resources to their stale pre-migration copies).
    """
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    # Old resources exist in the prefix: installs (retained) and environments (migrated)
    old_install = base_prefix / "opt" / "spack"
    (old_install / ".spack-db").mkdir(parents=True)
    (old_install / ".spack-db" / "index.json").write_text("{}", encoding="utf-8")
    old_envs = base_prefix / "var" / "spack" / "environments" / "myenv"
    old_envs.mkdir(parents=True)
    (old_envs / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    # Simulate an approved migration: envs copied, installs retained, decision recorded
    layout_dir = etc_spack / "layout"
    layout_dir.mkdir()
    (layout_dir / "config.yaml").write_text(
        f"config:\n  install_tree:\n    root: {old_install}\n", encoding="utf-8"
    )
    Path(spack.migrate.migration_done_marker_path()).write_text("done\n", encoding="utf-8")

    if use_self:
        sp_isolate("--self")
    else:
        sp_isolate("--path", str(tmp_path / "iso"))

    cfg = spack.config.create()
    active = [s.name for s in cfg.active_scopes]

    # Both layout scopes are active, isolate's above the migration's, user above both
    assert "layout" in active and "isolate_layout" in active and "user" in active
    assert active.index("layout") < active.index("isolate_layout") < active.index("user")

    # Retained installs are still visible
    assert spack.config.canonicalize_path(cfg.get("config:install_tree:root")) == str(old_install)

    # Successfully migrated resources were NOT re-pinned to the stale prefix copies
    assert cfg.get("config:environments_root") == "$data_home/environments"
    assert cfg.get("config:gpg_path") == "$data_home/gpg"
    assert cfg.get("config:license_dir") == "$data_home/licenses"

    # Isolation locations apply
    isolation_target = Path(spack.paths.self_isolation_prefix) if use_self else tmp_path / "iso"
    assert cfg.get("config:locations:data")[0] == str(isolation_target)

    # `spack migrate undo` still reaches the isolated instance through the layout scope
    (layout_dir / "config.yaml").write_text(
        f"config:\n  install_tree:\n    root: {old_install}\n"
        f"  environments_root: {old_envs.parent}\n",
        encoding="utf-8",
    )
    cfg = spack.config.create()
    assert str(cfg.get("config:environments_root")) == str(old_envs.parent)


def test_isolate_reuse_old_keeps_generated_layout(isolate_paths, tmp_path):
    """``--reuse-old`` keeps an existing isolate layout config instead of regenerating it.

    The first ``--reuse-old`` writes generated settings to the isolate layout scope (not to
    the preserved target). Running it again, or after the user has edited that file,
    keeps the file as it is.
    """
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths
    target = tmp_path / "old-isolation"
    target.mkdir()
    (target / "config.yaml").write_text("config:\n  build_jobs: 3\n", encoding="utf-8")

    sp_isolate("--path", str(target), "--reuse-old")

    layout_config = isolate_scope_path / "layout" / "config.yaml"
    assert layout_config.exists()
    generated = layout_config.read_text(encoding="utf-8")

    # User edits the generated file
    edited = generated + "  build_jobs: 99\n"
    layout_config.write_text(edited, encoding="utf-8")

    out = sp_isolate("--path", str(target), "--reuse-old")
    assert "Keeping existing" in out

    # Edits survived, and the preserved target is untouched as well
    assert layout_config.read_text(encoding="utf-8") == edited
    assert (target / "config.yaml").read_text(encoding="utf-8") == "config:\n  build_jobs: 3\n"


def test_isolate_self_reuse_old_keeps_user_config(isolate_paths):
    """For ``--self``, the generated config is the user scope; ``--reuse-old`` must not
    discard settings the user has added to it since."""
    home_dir, base_prefix, etc_spack, isolate_scope_path = isolate_paths

    sp_isolate("--self")
    user_config = isolate_scope_path / "user" / "config.yaml"
    assert user_config.exists()

    spack.config.CONFIG = spack.config.create()
    sp_config("add", "config:build_jobs:7")
    assert "build_jobs: 7" in user_config.read_text(encoding="utf-8")

    out = sp_isolate("--self", "--reuse-old")
    assert "Keeping existing" in out
    assert "build_jobs: 7" in user_config.read_text(encoding="utf-8")

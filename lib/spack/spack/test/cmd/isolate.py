# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack
import spack.cmd.isolate
import spack.config
import spack.main
import spack.paths

sp_isolate = spack.main.SpackCommand("isolate")
sp_config = spack.main.SpackCommand("config")


@pytest.fixture
def mock_spack_paths(monkeypatch, tmp_path):
    """Set up a mock spack instance with paths redirected to tmp_path.

    Returns a tuple of (base_prefix, etc_spack, isolate_scope_path).
    """
    from spack.paths import SpackPaths

    base_prefix = tmp_path / "mock_spack"
    base_prefix.mkdir()
    etc_spack = base_prefix / "etc" / "spack"
    etc_spack.mkdir(parents=True)

    mock_paths = SpackPaths(_prefix=str(base_prefix))
    monkeypatch.setattr(spack.paths, "locations", mock_paths)

    isolate_scope_path = etc_spack / "isolate"
    monkeypatch.setattr(spack.cmd.isolate, "ISOLATE_SCOPE_PATH", str(isolate_scope_path))

    return base_prefix, etc_spack, isolate_scope_path


def test_isolate_smoke_test(mock_spack_paths, tmp_path):
    """Basic smoke test for isolate command."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths
    (etc_spack / "include.yaml").write_text(
        'include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n',
        encoding="utf-8",
    )
    (etc_spack / "standard_scopes").mkdir()

    isolated_path = tmp_path / "test-isolation"
    sp_isolate("--path", str(isolated_path))

    assert isolate_scope_path.exists()
    assert isolated_path.exists()
    assert not (isolate_scope_path / "bootstrap.yaml").exists()
    assert not (isolate_scope_path / "config.yaml").exists()
    assert (isolate_scope_path / "include.yaml").exists()
    assert (isolated_path / "config.yaml").exists()

    cfg = spack.config.create()
    for location in ("data", "state", "cache"):
        assert cfg.get(f"config:locations:{location}")[0] == str(isolated_path)

    with open(isolate_scope_path / "include.yaml", encoding="utf-8") as f:
        include_text = f.read()
    assert "layout" in include_text


def test_isolate_added_config(mock_spack_paths, tmp_path):
    """Test that config added after isolate goes to the isolated path."""

    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    # Create include.yaml that references isolate scope
    include_yaml = etc_spack / "include.yaml"
    with open(include_yaml, "w", encoding="utf-8") as f:
        f.write('include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n')

    # Create standard_scopes/include.yaml
    standard_scopes_dir = etc_spack / "standard_scopes"
    standard_scopes_dir.mkdir()
    with open(standard_scopes_dir / "include.yaml", "w", encoding="utf-8") as f:
        f.write(
            'include:\n  - name: "user"\n    path: "~/.config/spack"\n'
            "    optional: true\n    prefer_modify: true\n"
        )

    # Create isolated user path
    isolated_path = tmp_path / "test-isolation"

    # Run isolate command
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


def test_isolate_replaces_old_isolate_config(mock_spack_paths, tmp_path):
    """An old isolate scope is replaced by the current include override."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths
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


def test_isolate_reuse_old_target(mock_spack_paths, tmp_path):
    """Reuse an old target after restoring tracked include.yaml before pulling.

    This test applies to any old isolation target. If the target came from
    the old ``spack isolate --self`` command, it is also the old isolate
    scope, so this compatibility path only makes sense when the user restored
    ``etc/spack/include.yaml`` before pulling the new Spack. Running the old
    ``spack isolate --undo`` before the pull would remove that target and its
    configuration, leaving nothing for ``--reuse-old`` to reuse.
    """
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths
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
def test_isolate_reuse_old_self_target(mock_spack_paths, tmp_path, args):
    """Reuse an existing self target through either supported spelling."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths
    (etc_spack / "include.yaml").write_text(
        'include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n',
        encoding="utf-8",
    )
    (etc_spack / "standard_scopes").mkdir()
    isolate_scope_path.mkdir(parents=True)
    existing_files = {
        "config.yaml": "config:\n  build_jobs: 3\n",
        "repos.yaml": "repos:\n  builtin:\n    destination: /shared/builtin\n",
        "bootstrap.yaml": "bootstrap:\n  root: /shared/bootstrap\n",
    }
    for name, contents in existing_files.items():
        (isolate_scope_path / name).write_text(contents, encoding="utf-8")

    # An old install makes the migration/resource-recording path generate the
    # layout scope, where the new isolation locations are supplied without
    # modifying the preserved target config.yaml.
    old_install = base_prefix / "opt" / "spack" / "bin"
    old_install.mkdir(parents=True)
    (old_install / "spack").write_text("old install", encoding="utf-8")

    command_args = ["--reuse-old"] + args
    if args == ["--path", "isolate"]:
        command_args[2] = str(isolate_scope_path)
    sp_isolate(*command_args)

    for name, contents in existing_files.items():
        assert (isolate_scope_path / name).read_text(encoding="utf-8") == contents
    include_text = (isolate_scope_path / "include.yaml").read_text(encoding="utf-8")
    assert "user-redirect" in include_text
    assert "layout" in include_text
    assert (isolate_scope_path / "user-redirect").is_dir()

    cfg = spack.config.create()
    assert cfg.get("config:build_jobs") == 3
    assert cfg.get("config:locations:data")[0] == str(isolate_scope_path)
    assert cfg.highest_precedence_scope().name == "user"
    assert cfg.highest_precedence_scope().path == str(isolate_scope_path / "user-redirect")


def test_isolate_path_self_target_requires_reuse(mock_spack_paths):
    """An existing self target is not reused implicitly through --path."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths
    isolate_scope_path.mkdir(parents=True)
    with pytest.raises(Exception):
        sp_isolate("--path", str(isolate_scope_path))


def test_isolate_rejects_reuse_and_overwrite_together(mock_spack_paths):
    """Reuse and overwrite express contradictory target handling."""
    with pytest.raises(spack.main.SpackCommandError):
        sp_isolate("--self", "--reuse-old", "--overwrite")


def test_isolate_overwrite_same_dir(mock_spack_paths, tmp_path):
    """Test that --overwrite works when isolating to the same directory."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    isolated_path1 = tmp_path / "test-isolation1"
    sp_isolate("--path", str(isolated_path1))
    with pytest.raises(Exception):
        sp_isolate("--path", str(isolated_path1))
    sp_isolate("--overwrite", "--path", str(isolated_path1))


def test_isolate_overwrite_different_dir(mock_spack_paths, tmp_path):
    """Test that --overwrite works when switching to a different directory."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    isolated_path1 = tmp_path / "test-isolation1"
    isolated_path2 = tmp_path / "test-isolation2"
    sp_isolate("--path", str(isolated_path1))
    with pytest.raises(Exception):
        sp_isolate("--path", str(isolated_path1))
    sp_isolate("--overwrite", "--path", str(isolated_path2))
    assert not (isolate_scope_path / "bootstrap.yaml").exists()
    assert (isolated_path2 / "config.yaml").exists()


def test_self_isolate(mock_spack_paths, tmp_path):
    """Test --self isolate (stores isolation in Spack's prefix)."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    # Create include.yaml
    with open(etc_spack / "include.yaml", "w", encoding="utf-8") as f:
        f.write('include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n')

    # Create standard_scopes
    standard_scopes_dir = etc_spack / "standard_scopes"
    standard_scopes_dir.mkdir()
    with open(standard_scopes_dir / "include.yaml", "w", encoding="utf-8") as f:
        f.write(
            'include:\n  - name: "user"\n    path: "~/.config/spack"\n'
            "    optional: true\n    prefer_modify: true\n"
        )

    sp_isolate("--self")
    assert isolate_scope_path.exists()
    assert not (isolate_scope_path / "bootstrap.yaml").exists()
    assert (isolate_scope_path / "config.yaml").exists()
    assert (isolate_scope_path / "include.yaml").exists()
    assert (isolate_scope_path / "user-redirect").exists()

    # Reload config to pick up isolate scope
    spack.config.CONFIG = spack.config.create()

    sp_config("add", "packages:gcc:buildable:false")
    # Config goes to user-redirect subdirectory
    new_config_path = isolate_scope_path / "user-redirect" / "packages.yaml"
    assert new_config_path.exists()
    with open(new_config_path, encoding="utf-8") as f:
        text = f.read().strip()
    expected_text = """\
packages:
  gcc:
    buildable: false"""
    assert text == expected_text


def test_self_isolate_overwrite(mock_spack_paths, tmp_path):
    """Test --self --overwrite clears previous isolate config."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    # Create include.yaml
    with open(etc_spack / "include.yaml", "w", encoding="utf-8") as f:
        f.write('include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n')

    # Create standard_scopes
    standard_scopes_dir = etc_spack / "standard_scopes"
    standard_scopes_dir.mkdir()
    with open(standard_scopes_dir / "include.yaml", "w", encoding="utf-8") as f:
        f.write(
            'include:\n  - name: "user"\n    path: "~/.config/spack"\n'
            "    optional: true\n    prefer_modify: true\n"
        )

    sp_isolate("--self")
    with pytest.raises(Exception):
        sp_isolate("--self")

    # Config goes to user-redirect subdirectory
    new_concr_config_path = isolate_scope_path / "user-redirect" / "concretizer.yaml"
    new_pkgs_config_path = isolate_scope_path / "user-redirect" / "packages.yaml"

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


def test_isolate_undo(mock_spack_paths, tmp_path):
    """Test that --undo removes the isolate scope."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    isolated_path = tmp_path / "test-isolation"
    sp_isolate("--path", str(isolated_path))
    assert isolate_scope_path.exists()

    sp_isolate("--undo")
    assert not isolate_scope_path.exists()

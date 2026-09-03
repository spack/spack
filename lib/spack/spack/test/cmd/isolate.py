# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib
import shutil

import pytest

import spack.cmd.isolate
import spack.config
import spack.main
import spack.paths
from spack.test.conftest import _create_mock_configuration_scopes

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


@pytest.fixture(scope="function")
def mutable_config_with_dir(tmp_path_factory: pytest.TempPathFactory, configuration_dir):
    """Like config, but tests can modify the configuration. This fixture also
    yields the configuration directory, unlike conf_test.mutable_config
    """
    mutable_dir = tmp_path_factory.mktemp("mutable_config") / "tmp"
    shutil.copytree(configuration_dir, mutable_dir)

    scopes = _create_mock_configuration_scopes(mutable_dir)
    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg, mutable_dir


@pytest.fixture(scope="function")
def mock_pre_isolate_config(mutable_config_with_dir, monkeypatch, tmp_path):
    _, cfg_dir = mutable_config_with_dir

    # Create a mock spack instance with etc_path pointing to our test directory
    # cfg_dir is typically .../tmp/spack, so we need prefix to be .../tmp/.. to get etc/spack
    # Actually cfg_dir.parent is the right prefix if cfg_dir is prefix/etc/spack
    from spack.paths import SpackPaths

    # cfg_dir is the mutable config directory (e.g., /tmp/test/spack)
    # We need to find the prefix such that prefix/etc/spack == cfg_dir
    # So if cfg_dir ends with /etc/spack, prefix is cfg_dir/../..
    # But mutable_config likely puts things at tmp/spack directly
    # Let me check: cfg_dir typically is something like .../tmp, and we want etc_path to be cfg_dir
    # So prefix should be set such that prefix/etc/spack = cfg_dir
    # That means prefix = cfg_dir/../../..  if cfg_dir is at "etc/spack" level
    # Actually, let's just check what cfg_dir actually is by its structure

    # The mutable_config_with_dir fixture creates config at tmp_path/spack
    # So cfg_dir is tmp_path/spack, and we want etc_path to be cfg_dir
    # If etc_path = prefix/etc/spack, then prefix = cfg_dir/../../..
    # But that seems wrong. Let me just compute it properly:
    # We want: cfg_dir == prefix/etc/spack
    # So: prefix = cfg_dir/../.. (go up two levels from "spack" to get to the prefix)
    prefix = cfg_dir.parent.parent
    mock_paths = SpackPaths(_prefix=str(prefix))
    monkeypatch.setattr(spack.paths, "locations", mock_paths)

    # The isolate scope will now naturally be at mock_paths.etc_path/isolate
    isolate_path = pathlib.Path(mock_paths.etc_path) / "isolate"
    monkeypatch.setattr(spack.cmd.isolate, "ISOLATE_SCOPE_PATH", str(isolate_path))

    yield cfg_dir, tmp_path


def test_isolate_smoke_test(mock_pre_isolate_config):
    cfg_dir, iso_root = mock_pre_isolate_config
    isolated_path = iso_root / "test-isolation"
    sp_isolate("--path", str(isolated_path))
    assert os.path.exists(spack.cmd.isolate.ISOLATE_SCOPE_PATH)
    assert isolated_path.exists()
    assert os.path.exists(os.path.join(spack.cmd.isolate.ISOLATE_SCOPE_PATH, "bootstrap.yaml"))
    assert os.path.exists(os.path.join(spack.cmd.isolate.ISOLATE_SCOPE_PATH, "config.yaml"))
    assert os.path.exists(os.path.join(spack.cmd.isolate.ISOLATE_SCOPE_PATH, "include.yaml"))
    # we reload the config after isolation
    # With the new implementation, the isolate scope uses include:: override,
    # so "user" scope should point to the isolated path, not "isolate" as a separate scope
    with spack.config.use_configuration(cfg_dir / "spack"):
        # The user scope should exist (redirected by isolate's include.yaml)
        assert "user" in sp_config("scopes")


def test_isolate_added_config(mock_spack_paths, tmp_path):
    """Test that config added after isolate goes to the isolated path."""
    import spack.util.spack_yaml as syaml

    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    # Create include.yaml that references isolate scope
    include_yaml = etc_spack / "include.yaml"
    with open(include_yaml, "w") as f:
        f.write('include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n')

    # Create standard_scopes/include.yaml
    standard_scopes_dir = etc_spack / "standard_scopes"
    standard_scopes_dir.mkdir()
    with open(standard_scopes_dir / "include.yaml", "w") as f:
        f.write('include:\n  - name: "user"\n    path: "~/.config/spack"\n    optional: true\n    prefer_modify: true\n')

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

    with open(config_file) as f:
        text = f.read().strip()
    expected_text = """\
config:
  build_jobs: 42"""
    assert text == expected_text


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
    with open(isolate_scope_path / "bootstrap.yaml", "r", encoding="utf-8") as f:
        text = f.read().strip()
    expected_text = f"""\
bootstrap:
  root: {isolated_path2 / "bootstrap"}"""
    assert text == expected_text


def test_self_isolate(mock_spack_paths, tmp_path):
    """Test --self isolate (stores isolation in Spack's prefix)."""
    base_prefix, etc_spack, isolate_scope_path = mock_spack_paths

    # Create include.yaml
    with open(etc_spack / "include.yaml", "w") as f:
        f.write('include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n')

    # Create standard_scopes
    standard_scopes_dir = etc_spack / "standard_scopes"
    standard_scopes_dir.mkdir()
    with open(standard_scopes_dir / "include.yaml", "w") as f:
        f.write('include:\n  - name: "user"\n    path: "~/.config/spack"\n    optional: true\n    prefer_modify: true\n')

    sp_isolate("--self")
    assert isolate_scope_path.exists()
    assert (isolate_scope_path / "bootstrap.yaml").exists()
    assert (isolate_scope_path / "config.yaml").exists()
    assert (isolate_scope_path / "include.yaml").exists()
    assert (isolate_scope_path / "user-redirect").exists()

    # Reload config to pick up isolate scope
    spack.config.CONFIG = spack.config.create()

    sp_config("add", "packages:gcc:buildable:false")
    # Config goes to user-redirect subdirectory
    new_config_path = isolate_scope_path / "user-redirect" / "packages.yaml"
    assert new_config_path.exists()
    with open(new_config_path) as f:
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
    with open(etc_spack / "include.yaml", "w") as f:
        f.write('include:\n  - path: "isolate"\n    optional: true\n  - path: "standard_scopes"\n')

    # Create standard_scopes
    standard_scopes_dir = etc_spack / "standard_scopes"
    standard_scopes_dir.mkdir()
    with open(standard_scopes_dir / "include.yaml", "w") as f:
        f.write('include:\n  - name: "user"\n    path: "~/.config/spack"\n    optional: true\n    prefer_modify: true\n')

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
    with open(new_concr_config_path) as f:
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

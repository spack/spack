# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path

import pytest

import spack.config
import spack.main

sp_migrate = spack.main.SpackCommand("migrate")
sp_config = spack.main.SpackCommand("config")


def _write_layout_config(path: Path, **config):
    path.mkdir(parents=True, exist_ok=True)
    lines = ["config: {}"] if not config else ["config:"]
    for key, value in config.items():
        lines.append(f"  {key}: {value}")
    (path / "config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_migrate_undo_restores_backup_and_configuration(mock_spack_instance, monkeypatch):
    """Undo points scopes back to old locations (resources already there)."""
    home_dir, base_prefix = mock_spack_instance

    # Create migration marker
    marker = Path(base_prefix) / ".migration-done"
    marker.write_text("Migration completed\n", encoding="utf-8")

    # Create old resources at their original locations
    old_licenses = Path(base_prefix) / "etc" / "spack" / "licenses"
    old_envs = Path(base_prefix) / "var" / "spack" / "environments"
    old_gpg = Path(base_prefix) / "opt" / "spack" / "gpg"

    old_licenses.mkdir(parents=True)
    (old_licenses / "license.dat").write_text("license", encoding="utf-8")

    (old_envs / "demo").mkdir(parents=True)
    (old_envs / "demo" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    (old_gpg / "private-keys-v1.d").mkdir(parents=True)
    (old_gpg / "private-keys-v1.d" / "key").write_text("key", encoding="utf-8")

    layout = Path(base_prefix) / "etc" / "spack" / "layout"
    _write_layout_config(layout)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    sp_migrate("undo", "--restore-old-user-scope")

    # Old resources should still exist at their original locations
    assert (old_licenses / "license.dat").read_text(encoding="utf-8") == "license"
    assert (old_envs / "demo" / "spack.yaml").exists()
    assert (old_gpg / "private-keys-v1.d" / "key").exists()

    # Layout scope should point to old locations
    layout_text = (layout / "config.yaml").read_text(encoding="utf-8")
    assert str(old_licenses) in layout_text
    assert str(old_envs) in layout_text
    assert str(old_gpg) in layout_text

    standard_scopes = (
        Path(base_prefix) / "etc" / "spack" / "standard_scopes" / "include.yaml"
    ).read_text(encoding="utf-8")
    assert "~/.spack" in standard_scopes

    # Verify ~/.spack is actually the active write scope
    old_user = Path(home_dir) / ".spack"
    old_user.mkdir(exist_ok=True)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    sp_config("add", "config:build_jobs:99")

    old_user_config = old_user / "config.yaml"
    assert old_user_config.exists()
    assert "build_jobs: 99" in old_user_config.read_text(encoding="utf-8")


def test_undo_nothing_to_undo(mock_spack_instance, monkeypatch):
    """Undo requires old resources to exist."""
    home_dir, base_prefix = mock_spack_instance

    # No old resources
    layout = Path(base_prefix) / "etc" / "spack" / "layout"
    _write_layout_config(layout)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    sp_migrate("undo", fail_on_error=False)

    assert "Nothing to do" in sp_migrate.output
    assert "no old resources" in sp_migrate.output


def test_migrate_cleanup_old_removes_unreferenced_legacy_directory(
    mock_spack_instance, monkeypatch
):
    """cleanup-old removes ~/.spack only when active configuration no longer uses it."""
    home_dir, base_prefix = mock_spack_instance
    old_user = Path(home_dir) / ".spack"
    old_user.mkdir()
    (old_user / "config.yaml").write_text("config: {}\n", encoding="utf-8")

    # Create new user config location so fallback to ~/.spack is not used
    new_user = Path(home_dir) / ".config" / "spack"
    new_user.mkdir(parents=True)
    (new_user / "config.yaml").write_text("config: {}\n", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    sp_migrate("cleanup-old")

    assert not old_user.exists()


def test_migrate_cleanup_old_rejects_referenced_legacy_directory(mock_spack_instance, monkeypatch):
    """cleanup-old preserves ~/.spack while a configured path still references it."""
    home_dir, base_prefix = mock_spack_instance
    old_user = Path(home_dir) / ".spack"
    old_user.mkdir()
    (old_user / "config.yaml").write_text("config: {}\n", encoding="utf-8")
    standard_scopes = Path(base_prefix) / "etc" / "spack" / "standard_scopes"
    include_path = standard_scopes / "include.yaml"
    include_text = include_path.read_text(encoding="utf-8")
    include_path.write_text(include_text.replace("~/.config/spack", "~/.spack"), encoding="utf-8")
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    with pytest.raises(spack.main.SpackCommandError):
        sp_migrate("cleanup-old")
    assert "still refers" in sp_migrate.output

    assert old_user.exists()


def test_migrate_can_alternate_between_old_and_new_layout(mock_spack_instance, monkeypatch):
    """Can alternate between undo and use-new-layout to switch layouts."""
    home_dir, base_prefix = mock_spack_instance

    # Create old resources at their original locations
    old_licenses = Path(base_prefix) / "etc" / "spack" / "licenses"
    old_envs = Path(base_prefix) / "var" / "spack" / "environments"
    old_gpg = Path(base_prefix) / "opt" / "spack" / "gpg"

    old_licenses.mkdir(parents=True)
    (old_licenses / "license.dat").write_text("license", encoding="utf-8")

    (old_envs / "demo").mkdir(parents=True)
    (old_envs / "demo" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")

    (old_gpg / "private-keys-v1.d").mkdir(parents=True)
    (old_gpg / "private-keys-v1.d" / "key").write_text("key", encoding="utf-8")

    layout = Path(base_prefix) / "etc" / "spack" / "layout"
    new_data = Path(home_dir) / ".local" / "share" / "spack"

    # Start with no layout scope
    if layout.exists():
        import shutil

        shutil.rmtree(layout)

    # Round 1: use-new-layout should migrate to XDG locations
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    sp_migrate("use-new-layout")

    # Check that config points to new XDG locations (may be $data_home variable)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    license_dir = spack.config.CONFIG.get("config:license_dir")
    envs_root = spack.config.CONFIG.get("config:environments_root")
    gpg_path = spack.config.CONFIG.get("config:gpg_path")
    # Should contain either the full path or $data_home/... which indicates XDG layout
    assert "$data_home" in license_dir or str(new_data / "licenses") in license_dir
    assert "$data_home" in envs_root or str(new_data / "environments") in envs_root
    assert "$data_home" in gpg_path or str(new_data / "gpg") in gpg_path

    # New locations should exist
    assert (new_data / "licenses" / "license.dat").exists()
    assert (new_data / "environments" / "demo" / "spack.yaml").exists()
    assert (new_data / "gpg" / "private-keys-v1.d" / "key").exists()

    # Round 2: undo should point back to old locations
    # First, put resources back in old locations for undo to work with
    if not (old_licenses / "license.dat").exists():
        old_licenses.mkdir(parents=True, exist_ok=True)
        (old_licenses / "license.dat").write_text("license", encoding="utf-8")
    if not (old_envs / "demo" / "spack.yaml").exists():
        (old_envs / "demo").mkdir(parents=True, exist_ok=True)
        (old_envs / "demo" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    if not (old_gpg / "private-keys-v1.d" / "key").exists():
        (old_gpg / "private-keys-v1.d").mkdir(parents=True, exist_ok=True)
        (old_gpg / "private-keys-v1.d" / "key").write_text("key", encoding="utf-8")

    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    sp_migrate("undo")

    # Check that config now points to old locations
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    assert str(old_licenses) in spack.config.CONFIG.get("config:license_dir")
    assert str(old_envs) in spack.config.CONFIG.get("config:environments_root")
    assert str(old_gpg) in spack.config.CONFIG.get("config:gpg_path")

    # Round 3: use-new-layout again should work
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    sp_migrate("use-new-layout")

    # Check that config points to new XDG locations again
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    license_dir = spack.config.CONFIG.get("config:license_dir")
    envs_root = spack.config.CONFIG.get("config:environments_root")
    gpg_path = spack.config.CONFIG.get("config:gpg_path")
    # Should contain either the full path or $data_home/... which indicates XDG layout
    assert "$data_home" in license_dir or str(new_data / "licenses") in license_dir
    assert "$data_home" in envs_root or str(new_data / "environments") in envs_root
    assert "$data_home" in gpg_path or str(new_data / "gpg") in gpg_path

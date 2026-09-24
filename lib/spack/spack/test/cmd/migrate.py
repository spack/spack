# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path

import pytest

import spack.config
import spack.main

sp_migrate = spack.main.SpackCommand("migrate")


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

    sp_migrate("undo")

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


def test_migrate_undo_requires_migration_marker(mock_spack_instance, monkeypatch):
    """Undo requires migration marker to exist."""
    home_dir, base_prefix = mock_spack_instance

    # No migration marker
    layout = Path(base_prefix) / "etc" / "spack" / "layout"
    _write_layout_config(layout)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    sp_migrate("undo")

    assert "No migration has been performed" in sp_migrate.output
    assert "Nothing to undo" in sp_migrate.output


def test_migrate_cleanup_old_removes_unreferenced_legacy_directory(
    mock_spack_instance, monkeypatch
):
    """cleanup-old removes ~/.spack only when active configuration no longer uses it."""
    home_dir, base_prefix = mock_spack_instance
    old_user = Path(home_dir) / ".spack"
    old_user.mkdir()
    (old_user / "config.yaml").write_text("config: {}\n", encoding="utf-8")
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

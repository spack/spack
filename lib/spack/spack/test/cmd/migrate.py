# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import subprocess
import sys
from pathlib import Path

import pytest

import spack.config
import spack.main
import spack.migrate
import spack.util.tty
from spack.util.filesystem import getuid

sp_migrate = spack.main.SpackCommand("migrate")


def _write_layout_config(path: Path, **config):
    path.mkdir(parents=True, exist_ok=True)
    lines = ["config: {}"] if not config else ["config:"]
    for key, value in config.items():
        lines.append(f"  {key}: {value}")
    (path / "config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_migrate_undo_restores_old_layout(mock_spack_instance, monkeypatch):
    """Undo points the layout scope back at the old locations (resources already there)."""
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
    assert os.path.join("$spack", "etc", "spack", "licenses") in layout_text
    assert os.path.join("$spack", "var", "spack", "environments") in layout_text
    assert os.path.join("$spack", "opt", "spack", "gpg") in layout_text

    # The tracked standard scopes file is not touched
    standard_scopes = (
        Path(base_prefix) / "etc" / "spack" / "standard_scopes" / "include.yaml"
    ).read_text(encoding="utf-8")
    assert "~/.config/spack" in standard_scopes
    assert '"~/.spack"' not in standard_scopes


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


def _setup_cleanup_old(home_dir, new_user_config="config: {}\n"):
    """Create a ~/.spack with some content and a migrated ~/.config/spack."""
    old_user = Path(home_dir) / ".spack"
    old_user.mkdir()
    (old_user / "config.yaml").write_text("config: {}\n", encoding="utf-8")
    (old_user / "bootstrap" / "store").mkdir(parents=True)
    (old_user / "bootstrap" / "store" / "blob").write_bytes(b"\0" * 4096)

    new_user = Path(home_dir) / ".config" / "spack"
    new_user.mkdir(parents=True)
    (new_user / "config.yaml").write_text(new_user_config, encoding="utf-8")
    return old_user, new_user


def test_migrate_cleanup_old_removes_unreferenced_legacy_directory(
    mock_spack_instance, monkeypatch
):
    """cleanup-old --yes removes ~/.spack when nothing fatal refers to it. Old config files
    still being in ~/.spack is not a reference: only the active user scope pointing there is.
    """
    home_dir, base_prefix = mock_spack_instance
    old_user, new_user = _setup_cleanup_old(home_dir)
    assert (old_user / "config.yaml").exists()
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())
    assert spack.config.CONFIG.scopes["user"].path == str(new_user)

    out = sp_migrate("cleanup-old", "--yes")

    assert not old_user.exists()
    assert "user configuration scope" not in out
    # The report names the directory, its contents, and what was not checked
    assert "permanently delete" in out
    assert "bootstrap" in out
    assert "Not checked" in out


def test_migrate_cleanup_old_dry_run_does_not_remove(mock_spack_instance, monkeypatch):
    home_dir, base_prefix = mock_spack_instance
    old_user, _ = _setup_cleanup_old(home_dir)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    out = sp_migrate("cleanup-old", "--dry-run")

    assert old_user.exists()
    assert "Dry run" in out


def test_migrate_cleanup_old_requires_confirmation(mock_spack_instance, monkeypatch):
    """Without --yes, cleanup-old prompts; with no terminal it refuses."""
    home_dir, base_prefix = mock_spack_instance
    old_user, _ = _setup_cleanup_old(home_dir)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    # No terminal: refuse
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    with pytest.raises(spack.main.SpackCommandError):
        sp_migrate("cleanup-old")
    assert "no terminal" in sp_migrate.output
    assert old_user.exists()

    # Terminal, user says no
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(spack.util.tty, "get_yes_or_no", lambda *a, **k: False)
    out = sp_migrate("cleanup-old")
    assert "Not removing" in out
    assert old_user.exists()

    # Terminal, user says yes
    monkeypatch.setattr(spack.util.tty, "get_yes_or_no", lambda *a, **k: True)
    sp_migrate("cleanup-old")
    assert not old_user.exists()


def test_migrate_cleanup_old_refuses_install_tree(mock_spack_instance, monkeypatch):
    """An install tree under ~/.spack (config:install_tree:root) is never deleted, even
    with --yes."""
    home_dir, base_prefix = mock_spack_instance
    old_user, new_user = _setup_cleanup_old(home_dir)
    store = old_user / "opt"
    store.mkdir()
    (new_user / "config.yaml").write_text(
        f"config:\n  install_tree:\n    root: {store}\n", encoding="utf-8"
    )
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    with pytest.raises(spack.main.SpackCommandError):
        sp_migrate("cleanup-old", "--yes")

    assert old_user.exists()
    assert "current install tree" in sp_migrate.output
    assert "config:install_tree:root" in sp_migrate.output


def test_migrate_cleanup_old_reports_references(mock_spack_instance, monkeypatch):
    """Non-fatal references to ~/.spack are listed but do not block removal."""
    home_dir, base_prefix = mock_spack_instance
    old_user, new_user = _setup_cleanup_old(home_dir)
    (new_user / "config.yaml").write_text(
        f"config:\n  source_cache: {old_user}/srccache\n", encoding="utf-8"
    )
    (new_user / "mirrors.yaml").write_text(
        f"mirrors:\n  local: file://{old_user}/mirror\n", encoding="utf-8"
    )
    (new_user / "repos.yaml").write_text(
        f"repos:\n  mine: {old_user}/myrepo/spack_repo/mine\n", encoding="utf-8"
    )
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    out = sp_migrate("cleanup-old", "--yes")

    assert "still refers" in out
    assert "config:source_cache" in out
    assert "mirrors:local" in out
    assert "repos:mine" in out
    # ... but none of these block removal
    assert not old_user.exists()


def test_migrate_cleanup_old_user_scope_reference(mock_spack_instance, monkeypatch):
    """A user scope still pointing at ~/.spack is reported and is a hard stop, even with --yes."""
    home_dir, base_prefix = mock_spack_instance
    old_user, _ = _setup_cleanup_old(home_dir)
    standard_scopes = Path(base_prefix) / "etc" / "spack" / "standard_scopes"
    include_path = standard_scopes / "include.yaml"
    include_text = include_path.read_text(encoding="utf-8")
    include_path.write_text(include_text.replace("~/.config/spack", "~/.spack"), encoding="utf-8")
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    with pytest.raises(spack.main.SpackCommandError):
        sp_migrate("cleanup-old", "--yes")

    out = sp_migrate.output
    assert "still refers" in out
    assert "user configuration scope" in out
    assert "active user configuration" in out
    assert old_user.exists()


def test_migrate_cleanup_old_refuses_symlink(mock_spack_instance, monkeypatch):
    home_dir, base_prefix = mock_spack_instance
    target = Path(home_dir) / "real-dot-spack"
    target.mkdir()
    (target / "config.yaml").write_text("config: {}\n", encoding="utf-8")
    (Path(home_dir) / ".spack").symlink_to(target)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    with pytest.raises(spack.main.SpackCommandError):
        sp_migrate("cleanup-old", "--yes")

    assert "symbolic link" in sp_migrate.output
    assert target.exists()
    assert (target / "config.yaml").exists()


@pytest.mark.not_on_windows("permission bits do not apply on Windows")
@pytest.mark.skipif(getuid() == 0, reason="root ignores permission bits")
def test_migrate_cleanup_old_reports_removal_failures(mock_spack_instance, monkeypatch):
    home_dir, base_prefix = mock_spack_instance
    old_user, _ = _setup_cleanup_old(home_dir)
    locked = old_user / "bootstrap" / "store"
    locked.chmod(0o555)
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    try:
        with pytest.raises(spack.main.SpackCommandError):
            sp_migrate("cleanup-old", "--yes")
        assert "Could not completely remove" in sp_migrate.output
        assert "blob" in sp_migrate.output
    finally:
        locked.chmod(0o755)


@pytest.mark.not_on_windows("Spack has no cross-process locks on Windows")
def test_migrate_use_new_layout_holds_the_migration_lock(mock_spack_instance, monkeypatch):
    """The layout scope and marker are removed and re-created under the migration lock, so a
    command started meanwhile waits rather than finding no decision and making its own."""
    _, base_prefix = mock_spack_instance
    old_envs = Path(base_prefix) / "var" / "spack" / "environments"
    (old_envs / "demo").mkdir(parents=True)
    (old_envs / "demo" / "spack.yaml").write_text("spack:\n  specs: []\n", encoding="utf-8")
    monkeypatch.setattr(spack.config, "CONFIG", spack.config.create())

    lock_path = spack.migrate._migration_lock_path()
    held_during_migration = []
    real_migrate = spack.migrate.migrate_spack_prefix

    def check_lock_then_migrate(old_resources):
        # Spack's locks are reentrant within a process: probe from another one
        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys, fcntl\n"
                "try:\n"
                "    fcntl.lockf(open(sys.argv[1], 'r+'), fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
                "    print('free')\n"
                "except FileNotFoundError:\n"
                "    print('free')\n"
                "except OSError:\n"
                "    print('held')\n",
                lock_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True,
        )
        held_during_migration.append(probe.stdout.strip())
        real_migrate(old_resources)

    monkeypatch.setattr(spack.migrate, "migrate_spack_prefix", check_lock_then_migrate)
    sp_migrate("use-new-layout")

    assert held_during_migration == ["held"]
    assert spack.migrate.migration_done()


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

    new_data = Path(home_dir) / ".local" / "share" / "spack"

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
        old_licenses.mkdir(parents=True)
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
    assert str(old_licenses) in spack.config.canonicalize_path(
        spack.config.CONFIG.get("config:license_dir")
    )
    assert str(old_envs) in spack.config.canonicalize_path(
        spack.config.CONFIG.get("config:environments_root")
    )
    assert str(old_gpg) in spack.config.canonicalize_path(
        spack.config.CONFIG.get("config:gpg_path")
    )

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

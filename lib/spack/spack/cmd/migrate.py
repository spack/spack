# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import spack.config
import spack.paths
import spack.util.filesystem as fs
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "undo auto-migration of licenses and environments"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "action", nargs="?", choices=["undo"], help="action to perform (only 'undo' is supported)"
    )
    subparser.add_argument(
        "--dry-run", action="store_true", help="show what would be done without actually doing it"
    )


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Undo auto-migration of licenses and environments.

    The `spack migrate undo` command restores the Spack instance to its
    pre-auto-migration state by copying licenses and environments from
    $spack/.migration-backup/ back to their original locations, updating
    the layout scope to point to those old locations, and removing the
    backup directory.

    IMPORTANT: This does NOT touch any files in shared $HOME directories
    (e.g., ~/.local/share/spack). Auto-migration copies (not moves) files,
    so the shared directories remain intact for other Spack instances.
    """
    if args.action != "undo":
        tty.die(
            "The manual `spack migrate` command has been deprecated.\n"
            "\n"
            "Auto-migration now happens automatically when you run Spack.\n"
            "If you need to undo auto-migration, use:\n"
            "  spack migrate undo\n"
            "\n"
            "For more information, see the Spack documentation."
        )

    # Get backup directory path
    backup_dir = spack.config._migration_backup_path()

    if not os.path.exists(backup_dir):
        tty.msg(f"No migration backup found at {backup_dir}")
        tty.msg("Nothing to undo.")
        return

    # Get old resource paths
    old_licenses_dir = spack.paths.old_licenses_path
    old_envs_dir = spack.paths.old_envs_path

    # Check what's in the backup
    backup_licenses = os.path.join(backup_dir, "licenses")
    backup_envs = os.path.join(backup_dir, "environments")

    has_licenses = os.path.exists(backup_licenses) and os.listdir(backup_licenses)
    has_envs = os.path.exists(backup_envs) and os.listdir(backup_envs)

    if not has_licenses and not has_envs:
        tty.msg(f"Backup directory exists but is empty: {backup_dir}")
        if args.dry_run:
            tty.msg(f"Would remove {backup_dir}")
        else:
            shutil.rmtree(backup_dir)
            tty.msg(f"Removed empty backup directory: {backup_dir}")
        return

    # Show what will be done
    if args.dry_run:
        tty.msg("Would perform the following operations:")
        if has_licenses:
            tty.msg(f"  - Restore licenses from {backup_licenses} to {old_licenses_dir}")
        if has_envs:
            tty.msg(f"  - Restore environments from {backup_envs} to {old_envs_dir}")
        tty.msg("  - Update layout scope to point to old locations")
        tty.msg(f"  - Remove backup directory: {backup_dir}")
        return

    # Perform the undo
    tty.msg("Undoing auto-migration...")

    # Restore licenses
    if has_licenses:
        # Check for conflicts
        if os.path.exists(old_licenses_dir):
            existing = set(os.listdir(old_licenses_dir))
            backup_files = set(os.listdir(backup_licenses))
            conflicts = existing & backup_files
            if conflicts:
                tty.die(
                    f"Cannot restore licenses: conflicts detected in {old_licenses_dir}:\n"
                    + "\n".join(f"  - {f}" for f in conflicts)
                    + "\n\nPlease resolve conflicts manually before running undo."
                )
        else:
            fs.mkdirp(old_licenses_dir)

        # Copy from backup to old location
        for entry in os.listdir(backup_licenses):
            src = os.path.join(backup_licenses, entry)
            dst = os.path.join(old_licenses_dir, entry)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        tty.msg(f"  Restored licenses to {old_licenses_dir}")

    # Restore environments
    if has_envs:
        # Check for conflicts
        if os.path.exists(old_envs_dir):
            existing = set(os.listdir(old_envs_dir))
            backup_files = set(os.listdir(backup_envs))
            conflicts = existing & backup_files
            if conflicts:
                tty.die(
                    f"Cannot restore environments: conflicts detected in {old_envs_dir}:\n"
                    + "\n".join(f"  - {f}" for f in conflicts)
                    + "\n\nPlease resolve conflicts manually before running undo."
                )
        else:
            fs.mkdirp(old_envs_dir)

        # Copy from backup to old location
        for entry in os.listdir(backup_envs):
            src = os.path.join(backup_envs, entry)
            dst = os.path.join(old_envs_dir, entry)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        tty.msg(f"  Restored environments to {old_envs_dir}")

    # Update layout scope to point to old locations
    layout_scope_path = spack.config._layout_scope_path()
    config_yaml_path = os.path.join(layout_scope_path, "config.yaml")

    if os.path.exists(config_yaml_path):
        with open(config_yaml_path, "r", encoding="utf-8") as f:
            layout_config = syaml.load(f) or {}
    else:
        layout_config = {}

    if "config" not in layout_config:
        layout_config["config"] = {}

    # Point to old locations
    if has_licenses:
        layout_config["config"]["licenses_dir"] = old_licenses_dir
    if has_envs:
        layout_config["config"]["environments_root"] = old_envs_dir

    # Write updated layout scope
    fs.mkdirp(layout_scope_path)
    with open(config_yaml_path, "w", encoding="utf-8") as f:
        syaml.dump(layout_config, f)
    tty.msg(f"  Updated layout scope: {config_yaml_path}")

    # Remove backup directory
    shutil.rmtree(backup_dir)
    tty.msg(f"  Removed backup directory: {backup_dir}")

    tty.msg("\nUndo complete!")
    tty.msg(
        "\nNOTE: Files in shared directories (e.g., ~/.local/share/spack) were NOT touched.\n"
        "Auto-migration copies (not moves) files, so they remain available for other\n"
        "Spack instances."
    )

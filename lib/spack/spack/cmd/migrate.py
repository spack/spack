# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import spack.config
import spack.llnl.util.tty as tty
import spack.paths
import spack.util.spack_yaml as syaml

description = "migrate user config and cache from old to new locations"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be migrated without actually moving files",
    )
    subparser.add_argument(
        "--clear",
        action="store_true",
        help="move entire ~/.spack directory to backup location after migration",
    )
    subparser.add_argument(
        "--backup",
        type=str,
        help=(
            "specify custom backup location for ~/.spack "
            "(default: ~/.local/share/spack/dotspack_backup)"
        ),
    )


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Migrate user config and package repositories from ~/.spack to new locations.

    This command migrates:
    - User config files: ~/.spack/*.yaml -> ~/.config/spack/
    - Package repositories: ~/.spack/package_repos -> ~/.local/state/spack/package_repos
    - Updates $spack/etc/spack-new/config.yaml to use new locations
    """
    home = os.path.expanduser("~")
    old_location = os.path.join(home, ".spack")
    new_config_location = os.path.join(home, ".config", "spack")
    new_state_location = os.path.join(home, ".local", "state", "spack")

    if args.backup:
        backup_location = os.path.expanduser(args.backup)
    else:
        backup_location = os.path.join(home, ".local", "share", "spack", "dotspack_backup")

    spack_new_path = os.path.join(spack.paths.etc_path, "spack-new")
    spack_new_config = os.path.join(spack_new_path, "config.yaml")

    if not os.path.exists(old_location):
        tty.die(f"Old configuration location does not exist: {old_location}")

    # Check if backup already exists
    if args.clear and os.path.exists(backup_location):
        tty.die(f"Backup location already exists: {backup_location}")

    # Track what we'll migrate
    migrations = []

    # 1. Check for config files to migrate (*.yaml and *.yml files in ~/.spack/)
    config_files = []
    if os.path.isdir(old_location):
        for item in os.listdir(old_location):
            if item.endswith(".yaml") or item.endswith(".yml"):
                config_files.append(item)

    if config_files:
        if os.path.exists(new_config_location):
            existing_configs = [
                f
                for f in os.listdir(new_config_location)
                if f.endswith(".yaml") or f.endswith(".yml")
            ]
            if existing_configs and not args.dry_run:
                tty.warn(
                    f"New config location already contains config files: {new_config_location}\n"
                    f"  Existing files: {', '.join(existing_configs)}\n"
                    "  These will not be overwritten."
                )

        migrations.append(("config", config_files, old_location, new_config_location))

    # 2. Check for package repositories to migrate
    old_package_repos = os.path.join(old_location, "package_repos")
    new_package_repos = os.path.join(new_state_location, "package_repos")

    if os.path.exists(old_package_repos) and os.path.isdir(old_package_repos):
        repos = os.listdir(old_package_repos)
        if repos:
            if os.path.exists(new_package_repos):
                existing_repos = os.listdir(new_package_repos)
                if existing_repos and not args.dry_run:
                    tty.warn(
                        f"New package repository location already exists: {new_package_repos}\n"
                        f"  Existing repos: {', '.join(existing_repos)}\n"
                        "  These will not be overwritten."
                    )

            migrations.append(("package_repos", repos, old_package_repos, new_package_repos))

    if not migrations:
        tty.msg("Nothing to migrate - no config files or package repositories found in ~/.spack")
        return

    if args.dry_run:
        # Show what will be migrated
        tty.msg("Would migrate the following:")
        for migration_type, items, src, dst in migrations:
            if migration_type == "config":
                tty.msg(f"\n  Config files from {src}/ to {dst}/:")
                for item in items:
                    tty.msg(f"    - {item}")
            elif migration_type == "package_repos":
                tty.msg(f"\n  Package repositories from {src}/ to {dst}/:")
                for item in items:
                    tty.msg(f"    - {item}")

        # Show spack-new config update
        if os.path.exists(spack_new_config):
            tty.msg(f"\n  Update {spack_new_config}:")
            tty.msg(f"    config:user_cache_path: {new_state_location}")

        if args.clear:
            tty.msg(f"\n  Move ~/.spack to backup: {backup_location}")

        return

    # Perform migrations
    for migration_type, items, src, dst in migrations:
        # Ensure destination directory exists
        os.makedirs(dst, exist_ok=True)

        if migration_type == "config":
            for item in items:
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                if not os.path.exists(dst_path):
                    tty.debug(f"Copying {src_path} -> {dst_path}")
                    shutil.copy2(src_path, dst_path)
                else:
                    tty.debug(f"Skipping {item} (already exists at destination)")

        elif migration_type == "package_repos":
            for item in items:
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                if not os.path.exists(dst_path):
                    tty.debug(f"Copying {src_path} -> {dst_path}")
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                else:
                    tty.debug(f"Skipping {item} (already exists at destination)")

    tty.msg("\nMigration complete!")
    tty.msg(f"  Config location: {new_config_location}")
    tty.msg(f"  State location: {new_state_location}")

    # Update spack-new config.yaml to point user_cache_path to new location
    if os.path.exists(spack_new_config):
        try:
            with open(spack_new_config, "r") as f:
                config_data = syaml.load_config(f)

            if "config" not in config_data:
                config_data["config"] = {}

            config_data["config"]["user_cache_path"] = new_state_location

            with open(spack_new_config, "w") as f:
                syaml.dump_config(config_data, stream=f, default_flow_style=False)

            tty.msg(f"\nUpdated {spack_new_config}")
            tty.msg(f"  Set config:user_cache_path to {new_state_location}")
        except Exception as e:
            tty.warn(f"Could not update {spack_new_config}: {e}")

    if args.clear:
        os.makedirs(os.path.dirname(backup_location), exist_ok=True)
        shutil.move(old_location, backup_location)
        tty.msg(f"\nBackup complete! Original ~/.spack moved to {backup_location}")
    else:
        tty.msg("\nNote: ~/.spack still exists. Use --clear to move it to a backup location.")

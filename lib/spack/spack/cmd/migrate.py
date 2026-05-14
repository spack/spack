# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import spack.llnl.util.tty as tty
from spack.paths_base import locations as paths_base

description = "migrate user config and cache from old to new locations"
section = "config"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="show what would be migrated without actually moving files",
    )


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Migrate user config and package repositories from ~/.spack to new locations.

    This command migrates:
    - User config files: ~/.spack/*.yaml -> ~/.config/spack/
    - Package repositories: ~/.spack/package_repos -> ~/.local/state/spack/package_repos
    """
    old_location = os.path.expanduser("~/.spack")
    new_config_location = paths_base.user_config_path
    new_state_location = os.path.join(os.path.expanduser("~"), ".local", "state", "spack")

    # Check if old location exists
    if not os.path.exists(old_location):
        tty.die(f"Old configuration location does not exist: {old_location}")

    # Track what we'll migrate
    migrations = []
    errors = []

    # 1. Check for config files to migrate (*.yaml and *.yml files in ~/.spack/)
    config_files = []
    if os.path.isdir(old_location):
        for item in os.listdir(old_location):
            if item.endswith(".yaml") or item.endswith(".yml"):
                config_files.append(item)

    if config_files:
        # Check if new config location already has config files
        if os.path.exists(new_config_location):
            existing_configs = [
                f for f in os.listdir(new_config_location)
                if f.endswith(".yaml") or f.endswith(".yml")
            ]
            if existing_configs:
                errors.append(
                    f"New config location already contains config files: {new_config_location}\n"
                    f"  Existing files: {', '.join(existing_configs)}"
                )

        if not errors:
            migrations.append(
                ("config", config_files, old_location, new_config_location)
            )

    # 2. Check for package repositories to migrate
    old_package_repos = os.path.join(old_location, "package_repos")
    new_package_repos = os.path.join(new_state_location, "package_repos")

    if os.path.exists(old_package_repos) and os.path.isdir(old_package_repos):
        # Check if there's anything in it
        repos = os.listdir(old_package_repos)
        if repos:
            # Check if new location already has package repositories
            if os.path.exists(new_package_repos):
                existing_repos = os.listdir(new_package_repos)
                if existing_repos:
                    errors.append(
                        f"New package repository location already exists: {new_package_repos}\n"
                        f"  Existing repos: {', '.join(existing_repos)}"
                    )

            if not errors:
                migrations.append(
                    ("package_repos", repos, old_package_repos, new_package_repos)
                )

    # Report errors if any
    if errors:
        tty.die("Cannot migrate due to conflicts:\n  " + "\n  ".join(errors))

    # Report what we found
    if not migrations:
        tty.msg("Nothing to migrate - no config files or package repositories found in ~/.spack")
        return

    # Show what will be migrated
    tty.msg("Will migrate the following:")
    for migration_type, items, src, dst in migrations:
        if migration_type == "config":
            tty.msg(f"\n  Config files from {src}/ to {dst}/:")
            for item in items:
                tty.msg(f"    - {item}")
        elif migration_type == "package_repos":
            tty.msg(f"\n  Package repositories from {src}/ to {dst}/:")
            for item in items:
                tty.msg(f"    - {item}")

    if args.dry_run:
        tty.msg("\nDry run - no files were moved")
        return

    # Perform migrations
    tty.msg("\nMigrating files...")

    for migration_type, items, src, dst in migrations:
        # Ensure destination directory exists
        os.makedirs(dst, exist_ok=True)

        if migration_type == "config":
            # Move config files
            for item in items:
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                tty.debug(f"Moving {src_path} -> {dst_path}")
                shutil.move(src_path, dst_path)
            tty.msg(f"  Migrated {len(items)} config file(s) to {dst}")

        elif migration_type == "package_repos":
            # Move entire package_repos directory contents
            for item in items:
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                tty.debug(f"Moving {src_path} -> {dst_path}")
                shutil.move(src_path, dst_path)
            tty.msg(f"  Migrated {len(items)} package repositor(y|ies) to {dst}")

    tty.msg("\nMigration complete!")
    tty.msg(f"  Config location: {new_config_location}")
    tty.msg(f"  State location: {new_state_location}")

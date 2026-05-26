# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import spack.llnl.util.tty as tty
from spack.paths import locations as paths
from spack.paths_base import locations as paths_base

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
        help="move entire ~/.spack directory to backup location:"
        "use this if no other instances need this old location",
    )
    subparser.add_argument(
        "--clear-only",
        action="store_true",
        help="only move ~/.spack to backup without migrating files "
        "(useful after running migrate without --clear)",
    )
    subparser.add_argument(
        "--replace",
        action="store_true",
        help="replace existing files in new locations (use with --clear "
        "if you forgot to use --clear on first run)",
    )
    subparser.add_argument(
        "--restore",
        action="store_true",
        help="restore ~/.spack from backup location (after --clear)",
    )
    subparser.add_argument(
        "--i-need-old-spack",
        action="store_true",
        help="print help about mixing pre-1.2-Spack and Spack >= 1.2",
    )


def restore(args: argparse.Namespace) -> None:
    """Restore ~/.spack from backup location."""
    old_location = os.path.expanduser("~/.spack")

    # Check both the current backup location and the default one
    backup_locations = [paths.dotspack_backup]
    default_backup = os.path.join(paths.default_data_home, "dotspack_backup")
    if default_backup != paths.dotspack_backup:
        backup_locations.append(default_backup)

    # Find which backup location exists
    backup_location = None
    for loc in backup_locations:
        if os.path.exists(loc):
            backup_location = loc
            break

    if not backup_location:
        tty.die(
            "No backup found. Checked:\n" + "\n".join(f"  - {loc}" for loc in backup_locations)
        )

    # Check if ~/.spack already exists
    if os.path.exists(old_location):
        tty.die(f"Cannot restore: {old_location} already exists")

    if args.dry_run:
        tty.msg(f"Would restore from {backup_location} to {old_location}")
        return

    tty.msg(f"Restoring from {backup_location} to {old_location}...")
    shutil.copytree(backup_location, old_location)
    tty.msg("Restore complete!")


def i_need_old_spack():
    # Note: I specifically recommend SPACK_USER_CACHE_PATH= rather
    # than SPACK_STATE_HOME=..., because if a pre-1.2 instance *is*
    # eventually updated, it would take the existence of
    # SPACK_STATE_HOME as an indication to use new-style defaults
    # for installs etc., and ignore existing installs in
    # $spack/opt/spack
    print("""\
If you're getting a warning about using resources in ~/.spack, and
you have pre-1.2 Spack instances that cannot upgrade, you can run

  spack migrate

(without --clear). This will create a copy of the user config and
package repo for 1.2+ instances to use; that is usually fine, but
pre-1.2 instances and 1.2+ instances will have divergent config and
packages (unless e.g. SPACK_DISABLE_LOCAL_CONFIG is set).
          
Examples of divergence:

- pre-1.2 and 1.2 instances may have different notions of what
  compilers are available: (this is generally addressed by making
  sure to run `spack compiler add` for at least one instance of
  each category).
- `spack repo --update`: if run in a pre-1.2 instance, will not
  affect 1.2+ instances.

You can avoid this divergence issue by forcing new spack instances
to also use ~/.spack (which will silence this warning).

If a new instance sees SPACK_USER_CACHE_PATH=~/.spack, that will
silence the warning.

Other explicit uses of ~/.spack will also silence this warning
(e.g. setting `config:locations:state:~/.spack`, or pointing
the user scope's `path` to `~/.spack`).
""")


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Migrate user config and package repositories from ~/.spack to new locations.

    This command migrates:
    - User config files: ~/.spack/...yaml -> ~/.config/spack/
    - Package repositories: ~/.spack/package_repos -> ~/.local/state/spack/package_repos
    """
    if args.i_need_old_spack:
        i_need_old_spack()
        return

    if args.restore:
        restore(args)
        return

    old_location = os.path.expanduser("~/.spack")
    new_config_location = paths_base.user_config_path
    new_state_location = os.path.join(os.path.expanduser("~"), ".local", "state", "spack")
    backup_location = paths.dotspack_backup

    if args.clear_only:
        if not os.path.exists(old_location):
            tty.die(f"Old configuration location does not exist: {old_location}")
        if os.path.exists(backup_location):
            tty.die(f"Backup location already exists: {backup_location}")

        if args.dry_run:
            tty.msg(f"Would move {old_location} to {backup_location}")
            return

        os.makedirs(os.path.dirname(backup_location), exist_ok=True)
        shutil.move(old_location, backup_location)
        tty.msg(f"Backup complete! Original ~/.spack moved to {backup_location}")
        return

    # Handle --replace: delete destination directories before migrating
    if args.replace:
        if os.path.exists(new_config_location):
            tty.msg(f"Removing existing config location: {new_config_location}")
            shutil.rmtree(new_config_location)
        new_package_repos = os.path.join(new_state_location, "package_repos")
        if os.path.exists(new_package_repos):
            tty.msg(f"Removing existing package repos: {new_package_repos}")
            shutil.rmtree(new_package_repos)

    if not os.path.exists(old_location):
        tty.die(f"Old configuration location does not exist: {old_location}")

    # Check if backup already exists
    if args.clear and os.path.exists(backup_location):
        tty.die(f"Backup location already exists: {backup_location}")

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
        if os.path.exists(new_config_location):
            existing_configs = [
                f
                for f in os.listdir(new_config_location)
                if f.endswith(".yaml") or f.endswith(".yml")
            ]
            if existing_configs:
                errors.append(
                    f"New config location already contains config files: {new_config_location}\n"
                    f"  Existing files: {', '.join(existing_configs)}"
                )

        if not errors:
            migrations.append(("config", config_files, old_location, new_config_location))

    # 2. Check for package repositories to migrate
    old_package_repos = os.path.join(old_location, "package_repos")
    new_package_repos = os.path.join(new_state_location, "package_repos")

    if os.path.exists(old_package_repos) and os.path.isdir(old_package_repos):
        repos = os.listdir(old_package_repos)
        if repos:
            if os.path.exists(new_package_repos):
                existing_repos = os.listdir(new_package_repos)
                if existing_repos:
                    errors.append(
                        f"New package repository location already exists: {new_package_repos}\n"
                        f"  Existing repos: {', '.join(existing_repos)}"
                    )

            if not errors:
                migrations.append(("package_repos", repos, old_package_repos, new_package_repos))

    if errors:
        tty.msg("Migration conflicts detected (files already in new locations):")
        for error in errors:
            tty.msg(f"  {error}")
        tty.msg("\nSkipping migration and backup/clear due to conflicts")
        # Exit early here regardless of --clear (we shouldn't move .spack if
        # we couldn't copy out the components we want)
        return
    elif not migrations:
        tty.msg("Nothing to migrate - no config files or package repositories found in ~/.spack")

    if args.dry_run:
        # Show what will be migrated
        if migrations:
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
        return

    if migrations:
        for migration_type, items, src, dst in migrations:
            # Ensure destination directory exists
            os.makedirs(dst, exist_ok=True)

            if migration_type == "config":
                for item in items:
                    src_path = os.path.join(src, item)
                    dst_path = os.path.join(dst, item)
                    tty.debug(f"Copying {src_path} -> {dst_path}")
                    shutil.copy2(src_path, dst_path)

            elif migration_type == "package_repos":
                for item in items:
                    src_path = os.path.join(src, item)
                    dst_path = os.path.join(dst, item)
                    tty.debug(f"Copying {src_path} -> {dst_path}")
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)

        tty.msg("\nMigration complete!")
        tty.msg(f"  Config location: {new_config_location}")
        tty.msg(f"  State location: {new_state_location}")

    if args.clear:
        os.makedirs(os.path.dirname(backup_location), exist_ok=True)
        shutil.move(old_location, backup_location)
        tty.msg(f"Backup complete! Original ~/.spack moved to {backup_location}")

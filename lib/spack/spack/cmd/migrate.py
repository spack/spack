# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import spack.llnl.util.tty as tty

description = "migrate user config from ~/.spack to ~/.config/spack"
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
        "--i-need-old-spack",
        action="store_true",
        help="print help about mixing pre-1.2 Spack and Spack >= 1.2",
    )


def i_need_old_spack():
    """Print information about running old and new Spack versions together."""
    print("""\
If you're getting a warning about using resources in ~/.spack, and
you have pre-1.2 Spack instances that cannot upgrade, you can run

  spack migrate

(without --clear). This will create a copy of the user config for
1.2+ instances to use; that is usually fine, but pre-1.2 instances
and 1.2+ instances will have divergent config (unless e.g.
SPACK_DISABLE_LOCAL_CONFIG is set).

About divergence:

Pre-1.2 instances will use ~/.spack, and 1.2+ instances (including
those that upgrade to 1.2+) will use ~/.config/spack. This means for
example that pre-1.2 and 1.2+ instances may have different notions
of what compilers are available.

You can avoid this divergence issue by forcing new Spack instances
to also use ~/.spack (which will silence the warning).
""")


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Migrate user config files from ~/.spack to ~/.config/spack.

    This command copies config files (*.yaml, *.yml) from ~/.spack/ to
    ~/.config/spack/ to support the new XDG-compliant directory layout.
    """
    if args.i_need_old_spack:
        i_need_old_spack()
        return

    old_location = os.path.expanduser("~/.spack")
    new_config_location = os.path.expanduser("~/.config/spack")
    backup_location = os.path.expanduser("~/.spack.backup")

    if not os.path.exists(old_location):
        tty.msg(f"Old configuration location does not exist: {old_location}")
        tty.msg("Nothing to migrate.")
        return

    # Check if backup already exists (for --clear)
    if args.clear and os.path.exists(backup_location):
        tty.die(f"Backup location already exists: {backup_location}")

    # Find config files to migrate
    config_files = []
    if os.path.isdir(old_location):
        for item in os.listdir(old_location):
            if item.endswith(".yaml") or item.endswith(".yml"):
                config_files.append(item)

    if not config_files:
        tty.msg("No config files found in ~/.spack to migrate.")
        if args.clear:
            # Still do the backup if --clear was requested
            if args.dry_run:
                tty.msg(f"Would move {old_location} to {backup_location}")
            else:
                tty.msg(f"Moving {old_location} to {backup_location}...")
                shutil.move(old_location, backup_location)
                tty.msg("Backup complete!")
        return

    # Check for conflicts in new location
    conflicts = []
    if os.path.exists(new_config_location):
        for config_file in config_files:
            new_path = os.path.join(new_config_location, config_file)
            if os.path.exists(new_path):
                conflicts.append(config_file)

    if conflicts:
        tty.die(
            f"Migration conflicts detected - these files already exist in {new_config_location}:\n"
            + "\n".join(f"  - {f}" for f in conflicts)
            + "\n\nPlease resolve conflicts manually before migrating."
        )

    # Show what will be migrated
    if args.dry_run:
        tty.msg("Would migrate the following:")
        tty.msg(f"\n  Config files from {old_location}/ to {new_config_location}/:")
        for config_file in config_files:
            tty.msg(f"    - {config_file}")
        if args.clear:
            tty.msg(f"\nWould then move {old_location} to {backup_location}")
        return

    # Perform the migration
    os.makedirs(new_config_location, exist_ok=True)
    tty.msg(f"Migrating config files from {old_location} to {new_config_location}...")

    for config_file in config_files:
        old_path = os.path.join(old_location, config_file)
        new_path = os.path.join(new_config_location, config_file)
        shutil.copy2(old_path, new_path)
        tty.msg(f"  Copied: {config_file}")

    tty.msg("Migration complete!")

    # Handle --clear: move ~/.spack to backup
    if args.clear:
        tty.msg(f"\nMoving {old_location} to {backup_location}...")
        shutil.move(old_location, backup_location)
        tty.msg(f"Backup complete! Original ~/.spack moved to {backup_location}")
        tty.msg(f"\nYou can restore it with:\n  mv {backup_location} {old_location}")

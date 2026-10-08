# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import spack.config
import spack.paths
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "manage migration of Spack resources"
section = "config"
level = "long"


def _restore_user_scope_path() -> None:
    """Point the standard user scope back at the legacy ~/.spack location."""
    include_path = os.path.join(spack.paths.etc_path, "standard_scopes", "include.yaml")
    with open(include_path, "r", encoding="utf-8") as f:
        include_config = syaml.load(f) or {}

    includes = include_config.get("include", [])
    for entry in includes:
        if isinstance(entry, dict) and entry.get("name") == "user":
            entry["path"] = "~/.spack"
            break
    else:
        tty.die(f"Cannot restore user scope: no user entry in {include_path}")

    with open(include_path, "w", encoding="utf-8") as f:
        syaml.dump(include_config, f)
    tty.msg(f"  Updated user scope: {include_path}")


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "action",
        choices=["undo", "cleanup-old", "use-new-layout"],
        help="migration action to perform",
    )
    subparser.add_argument(
        "--dry-run", action="store_true", help="show what would be done without actually doing it"
    )
    subparser.add_argument(
        "--restore-old-user-scope",
        action="store_true",
        help=(
            "restore the user scope to ~/.spack (changes git-managed config in the"
            " Spack repository)"
        ),
    )

    subparser.epilog = (
        "WARNING:\n"
        "  Do not run this command in parallel with other spack commands for the same\n"
        "  Spack instance. This command modifies configuration files that other processes\n"
        "  may be reading, and does not use locking to coordinate with them."
    )


def _under_old_dotspack(path: str) -> bool:
    old_path = os.path.realpath(os.path.expanduser("~/.spack"))
    try:
        return (
            os.path.commonpath([old_path, os.path.realpath(os.path.expanduser(path))]) == old_path
        )
    except ValueError:
        return False


def _cleanup_old() -> None:
    old_path = os.path.expanduser("~/.spack")
    if not os.path.isdir(old_path):
        tty.msg(f"No old user directory found at {old_path}")
        return

    references = []
    user_scope = spack.config.CONFIG.scopes.get("user")
    if (
        user_scope is not None
        and hasattr(user_scope, "path")
        and _under_old_dotspack(user_scope.path)
    ):
        references.append(f"user scope ({user_scope.path})")

    if _under_old_dotspack(spack.paths.user_cache_path):
        references.append(f"user cache ({spack.paths.user_cache_path})")

    for config_var in ("config:license_dir", "config:gpg_path", "config:environments_root"):
        value = spack.config.CONFIG.get(config_var, None)
        if not value:
            continue
        if _under_old_dotspack(value):
            references.append(f"{config_var} ({value})")

    if references:
        tty.die(
            "Cannot remove ~/.spack because the active configuration still refers to it:\n"
            + "\n".join(f"  - {reference}" for reference in references)
        )

    shutil.rmtree(old_path)
    tty.msg(f"Removed old user directory: {old_path}")


def _use_new_layout(args):
    """Remove layout scope and trigger migration to new XDG locations."""
    layout_scope_path = os.path.join(spack.paths.etc_path, "layout")
    marker_path = spack.config._migration_done_marker_path()

    old_resources = spack.config._detect_old_resources()

    if not any(old_resources.values()):
        tty.msg("No old resources: nothing to migrate")
        return

    if args.dry_run:
        if os.path.exists(layout_scope_path) or os.path.exists(marker_path):
            tty.msg(f"Would remove layout scope: {layout_scope_path}")
        tty.msg("Would trigger migration to new XDG layout")
        return
    else:
        if os.path.exists(layout_scope_path):
            tty.msg(f"Removing layout scope: {layout_scope_path}")
            shutil.rmtree(layout_scope_path)
            tty.msg("  Layout scope removed")
        if os.path.exists(marker_path):
            os.remove(marker_path)

    spack.config._do_migrate_spack_prefix(old_resources)


def _undo(args):
    """Undo migration by pointing all resources back to their old locations."""

    old_resources = spack.config._detect_old_resources()

    if not any(old_resources.values()):
        tty.die(
            "Nothing to do: this spack instance has no old resources, and would not have "
            "been migrated."
        )

    if args.dry_run:
        tty.msg("Would perform the following operations:")
        if old_resources.get("licenses"):
            tty.msg(f"  - Point license_dir back to {spack.paths.old_licenses_path}")
        if old_resources.get("environments"):
            tty.msg(f"  - Point environments_root back to {spack.paths.old_envs_path}")
        if old_resources.get("gpg_keys"):
            tty.msg(f"  - Point gpg_path back to {spack.paths.old_gpg_path}")
            tty.msg(f"  - Point gpg_keys_path back to {spack.paths.old_gpg_keys_path}")
        # Installs are never migrated, so don't need to mention that
        tty.msg("  - Update layout scope to use old locations")
        if args.restore_old_user_scope:
            tty.msg("  - Update standard scopes to use ~/.spack for the user scope")
        return

    tty.msg("Undoing migration...")

    # In the context of prompted migration, this is locked, but this command
    # does not hold .migration-lock because all other spack commands would
    # have to hold it for their entire duration to safely interact (which
    # seems expensive for something that would be used rarely).
    spack.config._force_old_layout(old_resources, print_message=False)

    tty.msg("  Updated layout scope to point to old locations")

    if args.restore_old_user_scope:
        _restore_user_scope_path()

    tty.msg("\nUndo complete!")
    tty.msg(
        "\nNOTE: Old resources remain at their original locations. New locations may be\n"
        "left in place for other Spack instances to use, or manually removed if desired."
    )


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.action == "cleanup-old":
        _cleanup_old()
    elif args.action == "undo":
        _undo(args)
    elif args.action == "use-new-layout":
        _use_new_layout(args)
    else:
        raise AssertionError("Unexpected: should be one of: [cleanup-old, undo, use-new-layout]")

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
        "action", nargs="?", choices=["undo", "cleanup-old"], help="migration action to perform"
    )
    subparser.add_argument(
        "--dry-run", action="store_true", help="show what would be done without actually doing it"
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
        if value and _under_old_dotspack(value):
            references.append(f"{config_var} ({value})")

    if references:
        tty.die(
            "Cannot remove ~/.spack because the active configuration still refers to it:\n"
            + "\n".join(f"  - {reference}" for reference in references)
        )

    shutil.rmtree(old_path)
    tty.msg(f"Removed old user directory: {old_path}")


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Undo auto-migration of licenses and environments.

    The `spack migrate undo` command updates the layout scope to point all
    resources back to their old locations. Old resources remain at their
    original locations (migration copies them, leaving originals in place).
    New locations may be left in place for other Spack instances to use,
    or manually removed if desired.
    """
    if args.action == "cleanup-old":
        _cleanup_old()
        return

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

    # Check if migration marker exists
    marker_path = spack.config._migration_done_marker_path()
    if not os.path.exists(marker_path):
        tty.msg("No migration has been performed.")
        tty.msg("Nothing to undo.")
        return

    # Get old resource paths
    old_licenses_dir = spack.paths.old_licenses_path
    old_envs_dir = spack.paths.old_envs_path
    old_gpg_dir = spack.paths.old_gpg_path
    old_gpg_keys_dir = spack.paths.old_gpg_keys_path

    # Check what old resources exist
    has_licenses = os.path.exists(old_licenses_dir)
    has_envs = os.path.exists(old_envs_dir)
    has_gpg = os.path.exists(old_gpg_dir)

    if not has_licenses and not has_envs and not has_gpg:
        tty.msg("No old resources found to point back to.")
        tty.msg("Nothing to undo.")
        return

    # Show what will be done
    if args.dry_run:
        tty.msg("Would perform the following operations:")
        if has_licenses:
            tty.msg(f"  - Point license_dir back to {old_licenses_dir}")
        if has_envs:
            tty.msg(f"  - Point environments_root back to {old_envs_dir}")
        if has_gpg:
            tty.msg(f"  - Point gpg_path back to {old_gpg_dir}")
            tty.msg(f"  - Point gpg_keys_path back to {old_gpg_keys_dir}")
        tty.msg("  - Update layout scope to use old locations")
        tty.msg("  - Update standard scopes to use ~/.spack for the user scope")
        return

    # Perform the undo
    tty.msg("Undoing auto-migration...")

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
        layout_config["config"]["license_dir"] = old_licenses_dir
        tty.msg(f"  Pointing license_dir to {old_licenses_dir}")
    if has_envs:
        layout_config["config"]["environments_root"] = old_envs_dir
        tty.msg(f"  Pointing environments_root to {old_envs_dir}")
    if has_gpg:
        layout_config["config"]["gpg_path"] = old_gpg_dir
        layout_config["config"]["gpg_keys_path"] = old_gpg_keys_dir
        tty.msg(f"  Pointing gpg_path to {old_gpg_dir}")
        tty.msg(f"  Pointing gpg_keys_path to {old_gpg_keys_dir}")

    layout_config["config"].setdefault("locations", {})["state"] = [os.path.expanduser("~/.spack")]

    # Write updated layout scope
    fs.mkdirp(layout_scope_path)
    with open(config_yaml_path, "w", encoding="utf-8") as f:
        syaml.dump(layout_config, f)
    tty.msg(f"  Updated layout scope: {config_yaml_path}")

    # Restore the legacy user-scope default at the scope that defines it. This
    # must be above layout in precedence and therefore cannot be represented in
    # the layout scope itself.
    _restore_user_scope_path()

    tty.msg("\nUndo complete!")
    tty.msg(
        "\nNOTE: Old resources remain at their original locations. New locations may be\n"
        "left in place for other Spack instances to use, or manually removed if desired."
    )

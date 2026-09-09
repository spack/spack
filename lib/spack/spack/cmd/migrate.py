# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union

import spack.config
import spack.paths
import spack.util.filesystem as fs
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "undo auto-migration of licenses and environments"
section = "config"
level = "long"


class Index:
    """Represents a list index in a YAML path."""

    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return f"Index({self.idx})"


def backup_location():
    """Return the backup location for ~/.spack (in $state_home/dotspack_backup)."""
    state_home = spack.config.substitute_path_variables("$state_home")
    return os.path.join(state_home, "dotspack_backup")


def walk_yaml_for_paths(
    data: Any,
    config_file_dir: str,
    key_path: Optional[List[Union[str, Index]]] = None,
    in_include: bool = False,
) -> List[Tuple[List[Union[str, Index]], str, str, bool]]:
    """Walk YAML data and find all string values that exist as filesystem paths.

    Args:
        data: YAML data structure (dict, list, or scalar)
        config_file_dir: Directory containing the config file (for resolving relative paths)
        key_path: Current path through the YAML structure (list of str keys or Index objects)
        in_include: Whether we're currently inside an include: section

    Returns:
        List of (key_path, original_value, resolved_abs_path, in_include) tuples
        for all string values that exist as filesystem paths.
        key_path is a list of str (dict keys) or Index (list indices).
    """
    if key_path is None:
        key_path = []

    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            # Track if we're entering an include section
            is_include_section = key == "include"
            child_in_include = in_include or is_include_section

            if isinstance(value, (dict, list)):
                nested = walk_yaml_for_paths(
                    value, config_file_dir, key_path + [key], child_in_include
                )
                results.extend(nested)
            elif isinstance(value, str):
                abs_path = resolve_and_check_path(value, config_file_dir)
                if abs_path:
                    results.append((key_path + [key], value, abs_path, child_in_include))

    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, (dict, list)):
                nested = walk_yaml_for_paths(
                    item, config_file_dir, key_path + [Index(idx)], in_include
                )
                results.extend(nested)
            elif isinstance(item, str):
                abs_path = resolve_and_check_path(item, config_file_dir)
                if abs_path:
                    results.append((key_path + [Index(idx)], item, abs_path, in_include))

    return results


def resolve_and_check_path(value: str, config_file_dir: str) -> str:
    """Resolve a potential path and check if it exists.

    Args:
        value: String that might be a path
        config_file_dir: Directory to resolve relative paths against

    Returns:
        Absolute path if it exists, empty string otherwise
    """
    if not value or not isinstance(value, str):
        return ""

    # Skip env/config vars:
    # - They are already absolute
    # - The ones that point into ~, include: cannot use
    if value.startswith("$"):
        return ""

    if os.path.isabs(value):
        return value if os.path.exists(value) else ""

    # Try resolving as relative to the config file directory
    candidate = os.path.normpath(os.path.join(config_file_dir, value))
    return candidate if os.path.exists(candidate) else ""


def absolutize_path_in_yaml(
    data: Any, key_path_parts: List[Union[str, Index]], new_value: str
) -> None:
    """Navigate to a location in YAML data and replace the value.

    Args:
        data: Root YAML data structure
        key_path_parts: Path components to navigate (list of str or Index objects)
        new_value: New value to set

    Raises:
        KeyError: If a dict key in the path doesn't exist
        IndexError: If a list index in the path is out of range
        TypeError: If trying to index into a non-dict/non-list
    """
    current = data

    for key in key_path_parts[:-1]:
        if isinstance(key, Index):
            current = current[key.idx]
        else:
            current = current[key]

    final_key = key_path_parts[-1]
    if isinstance(final_key, Index):
        current[final_key.idx] = new_value
    else:
        current[final_key] = new_value


def process_config_file_paths(
    file_path: str, old_location: str, new_config_location: str
) -> Tuple[Optional[Dict[str, Any]], List[Tuple[str, str, str]]]:
    """Process a config file to absolutize relative paths (except in include sections).

    Also rewrites absolute paths in include sections that point to old_location.

    Args:
        file_path: Path to the config file
        old_location: Old config location (e.g., ~/.spack)
        new_config_location: New config location (e.g., ~/.config/spack)

    Returns:
        Tuple of (modified_data, path_info) where:
        - modified_data is the modified YAML dict if changes were made,
          None if no changes were needed or if the file was empty
        - path_info is [(key_path_str, original_value, action), ...]
          where action is one of: "absolutized", "kept-relative", "rewritten"
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = syaml.load(f)

    if not data:
        return None, []

    config_dir = os.path.dirname(file_path)
    found_paths = walk_yaml_for_paths(data, config_dir)

    path_info = []
    modified = False

    old_location_norm = os.path.normpath(os.path.abspath(old_location))
    new_config_location_norm = os.path.normpath(os.path.abspath(new_config_location))

    for key_path, original_value, abs_path, in_include in found_paths:
        # Build human-readable path string for reporting
        path_parts = []
        for part in key_path:
            if isinstance(
                part, Index
            ):  # Implement __str__ for Index so we can just str() everything
                path_parts.append(f"[{part.idx}]")
            else:
                path_parts.append(part)
        key_path_str = ".".join(path_parts)

        if os.path.isabs(original_value):
            if in_include:
                # Check if it points to something under old_location
                abs_path_norm = os.path.normpath(os.path.abspath(original_value))
                try:
                    rel_path = os.path.relpath(abs_path_norm, old_location_norm)
                    # If relpath doesn't start with "..", it's under old_location
                    # (os.pardir is ".." on Unix/Windows, but use string check after normpath)
                    if not os.path.normpath(rel_path).startswith(".."):
                        # Rewrite to point to new location
                        new_path = os.path.join(new_config_location_norm, rel_path)
                        absolutize_path_in_yaml(data, key_path, new_path)
                        path_info.append((key_path_str, original_value, "rewritten"))
                        modified = True
                except ValueError:
                    # Different drives on Windows, can't compute relative path
                    pass
        else:
            # Relative path
            path_info.append(
                (key_path_str, original_value, "kept-relative" if in_include else "absolutized")
            )

            # Only absolutize if NOT in an include section
            if not in_include:
                absolutize_path_in_yaml(data, key_path, abs_path)
                modified = True

    return data if modified else None, path_info


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "action",
        nargs="?",
        choices=["undo"],
        help="action to perform (only 'undo' is supported)",
    )
    subparser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be done without actually doing it",
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
        tty.msg(f"  - Update layout scope to point to old locations")
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
        f"\nNOTE: Files in shared directories (e.g., ~/.local/share/spack) were NOT touched.\n"
        f"Auto-migration copies (not moves) files, so they remain available for other\n"
        f"Spack instances."
    )

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union

import spack.config
import spack.util.filesystem as fs
import spack.util.spack_yaml as syaml
from spack.util import tty


class Index:
    """Represents a list index in a YAML path."""

    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return f"Index({self.idx})"

description = "migrate user config from ~/.spack to ~/.config/spack"
section = "config"
level = "long"


def backup_location():
    """Return the backup location for ~/.spack (in $state_home/dotspack_backup)."""
    state_home = spack.config.substitute_path_variables("$state_home")
    return os.path.join(state_home, "dotspack_backup")


def walk_yaml_for_paths(
    data: Any,
    config_file_dir: str,
    key_path: List[Union[str, Index]] = None,
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

            # Recurse into nested structures
            if isinstance(value, (dict, list)):
                nested = walk_yaml_for_paths(
                    value, config_file_dir, key_path + [key], child_in_include
                )
                results.extend(nested)
            elif isinstance(value, str):
                # Check if this string is a path that exists
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
                # Check if this string is a path that exists
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

    # Skip Spack path variables (they're not filesystem paths yet)
    if value.startswith("$"):
        return ""

    # Check if it's already absolute and exists
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

    # Navigate to parent
    for key in key_path_parts[:-1]:
        if isinstance(key, Index):
            current = current[key.idx]
        else:
            current = current[key]

    # Update the final key
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

    # Normalize paths for comparison
    old_location_norm = os.path.normpath(os.path.abspath(old_location))
    new_config_location_norm = os.path.normpath(os.path.abspath(new_config_location))

    for key_path, original_value, abs_path, in_include in found_paths:
        # Build human-readable path string for reporting
        path_parts = []
        for part in key_path:
            if isinstance(part, Index):
                path_parts.append(f"[{part.idx}]")
            else:
                path_parts.append(part)
        key_path_str = ".".join(path_parts)

        if os.path.isabs(original_value):
            # Absolute path
            if in_include:
                # Check if it points to something under old_location
                abs_path_norm = os.path.normpath(os.path.abspath(original_value))
                try:
                    rel_path = os.path.relpath(abs_path_norm, old_location_norm)
                    # If relpath doesn't start with "..", it's under old_location
                    if not rel_path.startswith(".."):
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
            path_info.append((key_path_str, original_value, "kept-relative" if in_include else "absolutized"))

            # Only absolutize if NOT in an include section
            if not in_include:
                absolutize_path_in_yaml(data, key_path, abs_path)
                modified = True

    return data if modified else None, path_info


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
        "--restore",
        action="store_true",
        help="restore ~/.spack from backup location (reverses --clear)",
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
to also use ~/.spack (which will silence the warning) or by forcing
old Spack instances to use `~/.config/spack`. For all versions after
Spack v1.0, this can be done in the `includes` section of the Spack
config scope in `$spack/etc/spack/include.yaml`.
""")


def migrate(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Migrate user config files from ~/.spack to ~/.config/spack.

    This command copies config files (...yaml, ...yml) from ~/.spack/ to
    ~/.config/spack/ to support the new XDG-compliant directory layout.
    """
    if args.i_need_old_spack:
        i_need_old_spack()
        return

    old_location = os.path.expanduser("~/.spack")
    new_config_location = os.path.expanduser("~/.config/spack")
    backup_loc = backup_location()

    # Handle --restore
    if args.restore:
        if not os.path.exists(backup_loc):
            tty.die(
                f"Backup location does not exist: {backup_loc}"
                "\nIf you have moved $state_home (e.g. by setting"
                "\nSPACK_STATE_HOME) since the time that the backup"
                "\nwas created, restoring the previous value should"
                "\nbe enough for this command to succeed."
            )

        if os.path.exists(old_location):
            tty.die(
                f"Cannot restore: {old_location} already exists.\n"
                f"Please remove or rename it before restoring from backup."
            )

        if args.dry_run:
            tty.msg(f"Would move {backup_loc} to {old_location}")
        else:
            tty.msg(f"Restoring {backup_loc} to {old_location}...")
            shutil.move(backup_loc, old_location)
            tty.msg("Restore complete!")
        return

    if not os.path.exists(old_location):
        tty.msg(f"Old configuration location does not exist: {old_location}")
        tty.msg("Nothing to migrate.")
        return

    # Check if backup already exists (for --clear)
    if args.clear and os.path.exists(backup_loc):
        tty.die(f"Backup location already exists: {backup_loc}")

    # Find config files to migrate (recursively)
    config_files = []
    if os.path.isdir(old_location):
        found = fs.find(old_location, ["*.yaml", "*.yml"], recursive=True)
        # Convert absolute paths to relative paths from old_location
        config_files = [os.path.relpath(f, old_location) for f in found]

    if not config_files:
        tty.msg("No config files found in ~/.spack to migrate.")
        if args.clear:
            # Still do the backup if --clear was requested
            if args.dry_run:
                tty.msg(f"Would move {old_location} to {backup_loc}")
            else:
                tty.msg(f"Moving {old_location} to {backup_loc}...")
                shutil.move(old_location, backup_loc)
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

        all_path_info = []
        for config_file in config_files:
            old_path = os.path.join(old_location, config_file)
            # Check for paths even in dry-run
            _, path_info = process_config_file_paths(old_path, old_location, new_config_location)
            if path_info:
                all_path_info.extend(
                    (config_file, key_path, value, action)
                    for key_path, value, action in path_info
                )
                tty.msg(f"    - {config_file} (contains {len(path_info)} path(s) to process)")
            else:
                tty.msg(f"    - {config_file}")

        if all_path_info:
            tty.msg("\n  Paths that would be processed:")
            for config_file, key_path, value, action in all_path_info:
                if action == "absolutized":
                    status = "(would absolutize)"
                elif action == "kept-relative":
                    status = "(would keep relative - in include)"
                elif action == "rewritten":
                    status = "(would rewrite to new location)"
                else:
                    status = f"({action})"
                tty.msg(f"    {config_file}:{key_path} = {value} {status}")

        if args.clear:
            tty.msg(f"\nWould then move {old_location} to {backup_loc}")
        return

    # Perform the migration
    os.makedirs(new_config_location, exist_ok=True)
    tty.msg(f"Migrating config files from {old_location} to {new_config_location}...")

    all_path_info = []

    for config_file in config_files:
        old_path = os.path.join(old_location, config_file)
        new_path = os.path.join(new_config_location, config_file)

        # Process the file to handle paths
        modified_data, path_info = process_config_file_paths(old_path, old_location, new_config_location)

        # Track paths for reporting
        if path_info:
            all_path_info.extend(
                (config_file, key_path, value, action)
                for key_path, value, action in path_info
            )

        # Write the file (modified if needed, otherwise copy)
        # Ensure parent directory exists for nested files
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        if modified_data is not None:
            # Write modified YAML
            with open(new_path, "w", encoding="utf-8") as f:
                syaml.dump(modified_data, f)
            tty.msg(f"  Copied (with modified paths): {config_file}")
        else:
            # No modifications needed, just copy
            shutil.copy2(old_path, new_path)
            tty.msg(f"  Copied: {config_file}")

    tty.msg("Migration complete!")

    # Report paths that were processed
    if all_path_info:
        tty.warn("Processed paths in config files:")
        for config_file, key_path, value, action in all_path_info:
            if action == "absolutized":
                status = "(converted to absolute)"
            elif action == "kept-relative":
                status = "(kept relative - in include)"
            elif action == "rewritten":
                status = "(rewritten to new location)"
            else:
                status = f"({action})"
            tty.msg(f"  {config_file}:{key_path} = {value} {status}")

    # Handle --clear: move ~/.spack to backup
    if args.clear:
        tty.msg(f"\nMoving {old_location} to {backup_loc}...")
        shutil.move(old_location, backup_loc)
        tty.msg(f"Backup complete! Original ~/.spack moved to {backup_loc}")
        tty.msg("\nYou can restore it with:\n  spack migrate --restore")

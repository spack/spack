# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
from typing import Any, Dict, List, Set, Tuple

import spack.config
import spack.util.filesystem as fs
import spack.util.spack_yaml as syaml
from spack.util import tty

description = "migrate user config from ~/.spack to ~/.config/spack"
section = "config"
level = "long"


def backup_location():
    """Return the backup location for ~/.spack (in $state_home/dotspack_backup)."""
    state_home = spack.config.substitute_path_variables("$state_home")
    return os.path.join(state_home, "dotspack_backup")


def walk_yaml_for_paths(
    data: Any, config_file_dir: str, key_path: List[str] = None, in_include: bool = False
) -> List[Tuple[str, str, str, bool]]:
    """Walk YAML data and find all string values that exist as filesystem paths.

    Args:
        data: YAML data structure (dict, list, or scalar)
        config_file_dir: Directory containing the config file (for resolving relative paths)
        key_path: Current path through the YAML structure
        in_include: Whether we're currently inside an include: section

    Returns:
        List of (key_path_str, original_value, resolved_abs_path, in_include) tuples
        for all string values that exist as filesystem paths
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
                    path_str = ".".join(str(k) for k in key_path + [key])
                    results.append((path_str, value, abs_path, child_in_include))

    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, (dict, list)):
                nested = walk_yaml_for_paths(
                    item, config_file_dir, key_path + [f"[{idx}]"], in_include
                )
                results.extend(nested)
            elif isinstance(item, str):
                # Check if this string is a path that exists
                abs_path = resolve_and_check_path(item, config_file_dir)
                if abs_path:
                    path_str = ".".join(str(k) for k in key_path + [f"[{idx}]"])
                    results.append((path_str, item, abs_path, in_include))

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


def absolutize_path_in_yaml(data: Any, key_path_parts: List[str], new_value: str) -> bool:
    """Navigate to a location in YAML data and replace the value.

    Args:
        data: Root YAML data structure
        key_path_parts: Path components to navigate (e.g., ['config', 'paths', '[0]'])
        new_value: New value to set

    Returns:
        True if the value was updated, False otherwise
    """
    current = data

    # Navigate to parent
    for key in key_path_parts[:-1]:
        if key.startswith("[") and key.endswith("]"):
            # List index
            idx = int(key.strip("[]"))
            current = current[idx]
        else:
            # Dict key
            current = current[key]

    # Update the final key
    final_key = key_path_parts[-1]
    if final_key.startswith("[") and final_key.endswith("]"):
        idx = int(final_key.strip("[]"))
        current[idx] = new_value
    else:
        current[final_key] = new_value

    return True


def process_config_file_paths(
    file_path: str,
) -> Tuple[Dict[str, Any], List[Tuple[str, str, bool]]]:
    """Process a config file to absolutize relative paths (except in include sections).

    Args:
        file_path: Path to the config file

    Returns:
        Tuple of (modified_data or None, relative_paths_info)
        where relative_paths_info is [(key_path, original_value, in_include), ...]
        modified_data is None if no changes were made
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = syaml.load(f)

    if not data:
        return None, []

    config_dir = os.path.dirname(file_path)
    found_paths = walk_yaml_for_paths(data, config_dir)

    relative_paths_info = []
    modified = False

    for key_path_str, original_value, abs_path, in_include in found_paths:
        # If it's a relative path (not absolute originally)
        if not os.path.isabs(original_value):
            relative_paths_info.append((key_path_str, original_value, in_include))

            # Only absolutize if NOT in an include section
            if not in_include:
                key_parts = []
                # Parse the key path string back into parts
                for part in key_path_str.split("."):
                    key_parts.append(part)

                absolutize_path_in_yaml(data, key_parts, abs_path)
                modified = True

    return data if modified else None, relative_paths_info


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

        all_relative_paths = []
        for config_file in config_files:
            old_path = os.path.join(old_location, config_file)
            # Check for relative paths even in dry-run
            _, relative_paths = process_config_file_paths(old_path)
            if relative_paths:
                all_relative_paths.extend(
                    (config_file, key_path, value, in_include)
                    for key_path, value, in_include in relative_paths
                )
                tty.msg(f"    - {config_file} (contains {len(relative_paths)} relative path(s))")
            else:
                tty.msg(f"    - {config_file}")

        if all_relative_paths:
            tty.msg("\n  Relative paths that would be processed:")
            for config_file, key_path, value, in_include in all_relative_paths:
                status = "(would keep relative - in include)" if in_include else "(would absolutize)"
                tty.msg(f"    {config_file}:{key_path} = {value} {status}")

        if args.clear:
            tty.msg(f"\nWould then move {old_location} to {backup_loc}")
        return

    # Perform the migration
    os.makedirs(new_config_location, exist_ok=True)
    tty.msg(f"Migrating config files from {old_location} to {new_config_location}...")

    all_relative_paths = []

    for config_file in config_files:
        old_path = os.path.join(old_location, config_file)
        new_path = os.path.join(new_config_location, config_file)

        # Process the file to handle relative paths
        modified_data, relative_paths = process_config_file_paths(old_path)

        # Track relative paths for warning
        if relative_paths:
            all_relative_paths.extend(
                (config_file, key_path, value, in_include)
                for key_path, value, in_include in relative_paths
            )

        # Write the file (modified if needed, otherwise copy)
        # Ensure parent directory exists for nested files
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        if modified_data is not None:
            # Write modified YAML
            with open(new_path, "w", encoding="utf-8") as f:
                syaml.dump(modified_data, f)
            tty.msg(f"  Copied (with absolutized paths): {config_file}")
        else:
            # No modifications needed, just copy
            shutil.copy2(old_path, new_path)
            tty.msg(f"  Copied: {config_file}")

    tty.msg("Migration complete!")

    # Warn about relative paths found
    if all_relative_paths:
        tty.warn("Found relative paths in config files:")
        for config_file, key_path, value, in_include in all_relative_paths:
            status = "(kept relative - in include)" if in_include else "(converted to absolute)"
            tty.msg(f"  {config_file}:{key_path} = {value} {status}")

    # Handle --clear: move ~/.spack to backup
    if args.clear:
        tty.msg(f"\nMoving {old_location} to {backup_loc}...")
        shutil.move(old_location, backup_loc)
        tty.msg(f"Backup complete! Original ~/.spack moved to {backup_loc}")
        tty.msg("\nYou can restore it with:\n  spack migrate --restore")

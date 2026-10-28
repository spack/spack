# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module implements the migration from Spack@:1.2 config layout to Spack@1.3: layout."""

import filecmp
import os
import shutil
import sys
import time
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import spack.error
import spack.paths
import spack.util.hash
import spack.util.lock
import spack.util.spack_yaml as syaml
from spack.util import filesystem, lang, tty


class DestinationCheck(Enum):
    """Actions for destination verification callback in migration."""

    PROCEED = "proceed"  # Destination is clear, proceed with migration
    SKIP = "skip"  # Already migrated correctly, skip but return success
    FAIL = "fail"  # Conflict detected, abort migration


def detect_old_resources() -> Dict[str, bool]:
    """Detect presence of old Spack-internal resources.

    Returns:
        Dictionary with keys: 'installs', 'gpg_keys', 'licenses', 'environments'
    """

    def _has_entries(path: str, ignore: Optional[List[str]] = None) -> bool:
        """Check if directory exists and has entries."""
        if not os.path.exists(path):
            return False
        try:
            for entry in os.listdir(path):
                if ignore and entry in ignore:
                    continue
                return True
            return False
        except NotADirectoryError:
            # catch TOCTOU issue from path removed after check
            return False
        except PermissionError as e:
            tty.die(
                f"Spack encountered a permission error at {e.filename} while attempting to read "
                "old storage locations to migrate data. Fix the permissions or contact an admin "
                "of this Spack instance to run `spack migrate`."
            )

    opt_spack = os.path.join(spack.paths.opt_path, "spack")

    return {
        "installs": _has_entries(opt_spack, ignore=["gpg"]),
        "gpg_keys": _has_entries(spack.paths.old_gpg_path)
        or _has_entries(spack.paths.old_gpg_keys_path),
        "licenses": _has_entries(spack.paths.old_licenses_path),
        "environments": _has_entries(spack.paths.old_envs_path),
    }


class Index:
    """Represents a list index in a YAML path."""

    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return f"Index({self.idx})"


def _check_for_escaping_env_variables(data: Any, file_context: str = "") -> None:
    """Check YAML data for $env/.. patterns that escape the environment.

    Args:
        data: YAML data structure to check
        file_context: Description of the file being checked (for error messages)

    Raises:
        spack.error.SpackError: If $env/.. pattern found
    """
    if isinstance(data, dict):
        for value in data.values():
            _check_for_escaping_env_variables(value, file_context)
    elif isinstance(data, list):
        for item in data:
            _check_for_escaping_env_variables(item, file_context)
    elif isinstance(data, str):
        if "$env" in data and "/.." in data:
            context = f" in {file_context}" if file_context else ""
            raise spack.error.SpackError(
                f"Cannot migrate: path '{data}'{context} contains $env/.. which would "
                f"reference outside the environment. Expand the variable or use an absolute path."
            )


def _walk_yaml_for_paths(
    data: Any, config_file_dir: str, key_path: Optional[List[Union[str, Index]]] = None
) -> List[Tuple[List[Union[str, Index]], str, str]]:
    """Walk YAML data and find strings that look like paths.

    Identifies paths as:
    - Absolute paths (os.path.isabs() - handles / on Unix and C:\\ on Windows)
    - Relative paths starting with ../

    Args:
        data: YAML data structure to walk
        config_file_dir: Directory containing the config file (for resolving relative paths)
        key_path: Current position in the YAML structure

    Returns:
        List of (key_path, original_value, absolute_path) tuples
    """
    if key_path is None:
        key_path = []

    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                nested = _walk_yaml_for_paths(value, config_file_dir, key_path + [key])
                results.extend(nested)
            elif isinstance(value, str):
                # Check if string looks like a path
                if os.path.isabs(value) or value.startswith("../"):
                    abs_path = _resolve_and_check_path(value, config_file_dir)
                    if abs_path:
                        results.append((key_path + [key], value, abs_path))

    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, (dict, list)):
                nested = _walk_yaml_for_paths(item, config_file_dir, key_path + [Index(idx)])
                results.extend(nested)
            elif isinstance(item, str):
                # Check if string looks like a path
                if os.path.isabs(item) or item.startswith("../"):
                    abs_path = _resolve_and_check_path(item, config_file_dir)
                    if abs_path:
                        results.append((key_path + [Index(idx)], item, abs_path))

    return results


def _resolve_and_check_path(value: str, config_file_dir: str) -> str:
    """Resolve a potential path string to an absolute path.

    Used by _walk_yaml_for_paths which examines strings that look like paths
    (absolute or starting with ../), so we can assume these are meant to be path references.
    """
    if not value or value.startswith("$"):
        return ""

    if os.path.isabs(value):
        return value

    return os.path.normpath(os.path.join(config_file_dir, value))


def _absolutize_path_in_yaml(
    data: Any, key_path_parts: List[Union[str, Index]], new_value: str
) -> None:
    """Replace a value at a path in a YAML data structure."""
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


def process_env_file_paths(
    file_path: str,
    old_env_dir: str,
    new_env_dir: str,
    old_envs_root: Optional[str] = None,
    new_envs_root: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Rewrite paths in environment config files for environment relocation.

    Applies environment-specific path rewriting rules:

    1. Absolute path inside old env -> rewrite to new env location
    2. Relative path staying inside env -> keep relative (works in new location)
    3. Absolute path outside env and outside envs root -> unchanged

    BLOCKED (migration fails if these are found):
    4. Relative path pointing outside env -> BLOCKS MIGRATION
    5. Absolute path in envs root but outside this env (sibling) -> BLOCKS MIGRATION

    Args:
        file_path: Path to the yaml file to process
        old_env_dir: Old environment directory root
        new_env_dir: New environment directory root
        old_envs_root: Old environments root (parent of all envs being migrated)
        new_envs_root: New environments root (target parent for migrated envs)

    Returns:
        Modified data if any paths were changed, None otherwise

    Raises:
        spack.error.SpackError: If environment has external references that prevent migration
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = syaml.load(f)

    if not data:
        return None

    # Check for $env/.. patterns that escape the environment
    rel_file = os.path.relpath(file_path, os.path.abspath(new_env_dir))
    _check_for_escaping_env_variables(data, rel_file)

    # file_path is in the new location (staging), but we need to resolve relative paths
    # as they would have been in the old location
    new_config_dir = os.path.dirname(file_path)
    old_env_norm = os.path.normpath(os.path.abspath(old_env_dir))
    new_env_norm = os.path.normpath(os.path.abspath(new_env_dir))

    # Calculate what the config dir would have been in the old location
    rel_to_new_env = os.path.relpath(new_config_dir, new_env_norm)
    old_config_dir = os.path.join(old_env_norm, rel_to_new_env)

    found_paths = _walk_yaml_for_paths(data, old_config_dir)
    modified = False

    for key_path, original_value, abs_path in found_paths:
        abs_path_norm = os.path.normpath(os.path.abspath(abs_path))

        # Check if path is inside the env being moved
        try:
            rel_to_old_env = os.path.relpath(abs_path_norm, old_env_norm)
            inside_env = not rel_to_old_env.startswith("..")
        except ValueError:
            # Different drives on Windows
            inside_env = False

        if inside_env:
            # Rule 1: Path inside env - rewrite if absolute, keep relative if relative
            if os.path.isabs(original_value):
                new_path = os.path.join(new_env_norm, rel_to_old_env)
                _absolutize_path_in_yaml(data, key_path, new_path)
                modified = True
            # else: Rule 2: Relative path inside env: keep as-is
        else:
            # Path is outside the env
            if not os.path.isabs(original_value):
                # Rule 4: Relative path outside env -> BLOCK MIGRATION
                rel_file = os.path.relpath(file_path, new_env_norm)
                raise spack.error.SpackError(
                    f"Environment cannot be migrated: relative path '{original_value}' "
                    f"in {rel_file} points outside the environment to {abs_path}. "
                    f"Either make this an absolute path or move the target inside the environment."
                )

            # Absolute path outside env - check if it's in envs root (sibling reference)
            if old_envs_root:
                try:
                    envs_root_norm = os.path.normpath(os.path.abspath(old_envs_root))
                    rel_to_envs_root = os.path.relpath(abs_path_norm, envs_root_norm)
                    inside_envs_root = not rel_to_envs_root.startswith("..")
                except ValueError:
                    # Different drives
                    inside_envs_root = False

                if inside_envs_root:
                    # Rule 5: Absolute path to sibling in envs root -> BLOCK MIGRATION
                    rel_file = os.path.relpath(file_path, new_env_norm)
                    raise spack.error.SpackError(
                        f"Environment cannot be migrated: absolute path '{original_value}' "
                        f"in {rel_file} points to a sibling location in the environments root. "
                        f"Move the target outside the environments root or inside this "
                        f"environment."
                    )

            # Rule 3: Absolute path outside env and outside envs root -> OK, unchanged

    return data if modified else None


def _process_yaml_files_in_directory(
    old_dir: str,
    staging_dir: str,
    processor_func: Callable[[str, str, str], Optional[Dict[str, Any]]],
    new_dir: str,
    excluded_toplevel_dirs: Optional[Set[str]] = None,
) -> None:
    """Walk directory tree, find YAML files, and process them.

    Args:
        old_dir: Source directory to walk
        staging_dir: Staging directory where processed files are written
        processor_func: Function(yaml_file_path, old_dir, new_dir) -> modified_data or None
        new_dir: Target directory (passed to processor_func)
        excluded_toplevel_dirs: Set of directory names to skip at the first level
    """
    if excluded_toplevel_dirs is None:
        excluded_toplevel_dirs = set()

    for root, dirs, files in os.walk(old_dir, followlinks=False):
        # Skip excluded toplevel directories
        if root == old_dir:
            dirs[:] = [d for d in dirs if d not in excluded_toplevel_dirs]

        for filename in files:
            if not (filename.endswith(".yaml") or filename.endswith(".yml")):
                continue

            old_path = os.path.join(root, filename)
            rel_path = os.path.relpath(old_path, old_dir)
            staging_file_path = os.path.join(staging_dir, rel_path)

            try:
                modified_data = processor_func(old_path, old_dir, new_dir)

                os.makedirs(os.path.dirname(staging_file_path), exist_ok=True)

                if modified_data is not None:
                    old_mode = os.stat(old_path).st_mode & 0o777
                    with open(staging_file_path, "w", encoding="utf-8") as f:
                        syaml.dump(modified_data, f)
                    os.chmod(staging_file_path, old_mode)
                else:
                    shutil.copy2(old_path, staging_file_path)
            except (syaml.SpackYAMLError, OSError) as e:
                tty.debug(f"Skipping {rel_path} during migration: {e}")


def process_config_file_paths(
    file_path: str, old_location: str, new_config_location: str
) -> Optional[Dict[str, Any]]:
    """Rewrite paths in config files for relocation.

    - Absolute paths inside old_location: rewrite to new_location
    - Relative paths starting with ../: make absolute
    - Other paths: leave as-is (files copied to new location)

    Returns the modified data if any paths were changed, None otherwise.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = syaml.load(f)

    if not data:
        return None

    config_dir = os.path.dirname(file_path)
    found_paths = _walk_yaml_for_paths(data, config_dir)
    modified = False

    old_location_norm = os.path.normpath(os.path.abspath(old_location))
    new_config_location_norm = os.path.normpath(os.path.abspath(new_config_location))

    for key_path, original_value, abs_path in found_paths:
        if os.path.isabs(original_value):
            # Absolute path - rewrite if inside old_location
            abs_path_norm = os.path.normpath(abs_path)
            try:
                rel_to_old = os.path.relpath(abs_path_norm, old_location_norm)
                if not rel_to_old.startswith(".."):
                    # Inside old_location - rewrite to new location
                    new_path = os.path.join(new_config_location_norm, rel_to_old)
                    _absolutize_path_in_yaml(data, key_path, new_path)
                    modified = True
            except ValueError:
                # Different drives on Windows - not inside old_location
                pass
        else:
            # Relative path starting with ../ - make absolute
            _absolutize_path_in_yaml(data, key_path, abs_path)
            modified = True

    return data if modified else None


def can_migrate_to_location(location: str):
    """Verify destination is empty or doesn't exist (for use as verify_destination_callback)."""
    if not os.path.lexists(location):
        return DestinationCheck.PROCEED

    if not os.path.isdir(location):
        tty.warn(f"{location} exists as a file or dangling symlink, cannot migrate")
        return DestinationCheck.FAIL

    if os.listdir(location):
        tty.debug(f"{location} already has files, skipping migration")
        return DestinationCheck.FAIL

    if not os.access(location, os.W_OK):
        tty.debug(f"{location} is not writable, skipping migration")
        return DestinationCheck.FAIL

    # Empty directory - safe to migrate
    return DestinationCheck.PROCEED


def _is_nonempty_directory(path: str) -> bool:
    try:
        return bool(os.listdir(path))
    except OSError:
        return False


def _make_marker_verifier(marker_name: str):
    def verify_with_marker(dest_path):
        if not os.path.exists(dest_path):
            return DestinationCheck.PROCEED
        marker_path = os.path.join(dest_path, marker_name)
        if os.path.exists(marker_path):
            tty.debug(f"Already migrated from this spack instance (found marker {marker_name})")
            return DestinationCheck.SKIP
        tty.warn(f"Destination exists from different source: {dest_path}")
        return DestinationCheck.FAIL

    return verify_with_marker


def migrate_with_staging(
    old_path: str,
    new_path: str,
    prepare_staging_callback,
    lock_name: Optional[str],
    staging_name: str,
    description: str,
    verify_destination_callback,
) -> bool:
    """Generic migration function for resources.

    Common pattern for atomic migrations:
    1. Check source exists and has content
    2. Verify destination (via callback) - can skip, fail, or proceed
    3. Acquire lock (unless lock_name is None, meaning caller handles locking)
    4. Re-verify destination inside lock (state may have changed)
    5. Create staging directory
    6. Call callback to populate staging (copy/process files)
    7. Atomically rename staging to destination

    Args:
        lock_name: Name of lock file. If None, caller is responsible for locking.
        verify_destination_callback: Function that checks destination and returns
            DestinationCheck.SKIP (already migrated), FAIL (can't migrate), or
            PROCEED (safe to migrate). Use can_migrate_to_location for simple
            empty-directory checks, or _make_marker_verifier for marker-based checks.
    """
    if not _is_nonempty_directory(old_path):
        return False

    # Verify destination before locking. This will almost always trigger an early
    # return (skip locking). Marker-based verifiers check for already-migrated
    # destinations first (which won't be empty due to marker file), then fall back
    # to the empty-directory check.
    action = verify_destination_callback(new_path)
    if action == DestinationCheck.SKIP:
        return True
    elif action == DestinationCheck.FAIL:
        return False
    # PROCEED continues to acquire lock and migrate

    # Prepare parent directory and staging path
    parent = os.path.dirname(new_path)
    staging_path = os.path.join(parent, staging_name)
    filesystem.mkdirp(parent)

    # Acquire lock only if caller didn't take responsibility for it
    lock = None
    lock_acquired = False
    if lock_name is not None:
        lock_path = os.path.join(parent, lock_name)
        lock = spack.util.lock.Lock(lock_path, default_timeout=120)

    try:
        if lock is not None:
            lock.acquire_write()
            lock_acquired = True

        # Verify destination again inside lock (state may have changed)
        action = verify_destination_callback(new_path)
        if action == DestinationCheck.SKIP:
            return True
        elif action == DestinationCheck.FAIL:
            return False
        # PROCEED continues normal flow

        if not _is_nonempty_directory(old_path):
            return False

        # Check destination and verify we can write to it
        try:
            if os.path.lexists(new_path):
                if os.path.isdir(new_path) and not os.listdir(new_path):
                    os.rmdir(new_path)
                    tty.debug(f"Removed empty {new_path} to proceed with migration")
                else:
                    # Not empty or not a directory - can't migrate
                    # This should have been caught by verify_destination_callback, but
                    # kept as a safety check
                    return False

            # Verify we have permissions to create new_path by testing with makedirs
            # This creates the directory so os.rename() will work later
            os.makedirs(new_path, exist_ok=True)
            # Remove it immediately so os.rename() from staging will work
            os.rmdir(new_path)

        except PermissionError:
            # Cannot write to destination - migration not possible
            return False

        # Clean up stale staging directory from previous failed attempt
        if os.path.exists(staging_path):
            shutil.rmtree(staging_path, ignore_errors=True)

        # Callback creates staging directory and populates it
        tty.debug(f"Migrating {description} from {old_path} to {new_path}")
        prepare_staging_callback(old_path, staging_path, new_path)

        # Set staging directory permissions to 0700 before rename
        # (migrating to home directory, only user should access)
        os.chmod(staging_path, 0o700)

        # Atomically rename staging to final destination
        os.rename(staging_path, new_path)
        tty.debug(f"{description.capitalize()} migrated from {old_path} to {new_path}")
        return True

    except MigrationStagingError as e:
        tty.debug(f"Cannot migrate {description}: {e}")
        return False

    except spack.error.SpackError as e:
        tty.warn(f"Cannot migrate {description}: {e}")
        return False

    except (OSError, shutil.Error) as e:
        tty.warn(f"Failed to migrate {description}: {e}")
        return False

    finally:
        # Clean up staging directory if it still exists
        if os.path.exists(staging_path):
            shutil.rmtree(staging_path, ignore_errors=True)

        if lock_acquired and lock is not None:
            lock.release_write()


def _rewrite_symlinks_after_copy(staging_path, old_location, new_location, error_on_rewrite=False):
    """Rewrite or detect problematic symlinks in staging directory after copying.

    Rules:
    - Relative symlinks pointing outside old_location: make absolute (or error)
    - Absolute symlinks pointing inside old_location: rewrite to new_location (or error)
    - Other symlinks: leave as-is

    Args:
        staging_path: Directory where files were copied to
        old_location: Original source directory
        new_location: Target directory for migration
        error_on_rewrite: If True, raise MigrationStagingError instead of rewriting

    Returns:
        A list of (link_path, old_target, new_target) tuples for reporting.

    Raises:
        MigrationStagingError: If error_on_rewrite=True and problematic symlinks found
    """
    rewrites = []
    old_location_real = os.path.realpath(old_location)

    for root, dirs, files in os.walk(staging_path, followlinks=False):
        for name in list(dirs) + list(files):
            path = os.path.join(root, name)

            if not os.path.islink(path):
                continue

            target = os.readlink(path)
            new_target = None

            if os.path.isabs(target):
                # Absolute symlink - check if it points into old_location
                target_real = os.path.realpath(target)
                try:
                    if os.path.commonpath([target_real, old_location_real]) == old_location_real:
                        # Points inside old location - would need rewriting
                        rel_path = os.path.relpath(target_real, old_location_real)
                        new_target = os.path.join(new_location, rel_path)
                except (ValueError, OSError):
                    # Different drives on Windows, or path doesn't exist - leave as-is
                    pass
            else:
                # Relative symlink - check if resolved target is outside old_location
                # Resolve relative to the ORIGINAL link location (in old_location)
                rel_path_in_staging = os.path.relpath(path, staging_path)
                original_link = os.path.join(old_location, rel_path_in_staging)
                original_link_dir = os.path.dirname(original_link)

                try:
                    # Resolve the target relative to original link directory
                    # (target was read from staging, but we resolve as if from original location)
                    resolved = os.path.normpath(os.path.join(original_link_dir, target))
                    resolved_real = (
                        os.path.realpath(resolved) if os.path.exists(resolved) else resolved
                    )

                    # Check if resolved target is outside old_location
                    try:
                        common = os.path.commonpath([resolved_real, old_location_real])
                        if common != old_location_real:
                            # Points outside - would need to make absolute
                            new_target = resolved_real
                    except ValueError:
                        # Different drives or no common path - definitely outside
                        new_target = resolved_real
                except (OSError, ValueError):
                    # Can't resolve - leave as-is
                    pass

            if new_target:
                rewrites.append((path, target, new_target))
                if error_on_rewrite:
                    rel_path = os.path.relpath(path, staging_path)
                    raise MigrationStagingError(
                        f"Cannot migrate: symlink '{rel_path}' points to '{target}' which would "
                        f"require rewriting to '{new_target}'. Environment migration does not "
                        f"support symlink rewriting."
                    )
                # Rewrite mode: update the symlink
                os.unlink(path)
                os.symlink(new_target, path)

    return rewrites


def _prepare_config_staging(old_location, staging_path, new_location):
    """Callback for config migration - copies files and processes config files.

    Strategy:
    1. Copy all non-YAML files/dirs from ~/.spack to staging (excluding certain cache dirs)
    2. Process and copy YAML files with path rewriting
    3. Rewrite symlinks as needed
    """
    # Directories to exclude at the first level (cache/temporary data)
    EXCLUDED_TOPLEVEL_DIRS = {
        "bootstrap",
        "cache",
        "git_repos",
        "package_repos",
        "reports",
        "test",
        "stage",
    }

    # Helper to skip YAML files during directory copy
    def ignore_yaml_files(directory, contents):
        return [name for name in contents if name.endswith(".yaml") or name.endswith(".yml")]

    # First pass: copy non-YAML files and directories
    for item in os.listdir(old_location):
        old_item_path = os.path.join(old_location, item)
        staging_item_path = os.path.join(staging_path, item)

        # Skip excluded toplevel directories
        if os.path.isdir(old_item_path) and item in EXCLUDED_TOPLEVEL_DIRS:
            tty.debug(f"Skipping excluded directory: {item}")
            continue

        # Skip YAML files (process separately)
        if item.endswith(".yaml") or item.endswith(".yml"):
            continue

        # Copy everything else
        try:
            if os.path.isdir(old_item_path):
                # Copy directory but ignore YAML files inside
                shutil.copytree(
                    old_item_path, staging_item_path, symlinks=True, ignore=ignore_yaml_files
                )
            else:
                shutil.copy2(old_item_path, staging_item_path)
        except OSError as e:
            tty.debug(f"Skipping {item} during migration: {e}")

    # Second pass: process and copy YAML files
    _process_yaml_files_in_directory(
        old_location, staging_path, process_config_file_paths, new_location, EXCLUDED_TOPLEVEL_DIRS
    )

    # Third pass: rewrite symlinks
    symlink_rewrites = _rewrite_symlinks_after_copy(staging_path, old_location, new_location)
    if symlink_rewrites:
        tty.warn("Rewrote symlinks during migration:")
        for link_path, old_target, new_target in symlink_rewrites:
            rel_link = os.path.relpath(link_path, staging_path)
            tty.warn(f"  {rel_link}: {old_target} -> {new_target}")


def _prepare_package_repos_staging(old_path, staging_path, new_path):
    """Callback for package repos migration - copy while holding old repo lock.

    Acquires the old package-repository.lock to prevent copying a repo that's
    currently being cloned by another Spack instance using the old locations.
    """
    # Acquire the old lock to prevent copying a half-cloned repo
    # The old lock was in ~/.spack (parent of old package_repos location)
    old_lock_dir = os.path.dirname(old_path)
    old_lock_path = os.path.join(old_lock_dir, "package-repository.lock")

    old_repo_lock = spack.util.lock.Lock(old_lock_path)
    with spack.util.lock.ReadTransaction(old_repo_lock):
        shutil.copytree(old_path, staging_path, symlinks=True)


def _prepare_gpg_staging(old_path, staging_path, marker_name):
    """Callback for GPG migration - copy directory, set permissions, add marker."""
    shutil.copytree(old_path, staging_path)
    os.chmod(staging_path, 0o700)
    with open(os.path.join(staging_path, marker_name), "w", encoding="utf-8") as f:
        f.write(f"Migrated from {spack.paths.prefix}\n")


def _migrate_user_config() -> bool:
    """Copy config files from ~/.spack to user config location.

    Respects XDG_CONFIG_HOME but skips migration if SPACK_USER_CONFIG_PATH is set.
    """
    # If SPACK_USER_CONFIG_PATH is set, don't migrate - user has explicit override
    if os.getenv("SPACK_USER_CONFIG_PATH"):
        return False

    old_location = os.path.expanduser("~/.spack")
    new_location = migration_config_home()

    return migrate_with_staging(
        old_path=old_location,
        new_path=new_location,
        prepare_staging_callback=_prepare_config_staging,
        lock_name=".spack-user-config-migration.lock",
        staging_name=".spack-config-staging",
        description="user config",
        verify_destination_callback=can_migrate_to_location,
    )


def _migrate_package_repositories() -> bool:
    """Copy legacy package repositories to the new default location."""
    old_path = spack.paths.old_package_repos_path
    data_home = migration_data_home()
    new_path = os.path.join(data_home, "package_repos")

    return migrate_with_staging(
        old_path=old_path,
        new_path=new_path,
        prepare_staging_callback=_prepare_package_repos_staging,
        lock_name=".spack-package-repos-migration-lock",
        staging_name=".package-repos-migration",
        description="package repositories",
        verify_destination_callback=can_migrate_to_location,
    )


def _migration_lock_path() -> str:
    """Path to the migration lock file for $spack prefix resources."""
    return os.path.join(spack.paths.prefix, ".migration-lock")


def migration_done_marker_path() -> str:
    """Path to the marker file indicating migration is complete."""
    return os.path.join(spack.paths.prefix, ".migration-done")


def _migration_source_hash() -> str:
    """Compute a hash of the spack prefix to identify this migration source.

    This hash is used in marker files to distinguish migrations from different
    spack instances, enabling fault tolerance when migrations are interrupted.

    Returns:
        8-character hex hash of the normalized spack prefix path
    """
    prefix_str = os.path.normpath(spack.paths.prefix)
    return spack.util.hash.b32_hash(prefix_str)[:8]


def _migrate_gpg(
    old_gpg_home: str, target_gpg_home: str, old_gpg_keys: str, target_gpg_keys: str
) -> bool:
    """Migrate both GPG home (keyring) and GPG keys directories.

    Returns True only if both migrations succeed. If either fails, both should
    be configured to their old locations.
    """
    # Check if sources exist - if neither exists, nothing to migrate
    gpg_home_exists = os.path.exists(old_gpg_home)
    gpg_keys_exists = os.path.exists(old_gpg_keys)

    if not gpg_home_exists and not gpg_keys_exists:
        return True

    # Compute marker name for this spack instance
    source_hash = _migration_source_hash()
    marker_name = f".migration-{source_hash}"
    verify_with_marker = _make_marker_verifier(marker_name)

    if gpg_home_exists:
        success = migrate_with_staging(
            old_path=old_gpg_home,
            new_path=target_gpg_home,
            prepare_staging_callback=lambda old, staging, new: _prepare_gpg_staging(
                old, staging, marker_name
            ),
            lock_name=".gpg-home-migration.lock",
            staging_name=".spack-gpg-home-staging",
            description="GPG home",
            verify_destination_callback=verify_with_marker,
        )
        if not success:
            return False

    # Only proceed to gpg_keys if gpg_home succeeded (or didn't exist)
    if gpg_keys_exists:
        return migrate_with_staging(
            old_path=old_gpg_keys,
            new_path=target_gpg_keys,
            prepare_staging_callback=lambda old, staging, new: _prepare_gpg_staging(
                old, staging, marker_name
            ),
            lock_name=".gpg-keys-migration.lock",
            staging_name=".spack-gpg-keys-staging",
            description="GPG keys",
            verify_destination_callback=verify_with_marker,
        )

    return True


def _migrate_environments(src_dir: str, dst_dir: str) -> bool:
    """Copy environments under one lock, removing partial results on failure."""
    if not os.path.exists(src_dir):
        return True

    source_hash = _migration_source_hash()
    marker_name = f".migration-{source_hash}"
    verify_with_marker = _make_marker_verifier(marker_name)

    try:
        filesystem.mkdirp(dst_dir)
    except (OSError, PermissionError):
        # Cannot create destination directory - migration not possible
        return False

    # Define environment metadata/view exclusion callback
    # Use hardcoded marker instead of importing from environment module to avoid
    # circular imports during module load time
    VIEW_MARKER_FILE = ".spack-view"

    def ignore_views(directory, names):
        """Exclude view directories during environment copy.

        Skips:
        - .spack-env directories (always - contains default views at .spack-env/view)
        - ._view at environment root only (old format pre-June 2026: symlinks to ._view/<hash>/)
        - Directories with .spack-view marker anywhere (custom-location views, June 2026+)

        spack.lock is copied

        Note: Skipping .spack-env also excludes cached repos and locks as a side effect.
        """
        ignored = []
        is_env_root = os.path.normpath(directory) == os.path.normpath(src_dir)

        for name in names:
            path = os.path.join(directory, name)

            # Always skip .spack-env directory (contains default views)
            if name == ".spack-env":
                ignored.append(name)
                tty.debug(f"Excluding .spack-env directory: {path}")
            # Skip ._view ONLY at environment root (old format container)
            elif is_env_root and name == "._view":
                ignored.append(name)
                tty.debug(f"Excluding root-level ._view directory: {path}")
            # Skip custom-location views with marker file (anywhere in tree)
            elif os.path.isdir(path) and os.path.exists(os.path.join(path, VIEW_MARKER_FILE)):
                ignored.append(name)
                tty.debug(f"Excluding view directory with marker: {path}")
        return ignored

    # Define staging callback for environment migration
    def prepare_env_staging(old_path, staging_path, new_path):
        """Copy environment and rewrite paths.

        Raises:
            MigrationStagingError: If the environment cannot be safely migrated due to:
                - The env directory itself being a symlink
                - Symlinks inside the env pointing to absolute paths within the old env
                - Symlinks inside the env pointing outside the staging directory
        """
        # Check if the env directory itself is a symlink
        if os.path.islink(old_path):
            raise MigrationStagingError(f"Environment directory {old_path} is a symlink")

        shutil.copytree(old_path, staging_path, symlinks=True, ignore=ignore_views)

        # Check for problematic symlinks (raises MigrationStagingError if found)
        _rewrite_symlinks_after_copy(staging_path, old_path, new_path, error_on_rewrite=True)

        # Rewrite paths in environment config files
        yaml_files = filesystem.find(staging_path, ["*.yaml", "*.yml"], recursive=True)
        for yaml_file in yaml_files:
            processed = process_env_file_paths(yaml_file, old_path, new_path, src_dir, dst_dir)
            if processed:
                # Get original file permissions before rewriting
                old_mode = os.stat(yaml_file).st_mode & 0o777
                with open(yaml_file, "w", encoding="utf-8") as f:
                    syaml.dump(processed, f)
                # Restore original permissions
                os.chmod(yaml_file, old_mode)
                tty.debug(f"Rewrote paths in {yaml_file}")

        # Add migration marker to identify this source
        with open(os.path.join(staging_path, marker_name), "w", encoding="utf-8") as f:
            f.write(f"Migrated from {spack.paths.prefix}\n")

    # Acquire lock for all environments
    lock = spack.util.lock.Lock(os.path.join(dst_dir, ".lock"), default_timeout=120)
    try:
        lock.acquire_write()

        # Check occupied destinations before copying any new environments. This
        # lets migrate_with_staging reject conflicts without leaving a partial
        # migration behind.
        source_entries = {
            entry for entry in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, entry))
        }
        destination_entries = set(os.listdir(dst_dir))
        intersection = sorted(source_entries & destination_entries)
        remainder = sorted(source_entries - destination_entries)

        # Check if any environments in remainder have installs inside them
        # (indicated by .spack-db/index.json - these are non-relocatable)
        # Also check whether they have specs with dev_path in the lockfile,
        # we do not currently relocate those.
        for entry in remainder:
            env_path = os.path.join(src_dir, entry)
            if os.path.isdir(env_path):
                # Look for database index file anywhere under the environment directory
                db_index = None
                for root, _, files in os.walk(env_path):
                    if os.path.basename(root) == ".spack-db" and "index.json" in files:
                        db_index = os.path.join(env_path, root, "index.json")
                        break

                if db_index:
                    tty.debug(
                        f"Environment {entry} has installs inside it "
                        f"(found {db_index}); skipping migration of all environments"
                    )
                    return False

                # Read the lockfile and look for dev_path variants
                # Technically, we could also read the yaml file and only return False if the
                # dev_path comes from a relative path in the yaml, but we are conservative here
                lock_path = os.path.join(env_path, "spack.lock")
                if os.path.exists(lock_path):
                    with open(lock_path, "r", encoding="utf-8") as f:
                        if '"dev_path":' in f.read():
                            tty.debug(
                                f"environment {entry} has develop specs in it. "
                                "Skipping migration of all environments"
                            )
                            return False

        copied = []
        for entry in intersection + remainder:
            src_path = os.path.join(src_dir, entry)
            dst_path = os.path.join(dst_dir, entry)
            success = migrate_with_staging(
                old_path=src_path,
                new_path=dst_path,
                prepare_staging_callback=prepare_env_staging,
                lock_name=None,  # Parent holds the lock
                staging_name=f".spack-env-{entry}-staging",
                description=f"environment {entry}",
                verify_destination_callback=verify_with_marker,
            )
            if success:
                if entry not in destination_entries:
                    copied.append(entry)
            else:
                for done in copied:
                    shutil.rmtree(os.path.join(dst_dir, done), ignore_errors=True)
                return False

        # All environments copied successfully - old environments remain in place
        return True
    finally:
        lock.release_write()


def _dirs_identical(src_dir: str, dst_dir: str) -> bool:
    """Check if two directory trees have identical structure and content.

    Uses deep comparison (actual file content), not shallow (size/mtime only).
    """
    cmp = filecmp.dircmp(src_dir, dst_dir)

    if cmp.left_only or cmp.right_only:
        return False

    # Check common files with deep comparison (content, not just size/mtime)
    for common_file in cmp.common_files:
        src_file = os.path.join(src_dir, common_file)
        dst_file = os.path.join(dst_dir, common_file)
        if not filecmp.cmp(src_file, dst_file, shallow=False):
            return False

    # Recursively check subdirectories
    for subdir in cmp.common_dirs:
        if not _dirs_identical(os.path.join(src_dir, subdir), os.path.join(dst_dir, subdir)):
            return False

    return True


def _migrate_licenses(src_dir: str, dst_dir: str) -> bool:
    """Copy licenses individually without claiming to lock out manual edits.

    Symlinks are copied as symlinks (not dereferenced), preserving their targets.
    Since the old license directory remains in place after migration, symlinks
    pointing to old locations will continue to work.
    """
    if not os.path.exists(src_dir):
        return True

    src_entries = sorted(os.listdir(src_dir))
    if not src_entries:
        return True

    try:
        filesystem.mkdirp(dst_dir)
    except (OSError, PermissionError):
        # Cannot create destination directory - migration not possible
        return False

    copied = []

    for entry in src_entries:
        src_path = os.path.join(src_dir, entry)
        dst_path = os.path.join(dst_dir, entry)
        try:
            if os.path.lexists(dst_path):
                # Check if content matches (prior copy or identical from another checkout)
                if os.path.islink(src_path) and os.path.islink(dst_path):
                    # For symlinks, compare targets
                    if os.readlink(src_path) == os.readlink(dst_path):
                        tty.debug(
                            f"License symlink {entry} already exists with matching target, "
                            f"skipping"
                        )
                        copied.append(entry)
                        continue
                elif os.path.isfile(src_path) and os.path.isfile(dst_path):
                    with open(src_path, "rb") as f:
                        src_hash = spack.util.hash.b32_hash(
                            f.read().decode("utf-8", errors="replace")
                        )
                    with open(dst_path, "rb") as f:
                        dst_hash = spack.util.hash.b32_hash(
                            f.read().decode("utf-8", errors="replace")
                        )
                    if src_hash == dst_hash:
                        tty.debug(
                            f"License file {entry} already exists with matching content, skipping"
                        )
                        copied.append(entry)
                        continue
                elif os.path.isdir(src_path) and os.path.isdir(dst_path):
                    # For directories, check if trees are identical
                    if _dirs_identical(src_path, dst_path):
                        tty.debug(
                            f"License directory {entry} already exists with matching content, "
                            f"skipping"
                        )
                        copied.append(entry)
                        continue
                # Hash mismatch or type mismatch - stop migration
                raise FileExistsError(dst_path)

            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, symlinks=True)
            else:
                # Copy file or symlink (follow_symlinks=False preserves symlinks)
                shutil.copy2(src_path, dst_path, follow_symlinks=False)
            copied.append(entry)
        except (OSError, shutil.Error) as e:
            tty.warn(
                f"License migration stopped at {entry}: {e}. Copied licenses: "
                f"{', '.join(copied) if copied else 'none'}. The old license directory "
                f"will remain configured; copied files may remain in {dst_dir}."
            )
            return False
    return True


def migrate_home() -> Dict[str, bool]:
    """Migrate user config and package repos from ~/.spack to new XDG locations.

    This is independent of $spack prefix migration and runs whenever:
    - Old locations have content
    - New locations don't exist (checked by individual migration functions)

    This allows users who git pull a new Spack to get their ~/.spack migrated
    regardless of what's in the $spack prefix.

    Prints a message only if anything was actually migrated.

    Returns:
        Dict with keys 'user_config' and 'package_repos', values True if migrated
    """

    tty.debug("Home directory migration called")

    user_config_migrated = _migrate_user_config()
    package_repos_migrated = _migrate_package_repositories()

    # Print message only if something was actually migrated
    if user_config_migrated or package_repos_migrated:
        parts = ["Spack migrated home directory resources:"]
        if user_config_migrated:
            parts.append("  - Copied user configuration from ~/.spack to ~/.config/spack.")
        if package_repos_migrated:
            parts.append(
                "  - Copied package repositories from ~/.spack to the shared data location."
            )
        parts.append("  - ~/.spack was retained because older Spack instances may still use it.")
        sys.stderr.write("\n".join(parts) + "\n")

    return {"user_config": user_config_migrated, "package_repos": package_repos_migrated}


def migration_config_home() -> str:
    """Compute migration target for config_home with XDG fallback chain.

    Uses (in order of precedence):
    1. XDG_CONFIG_HOME environment variable (append /spack)
    2. Default XDG_CONFIG_HOME location: ~/.config/spack

    This does not use config, since migration happens before config is fully loaded.
    Does not check SPACK_USER_CONFIG_PATH - if that's set, caller should skip migration.
    """
    xdg_config = os.getenv("XDG_CONFIG_HOME")
    if xdg_config:
        return os.path.join(xdg_config, "spack")

    return os.path.join(os.path.expanduser("~"), ".config", "spack")


def migration_data_home() -> str:
    """Compute migration target for data_home with XDG fallback chain.

    Uses (in order of precedence):
    1. SPACK_DATA_HOME environment variable
    2. XDG_DATA_HOME environment variable
    3. Default XDG_DATA_HOME location: ~/.local/share/spack

    This does not use config, since migration happens before config is fully loaded.
    """
    spack_data = os.getenv("SPACK_DATA_HOME")
    if spack_data:
        return spack_data

    xdg_data = os.getenv("XDG_DATA_HOME")
    if xdg_data:
        return os.path.join(xdg_data, "spack")

    return os.path.join(os.path.expanduser("~"), ".local", "share", "spack")


def _prompt_for_prefix_migration(old_resources: Dict[str, bool], timeout: float = 60) -> bool:
    """Ask whether portable resources under the Spack prefix may be copied
    A return value of ``True`` means the user saw the prompt and responded "yes";
    a return value of ``False`` means either the user responded "no", or the user
    never saw the prompt (e.g. because Spack is being run as part of a script).

    This can also return False if it detects that no resources are eligible for
    moving (in which case there would be no point in prompting the user for that).
    """
    if os.getenv("SPACK_AUTOMIGRATE_YES"):
        return True
    data_home = migration_data_home()
    resources = []
    if old_resources["gpg_keys"] and not os.getenv("SPACK_GNUPGHOME"):
        resources.append(
            (
                "GPG data",
                f"{spack.paths.old_gpg_path} and {spack.paths.old_gpg_keys_path}",
                f"{data_home}/gpg and {data_home}/gpg-keys",
            )
        )
    if old_resources["licenses"]:
        resources.append(
            ("licenses", spack.paths.old_licenses_path, os.path.join(data_home, "licenses"))
        )
    if old_resources["environments"]:
        resources.append(
            ("environments", spack.paths.old_envs_path, os.path.join(data_home, "environments"))
        )

    if not resources:
        return False

    # Check stdin and stderr are both ttys (prompt goes to stderr)
    if not sys.stdin.isatty() or not sys.stderr.isatty():
        return False

    # On Unix, also check if we're in the foreground process group
    # (Windows doesn't have process groups, so skip this check there)
    if sys.platform != "win32":
        try:
            if os.getpgrp() != os.tcgetpgrp(sys.stdin.fileno()):
                return False
        except OSError:
            # Can't determine process group - assume we can't prompt
            return False

    tty.info(
        "Spack found resources in its legacy internal layout.",
        "Spack can copy the following resources to the new user data location",
        "(based on XDG_DATA_HOME/SPACK_DATA_HOME environment variables):",
        *[f"{name}: {old} -> {new}" for name, old, new in resources],
        "If (y)es: Spack attempts to copy local resources into the new default location;"
        " the old resources are not deleted and this can be undone later with"
        " `spack migrate --undo`",
        "If (n)o (the default): configuration is updated to prefer the old locations over"
        " the new defaults; nothing inside the Spack prefix is copied into $HOME.",
        stream=sys.stderr,
    )

    deadline = time.monotonic() + timeout
    prompt = "Proceed with copying these resources? [y/N]"

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            sys.stderr.write("\r" + " " * 80 + "\r")  # Clear the line
            sys.stderr.flush()
            tty.info(
                "No response received; keeping resources in their old locations.",
                stream=sys.stderr,
            )
            return False

        answer = lang.readline_with_timeout(prompt, remaining, update_interval=1.0)

        if answer is None:
            # Timeout expired
            sys.stderr.write("\r" + " " * 80 + "\r")  # Clear the line
            sys.stderr.flush()
            tty.info(
                "No response received; keeping resources in their old locations.",
                stream=sys.stderr,
            )
            return False

        answer = answer.strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no", ""):
            # Empty string (just hitting enter) defaults to "no"
            return False
        else:
            sys.stderr.write(
                f'Must enter (y)es or (n)o or newline (implied "no"), got: "{answer}"\n'
            )
            # Loop back and ask again with remaining time


def migrate_spack_prefix(old_resources):
    """Migrate Spack prefix data from old to new locations.

    Migrates portable resources (licenses, environments, GPG data) from old
    locations under $spack to new XDG-style shared locations. Existing installs
    are retained in place. Configuration is written to the layout scope.

    This is called during initialization after the user approves migration, or
    directly by `spack migrate use-new-layout`.
    """
    tty.debug("Spack prefix migration called")

    migrated_resources: List[str] = []

    # Compute data_home using XDG fallback chain (without config, since CONFIG doesn't exist yet)
    data_home = migration_data_home()

    # 1. Handle GPG (both keyring and keys directory)
    old_gpg_home = spack.paths.old_gpg_path
    old_gpg_keys = spack.paths.old_gpg_keys_path
    if old_resources["gpg_keys"]:
        target_gpg_home = os.path.join(data_home, "gpg")
        target_gpg_keys = os.path.join(data_home, "gpg-keys")
        gnupghome = os.getenv("SPACK_GNUPGHOME")

        if not gnupghome:
            if _migrate_gpg(old_gpg_home, target_gpg_home, old_gpg_keys, target_gpg_keys):
                migrated_resources.append("GPG data")
                del old_resources["gpg_keys"]

    # 2. Handle licenses
    if old_resources["licenses"]:
        old_licenses = spack.paths.old_licenses_path
        target_licenses = os.path.join(data_home, "licenses")
        if _migrate_licenses(old_licenses, target_licenses):
            migrated_resources.append("licenses")
            tty.debug(f"Copied licenses from {old_licenses} to {target_licenses}")
            del old_resources["licenses"]

    # 3. Handle environments
    if old_resources["environments"]:
        old_envs = spack.paths.old_envs_path
        target_envs = os.path.join(data_home, "environments")
        if _migrate_environments(old_envs, target_envs):
            migrated_resources.append("environments")
            tty.debug(f"Copied environments from {old_envs} to {target_envs}")
            del old_resources["environments"]

    # 4. Installs: these are always pointed to the old locations if they exist.
    # This method deletes items that are migrated from old_resources, so we
    # retain them simply by never deleting that entry

    # Write layout scope for resources that didn't migrate
    retained_resources = _force_old_layout(old_resources)

    # Write migration completion marker as the last step
    # This allows other processes to detect that migration finished
    marker_path = migration_done_marker_path()
    with open(marker_path, "w", encoding="utf-8") as f:
        f.write("Migration completed\n")
    tty.debug(f"Wrote migration completion marker: {marker_path}")

    # Print migration summary
    parts = []
    if migrated_resources:
        parts.append("Spack migrated old resources.")
        parts.append("  - Migrated: " + ", ".join(migrated_resources) + ".")
        if "environments" in migrated_resources:
            parts.extend(
                [
                    "  - Environment views were not copied. Activate each environment and run "
                    "`spack env view regenerate` to recreate them.",
                    "  - If you have an environment activated by a prior command (not this one) "
                    "you will need to deactivate and then reactivate it.",
                ]
            )
    else:
        parts.append("No Spack-internal resources were migrated")

    if retained_resources:
        parts.append("  - Retained: " + ", ".join(retained_resources) + ".")

    if migrated_resources:
        parts.extend(["", "To undo this migration, run `spack migrate undo`."])
    sys.stderr.write("\n".join(parts) + "\n")


def _force_old_layout(to_move) -> List[str]:
    config_path = os.path.join(spack.paths.layout_scope_path, "config.yaml")
    filesystem.mkdirp(spack.paths.layout_scope_path, default_perms="parents")

    config_changes: Dict[str, Any] = {}
    retained_resources: List[str] = []

    if to_move.get("installs"):
        retained_resources.append("existing installs")
        config_changes["install_tree"] = {"root": os.path.join(spack.paths.prefix, "opt", "spack")}

    old_gpg_home = spack.paths.old_gpg_path
    old_gpg_keys = spack.paths.old_gpg_keys_path
    if to_move.get("gpg_keys"):
        config_changes["gpg_path"] = old_gpg_home
        config_changes["gpg_keys_path"] = old_gpg_keys
        retained_resources.append(f"GPG data ({old_gpg_home})")

    if to_move.get("licenses"):
        old_licenses = spack.paths.old_licenses_path
        config_changes["license_dir"] = old_licenses
        retained_resources.append(f"licenses ({old_licenses})")

    if to_move.get("environments"):
        old_envs = spack.paths.old_envs_path
        config_changes["environments_root"] = old_envs
        retained_resources.append(f"environments ({old_envs})")

    # Write config scope files to the layout scope only if we have config changes
    if config_changes:
        with open(config_path, "w", encoding="utf-8") as f:
            syaml.dump({"config": config_changes}, f)
        tty.debug(f"Wrote config.yaml to {config_path}")
    else:
        tty.debug("No config changes needed, skipping config.yaml")

    tty.debug(f"Created layout scope pointing to old locations {spack.paths.layout_scope_path}")

    return retained_resources


def force_old_layout(to_move, print_message=True):
    retained_resources = _force_old_layout(to_move)

    marker_path = migration_done_marker_path()
    with open(marker_path, "w", encoding="utf-8") as f:
        f.write("Migration completed\n")
    tty.debug(f"Wrote migration completion marker: {marker_path}")

    parts = ["No Spack-internal resources were migrated"]
    if retained_resources:
        parts.append("  - Retained: " + ", ".join(retained_resources) + ".")
    sys.stderr.write("\n".join(parts) + "\n")


def generate_old_layout_config(old_resources, scope_config):
    if old_resources["installs"]:
        scope_config["config"]["install_tree"] = {
            "root": os.path.join(spack.paths.prefix, "opt", "spack")
        }
        tty.debug(f"Keeping existing installs in {spack.paths.prefix}/opt/spack")

    if old_resources["gpg_keys"]:
        old_gpg_home = spack.paths.old_gpg_path
        old_gpg_keys = spack.paths.old_gpg_keys_path
        scope_config["config"]["gpg_path"] = old_gpg_home
        scope_config["config"]["gpg_keys_path"] = old_gpg_keys
        tty.debug(f"Keeping GPG data in {old_gpg_home} and {old_gpg_keys}")

    if old_resources["licenses"]:
        scope_config["config"]["license_dir"] = spack.paths.old_licenses_path
        tty.debug(f"Keeping licenses in {spack.paths.old_licenses_path}")

    if old_resources["environments"]:
        scope_config["config"]["environments_root"] = spack.paths.old_envs_path
        tty.debug(f"Keeping environments in {spack.paths.old_envs_path}")


def perform_migration():
    """Check for migration and prompt if needed.

    This runs before the CONFIG singleton is created, so migration functions
    cannot rely on CONFIG being available.
    """
    # Returns True iff config was migrated
    # Because this rewrites config, it should either run first thing (before config
    # is loaded) or last (right before termination of the process)
    old_resources = detect_old_resources()

    if os.path.exists(spack.paths.isolate_scope_path):
        if any(old_resources.values()):
            if not os.path.exists(os.path.join(spack.paths.isolate_scope_path, "layout")):
                # TODO: could automate logic in the `spack isolate`` command to run here:
                # - generate layout config in etc/spack/isolate/
                # - infer whether user ran with --self or --path (and in the latter case,
                #   infer what --path was)
                # - set up writable user scope
                # As it is, if we proceeded without doing this, installs would be
                # automatically written to $HOME in some cases.
                raise RuntimeError(
                    "Detected that Spack was previously isolated:"
                    " run `spack isolate --reuse-old...` or delete etc/spack/isolate"
                )
        return False

    # Migrate user config scope and package repos. An entirely-new spack
    # instance can do this (and needs to in order to access user config
    # in new location). This occurs whether or not there are resources in
    # the spack prefix that need to be migrated, but not if the
    # `spack isolate` command has been run
    #
    # The method returns a dict with keys "user_config" and "package_repos", and
    # values whether they were migrated
    config_migrated = migrate_home()["user_config"]

    marker_path = migration_done_marker_path()
    if os.path.exists(marker_path):
        return config_migrated

    if any(old_resources.values()):
        lock_path = _migration_lock_path()
        lock = spack.util.lock.Lock(lock_path, default_timeout=120)
        try:
            with spack.util.lock.WriteTransaction(lock):
                if not os.path.exists(marker_path):
                    # Waiting for user input inside the lock prevents other
                    # instances from progressing, but prevents a scenario where
                    # user says "Y" and then a separate non-tty process subverts
                    # that
                    try:
                        user_allows_it = _prompt_for_prefix_migration(old_resources)
                        if user_allows_it:
                            migrate_spack_prefix(old_resources)
                        else:
                            force_old_layout(old_resources)
                    except PermissionError as e:
                        tty.die(
                            f"PermissionError accessing {e.filename}. Writing to the Spack prefix "
                            "is required to migrate your Spack data. Fix the permissions or "
                            "contact someone with permissions to run `spack migrate`."
                        )
        except spack.util.lock.LockPermissionError:
            # Read-only prefix
            tty.die(
                "The spack prefix is not writable. "
                "Writing to the Spack prefix is required to migrate to new data storage locations."
                " Contact an admin of the Spack instance to run `spack migrate`."
            )
        except spack.util.lock.LockTimeoutError as e:
            # Some other migration process is taking too long, bail vs. hang
            tty.die(f"Timed out waiting for migration lock: {e}")

    return config_migrated


class MigrationStagingError(spack.error.SpackError):
    """Raised when a resource cannot be safely staged for migration."""

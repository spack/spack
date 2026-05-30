# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""

import os
import pathlib
import sys as _sys
import types as _types
from pathlib import PurePath

import spack.llnl.util.filesystem
import spack.util.hash as hash


def dir_is_occupied(x, except_for=None):
    """Check if a directory exists and contains files (excluding specified names)."""
    x = pathlib.Path(x)
    except_for = except_for or set()
    if not x.is_dir():
        return False
    for path in x.iterdir():
        if path.parts[-1] not in except_for:
            return True
    return False


class SpackPaths:
    """Object containing paths for a Spack instance with layout detection."""

    def __init__(self, _prefix=None):
        #: This file lives in $prefix/lib/spack/spack/__file__
        self.prefix = _prefix or str(PurePath(spack.llnl.util.filesystem.ancestor(__file__, 4)))

        #: synonym for prefix
        self.spack_root = self.prefix

        #: bin directory in the spack prefix
        self.bin_path = os.path.join(self.prefix, "bin")

        #: The spack script itself
        self.spack_script = os.path.join(self.bin_path, "spack")

        #: The sbang script in the spack installation
        self.sbang_script = os.path.join(self.bin_path, "sbang")

        # spack directory hierarchy
        self.lib_path = os.path.join(self.prefix, "lib", "spack")
        self.module_path = os.path.join(self.lib_path, "spack")
        self.vendor_path = os.path.join(self.module_path, "vendor")
        self.command_path = os.path.join(self.module_path, "cmd")
        self.analyzers_path = os.path.join(self.module_path, "analyzers")
        self.platform_path = os.path.join(self.module_path, "platforms")
        self.compilers_path = os.path.join(self.module_path, "compilers")
        self.operating_system_path = os.path.join(self.module_path, "operating_systems")
        self.test_path = os.path.join(self.module_path, "test")
        self.hooks_path = os.path.join(self.module_path, "hooks")
        self.opt_path = os.path.join(self.prefix, "opt")
        self.share_path = os.path.join(self.prefix, "share", "spack")
        self.etc_path = os.path.join(self.prefix, "etc", "spack")

        #: Things in $spack/etc/spack
        self.default_license_dir = os.path.join(self.etc_path, "licenses")

        #: Things in $spack/var/spack
        self.var_path = os.path.join(self.prefix, "var", "spack")

        # read-only things in $spack/var/spack
        self.repos_path = os.path.join(self.var_path, "repos")
        self.test_repos_path = os.path.join(self.var_path, "test_repos")
        self.mock_packages_path = os.path.join(self.test_repos_path, "spack_repo", "builtin_mock")

        # GPG paths for mock data
        self.mock_gpg_data_path = os.path.join(self.var_path, "gpg.mock", "data")
        self.mock_gpg_keys_path = os.path.join(self.var_path, "gpg.mock", "keys")

        # Old layout paths for detection
        self.old_install_path = os.path.join(self.prefix, "opt", "spack")
        self.old_envs_path = os.path.join(self.var_path, "environments")
        self.old_fetch_cache_path = os.path.join(self.var_path, "cache")
        self.old_gpg_path = os.path.join(self.prefix, "opt", "spack", "gpg")
        self.old_gpg_keys_path = os.path.join(self.var_path, "gpg")
        self.old_licenses_path = os.path.join(self.etc_path, "licenses")

        expanded_home = os.path.expanduser("~")

        # If this exists, this was the location for configs and for the package repository
        self.old_default_dot_spack = os.path.join(expanded_home, ".spack")

        #: User configuration location
        self.user_config_path = os.path.expanduser(
            os.getenv("SPACK_USER_CONFIG_PATH") or os.path.join(expanded_home, ".config", "spack")
        )

        #: System configuration location
        self.system_config_path = os.path.expanduser(
            os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
        )

        #: Not a location itself, but used for when Spack instances
        #: share the same cache base directory for caches that should
        #: not be shared between those instances.
        self.spack_instance_id = hash.b32_hash(self.spack_root)[:7]

        # Detect old layout
        self.old_layout_detected = detect_old_spack_layout(self)

        # User cache path - simplified version that uses SPACK_USER_CACHE_PATH or ~/.local/state/spack
        self.user_cache_path = os.path.expanduser(
            os.getenv("SPACK_USER_CACHE_PATH") or os.path.join(expanded_home, ".local", "state", "spack")
        )

        #: Default paths based on user_cache_path
        self.default_fetch_cache_path = os.path.join(self.var_path, "cache")
        self.gpg_keys_path = os.path.join(self.var_path, "gpg")
        self.gpg_path = os.path.join(self.opt_path, "spack", "gpg")
        self.reports_path = os.path.join(self.user_cache_path, "reports")
        self.default_test_path = os.path.join(self.user_cache_path, "test")
        self.default_monitor_path = os.path.join(self.reports_path, "monitor")
        self.user_repos_cache_path = os.path.join(self.user_cache_path, "git_repos")
        self.package_repos_path = os.path.join(self.user_cache_path, "package_repos")
        self.default_user_bootstrap_path = os.path.join(self.user_cache_path, "bootstrap")
        self.default_misc_cache_path = os.path.join(self.user_cache_path, self.spack_instance_id, "cache")

        #: Backup location for old .spack directory (used by migrate command)
        self.dotspack_backup = os.path.join(expanded_home, ".spack.backup")


def detect_old_spack_layout(paths):
    """Detect if the old Spack layout is present.

    Args:
        paths: SpackPaths instance to check

    Returns:
        True if old layout data is detected, False otherwise
    """
    checks = [
        # It's important if this directory is occupied but we have a separate
        # check for that, so exclude that directory here
        (paths.old_install_path, ["gpg"]),
        (paths.old_envs_path, []),
        (paths.old_fetch_cache_path, []),
        (paths.old_gpg_path, []),
        (paths.old_gpg_keys_path, ["README.md"]),
        (paths.old_licenses_path, []),
    ]
    for x, y in checks:
        if dir_is_occupied(x, except_for=set(y)):
            return True
    return False


def detect_layout(scheme):
    """True if ``scheme`` is the active layout (``"old"`` or new).

    Used by ``etc/spack/defaults/include.yaml`` to choose which scheme
    yaml to include. Honors "unilateral override": if the user has set
    any new-style location env var (SPACK_DATA_HOME, SPACK_STATE_HOME,
    SPACK_CACHE_HOME), new layout is selected even when legacy
    $spack-local data is present.

    Cannot call ``config.get(...)`` here: this runs during config
    initialization (an include's ``when:`` is evaluated before the scope
    is pushed), so reading config would recurse into the singleton init.
    Env-var + filesystem probes only.
    """
    if scheme != "old":
        raise ValueError(f"unknown layout scheme: {scheme!r} (expected 'old')")

    # Check if user explicitly set new-layout environment variables
    new_layout_env_vars = ["SPACK_DATA_HOME", "SPACK_STATE_HOME", "SPACK_CACHE_HOME"]
    env_forces_new = any(v in os.environ for v in new_layout_env_vars)

    # Detect if old layout data exists
    is_old = locations.old_layout_detected and not env_forces_new
    return is_old


# Module-level singleton instance
locations = SpackPaths()

#: Recorded directory where spack command was originally invoked
spack_working_dir = None


def set_working_dir():
    """Change the working directory to getcwd, or spack prefix if no cwd."""
    global spack_working_dir
    try:
        spack_working_dir = os.getcwd()
    except OSError:
        os.chdir(locations.prefix)
        spack_working_dir = locations.prefix


# Module shim: lets callers keep using `spack.paths.X` for any attribute on
# `locations` (e.g. `spack.paths.gpg_path`, `spack.paths.prefix`).
# Uses a sys.modules swap because we want all attribute access to delegate
# to the locations object.
class _PathsModule(_types.ModuleType):
    def __getattr__(self, name: str):
        return getattr(locations, name)


_shim = _PathsModule(__name__)
_shim.__dict__.update(_sys.modules[__name__].__dict__)
_sys.modules[__name__] = _shim

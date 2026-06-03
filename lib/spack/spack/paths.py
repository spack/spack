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
import sys
import types
from pathlib import PurePath
from typing import TYPE_CHECKING

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

        self._user_cache_path = None

        #: Backup location for old .spack directory (used by migrate command)
        self.dotspack_backup = os.path.join(expanded_home, ".spack.backup")

    @property
    def user_cache_path(self):
        import spack.util.path

        expanded_home = os.path.expanduser("~")
        return spack.util.path._resolve_location_var("state") or os.path.join(
            expanded_home, ".local", "state", "spack"
        )

    @property
    def reports_path(self):
        return os.path.join(self.user_cache_path, "reports")

    @property
    def default_test_path(self):
        return os.path.join(self.user_cache_path, "test")

    @property
    def default_monitor_path(self):
        return os.path.join(self.reports_path, "monitor")

    @property
    def user_repos_cache_path(self):
        return os.path.join(self.user_cache_path, "git_repos")

    @property
    def package_repos_path(self):
        return os.path.join(self.user_cache_path, "package_repos")

    @property
    def default_user_bootstrap_path(self):
        return os.path.join(self.user_cache_path, "bootstrap")

    @property
    def default_misc_cache_path(self):
        return os.path.join(self.user_cache_path, self.spack_instance_id, "cache")

    @property
    def gpg_path(self):
        """GPG home directory - reads from config."""
        import spack.config
        import spack.util.path

        cfg = spack.config.get("config:gpg_path", None)
        if cfg:
            return spack.util.path.canonicalize_path(cfg)
        # Fallback if config not set (shouldn't happen with defaults)
        data_home = spack.util.path.substitute_path_variables("$data_home")
        return os.path.join(data_home, "gpg")

    @property
    def gpg_keys_path(self):
        """GPG keys directory - reads from config."""
        import spack.config
        import spack.util.path

        cfg = spack.config.get("config:gpg_keys_path", None)
        if cfg:
            return spack.util.path.canonicalize_path(cfg)
        # Fallback if config not set (shouldn't happen with defaults)
        data_home = spack.util.path.substitute_path_variables("$data_home")
        return os.path.join(data_home, "gpg-keys")

    @property
    def default_fetch_cache_path(self):
        """Source cache directory - reads from config."""
        import spack.config
        import spack.util.path

        cfg = spack.config.get("config:source_cache", None)
        if cfg:
            return spack.util.path.canonicalize_path(cfg)
        # Fallback if config not set (shouldn't happen with defaults)
        data_home = spack.util.path.substitute_path_variables("$data_home")
        return os.path.join(data_home, "cache")


def detect_old_spack_layout(paths):
    """Detect if the old Spack layout is present.

    Args:
        paths: SpackPaths instance to check

    Returns:
        True if old layout data is detected, False otherwise
    """
    checks = [
        # Regarding excluding gpg here: it's important if this
        # directory is occupied but we have a separate check for
        # that, so exclude that directory here
        (paths.old_install_path, ["gpg", ".spack-db"]),
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
    if any(v in os.environ for v in new_layout_env_vars):
        return False

    # Detect if old layout data exists
    # Access via sys.modules to respect monkeypatching in tests
    locations_obj = sys.modules[__name__].locations
    return locations_obj.old_layout_detected


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


# Type hints for mypy - these module-level attributes are dynamically resolved at runtime
# via the module shim below. Declared here so mypy can see them when checking imports.
if TYPE_CHECKING:
    # From SpackPaths
    prefix: str
    spack_root: str
    bin_path: str
    spack_script: str
    sbang_script: str
    lib_path: str
    module_path: str
    vendor_path: str
    command_path: str
    analyzers_path: str
    platform_path: str
    compilers_path: str
    operating_system_path: str
    test_path: str
    hooks_path: str
    opt_path: str
    share_path: str
    etc_path: str
    default_license_dir: str
    var_path: str
    repos_path: str
    test_repos_path: str
    mock_packages_path: str
    mock_gpg_data_path: str
    mock_gpg_keys_path: str
    old_install_path: str
    old_envs_path: str
    old_fetch_cache_path: str
    old_gpg_path: str
    old_gpg_keys_path: str
    old_licenses_path: str
    old_default_dot_spack: str
    user_config_path: str
    system_config_path: str
    spack_instance_id: str
    old_layout_detected: bool
    user_cache_path: str
    default_fetch_cache_path: str
    gpg_keys_path: str
    gpg_path: str
    reports_path: str
    default_test_path: str
    default_monitor_path: str
    user_repos_cache_path: str
    package_repos_path: str
    default_user_bootstrap_path: str
    default_misc_cache_path: str
    dotspack_backup: str


# Module shim: lets callers keep using `spack.paths.X` for any attribute on
# `locations` (e.g. `spack.paths.gpg_path`, `spack.paths.prefix`).
# Uses a sys.modules swap because we want all attribute access to delegate
# to the locations object.
class _PathsModule(types.ModuleType):
    def __getattribute__(self, name: str):
        # For special attributes, use normal resolution
        if name in ("__dict__", "__class__", "__name__"):
            return object.__getattribute__(self, name)

        # Look up 'locations' from module __dict__
        module_dict = object.__getattribute__(self, "__dict__")

        # If it's a known module-level attribute (not from locations), return it
        if name in (
            "locations",
            "SpackPaths",
            "detect_old_spack_layout",
            "detect_layout",
            "dir_is_occupied",
            "set_working_dir",
            "spack_working_dir",
        ):
            if name in module_dict:
                return module_dict[name]
            raise AttributeError(f"module 'spack.paths' has no attribute '{name}'")

        # Otherwise delegate to locations object
        locs = module_dict.get("locations")
        if locs is None:
            raise AttributeError(f"module 'spack.paths' has no attribute '{name}'")
        return getattr(locs, name)  # type: ignore[return-value]


_shim = _PathsModule(__name__)
_shim.__dict__.update(sys.modules[__name__].__dict__)
sys.modules[__name__] = _shim

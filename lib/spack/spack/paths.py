# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""

import os
from pathlib import PurePath

import spack.llnl.util.filesystem
import spack.util.hash as hash

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = str(PurePath(spack.llnl.util.filesystem.ancestor(__file__, 4)))

#: synonym for prefix
spack_root = prefix

#: bin directory in the spack prefix
bin_path = os.path.join(prefix, "bin")

#: The spack script itself
spack_script = os.path.join(bin_path, "spack")

#: The sbang script in the spack installation
sbang_script = os.path.join(bin_path, "sbang")

# spack directory hierarchy
lib_path = os.path.join(prefix, "lib", "spack")
module_path = os.path.join(lib_path, "spack")
vendor_path = os.path.join(module_path, "vendor")
command_path = os.path.join(module_path, "cmd")
analyzers_path = os.path.join(module_path, "analyzers")
platform_path = os.path.join(module_path, "platforms")
compilers_path = os.path.join(module_path, "compilers")
operating_system_path = os.path.join(module_path, "operating_systems")
test_path = os.path.join(module_path, "test")
hooks_path = os.path.join(module_path, "hooks")
opt_path = os.path.join(prefix, "opt")
share_path = os.path.join(prefix, "share", "spack")
etc_path = os.path.join(prefix, "etc", "spack")

#
# Things in $spack/etc/spack
#
default_license_dir = os.path.join(etc_path, "licenses")

#
# Things in $spack/var/spack
#
var_path = os.path.join(prefix, "var", "spack")

# read-only things in $spack/var/spack
repos_path = os.path.join(var_path, "repos")
test_repos_path = os.path.join(var_path, "test_repos")
mock_packages_path = os.path.join(test_repos_path, "spack_repo", "builtin_mock")

#
# Writable things in $spack/var/spack
# TODO: Deprecate these, as we want a read-only spack prefix by default.
# TODO: These should probably move to user cache, or some other location.
#
# fetch cache for downloaded files
default_fetch_cache_path = os.path.join(var_path, "cache")

# GPG paths - declared here but will be initialized later after defining helper functions
gpg_keys_path = None
gpg_path = None
mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")


#: Not a location itself, but used for when Spack instances
#: share the same cache base directory for caches that should
#: not be shared between those instances.
spack_instance_id = hash.b32_hash(spack_root)[:7]


# Below paths are where Spack can write information for the user.
# Some are caches, some are not exactly caches.
#
# The options that start with `default_` below are overridable in
# `config.yaml`, but they default to use `user_cache_path/<location>`.
#
# You can override the top-level directory (the user cache path) by
# setting `SPACK_USER_CACHE_PATH`. Otherwise it defaults to ~/.spack.
#


def _get_config_value(key, default):
    """Helper to get config values, avoiding circular imports.

    Applies variable substitution ($user_cache_path, $spack, etc.) to the value.
    """
    try:
        import spack.config
        import spack.util.path
        value = spack.config.get(key, default)
        if value and isinstance(value, str):
            value = spack.util.path.substitute_path_variables(value)
        return value
    except (ImportError, Exception):
        # During bootstrap or if config isn't ready, use default
        return default


def _get_user_cache_path():
    """Get user_cache_path from config or environment."""
    # First check environment variable (for backwards compatibility)
    env_path = os.getenv("SPACK_USER_CACHE_PATH")
    if env_path:
        return os.path.expanduser(env_path)

    # Then check config
    config_path = _get_config_value("config:user_cache_path", None)
    if config_path:
        return config_path

    # Fall back to old default
    return os.path.expanduser("~%s.spack" % os.sep)


def _get_user_cache_path_cached():
    """Cached version of user_cache_path."""
    if not hasattr(_get_user_cache_path_cached, "_cached"):
        _get_user_cache_path_cached._cached = str(PurePath(_get_user_cache_path()))
    return _get_user_cache_path_cached._cached


def _get_reports_path():
    """Get reports_path from config or compute default."""
    config_path = _get_config_value("config:reports_path", None)
    if config_path:
        return config_path
    return os.path.join(_get_user_cache_path_cached(), "reports")


def _get_default_monitor_path():
    """Get default_monitor_path from config or compute default."""
    config_path = _get_config_value("config:default_monitor_path", None)
    if config_path:
        return config_path
    return os.path.join(_get_reports_path(), "monitor")


def _get_user_repos_cache_path():
    """Get user_repos_cache_path from config or compute default."""
    config_path = _get_config_value("config:user_repos_cache_path", None)
    if config_path:
        return config_path
    return os.path.join(_get_user_cache_path_cached(), "git_repos")


def _get_package_repos_path():
    """Get package_repos_path from config or compute default."""
    config_path = _get_config_value("config:package_repos_path", None)
    if config_path:
        return config_path
    return os.path.join(_get_user_cache_path_cached(), "package_repos")


def _get_gpg_path():
    """Get gpg_path from config or compute default."""
    config_path = _get_config_value("config:gpg_path", None)
    if config_path:
        return config_path
    # Old default was in opt/spack/gpg
    return os.path.join(opt_path, "spack", "gpg")


def _get_gpg_keys_path():
    """Get gpg_keys_path from config or compute default."""
    config_path = _get_config_value("config:gpg_keys_path", None)
    if config_path:
        return config_path
    # Old default was in var/spack/gpg
    return os.path.join(var_path, "gpg")


# These are computed lazily to allow config to be loaded first
user_cache_path = str(PurePath(_get_user_cache_path_cached()))

#: junit, cdash, etc. reports about builds
reports_path = _get_reports_path()

#: installation test (spack test) output
default_test_path = os.path.join(user_cache_path, "test")

#: spack monitor analysis directories
default_monitor_path = _get_default_monitor_path()

#: git repositories fetched to compare commits to versions
user_repos_cache_path = _get_user_repos_cache_path()

#: default location where remote package repositories are cloned
package_repos_path = _get_package_repos_path()

#: bootstrap store for bootstrapping clingo and other tools
default_user_bootstrap_path = os.path.join(user_cache_path, "bootstrap")

#: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
default_misc_cache_path = os.path.join(user_cache_path, spack_instance_id, "cache")

# Initialize GPG paths now that helper functions are defined
gpg_path = _get_gpg_path()
gpg_keys_path = _get_gpg_keys_path()

# Below paths pull configuration from the host environment.
#
# There are three environment variables you can use to isolate spack from
# the host environment:
# - `SPACK_USER_CONFIG_PATH`: override `~/.spack` location (for config and caches)
# - `SPACK_SYSTEM_CONFIG_PATH`: override `/etc/spack` configuration scope.
# - `SPACK_DISABLE_LOCAL_CONFIG`: disable both of these locations.


# User configuration and caches in $HOME/.spack
def _get_user_config_path():
    return os.path.expanduser(os.getenv("SPACK_USER_CONFIG_PATH") or "~%s.spack" % os.sep)


# Configuration in /etc/spack on the system
def _get_system_config_path():
    return os.path.expanduser(
        os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
    )


#: User configuration location
user_config_path = _get_user_config_path()

#: System configuration location
system_config_path = _get_system_config_path()

#: Recorded directory where spack command was originally invoked
spack_working_dir = None


def set_working_dir():
    """Change the working directory to getcwd, or spack prefix if no cwd."""
    global spack_working_dir
    try:
        spack_working_dir = os.getcwd()
    except OSError:
        os.chdir(prefix)
        spack_working_dir = prefix

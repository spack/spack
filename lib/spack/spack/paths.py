# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.

Paths that depend on configuration (the user cache, where package
repositories are cloned, the GPG home, ...) are not defined here; see
the corresponding functions in :mod:`spack.config`.
"""

import os
from pathlib import PurePath

import spack.util.filesystem
from spack.util import hash

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = str(PurePath(spack.util.filesystem.ancestor(__file__, 4)))

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

#: Configuration scope written by ``spack isolate``
isolate_scope_path = os.path.join(etc_path, "isolate")

#: Configuration scope written by the migration, recording where old resources live
layout_scope_path = os.path.join(etc_path, "layout")

#: Data location used by ``spack isolate --self``
self_isolation_prefix = os.path.join(prefix, ".isolate")

#
# Things in $spack/var/spack
#
var_path = os.path.join(prefix, "var", "spack")

# read-only things in $spack/var/spack
repos_path = os.path.join(var_path, "repos")
test_repos_path = os.path.join(var_path, "test_repos")
mock_packages_path = os.path.join(test_repos_path, "spack_repo", "builtin_mock")

# GPG paths for mock data
mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")

#
# Locations where Spack <= 1.2 wrote data into its own prefix, and into ~/.spack.
# Used only to detect and migrate such data; see :mod:`spack.migrate`.
#
old_envs_path = os.path.join(var_path, "environments")
old_gpg_path = os.path.join(opt_path, "spack", "gpg")
old_gpg_keys_path = os.path.join(var_path, "gpg")
old_licenses_path = os.path.join(etc_path, "licenses")
old_default_dot_spack = os.path.expanduser(os.path.join("~", ".spack"))
old_package_repos_path = os.path.join(old_default_dot_spack, "package_repos")


#: Not a location itself, but used for when Spack instances
#: share the same cache base directory for caches that should
#: not be shared between those instances.
spack_instance_id = hash.b32_hash(spack_root)[:7]


# Below paths pull configuration from the host environment.
#
# There are three environment variables you can use to isolate spack from
# the host environment:
# - `SPACK_USER_CONFIG_PATH`: override `~/.config/spack` location
# - `SPACK_SYSTEM_CONFIG_PATH`: override `/etc/spack` configuration scope.
# - `SPACK_DISABLE_LOCAL_CONFIG`: disable both of these locations.


# User configuration in $XDG_CONFIG_HOME/spack
def _get_user_config_path():
    return os.path.expanduser(
        os.getenv("SPACK_USER_CONFIG_PATH") or os.path.join("~", ".config", "spack")
    )


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

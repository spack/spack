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
from pathlib import PurePath
from typing import Optional

import llnl.util.filesystem

import spack.util.hash as hash

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = str(PurePath(llnl.util.filesystem.ancestor(__file__, 4)))

xdg_config_home = "XDG_CONFIG_HOME"
xdg_state_home = "XDG_STATE_HOME"
xdg_data_home = "XDG_DATA_HOME"
spack_data_home_varname = "SPACK_DATA_HOME"
xdg_cache_home = "XDG_CACHE_HOME"


# This is for tests that want to clean the environment of XDG_ variables that
# affect spack behavior
def _unset_xdg_vars(env):
    saved = {}
    for xdg_var in [xdg_config_home, xdg_state_home, xdg_data_home, xdg_cache_home]:
        if xdg_var in env:
            saved[xdg_var] = env.pop(xdg_var)
    return saved


def _define_xdg_or_backup(xdg_var, backup):
    if xdg_var in os.environ:
        spack_xdg_defined = os.path.join(os.environ[xdg_var], "spack")
    else:
        spack_xdg_defined = os.path.join(backup, "spack")
    return os.path.expanduser(spack_xdg_defined)


#: Resolved XDG_STATE_HOME, with additional "spack" subdirectory
spack_xdg_state_home = lambda: _define_xdg_or_backup(
    xdg_state_home, os.path.join("~", ".local", "state")
)
spack_xdg_config_home = lambda: _define_xdg_or_backup(
    xdg_config_home, os.path.join("~", ".config")
)
spack_xdg_data_home = lambda: _define_xdg_or_backup(
    xdg_data_home, os.path.join("~", ".local", "share")
)

spack_xdg_data_home_nodefault: Optional[str]
if xdg_data_home in os.environ:
    spack_xdg_data_home_nodefault = os.path.expanduser(
        os.path.join(os.environ[xdg_data_home], "spack")
    )
else:
    spack_xdg_data_home_nodefault = None

spack_xdg_cache_home = lambda: _define_xdg_or_backup(xdg_cache_home, os.path.join("~", ".cache"))


def spack_data_home():
    # spack_data_home is where we know we can put large amounts of data:
    # users can set SPACK_DATA_HOME to tell spack explicitly about such
    # a location. If XDG_DATA_HOME is set, we assume we can use that.
    # If neither are set, we assume the spack prefix is the only place
    # available to us (we do not use ~ and in particular the default for
    # XDG_DATA_HOME).
    if spack_data_home_varname in os.environ:
        return os.environ[spack_data_home_varname]
    elif spack_xdg_data_home_nodefault:
        return spack_xdg_data_home_nodefault
    else:
        return os.path.join(prefix, "opt", "data")


# User configuration
def _get_user_config_path():
    return os.path.expanduser(os.getenv("SPACK_USER_CONFIG_PATH") or spack_xdg_config_home())


# Configuration in /etc/spack on the system
# Override w/ `SPACK_SYSTEM_CONFIG_PATH`
def _get_system_config_path():
    return os.path.expanduser(
        os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
    )


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    return x.is_dir() and bool(set(x.iterdir()) - except_for)


#: User configuration location
user_config_path = _get_user_config_path()

#: System configuration location
system_config_path = _get_system_config_path()

#: When Spack is provided by an admin to a user, the admin can
#: provide a config that only applies for the end-users
end_user_cfg_path = os.path.join(system_config_path, "end-user")

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
external_path = os.path.join(lib_path, "external")
module_path = os.path.join(lib_path, "spack")
command_path = os.path.join(module_path, "cmd")
analyzers_path = os.path.join(module_path, "analyzers")
platform_path = os.path.join(module_path, "platforms")
compilers_path = os.path.join(module_path, "compilers")
operating_system_path = os.path.join(module_path, "operating_systems")
test_path = os.path.join(module_path, "test")
hooks_path = os.path.join(module_path, "hooks")
share_path = os.path.join(prefix, "share", "spack")
etc_path = os.path.join(prefix, "etc", "spack")
default_license_dir = os.path.join(etc_path, "licenses")
var_path = os.path.join(prefix, "var", "spack")


spack_instance_id = lambda: hash.b32_hash(prefix)[:7]

#: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
default_misc_cache_path = os.path.join(spack_xdg_state_home(), spack_instance_id(), "cache")

#: concretization cache for Spack concretizations
default_conc_cache_path = os.path.join(default_misc_cache_path, "concretization")

modules_base = None
for module_dir in ["lmod", "modules"]:
    if dir_is_occupied(os.path.join(share_path, module_dir)):
        modules_base = share_path
if not modules_base:
    modules_base = os.path.join(spack_xdg_data_home(), "modules")


def default_install_location():
    # Precedence for installs:
    # 1. config:install_tree:root
    # 2. explicitly defined SPACK_DATA_HOME
    # 3. occupied old install path (inside spack prefix)
    # 4. explicitly defined XDG_DATA_HOME
    # 5. inside spack prefix (slightly different compared to old install path)
    old_install_path = os.path.join(prefix, "opt", "spack")
    if spack_data_home_varname in os.environ:
        return os.path.join(spack_data_home(), "installs")
    elif dir_is_occupied(old_install_path):
        return old_install_path
    else:
        return os.path.join(spack_data_home(), "installs")


# Environments follow the same precedence rules as installs
# (the view and dev_path packages can take up significant space)
old_envs_path = os.path.join(var_path, "environments")
if spack_data_home_varname in os.environ:
    envs_path = os.path.join(spack_data_home(), "environments")
elif dir_is_occupied(old_envs_path):
    envs_path = old_envs_path
else:
    envs_path = os.path.join(spack_data_home(), "environments")

default_fetch_cache_path = os.path.join(spack_data_home(), "downloads")

# TODO: we could shutil.mv resources from old paths to new paths

# $spack/var/spack is generally read-only. Older instances may
# write gpg keys or environments into ...var/
repos_path = os.path.join(var_path, "repos")
test_repos_path = os.path.join(var_path, "test_repos")
packages_path = os.path.join(repos_path, "spack_repo", "builtin")
mock_packages_path = os.path.join(test_repos_path, "spack_repo", "builtin_mock")

mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")

# Below paths are where Spack can write information for the user.
# Some are caches, some are not exactly caches.
#
# The options that start with `default_` below are overridable in
# `config.yaml`, but they default to use `user_cache_path/<location>`.
#
# You can override the top-level directory (the user cache path) by
# setting `SPACK_USER_CACHE_PATH`. Otherwise it defaults to ~/.spack.
#
def _get_user_cache_path():
    return os.path.expanduser(os.getenv("SPACK_USER_CACHE_PATH") or spack_xdg_data_home())


user_cache_path = str(PurePath(_get_user_cache_path()))

#: junit, cdash, etc. reports about builds
reports_path = os.path.join(user_cache_path, "reports")

#: installation test (spack test) output
default_test_path = os.path.join(user_cache_path, "test")

#: spack monitor analysis directories
default_monitor_path = os.path.join(reports_path, "monitor")

#: git repositories fetched to compare commits to versions
user_repos_cache_path = os.path.join(user_cache_path, "git_repos")

#: bootstrap store for bootstrapping clingo and other tools
default_user_bootstrap_path = os.path.join(user_cache_path, "bootstrap")

old_gpg_path = os.path.join("prefix", "opt" "spack", "gpg")
if dir_is_occupied(old_gpg_path):
    gpg_path = old_gpg_path
else:
    gpg_path = os.path.join(user_cache_path, "gpg")

old_gpg_keys_path = os.path.join(var_path, "gpg")
if dir_is_occupied(old_gpg_keys_path):
    gpg_keys_path = old_gpg_keys_path
else:
    gpg_keys_path = os.path.join(user_cache_path, "gpg-keys")

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

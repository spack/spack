# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import os
import posixpath

import llnl.util.filesystem

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = llnl.util.filesystem.ancestor(__file__, 4)

#: synonym for prefix
spack_root = prefix

#: bin directory in the spack prefix
bin_path = posixpath.join(prefix, "bin")

#: The spack script itself
spack_script = posixpath.join(bin_path, "spack")

#: The sbang script in the spack installation
sbang_script = posixpath.join(bin_path, "sbang")

# spack directory hierarchy
lib_path              = posixpath.join(prefix, "lib", "spack")
external_path         = posixpath.join(lib_path, "external")
build_env_path        = posixpath.join(lib_path, "env")
module_path           = posixpath.join(lib_path, "spack")
command_path          = posixpath.join(module_path, "cmd")
analyzers_path        = posixpath.join(module_path, "analyzers")
platform_path         = posixpath.join(module_path, 'platforms')
compilers_path        = posixpath.join(module_path, "compilers")
build_systems_path    = posixpath.join(module_path, 'build_systems')
operating_system_path = posixpath.join(module_path, 'operating_systems')
test_path             = posixpath.join(module_path, "test")
hooks_path            = posixpath.join(module_path, "hooks")
opt_path              = posixpath.join(prefix, "opt")
share_path            = posixpath.join(prefix, "share", "spack")
etc_path              = posixpath.join(prefix, "etc")


#
# Things in $spack/var/spack
#
var_path              = posixpath.join(prefix, "var", "spack")

# read-only things in $spack/var/spack
repos_path            = posixpath.join(var_path, "repos")
packages_path         = posixpath.join(repos_path, "builtin")
mock_packages_path    = posixpath.join(repos_path, "builtin.mock")

#
# Writable things in $spack/var/spack
# TODO: Deprecate these, as we want a read-only spack prefix by default.
# TODO: These should probably move to user cache, or some other location.
#
# fetch cache for downloaded files
default_fetch_cache_path = posixpath.join(var_path, "cache")

# GPG paths.
gpg_keys_path      = posixpath.join(var_path, "gpg")
mock_gpg_data_path = posixpath.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = posixpath.join(var_path, "gpg.mock", "keys")
gpg_path           = posixpath.join(opt_path, "spack", "gpg")


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
    return os.path.expanduser(os.getenv('SPACK_USER_CACHE_PATH') or "~/.spack")


user_cache_path = _get_user_cache_path()

#: junit, cdash, etc. reports about builds
reports_path = posixpath.join(user_cache_path, "reports")

#: installation test (spack test) output
default_test_path = posixpath.join(user_cache_path, "test")

#: spack monitor analysis directories
default_monitor_path = posixpath.join(reports_path, "monitor")

#: git repositories fetched to compare commits to versions
user_repos_cache_path = posixpath.join(user_cache_path, 'git_repos')

#: bootstrap store for bootstrapping clingo and other tools
default_user_bootstrap_path = posixpath.join(user_cache_path, 'bootstrap')

#: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
default_misc_cache_path = posixpath.join(user_cache_path, 'cache')


# Below paths pull configuration from the host environment.
#
# There are three environment variables you can use to isolate spack from
# the host environment:
# - `SPACK_USER_CONFIG_PATH`: override `~/.spack` location (for config and caches)
# - `SPACK_SYSTEM_CONFIG_PATH`: override `/etc/spack` configuration scope.
# - `SPACK_DISABLE_LOCAL_CONFIG`: disable both of these locations.


# User configuration and caches in $HOME/.spack
def _get_user_config_path():
    return os.path.expanduser(os.getenv('SPACK_USER_CONFIG_PATH') or "~/.spack")


# Configuration in /etc/spack on the system
def _get_system_config_path():
    return os.path.expanduser(os.getenv('SPACK_SYSTEM_CONFIG_PATH') or "/etc/spack")


#: User configuration location
user_config_path = _get_user_config_path()

#: System configuration location
system_config_path = _get_system_config_path()

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import os

from pathlib import Path

import llnl.util.filesystem

#: This file lives in $prefix/lib/spack/spack/__file__
prefix = llnl.util.filesystem.ancestor(__file__, 4)

#: synonym for prefix
spack_root = prefix

#: bin directory in the spack prefix
bin_path = prefix.joinpath( "bin")

#: The spack script itself
spack_script = bin_path.joinpath( "spack")

#: The sbang script in the spack installation
sbang_script = bin_path.joinpath( "sbang")

# spack directory hierarchy
lib_path              = prefix.joinpath( "lib", "spack")
external_path         = lib_path.joinpath( "external")
build_env_path        = lib_path.joinpath( "env")
module_path           = lib_path.joinpath( "spack")
command_path          = module_path.joinpath( "cmd")
analyzers_path        = module_path.joinpath( "analyzers")
platform_path         = module_path.joinpath( 'platforms')
compilers_path        = module_path.joinpath( "compilers")
build_systems_path    = module_path.joinpath( 'build_systems')
operating_system_path = module_path.joinpath( 'operating_systems')
test_path             = module_path.joinpath( "test")
hooks_path            = module_path.joinpath( "hooks")
opt_path              = prefix.joinpath( "opt")
share_path            = prefix.joinpath( "share", "spack")
etc_path              = prefix.joinpath( "etc", "spack")

#
# Things in $spack/etc/spack
#
default_license_dir   = etc_path.joinpath( "licenses")

#
# Things in $spack/var/spack
#
var_path              = prefix.joinpath( "var", "spack")

# read-only things in $spack/var/spack
repos_path            = var_path.joinpath( "repos")
packages_path         = repos_path.joinpath( "builtin")
mock_packages_path    = repos_path.joinpath( "builtin.mock")

#
# Writable things in $spack/var/spack
# TODO: Deprecate these, as we want a read-only spack prefix by default.
# TODO: These should probably move to user cache, or some other location.
#
# fetch cache for downloaded files
default_fetch_cache_path = var_path.joinpath( "cache")

# GPG paths.
gpg_keys_path      = var_path.joinpath( "gpg")
mock_gpg_data_path = var_path.joinpath( "gpg.mock", "data")
mock_gpg_keys_path = var_path.joinpath( "gpg.mock", "keys")
gpg_path           = opt_path.joinpath( "spack", "gpg")


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
    return (os.getenv('SPACK_USER_CACHE_PATH')
                              or "~%s.spack" % os.sep).expanduser()


user_cache_path = _get_user_cache_path()

#: junit, cdash, etc. reports about builds
reports_path = user_cache_path.joinpath( "reports")

#: installation test (spack test) output
default_test_path = user_cache_path.joinpath( "test")

#: spack monitor analysis directories
default_monitor_path = reports_path.joinpath( "monitor")

#: git repositories fetched to compare commits to versions
user_repos_cache_path = user_cache_path.joinpath( 'git_repos')

#: bootstrap store for bootstrapping clingo and other tools
default_user_bootstrap_path = user_cache_path.joinpath( 'bootstrap')

#: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
default_misc_cache_path = user_cache_path.joinpath( 'cache')


# Below paths pull configuration from the host environment.
#
# There are three environment variables you can use to isolate spack from
# the host environment:
# - `SPACK_USER_CONFIG_PATH`: override `~/.spack` location (for config and caches)
# - `SPACK_SYSTEM_CONFIG_PATH`: override `/etc/spack` configuration scope.
# - `SPACK_DISABLE_LOCAL_CONFIG`: disable both of these locations.


# User configuration and caches in $HOME/.spack
def _get_user_config_path():
    return Path(os.getenv('SPACK_USER_CONFIG_PATH') or
                              "~%s.spack" % os.sep).expanduser()


# Configuration in /etc/spack on the system
def _get_system_config_path():
    return Path(os.getenv('SPACK_SYSTEM_CONFIG_PATH') or
                              os.sep + Path('etc').joinpath( 'spack')).expanduser()


#: User configuration location
user_config_path = _get_user_config_path()

#: System configuration location
system_config_path = _get_system_config_path()

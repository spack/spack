# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import itertools
import os
import pathlib
from enum import Enum

import spack.config as config
import spack.paths_base as paths_base
import spack.util.hash as hash


class XDG_vars(Enum):
    config_home = "XDG_CONFIG_HOME"
    state_home = "XDG_STATE_HOME"
    data_home = "XDG_DATA_HOME"
    cache_home = "XDG_CACHE_HOME"


class XDG_overrides(Enum):
    config_home = "SPACK_CONFIG_HOME"
    state_home = "SPACK_STATE_HOME"
    data_home = "SPACK_DATA_HOME"
    cache_home = "SPACK_CACHE_HOME"


# This is for tests that want to clean the environment of XDG_ variables that
# affect spack behavior (and the corresponding SPACK_ overrides). Note that
# these vars will affect .default_test_path for the running instance, but
# the unit tests will not see the env vars
def _unset_xdg_vars(env):
    for xdg_var in itertools.chain(XDG_vars, XDG_overrides):
        env.pop(xdg_var.value, None)


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    return x.is_dir() and bool(set(x.iterdir()) - except_for)


class SpackPaths:
    def __init__(self, base):
        self.base = base

        #: Not a location itself, but used for when Spack instances
        #: share the same cache base directory for caches that should
        #: not be shared between those instances.
        self.spack_instance_id = hash.b32_hash(base.prefix)[:7]

    @property
    def state_home(self):
        return self.resolve_a_home(
            ["SPACK_STATE_HOME", "SPACK_USER_CACHE_PATH"],
            "XDG_STATE_HOME",
            "state",
            os.path.join(".local", "state"),
        )

    @property
    def cache_home(self):
        return self.resolve_a_home("SPACK_CACHE_HOME", "XDG_CACHE_HOME", "cache", ".cache")

    @property
    def data_home(self):
        return self.resolve_a_home(
            "SPACK_DATA_HOME", "XDG_DATA_HOME", "data", os.path.join(".local", "share")
        )

    @property
    def user_cache_path(self):
        return self.state_home

    @property
    def default_install_location(self):
        return self._fallback_old_location_if_used(
            self.base.old_install_path, os.path.join(self.data_home, "installs")
        )

    @property
    def default_envs_path(self):
        return self._fallback_old_location_if_used(
            self.base.old_envs_path, os.path.join(self.data_home, "envs")
        )

    @property
    def reports_path(self):
        #: junit, cdash, etc. reports about builds
        return os.path.join(self.state_home, "reports")

    @property
    def default_test_path(self):
        #: installation test (spack test) output
        return os.path.join(self.state_home, "test")

    @property
    def default_monitor_path(self):
        #: spack monitor analysis directories
        return os.path.join(self.reports_path, "monitor")

    @property
    def user_repos_cache_path(self):
        #: git repositories fetched to compare commits to versions
        if hasattr(self, "_user_repos_cache_path"):
            return self._user_repos_cache_path
        return os.path.join(self.state_home, "git_repos")

    @user_repos_cache_path.setter
    def user_repos_cache_path(self, val):
        # setter for tests
        self._user_repos_cache_path = val

    @property
    def package_repos_path(self):
        #: default location where remote package repositories are cloned
        return os.path.join(self.state_home, "package_repos")

    @property
    def gpg_path(self):
        return self._fallback_old_location_if_used(
            self.base.old_gpg_path, os.path.join(self.data_home, "gpg")
        )

    @property
    def gpg_keys_path(self):
        return self._fallback_old_location_if_used(
            self.base.old_gpg_keys_path, os.path.join(self.data_home, "gpg-keys")
        )

    @property
    def modules_base(self):
        modules_base = None
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.base.share_path, module_dir)):
                modules_base = self.base.share_path
        if not modules_base:
            modules_base = self.data_home
        return modules_base

    @property
    def default_misc_cache_path(self):
        #: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
        #: overridden by `config:misc_cache`
        return os.path.join(self.state_home, self.spack_instance_id, "cache")

    def __getattr__(self, name):
        # Things that aren't sensitive to import cycles can import the
        # paths module and access all items from it
        return getattr(self.base, name)

    def resolve_a_home(self, env_vars, xdg_var, config_var, home_rel):
        """
        Data stored by spack is split into state, data, and cache components.
        This function can resolve where each of these components should be
        stored.

        Args:
            env_vars: spack-specific environment variables that indicate the
                component location. Can be a list or a single variable. If this
                is a list, earlier elements have precedence.
            xdg_var: the XDG-based environment variable that indicates the
                component location.
            config_var: the spack config variable that indicates the component
                location.
            home_rel: for $SPACK_HOME and config:locations:home, this relative
                path is appended to the result to get the component location.
        """
        disable_env = config.get("config:locations:disable_env", False)

        def spack_env_check():
            if disable_env:
                return
            if isinstance(env_vars, str):
                x = [env_vars]
            else:
                x = env_vars
            for n in x:
                if n in os.environ:
                    return os.environ[n]

        def xdg_env_check():
            if disable_env:
                return
            if xdg_var in os.environ:
                return os.path.join(os.environ[xdg_var], "spack")

        def spack_home_env_check():
            if disable_env:
                return
            if "SPACK_HOME" in os.environ:
                return os.path.join(os.environ["SPACK_HOME"], home_rel, "spack")

        def cfg_check():
            return config.get(f"config:locations:{config_var}", None)

        def spack_home_cfg_check():
            h = config.get("config:locations:home", None)
            if h:
                return os.path.join(h, home_rel, "spack")

        for check in [
            spack_env_check,
            xdg_env_check,
            spack_home_env_check,
            cfg_check,
            spack_home_cfg_check,
        ]:
            possible_resolution = check()
            if possible_resolution:
                return possible_resolution

        return os.path.join(os.path.expanduser("~"), home_rel, "spack")

    def _fallback_old_location_if_used(self, old_location, new_location):
        # TODO: perhaps it should be configurable whether old locations
        # are used. Other option is to relocate downloads & gpg keys.
        if dir_is_occupied(new_location):
            return new_location
        elif dir_is_occupied(old_location):
            # TODO: should probably raise a deprecation warning here encouraging
            # them to set their config explicitly back to the old value that
            # will allow us to eventually remove these fallbacks
            return old_location
        else:
            return new_location


locations = SpackPaths(paths_base.locations)

# At least one builtin spack package expects that spack.paths is
# importable and that it has spack_script as a module-level attribute.
# Some test packages expect other paths (like test_path)
prefix = locations.prefix
spack_root = locations.spack_root
bin_path = locations.bin_path
spack_script = locations.spack_script
sbang_script = locations.sbang_script
lib_path = locations.lib_path
external_path = locations.external_path
module_path = locations.module_path
vendor_path = locations.vendor_path
command_path = locations.command_path
analyzers_path = locations.analyzers_path
platform_path = locations.platform_path
compilers_path = locations.compilers_path
operating_system_path = locations.operating_system_path
test_path = locations.test_path
hooks_path = locations.hooks_path
share_path = locations.share_path
etc_path = locations.etc_path
default_license_dir = locations.default_license_dir
var_path = locations.var_path
test_repos_path = locations.test_repos_path
mock_packages_path = locations.mock_packages_path
mock_gpg_data_path = locations.mock_gpg_data_path
mock_gpg_keys_path = locations.mock_gpg_keys_path
default_xdg_cache_home = locations.default_xdg_cache_home
system_config_path = locations.system_config_path
user_config_path = locations.user_config_path

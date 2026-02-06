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
from enum import Enum

import spack.config as config
import spack.paths_base as paths_base
import spack.util.hash as hash


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    return x.is_dir() and bool(set(x.iterdir()) - except_for)


class Provenance(Enum):
    SPACK_ENV = 1  # SPACK_x_HOME
    SPACK_HOME_ENV = 2  # SPACK_HOME
    CONFIG_VAR = 3  # config:locations:x
    CONFIG_HOME_VAR = 4  # config:locations:home
    XDG_VAR = 5  # XDG_x_HOME
    NOTHING_SET = 6  # None of the above are set

    def respectable(self):
        return self in {
            Provenance.SPACK_ENV,
            Provenance.SPACK_HOME_ENV,
            Provenance.CONFIG_VAR,
            Provenance.CONFIG_HOME_VAR,
        }


class HomeResolution:
    def __init__(self, basedir):
        self.basedir = pathlib.Path(basedir)

    def resolve(self, subdir, old_location=None):
        return self.basedir / subdir


class XdgOrDefaultResolution:
    def __init__(self, defaultdir, xdgdir=None):
        self.defaultdir = pathlib.Path(defaultdir)
        self.xdgdir = pathlib.Path(xdgdir) if xdgdir else None

    def resolve(self, subdir, old_location=None):
        if old_location and dir_is_occupied(old_location):
            return old_location
        elif self.xdgdir and dir_is_occupied(self.xdgdir / subdir):
            return self.xdgdir
        elif dir_is_occupied(self.defaultdir / subdir):
            return self.defaultdir
        elif self.xdgdir:
            return self.xdgdir / subdir
        else:
            return self.defaultdir / subdir


class SpackPaths:
    def __init__(self, base):
        self.base = base

        self._state_home = None
        self._data_home = None
        self._cache_home = None

        #: Not a location itself, but used for when Spack instances
        #: share the same cache base directory for caches that should
        #: not be shared between those instances.
        self.spack_instance_id = hash.b32_hash(base.prefix)[:7]

    @property
    def state_home(self):
        if not self._state_home:
            self._state_home = self.resolve_a_home(
                ["SPACK_STATE_HOME", "SPACK_USER_CACHE_PATH"],
                "XDG_STATE_HOME",
                "state",
                os.path.join(".local", "state"),
            )
        return self._state_home

    @property
    def cache_home(self):
        if not self._cache_home:
            self._cache_home = self.resolve_a_home(
                "SPACK_CACHE_HOME", "XDG_CACHE_HOME", "cache", ".cache"
            )
        return self._cache_home

    @property
    def data_home(self):
        if not self._data_home:
            self._data_home = self.resolve_a_home(
                "SPACK_DATA_HOME", "XDG_DATA_HOME", "data", os.path.join(".local", "share")
            )
        return self._data_home

    @property
    def user_cache_path(self):
        return self.state_home

    @property
    def default_install_location(self):
        return self.data_home.resolve("installs", self.base.old_install_path)

    @property
    def default_envs_path(self):
        return self.data_home.resolve("envs", self.base.old_envs_path)

    @property
    def reports_path(self):
        #: junit, cdash, etc. reports about builds
        return self.state_home.resolve("reports")

    @property
    def default_test_path(self):
        #: installation test (spack test) output
        return self.state_home.resolve("test")

    @property
    def default_monitor_path(self):
        #: spack monitor analysis directories
        return os.path.join(self.reports_path, "monitor")

    @property
    def user_repos_cache_path(self):
        #: git repositories fetched to compare commits to versions
        if hasattr(self, "_user_repos_cache_path"):
            return self._user_repos_cache_path
        return self.state_home.resolve("git_repos")

    @user_repos_cache_path.setter
    def user_repos_cache_path(self, val):
        # setter for tests
        self._user_repos_cache_path = val

    @property
    def package_repos_path(self):
        #: default location where remote package repositories are cloned
        return self.state_home.resolve("package_repos")

    @property
    def gpg_path(self):
        return self.data_home.resolve("gpg", self.base.old_gpg_path)

    @property
    def gpg_keys_path(self):
        return self.data_home.resolve("gpg-keys", self.base.old_gpg_keys_path)

    @property
    def modules_base(self):
        # This is similar to logic _fallback_old_location_if_used, but this
        # moves the modules base if any component (typically one of lmod or
        # tcl) has been relocated, so is examining one-layer deeper
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.data_home, module_dir)):
                return self.data_home
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.base.share_path, module_dir)):
                return self.base.share_path
        return self.data_home

    @property
    def default_misc_cache_path(self):
        #: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
        #: overridden by `config:misc_cache`
        return self.state_home.resolve(pathlib.Path(self.spack_instance_id) / "cache")

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
                return (
                    os.path.join(os.environ["SPACK_HOME"], home_rel, "spack")
                )

        def cfg_check():
            val = config.get(f"config:locations:{config_var}", None)
            if val:
                return val

        def spack_home_cfg_check():
            h = config.get("config:locations:home", None)
            if h:
                return os.path.join(h, home_rel, "spack")

        for check in [
            spack_env_check,
            spack_home_env_check,
            cfg_check,
            spack_home_cfg_check,
        ]:
            possible_resolution = check()
            if possible_resolution:
                return HomeResolution(os.path.expanduser(possible_resolution))

        # TODO: need to update this
        # encapsulate the final fallback and the XDG_x var in one value
        # this object needs a resolve(subdir) method
        # if XDG_x is set but subdir of it is empty, return the default dir if it is nonempty

        return XdgOrDefaultResolution(os.path.join(os.path.expanduser("~"), home_rel, "spack"),
                                      xdg_env_check())


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
system_config_path = locations.system_config_path
user_config_path = locations.user_config_path

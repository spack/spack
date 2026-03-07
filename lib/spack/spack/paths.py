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
from functools import partial

import spack.config as config
import spack.llnl.util.tty as tty
import spack.paths_base as paths_base


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    return x.is_dir() and bool(set(x.iterdir()) - except_for)


class Provenance(Enum):
    # Used entirely inside this module, for recording configuration
    # or environment options that the user set in order to influence
    # the location of data that used to live in $spack and following
    # #47615 now lives outside of it

    SPACK_ENV = 1  # SPACK_x_HOME
    SPACK_HOME_ENV = 2  # SPACK_HOME
    CONFIG_VAR = 3  # config:locations:x
    CONFIG_HOME_VAR = 4  # config:locations:home
    XDG_VAR = 5  # XDG_x_HOME
    NOTHING_SET = 6  # None of the above are set

    def unilateral_override(self):
        # The following mechanisms for indicating user preference
        # override the existence of data stored in its old location
        # in $spack prior to #47615
        return self in {
            Provenance.SPACK_ENV,
            Provenance.SPACK_HOME_ENV,
            Provenance.CONFIG_VAR,
            Provenance.CONFIG_HOME_VAR,
        }


class SpackPaths:

    relative_state_home = os.path.join(".local", "state")
    relative_data_home = os.path.join(".local", "share")
    relative_cache_home = ".cache"

    def __init__(self, base):
        self.base = base

        self._state_home = None
        self._data_home = None
        self._cache_home = None

        self.default_state_home, self.default_data_home, self.default_cache_home = (
            os.path.join(os.path.expanduser("~"), x, "spack")
            for x in [
                SpackPaths.relative_state_home,
                SpackPaths.relative_data_home,
                SpackPaths.relative_cache_home,
            ]
        )

    @property
    def state_home(self):
        if not self._state_home:
            self._state_home, self._state_home_provenance = self.resolve_a_home(
                ["SPACK_STATE_HOME", "SPACK_USER_CACHE_PATH"],
                "XDG_STATE_HOME",
                "state",
                SpackPaths.relative_state_home,
            )
        return self._state_home

    @property
    def cache_home(self):
        if not self._cache_home:
            self._cache_home, self._cache_home_provenance = self.resolve_a_home(
                "SPACK_CACHE_HOME", "XDG_CACHE_HOME", "cache", SpackPaths.relative_cache_home
            )
        return self._cache_home

    @property
    def data_home(self):
        if not self._data_home:
            self._data_home, self._data_home_provenance = self.resolve_a_home(
                "SPACK_DATA_HOME", "XDG_DATA_HOME", "data", SpackPaths.relative_data_home
            )
        return self._data_home

    @property
    def spack_home(self):
        disable_env = config.get("config:locations:disable_env", False)
        spack_home_env = os.environ.get("SPACK_HOME", None)
        if not disable_env and spack_home_env:
            return spack_home_env

        spack_home_cfg = config.get("config:locations:home", None)
        if spack_home_cfg:
            return spack_home_cfg

        return os.path.expanduser("~")

    @property
    def user_cache_path(self):
        return self.state_home

    @property
    def default_install_location(self):
        return self._decide_old_or_new_location(
            self.base.old_install_path,
            os.path.join(self.data_home, "installs"),
            os.path.join(self.default_data_home, "installs"),
            self._data_home_provenance,
        )

    def bypassed_old_installs_warning(self, _show=True):
        if (
            self.default_install_location != self.base.old_install_path
            and dir_is_occupied(self.base.old_install_path)
            and not self._data_home_provenance.unilateral_override()
        ):
            msg = (
                f"Detected installs in {self.base.old_install_path}; Spack's default"
                " install path resolution mechanism is active and determined that"
                f" {self.default_install_location} is where it should look for and"
                " place new installs. You can suppress this warning by setting"
                " config:install_tree:root, config:locations:home, config:locations:data,"
                " SPACK_DATA_HOME, or SPACK_HOME"
            )
            if _show:
                tty.warn(msg)
            return msg
        return ""

    def bypassed_old_envs_warning(self, _show=True):
        if (
            self.default_envs_path != self.base.old_envs_path
            and dir_is_occupied(self.base.old_envs_path)
            and not self._data_home_provenance.unilateral_override()
        ):
            msg = (
                f"Detected environments in {self.base.old_envs_path}; Spack's default"
                " environment path resolution mechanism is active and determined that"
                f" {self.default_envs_path} is where it should look for and"
                " place new environments. You can suppress this warning by setting"
                " config:install_tree:root, config:locations:home, config:locations:data,"
                " SPACK_DATA_HOME, or SPACK_HOME"
            )
            if _show:
                tty.warn(msg)
            return msg
        return ""

    @property
    def default_envs_path(self):
        return self._decide_old_or_new_location(
            self.base.old_envs_path,
            os.path.join(self.data_home, "envs"),
            os.path.join(self.default_data_home, "envs"),
            self._data_home_provenance,
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
        return self._decide_old_or_new_location(
            self.base.old_gpg_path,
            os.path.join(self.data_home, "gpg"),
            os.path.join(self.default_data_home, "gpg"),
            self._data_home_provenance,
        )

    @property
    def gpg_keys_path(self):
        return self._decide_old_or_new_location(
            self.base.old_gpg_keys_path,
            os.path.join(self.data_home, "gpg-keys"),
            os.path.join(self.default_data_home, "gpg-keys"),
            self._data_home_provenance,
        )

    @property
    def default_misc_cache_path(self):
        #: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
        #: overridden by `config:misc_cache`
        # TODO: restore when .ci/gitlab/configs/ci.yaml in spack-packages is
        # updated to tolerate this relocation of misc caches
        # return os.path.join(self.state_home, self.spack_instance_id, "cache")
        return os.path.join(self.state_home, "cache")

    def __getattr__(self, name):
        # Things that aren't sensitive to import cycles can import the
        # paths module and access all items from paths_base
        try:
            base = object.__getattribute__(self, "base")
        except AttributeError:
            raise AttributeError(name)
        return getattr(base, name)

    def resolve_a_home(self, spack_vars, xdg_var, config_var, home_rel):
        """
        Data stored by spack is split into state, data, and cache components.
        This function can resolve where each of these components should be
        stored.

        Args:
            spack_vars: spack-specific environment variables that indicate the
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

        append_rel = lambda base, rel: str(pathlib.Path(base) / (rel or ""))

        def cfg_check(path, provenance, rel=None):
            found = config.get(path, None)
            if found:
                import spack.util.path

                with spack.util.path.limited_paths():
                    found = spack.util.path.canonicalize_path(found)
                return append_rel(found, rel), provenance

        spack_cfg_check = partial(
            cfg_check, f"config:locations:{config_var}", Provenance.CONFIG_VAR
        )
        spack_home_cfg_check = partial(
            cfg_check,
            "config:locations:home",
            Provenance.CONFIG_HOME_VAR,
            rel=os.path.join(home_rel, "spack"),
        )

        def env_check(env_vars, provenance, rel=None):
            if disable_env:
                return

            for v in env_vars:
                if v in os.environ:
                    return append_rel(os.environ[v], rel), provenance

        spack_vars = [spack_vars] if isinstance(spack_vars, str) else spack_vars
        spack_env_check = partial(env_check, spack_vars, Provenance.SPACK_ENV)
        spack_home_env_check = partial(
            env_check,
            ["SPACK_HOME"],
            Provenance.SPACK_HOME_ENV,
            rel=os.path.join(home_rel, "spack"),
        )
        xdg_env_check = partial(env_check, [xdg_var], Provenance.XDG_VAR, rel="spack")

        for check in [
            spack_env_check,
            spack_home_env_check,
            spack_cfg_check,
            spack_home_cfg_check,
            xdg_env_check,
        ]:
            possible_resolution = check()
            if possible_resolution:
                path, provenance = possible_resolution
                return os.path.expanduser(path), provenance

        return os.path.join(os.path.expanduser("~"), home_rel, "spack"), Provenance.NOTHING_SET

    def _decide_old_or_new_location(
        self, old_location, new_location, default_new_location, provenance
    ):
        if dir_is_occupied(new_location) or provenance.unilateral_override():
            return new_location
        elif dir_is_occupied(default_new_location):
            # This can occur e.g. if someone clones a new instance of spack,
            # which would write into the default new location, and then later
            # they set XDG_DATA_HOME
            return new_location
        elif dir_is_occupied(old_location):
            return old_location
        else:
            return new_location

    @property
    def modules_base(self):
        # This is similar to logic _decide_old_or_new_location, but this
        # moves the modules base if any component (typically one of lmod or
        # tcl) has been relocated, so is examining one-layer deeper
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.data_home, module_dir)):
                return self.data_home

        new_default_is_occupied = False
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.data_home, module_dir)):
                new_default_is_occupied = True
                break
        if new_default_is_occupied:
            return self.data_home

        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.base.share_path, module_dir)):
                return self.base.share_path
        return self.data_home


locations = SpackPaths(paths_base.locations)


def freeze():
    """
    Run this first-thing when starting a spack child process that is
    used for builds. Resolve all variables that are XDG-dependent, in
    case the build sets those XDG variables.

    Note that for this reason, the private variables like _data_home
    are important for more than just caching.
    """
    locations.state_home
    locations.data_home
    locations.cache_home


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

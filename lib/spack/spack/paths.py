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
from contextlib import contextmanager
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


class XDG_vars(Enum):
    state_home = "XDG_STATE_HOME"
    data_home = "XDG_DATA_HOME"
    cache_home = "XDG_CACHE_HOME"


class Spack_vars(Enum):
    state_home = "SPACK_STATE_HOME"
    data_home = "SPACK_DATA_HOME"
    cache_home = "SPACK_CACHE_HOME"
    user_cache_path = "SPACK_USER_CACHE_PATH"
    home = "SPACK_HOME"


# This is for tests that want to clean the environment of XDG_ variables that
# affect spack behavior. Note that this will not influence install_test.py's
# view of config:test_stage
def _unset_path_vars(env):
    for env_var in itertools.chain(XDG_vars, Spack_vars):
        env.pop(env_var.value, None)


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
                "state",
                SpackPaths.relative_state_home,
                "XDG_STATE_HOME",
            )
        return self._state_home

    @property
    def cache_home(self):
        if not self._cache_home:
            self._cache_home, self._cache_home_provenance = self.resolve_a_home(
                "SPACK_CACHE_HOME", "cache", SpackPaths.relative_cache_home, "XDG_CACHE_HOME"
            )
        return self._cache_home

    @property
    def data_home(self):
        if not self._data_home:
            self._data_home, self._data_home_provenance = self.resolve_a_home(
                "SPACK_DATA_HOME", "data", SpackPaths.relative_data_home, "XDG_DATA_HOME"
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

    @contextmanager
    def redirect_state_home(self, x):
        old = self._state_home
        self._state_home = x
        yield
        if old:
            self._state_home = old

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

    def __getattr__(self, name):
        # Things that aren't sensitive to import cycles can import the
        # paths module and access all items from paths_base
        try:
            base = object.__getattribute__(self, "base")
        except AttributeError:
            raise AttributeError(name)
        return getattr(base, name)

    def resolve_a_home(self, spack_vars, config_var, home_rel, xdg_var):
        """
        Files stored by spack are split into state, data, and cache components.
        Each of these categories has the same fall-through/prioritization path,
        established by this function:

            1. ``SPACK_x_HOME``: for example if the ``SPACK_DATA_HOME`` env var is
               set, it has the highest precedence.
            2. If the ``SPACK_HOME`` env variable is set, it can collect all of these
               components together
            3. ``config:locations:x``
            4. ``config:locations:home``
            5. ``XDG_x_HOME``: e.g. if the ``XDG_DATA_HOME`` env var is set
            6. In the user's home directory, in the XDG default location for that
               component.

        Note that configuration settings for specific data (e.g.
        ``config:install_tree:root`` for where installs are placed) will take
        precedence over any of this.

        Args:
            spack_vars: spack-specific environment variables that indicate the
                component location. Can be a list or a single variable. If this
                is a list, earlier elements have precedence.
            config_var: the spack config variable that indicates the component
                location.
            home_rel: for $SPACK_HOME and config:locations:home, this relative
                path is appended to the result to get the component location.
            xdg_var: the XDG-based environment variable that indicates the
                component location.
        """
        disable_env = config.get("config:locations:disable_env", False)

        append_rel = lambda base, rel: str(pathlib.Path(base) / (rel or ""))

        def cfg_check(path, provenance, rel=None):
            found = config.get(path, None)
            if found:
                import spack.util.path

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

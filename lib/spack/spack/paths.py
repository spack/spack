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
import spack.paths_base as paths_base


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    if not x.is_dir():
        return False
    for path in x.iterdir():
        if path.parts[-1] not in except_for:
            return True
    return False


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

    @classmethod
    def new_layout(cls):
        # Exclude SPACK_USER_CACHE_PATH
        return [
            Spack_vars.state_home,
            Spack_vars.data_home,
            Spack_vars.cache_home,
            Spack_vars.home,
        ]


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

        self.default_data_home = os.path.join(
            os.path.expanduser("~"), SpackPaths.relative_data_home, "spack"
        )

        self.old_layout_detected = detect_old_spack_layout(base)
        self._new_layout_enforced = None

    @property
    def new_layout_enforced(self):
        if self._new_layout_enforced is None:
            self._new_layout_enforced = new_layout_enforced()
        return self._new_layout_enforced

    @property
    def state_home(self):
        if not self._state_home:
            state_home, _ = self.resolve_a_home(
                ["SPACK_STATE_HOME", "SPACK_USER_CACHE_PATH"],
                "state",
                SpackPaths.relative_state_home,
                "XDG_STATE_HOME",
            )

            self.default_state_home_dot_spack = False

            def cfg_state_home():
                return config.get("config:locations:home", None) or config.get(
                    "config:locations:state", None
                )

            def env_state_home():
                disable_env = config.get("config:locations:disable_env", False)
                return not disable_env and any(
                    x in os.environ
                    for x in ["SPACK_USER_CACHE_PATH", "SPACK_STATE_HOME", "SPACK_HOME"]
                )

            if env_state_home() or cfg_state_home():
                self._state_home = state_home
            elif dir_is_occupied(state_home):
                self._state_home = state_home
            elif dir_is_occupied(self.base.old_default_dot_spack):
                self._state_home = self.base.old_default_dot_spack
                self.default_state_home_dot_spack = True
            else:
                self._state_home = state_home

        return self._state_home

    @property
    def cache_home(self):
        if not self._cache_home:
            self._cache_home, _ = self.resolve_a_home(
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
    def data_home_provenance(self):
        if not self._data_home_provenance:
            self._data_home, self._data_home_provenance = self.resolve_a_home(
                "SPACK_DATA_HOME", "data", SpackPaths.relative_data_home, "XDG_DATA_HOME"
            )
        return self._data_home_provenance

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
            self.data_home_provenance,
        )

    @property
    def default_envs_path(self):
        return self._decide_old_or_new_location(
            self.base.old_envs_path,
            os.path.join(self.data_home, "environments"),
            os.path.join(self.default_data_home, "environments"),
            self.data_home_provenance,
        )

    @property
    def default_license_dir(self):
        if self.old_layout_detected:
            return self.base.old_licenses_path
        else:
            return os.path.join(self.data_home, "licenses")

    @property
    def default_modules_base(self):
        if self.old_layout_detected:
            return self.base.share_path
        else:
            return os.path.join(self.data_home)

    @property
    def default_downloads_dir(self):
        if self.old_layout_detected:
            return self.base.old_fetch_cache_path
        else:
            return os.path.join(self.data_home, "downloads")

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

    @contextmanager
    def redirect_state_home(self, x):
        old = self._state_home
        self._state_home = x
        yield
        self._state_home = old

    @contextmanager
    def redirect_user_repos_cache_path(self, x):
        # This is under state_home, but tests may want to selectively redirect
        # only this attribute (e.g. to avoid regenerating provider cache)
        self._user_repos_cache_path = x
        yield
        delattr(self, "_user_repos_cache_path")

    @property
    def package_repos_path(self):
        #: default location where remote package repositories are cloned
        return os.path.join(self.state_home, "package_repos")

    @property
    def dotspack_backup(self):
        #: backup location for old ~/.spack directory during migration
        return os.path.join(self.data_home, "dotspack_backup")

    @property
    def gpg_path(self):
        return self._decide_old_or_new_location(
            self.base.old_gpg_path,
            os.path.join(self.data_home, "gpg"),
            os.path.join(self.default_data_home, "gpg"),
            self.data_home_provenance,
        )

    @property
    def gpg_keys_path(self):
        return self._decide_old_or_new_location(
            self.base.old_gpg_keys_path,
            os.path.join(self.data_home, "gpg-keys"),
            os.path.join(self.default_data_home, "gpg-keys"),
            self.data_home_provenance,
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
        if self.new_layout_enforced:
            return new_location
        if self.old_layout_detected:
            return old_location
        else:
            return new_location


def new_layout_enforced():
    cfg = config.get("config:locations", {})
    for x in ["home", "data", "state", "cache"]:
        if cfg.get(x, None):
            return True

    use_env = not bool(cfg.get("disable_env", False))
    return use_env and any(x.value in os.environ for x in Spack_vars.new_layout())


def detect_old_spack_layout(paths: paths_base.SpackPathsBase):
    checks = [
        # It's important if this directory is occupied but we have a separate
        # check for that, so exclude that directory here
        (paths.old_install_path, ["gpg"]),
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


locations = SpackPaths(paths_base.locations)


def freeze():
    """
    Run this first-thing when starting a spack child process that is
    used for builds. Resolve all variables that are XDG-dependent, in
    case the build sets those XDG variables.

    Note that for this reason, the private variables like _data_home
    are important for more than just caching.
    """
    return {
        "state_home": locations.state_home,
        "data_home": locations.data_home,
        "cache_home": locations.cache_home,
        "old_layout_detected": locations.old_layout_detected,
        "new_layout_enforced": new_layout_enforced(),
    }


def restore(bundled_state):
    locations._state_home = bundled_state["state_home"]
    locations._data_home = bundled_state["data_home"]
    locations._cache_home = bundled_state["cache_home"]
    locations.old_layout_detected = bundled_state["old_layout_detected"]
    locations._new_layout_enforced = bundled_state["new_layout_enforced"]

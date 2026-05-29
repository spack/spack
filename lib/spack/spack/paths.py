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
import sys as _sys
import types as _types
from contextlib import contextmanager
from enum import Enum
from functools import partial
from typing import TYPE_CHECKING

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
        # Exclude SPACK_USER_CACHE_PATH (legacy env var, doesn't signal new
        # layout preference the way the others do).
        return [
            Spack_vars.state_home,
            Spack_vars.data_home,
            Spack_vars.cache_home,
            Spack_vars.home,
        ]


# Used by tests to scrub the environment of XDG_ variables that would
# affect Spack's path resolution. Does not influence config:test_stage.
def _unset_path_vars(env):
    for env_var in itertools.chain(XDG_vars, Spack_vars):
        env.pop(env_var.value, None)


# Relative paths under SPACK_HOME used when SPACK_HOME or
# config:locations:home is set without explicit data/state/cache homes.
_RELATIVE_STATE = os.path.join(".local", "state")
_RELATIVE_DATA = os.path.join(".local", "share")
_RELATIVE_CACHE = ".cache"


class SpackPaths:
    """Per-instance Spack path resolution.

    The four "home" properties (``state_home``, ``data_home``,
    ``cache_home``, ``spack_home``) resolve to whatever the active layout
    scheme yaml provides via ``config:locations:*`` — with two
    higher-priority overrides preserved in Python:

        1. ``SPACK_x_HOME`` env var (highest)
        2. ``SPACK_HOME`` env var with the XDG-style subpath appended
        3. ``config:locations:x`` (from scheme yaml or higher scopes)
        4. ``config:locations:home`` with subpath (rarely needed when
           scheme yaml is loaded, but kept for completeness)

    Everything else that used to live in this module as ``default_*``
    properties (default install root, envs root, license dir, gpg paths,
    download cache) now comes directly from config, with the active
    scheme yaml supplying the defaults. See
    ``etc/spack/defaults/{old,xdg}/config.yaml``.
    """

    def __init__(self, base):
        self.base = base

        self._state_home = None
        self._data_home = None
        self._cache_home = None

        self.old_layout_detected = detect_old_spack_layout(base)

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

        def cfg_check(path, rel=None):
            found = config.get(path, None)
            if found:
                import spack.util.path

                found = spack.util.path.canonicalize_path(found)
                return append_rel(found, rel)

        spack_cfg_check = partial(cfg_check, f"config:locations:{config_var}")
        spack_home_cfg_check = partial(
            cfg_check, "config:locations:home", rel=os.path.join(home_rel, "spack")
        )

        def env_check(env_vars, rel=None):
            if disable_env:
                return

            for v in env_vars:
                if v in os.environ:
                    return append_rel(os.environ[v], rel)

        spack_vars = [spack_vars] if isinstance(spack_vars, str) else spack_vars
        spack_env_check = partial(env_check, spack_vars)
        spack_home_env_check = partial(
            env_check, ["SPACK_HOME"], rel=os.path.join(home_rel, "spack")
        )
        xdg_env_check = partial(env_check, [xdg_var], rel="spack")

        for check in [
            spack_env_check,
            spack_home_env_check,
            spack_cfg_check,
            spack_home_cfg_check,
            xdg_env_check,
        ]:
            possible_resolution = check()
            if possible_resolution:
                return os.path.expanduser(possible_resolution)

        return os.path.join(os.path.expanduser("~"), home_rel, "spack")

    @property
    def state_home(self):
        if not self._state_home:
            # SPACK_USER_CACHE_PATH is a legacy alias for SPACK_STATE_HOME.
            self._state_home = self.resolve_a_home(
                ["SPACK_USER_CACHE_PATH", "SPACK_STATE_HOME"],
                "state",
                _RELATIVE_STATE,
                "XDG_STATE_HOME",
            )
        return self._state_home

    @property
    def cache_home(self):
        if not self._cache_home:
            self._cache_home = self.resolve_a_home(
                "SPACK_CACHE_HOME", "cache", _RELATIVE_CACHE, "XDG_CACHE_HOME"
            )
        return self._cache_home

    @property
    def data_home(self):
        if not self._data_home:
            self._data_home = self.resolve_a_home(
                "SPACK_DATA_HOME", "data", _RELATIVE_DATA, "XDG_DATA_HOME"
            )
        return self._data_home

    @property
    def spack_home(self):
        disable_env = config.get("config:locations:disable_env", False)
        if not disable_env:
            env_home = os.environ.get("SPACK_HOME")
            if env_home:
                return os.path.expanduser(env_home)

        cfg_home = config.get("config:locations:home", None)
        if cfg_home:
            import spack.util.path

            return spack.util.path.canonicalize_path(cfg_home)

        return os.path.expanduser("~")

    @property
    def user_cache_path(self):
        return self.state_home

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
        #: backup location for old ~/.spack directory during migration.
        # Pinned to the XDG default (~/.local/share/spack/dotspack_backup)
        # rather than the active scheme's data_home, because the backup is
        # a one-time migration artifact and shouldn't move around when the
        # user sets SPACK_DATA_HOME or config:locations:data.
        return os.path.join(os.path.expanduser("~"), _RELATIVE_DATA, "spack", "dotspack_backup")

    @property
    def gpg_path(self):
        cfg = config.get("config:gpg_path", None)
        if cfg:
            import spack.util.path

            return spack.util.path.canonicalize_path(cfg)
        return os.path.join(self.data_home, "gpg")

    @property
    def gpg_keys_path(self):
        cfg = config.get("config:gpg_keys_path", None)
        if cfg:
            import spack.util.path

            return spack.util.path.canonicalize_path(cfg)
        return os.path.join(self.data_home, "gpg-keys")

    def __getattr__(self, name):
        # Things that aren't sensitive to import cycles can import the
        # paths module and access all items from paths_base
        try:
            base = object.__getattribute__(self, "base")
        except AttributeError:
            raise AttributeError(name)
        return getattr(base, name)


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


def detect_layout(scheme):
    """True if ``scheme`` is the active layout (``"old"`` or ``"xdg"``).

    Used by ``etc/spack/defaults/include.yaml`` to choose which scheme
    yaml to include. Honors "unilateral override": if the user has set
    any new-style location env var (SPACK_DATA_HOME, SPACK_STATE_HOME,
    SPACK_CACHE_HOME, SPACK_HOME), xdg is selected even when legacy
    $spack-local data is present.

    Cannot call ``config.get(...)`` here: this runs during config
    initialization (an include's ``when:`` is evaluated before the scope
    is pushed), so reading config would recurse into the singleton init.
    Env-var + filesystem probes only. config:locations:* set in
    user/site/system scopes still overrides specific values once those
    scopes are loaded.
    """
    if scheme not in ("old", "xdg"):
        raise ValueError(f"unknown layout scheme: {scheme!r} (expected 'old' or 'xdg')")
    env_forces_new = any(v.value in os.environ for v in Spack_vars.new_layout())
    is_old = detect_old_spack_layout(paths_base.locations) and not env_forces_new
    return is_old if scheme == "old" else not is_old


locations = SpackPaths(paths_base.locations)


def freeze():
    """Snapshot resolved homes for a child build process.

    Builds may set their own XDG_* env vars, which would otherwise change
    Spack's path resolution mid-build. Call this in the parent, ship the
    dict to the child, and call ``restore()`` there.
    """
    # Look up locations dynamically so tests can monkeypatch it
    import spack.paths as paths_module
    locs = paths_module.locations

    return {
        "state_home": locs.state_home,
        "data_home": locs.data_home,
        "cache_home": locs.cache_home,
        "old_layout_detected": locs.old_layout_detected,
    }


def restore(bundled_state):
    # Look up locations dynamically so tests can monkeypatch it
    import spack.paths as paths_module
    locs = paths_module.locations

    locs._state_home = bundled_state["state_home"]
    locs._data_home = bundled_state["data_home"]
    locs._cache_home = bundled_state["cache_home"]
    locs.old_layout_detected = bundled_state["old_layout_detected"]


# Type hints for mypy - these module-level attributes are dynamically resolved at runtime
# via the module shim below. Declared here so mypy can see them when checking imports.
if TYPE_CHECKING:
    # From SpackPaths
    state_home: str
    data_home: str
    cache_home: str
    spack_home: str
    user_cache_path: str
    reports_path: str
    default_monitor_path: str
    user_repos_cache_path: str
    package_repos_path: str
    dotspack_backup: str
    gpg_path: str
    gpg_keys_path: str
    old_layout_detected: bool

    # From SpackPathsBase (via delegation)
    prefix: str
    spack_root: str
    bin_path: str
    spack_script: str
    sbang_script: str
    lib_path: str
    external_path: str
    module_path: str
    vendor_path: str
    command_path: str
    platform_path: str
    compilers_path: str
    operating_system_path: str
    test_path: str
    hooks_path: str
    share_path: str
    etc_path: str
    var_path: str
    test_repos_path: str
    mock_packages_path: str
    mock_gpg_data_path: str
    mock_gpg_keys_path: str
    old_install_path: str
    old_envs_path: str
    old_fetch_cache_path: str
    old_gpg_path: str
    old_gpg_keys_path: str
    old_licenses_path: str
    old_default_dot_spack: str
    user_config_path: str
    system_config_path: str
    spack_instance_id: str


# Module shim: lets callers keep using `spack.paths.X` for any attribute on
# `locations` (e.g. `spack.paths.gpg_path`), which itself delegates to
# `paths_base.locations` for static attributes (e.g. `spack.paths.prefix`).
# Uses a sys.modules swap because Spack still supports Python 3.6, which
# predates PEP 562 (module-level `__getattr__`). When 3.6 support is dropped,
# replace this block with a plain
# `def __getattr__(name): return getattr(locations, name)`.
class _PathsModule(_types.ModuleType):
    def __getattr__(self, name: str) -> str:
        return getattr(locations, name)  # type: ignore[return-value]


_shim = _PathsModule(__name__)
_shim.__dict__.update(_sys.modules[__name__].__dict__)
_sys.modules[__name__] = _shim

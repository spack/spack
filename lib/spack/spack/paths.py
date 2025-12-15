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
from collections import namedtuple
from enum import Enum
from pathlib import PurePath

import spack.util.hash as hash
import spack.paths_base as paths_base
import spack.config as config


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
    saved = {}
    for xdg_var in itertools.chain(XDG_vars, XDG_overrides):
        if xdg_var.value in env:
            saved[xdg_var.value] = env.pop(xdg_var.value)
    return saved


def _spack_xdg_or_backup(xdg_mapping):
    if xdg_mapping.spack in os.environ:
        val = os.environ[xdg_mapping.spack]
    elif xdg_mapping.xdg in os.environ:
        val = os.path.join(os.environ[xdg_mapping.xdg], "spack")
    else:
        val = os.path.join(xdg_mapping.xdg_default, "spack")

    return os.path.expanduser(val)


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
            ["SPACK_USER_CACHE_PATH", "SPACK_STATE_HOME"],
            "XDG_STATE_HOME",
            "state",
            ".local/state/spack",
        )

    @property
    def cache_home(self):
        return self.resolve_a_home("SPACK_CACHE_HOME", "XDG_CACHE_HOME", "cache", ".cache/spack")

    @property
    def data_home(self):
        return self.resolve_a_home(
            "SPACK_DATA_HOME", "XDG_DATA_HOME", "data", ".local/share/spack"
        )

    @property
    def user_cache_path(self):
        return self.state_home

    @property
    def default_install_location(self):
        return self.prefer_old_location(
            self.base.old_install_path, os.path.join(self.data_home, "installs")
        )

    @property
    def default_envs_path(self):
        return self.prefer_old_location(
            self.base.old_envs_path, os.path.join(self.data_home, "envs")
        )

    @property
    def default_fetch_cache_path(self):
        return self.prefer_old_location(
            self.base.old_fetch_cache_path, os.path.join(self.data_home, "downloads")
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
        return os.path.join(self.state_home, "git_repos")

    @property
    def package_repos_path(self):
        #: default location where remote package repositories are cloned
        return os.path.join(self.state_home, "package_repos")

    @property
    def default_user_bootstrap_path(self):
        #: bootstrap store for bootstrapping clingo and other tools
        #: overridden by `bootstrap:root`
        return os.path.join(self.state_home, "bootstrap")

    @property
    def gpg_path(self):
        return self.prefer_old_location(
            self.base.old_gpg_path, os.path.join(self.data_home, "gpg")
        )

    @property
    def gpg_keys_path(self):
        return self.prefer_old_location(
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
            return os.environ.get(xdg_var, None)

        def spack_home_env_check():
            if disable_env:
                return
            if "SPACK_HOME" in os.environ:
                return os.path.join(os.environ["SPACK_HOME"], home_rel)

        def cfg_check():
            return config.get(f"config:locations:{config_var}", None)

        def spack_home_cfg_check():
            h = config.get("config:locations:home", None)
            if h:
                return os.path.join(h, home_rel)

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

        return os.path.join(os.path.expanduser("~"), home_rel)

    def prefer_old_location(self, old_location, new_location):
        # TODO: perhaps it should be configurable whether old locations
        # are used. Other option is to relocate downloads & gpg keys.
        # TODO: if user sets SPACK/XDG_DATA_HOME, should we move installs
        # there even if old dir is occupied? (right now that's what is
        # happening here)
        if dir_is_occupied(old_location):
            return old_location
        else:
            return new_location


locations = SpackPaths(paths_base.locations)

spack_script = locations.spack_script

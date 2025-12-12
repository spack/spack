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


xdg_mapping = namedtuple("xdg_mapping", ["spack", "xdg", "xdg_default"])


class XDG_mappings(Enum):
    config_home = xdg_mapping(
        spack=XDG_overrides.config_home.value,
        xdg=XDG_vars.config_home.value,
        xdg_default=os.path.join("~", ".config"),
    )
    state_home = xdg_mapping(
        spack=XDG_overrides.state_home.value,
        xdg=XDG_vars.state_home.value,
        xdg_default=os.path.join("~", ".local", "state"),
    )
    data_home = xdg_mapping(
        spack=XDG_overrides.data_home.value,
        xdg=XDG_vars.data_home.value,
        xdg_default=os.path.join("~", ".local", "share"),
    )
    cache_home = xdg_mapping(
        spack=XDG_overrides.cache_home.value,
        xdg=XDG_vars.cache_home.value,
        xdg_default=os.path.join("~", ".cache"),
    )


class Location_vars(Enum):
    user_cache_path = "USER_CACHE_PATH"


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
        #: Not a location itself, but used for when Spack instances
        #: share the same cache base directory for caches that should
        #: not be shared between those instances.
        self.spack_instance_id = hash.b32_hash(base.prefix)[:7]

        # Resolved XDG_x_HOME variables, with additional "spack" subdirectory.
        # Resolves to default value from XDG spec if unset.
        self.spack_state_home = _spack_xdg_or_backup(XDG_mappings.state_home.value)
        self.spack_config_home = _spack_xdg_or_backup(XDG_mappings.config_home.value)
        self.spack_cache_home = _spack_xdg_or_backup(XDG_mappings.cache_home.value)
        self.spack_data_home = _spack_xdg_or_backup(XDG_mappings.data_home.value)

        self.default_install_location = self.large_data_component("installs", base.old_install_path)
        self.default_envs_path = self.large_data_component("environments", base.old_envs_path)
        self.default_fetch_cache_path = self.large_data_component(
            "downloads", base.old_fetch_cache_path
        )

        self.user_cache_path = str(
            PurePath(
                os.path.expanduser(
                    os.getenv("SPACK_USER_CACHE_PATH") or self.data_home_for_small_data()
                )
            )
        )

        #: junit, cdash, etc. reports about builds
        self.reports_path = os.path.join(self.user_cache_path, "reports")

        #: installation test (spack test) output
        self.default_test_path = os.path.join(self.user_cache_path, "test")

        #: spack monitor analysis directories
        self.default_monitor_path = os.path.join(self.reports_path, "monitor")

        #: git repositories fetched to compare commits to versions
        self.user_repos_cache_path = os.path.join(self.user_cache_path, "git_repos")

        #: default location where remote package repositories are cloned
        self.package_repos_path = os.path.join(self.user_cache_path, "package_repos")

        #: bootstrap store for bootstrapping clingo and other tools
        #: overridden by `bootstrap:root`
        self.default_user_bootstrap_path = os.path.join(self.user_cache_path, "bootstrap")

        old_gpg_path = os.path.join(base.prefix, "opt", "spack", "gpg")
        if dir_is_occupied(old_gpg_path):
            self.gpg_path = old_gpg_path
        else:
            self.gpg_path = os.path.join(self.user_cache_path, "gpg")

        old_gpg_keys_path = os.path.join(base.var_path, "gpg")
        if dir_is_occupied(old_gpg_keys_path):
            self.gpg_keys_path = old_gpg_keys_path
        else:
            self.gpg_keys_path = os.path.join(self.user_cache_path, "gpg-keys")

        self.modules_base = None
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(base.share_path, module_dir)):
                self.modules_base = base.share_path
        if not self.modules_base:
            self.modules_base = self.user_cache_path

        #: User configuration location
        self.user_config_path = os.path.expanduser(
            os.getenv("SPACK_USER_CONFIG_PATH") or self.spack_config_home
        )

        #: System configuration location
        self.system_config_path = os.path.expanduser(
            os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
        )

        #: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
        #: overridden by `config:misc_cache`
        self.default_misc_cache_path = os.path.join(
            self.spack_state_home, self.spack_instance_id, "cache"
        )

    def data_home_for_small_data(self):
        return self.spack_data_home

    def large_data_component(self, subdir, old_location):
        if XDG_overrides.data_home.value in os.environ:
            return os.path.join(os.environ[XDG_overrides.data_home.value], subdir)
        elif XDG_vars.data_home.value in os.environ:
            return os.path.expanduser(
                os.path.join(os.environ[XDG_vars.data_home.value], "spack", subdir)
            )
        else:
            return old_location


locations = SpackPaths(paths_base.locations)

spack_instance_id = locations.spack_instance_id
spack_state_home = locations.spack_state_home
spack_config_home = locations.spack_config_home
spack_cache_home = locations.spack_cache_home
spack_data_home = locations.spack_data_home
default_install_location = locations.default_install_location
default_envs_path = locations.default_envs_path
default_fetch_cache_path = locations.default_fetch_cache_path
user_cache_path = locations.user_cache_path
reports_path = locations.reports_path
default_test_path = locations.default_test_path
default_monitor_path = locations.default_monitor_path
user_repos_cache_path = locations.user_repos_cache_path
package_repos_path = locations.package_repos_path
default_user_bootstrap_path = locations.default_user_bootstrap_path
gpg_path = locations.gpg_path
gpg_keys_path = locations.gpg_keys_path
modules_base = locations.modules_base
user_config_path = locations.user_config_path
system_config_path = locations.system_config_path
default_misc_cache_path = locations.default_misc_cache_path

# Copy from paths_base
prefix = paths_base.prefix
spack_root = paths_base.spack_root
bin_path = paths_base.bin_path
spack_script = paths_base.spack_script
sbang_script = paths_base.sbang_script
lib_path = paths_base.lib_path
external_path = paths_base.external_path
module_path = paths_base.module_path
vendor_path = paths_base.vendor_path
command_path = paths_base.command_path
analyzers_path = paths_base.analyzers_path
platform_path = paths_base.platform_path
compilers_path = paths_base.compilers_path
operating_system_path = paths_base.operating_system_path
test_path = paths_base.test_path
hooks_path = paths_base.hooks_path
share_path = paths_base.share_path
etc_path = paths_base.etc_path
default_license_dir = paths_base.default_license_dir
var_path = paths_base.var_path
repos_path = paths_base.repos_path
test_repos_path = paths_base.test_repos_path
mock_packages_path = paths_base.mock_packages_path
mock_gpg_data_path = paths_base.mock_gpg_data_path
mock_gpg_keys_path = paths_base.mock_gpg_keys_path
default_xdg_cache_home = paths_base.default_xdg_cache_home
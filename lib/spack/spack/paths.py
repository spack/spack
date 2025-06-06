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
from pathlib import PurePath

import llnl.util.filesystem

import spack.util.hash as hash


class XDG_vars(Enum):
    config_home = "XDG_CONFIG_HOME"
    state_home = "XDG_STATE_HOME"
    data_home = "XDG_DATA_HOME"
    cache_home = "XDG_CACHE_HOME"


class Location_vars(Enum):
    user_cache_path = "USER_CACHE_PATH"
    spack_data_home = "SPACK_DATA_HOME"


# This is for tests that want to clean the environment of XDG_ variables that
# affect spack behavior
def _unset_xdg_vars(env):
    saved = {}
    for xdg_var in XDG_vars:
        if xdg_var.value in env:
            saved[xdg_var.value] = env.pop(xdg_var.value)
    return saved


def _define_xdg_or_backup(xdg_var, backup):
    if xdg_var in os.environ:
        spack_xdg_defined = os.path.join(os.environ[xdg_var], "spack")
    else:
        spack_xdg_defined = os.path.join(backup, "spack")
    return os.path.expanduser(spack_xdg_defined)


def dir_is_occupied(x, except_for=None):
    x = pathlib.Path(x)
    except_for = except_for or set()
    return x.is_dir() and bool(set(x.iterdir()) - except_for)


class SpackPaths:
    def __init__(self, _prefix=None):
        #: This file lives in $prefix/lib/spack/spack/__file__
        self.prefix = _prefix or str(PurePath(llnl.util.filesystem.ancestor(__file__, 4)))

        #: synonym for prefix
        self.spack_root = self.prefix

        #: bin directory in the spack prefix
        self.bin_path = os.path.join(self.prefix, "bin")

        #: The spack script itself
        self.spack_script = os.path.join(self.bin_path, "spack")

        #: The sbang script in the spack installation
        self.sbang_script = os.path.join(self.bin_path, "sbang")

        # spack directory hierarchy
        self.lib_path = os.path.join(self.prefix, "lib", "spack")
        self.external_path = os.path.join(self.lib_path, "external")
        self.module_path = os.path.join(self.lib_path, "spack")
        self.command_path = os.path.join(self.module_path, "cmd")
        self.analyzers_path = os.path.join(self.module_path, "analyzers")
        self.platform_path = os.path.join(self.module_path, "platforms")
        self.compilers_path = os.path.join(self.module_path, "compilers")
        self.operating_system_path = os.path.join(self.module_path, "operating_systems")
        self.test_path = os.path.join(self.module_path, "test")
        self.hooks_path = os.path.join(self.module_path, "hooks")
        self.share_path = os.path.join(self.prefix, "share", "spack")
        self.etc_path = os.path.join(self.prefix, "etc", "spack")
        self.default_license_dir = os.path.join(self.etc_path, "licenses")
        self.var_path = os.path.join(self.prefix, "var", "spack")

        # $spack/var/spack is generally read-only. Older instances may
        # write gpg keys or environments into ...var/
        self.repos_path = os.path.join(self.var_path, "repos")
        self.test_repos_path = os.path.join(self.var_path, "test_repos")
        self.mock_packages_path = os.path.join(self.test_repos_path, "spack_repo", "builtin_mock")

        self.mock_gpg_data_path = os.path.join(self.var_path, "gpg.mock", "data")
        self.mock_gpg_keys_path = os.path.join(self.var_path, "gpg.mock", "keys")

        #: Not a location itself, but used for when Spack instances
        #: share the same cache base directory for caches that should
        #: not be shared between those instances.
        self.spack_instance_id = hash.b32_hash(self.prefix)[:7]

        # Resolved XDG_x_HOME variables, with additional "spack" subdirectory.
        # Resolves to default value from XDG spec if unset.
        self.xdg_state_home = _define_xdg_or_backup(
            XDG_vars.state_home.value, os.path.join("~", ".local", "state")
        )
        self.xdg_config_home = _define_xdg_or_backup(
            XDG_vars.config_home.value, os.path.join("~", ".config")
        )
        self.xdg_cache_home = _define_xdg_or_backup(
            XDG_vars.cache_home.value, os.path.join("~", ".cache")
        )
        self.xdg_data_home = _define_xdg_or_backup(
            XDG_vars.data_home.value, os.path.join("~", ".local", "share")
        )

        # ------ Next section
        # Spack can write a lot of data into the next 3 locations, and
        # they used to be inside of Spack by default. They can be set
        # to any location with `config:` settings, and those have priority.
        # They can also be redirected by setting the SPACK_DATA_HOME or
        # XDG_DATA_HOME environment variables. If none of those are
        # set, then they point to inside of the Spack prefix.
        #
        # Precedence:
        # 1. config: setting (code consults the config before this
        #    module)
        # 2. explicitly defined SPACK_DATA_HOME
        # 3. explicitly defined XDG_DATA_HOME
        # 4. old default path, if occupied (inside spack prefix)
        # 5. inside spack prefix (slightly different compared to old
        #    install path)
        old_install_path = os.path.join(self.prefix, "opt", "spack")
        self.default_install_location = self.large_data_component("installs", old_install_path)

        old_envs_path = os.path.join(self.var_path, "environments")
        self.default_envs_path = self.large_data_component("environments", old_envs_path)

        old_fetch_cache_path = os.path.join(self.var_path, "cache")
        self.default_fetch_cache_path = self.large_data_component(
            "downloads", old_fetch_cache_path
        )

        # ------ Next section
        # Spack can write data into the following locations, but it
        # isn't expected to be substantial, so Spack can choose to set
        # "~" as a default. They are all organized under a single
        # directory that users can refer to in config as $user_cache_path
        #
        # You can override the top-level directory (the user cache path) by
        # setting `SPACK_USER_CACHE_PATH`, `SPACK_DATA_HOME`, or
        # `XDG_DATA_HOME`; if none of those are set, then the default for
        # `XDG_DATA_HOME` is used (~/.local/share).
        #
        # Precedence:
        # 1. Config setting (not available for all of these)
        # 2. SPACK_USER_CACHE_PATH
        # 3. explicitly defined SPACK_DATA_HOME
        # 4. explicitly defined XDG_DATA_HOME
        # 5. default for XDG_DATA_HOME
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

        # ------ Next section
        # The next three locations used to be written inside of the
        # Spack prefix, and are now organized under $user_cache_path
        # by default, *except* for old installs of Spack that have
        # data written into the old locations (in which case, when
        # they pull this update, they will continue to use those
        # locations)

        old_gpg_path = os.path.join("prefix", "opt" "spack", "gpg")
        if dir_is_occupied(old_gpg_path):
            self.gpg_path = old_gpg_path
        else:
            self.gpg_path = os.path.join(self.user_cache_path, "gpg")

        old_gpg_keys_path = os.path.join(self.var_path, "gpg")
        if dir_is_occupied(old_gpg_keys_path):
            self.gpg_keys_path = old_gpg_keys_path
        else:
            self.gpg_keys_path = os.path.join(self.user_cache_path, "gpg-keys")

        self.modules_base = None
        for module_dir in ["lmod", "modules"]:
            if dir_is_occupied(os.path.join(self.share_path, module_dir)):
                self.modules_base = self.share_path
        if not self.modules_base:
            self.modules_base = os.path.join(self.user_cache_path, "modules")

        # ------ Next section
        # Spack can also write data into the following locations, and their
        # defaults are not controlled by SPACK/XDG_DATA_HOME or
        # SPACK_USER_CACHE_PATH. Like the prior section, the data written
        # into these locations isn't expected to take up much space, so in
        # some cases defaults to "~" (in those cases in compliance with
        # XDG defaults).

        # There are three environment variables you can use to isolate spack from
        # the host environment:
        # - `SPACK_USER_CONFIG_PATH`: override `~/.spack` location (for config and caches)
        # - `SPACK_SYSTEM_CONFIG_PATH`: override `/etc/spack` configuration scope.
        # - `SPACK_DISABLE_LOCAL_CONFIG`: disable both of these locations.

        #: User configuration location
        self.user_config_path = os.path.expanduser(
            os.getenv("SPACK_USER_CONFIG_PATH") or self.xdg_config_home
        )

        #: System configuration location
        self.system_config_path = os.path.expanduser(
            os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
        )

        #: When Spack is provided by an admin to a user, the admin can
        #: provide a config that only applies for the end-users
        self.end_user_cfg_path = os.path.join(self.system_config_path, "end-user")

        #: transient caches for Spack data (virtual cache, patch sha256 lookup, etc.)
        #: overridden by `config:misc_cache`
        self.default_misc_cache_path = os.path.join(
            self.xdg_state_home, self.spack_instance_id, "misc-cache"
        )

        #: concretization cache for Spack concretizations
        #: overridden by `config:concretization_cache:url`
        self.default_conc_cache_path = os.path.join(self.default_misc_cache_path, "concretization")

    def data_home_for_small_data(self):
        if Location_vars.spack_data_home.value in os.environ:
            return os.environ[Location_vars.spack_data_home.value]
        else:
            return self.xdg_data_home

    def large_data_component(self, subdir, old_location):
        if Location_vars.spack_data_home.value in os.environ:
            return os.path.join(os.environ[Location_vars.spack_data_home.value], subdir)
        elif XDG_vars.data_home.value in os.environ:
            return os.path.expanduser(
                os.path.join(os.environ[XDG_vars.data_home.value], "spack", subdir)
            )
        elif dir_is_occupied(old_location):
            return old_location
        else:
            return os.path.join(self.prefix, "opt", "data", subdir)


locations = SpackPaths()

prefix = locations.prefix
spack_root = locations.spack_root
bin_path = locations.bin_path
spack_script = locations.spack_script
sbang_script = locations.sbang_script
lib_path = locations.lib_path
external_path = locations.external_path
module_path = locations.module_path
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
repos_path = locations.repos_path
test_repos_path = locations.test_repos_path
mock_packages_path = locations.mock_packages_path
mock_gpg_data_path = locations.mock_gpg_data_path
mock_gpg_keys_path = locations.mock_gpg_keys_path
spack_instance_id = locations.spack_instance_id
xdg_state_home = locations.xdg_state_home
xdg_config_home = locations.xdg_config_home
xdg_cache_home = locations.xdg_cache_home
xdg_data_home = locations.xdg_data_home
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
end_user_cfg_path = locations.end_user_cfg_path
default_misc_cache_path = locations.default_misc_cache_path
default_conc_cache_path = locations.default_conc_cache_path


#: Recorded directory where spack command was originally invoked
spack_working_dir = None


def set_working_dir():
    """Change the working directory to getcwd, or spack prefix if no cwd."""
    global spack_working_dir
    try:
        spack_working_dir = os.getcwd()
    except OSError:
        os.chdir(prefix)
        spack_working_dir = prefix

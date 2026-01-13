# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import os
from enum import Enum
from pathlib import PurePath

import spack.llnl.util.filesystem


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


class SpackPathsBase:
    def __init__(self, _prefix=None):
        #: This file lives in $prefix/lib/spack/spack/__file__
        self.prefix = _prefix or str(PurePath(spack.llnl.util.filesystem.ancestor(__file__, 4)))

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
        self.vendor_path = os.path.join(self.module_path, "vendor")
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
        self.test_repos_path = os.path.join(self.var_path, "test_repos")
        self.mock_packages_path = os.path.join(self.test_repos_path, "spack_repo", "builtin_mock")

        self.mock_gpg_data_path = os.path.join(self.var_path, "gpg.mock", "data")
        self.mock_gpg_keys_path = os.path.join(self.var_path, "gpg.mock", "keys")

        self.old_install_path = os.path.join(self.prefix, "opt", "spack")
        self.old_envs_path = os.path.join(self.var_path, "environments")
        self.old_fetch_cache_path = os.path.join(self.var_path, "cache")
        self.old_gpg_path = os.path.join(self.prefix, "opt", "spack", "gpg")
        self.old_gpg_keys_path = os.path.join(self.var_path, "gpg")

        #: User configuration location
        self.user_config_path = os.path.expanduser(
            os.getenv("SPACK_USER_CONFIG_PATH") or os.path.join("~", ".config", "spack")
        )

        #: System configuration location
        self.system_config_path = os.path.expanduser(
            os.getenv("SPACK_SYSTEM_CONFIG_PATH") or os.sep + os.path.join("etc", "spack")
        )

    @property
    def env_based_state_home(self):
        """Spack has config-based logic for choosing a home for most state, but
        this is specifically for caching state related to the config system
        itself: it is based entirely on env vars and not on configuration
        variables. It is not affected by `config:locations:disable_env`.
        """
        override = lambda: os.environ.get(XDG_overrides.state_home.value)
        xdg = lambda: os.environ.get(XDG_vars.state_home.value)
        default = lambda: os.path.expanduser(os.path.join("~", ".state", "spack"))
        return override() or xdg() or default()


locations = SpackPathsBase()
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
system_config_path = locations.system_config_path
user_config_path = locations.user_config_path


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

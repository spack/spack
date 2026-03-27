# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import os
from enum import Enum
from pathlib import PurePath

import spack.llnl.util.filesystem
import spack.util.hash as hash


class XDG_vars(Enum):
    state_home = "XDG_STATE_HOME"
    data_home = "XDG_DATA_HOME"
    cache_home = "XDG_CACHE_HOME"


class XDG_overrides(Enum):
    state_home = "SPACK_STATE_HOME"
    data_home = "SPACK_DATA_HOME"
    cache_home = "SPACK_CACHE_HOME"


# This is for tests that want to clean the environment of XDG_ variables that
# affect spack behavior. Note that this will not influence install_test.py's
# view of config:test_stage
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
        self.platform_path = os.path.join(self.module_path, "platforms")
        self.compilers_path = os.path.join(self.module_path, "compilers")
        self.operating_system_path = os.path.join(self.module_path, "operating_systems")
        self.test_path = os.path.join(self.module_path, "test")
        self.hooks_path = os.path.join(self.module_path, "hooks")
        self.share_path = os.path.join(self.prefix, "share", "spack")
        self.etc_path = os.path.join(self.prefix, "etc", "spack")
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

        #: Not a location itself, but used for when Spack instances
        #: share the same cache base directory for caches that should
        #: not be shared between those instances.
        self.spack_instance_id = hash.b32_hash(self.prefix)[:7]


locations = SpackPathsBase()

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

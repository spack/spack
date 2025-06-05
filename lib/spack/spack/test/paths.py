# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import spack.paths as paths


def test_install_location(working_env, tmpdir):
    base_prefix = str(tmpdir.join("prefix").ensure(dir=True))
    xdg_data_home = str(tmpdir.join("xdg_data_home"))
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p1 = paths.SpackPaths(base_prefix)
    assert p1.default_install_location == str(pathlib.Path(xdg_data_home) / "spack" / "installs")

    # Check that SPACK_DATA_HOME overrides
    spack_data_home = str(tmpdir.join("spack_data_home"))
    os.environ["SPACK_DATA_HOME"] = spack_data_home
    p2 = paths.SpackPaths(base_prefix)
    assert p2.default_install_location == str(pathlib.Path(spack_data_home) / "installs")


def test_system_config_path_is_overridable(working_env, tmpdir):
    redirect_syscfg_path = "/some/path"
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = redirect_syscfg_path
    p1 = paths.SpackPaths(str(tmpdir))
    assert p1.system_config_path == redirect_syscfg_path


def test_system_config_path_is_default_when_env_var_is_empty(working_env, tmpdir):
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = ""
    p1 = paths.SpackPaths(str(tmpdir))
    assert os.sep + os.path.join("etc", "spack") == p1.system_config_path


def test_user_config_path_is_overridable(working_env, tmpdir):
    redirect_usrcfg_path = "/some/path"
    os.environ["SPACK_USER_CONFIG_PATH"] = redirect_usrcfg_path
    p1 = paths.SpackPaths(str(tmpdir))
    assert p1.user_config_path == redirect_usrcfg_path


def test_user_config_path_is_default_when_env_var_is_empty(working_env, tmpdir):
    os.environ["SPACK_USER_CONFIG_PATH"] = ""
    p1 = paths.SpackPaths(str(tmpdir))
    assert os.path.expanduser(os.path.join("~", ".config", "spack")) == p1.user_config_path


def test_user_cache_path_is_overridable(working_env, tmpdir):
    redirect_usr_cache = "/some/path"
    os.environ["SPACK_USER_CACHE_PATH"] = redirect_usr_cache
    p1 = paths.SpackPaths(str(tmpdir))
    assert p1.user_cache_path == redirect_usr_cache


def test_user_cache_path_is_default_when_env_var_is_empty(working_env, tmpdir):
    os.environ["SPACK_USER_CACHE_PATH"] = ""
    p1 = paths.SpackPaths(str(tmpdir))
    assert (
        os.path.expanduser(os.path.join("~", ".local", "share", "spack"))
        == p1.user_cache_path
    )
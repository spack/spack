# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import spack.config
from spack.paths import SpackPaths
from spack.paths_base import SpackPathsBase


def _ensure_dir(pathlike):
    pathlike.mkdir(parents=True, exist_ok=True)
    return str(pathlike)


def test_install_location(working_env, tmp_path, mutable_config):
    # If prior default install dir inside spack prefix does not
    # exist, place installs in $HOME
    base_prefix = _ensure_dir(tmp_path / "spack-root")
    home_prefix = _ensure_dir(tmp_path / "home-prefix")
    os.environ.pop("USERPROFILE", None)
    os.environ.pop("HOMEDRIVE", None)
    os.environ.pop("HOMEPATH", None)
    os.environ["HOME"] = home_prefix
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    assert p1.default_install_location == str(
        pathlib.Path(home_prefix) / ".local" / "share" / "spack" / "installs"
    )

    spack.config.set("config:locations", {})

    # "config:locations:home" variable overrides default
    spack_home_prefix = _ensure_dir(tmp_path / "spack-home")
    spack.config.set("config:locations:home", spack_home_prefix)
    p2 = SpackPaths(SpackPathsBase(base_prefix))
    assert p2.default_install_location == str(
        pathlib.Path(spack_home_prefix) / ".local" / "share" / "spack" / "installs"
    )

    # "config:locations:data" overrides the above
    spack_data_prefix = _ensure_dir(tmp_path / "spack-data")
    spack.config.set("config:locations:data", spack_data_prefix)
    p3 = SpackPaths(SpackPathsBase(base_prefix))
    assert p3.default_install_location == str(pathlib.Path(spack_data_prefix) / "installs")

    # $XDG_DATA_HOME overrides all the above
    xdg_data_home = _ensure_dir(tmp_path / "xdg_data_home")
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p4 = SpackPaths(SpackPathsBase(base_prefix))
    assert p4.default_install_location == str(pathlib.Path(xdg_data_home) / "spack" / "installs")

    # Check that $SPACK_DATA_HOME overrides all the above
    spack_data_home = _ensure_dir(tmp_path / "spack_data_home")
    os.environ["SPACK_DATA_HOME"] = spack_data_home
    p5 = SpackPaths(SpackPathsBase(base_prefix))
    assert p5.default_install_location == str(pathlib.Path(spack_data_home) / "installs")

    # Disable all location-based env vars: this will then defer
    # to using "config:locations:data"
    spack.config.set("config:locations:disable_env", True)
    p6 = SpackPaths(SpackPathsBase(base_prefix))
    assert p6.default_install_location == str(pathlib.Path(spack_data_prefix) / "installs")


def test_system_config_path_is_overridable(working_env, tmp_path):
    redirect_syscfg_path = str(pathlib.Path(tmp_path) / "redirected_syscfg")
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = redirect_syscfg_path
    p1 = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base-prefix")))
    assert p1.system_config_path == redirect_syscfg_path


def test_system_config_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = ""
    p1 = SpackPaths(SpackPathsBase(str(tmp_path)))
    assert os.sep + os.path.join("etc", "spack") == p1.system_config_path


def test_user_config_path_is_overridable(working_env, tmp_path):
    redirect_usrcfg_path = str(pathlib.Path(tmp_path) / "redirected_usrcfg")
    os.environ["SPACK_USER_CONFIG_PATH"] = redirect_usrcfg_path
    p1 = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base-prefix")))
    assert p1.user_config_path == redirect_usrcfg_path


def test_user_config_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_USER_CONFIG_PATH"] = ""
    p1 = SpackPaths(SpackPathsBase(str(tmp_path)))
    assert os.path.expanduser(os.path.join("~", ".config", "spack")) == p1.user_config_path


def test_user_cache_path_is_overridable(working_env, tmp_path):
    redirect_usr_cache = str(pathlib.Path(tmp_path) / "redirected_usr_cache")
    os.environ["SPACK_USER_CACHE_PATH"] = redirect_usr_cache
    p1 = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base-prefix")))
    assert p1.user_cache_path == redirect_usr_cache

    # Check that things that are supposed to be bundled inside of
    # $user_cache_path are also relocated
    assert p1.package_repos_path == str(pathlib.Path(redirect_usr_cache) / "package_repos")


def test_gpg_only_use_new_path_if_old_is_empty(working_env, tmp_path):
    base_prefix = _ensure_dir(tmp_path / "base-prefix")
    os.environ["HOME"] = base_prefix

    new_default_gpg_base = pathlib.Path(base_prefix) / ".local" / "share" / "spack"

    p1 = SpackPaths(SpackPathsBase(base_prefix))
    assert p1.gpg_path == str(new_default_gpg_base / "gpg")
    assert p1.gpg_keys_path == str(new_default_gpg_base / "gpg-keys")

    old_gpg_dir = pathlib.Path(base_prefix) / "opt" / "spack" / "gpg"
    (old_gpg_dir).mkdir(parents=True)
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    # Old dir exists, but is empty, so it should not be used
    assert p1.gpg_path == str(new_default_gpg_base / "gpg")
    (old_gpg_dir / "something").touch()
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    # Now it should redirect
    assert p1.gpg_path == str(old_gpg_dir)
    # But the keys are handled separately and should use the new path
    assert p1.gpg_keys_path == str(new_default_gpg_base / "gpg-keys")

    old_gpg_keys_dir = pathlib.Path(base_prefix) / "var" / "spack" / "gpg"
    old_gpg_keys_dir.mkdir(parents=True)
    (old_gpg_keys_dir / "something").touch()
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    assert p1.gpg_keys_path == str(old_gpg_keys_dir)


def test_user_cache_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_USER_CACHE_PATH"] = ""
    p1 = SpackPaths(SpackPathsBase(str(tmp_path)))
    assert os.path.expanduser(os.path.join("~", ".local", "state", "spack")) == p1.user_cache_path

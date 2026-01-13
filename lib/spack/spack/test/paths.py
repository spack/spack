# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.config
import spack.paths_base
from spack.paths import SpackPaths
from spack.paths_base import SpackPathsBase


def _ensure_dir(pathlike):
    pathlike.mkdir(parents=True, exist_ok=True)
    return str(pathlike)


@pytest.fixture(scope="module", autouse=True)
def clear_xdg_vars():
    saved = os.environ.copy()
    spack.paths_base._unset_xdg_vars(os.environ)
    yield
    os.environ.update(saved)


@pytest.fixture
def set_home():
    def _set_home(val):
        # Clear some env vars that can interfere w/ expanduser(~) on Windows
        os.environ.pop("USERPROFILE", None)
        os.environ.pop("HOMEDRIVE", None)
        os.environ.pop("HOMEPATH", None)
        os.environ["HOMEPATH"] = val

        # For expanduser on Linux
        os.environ["HOME"] = val

    yield _set_home


def test_install_location(working_env, tmp_path, mutable_config, set_home):
    # If prior default install dir inside spack prefix does not
    # exist, place installs in $HOME
    base_prefix = _ensure_dir(tmp_path / "spack-root")
    home_prefix = _ensure_dir(tmp_path / "home-prefix")

    empty_dir = _ensure_dir(tmp_path / "empty")

    def paths_base_empty_old_install():
        pb = SpackPathsBase(base_prefix)
        pb.old_install_path = empty_dir
        return pb

    set_home(home_prefix)

    p1 = SpackPaths(paths_base_empty_old_install())
    assert p1.default_install_location == str(
        pathlib.Path(home_prefix) / ".local" / "share" / "spack" / "installs"
    )

    spack.config.set("config:locations", {})

    # "config:locations:home" variable overrides default
    spack_home_prefix = _ensure_dir(tmp_path / "spack-home")
    spack.config.set("config:locations:home", spack_home_prefix)
    p2 = SpackPaths(paths_base_empty_old_install())
    assert p2.default_install_location == str(
        pathlib.Path(spack_home_prefix) / ".local" / "share" / "spack" / "installs"
    )

    # "config:locations:data" overrides the above
    spack_data_prefix = _ensure_dir(tmp_path / "spack-data")
    spack.config.set("config:locations:data", spack_data_prefix)
    p3 = SpackPaths(paths_base_empty_old_install())
    assert p3.default_install_location == str(pathlib.Path(spack_data_prefix) / "installs")

    # $XDG_DATA_HOME overrides all the above
    xdg_data_home = _ensure_dir(tmp_path / "xdg_data_home")
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p4 = SpackPaths(paths_base_empty_old_install())
    assert p4.default_install_location == str(pathlib.Path(xdg_data_home) / "spack" / "installs")

    # Check that $SPACK_DATA_HOME overrides all the above
    spack_data_home = _ensure_dir(tmp_path / "spack_data_home")
    os.environ["SPACK_DATA_HOME"] = spack_data_home
    p5 = SpackPaths(paths_base_empty_old_install())
    assert p5.default_install_location == str(pathlib.Path(spack_data_home) / "installs")

    # Disable all location-based env vars: this will then defer
    # to using "config:locations:data"
    spack.config.set("config:locations:disable_env", True)
    p6 = SpackPaths(paths_base_empty_old_install())
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
    redirect1 = str(pathlib.Path(tmp_path) / "redirected_usr_cache")
    os.environ["SPACK_USER_CACHE_PATH"] = redirect1
    p1 = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base-prefix")))
    assert p1.user_cache_path == redirect1
    # Check that things that are supposed to be bundled inside of
    # $user_cache_path are also relocated
    assert p1.package_repos_path == str(pathlib.Path(redirect1) / "package_repos")

    # Now check that $SPACK_STATE_HOME takes precedence when both are set
    redirect2 = str(pathlib.Path(tmp_path) / "redirected_usr_cache2")
    os.environ["SPACK_STATE_HOME"] = redirect2
    assert p1.user_cache_path == redirect2
    assert p1.package_repos_path == str(pathlib.Path(redirect2) / "package_repos")


def test_gpg_only_use_new_path_if_old_is_empty(working_env, tmp_path, set_home):
    base_prefix = _ensure_dir(tmp_path / "base-prefix")
    set_home(base_prefix)

    new_default_gpg_base = pathlib.Path(base_prefix) / ".local" / "share" / "spack"

    p1 = SpackPaths(SpackPathsBase(base_prefix))
    assert p1.gpg_path == str(new_default_gpg_base / "gpg")
    assert p1.gpg_keys_path == str(new_default_gpg_base / "gpg-keys")

    old_gpg_dir = pathlib.Path(base_prefix) / "opt" / "spack" / "gpg"
    (old_gpg_dir).mkdir(parents=True)
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    # Old dir exists, but is empty, so it should not be used
    assert p1.gpg_path == str(new_default_gpg_base / "gpg")

    # Put something in the old dir: it should now redirect
    (old_gpg_dir / "something").touch()
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    assert p1.gpg_path == str(old_gpg_dir)

    # But the keys are handled separately and should use the new path
    new_gpg_keys_dir = pathlib.Path(new_default_gpg_base / "gpg-keys")
    assert p1.gpg_keys_path == str(new_gpg_keys_dir)

    # Check that the keys will also redirect
    old_gpg_keys_dir = pathlib.Path(base_prefix) / "var" / "spack" / "gpg"
    old_gpg_keys_dir.mkdir(parents=True)
    (old_gpg_keys_dir / "something").touch()
    p1 = SpackPaths(SpackPathsBase(base_prefix))
    assert p1.gpg_keys_path == str(old_gpg_keys_dir)

    # When something is in both the new and old locations, prefer the new
    new_gpg_keys_dir.mkdir(parents=True)
    (new_gpg_keys_dir / "something").touch()
    assert p1.gpg_keys_path == str(new_gpg_keys_dir)

    # And the gpg dir itself remains the old dir: reaffirm that
    assert p1.gpg_path == str(old_gpg_dir)


def test_user_cache_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_USER_CACHE_PATH"] = ""
    p1 = SpackPaths(SpackPathsBase(str(tmp_path)))
    assert os.path.expanduser(os.path.join("~", ".local", "state", "spack")) == p1.user_cache_path

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import spack.paths as paths


def _ensure_dir(pathlike):
    pathlike.mkdir(parents=True, exist_ok=True)
    return str(pathlike)


def test_install_location(working_env, tmp_path):
    # With no direction from env vars, a fresh clone of Spack
    # should default to using the Spack prefix. It was moved from
    # where it used to be
    base_prefix = _ensure_dir(tmp_path / "base-prefix")
    p1 = paths.SpackPaths(base_prefix)
    assert p1.default_install_location == str(
        pathlib.Path(base_prefix) / "opt" / "data" / "installs"
    )

    # If XDG_DATA_HOME and SPACK_DATA_HOME aren't set, and
    # there are installs in the old prefix, use that
    preexisting_install_dir = pathlib.Path(base_prefix) / "opt" / "spack" / ".spack-db"
    (preexisting_install_dir).mkdir(parents=True)
    p1 = paths.SpackPaths(base_prefix)
    assert p1.default_install_location == str(preexisting_install_dir.parent)

    # XDG_DATA_HOME overrides all the above
    xdg_data_home = _ensure_dir(tmp_path / "xdg_data_home")
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p1 = paths.SpackPaths(base_prefix)
    assert p1.default_install_location == str(pathlib.Path(xdg_data_home) / "spack" / "installs")

    # Check that SPACK_DATA_HOME overrides all the above
    spack_data_home = _ensure_dir(tmp_path / "spack_data_home")
    os.environ["SPACK_DATA_HOME"] = spack_data_home
    p2 = paths.SpackPaths(base_prefix)
    assert p2.default_install_location == str(pathlib.Path(spack_data_home) / "installs")


def test_system_config_path_is_overridable(working_env, tmp_path):
    redirect_syscfg_path = str(pathlib.Path(tmp_path) / "redirected_syscfg")
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = redirect_syscfg_path
    p1 = paths.SpackPaths(_ensure_dir(tmp_path / "base-prefix"))
    assert p1.system_config_path == redirect_syscfg_path


def test_system_config_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_SYSTEM_CONFIG_PATH"] = ""
    p1 = paths.SpackPaths(str(tmp_path))
    assert os.sep + os.path.join("etc", "spack") == p1.system_config_path


def test_user_config_path_is_overridable(working_env, tmp_path):
    redirect_usrcfg_path = str(pathlib.Path(tmp_path) / "redirected_usrcfg")
    os.environ["SPACK_USER_CONFIG_PATH"] = redirect_usrcfg_path
    p1 = paths.SpackPaths(_ensure_dir(tmp_path / "base-prefix"))
    assert p1.user_config_path == redirect_usrcfg_path


def test_user_config_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_USER_CONFIG_PATH"] = ""
    p1 = paths.SpackPaths(str(tmp_path))
    assert os.path.expanduser(os.path.join("~", ".config", "spack")) == p1.user_config_path


def test_user_cache_path_is_overridable(working_env, tmp_path):
    redirect_usr_cache = str(pathlib.Path(tmp_path) / "redirected_usr_cache")
    os.environ["SPACK_USER_CACHE_PATH"] = redirect_usr_cache
    p1 = paths.SpackPaths(_ensure_dir(tmp_path / "base-prefix"))
    assert p1.user_cache_path == redirect_usr_cache

    # Check that things that are supposed to be bundled inside of
    # $user_cache_path are also relocated
    assert p1.package_repos_path == str(pathlib.Path(redirect_usr_cache) / "package_repos")


def test_gpg_only_use_new_path_if_old_is_empty(working_env, tmp_path):
    user_cache_path = _ensure_dir(tmp_path / "user-cache")
    base_prefix = _ensure_dir(tmp_path / "base-prefix")
    os.environ["SPACK_USER_CACHE_PATH"] = user_cache_path

    p1 = paths.SpackPaths(base_prefix)
    assert p1.gpg_path == str(pathlib.Path(user_cache_path) / "gpg")
    assert p1.gpg_keys_path == str(pathlib.Path(user_cache_path) / "gpg-keys")

    old_gpg_dir = pathlib.Path(base_prefix) / "opt" / "spack" / "gpg"
    (old_gpg_dir).mkdir(parents=True)
    p1 = paths.SpackPaths(base_prefix)
    # Old dir exists, but is empty, so it should not be used
    assert p1.gpg_path == str(pathlib.Path(user_cache_path) / "gpg")
    (old_gpg_dir / "something").touch()
    p1 = paths.SpackPaths(base_prefix)
    # Now it should redirect
    assert p1.gpg_path == str(old_gpg_dir)
    # But the keys are handled separately and should use the new path
    assert p1.gpg_keys_path == str(pathlib.Path(user_cache_path) / "gpg-keys")

    old_gpg_keys_dir = pathlib.Path(base_prefix) / "var" / "spack" / "gpg"
    old_gpg_keys_dir.mkdir(parents=True)
    (old_gpg_keys_dir / "something").touch()
    p1 = paths.SpackPaths(base_prefix)
    assert p1.gpg_keys_path == str(old_gpg_keys_dir)


def test_user_cache_path_is_default_when_env_var_is_empty(working_env, tmp_path):
    os.environ["SPACK_USER_CACHE_PATH"] = ""
    p1 = paths.SpackPaths(str(tmp_path))
    assert os.path.expanduser(os.path.join("~", ".local", "share", "spack")) == p1.user_cache_path

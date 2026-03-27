# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.config
import spack.paths
import spack.paths_base
import spack.subprocess_context
from spack.paths import SpackPaths
from spack.paths_base import SpackPathsBase


def _ensure_dir(pathlike):
    pathlike.mkdir(parents=True, exist_ok=True)
    return str(pathlike)


@pytest.fixture(autouse=True)
def clear_env_vars(working_env):
    spack.paths_base._unset_xdg_vars(os.environ)
    for x in [
        "SPACK_USER_CACHE_PATH",
        "SPACK_HOME",
        "SPACK_DATA_HOME",
        "SPACK_STATE_HOME",
        "SPACK_CACHE_HOME",
    ]:
        os.environ.pop(x, None)


@pytest.fixture
def set_home():
    def _set_home(val):
        # Clear some env vars that can interfere w/ expanduser(~) on Windows
        os.environ.pop("USERPROFILE", None)
        os.environ.pop("HOMEDRIVE", None)
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

    # $XDG_DATA_HOME overrides the default
    xdg_data_home = _ensure_dir(tmp_path / "xdg_data_home")
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p4 = SpackPaths(paths_base_empty_old_install())
    assert p4.default_install_location == str(pathlib.Path(xdg_data_home) / "spack" / "installs")

    _unconditional_path_override_checks(tmp_path, paths_base_empty_old_install)


def test_install_location_old_installs_exist(working_env, tmp_path, mutable_config, set_home):
    # If prior default install dir inside spack prefix does not
    # exist, place installs in $HOME
    base_prefix = _ensure_dir(tmp_path / "spack-root")
    home_prefix = _ensure_dir(tmp_path / "home-prefix")

    nonempty_dir = _ensure_dir(tmp_path / "not-empty")
    (pathlib.Path(nonempty_dir) / "afile").touch()

    def paths_base_nonempty_old_install():
        pb = SpackPathsBase(base_prefix)
        pb.old_install_path = nonempty_dir
        return pb

    set_home(home_prefix)

    # The new default installs dir is ignored if it is empty and
    # the old install location has anything in it
    p1 = SpackPaths(paths_base_nonempty_old_install())
    assert p1.default_install_location == nonempty_dir

    # If there are spack installs in the new installs dir, it is
    # preferred over the old dir
    new_default_installs_dir = _ensure_dir(
        pathlib.Path(home_prefix) / ".local" / "share" / "spack" / "installs"
    )
    (pathlib.Path(new_default_installs_dir) / "afile").touch()
    assert p1.default_install_location == new_default_installs_dir
    assert (
        f"{new_default_installs_dir} is where it should look"
        in p1.bypassed_old_installs_warning(_show=False)
    )

    spack.config.set("config:locations", {})

    # XDG_DATA_HOME overrides the old install location *even if it is empty
    # and the old install location is not*, if there are installs in the new
    # default location
    xdg_data_home = _ensure_dir(tmp_path / "xdg_data_home")
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p4 = SpackPaths(paths_base_nonempty_old_install())
    xdg_installs_location = _ensure_dir(pathlib.Path(xdg_data_home) / "spack" / "installs")
    assert p4.default_install_location == str(xdg_installs_location)
    assert f"{xdg_installs_location} is where it should look" in p4.bypassed_old_installs_warning(
        _show=False
    )

    # (sanity) XDG_DATA_HOME still overrides when there is something in it
    (pathlib.Path(xdg_installs_location) / "afile").touch()
    assert p4.default_install_location == str(xdg_installs_location)

    _unconditional_path_override_checks(tmp_path, paths_base_nonempty_old_install)


def _unconditional_path_override_checks(tmp_path, base_paths_generator):
    # "config:locations:home" variable overrides the above (even if there
    # are no installs there and there are installs in the old location)
    spack_home_cfg_prefix = _ensure_dir(tmp_path / "spack-home2")
    spack.config.set("config:locations:home", spack_home_cfg_prefix)
    p2 = SpackPaths(base_paths_generator())
    assert p2.default_install_location == str(
        pathlib.Path(spack_home_cfg_prefix) / ".local" / "share" / "spack" / "installs"
    )
    assert not p2.bypassed_old_installs_warning(_show=False)

    # "config:locations:data" overrides the above
    spack_data_prefix = _ensure_dir(tmp_path / "spack-data")
    spack.config.set("config:locations:data", spack_data_prefix)
    p3 = SpackPaths(base_paths_generator())
    assert p3.default_install_location == str(pathlib.Path(spack_data_prefix) / "installs")

    # SPACK_HOME env variable overrides the above (even if there
    # are no installs there and there are installs in the old location)
    spack_home_env_prefix = _ensure_dir(tmp_path / "spack-home1")
    os.environ["SPACK_HOME"] = spack_home_env_prefix
    p1 = SpackPaths(base_paths_generator())
    assert p1.default_install_location == str(
        pathlib.Path(spack_home_env_prefix) / ".local" / "share" / "spack" / "installs"
    )

    # Check that $SPACK_DATA_HOME overrides all the above
    spack_data_home = _ensure_dir(tmp_path / "spack_data_home")
    os.environ["SPACK_DATA_HOME"] = spack_data_home
    p5 = SpackPaths(base_paths_generator())
    assert p5.default_install_location == str(pathlib.Path(spack_data_home) / "installs")

    # Disable all location-based env vars: this will then defer
    # to using "config:locations:data"
    spack.config.set("config:locations:disable_env", True)
    p6 = SpackPaths(base_paths_generator())
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
    p2 = SpackPaths(SpackPathsBase(_ensure_dir(tmp_path / "base-prefix")))
    assert p2.user_cache_path == redirect2
    assert p2.package_repos_path == str(pathlib.Path(redirect2) / "package_repos")


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


def test_user_cache_path_is_default_when_env_var_is_empty(tmp_path, set_home):
    homedir = _ensure_dir(tmp_path / "base-prefix")
    set_home(homedir)
    p1 = SpackPaths(SpackPathsBase(str(tmp_path)))
    assert (
        str(pathlib.Path(homedir) / os.path.join(".local", "state", "spack")) == p1.user_cache_path
    )


def test_location_vars_that_use_other_location_vars(
    tmp_path, set_home, mutable_config, monkeypatch
):
    homedir = _ensure_dir(tmp_path / "test-home")
    set_home(homedir)

    basedir = _ensure_dir(tmp_path / "spack-root")

    mutable_config.set("config", {"locations": {"home": "$spack/home"}})

    p1 = SpackPaths(SpackPathsBase(str(basedir)))
    # This is a bit strange but resolution of the config variable involves accessing
    # the module, so we need to monkeypatch that
    monkeypatch.setattr(spack.paths_base, "locations", p1.base)
    install_rel = pathlib.Path(".local") / "share" / "spack" / "installs"
    assert p1.default_install_location == str(pathlib.Path(basedir) / "home" / install_rel)

    # Now try defining a $data_home -> $spack_home -> $spack
    p2 = SpackPaths(SpackPathsBase(str(basedir)))
    monkeypatch.setattr(spack.paths_base, "locations", p2.base)
    mutable_config.set("config", {"locations": {"home": "$spack/home", "data": "$spack_home"}})
    assert p2.default_install_location == str(pathlib.Path(basedir) / "home" / "installs")


def test_license_dir_config(mutable_config, mock_packages, tmp_path, monkeypatch, set_home):
    """Ensure license directory is customizable"""
    import spack.config
    import spack.package_base
    import spack.repo

    basedir = _ensure_dir(tmp_path / "spack-root")
    homedir = _ensure_dir(tmp_path / "base-prefix")
    set_home(homedir)

    p1 = SpackPaths(SpackPathsBase(str(basedir)))
    monkeypatch.setattr(spack.paths, "locations", p1)

    default_cfg_val = os.path.join("$data_home", "licenses")
    resolved_dir = str(pathlib.Path(homedir) / ".local" / "share" / "spack" / "licenses")
    assert spack.config.get("config:license_dir") == default_cfg_val
    assert spack.package_base.PackageBase.global_license_dir == resolved_dir
    assert spack.repo.PATH.get_pkg_class("pkg-a").global_license_dir == resolved_dir

    abs_path = str(tmp_path / "foo" / "bar" / "baz")
    spack.config.set("config:license_dir", abs_path)
    assert spack.config.get("config:license_dir") == abs_path
    assert spack.package_base.PackageBase.global_license_dir == abs_path
    assert spack.repo.PATH.get_pkg_class("pkg-a").global_license_dir == abs_path


class SetAnXdgVarAndReadDataHome:
    """Access an XDG-dependent variable from spack.paths as quickly as
    possible.
    """

    def __init__(self, home_prefix):
        self.home_prefix = home_prefix

    def __call__(self):
        import spack.paths

        os.environ["XDG_DATA_HOME"] = "/made-up-value-that-shouldnt-matter"

        expected = str(pathlib.Path(self.home_prefix) / ".local" / "share" / "spack" / "installs")
        assert (
            spack.paths.locations.default_install_location == expected
        ), f"Expected {expected}\nGot {spack.paths.locations.default_install_location}"


def test_child_proc_sanity_xdg_based_paths(tmp_path, set_home, monkeypatch):
    # Unlike the other tests in this module, this is specifically testing
    # the behavior of the spack.paths module vs. (the more targeted testing
    # of) classes defined within it.
    base_prefix = _ensure_dir(tmp_path / "spack-root")
    home_prefix = _ensure_dir(tmp_path / "home-prefix")

    empty_dir = _ensure_dir(tmp_path / "empty")

    set_home(home_prefix)

    import spack.paths

    pbtest = SpackPathsBase(base_prefix)
    pbtest.old_install_path = empty_dir
    ptest = SpackPaths(pbtest)
    monkeypatch.setattr(spack.paths, "locations", ptest)

    spack_process = spack.subprocess_context.SpackTestProcess(
        SetAnXdgVarAndReadDataHome(home_prefix)
    )
    p = spack_process.create()
    p.start()
    p.join()
    assert p.exitcode == 0

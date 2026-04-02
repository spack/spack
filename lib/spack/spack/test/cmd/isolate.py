# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil
from pathlib import Path

import pytest

import spack.config
import spack.paths_base
import spack.util.spack_yaml as syaml
from spack.main import SpackCommand
from spack.paths import SpackPaths
from spack.paths import locations as paths
from spack.paths_base import SpackPathsBase

isolate = SpackCommand("isolate")


@pytest.fixture()
def mock_spack_scope(tmp_path_factory, mutable_config):
    higher_scope_dir = tmp_path_factory.mktemp("higher")
    spack_scope_dir = tmp_path_factory.mktemp("test-spack-scope")
    lower_scope_dir = tmp_path_factory.mktemp("higher")

    # Copy the real spack scope includes into a test location, so that
    # we can check that this command modifies it.
    src_file = Path(paths.prefix) / "etc" / "spack" / "include.yaml"
    cpy_dst = str(Path(spack_scope_dir) / "include.yaml")
    shutil.copyfile(src_file, cpy_dst)

    scopes = [
        spack.config.DirectoryConfigScope("lower", str(lower_scope_dir)),
        spack.config.DirectoryConfigScope("spack", str(spack_scope_dir)),
        spack.config.DirectoryConfigScope("higher", str(higher_scope_dir)),
    ]

    with spack.config.use_configuration(*scopes) as config:
        yield config


def includes_as_a_dict():
    includes = spack.config.get("include")
    return dict((scope["name"], scope) for scope in includes)


def test_isolate_removes_scopes(mock_spack_scope):
    # In default case, spack has two scopes that point to locations
    # outside of spack. `spack isolate` should remove both if they
    # haven't been modified.

    assert not spack.config.get("config:locations:home")
    initial_cfg = includes_as_a_dict()
    assert "user" in initial_cfg
    assert "system" in initial_cfg

    spack.config.get("include")
    output = isolate()

    # Warnings would be printed if user modifications are detected.
    # In this test we haven't made any, so there shouldn't be any
    # warnings.
    assert "Warning:" not in output

    after_cfg = includes_as_a_dict()
    assert "user" not in after_cfg
    assert "system" not in after_cfg


def test_isolate_retains_scope_when_not_default(mock_spack_scope):
    cfg_as_dict = includes_as_a_dict()
    non_default_path = "/something/else/not/the/default"
    cfg_as_dict["user"]["path"] = non_default_path

    spack.config.set("include", syaml.syaml_list(cfg_as_dict.values()), scope="spack")
    isolate()

    after_cfg = includes_as_a_dict()
    assert "system" not in after_cfg
    assert after_cfg["user"]["path"] == non_default_path


@pytest.fixture
def redirect_base_paths(tmp_path_factory, monkeypatch):
    base_prefix = str(tmp_path_factory.mktemp("base-test"))
    pb = SpackPathsBase(base_prefix)
    # spack.util.path.canonicalize_path uses paths_base.locations
    # so this should generally be monkeypatched when testing anything
    # that modifies path vars
    monkeypatch.setattr(spack.paths_base, "locations", pb)
    yield pb


def test_isolate_redirect_installs(
    mock_spack_scope, set_home, tmp_path_factory, redirect_base_paths
):
    # in the default case where a user clones a new spack instance, it will
    # write into ~. Check that `spack isolate` redirects installs (for example)
    # into $spack
    base = redirect_base_paths
    home_prefix = str(tmp_path_factory.mktemp("home-test"))
    set_home(home_prefix)

    p1 = SpackPaths(base)
    assert p1.default_install_location == str(
        Path(home_prefix) / ".local" / "share" / "spack" / "installs"
    )

    isolate()

    p2 = SpackPaths(base)
    assert p2.default_install_location == str(
        Path(p2.base.prefix) / "all-data" / ".local" / "share" / "spack" / "installs"
    )


def test_isolate_cfg_points_outside_spack(
    mock_spack_scope, tmp_path_factory, mutable_config, redirect_base_paths
):
    # check that `spack isolate` will rewrite config:locations:home
    # when it points outside of $spack
    base = redirect_base_paths
    dir_outside_spack = str(tmp_path_factory.mktemp("outside-dir"))

    spack.config.set("config:locations", {"home": dir_outside_spack}, scope="spack")

    initial_expected = str(Path(dir_outside_spack) / ".local" / "share" / "spack" / "installs")
    p1 = SpackPaths(base)
    assert p1.default_install_location == initial_expected

    # First try to isolate without --force-... - nothing should happen
    cmd_output = isolate()
    assert "config:locations:home is outside of $spack" in cmd_output
    assert "You can override with --force-home" in cmd_output
    p2 = SpackPaths(base)
    assert p2.default_install_location == initial_expected

    isolate("--force-home")
    p3 = SpackPaths(base)
    assert p3.default_install_location == str(
        Path(base.prefix) / "all-data" / ".local" / "share" / "spack" / "installs"
    )


def test_isolate_unaffected_by_higher_scope(
    mock_spack_scope, tmp_path_factory, mutable_config, redirect_base_paths
):
    # set config:locations:home in a higher-precedence scope: make sure
    # that `spack isolate` does not interfere
    base = redirect_base_paths
    dir_outside_spack = str(tmp_path_factory.mktemp("outside-dir"))

    spack.config.set("config", {"locations": {"home": dir_outside_spack}}, scope="higher")

    p1 = SpackPaths(base)
    expected_path = str(Path(dir_outside_spack) / ".local" / "share" / "spack" / "installs")
    assert p1.default_install_location == expected_path

    isolate()

    p2 = SpackPaths(base)
    # `spack isolate` does not modify scopes other than the 'spack' scope
    assert p2.default_install_location == expected_path

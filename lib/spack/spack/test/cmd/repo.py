# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib

import pytest

import spack.config
import spack.environment as ev
import spack.main
import spack.repo
from spack.main import SpackCommand

repo = spack.main.SpackCommand("repo")
env = SpackCommand("env")


def test_help_option():
    # Test 'spack repo --help' to check basic import works
    # and the command exits successfully
    with pytest.raises(SystemExit):
        repo("--help")
    assert repo.returncode in (None, 0)


def test_create_add_list_remove(mutable_config, tmp_path: pathlib.Path):
    # Create a new repository and check that the expected
    # files are there
    repo("create", str(tmp_path), "mockrepo")
    assert (tmp_path / "spack_repo" / "mockrepo" / "repo.yaml").exists()

    # Add the new repository and check it appears in the list output
    repo("add", "--scope=site", str(tmp_path / "spack_repo" / "mockrepo"))
    output = repo("list", "--scope=site", output=str)
    assert "mockrepo" in output

    # Then remove it and check it's not there
    repo("remove", "--scope=site", str(tmp_path / "spack_repo" / "mockrepo"))
    output = repo("list", "--scope=site", output=str)
    assert "mockrepo" not in output


def test_env_repo_path_vars_substitution(
    tmpdir, install_mockery, mutable_mock_env_path, monkeypatch
):
    """Test Spack correctly substitues repo paths with environment variables when creating an
    environment from a manifest file."""

    monkeypatch.setenv("CUSTOM_REPO_PATH", ".")

    # setup environment from spack.yaml
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w", encoding="utf-8") as f:
            f.write(
                """\
spack:
  specs: []

  repos:
    - $CUSTOM_REPO_PATH
"""
            )
        # creating env from manifest file
        env("create", "test", "./spack.yaml")
        # check that repo path was correctly substituted with the environment variable
        current_dir = os.getcwd()
        with ev.read("test") as newenv:
            repos_specs = spack.config.get("repos", default={}, scope=newenv.scope_name)
            assert current_dir in repos_specs


def test_repo_migrate(tmp_path: pathlib.Path, config):
    path, _ = spack.repo.create_repo(str(tmp_path), "mockrepo", package_api=(2, 0))
    pkgs_path = spack.repo.from_path(path).packages_path

    pkg1 = pathlib.Path(os.path.join(pkgs_path, "foo", "package.py"))
    pkg2 = pathlib.Path(os.path.join(pkgs_path, "bar", "package.py"))

    pkg1.parent.mkdir(parents=True)
    pkg2.parent.mkdir(parents=True)

    pkg1.write_text(
        """\
# some comment

from spack.package import *

class Foo(Package):
    pass
""",
        encoding="utf-8",
    )
    pkg2.write_text(
        """\
# some comment

from spack.package import *

class Bar(CMakePackage):
    generator("ninja")
""",
        encoding="utf-8",
    )

    repo("migrate", path)

    assert (
        pkg1.read_text(encoding="utf-8")
        == """\
# some comment

from spack.build_systems.generic import Package
from spack.package import *

class Foo(Package):
    pass
"""
    )

    assert (
        pkg2.read_text(encoding="utf-8")
        == """\
# some comment

from spack.build_systems.cmake import CMakePackage, generator
from spack.package import *

class Bar(CMakePackage):
    generator("ninja")
"""
    )

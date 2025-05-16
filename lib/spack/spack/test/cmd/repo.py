# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io
import os
import pathlib

import pytest

from llnl.util.filesystem import working_dir

import spack.config
import spack.environment as ev
import spack.main
import spack.repo
import spack.repo_migrate
from spack.main import SpackCommand
from spack.util.executable import Executable

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


OLD_7ZIP = b"""\
# some comment

from spack.package import *

class _7zip(Package):
    pass
"""

NEW_7ZIP = b"""\
# some comment

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *

class _7zip(Package):
    pass
"""

OLD_NUMPY = b"""\
# some comment

from spack.package import *

class PyNumpy(CMakePackage):
    generator("ninja")
"""

NEW_NUMPY = b"""\
# some comment

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack.package import *

class PyNumpy(CMakePackage):
    generator("ninja")
"""


def test_repo_migrate(tmp_path: pathlib.Path, config):
    old_root, _ = spack.repo.create_repo(str(tmp_path), "org.repo", package_api=(1, 0))
    pkgs_path = pathlib.Path(spack.repo.from_path(old_root).packages_path)
    new_root = pathlib.Path(old_root) / "spack_repo" / "org" / "repo"

    pkg_7zip_old = pkgs_path / "7zip" / "package.py"
    pkg_numpy_old = pkgs_path / "py-numpy" / "package.py"
    pkg_py_7zip_new = new_root / "packages" / "_7zip" / "package.py"
    pkg_py_numpy_new = new_root / "packages" / "py_numpy" / "package.py"

    pkg_7zip_old.parent.mkdir(parents=True)
    pkg_numpy_old.parent.mkdir(parents=True)

    pkg_7zip_old.write_bytes(OLD_7ZIP)
    pkg_numpy_old.write_bytes(OLD_NUMPY)

    repo("migrate", "--fix", old_root)

    # old files are not touched since they are moved
    assert pkg_7zip_old.read_bytes() == OLD_7ZIP
    assert pkg_numpy_old.read_bytes() == OLD_NUMPY

    # new files are created and have updated contents
    assert pkg_py_7zip_new.read_bytes() == NEW_7ZIP
    assert pkg_py_numpy_new.read_bytes() == NEW_NUMPY


@pytest.mark.not_on_windows("Known failure on windows")
def test_migrate_diff(git: Executable, tmp_path: pathlib.Path):
    root, _ = spack.repo.create_repo(str(tmp_path), "foo", package_api=(2, 0))
    r = pathlib.Path(root)
    pkg_7zip = r / "packages" / "_7zip" / "package.py"
    pkg_py_numpy_new = r / "packages" / "py_numpy" / "package.py"
    pkg_broken = r / "packages" / "broken" / "package.py"

    pkg_7zip.parent.mkdir(parents=True)
    pkg_py_numpy_new.parent.mkdir(parents=True)
    pkg_broken.parent.mkdir(parents=True)
    pkg_7zip.write_bytes(OLD_7ZIP)
    pkg_py_numpy_new.write_bytes(OLD_NUMPY)
    pkg_broken.write_bytes(b"syntax(error")

    stderr = io.StringIO()

    with open(tmp_path / "imports.patch", "w", encoding="utf-8") as stdout:
        spack.repo_migrate.migrate_v2_imports(
            str(r / "packages"), str(r), fix=False, out=stdout, err=stderr
        )

    assert f"Skipping {pkg_broken}" in stderr.getvalue()

    # apply the patch and verify the changes
    with working_dir(str(r)):
        git("apply", str(tmp_path / "imports.patch"))

    assert pkg_7zip.read_bytes() == NEW_7ZIP
    assert pkg_py_numpy_new.read_bytes() == NEW_NUMPY

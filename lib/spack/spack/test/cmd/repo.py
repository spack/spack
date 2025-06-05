# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io
import os
import pathlib
import sys
from typing import Dict, Optional, Union

import pytest

from llnl.util.filesystem import working_dir

import spack.cmd.repo
import spack.config
import spack.environment as ev
import spack.main
import spack.repo
import spack.repo_migrate
from spack.error import SpackError
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
    current_dir: $CUSTOM_REPO_PATH
"""
            )
        # creating env from manifest file
        env("create", "test", "./spack.yaml")
        # check that repo path was correctly substituted with the environment variable
        current_dir = os.getcwd()
        with ev.read("test") as newenv:
            repos_specs = spack.config.get("repos", default={}, scope=newenv.scope_name)
            assert current_dir in repos_specs.values()


OLD_7ZIP = b"""\
# some comment

from spack.package import *
from .blt import linker_helpers

class _7zip(Package):
    pass
"""

NEW_7ZIP = b"""\
# some comment

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
from ..blt.package import linker_helpers

class _7zip(Package):
    pass
"""

# this is written like this to be explicit about line endings and indentation
OLD_NUMPY = (
    b"# some comment\r\n"
    b"\r\n"
    b"import spack.pkg.builtin.foo, spack.pkg.builtin.bar\r\n"
    b"from spack.package import *\r\n"
    b"from something.unrelated import AutotoolsPackage\r\n"
    b"from spack.pkg.builtin.num7zip import _7zip\r\n"
    b"\r\n"
    b"\r\n"
    b"class PyNumpy(CMakePackage, AutotoolsPackage):\r\n"
    b"\tgenerator('ninja')\r\n"
    b"\r\n"
    b"\tdef example(self):\r\n"
    b"\t\t# unchanged comment: spack.pkg.builtin.foo.something\r\n"
    b"\t\treturn spack.pkg.builtin.foo.example(), foo, baz\r\n"
)

NEW_NUMPY = (
    b"# some comment\r\n"
    b"\r\n"
    b"import spack_repo.builtin.packages.foo.package, spack_repo.builtin.packages.bar.package\r\n"
    b"from spack_repo.builtin.build_systems.cmake import CMakePackage, generator\r\n"
    b"from spack.package import *\r\n"
    b"from something.unrelated import AutotoolsPackage\r\n"
    b"from spack_repo.builtin.packages._7zip.package import _7zip\r\n"
    b"\r\n"
    b"\r\n"
    b"class PyNumpy(CMakePackage, AutotoolsPackage):\r\n"
    b"\tgenerator('ninja')\r\n"
    b"\r\n"
    b"\tdef example(self):\r\n"
    b"\t\t# unchanged comment: spack.pkg.builtin.foo.something\r\n"
    b"\t\treturn spack_repo.builtin.packages.foo.package.example(), foo, baz\r\n"
)

OLD_NONTRIVIAL_IMPORT = b"""\
if True:
    from spack.pkg.builtin import (
        foo,
        bar as baz,
        num7zip as my7zip
    )

class NonTrivialImport(Package):
    pass
"""


NEW_NONTRIVIAL_IMPORT = b"""\
from spack_repo.builtin.build_systems.generic import Package


if True:
    import spack_repo.builtin.packages.foo.package as foo
    import spack_repo.builtin.packages.bar.package as baz
    import spack_repo.builtin.packages._7zip.package as my7zip

class NonTrivialImport(Package):
    pass
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


def test_migrate_diff(git: Executable, tmp_path: pathlib.Path):
    root, _ = spack.repo.create_repo(str(tmp_path), "foo", package_api=(2, 0))
    r = pathlib.Path(root)
    pkg_7zip = r / "packages" / "_7zip" / "package.py"
    pkg_py_numpy = r / "packages" / "py_numpy" / "package.py"
    pkg_broken = r / "packages" / "broken" / "package.py"
    pkg_nontrivial_import = r / "packages" / "non_trivial_import" / "package.py"

    pkg_7zip.parent.mkdir(parents=True)
    pkg_py_numpy.parent.mkdir(parents=True)
    pkg_broken.parent.mkdir(parents=True)
    pkg_nontrivial_import.parent.mkdir(parents=True)

    pkg_7zip.write_bytes(OLD_7ZIP)
    pkg_py_numpy.write_bytes(OLD_NUMPY)
    pkg_broken.write_bytes(b"syntax(error")
    pkg_nontrivial_import.write_bytes(OLD_NONTRIVIAL_IMPORT)

    stderr = io.StringIO()

    with open(tmp_path / "imports.patch", "wb") as patch_file:
        spack.repo_migrate.migrate_v2_imports(
            str(r / "packages"), str(r), patch_file=patch_file, err=stderr
        )

    err_output = stderr.getvalue()

    assert f"Skipping {pkg_broken}" in err_output

    # apply the patch and verify the changes
    with working_dir(str(r)):
        git("apply", str(tmp_path / "imports.patch"))

    # Git may change line endings upon applying the patch, so let Python normalize in TextIOWrapper
    # and compare strings instead of bytes.
    assert (
        pkg_7zip.read_text(encoding="utf-8")
        == io.TextIOWrapper(io.BytesIO(NEW_7ZIP), encoding="utf-8").read()
    )
    assert (
        pkg_py_numpy.read_text(encoding="utf-8")
        == io.TextIOWrapper(io.BytesIO(NEW_NUMPY), encoding="utf-8").read()
    )

    # the multi-line non-trivial import rewrite cannot be done in Python < 3.8 because it doesn't
    # support end_lineno in ast.ImportFrom. So here we check that it's either warned about or
    # modified correctly.
    if sys.version_info >= (3, 8):
        assert (
            pkg_nontrivial_import.read_text(encoding="utf-8")
            == io.TextIOWrapper(io.BytesIO(NEW_NONTRIVIAL_IMPORT), encoding="utf-8").read()
        )
    else:
        assert (
            f"{pkg_nontrivial_import}:2: cannot rewrite spack.pkg.builtin import statement"
            in err_output
        )


class MockRepo(spack.repo.Repo):
    def __init__(self, namespace: str):
        self.namespace = namespace


class MockDescriptor(spack.repo.RepoDescriptor):
    def __init__(self, to_construct: Dict[str, Union[spack.repo.Repo, Exception]]):
        self.to_construct = to_construct
        self.initialized = False

    def initialize(self, fetch=True, git=None) -> None:
        self.initialized = True

    def construct(self, cache, overrides=None):
        assert self.initialized, "MockDescriptor must be initialized before construction"
        return self.to_construct


def make_repo_config(repo_config: Optional[dict] = None) -> spack.config.Configuration:
    """Create a Configuration instance with writable scope and optional repo configuration."""
    scope = spack.config.InternalConfigScope("test", {"repos": repo_config or {}})
    scope.writable = True
    config = spack.config.Configuration()
    config.push_scope(scope)
    return config


def test_add_repo_name_already_exists(tmp_path: pathlib.Path):
    """Test _add_repo raises error when name already exists in config."""
    # Set up existing config with the same name
    config = make_repo_config({"test_name": "/some/path"})

    # Should raise error when name already exists
    with pytest.raises(SpackError, match="A repository with the name 'test_name' already exists"):
        spack.cmd.repo._add_repo(
            str(tmp_path), name="test_name", scope=None, paths=[], destination=None, config=config
        )


def test_add_repo_destination_with_local_path(tmp_path: pathlib.Path):
    """Test _add_repo raises error when args are added that do not apply to local paths."""
    # Should raise error when destination is provided with local path
    with pytest.raises(
        SpackError, match="The 'destination' argument is only valid for git repositories"
    ):
        spack.cmd.repo._add_repo(
            str(tmp_path),
            name="test_name",
            scope=None,
            paths=[],
            destination="/some/destination",
            config=make_repo_config(),
        )
    with pytest.raises(SpackError, match="The --paths flag is only valid for git repositories"):
        spack.cmd.repo._add_repo(
            str(tmp_path),
            name="test_name",
            scope=None,
            paths=["path1", "path2"],
            destination=None,
            config=make_repo_config(),
        )


def test_add_repo_computed_key_already_exists(tmp_path: pathlib.Path, monkeypatch):
    """Test _add_repo raises error when computed key already exists in config."""

    def mock_parse_config_descriptor(name, entry, lock):
        return MockDescriptor({str(tmp_path): MockRepo("test_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    # Should raise error when computed key already exists
    with pytest.raises(SpackError, match="A repository with the name 'test_repo' already exists"):
        spack.cmd.repo._add_repo(
            str(tmp_path),
            name=None,  # Will use namespace as key
            scope=None,
            paths=[],
            destination=None,
            config=make_repo_config({"test_repo": "/some/path"}),
        )


def test_add_repo_git_url_with_paths(monkeypatch):
    """Test _add_repo correctly handles git URL with multiple paths."""
    config = make_repo_config({"test_repo": "/some/path"})

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify the entry has the expected git structure
        assert "git" in entry
        assert entry["git"] == "https://example.com/repo.git"
        assert entry["paths"] == ["path1", "path2"]
        return MockDescriptor({"/some/path": MockRepo("git_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    # Should succeed with git URL and multiple paths
    key = spack.cmd.repo._add_repo(
        "https://example.com/repo.git",
        name="git_test",
        scope=None,
        paths=["path1", "path2"],
        destination=None,
        config=config,
    )

    assert key == "git_test"
    repos = config.get("repos", scope=None)
    assert "git_test" in repos
    assert repos["git_test"]["git"] == "https://example.com/repo.git"
    assert repos["git_test"]["paths"] == ["path1", "path2"]


def test_add_repo_git_url_with_destination(monkeypatch):
    """Test _add_repo correctly handles git URL with destination."""
    config = make_repo_config({"test_repo": "/some/path"})

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify the entry has the expected git structure
        assert "git" in entry
        assert entry["git"] == "https://example.com/repo.git"
        assert entry["destination"] == "/custom/destination"
        return MockDescriptor({"/some/path": MockRepo("git_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    # Should succeed with git URL and destination
    key = spack.cmd.repo._add_repo(
        "https://example.com/repo.git",
        name="git_test",
        scope=None,
        paths=[],
        destination="/custom/destination",
        config=config,
    )

    assert key == "git_test"
    repos = config.get("repos", scope=None)
    assert "git_test" in repos
    assert repos["git_test"]["git"] == "https://example.com/repo.git"
    assert repos["git_test"]["destination"] == "/custom/destination"


def test_add_repo_ssh_git_url_detection(monkeypatch):
    """Test _add_repo correctly detects SSH git URLs."""
    config = make_repo_config({"test_repo": "/some/path"})

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify the entry has the expected git structure
        assert "git" in entry
        assert entry["git"] == "git@github.com:user/repo.git"
        return MockDescriptor({"/some/path": MockRepo("git_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    # Should detect SSH URL as git URL (colon not preceded by forward slash)
    key = spack.cmd.repo._add_repo(
        "git@github.com:user/repo.git",
        name="ssh_git_test",
        scope=None,
        paths=[],
        destination=None,
        config=config,
    )

    assert key == "ssh_git_test"
    repos = config.get("repos", scope=None)
    assert "ssh_git_test" in repos
    assert repos["ssh_git_test"]["git"] == "git@github.com:user/repo.git"


def test_add_repo_no_usable_repositories_error(monkeypatch):
    """Test that _add_repo raises SpackError when no usable repositories can be constructed."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        return MockDescriptor(
            {"/path1": Exception("Invalid repo"), "/path2": Exception("Another error")}
        )

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    with pytest.raises(
        SpackError, match="No package repository could be constructed from /invalid/path"
    ):
        spack.cmd.repo._add_repo(
            "/invalid/path",
            name="test_repo",
            scope=None,
            paths=[],
            destination=None,
            config=config,
        )


def test_add_repo_multiple_repos_no_name_error(monkeypatch):
    """Test that _add_repo raises SpackError when multiple repositories found without
    specifying --name."""

    def mock_parse_config_descriptor(name, entry, lock):
        return MockDescriptor({"/path1": MockRepo("repo1"), "/path2": MockRepo("repo2")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    with pytest.raises(
        SpackError, match="Multiple package repositories found, please specify a name"
    ):
        spack.cmd.repo._add_repo(
            "/path/with/multiple/repos",
            name=None,  # No name specified
            scope=None,
            paths=[],
            destination=None,
            config=make_repo_config(),
        )


def test_add_repo_git_url_basic_success(monkeypatch):
    """Test successful addition of a git repository."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify git entry structure
        assert isinstance(entry, dict)
        assert entry["git"] == "https://github.com/example/repo.git"
        return MockDescriptor({"/git/path": MockRepo("git_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    key = spack.cmd.repo._add_repo(
        "https://github.com/example/repo.git",
        name="test_git_repo",
        scope=None,
        paths=[],
        destination=None,
        config=config,
    )

    assert key == "test_git_repo"
    repos_config = config.get("repos", scope=None)
    assert "test_git_repo" in repos_config
    assert "git" in repos_config["test_git_repo"]


def test_add_repo_git_url_with_custom_destination(monkeypatch):
    """Test successful addition of a git repository with destination."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify git entry structure with destination
        assert isinstance(entry, dict)
        assert "git" in entry
        assert "destination" in entry
        assert entry["destination"] == "/custom/destination"
        return MockDescriptor({"/git/path": MockRepo("git_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    key = spack.cmd.repo._add_repo(
        "git@github.com:example/repo.git",
        name="test_git_repo",
        scope=None,
        paths=[],
        destination="/custom/destination",
        config=config,
    )

    assert key == "test_git_repo"


def test_add_repo_git_url_with_single_repo_path_new(monkeypatch):
    """Test successful addition of a git repository with repo_path."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify git entry structure with repo_path
        assert isinstance(entry, dict)
        assert "git" in entry
        assert "paths" in entry
        assert entry["paths"] == ["subdirectory/repo"]
        return MockDescriptor({"/git/path": MockRepo("git_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    key = spack.cmd.repo._add_repo(
        "https://github.com/example/repo.git",
        name="test_git_repo",
        scope=None,
        paths=["subdirectory/repo"],
        destination=None,
        config=config,
    )

    assert key == "test_git_repo"


def test_add_repo_local_path_success(monkeypatch, tmp_path):
    """Test successful addition of a local repository."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        # Verify local path entry
        assert isinstance(entry, str)
        return MockDescriptor({str(tmp_path): MockRepo("test_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    key = spack.cmd.repo._add_repo(
        str(tmp_path),
        name="test_local_repo",
        scope=None,
        paths=[],
        destination=None,
        config=config,
    )

    assert key == "test_local_repo"
    # Verify the local path was added
    repos_config = config.get("repos")
    assert "test_local_repo" in repos_config
    assert repos_config["test_local_repo"] == str(tmp_path)


def test_add_repo_auto_name_from_namespace(monkeypatch, tmp_path):
    """Test successful addition of a repository with auto-generated name from namespace."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        return MockDescriptor({str(tmp_path): MockRepo("auto_name_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    key = spack.cmd.repo._add_repo(
        str(tmp_path),
        name=None,  # No name specified, should use namespace
        scope=None,
        paths=[],
        destination=None,
        config=config,
    )

    assert key == "auto_name_repo"
    # Verify the repo was added with the namespace as key
    repos_config = config.get("repos", scope=None)
    assert "auto_name_repo" in repos_config
    assert repos_config["auto_name_repo"] == str(tmp_path)


def test_add_repo_partial_repo_construction_warning(monkeypatch, tmp_path, capsys):
    """Test that _add_repo issues warnings for repos that can't be constructed but
    succeeds if at least one can be."""

    def mock_parse_config_descriptor(name, entry, lock):
        return MockDescriptor(
            {
                "/good/path": MockRepo("good_repo"),
                "/bad/path": Exception("Failed to construct repo"),
            }
        )

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    key = spack.cmd.repo._add_repo(
        "/mixed/path",
        name="test_mixed_repo",
        scope=None,
        paths=[],
        destination=None,
        config=make_repo_config(),
    )

    assert key == "test_mixed_repo"

    # Check that a warning was issued for the failed repo
    captured = capsys.readouterr()
    assert "Skipping package repository" in captured.err


@pytest.mark.parametrize(
    "test_url,expected_type",
    [
        ("ssh://git@github.com/user/repo.git", "git"),  # ssh URL
        ("git://github.com/user/repo.git", "git"),  # git protocol
        ("user@host:repo.git", "git"),  # SSH short form
        ("file:///local/path", "git"),  # file URL
        ("/local/path", "local"),  # local path
        ("./relative/path", "local"),  # relative path
        ("C:\\Windows\\Path", "local"),  # Windows path
    ],
)
def test_add_repo_git_url_detection_edge_cases(monkeypatch, test_url, expected_type):
    """Test edge cases for git URL detection."""
    config = make_repo_config()

    def mock_parse_config_descriptor(name, entry, lock):
        return MockDescriptor({"/path": MockRepo("test_repo")})

    monkeypatch.setattr(spack.repo, "parse_config_descriptor", mock_parse_config_descriptor)

    spack.cmd.repo._add_repo(
        test_url, name=None, scope=None, paths=[], destination=None, config=config
    )

    entry = config.get("repos").get("test_repo")

    if expected_type == "git":
        assert entry == {"git": test_url}
    else:
        assert isinstance(entry, str)


def test_repo_set_git_config(mutable_config):
    """Test that 'spack repo set' properly modifies git repository configurations."""
    # Set up initial git repository config in defaults scope
    git_url = "https://github.com/example/test-repo.git"
    initial_config = {"repos": {"test-repo": {"git": git_url}}}
    spack.config.set("repos", initial_config["repos"], scope="site")

    # Test setting destination and paths
    repo("set", "--scope=user", "--destination", "/custom/path", "test-repo")
    repo("set", "--scope=user", "--path", "subdir1", "--path", "subdir2", "test-repo")

    # Check that the user config has the updated entry
    user_repos = spack.config.get("repos", scope="user")
    assert user_repos["test-repo"]["paths"] == ["subdir1", "subdir2"]
    assert user_repos["test-repo"]["destination"] == "/custom/path"

    # Check that site scope is unchanged
    site_repos = spack.config.get("repos", scope="site")
    assert "destination" not in site_repos["test-repo"]


def test_repo_set_nonexistent_repo(mutable_config):
    with pytest.raises(SpackError, match="No repository with namespace 'nonexistent'"):
        repo("set", "--destination", "/some/path", "nonexistent")


def test_repo_set_does_not_work_on_local_path(mutable_config):
    spack.config.set("repos", {"local-repo": "/local/path"}, scope="site")
    with pytest.raises(SpackError, match="is not a git repository"):
        repo("set", "--destination", "/some/path", "local-repo")

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import shutil
import sys

import pytest

from llnl.util.filesystem import mkdirp, working_dir

import spack.cmd.pkg
import spack.main
import spack.repo

#: new fake package template
pkg_template = """\
from spack.package import *

class {name}(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/test-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        pass
"""

abc = set(("pkg-a", "pkg-b", "pkg-c"))
abd = set(("pkg-a", "pkg-b", "pkg-d"))


# Force all tests to use a git repository *in* the mock packages repo.
@pytest.fixture(scope="module")
def mock_pkg_git_repo(git, tmpdir_factory):
    """Copy the builtin.mock repo and make a mutable git repo inside it."""
    tmproot = tmpdir_factory.mktemp("mock_pkg_git_repo")
    repo_path = tmproot.join("builtin.mock")

    shutil.copytree(spack.paths.mock_packages_path, str(repo_path))
    mock_repo = spack.repo.RepoPath(str(repo_path))
    mock_repo_packages = mock_repo.repos[0].packages_path

    with working_dir(mock_repo_packages):
        git("init")

        # initial commit with mock packages
        # the -f is necessary in case people ignore build-* in their ignores
        git("add", "-f", ".")
        git("config", "user.email", "testing@spack.io")
        git("config", "user.name", "Spack Testing")
        git("-c", "commit.gpgsign=false", "commit", "-m", "initial mock repo commit")

        # add commit with pkg-a, pkg-b, pkg-c packages
        mkdirp("pkg-a", "pkg-b", "pkg-c")
        with open("pkg-a/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgA"))
        with open("pkg-b/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgB"))
        with open("pkg-c/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgC"))
        git("add", "pkg-a", "pkg-b", "pkg-c")
        git("-c", "commit.gpgsign=false", "commit", "-m", "add pkg-a, pkg-b, pkg-c")

        # remove pkg-c, add pkg-d
        with open("pkg-b/package.py", "a") as f:
            f.write("\n# change pkg-b")
        git("add", "pkg-b")
        mkdirp("pkg-d")
        with open("pkg-d/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgD"))
        git("add", "pkg-d")
        git("rm", "-rf", "pkg-c")
        git("-c", "commit.gpgsign=false", "commit", "-m", "change pkg-b, remove pkg-c, add pkg-d")

    with spack.repo.use_repositories(str(repo_path)):
        yield mock_repo_packages


@pytest.fixture(scope="module")
def mock_pkg_names():
    repo = spack.repo.PATH.get_repo("builtin.mock")

    # Be sure to include virtual packages since packages with stand-alone
    # tests may inherit additional tests from the virtuals they provide,
    # such as packages that implement `mpi`.
    names = set(
        name
        for name in repo.all_package_names(include_virtuals=True)
        if not name.startswith("pkg-")
    )
    return names


def split(output):
    """Split command line output into an array."""
    output = output.strip()
    return re.split(r"\s+", output) if output else []


pkg = spack.main.SpackCommand("pkg")


def test_packages_path():
    assert spack.repo.packages_path() == spack.repo.PATH.get_repo("builtin").packages_path


def test_mock_packages_path(mock_packages):
    assert spack.repo.packages_path() == spack.repo.PATH.get_repo("builtin.mock").packages_path


def test_pkg_add(git, mock_pkg_git_repo):
    with working_dir(mock_pkg_git_repo):
        mkdirp("pkg-e")
        with open("pkg-e/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgE"))

    pkg("add", "pkg-e")

    with working_dir(mock_pkg_git_repo):
        try:
            assert "A  pkg-e/package.py" in git("status", "--short", output=str)
        finally:
            shutil.rmtree("pkg-e")
            # Removing a package mid-run disrupts Spack's caching
            if spack.repo.PATH.repos[0]._fast_package_checker:
                spack.repo.PATH.repos[0]._fast_package_checker.invalidate()

    with pytest.raises(spack.main.SpackCommandError):
        pkg("add", "does-not-exist")


@pytest.mark.skipif(sys.platform == "win32", reason="stdout format conflict")
def test_pkg_list(mock_pkg_git_repo, mock_pkg_names):
    out = split(pkg("list", "HEAD^^"))
    assert sorted(mock_pkg_names) == sorted(out)

    out = split(pkg("list", "HEAD^"))
    assert sorted(mock_pkg_names.union(["pkg-a", "pkg-b", "pkg-c"])) == sorted(out)

    out = split(pkg("list", "HEAD"))
    assert sorted(mock_pkg_names.union(["pkg-a", "pkg-b", "pkg-d"])) == sorted(out)

    # test with three dots to make sure pkg calls `git merge-base`
    out = split(pkg("list", "HEAD^^..."))
    assert sorted(mock_pkg_names) == sorted(out)


@pytest.mark.skipif(sys.platform == "win32", reason="stdout format conflict")
def test_pkg_diff(mock_pkg_git_repo, mock_pkg_names):
    out = split(pkg("diff", "HEAD^^", "HEAD^"))
    assert out == ["HEAD^:", "pkg-a", "pkg-b", "pkg-c"]

    out = split(pkg("diff", "HEAD^^", "HEAD"))
    assert out == ["HEAD:", "pkg-a", "pkg-b", "pkg-d"]

    out = split(pkg("diff", "HEAD^", "HEAD"))
    assert out == ["HEAD^:", "pkg-c", "HEAD:", "pkg-d"]


@pytest.mark.skipif(sys.platform == "win32", reason="stdout format conflict")
def test_pkg_added(mock_pkg_git_repo):
    out = split(pkg("added", "HEAD^^", "HEAD^"))
    assert ["pkg-a", "pkg-b", "pkg-c"] == out

    out = split(pkg("added", "HEAD^^", "HEAD"))
    assert ["pkg-a", "pkg-b", "pkg-d"] == out

    out = split(pkg("added", "HEAD^", "HEAD"))
    assert ["pkg-d"] == out

    out = split(pkg("added", "HEAD", "HEAD"))
    assert out == []


@pytest.mark.skipif(sys.platform == "win32", reason="stdout format conflict")
def test_pkg_removed(mock_pkg_git_repo):
    out = split(pkg("removed", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("removed", "HEAD^^", "HEAD"))
    assert out == []

    out = split(pkg("removed", "HEAD^", "HEAD"))
    assert out == ["pkg-c"]


@pytest.mark.skipif(sys.platform == "win32", reason="stdout format conflict")
def test_pkg_changed(mock_pkg_git_repo):
    out = split(pkg("changed", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("changed", "--type", "c", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("changed", "--type", "a", "HEAD^^", "HEAD^"))
    assert out == ["pkg-a", "pkg-b", "pkg-c"]

    out = split(pkg("changed", "--type", "r", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("changed", "--type", "ar", "HEAD^^", "HEAD^"))
    assert out == ["pkg-a", "pkg-b", "pkg-c"]

    out = split(pkg("changed", "--type", "arc", "HEAD^^", "HEAD^"))
    assert out == ["pkg-a", "pkg-b", "pkg-c"]

    out = split(pkg("changed", "HEAD^", "HEAD"))
    assert out == ["pkg-b"]

    out = split(pkg("changed", "--type", "c", "HEAD^", "HEAD"))
    assert out == ["pkg-b"]

    out = split(pkg("changed", "--type", "a", "HEAD^", "HEAD"))
    assert out == ["pkg-d"]

    out = split(pkg("changed", "--type", "r", "HEAD^", "HEAD"))
    assert out == ["pkg-c"]

    out = split(pkg("changed", "--type", "ar", "HEAD^", "HEAD"))
    assert out == ["pkg-c", "pkg-d"]

    out = split(pkg("changed", "--type", "arc", "HEAD^", "HEAD"))
    assert out == ["pkg-b", "pkg-c", "pkg-d"]

    # invalid type argument
    with pytest.raises(spack.main.SpackCommandError):
        pkg("changed", "--type", "foo")


def test_pkg_fails_when_not_git_repo(monkeypatch):
    monkeypatch.setattr(spack.cmd, "spack_is_git_repo", lambda: False)
    with pytest.raises(spack.main.SpackCommandError):
        pkg("added")


def test_pkg_source_requires_one_arg(mock_packages):
    with pytest.raises(spack.main.SpackCommandError):
        pkg("source", "a", "b")

    with pytest.raises(spack.main.SpackCommandError):
        pkg("source", "--canonical", "a", "b")


def test_pkg_source(mock_packages):
    fake_source = pkg("source", "fake")

    fake_file = spack.repo.PATH.filename_for_package_name("fake")
    with open(fake_file) as f:
        contents = f.read()
        assert fake_source == contents


def test_pkg_canonical_source(mock_packages):
    source = pkg("source", "multimethod")
    assert '@when("@2.0")' in source
    assert "Check that multimethods work with boolean values" in source

    canonical_1 = pkg("source", "--canonical", "multimethod@1.0")
    assert "@when" not in canonical_1
    assert "should_not_be_reached by diamond inheritance test" not in canonical_1
    assert "return 'base@1.0'" in canonical_1
    assert "return 'base@2.0'" not in canonical_1
    assert "return 'first_parent'" not in canonical_1
    assert "'should_not_be_reached by diamond inheritance test'" not in canonical_1

    canonical_2 = pkg("source", "--canonical", "multimethod@2.0")
    assert "@when" not in canonical_2
    assert "return 'base@1.0'" not in canonical_2
    assert "return 'base@2.0'" in canonical_2
    assert "return 'first_parent'" in canonical_2
    assert "'should_not_be_reached by diamond inheritance test'" not in canonical_2

    canonical_3 = pkg("source", "--canonical", "multimethod@3.0")
    assert "@when" not in canonical_3
    assert "return 'base@1.0'" not in canonical_3
    assert "return 'base@2.0'" not in canonical_3
    assert "return 'first_parent'" not in canonical_3
    assert "'should_not_be_reached by diamond inheritance test'" not in canonical_3

    canonical_4 = pkg("source", "--canonical", "multimethod@4.0")
    assert "@when" not in canonical_4
    assert "return 'base@1.0'" not in canonical_4
    assert "return 'base@2.0'" not in canonical_4
    assert "return 'first_parent'" not in canonical_4
    assert "'should_not_be_reached by diamond inheritance test'" in canonical_4


def test_pkg_hash(mock_packages):
    output = pkg("hash", "a", "b").strip().split()
    assert len(output) == 2 and all(len(elt) == 32 for elt in output)

    output = pkg("hash", "multimethod").strip().split()
    assert len(output) == 1 and all(len(elt) == 32 for elt in output)


@pytest.mark.skipif(not spack.cmd.pkg.get_grep(), reason="grep is not installed")
def test_pkg_grep(mock_packages, capfd):
    # only splice-* mock packages have the string "splice" in them
    pkg("grep", "-l", "splice", output=str)
    output, _ = capfd.readouterr()
    assert output.strip() == "\n".join(
        spack.repo.PATH.get_pkg_class(name).module.__file__
        for name in ["splice-a", "splice-h", "splice-t", "splice-vh", "splice-z"]
    )

    # ensure that this string isn't fouhnd
    pkg("grep", "abcdefghijklmnopqrstuvwxyz", output=str, fail_on_error=False)
    assert pkg.returncode == 1
    output, _ = capfd.readouterr()
    assert output.strip() == ""

    # ensure that we return > 1 for an error
    pkg("grep", "--foobarbaz-not-an-option", output=str, fail_on_error=False)
    assert pkg.returncode == 2

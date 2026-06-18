# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import io
import os
import pathlib
import shutil
import sys

import pytest

import spack.cmd.style
import spack.main
import spack.paths
import spack.repo
from spack.cmd.style import _run_import_check, changed_files
from spack.llnl.util.filesystem import FileFilter, working_dir
from spack.util.executable import which

#: directory with sample style files
style_data = os.path.join(spack.paths.test_path, "data", "style")


style = spack.main.SpackCommand("style")

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="CI uses cross drive paths that raise errors with relpath"
)

RUFF = which("ruff")
MYPY = which("mypy")


@pytest.fixture(autouse=True)
def has_develop_branch(git):
    """spack style requires git and a develop branch to run -- skip if we're missing either."""
    git("show-ref", "--verify", "--quiet", "refs/heads/develop", fail_on_error=False)
    if git.returncode != 0:
        pytest.skip("requires git and a develop branch")


@pytest.fixture(scope="function")
def ruff_package(tmp_path: pathlib.Path):
    """Style only checks files that have been modified. This fixture makes a small
    change to the ``ruff`` mock package, yields the filename, then undoes the
    change on cleanup.
    """
    repo = spack.repo.from_path(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("ruff")
    rel_path = os.path.dirname(os.path.relpath(filename, spack.paths.prefix))
    tmp = tmp_path / rel_path / "ruff-ci-package.py"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.touch()
    tmp = str(tmp)

    shutil.copy(filename, tmp)
    package = FileFilter(tmp)
    package.filter("state = 'unmodified'", "state = 'modified'", string=True)
    yield tmp


@pytest.fixture
def ruff_package_with_errors(scope="function"):
    """A ruff package with errors."""
    repo = spack.repo.from_path(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("ruff")
    tmp = filename + ".tmp"

    shutil.copy(filename, tmp)
    package = FileFilter(tmp)

    # this is a ruff error (quote style and spacing before/after operator)
    package.filter('state = "unmodified"', "state    =    'modified'", string=True)

    # this is two ruff errors (unused import) (orderign)
    package.filter(
        "from spack.package import *", "from spack.package import *\nimport os", string=True
    )
    yield tmp


def test_changed_files_from_git_rev_base(git, tmp_path: pathlib.Path):
    """Test arbitrary git ref as base."""
    with working_dir(str(tmp_path)):
        git("init")
        git("checkout", "-b", "main")
        git("config", "user.name", "test user")
        git("config", "user.email", "test@user.com")
        git("commit", "--no-gpg-sign", "--allow-empty", "-m", "initial commit")

        (tmp_path / "bin").mkdir(parents=True, exist_ok=True)
        (tmp_path / "bin" / "spack").touch()
        assert changed_files(base="HEAD") == [pathlib.Path("bin/spack")]
        assert changed_files(base="main") == [pathlib.Path("bin/spack")]

        git("add", "bin/spack")
        git("commit", "--no-gpg-sign", "-m", "v1")
        assert changed_files(base="HEAD") == []
        assert changed_files(base="HEAD~") == [pathlib.Path("bin/spack")]


def test_changed_no_base(git, tmp_path: pathlib.Path, capfd):
    """Ensure that we fail gracefully with no base branch."""
    (tmp_path / "bin").mkdir(parents=True, exist_ok=True)
    (tmp_path / "bin" / "spack").touch()
    with working_dir(str(tmp_path)):
        git("init")
        git("config", "user.name", "test user")
        git("config", "user.email", "test@user.com")
        git("add", ".")
        git("commit", "--no-gpg-sign", "-m", "initial commit")

        with pytest.raises(SystemExit):
            changed_files(base="foobar")

        out, err = capfd.readouterr()
        assert "This repository does not have a 'foobar'" in err


def test_changed_files_all_files(mock_packages):
    # it's hard to guarantee "all files", so do some sanity checks.
    files = {
        os.path.join(spack.paths.prefix, os.path.normpath(path))
        for path in changed_files(all_files=True)
    }

    # spack has a lot of files -- check that we're in the right ballpark
    assert len(files) > 500

    # a builtin package
    zlib = spack.repo.PATH.get_pkg_class("zlib")
    zlib_file = zlib.module.__file__
    if zlib_file.endswith("pyc"):
        zlib_file = zlib_file[:-1]
    assert zlib_file in files

    # a core spack file
    assert os.path.join(spack.paths.module_path, "spec.py") in files

    # a mock package
    repo = spack.repo.from_path(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("ruff")
    assert filename in files

    # this test
    assert __file__ in files

    # ensure externals are excluded
    assert not any(f.startswith(spack.paths.vendor_path) for f in files)


def test_bad_root(tmp_path: pathlib.Path):
    """Ensure that `spack style` doesn't run on non-spack directories."""
    output = style("--root", str(tmp_path), fail_on_error=False)
    assert "This does not look like a valid spack root" in output
    assert style.returncode == 1


@pytest.fixture
def external_style_root(git, ruff_package_with_errors, tmp_path: pathlib.Path):
    """Create a mock repository for running spack style."""
    # create a sort-of spack-looking directory
    script = tmp_path / "bin" / "spack"
    script.parent.mkdir(parents=True, exist_ok=True)
    script.touch()
    spack_dir = tmp_path / "lib" / "spack" / "spack"
    spack_dir.mkdir(parents=True, exist_ok=True)
    (spack_dir / "__init__.py").touch()
    llnl_dir = tmp_path / "lib" / "spack" / "llnl"
    llnl_dir.mkdir(parents=True, exist_ok=True)
    (llnl_dir / "__init__.py").touch()

    # create a base develop branch
    with working_dir(str(tmp_path)):
        git("init")
        git("config", "user.name", "test user")
        git("config", "user.email", "test@user.com")
        git("add", ".")
        git("commit", "--no-gpg-sign", "-m", "initial commit")
        git("branch", "-m", "develop")
        git("checkout", "-b", "feature")

    # copy the buggy package in
    py_file = spack_dir / "dummy.py"
    py_file.touch()
    shutil.copy(ruff_package_with_errors, str(py_file))

    yield tmp_path, py_file


@pytest.mark.skipif(not RUFF, reason="ruff is not installed.")
def test_fix_style(external_style_root):
    """Make sure spack style --fix works."""
    tmp_path, py_file = external_style_root

    broken_dummy = os.path.join(style_data, "broken.dummy")
    broken_py = str(tmp_path / "lib" / "spack" / "spack" / "broken.py")
    fixed_py = os.path.join(style_data, "fixed.py")

    shutil.copy(broken_dummy, broken_py)
    assert not filecmp.cmp(broken_py, fixed_py)

    # dummy.py is in the same directory and will raise errors unrelated to this
    # check, don't fail on those errors, just check to make sure
    # we fixed the intended file correctly
    # Note: can't just specify the correct file due to cross drive issues on Windows
    style(
        "--root", str(tmp_path), "--tool", "ruff-check,ruff-format", "--fix", fail_on_error=False
    )
    assert filecmp.cmp(broken_py, fixed_py)


@pytest.mark.skipif(not RUFF, reason="ruff is not installed.")
@pytest.mark.skipif(not MYPY, reason="mypy is not installed.")
def test_external_root(external_style_root):
    """Ensure we can run in a separate root directory w/o configuration files."""
    tmp_path, py_file = external_style_root

    # make sure tools are finding issues with external root,
    # not the real one.
    output = style("--root-relative", "--root", str(tmp_path), fail_on_error=False)

    # make sure it failed
    assert style.returncode == 1

    # ruff-check error
    assert "Import block is un-sorted or un-formatted\n --> lib/spack/spack/dummy.py" in output

    # mypy error
    assert 'lib/spack/spack/dummy.py:45: error: Name "version" is not defined' in output

    # ruff-format error
    assert "--- lib/spack/spack/dummy.py" in output
    assert "+++ lib/spack/spack/dummy.py" in output

    # ruff-check error
    assert "`os` imported but unused\n --> lib/spack/spack/dummy.py" in output


@pytest.mark.skipif(not RUFF, reason="ruff is not installed.")
def test_style(ruff_package, tmp_path: pathlib.Path):
    root_relative = os.path.relpath(ruff_package, spack.paths.prefix)

    # use a working directory to test cwd-relative paths, as tests run in
    # the spack prefix by default
    with working_dir(str(tmp_path)):
        relative = os.path.relpath(ruff_package)

        # one specific arg
        output = style("--tool", "ruff-check", ruff_package, fail_on_error=False)
        assert relative in output
        assert "spack style checks were clean" in output

        # specific file that isn't changed
        output = style("--tool", "ruff-check", __file__, fail_on_error=False)
        assert relative not in output
        assert __file__ in output
        assert "spack style checks were clean" in output

    # root-relative paths
    output = style("--tool", "ruff-check", "--root-relative", ruff_package)
    assert root_relative in output
    assert "spack style checks were clean" in output


@pytest.mark.skipif(not RUFF, reason="ruff is not installed.")
def test_style_with_errors(ruff_package_with_errors):
    root_relative = os.path.relpath(ruff_package_with_errors, spack.paths.prefix)
    output = style(
        "--tool", "ruff-check", "--root-relative", ruff_package_with_errors, fail_on_error=False
    )
    assert root_relative in output
    assert style.returncode == 1
    assert "spack style found errors" in output


@pytest.mark.skipif(not RUFF, reason="ruff is not installed.")
def test_style_with_ruff_format(ruff_package_with_errors):
    output = style("--tool", "ruff-format", ruff_package_with_errors, fail_on_error=False)
    assert "ruff-format found errors" in output
    assert style.returncode == 1
    assert "spack style found errors" in output


def test_skip_tools():
    output = style("--skip", "import,ruff-check,ruff-format,mypy")
    assert "Nothing to run" in output


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires Python 3.9+")
def test_run_import_check(tmp_path: pathlib.Path):
    file = tmp_path / "issues.py"
    contents = '''
import spack.cmd
import spack.config  # do not drop this import because of this comment
import spack.repo
import spack.repo_utils

from spack_repo.builtin_mock.build_systems import autotools

# this comment about spack.error should not be removed
class Example(autotools.AutotoolsPackage):
    """this is a docstring referencing unused spack.error.SpackError, which is fine"""
    pass

def foo(config: "spack.error.SpackError"):
    # the type hint is quoted, so it should not be removed
    spack.util.executable.Executable("example")
    print(spack.__version__)
    print(spack.repo_utils.__file__)

import spack.enums
from spack.enums import ConfigScopePriority

import spack.util.url as url_util
def something(y: spack.util.url.Url): ...
'''
    file.write_text(contents)
    root = str(tmp_path)
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [file],
        fix=False,
        out=output_buf,
        root_relative=False,
        root=pathlib.Path(spack.paths.prefix),
        working_dir=pathlib.Path(root),
    )
    output = output_buf.getvalue()

    assert "issues.py: redundant import: spack.cmd" in output
    assert "issues.py: redundant import: spack.repo" in output
    assert "issues.py: redundant import: spack.config" not in output  # comment prevents removal
    assert "issues.py: redundant import: spack.enums" in output  # imported via from-import
    assert "issues.py: missing import: spack" in output  # used by spack.__version__
    assert "issues.py: missing import: spack.util.executable" in output
    assert "issues.py: missing import: spack.util.url" in output  # used in type hint
    assert "issues.py: missing import: spack.error" not in output  # not directly used
    assert exit_code == 1
    assert file.read_text() == contents  # fix=False should not change the file

    # run it with --fix, should have the same output.
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [file],
        fix=True,
        out=output_buf,
        root_relative=False,
        root=pathlib.Path(spack.paths.prefix),
        working_dir=pathlib.Path(root),
    )
    output = output_buf.getvalue()
    assert exit_code == 1
    assert "issues.py: redundant import: spack.cmd" in output
    assert "issues.py: redundant import: spack.enums" in output
    assert "issues.py: missing import: spack" in output
    assert "issues.py: missing import: spack.util.executable" in output
    assert "issues.py: missing import: spack.util.url" in output

    # after fix a second fix is idempotent
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [file],
        fix=True,
        out=output_buf,
        root_relative=False,
        root=pathlib.Path(spack.paths.prefix),
        working_dir=pathlib.Path(root),
    )
    output = output_buf.getvalue()
    assert exit_code == 0
    assert not output

    # check that the file was fixed
    new_contents = file.read_text()
    assert "import spack.cmd" not in new_contents
    assert "import spack.enums" not in new_contents
    assert "import spack\n" in new_contents
    assert "import spack.util.executable\n" in new_contents
    assert "import spack.util.url\n" in new_contents


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires Python 3.9+")
def test_run_import_check_syntax_error_and_missing(tmp_path: pathlib.Path):
    (tmp_path / "syntax-error.py").write_text("""this 'is n(ot python code""")
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [tmp_path / "syntax-error.py", tmp_path / "missing.py"],
        fix=False,
        out=output_buf,
        root_relative=True,
        root=tmp_path,
        working_dir=tmp_path / "does-not-matter",
    )
    output = output_buf.getvalue()
    assert "syntax-error.py: could not parse" in output
    assert "missing.py: could not parse" in output
    assert exit_code == 1


def test_case_sensitive_imports(tmp_path: pathlib.Path):
    # example.Example is a name, while example.example is a module.
    (tmp_path / "lib" / "spack" / "example").mkdir(parents=True)
    (tmp_path / "lib" / "spack" / "example" / "__init__.py").write_text("class Example:\n    pass")
    (tmp_path / "lib" / "spack" / "example" / "example.py").write_text("foo = 1")
    assert spack.cmd.style._module_part(tmp_path, "example.Example") == "example"


def test_pkg_imports():
    assert (
        spack.cmd.style._module_part(pathlib.Path(spack.paths.prefix), "spack.pkg.builtin.boost")
        is None
    )
    assert spack.cmd.style._module_part(pathlib.Path(spack.paths.prefix), "spack.pkg") is None

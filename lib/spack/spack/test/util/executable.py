# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import sys
from typing import List

import pytest

import llnl.util.filesystem as fs

import spack
import spack.main
import spack.util.executable as ex
from spack.hooks.sbang import filter_shebangs_in_directory


def test_read_unicode(tmp_path: pathlib.Path, working_env):
    with fs.working_dir(str(tmp_path)):
        script_name = "print_unicode.py"
        script_args: List[str] = []
        # read the unicode back in and see whether things work
        if sys.platform == "win32":
            script = ex.Executable("%s" % (sys.executable))
            script_args.append(script_name)
        else:
            script = ex.Executable("./%s" % script_name)

        os.environ["LD_LIBRARY_PATH"] = spack.main.spack_ld_library_path
        # make a script that prints some unicode
        with open(script_name, "w", encoding="utf-8") as f:
            f.write(
                """#!{0}
print(u'\\xc3')
""".format(
                    sys.executable
                )
            )

        # make it executable
        fs.set_executable(script_name)
        filter_shebangs_in_directory(".", [script_name])

        assert "\xc3" == script(*script_args, output=str).strip()


def test_which_relative_path_with_slash(tmp_path: pathlib.Path, working_env):
    (tmp_path / "exe").touch()
    path = str(tmp_path / "exe")

    os.environ["PATH"] = ""

    with fs.working_dir(str(tmp_path)):
        no_exe = ex.which(".{0}exe".format(os.path.sep))
        assert no_exe is None
        if sys.platform == "win32":
            # These checks are for 'executable' files, Windows
            # determines this by file extension.
            path += ".exe"
            (tmp_path / "exe.exe").touch()
        else:
            fs.set_executable(path)

        exe = ex.which(".{0}exe".format(os.path.sep), required=True)
        assert exe.path == path


def test_which_with_slash_ignores_path(tmp_path: pathlib.Path, working_env):
    (tmp_path / "exe").touch()
    (tmp_path / "bin").mkdir()
    (tmp_path / "bin" / "exe").touch()

    path = str(tmp_path / "exe")
    wrong_path = str(tmp_path / "bin" / "exe")
    os.environ["PATH"] = str(tmp_path / "bin")

    with fs.working_dir(str(tmp_path)):
        if sys.platform == "win32":
            # For Windows, need to create files with .exe after any assert is none tests
            (tmp_path / "exe.exe").touch()
            (tmp_path / "bin" / "exe.exe").touch()
            path = path + ".exe"
            wrong_path = wrong_path + ".exe"
        else:
            fs.set_executable(path)
            fs.set_executable(wrong_path)

        exe = ex.which(".{0}exe".format(os.path.sep), required=True)
        assert exe.path == path


def test_which(tmp_path: pathlib.Path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    assert ex.which("spack-test-exe") is None

    with pytest.raises(ex.CommandNotFoundError):
        ex.which("spack-test-exe", required=True)

    path = str(tmp_path / "spack-test-exe")

    with fs.working_dir(str(tmp_path)):
        if sys.platform == "win32":
            # For Windows, need to create files with .exe after any assert is none tests
            (tmp_path / "spack-test-exe.exe").touch()
            path += ".exe"
        else:
            fs.touch("spack-test-exe")
            fs.set_executable("spack-test-exe")

        exe = ex.which("spack-test-exe")
        assert exe is not None
        assert exe.path == path


@pytest.fixture
def make_script_exe(tmp_path: pathlib.Path):
    if sys.platform == "win32":
        pytest.skip("Can't test #!/bin/sh scripts on Windows.")

    def make_script(name, contents):
        script = tmp_path / f"{name}.sh"
        with script.open("w", encoding="utf-8") as f:
            f.write("#!/bin/sh\n")
            f.write(contents)
            f.write("\n")
        fs.set_executable(str(script))

        return ex.Executable(str(script))

    return make_script


def test_exe_fail(make_script_exe):
    fail = make_script_exe("fail", "exit 107")
    with pytest.raises(ex.ProcessError):
        fail()
    assert fail.returncode == 107


def test_exe_success(make_script_exe):
    succeed = make_script_exe("fail", "exit 0")
    succeed()
    assert succeed.returncode == 0


def test_exe_timeout(make_script_exe):
    timeout = make_script_exe("timeout", "sleep 100")
    with pytest.raises(ex.ProcessError):
        timeout(timeout=1)
    assert timeout.returncode == 1


def test_exe_not_exist(tmp_path: pathlib.Path):
    fail = ex.Executable(str(tmp_path / "foo"))  # doesn't exist
    with pytest.raises(ex.ProcessError):
        fail()
    assert fail.returncode == 1


def test_construct_from_pathlib(mock_executable):
    """Tests that we can construct an executable from a pathlib.Path object"""
    expected = "Hello world!"
    path = mock_executable("hello", output=f"echo {expected}\n")
    hello = ex.Executable(path)
    assert expected in hello(output=str)

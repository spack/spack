# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from pathlib import PurePath

import pytest

import llnl.util.filesystem as fs

import spack
import spack.main
import spack.util.executable as ex
from spack.hooks.sbang import filter_shebangs_in_directory


def test_read_unicode(tmpdir, working_env):
    with tmpdir.as_cwd():
        script_name = "print_unicode.py"
        # read the unicode back in and see whether things work
        if sys.platform == "win32":
            script = ex.Executable("%s" % (sys.executable))
            script_args = [script_name]
        else:
            script = ex.Executable("./%s" % script_name)
            script_args = []

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


def test_which_relative_path_with_slash(tmpdir, working_env):
    tmpdir.ensure("exe")
    path = str(tmpdir.join("exe"))

    os.environ["PATH"] = ""

    with tmpdir.as_cwd():
        no_exe = ex.which(".{0}exe".format(os.path.sep))
        assert no_exe is None
        if sys.platform == "win32":
            # These checks are for 'executable' files, Windows
            # determines this by file extension.
            path += ".exe"
            tmpdir.ensure("exe.exe")
        else:
            fs.set_executable(path)

        exe = ex.which(".{0}exe".format(os.path.sep))
        assert exe.path == path


def test_which_with_slash_ignores_path(tmpdir, working_env):
    tmpdir.ensure("exe")
    tmpdir.ensure("bin{0}exe".format(os.path.sep))

    path = str(tmpdir.join("exe"))
    wrong_path = str(tmpdir.join("bin", "exe"))
    os.environ["PATH"] = str(PurePath(wrong_path).parent)

    with tmpdir.as_cwd():
        if sys.platform == "win32":
            # For Windows, need to create files with .exe after any assert is none tests
            tmpdir.ensure("exe.exe")
            tmpdir.ensure("bin{0}exe.exe".format(os.path.sep))
            path = path + ".exe"
            wrong_path = wrong_path + ".exe"
        else:
            fs.set_executable(path)
            fs.set_executable(wrong_path)

        exe = ex.which(".{0}exe".format(os.path.sep))
        assert exe.path == path


def test_which(tmpdir, monkeypatch):
    monkeypatch.setenv("PATH", str(tmpdir))
    assert ex.which("spack-test-exe") is None

    with pytest.raises(ex.CommandNotFoundError):
        ex.which("spack-test-exe", required=True)

    path = str(tmpdir.join("spack-test-exe"))

    with tmpdir.as_cwd():
        if sys.platform == "win32":
            # For Windows, need to create files with .exe after any assert is none tests
            tmpdir.ensure("spack-test-exe.exe")
            path += ".exe"
        else:
            fs.touch("spack-test-exe")
            fs.set_executable("spack-test-exe")

        exe = ex.which("spack-test-exe")
        assert exe is not None
        assert exe.path == path


@pytest.fixture
def make_script_exe(tmpdir):
    if sys.platform == "win32":
        pytest.skip("Can't test #!/bin/sh scripts on Windows.")

    def make_script(name, contents):
        script = tmpdir / f"{name}.sh"
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


def test_exe_not_exist(tmpdir):
    fail = ex.Executable(str(tmpdir.join("foo")))  # doesn't exist
    with pytest.raises(ex.ProcessError):
        fail()
    assert fail.returncode == 1


def test_construct_from_pathlib(mock_executable):
    """Tests that we can construct an executable from a pathlib.Path object"""
    expected = "Hello world!"
    path = mock_executable("hello", output=f"echo {expected}\n")
    hello = ex.Executable(path)
    assert expected in hello(output=str)

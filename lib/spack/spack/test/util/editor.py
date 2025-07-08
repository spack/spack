# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from llnl.util.filesystem import set_executable

import spack.util.editor as ed

pytestmark = [
    pytest.mark.usefixtures("working_env"),
    pytest.mark.not_on_windows("editor not implemented on windows"),
]


# env vars that control the editor
EDITOR_VARS = ["SPACK_EDITOR", "VISUAL", "EDITOR"]


@pytest.fixture(scope="module", autouse=True)
def clean_env_vars():
    """Unset all editor env vars before tests."""
    for var in EDITOR_VARS:
        if var in os.environ:
            del os.environ[var]


@pytest.fixture(autouse=True)
def working_editor_test_env(working_env):
    """Don't leak environent variables between functions here."""


# parameterized fixture for editor var names
@pytest.fixture(params=EDITOR_VARS)
def editor_var(request):
    return request.param


def _make_exe(tmp_path_factory: pytest.TempPathFactory, name, contents=None):
    if sys.platform == "win32":
        name += ".exe"
    exe_dir = tmp_path_factory.mktemp(f"{name}_exe")
    path = exe_dir / name
    if contents is not None:
        path.write_text(f"#!/bin/sh\n{contents}\n", encoding="utf-8")
        set_executable(str(path))
    return str(path)


@pytest.fixture(scope="session")
def good_exe(tmp_path_factory: pytest.TempPathFactory):
    return _make_exe(tmp_path_factory, "good", "exit 0")


@pytest.fixture(scope="session")
def bad_exe(tmp_path_factory: pytest.TempPathFactory):
    return _make_exe(tmp_path_factory, "bad", "exit 1")


@pytest.fixture(scope="session")
def nosuch_exe(tmp_path_factory: pytest.TempPathFactory):
    return _make_exe(tmp_path_factory, "nosuch")


@pytest.fixture(scope="session")
def vim_exe(tmp_path_factory: pytest.TempPathFactory):
    return _make_exe(tmp_path_factory, "vim", "exit 0")


@pytest.fixture(scope="session")
def gvim_exe(tmp_path_factory: pytest.TempPathFactory):
    return _make_exe(tmp_path_factory, "gvim", "exit 0")


def test_find_exe_from_env_var(good_exe):
    os.environ["EDITOR"] = good_exe
    assert ed._find_exe_from_env_var("EDITOR") == (good_exe, [good_exe])


def test_find_exe_from_env_var_with_args(good_exe):
    os.environ["EDITOR"] = good_exe + " a b c"
    assert ed._find_exe_from_env_var("EDITOR") == (good_exe, [good_exe, "a", "b", "c"])


def test_find_exe_from_env_var_bad_path(nosuch_exe):
    os.environ["EDITOR"] = nosuch_exe
    assert ed._find_exe_from_env_var("FOO") == (None, [])


def test_editor_gvim_special_case(gvim_exe):
    os.environ["EDITOR"] = gvim_exe

    def assert_exec(exe, args):
        assert exe == gvim_exe
        assert args == [gvim_exe, "-f", "/path/to/file"]
        return 0

    assert ed.editor("/path/to/file", exec_fn=assert_exec)

    os.environ["EDITOR"] = gvim_exe + " -f"
    assert ed.editor("/path/to/file", exec_fn=assert_exec)


def test_editor_precedence(good_exe, gvim_exe, vim_exe, bad_exe):
    """Ensure we prefer editor variables in order of precedence."""
    os.environ["SPACK_EDITOR"] = good_exe
    os.environ["VISUAL"] = gvim_exe
    os.environ["EDITOR"] = vim_exe
    correct_exe = good_exe

    def assert_callback(exe, args):
        result = ed.executable(exe, args)
        if result == 0:
            assert exe == correct_exe
        return result

    ed.editor(exec_fn=assert_callback)

    os.environ["SPACK_EDITOR"] = bad_exe
    correct_exe = gvim_exe
    ed.editor(exec_fn=assert_callback)

    os.environ["VISUAL"] = bad_exe
    correct_exe = vim_exe
    ed.editor(exec_fn=assert_callback)


def test_find_exe_from_env_var_no_editor():
    if "FOO" in os.environ:
        os.environ.unset("FOO")
    assert ed._find_exe_from_env_var("FOO") == (None, [])


def test_editor(editor_var, good_exe):
    os.environ[editor_var] = good_exe

    def assert_exec(exe, args):
        assert exe == good_exe
        assert args == [good_exe, "/path/to/file"]
        return 0

    ed.editor("/path/to/file", exec_fn=assert_exec)


def test_editor_visual_bad(good_exe, bad_exe):
    os.environ["VISUAL"] = bad_exe
    os.environ["EDITOR"] = good_exe

    def assert_exec(exe, args):
        if exe == bad_exe:
            raise OSError()

        assert exe == good_exe
        assert args == [good_exe, "/path/to/file"]
        return 0

    ed.editor("/path/to/file", exec_fn=assert_exec)


def test_editor_no_visual(good_exe):
    os.environ["EDITOR"] = good_exe

    def assert_exec(exe, args):
        assert exe == good_exe
        assert args == [good_exe, "/path/to/file"]
        return 0

    ed.editor("/path/to/file", exec_fn=assert_exec)


def test_editor_no_visual_with_args(good_exe):
    # editor has extra args in the var (e.g., emacs -nw)
    os.environ["EDITOR"] = good_exe + " -nw --foo"

    def assert_exec(exe, args):
        assert exe == good_exe
        assert args == [good_exe, "-nw", "--foo", "/path/to/file"]
        return 0

    ed.editor("/path/to/file", exec_fn=assert_exec)


def test_editor_both_bad(nosuch_exe, vim_exe):
    os.environ["VISUAL"] = nosuch_exe
    os.environ["EDITOR"] = nosuch_exe

    os.environ["PATH"] = "%s%s%s" % (os.path.dirname(vim_exe), os.pathsep, os.environ["PATH"])

    def assert_exec(exe, args):
        assert exe == vim_exe
        assert args == [vim_exe, "/path/to/file"]
        return 0

    ed.editor("/path/to/file", exec_fn=assert_exec)


def test_no_editor():
    os.environ["PATH"] = ""

    def assert_exec(exe, args):
        assert False

    with pytest.raises(OSError, match=r"No text editor found.*"):
        ed.editor("/path/to/file", exec_fn=assert_exec)

    def assert_exec(exe, args):
        return False

    with pytest.raises(OSError, match=r"No text editor found.*"):
        ed.editor("/path/to/file", exec_fn=assert_exec)


def test_exec_fn_executable(editor_var, good_exe, bad_exe):
    """Make sure editor() works with ``ed.executable`` as well as execv"""
    os.environ[editor_var] = good_exe
    assert ed.editor(exec_fn=ed.executable)

    os.environ[editor_var] = bad_exe
    with pytest.raises(OSError, match=r"No text editor found.*"):
        ed.editor(exec_fn=ed.executable)

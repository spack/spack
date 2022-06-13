# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from llnl.util.filesystem import set_executable

import spack.util.editor as ed

pytestmark = [pytest.mark.usefixtures('working_env'),
              pytest.mark.skipif(sys.platform == 'win32',
                                 reason="editor not implemented on windows")]


def _make_exe(tmpdir_factory, name, contents=None):
    if sys.platform == "win32":
        name += '.exe'
    path = str(tmpdir_factory.mktemp('%s_exe' % name).join(name))
    if contents is not None:
        with open(path, 'w') as f:
            f.write('#!/bin/sh\n%s\n' % contents)
        set_executable(path)
    return path


@pytest.fixture(scope='session')
def good_exe(tmpdir_factory):
    return _make_exe(tmpdir_factory, 'good', 'exit 0')


@pytest.fixture(scope='session')
def bad_exe(tmpdir_factory):
    return _make_exe(tmpdir_factory, 'bad', 'exit 1')


@pytest.fixture(scope='session')
def nosuch_exe(tmpdir_factory):
    return _make_exe(tmpdir_factory, 'nosuch')


@pytest.fixture(scope='session')
def vim_exe(tmpdir_factory):
    return _make_exe(tmpdir_factory, 'vim', 'exit 0')


def test_find_exe_from_env_var(good_exe):
    os.environ['EDITOR'] = good_exe
    assert ed._find_exe_from_env_var('EDITOR') == (good_exe, [good_exe])


def test_find_exe_from_env_var_with_args(good_exe):
    os.environ['EDITOR'] = good_exe + ' a b c'
    assert ed._find_exe_from_env_var('EDITOR') == (
        good_exe, [good_exe, 'a', 'b', 'c'])


def test_find_exe_from_env_var_bad_path(nosuch_exe):
    os.environ['EDITOR'] = nosuch_exe
    assert ed._find_exe_from_env_var('FOO') == (None, [])


def test_find_exe_from_env_var_no_editor():
    if 'FOO' in os.environ:
        os.environ.unset('FOO')
    assert ed._find_exe_from_env_var('FOO') == (None, [])


def test_editor_visual(good_exe):
    os.environ['VISUAL'] = good_exe

    def assert_exec(exe, args):
        assert exe == good_exe
        assert args == [good_exe, '/path/to/file']

    ed.editor('/path/to/file', _exec_func=assert_exec)


def test_editor_visual_bad(good_exe, bad_exe):
    os.environ['VISUAL'] = bad_exe
    os.environ['EDITOR'] = good_exe

    def assert_exec(exe, args):
        if exe == bad_exe:
            raise OSError()

        assert exe == good_exe
        assert args == [good_exe, '/path/to/file']

    ed.editor('/path/to/file', _exec_func=assert_exec)


def test_editor_no_visual(good_exe):
    if 'VISUAL' in os.environ:
        del os.environ['VISUAL']
    os.environ['EDITOR'] = good_exe

    def assert_exec(exe, args):
        assert exe == good_exe
        assert args == [good_exe, '/path/to/file']

    ed.editor('/path/to/file', _exec_func=assert_exec)


def test_editor_no_visual_with_args(good_exe):
    if 'VISUAL' in os.environ:
        del os.environ['VISUAL']

    # editor has extra args in the var (e.g., emacs -nw)
    os.environ['EDITOR'] = good_exe + ' -nw --foo'

    def assert_exec(exe, args):
        assert exe == good_exe
        assert args == [good_exe, '-nw', '--foo', '/path/to/file']

    ed.editor('/path/to/file', _exec_func=assert_exec)


def test_editor_both_bad(nosuch_exe, vim_exe):
    os.environ['VISUAL'] = nosuch_exe
    os.environ['EDITOR'] = nosuch_exe

    os.environ['PATH'] = '%s%s%s' % (
        os.path.dirname(vim_exe), os.pathsep, os.environ['PATH'])

    def assert_exec(exe, args):
        assert exe == vim_exe
        assert args == [vim_exe, '/path/to/file']

    ed.editor('/path/to/file', _exec_func=assert_exec)

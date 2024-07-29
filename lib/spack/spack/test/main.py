# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.filesystem as fs

import spack.paths
import spack.util.executable as exe
import spack.util.git
from spack.main import get_version, main

git_exe_name = "git.bat" if sys.platform == "win32" else "git"
script_head = "@echo off" if sys.platform == "win32" else "#!/bin/sh"


def make_git_script(tmpdir, content, monkeypatch):
    git = str(tmpdir.join(git_exe_name))
    with open(git, "w") as f:
        f.write(
            f"""{script_head}
{content}
"""
        )
    fs.set_executable(git)
    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))


def test_version_git_nonsense_output(tmpdir, working_env, monkeypatch):
    content = "echo --|not a hash|----"
    make_git_script(tmpdir, content, monkeypatch)
    assert spack.spack_version == get_version()


def test_version_git_fails(tmpdir, working_env, monkeypatch):
    content = """
echo 26552533be04e83e66be2c28e0eb5011cb54e8fa
exit 1
"""
    make_git_script(tmpdir, content, monkeypatch)
    assert spack.spack_version == get_version()


def test_git_sha_output(tmpdir, working_env, monkeypatch):
    sha = "26552533be04e83e66be2c28e0eb5011cb54e8fa"
    content = "echo " + sha
    make_git_script(tmpdir, content, monkeypatch)
    expected = f"{spack.spack_version} ({sha})"
    assert expected == get_version()


def test_get_version_no_repo(tmpdir, monkeypatch):
    monkeypatch.setattr(spack.paths, "prefix", str(tmpdir))
    assert spack.spack_version == get_version()


def test_get_version_no_git(tmpdir, working_env, monkeypatch):
    monkeypatch.setattr(spack.util.git, "git", lambda: None)
    assert spack.spack_version == get_version()


def test_main_calls_get_version(tmpdir, capsys, working_env, monkeypatch):
    # act like git is not found in the PATH
    monkeypatch.setattr(spack.util.git, "git", lambda: None)

    # make sure we get a bare version (without commit) when this happens
    main(["-V"])
    out, err = capsys.readouterr()
    assert spack.spack_version == out.strip()


def test_get_version_bad_git(tmpdir, working_env, monkeypatch):
    content = "exit 1"
    make_git_script(tmpdir, content, monkeypatch)
    assert spack.spack_version == get_version()

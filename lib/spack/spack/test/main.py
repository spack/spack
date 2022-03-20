# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import llnl.util.filesystem as fs

import spack.paths
from spack.main import get_version, main

pytestmark = pytest.mark.skipif(
    sys.platform == 'win32',
    reason="Test functionality supported but tests are failing on Win")


def test_version_git_nonsense_output(tmpdir, working_env):
    git = str(tmpdir.join("git"))
    with open(git, "w") as f:
        f.write("""#!/bin/sh
echo --|not a hash|----
""")
    fs.set_executable(git)

    os.environ["PATH"] = str(tmpdir)
    assert spack.spack_version == get_version()


def test_git_sha_output(tmpdir, working_env):
    git = str(tmpdir.join("git"))
    sha = '26552533be04e83e66be2c28e0eb5011cb54e8fa'
    with open(git, "w") as f:
        f.write("""#!/bin/sh
echo {0}
""".format(sha))
    fs.set_executable(git)

    os.environ["PATH"] = str(tmpdir)
    expected = "{0} ({1})".format(spack.spack_version, sha)
    assert expected == get_version()


def test_get_version_no_repo(tmpdir, monkeypatch):
    monkeypatch.setattr(spack.paths, "prefix", str(tmpdir))
    assert spack.spack_version == get_version()


def test_get_version_no_git(tmpdir, working_env):
    os.environ["PATH"] = str(tmpdir)
    assert spack.spack_version == get_version()


def test_main_calls_get_version(tmpdir, capsys, working_env):
    os.environ["PATH"] = str(tmpdir)
    main(["-V"])
    assert spack.spack_version == capsys.readouterr()[0].strip()


def test_get_version_bad_git(tmpdir, working_env):
    bad_git = str(tmpdir.join("git"))
    with open(bad_git, "w") as f:
        f.write("""#!/bin/sh
exit 1
""")
    fs.set_executable(bad_git)

    os.environ["PATH"] = str(tmpdir)
    assert spack.spack_version == get_version()

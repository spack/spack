# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from llnl.util.filesystem import working_dir

import spack.paths
import spack.cmd
from spack.main import SpackCommand
from spack.util.executable import which

pytestmark = pytest.mark.skipif(
    not which('git') or not spack.cmd.spack_is_git_repo(),
    reason="needs git")

blame = SpackCommand('blame')


def test_blame_by_modtime(mock_packages):
    """Sanity check the blame command to make sure it works."""
    out = blame('--time', 'mpich')
    assert 'LAST_COMMIT' in out
    assert 'AUTHOR' in out
    assert 'EMAIL' in out


def test_blame_by_percent(mock_packages):
    """Sanity check the blame command to make sure it works."""
    out = blame('--percent', 'mpich')
    assert 'LAST_COMMIT' in out
    assert 'AUTHOR' in out
    assert 'EMAIL' in out


def test_blame_file(mock_packages):
    """Sanity check the blame command to make sure it works."""
    with working_dir(spack.paths.prefix):
        out = blame('bin/spack')
    assert 'LAST_COMMIT' in out
    assert 'AUTHOR' in out
    assert 'EMAIL' in out


def test_blame_by_git(mock_packages, capfd):
    """Sanity check the blame command to make sure it works."""
    with capfd.disabled():
        out = blame('--git', 'mpich')
    assert 'class Mpich' in out
    assert '    homepage   = "http://www.mpich.org"' in out

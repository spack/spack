# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pickle
import sys

import pytest

from spack.environment import Environment
from spack.environment.environment import SpackEnvironmentViewError, _error_on_nonempty_view_dir
from llnl.util.symlink import _windows_can_symlink


def test_environment_pickle(tmpdir):
    env1 = Environment(str(tmpdir))
    obj = pickle.dumps(env1)
    env2 = pickle.loads(obj)
    assert isinstance(env2, Environment)


@pytest.mark.skipif(
    sys.platform == "win32" and not _windows_can_symlink(), reason="Requires elevated privileges."
)
def test_error_on_nonempty_view_dir(tmpdir):
    """Error when the target is not an empty dir"""
    with tmpdir.as_cwd():
        os.mkdir("empty_dir")
        os.mkdir("nonempty_dir")
        with open(os.path.join("nonempty_dir", "file"), "wb"):
            pass
        os.symlink("empty_dir", "symlinked_empty_dir")
        os.symlink("does_not_exist", "broken_link")
        os.symlink("broken_link", "file")

        # This is OK.
        _error_on_nonempty_view_dir("empty_dir")

        # This is not OK.
        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("nonempty_dir")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("symlinked_empty_dir")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("broken_link")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("file")


@pytest.mark.skipif(_windows_can_symlink(), reason="Requires base privileges.")
@pytest.mark.skipif(sys.platform != "win32", reason="Windows only.")
def test_error_on_nonempty_view_dir__win32_base(tmpdir):
    """Error when the target is not an empty dir. Cant make broken links on purpose
    without elevated privileges on windows so this version is abridged for windows
    base user privileges."""
    with tmpdir.as_cwd():
        os.mkdir("empty_dir")
        os.mkdir("nonempty_dir")
        with open(os.path.join("nonempty_dir", "file"), "wb"):
            pass

        # This is OK.
        _error_on_nonempty_view_dir("empty_dir")

        # This is not OK.
        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("nonempty_dir")

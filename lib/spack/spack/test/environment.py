# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pickle

import pytest

from spack.environment import Environment
from spack.environment.environment import (
    SpackEnvironmentViewError,
    _error_on_nonempty_view_dir,
)


def test_environment_pickle(tmpdir):
    env1 = Environment(str(tmpdir))
    obj = pickle.dumps(env1)
    env2 = pickle.loads(obj)
    assert isinstance(env2, Environment)


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

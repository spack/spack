# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pickle
from pathlib import Path

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
        Path("empty_dir").mkdir()
        Path("nonempty_dir").mkdir()
        with open(os.path.join("nonempty_dir", "file"), "wb"):
            pass
        Path("symlinked_empty_dir").link_to("empty_dir")
        Path("broken_link").link_to("does_not_exist")
        Path("file").link_to("broken_link")

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

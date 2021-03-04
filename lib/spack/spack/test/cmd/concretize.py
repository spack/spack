# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest
import spack.environment as ev
from spack.main import SpackCommand


# everything here uses the mock_env_path
pytestmark = pytest.mark.usefixtures(
    'mutable_mock_env_path', 'config', 'mutable_mock_repo')

env        = SpackCommand('env')
add        = SpackCommand('add')
concretize = SpackCommand('concretize')


def test_concretize_test_all():
    """Check all test dependencies are concretized."""
    env('create', 'test')

    with ev.read('test') as e:
        add('depb')
        concretize('--test', 'all')
        assert e.matching_spec('test-dependency')


def test_concretize_test_root_not_recursively():
    """Check that test dependencies are not concretized recursively."""
    env('create', 'test')

    with ev.read('test') as e:
        add('depb')
        concretize('--test', 'root')
        assert e.matching_spec('test-dependency') is None


def test_concretize_test_root():
    """Check that root test dependencies are concretized."""
    env('create', 'test')

    with ev.read('test') as e:
        add('b')
        concretize('--test', 'root')
        assert e.matching_spec('test-dependency')

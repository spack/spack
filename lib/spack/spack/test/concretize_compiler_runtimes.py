# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
from spack.version import Version

pytestmark = [pytest.mark.only_clingo("Original concretizer does not support compiler runtimes")]


@pytest.fixture
def runtime_repo(config):
    repo = os.path.join(spack.paths.repos_path, "compiler_runtime.test")
    with spack.repo.use_repositories(repo) as mock_repo:
        yield mock_repo


@pytest.fixture
def enable_runtimes():
    original = spack.solver.asp.WITH_RUNTIME
    spack.solver.asp.WITH_RUNTIME = True
    yield
    spack.solver.asp.WITH_RUNTIME = original


def test_correct_gcc_runtime_is_injected_as_dependency(runtime_repo, enable_runtimes):
    s = spack.spec.Spec("a%gcc@10.2.1 ^b%gcc@4.5.0").concretized()
    a, b = s["a"], s["b"]

    # Both a and b should depend on the same gcc-runtime directly
    assert a.dependencies("gcc-runtime") == b.dependencies("gcc-runtime")

    # And the gcc-runtime version should be that of the newest gcc used in the dag.
    assert a["gcc-runtime"].version == Version("10.2.1")

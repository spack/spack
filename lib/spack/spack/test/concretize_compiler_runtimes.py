# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

pytestmark = [
    pytest.mark.only_clingo("Original concretizer does not support compiler runtimes"),
    pytest.mark.usefixtures("enable_runtimes"),
]


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


def test_correct_gcc_runtime_is_injected_as_dependency(runtime_repo):
    s = spack.spec.Spec("a%gcc@10.2.1 ^b%gcc@4.5.0").concretized()
    a, b = s["a"], s["b"]

    # Both a and b should depend on the same gcc-runtime directly
    assert a.dependencies("gcc-runtime") == b.dependencies("gcc-runtime")

    # And the gcc-runtime version should be that of the newest gcc used in the dag.
    assert a["gcc-runtime"].version == Version("10.2.1")


@pytest.mark.regression("41972")
def test_external_nodes_do_not_have_runtimes(runtime_repo, mutable_config, tmp_path):
    """Tests that external nodes don't have runtime dependencies."""

    packages_yaml = {"b": {"externals": [{"spec": "b@1.0", "prefix": f"{str(tmp_path)}"}]}}
    spack.config.set("packages", packages_yaml)

    s = spack.spec.Spec("a%gcc@10.2.1").concretized()

    a, b = s["a"], s["b"]

    # Since b is an external, it doesn't depend on gcc-runtime
    assert a.dependencies("gcc-runtime")
    assert a.dependencies("b")
    assert not b.dependencies("gcc-runtime")

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


@pytest.mark.parametrize(
    "root_str,reused_str,expected,nruntime",
    [
        # The reused runtime is older than we need, thus we'll add a more recent one for a
        ("a%gcc@10.2.1", "b%gcc@4.5.0", {"a": "gcc-runtime@10.2.1", "b": "gcc-runtime@4.5.0"}, 2),
        # The root is compiled with an older compiler, thus we'll reuse the runtime from b
        ("a%gcc@4.5.0", "b%gcc@10.2.1", {"a": "gcc-runtime@10.2.1", "b": "gcc-runtime@10.2.1"}, 1),
    ],
)
def test_reusing_specs_with_gcc_runtime(root_str, reused_str, expected, nruntime, runtime_repo):
    """Tests that we can reuse specs with a "gcc-runtime" leaf node. In particular, checks
    that the semantic for gcc-runtimes versions accounts for reused packages too.
    """
    reused_spec = spack.spec.Spec(reused_str).concretized()
    assert f"{expected['b']}" in reused_spec

    setup = spack.solver.asp.SpackSolverSetup(tests=False)
    driver = spack.solver.asp.PyclingoDriver()
    result, _, _ = driver.solve(
        setup, [spack.spec.Spec(f"{root_str} ^{reused_str}")], reuse=[reused_spec]
    )

    root = result.specs[0]

    runtime_a = root.dependencies("gcc-runtime")[0]
    assert runtime_a.satisfies(expected["a"])
    runtime_b = root["b"].dependencies("gcc-runtime")[0]
    assert runtime_b.satisfies(expected["b"])

    runtimes = [x for x in root.traverse() if x.name == "gcc-runtime"]
    assert len(runtimes) == nruntime

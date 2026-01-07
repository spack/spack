# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import pytest

import spack.concretize
import spack.config
import spack.environment as ev
import spack.spec
from spack.main import SpackCommand

pytestmark = [
    pytest.mark.usefixtures("mutable_config", "mutable_mock_env_path", "mutable_mock_repo"),
    pytest.mark.not_on_windows("Envs unsupported on Windows"),
]

# See lib/spack/spack/platforms/test.py for how targets are defined on the Test platform
test_targets = ("m1", "aarch64") if platform.machine() == "arm64" else ("core2", "x86_64")

change = SpackCommand("change")


@pytest.mark.parametrize("dep", [True, False])
@pytest.mark.parametrize(
    "orig_constraint,mutated_constraint",
    [
        ("@3.23.1", "@3.4.3"),
        ("cflags=-O3", "cflags='-O0 -g'"),
        ("os=debian6", "os=redhat6"),
        (f"target={test_targets[0]}", f"target={test_targets[1]}"),
        ("build_system=generic", "build_system=foo"),
        (
            f"@3.4.3 cflags=-g os=debian6 target={test_targets[1]} build_system=generic",
            f"@3.23.1 cflags=-O3 os=redhat6 target={test_targets[0]} build_system=foo",
        ),
    ],
)
def test_mutate_internals(dep, orig_constraint, mutated_constraint):
    """
    Check that Environment.mutate and Spec.mutate work for several different constraint types.

    Includes check that environment.mutate rehashing gets the same answer as spec.mutate rehashing.
    """
    ev.create("test")
    env = ev.read("test")

    spack.config.set("packages:cmake", {"require": orig_constraint})

    root_name = "cmake-client" if dep else "cmake"
    env.add(root_name)
    env.concretize()

    root_spec = next(env.roots()).copy()
    cmake_spec = root_spec["cmake"] if dep else root_spec
    orig_cmake_spec = cmake_spec.copy()
    orig_hash = root_spec.dag_hash()

    for spec in env.all_specs_generator():
        if spec.name == "cmake":
            assert spec.satisfies(orig_constraint)

    selector = spack.spec.Spec("cmake")
    mutator = spack.spec.Spec(mutated_constraint)
    env.mutate(selector=selector, mutator=mutator)
    cmake_spec.mutate(mutator)

    for spec in env.all_specs_generator():
        if spec.name == "cmake":
            assert spec.satisfies(mutated_constraint)
    assert cmake_spec.satisfies(mutated_constraint)

    # Make sure that we're not changing variant types single/multi
    for name, variant in cmake_spec.variants.items():
        assert variant.type == orig_cmake_spec.variants[name].type

    new_hash = next(env.roots()).dag_hash()
    assert new_hash != orig_hash
    assert root_spec.dag_hash() != orig_hash
    assert root_spec.dag_hash() == new_hash


@pytest.mark.parametrize("constraint", ["foo", "foo.bar", "foo%cmake@1.0", "foo@1.1:", "foo/abc"])
def test_mutate_spec_invalid(constraint):
    spec = spack.concretize.concretize_one("cmake-client")
    with pytest.raises(spack.spec.SpecMutationError):
        spec.mutate(spack.spec.Spec(constraint))


def _test_mutate_from_cli(args, create=True):
    if create:
        ev.create("test")

    env = ev.read("test")

    if create:
        env.add("cmake-client%cmake@3.4.3")
        env.add("cmake-client%cmake@3.23.1")
        env.concretize()
        env.write()

    with env:
        change(*args)

    return list(env.roots())


def test_mutate_from_cli():
    match_spec = "%cmake@3.4.3"
    constraint = "@3.0"
    args = ["--concrete", f"--match-spec={match_spec}", constraint]
    roots = _test_mutate_from_cli(args)

    assert any(r.satisfies(match_spec) for r in roots)
    for root in roots:
        if root.satisfies("match_spec"):
            assert root.satisfies(constraint)


def test_mutate_from_cli_multiple():
    match_spec = "%cmake@3.4.3"
    constraint1 = "@3.0"
    constraint2 = "build_system=foo"
    args = ["--concrete", f"--match-spec={match_spec}", constraint1, constraint2]
    roots = _test_mutate_from_cli(args)

    assert any(r.satisfies(match_spec) for r in roots)
    for root in roots:
        if root.satisfies("match_spec"):
            assert root.satisfies(constraint1)
            assert root.satisfies(constraint2)


def test_mutate_from_cli_no_abstract():
    match_spec = "cmake"
    constraint = "@3.0"
    args = ["--concrete", f"--match-spec={match_spec}", constraint]

    with pytest.raises(ValueError, match="Cannot change abstract spec"):
        _ = _test_mutate_from_cli(args)

    args = ["--concrete-only"] + args[1:]
    roots = _test_mutate_from_cli(args, create=False)

    for root in roots:
        assert root[match_spec].satisfies(constraint)


def test_mutate_from_cli_all_no_match_spec():
    constraint = "cmake-client@3.0"
    args = ["--concrete", "--all", constraint]
    roots = _test_mutate_from_cli(args)

    for root in roots:
        assert root.satisfies(constraint)

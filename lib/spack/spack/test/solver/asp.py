# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import pytest

import spack.spec
import spack.solver.asp as asp
import spack.store


pytestmark = [
    pytest.mark.skipif(
        spack.config.get("config:concretizer") == "original", reason="requires new concretizer"
    ),
    pytest.mark.usefixtures("mutable_config", "mock_packages"),
]


@pytest.fixture
def reusable_specs(mock_packages):
    reusable_specs = []
    for spec in ["mpich", "openmpi", "zmpi"]:
        reusable_specs.extend(s for s in spack.spec.Spec(spec).concretized().traverse(root=True))
    return list(sorted(set(reusable_specs)))


@pytest.mark.parametrize(
    "root,reuse",
    itertools.product(
        ("mpileaks ^mpich", "mpileaks ^openmpi", "mpileaks ^zmpi", "patch"),
        (True, False),
    ),
)
def test_all_facts_in_solve(database, root, reuse, reusable_specs):
    reusable_specs = reusable_specs if reuse else []

    solver = spack.solver.asp.Solver()
    setup = spack.solver.asp.SpackSolverSetup()
    result, _, _ = solver.driver.solve(setup, [spack.spec.Spec(root)], reuse=reusable_specs)

    *_, result_attrs = result.answers[0]
    result_attrs = set(result_attrs)

    def remove_hashes(attrs):
        return []

    for spec in result.specs:
        # check only link and run deps if reusing.
        deptype = ("link", "run") if reuse else "all"

        # get all facts about the spec and filter out just the "attr" ones.
        attrs = setup.spec_clauses(spec, deptype=deptype, body=True, expand_hashes=True)

        # only consider attr() functions, not other displayed atoms
        # don't consider any DAG/package hashes, as they are added after solving
        attrs = set(attr for attr in attrs if attr.name == "attr" and "hash" not in attr.args[0])

        # make sure all facts from the solver are in the actual solution.
        diff = attrs - result_attrs

        # this is a current bug in the solver: we don't manage dependency patches
        # properly, and with reuse it can grab something w/o the right patch.
        # See https://github.com/spack/spack/issues/32497
        # TODO: Remove this XFAIL when #32497 is fixed.
        patches = [a for a in diff if a.args[0] == "variant_value" and a.args[2] == "patches"]
        if diff and not (diff - set(patches)):
            pytest.xfail("Bug in new concretizer with patch constraints. See #32497.")

        assert not diff

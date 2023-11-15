# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

from spack.mapping import ConcreteSpecsByHash
from spack.spec import Spec


class TestConcreteSpecsByHash:
    """Tests the container of concrete specs"""

    @pytest.mark.parametrize("input_specs", [["a"], ["a foobar=bar", "b"], ["a foobar=baz", "b"]])
    def test_adding_specs(self, input_specs, default_mock_concretization):
        """Tests that concrete specs in the container are equivalent, but stored as different
        objects in memory.
        """
        container = ConcreteSpecsByHash()
        input_specs = [Spec(s).concretized() for s in input_specs]
        for s in input_specs:
            container.add(s)

        for root in input_specs:
            for node in root.traverse(root=True):
                assert node == container[node.dag_hash()]
                assert node.dag_hash() in container
                assert node is not container[node.dag_hash()]

    @pytest.mark.parametrize(
        "input_specs,queries",
        [(["a foo=bar", "a foo=baz"], [("gmake", 1), ("^gmake", 2), ("foo=bar", 2)])],
    )
    def test_querying_specs(self, input_specs, queries, default_mock_concretization):
        """Tests that querying the container with a few known specs, we'll get back the
        expected number of results.
        """
        container = ConcreteSpecsByHash()
        input_specs = [Spec(s).concretized() for s in input_specs]
        for s in input_specs:
            container.add(s)

        for query_spec, nexpected in queries:
            matching_specs = container.query(query_spec)
            assert len(matching_specs) == nexpected

    @pytest.mark.parametrize(
        "input_specs,query_spec",
        [
            (["a foo=bar", "a foo=baz"], "a"),
            (["a foo=bar", "a foo=baz"], "b"),
            (["a foo=bar", "a foo=baz"], "gmake"),
        ],
    )
    def test_delete_specs(self, input_specs, query_spec, default_mock_concretization):
        container = ConcreteSpecsByHash()
        input_specs = [Spec(s).concretized() for s in input_specs]
        for s in input_specs:
            container.add(s)

        matching_specs = container.query(query_spec)
        for delete_spec in matching_specs:
            container.delete(delete_spec, transitive=True)

        for spec in container.values():
            assert not spec.satisfies(query_spec)
            for parent_spec in spec.dependents():
                assert not parent_spec.satisfies(query_spec)

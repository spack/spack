# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Tests for to_dict() and to_node_dict() with circular run dependencies.
"""

import json

import pytest

import spack.concretize
import spack.repo
from spack.test.conftest import RepoBuilder


@pytest.mark.usefixtures("config")
class TestCircularDictMethods:
    """Tests for to_dict() and to_node_dict() with circular dependencies."""

    def test_to_dict_with_circular_deps(self, repo_builder: RepoBuilder):
        """Test that to_dict() works with circular run dependencies without hanging."""
        repo_builder.add_package("circ-a", dependencies=[("circ-b", "run", None)])
        repo_builder.add_package("circ-b", dependencies=[("circ-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("circ-a")
            spec_b = spec_a["circ-b"]

            # Should not raise RecursionError or hang
            dict_a = spec_a.to_dict()
            dict_b = spec_b.to_dict()

            # Verify structure - to_dict returns {"spec": {"_meta": ..., "nodes": [...]}}
            assert "spec" in dict_a
            assert "spec" in dict_b
            assert "nodes" in dict_a["spec"]
            assert "nodes" in dict_b["spec"]

            # Each node should have a hash
            nodes_a = dict_a["spec"]["nodes"]
            nodes_b = dict_b["spec"]["nodes"]

            # Find the root node (first node in the list)
            assert len(nodes_a) > 0
            assert len(nodes_b) > 0
            assert "hash" in nodes_a[0]
            assert "hash" in nodes_b[0]

            # Root hashes should be different
            assert nodes_a[0]["hash"] != nodes_b[0]["hash"]

    def test_to_node_dict_with_circular_deps(self, repo_builder: RepoBuilder):
        """Test that to_node_dict() works with circular run dependencies without hanging."""
        repo_builder.add_package("circ-a", dependencies=[("circ-b", "run", None)])
        repo_builder.add_package("circ-b", dependencies=[("circ-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("circ-a")
            spec_b = spec_a["circ-b"]

            # Should not raise RecursionError or hang
            node_dict_a = spec_a.to_node_dict()
            node_dict_b = spec_b.to_node_dict()

            # Verify structure
            assert "name" in node_dict_a
            assert "name" in node_dict_b

            # Note: to_node_dict() may not include hash depending on hash_descriptor
            # The key test is that it doesn't hang or recurse infinitely

            # Dependencies should be present
            assert "dependencies" in node_dict_a
            assert "dependencies" in node_dict_b

            # The circular dependency should be reflected
            # dependencies is a list of dicts with 'name' keys
            dep_names_a = [d["name"] for d in node_dict_a["dependencies"]]
            dep_names_b = [d["name"] for d in node_dict_b["dependencies"]]

            assert "circ-b" in dep_names_a
            assert "circ-a" in dep_names_b

    def test_dict_methods_determinism(self, repo_builder: RepoBuilder):
        """Test that to_dict() and to_node_dict() produce deterministic output."""
        repo_builder.add_package("circ-a", dependencies=[("circ-b", "run", None)])
        repo_builder.add_package("circ-b", dependencies=[("circ-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            # Concretize multiple times
            dicts = []
            node_dicts = []

            for _ in range(3):
                spec = spack.concretize.concretize_one("circ-a")
                dicts.append(json.dumps(spec.to_dict(), sort_keys=True))
                node_dicts.append(json.dumps(spec.to_node_dict(), sort_keys=True))

            # All should be identical
            assert len(set(dicts)) == 1, "to_dict() not deterministic"
            assert len(set(node_dicts)) == 1, "to_node_dict() not deterministic"

    def test_three_node_cycle_dict_methods(self, repo_builder: RepoBuilder):
        """Test dict methods with a 3-node cycle."""
        repo_builder.add_package("cyc-a", dependencies=[("cyc-b", "run", None)])
        repo_builder.add_package("cyc-b", dependencies=[("cyc-c", "run", None)])
        repo_builder.add_package("cyc-c", dependencies=[("cyc-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("cyc-a")

            # All three should produce valid dicts without hanging
            dict_a = spec_a.to_dict()
            dict_b = spec_a["cyc-b"].to_dict()
            dict_c = spec_a["cyc-c"].to_dict()

            node_dict_a = spec_a.to_node_dict()
            node_dict_b = spec_a["cyc-b"].to_node_dict()
            node_dict_c = spec_a["cyc-c"].to_node_dict()

            # All hashes should be unique - extract from root nodes
            hashes_from_to_dict = {
                dict_a["spec"]["nodes"][0]["hash"],
                dict_b["spec"]["nodes"][0]["hash"],
                dict_c["spec"]["nodes"][0]["hash"],
            }
            assert len(hashes_from_to_dict) == 3

            # Verify all dag_hash() calls work
            assert spec_a.dag_hash() != spec_a["cyc-b"].dag_hash()
            assert spec_a["cyc-b"].dag_hash() != spec_a["cyc-c"].dag_hash()
            assert spec_a.dag_hash() != spec_a["cyc-c"].dag_hash()

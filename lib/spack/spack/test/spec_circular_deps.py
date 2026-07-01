# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Tests for circular run dependencies and DAG hash computation with cycles.

This test suite covers:
- DAG hash computation with cycles using SCC detection
- Serialization methods (to_dict, to_node_dict, to_json, to_yaml)
- Dependency traversal with circular dependencies
"""

import json

import pytest

import spack.concretize
import spack.repo
from spack.test.conftest import RepoBuilder


@pytest.mark.usefixtures("config")
class TestCircularRunDependencies:
    """Tests for handling circular run dependencies in spec hashing."""

    def test_simple_circular_run_dependency(self, repo_builder: RepoBuilder):
        """Test A->(run)->B->(run)->A produces unique, deterministic hashes.

        Both packages should get unique hashes that are the same regardless
        of which node we start from.
        """
        repo_builder.add_package("circ-a", dependencies=[("circ-b", "run", None)])
        repo_builder.add_package("circ-b", dependencies=[("circ-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("circ-a")
            spec_b = spec_a["circ-b"]

            # Both should have valid hashes
            hash_a = spec_a.dag_hash()
            hash_b = spec_b.dag_hash()

            assert hash_a is not None
            assert hash_b is not None
            assert hash_a != hash_b  # Different nodes get different hashes

            # Hash should be deterministic - compute again from B
            spec_b2 = spack.concretize.concretize_one("circ-b")
            spec_a2 = spec_b2["circ-a"]

            assert spec_a2.dag_hash() == hash_a
            assert spec_b2.dag_hash() == hash_b

    def test_three_node_run_cycle(self, repo_builder: RepoBuilder):
        """Test A->(run)->B->(run)->C->(run)->A all get unique hashes.

        All three packages in the cycle should have unique, deterministic hashes.
        """
        repo_builder.add_package("cyc-a", dependencies=[("cyc-b", "run", None)])
        repo_builder.add_package("cyc-b", dependencies=[("cyc-c", "run", None)])
        repo_builder.add_package("cyc-c", dependencies=[("cyc-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("cyc-a")
            spec_b = spec_a["cyc-b"]
            spec_c = spec_a["cyc-c"]

            hash_a = spec_a.dag_hash()
            hash_b = spec_b.dag_hash()
            hash_c = spec_c.dag_hash()

            # All should have unique hashes
            assert hash_a != hash_b
            assert hash_b != hash_c
            assert hash_a != hash_c

            # Verify determinism from different entry points
            spec_b2 = spack.concretize.concretize_one("cyc-b")
            assert spec_b2.dag_hash() == hash_b
            assert spec_b2["cyc-c"].dag_hash() == hash_c
            assert spec_b2["cyc-a"].dag_hash() == hash_a

            spec_c2 = spack.concretize.concretize_one("cyc-c")
            assert spec_c2.dag_hash() == hash_c
            assert spec_c2["cyc-a"].dag_hash() == hash_a
            assert spec_c2["cyc-b"].dag_hash() == hash_b

    def test_run_cycle_with_link_deps(self, repo_builder: RepoBuilder):
        """Test cycle with link dependencies: A->(run)->B->(run)->A, both depend on X.

        The cycle hash must actually incorporate the link dependency's hash, so we assert that
        each cycle member's serialized node dict embeds X's hash rather than merely checking that
        the three hashes happen to differ.
        """
        repo_builder.add_package("link-x")
        repo_builder.add_package(
            "cyc-link-a", dependencies=[("cyc-link-b", "run", None), ("link-x", "link", None)]
        )
        repo_builder.add_package(
            "cyc-link-b", dependencies=[("cyc-link-a", "run", None), ("link-x", "link", None)]
        )

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("cyc-link-a")
            spec_b = spec_a["cyc-link-b"]
            spec_x = spec_a["link-x"]

            hash_a = spec_a.dag_hash()
            hash_b = spec_b.dag_hash()
            hash_x = spec_x.dag_hash()

            # All should have valid, unique hashes
            assert len({hash_a, hash_b, hash_x}) == 3

            # Each cycle member must embed X's hash as a dependency: this is what proves the link
            # dependency actually feeds into the cycle members' hashes.
            for member in (spec_a, spec_b):
                embedded = {d["name"]: d.get("hash") for d in member.to_node_dict()["dependencies"]}
                assert embedded.get("link-x") == hash_x

            # Hashes are deterministic across re-concretization.
            spec_a2 = spack.concretize.concretize_one("cyc-link-a")
            assert spec_a2.dag_hash() == hash_a
            assert spec_a2["cyc-link-b"].dag_hash() == hash_b
            assert spec_a2["link-x"].dag_hash() == hash_x

    def test_multiple_independent_cycles(self, repo_builder: RepoBuilder):
        """Test graph with two independent cycles.

        Root depends on two separate circular dependency components.
        """
        # First cycle: A <-> B
        repo_builder.add_package("ind-a", dependencies=[("ind-b", "run", None)])
        repo_builder.add_package("ind-b", dependencies=[("ind-a", "run", None)])

        # Second cycle: C <-> D
        repo_builder.add_package("ind-c", dependencies=[("ind-d", "run", None)])
        repo_builder.add_package("ind-d", dependencies=[("ind-c", "run", None)])

        # Root depends on both cycles with link deps so they're in dag_hash
        repo_builder.add_package(
            "ind-root", dependencies=[("ind-a", "link", None), ("ind-c", "link", None)]
        )

        with spack.repo.use_repositories(repo_builder.root):
            spec_root = spack.concretize.concretize_one("ind-root")

            hash_a = spec_root["ind-a"].dag_hash()
            hash_b = spec_root["ind-b"].dag_hash()
            hash_c = spec_root["ind-c"].dag_hash()
            hash_d = spec_root["ind-d"].dag_hash()
            hash_root = spec_root.dag_hash()

            # All should have unique hashes
            assert len({hash_a, hash_b, hash_c, hash_d, hash_root}) == 5

            # The root must embed the hashes of both cycle entry points it links against, proving
            # the two independent cycles both feed into the root's hash.
            root_deps = {d["name"]: d.get("hash") for d in spec_root.to_node_dict()["dependencies"]}
            assert root_deps.get("ind-a") == hash_a
            assert root_deps.get("ind-c") == hash_c

            # Hashes are deterministic across re-concretization.
            spec_root2 = spack.concretize.concretize_one("ind-root")
            assert spec_root2.dag_hash() == hash_root
            assert spec_root2["ind-a"].dag_hash() == hash_a
            assert spec_root2["ind-b"].dag_hash() == hash_b
            assert spec_root2["ind-c"].dag_hash() == hash_c
            assert spec_root2["ind-d"].dag_hash() == hash_d

    def test_deep_run_cycle(self, repo_builder: RepoBuilder):
        """Test cycle buried deep in dependency tree.

        Root ->(link)-> X ->(link)-> Y ->(run)-> A ->(run)-> B ->(run)-> A
        """
        # Circular component
        repo_builder.add_package("deep-a", dependencies=[("deep-b", "run", None)])
        repo_builder.add_package("deep-b", dependencies=[("deep-a", "run", None)])

        # Non-circular chain from root
        repo_builder.add_package("deep-y", dependencies=[("deep-a", "run", None)])
        repo_builder.add_package("deep-x", dependencies=[("deep-y", "link", None)])
        repo_builder.add_package("deep-root", dependencies=[("deep-x", "link", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_root = spack.concretize.concretize_one("deep-root")

            hash_root = spec_root.dag_hash()
            hash_x = spec_root["deep-x"].dag_hash()
            hash_y = spec_root["deep-y"].dag_hash()
            hash_a = spec_root["deep-a"].dag_hash()
            hash_b = spec_root["deep-b"].dag_hash()

            # All unique
            assert len({hash_root, hash_x, hash_y, hash_a, hash_b}) == 5

            # Cycle deps have consistent hashes when neither is the root
            assert spec_root["deep-a"]["deep-b"].dag_hash() == hash_b
            assert spec_root["deep-b"]["deep-a"].dag_hash() == hash_a

            # Hashes are deterministic across re-concretization.
            spec_root2 = spack.concretize.concretize_one("deep-root")
            assert spec_root2.dag_hash() == hash_root
            assert spec_root2["deep-x"].dag_hash() == hash_x
            assert spec_root2["deep-y"].dag_hash() == hash_y
            assert spec_root2["deep-a"].dag_hash() == hash_a
            assert spec_root2["deep-b"].dag_hash() == hash_b

    def test_to_dict_with_circular_deps(self, repo_builder: RepoBuilder):
        """Test that to_dict() works with circular run dependencies without hanging."""
        repo_builder.add_package("dict-a", dependencies=[("dict-b", "run", None)])
        repo_builder.add_package("dict-b", dependencies=[("dict-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("dict-a")
            spec_b = spec_a["dict-b"]

            # Should not raise RecursionError or hang
            dict_a = spec_a.to_dict()
            dict_b = spec_b.to_dict()

            # Verify structure
            assert "spec" in dict_a
            assert "spec" in dict_b
            assert "nodes" in dict_a["spec"]
            assert "nodes" in dict_b["spec"]

            # Root hashes should be different
            assert dict_a["spec"]["nodes"][0]["hash"] != dict_b["spec"]["nodes"][0]["hash"]

    def test_to_node_dict_with_circular_deps(self, repo_builder: RepoBuilder):
        """Test that to_node_dict() works with circular run dependencies without hanging."""
        repo_builder.add_package("node-a", dependencies=[("node-b", "run", None)])
        repo_builder.add_package("node-b", dependencies=[("node-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("node-a")
            spec_b = spec_a["node-b"]

            # Should not raise RecursionError or hang
            node_dict_a = spec_a.to_node_dict()
            node_dict_b = spec_b.to_node_dict()

            # The circular dependency should be reflected
            dep_names_a = [d["name"] for d in node_dict_a["dependencies"]]
            dep_names_b = [d["name"] for d in node_dict_b["dependencies"]]

            assert "node-b" in dep_names_a
            assert "node-a" in dep_names_b

    def test_dict_methods_determinism(self, repo_builder: RepoBuilder):
        """Test that to_dict() and to_node_dict() produce deterministic output."""
        repo_builder.add_package("ddet-a", dependencies=[("ddet-b", "run", None)])
        repo_builder.add_package("ddet-b", dependencies=[("ddet-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            # Concretize multiple times
            dicts = []
            node_dicts = []

            for _ in range(3):
                spec = spack.concretize.concretize_one("ddet-a")
                dicts.append(json.dumps(spec.to_dict(), sort_keys=True))
                node_dicts.append(json.dumps(spec.to_node_dict(), sort_keys=True))

            # All should be identical
            assert len(set(dicts)) == 1, "to_dict() not deterministic"
            assert len(set(node_dicts)) == 1, "to_node_dict() not deterministic"

    def test_to_json_with_circular_deps(self, repo_builder: RepoBuilder):
        """Verify to_json() works with circular dependencies."""
        repo_builder.add_package("json-a", dependencies=[("json-b", "run", None)])
        repo_builder.add_package("json-b", dependencies=[("json-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("json-a")

            # Should not hang or raise RecursionError
            json_str = spec.to_json()

            # Should be valid JSON
            parsed = json.loads(json_str)
            assert "spec" in parsed

    def test_to_yaml_with_circular_deps(self, repo_builder: RepoBuilder):
        """Verify to_yaml() works with circular dependencies."""
        repo_builder.add_package("yaml-a", dependencies=[("yaml-b", "run", None)])
        repo_builder.add_package("yaml-b", dependencies=[("yaml-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("yaml-a")

            # Should not hang or raise RecursionError
            yaml_str = spec.to_yaml()

            assert "yaml-a" in yaml_str
            assert "yaml-b" in yaml_str

    def test_dependency_traversal(self, repo_builder: RepoBuilder):
        """Verify traverse() works with circular run dependencies."""
        repo_builder.add_package("trav-a", dependencies=[("trav-b", "run", None)])
        repo_builder.add_package("trav-b", dependencies=[("trav-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("trav-a")
            spec_b = spec_a["trav-b"]

            # Should be able to traverse the dependency graph without hanging
            # Collect all specs encountered during traversal
            traversed_from_a = list(spec_a.traverse())
            traversed_from_b = list(spec_b.traverse())

            # Should include both specs in the cycle
            names_from_a = {s.name for s in traversed_from_a}
            names_from_b = {s.name for s in traversed_from_b}

            assert "trav-a" in names_from_a
            assert "trav-b" in names_from_a
            assert "trav-a" in names_from_b
            assert "trav-b" in names_from_b

            # Both should traverse the same set of specs (the cycle)
            assert names_from_a == names_from_b

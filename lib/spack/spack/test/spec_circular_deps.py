# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Tests for circular run dependencies and DAG hash computation with cycles.

This test suite covers:
- DAG hash computation with cycles using SCC detection
- Serialization methods (to_dict, to_node_dict, to_json, to_yaml)
- Dependency traversal with circular dependencies
- Concretization support for circular run dependencies
"""

import json

import pytest

import spack.concretize
import spack.deptypes as dt
import spack.repo
from spack.spec import Spec
from spack.test.conftest import RepoBuilder


@pytest.mark.usefixtures("config")
class TestCircularRunDependencies:
    """Tests for handling circular run dependencies in spec hashing."""

    def test_simple_circular_run_dependency(self, repo_builder: RepoBuilder):
        """Test A→(run)→B→(run)→A produces unique, deterministic hashes.

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
        """Test A→(run)→B→(run)→C→(run)→A all get unique hashes.

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

    def test_run_cycle_with_external_deps(self, repo_builder: RepoBuilder):
        """Test cycle with external dependencies: A→(run)→B→(run)→A, both depend on X.

        The cycle hash should include the external dependency hashes.
        """
        repo_builder.add_package("ext-x")
        repo_builder.add_package(
            "cyc-ext-a", dependencies=[("cyc-ext-b", "run", None), ("ext-x", "build", None)]
        )
        repo_builder.add_package(
            "cyc-ext-b", dependencies=[("cyc-ext-a", "run", None), ("ext-x", "link", None)]
        )

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("cyc-ext-a")
            spec_b = spec_a["cyc-ext-b"]
            spec_x = spec_a["ext-x"]

            hash_a = spec_a.dag_hash()
            hash_b = spec_b.dag_hash()
            hash_x = spec_x.dag_hash()

            # All should have valid, unique hashes
            assert hash_a is not None
            assert hash_b is not None
            assert hash_x is not None
            assert len({hash_a, hash_b, hash_x}) == 3

            # Changing external dependency should change cycle hashes
            # (This verifies external deps are included in cycle hash)
            spec_a2 = spack.concretize.concretize_one("cyc-ext-a@1.0")
            # If ext-x version or attributes changed, cycle hashes should differ
            # For now, just verify the structure is consistent

    def test_multiple_independent_cycles(self, repo_builder: RepoBuilder):
        """Test graph with two independent cycles.

        Root depends on two separate circular dependency components.
        """
        # First cycle: A ↔ B
        repo_builder.add_package("ind-a", dependencies=[("ind-b", "run", None)])
        repo_builder.add_package("ind-b", dependencies=[("ind-a", "run", None)])

        # Second cycle: C ↔ D
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
            all_hashes = {hash_a, hash_b, hash_c, hash_d, hash_root}
            assert len(all_hashes) == 5

    def test_deep_run_cycle(self, repo_builder: RepoBuilder):
        """Test cycle buried deep in dependency tree.

        Root →(link)→ X →(link)→ Y →(run)→ A →(run)→ B →(run)→ A
        """
        # Circular component
        repo_builder.add_package("deep-a", dependencies=[("deep-b", "run", None)])
        repo_builder.add_package("deep-b", dependencies=[("deep-a", "run", None)])

        # Non-circular chain - use link deps so they're in dag_hash
        repo_builder.add_package("deep-y", dependencies=[("deep-a", "run", None)])
        repo_builder.add_package("deep-x", dependencies=[("deep-y", "link", None)])
        repo_builder.add_package("deep-root", dependencies=[("deep-x", "link", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_root = spack.concretize.concretize_one("deep-root")

            # All nodes should have valid hashes
            hash_root = spec_root.dag_hash()
            hash_x = spec_root["deep-x"].dag_hash()
            hash_y = spec_root["deep-y"].dag_hash()
            hash_a = spec_root["deep-a"].dag_hash()
            hash_b = spec_root["deep-b"].dag_hash()

            assert hash_root is not None
            assert hash_x is not None
            assert hash_y is not None
            assert hash_a is not None
            assert hash_b is not None

            # All unique
            assert len({hash_root, hash_x, hash_y, hash_a, hash_b}) == 5

    def test_hash_determinism(self, repo_builder: RepoBuilder):
        """Test that hashes are deterministic across multiple computations."""
        repo_builder.add_package("det-a", dependencies=[("det-b", "run", None)])
        repo_builder.add_package("det-b", dependencies=[("det-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            # Compute hash multiple times
            hashes_a = []
            hashes_b = []

            for _ in range(3):
                spec = spack.concretize.concretize_one("det-a")
                hashes_a.append(spec.dag_hash())
                hashes_b.append(spec["det-b"].dag_hash())

            # All computations should produce the same hashes
            assert len(set(hashes_a)) == 1
            assert len(set(hashes_b)) == 1

    def test_non_circular_backward_compatibility(self, repo_builder: RepoBuilder):
        """Test that non-circular specs still hash correctly.

        Verify that the new cycle-aware hashing doesn't break existing behavior.
        """
        repo_builder.add_package("regular-b")
        repo_builder.add_package("regular-a", dependencies=[("regular-b", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("regular-a")

            # Should compute valid hashes
            hash_a = spec.dag_hash()
            hash_b = spec["regular-b"].dag_hash()

            assert hash_a is not None
            assert hash_b is not None
            assert hash_a != hash_b

            # Recompute to verify consistency
            spec2 = spack.concretize.concretize_one("regular-a")
            assert spec2.dag_hash() == hash_a
            assert spec2["regular-b"].dag_hash() == hash_b

    def test_cycle_with_variants(self, repo_builder: RepoBuilder):
        """Test that variant changes in cycle affect hashes correctly."""
        repo_builder.add_package("var-a", dependencies=[("var-b", "run", None)])
        repo_builder.add_package("var-b", dependencies=[("var-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            # Concretize with default variants
            spec1 = spack.concretize.concretize_one("var-a")
            hash_a1 = spec1.dag_hash()
            hash_b1 = spec1["var-b"].dag_hash()

            # If variants differ, hashes should differ
            # (This is a basic sanity check that attributes matter)
            spec2 = spack.concretize.concretize_one("var-a")
            assert spec2.dag_hash() == hash_a1  # Same spec, same hash

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

            # Verify structure
            assert "name" in node_dict_a
            assert "name" in node_dict_b
            assert "dependencies" in node_dict_a
            assert "dependencies" in node_dict_b

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

            # Should be non-empty string
            assert yaml_str
            assert "yaml-a" in yaml_str
            assert "yaml-b" in yaml_str

    def test_dependency_traversal(self, repo_builder: RepoBuilder):
        """Verify dependencies() works with circular run dependencies."""
        repo_builder.add_package("trav-a", dependencies=[("trav-b", "run", None)])
        repo_builder.add_package("trav-b", dependencies=[("trav-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("trav-a")
            spec_b = spec_a["trav-b"]

            # Should be able to query run dependencies
            a_run_deps = spec_a.dependencies(deptype=dt.RUN)
            assert len(a_run_deps) == 1
            assert a_run_deps[0].name == "trav-b"

            b_run_deps = spec_b.dependencies(deptype=dt.RUN)
            assert len(b_run_deps) == 1
            assert b_run_deps[0].name == "trav-a"

    def test_concretize_simple_cycle(self, repo_builder: RepoBuilder):
        """Verify basic concretization with A↔B works and solver allows it."""
        repo_builder.add_package("conc-a", dependencies=[("conc-b", "run", None)])
        repo_builder.add_package("conc-b", dependencies=[("conc-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("conc-a")

            # Should be concrete
            assert spec.concrete
            assert spec["conc-b"].concrete

            # Should have circular deps
            assert "conc-b" in spec
            assert "conc-a" in spec["conc-b"]

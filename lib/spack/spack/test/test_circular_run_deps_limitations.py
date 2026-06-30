# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Tests for circular run dependency support - verifying what works.

## Current Implementation Status

This implementation provides **hash computation** support for circular run dependencies:
- ✓ Specs with circular run dependencies can be concretized
- ✓ dag_hash() computes unique, deterministic hashes for all nodes in a cycle
- ✓ Specs can be serialized (to_dict, to_json, to_yaml)
- ✓ Hash computation uses SCC detection and topological sorting

## Known Limitations

The following components do NOT yet support circular dependencies:

1. **PackageInstaller**: The installer's dependency ordering logic creates a deadlock
   when both A depends on B and B depends on A. The installer waits for each to be
   installed before installing the other, creating an unresolvable state.

2. **Database.add()**: Adding specs with circular dependencies to the database causes
   infinite recursion in the database's internal traversal logic.

These limitations do not affect the core hash computation, which is the foundation
for all other operations. Future work can build on this to add installer and database support.
"""

import json

import pytest

import spack.concretize
import spack.deptypes as dt
import spack.repo
from spack.test.conftest import RepoBuilder


@pytest.mark.usefixtures("config")
class TestCircularRunDependenciesCore:
    """Tests for core circular dependency functionality that works."""

    def test_concretize_simple_cycle(self, repo_builder: RepoBuilder):
        """Verify basic concretization with A↔B works."""
        repo_builder.add_package("core-a", dependencies=[("core-b", "run", None)])
        repo_builder.add_package("core-b", dependencies=[("core-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("core-a")

            # Should be concrete
            assert spec.concrete
            assert spec["core-b"].concrete

            # Should have circular deps
            assert "core-b" in spec
            assert "core-a" in spec["core-b"]

    def test_hash_computation_simple_cycle(self, repo_builder: RepoBuilder):
        """Verify hash computation works for simple circular dependency."""
        repo_builder.add_package("hash-a", dependencies=[("hash-b", "run", None)])
        repo_builder.add_package("hash-b", dependencies=[("hash-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("hash-a")
            spec_b = spec_a["hash-b"]

            # Both should have valid hashes
            hash_a = spec_a.dag_hash()
            hash_b = spec_b.dag_hash()

            assert hash_a is not None
            assert hash_b is not None
            assert len(hash_a) == 32  # Base32 encoded
            assert len(hash_b) == 32
            assert hash_a != hash_b  # Different nodes get different hashes

    def test_hash_determinism_across_entry_points(self, repo_builder: RepoBuilder):
        """Verify hashes are the same regardless of entry point into cycle."""
        repo_builder.add_package("det-a", dependencies=[("det-b", "run", None)])
        repo_builder.add_package("det-b", dependencies=[("det-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            # Concretize from A
            spec_a1 = spack.concretize.concretize_one("det-a")
            hash_a_from_a = spec_a1.dag_hash()
            hash_b_from_a = spec_a1["det-b"].dag_hash()

            # Concretize from B
            spec_b1 = spack.concretize.concretize_one("det-b")
            hash_b_from_b = spec_b1.dag_hash()
            hash_a_from_b = spec_b1["det-a"].dag_hash()

            # Hashes should match regardless of entry point
            assert hash_a_from_a == hash_a_from_b
            assert hash_b_from_a == hash_b_from_b

    def test_three_node_cycle_hashes(self, repo_builder: RepoBuilder):
        """Verify hash computation for 3-node cycle A→B→C→A."""
        repo_builder.add_package("cyc3-a", dependencies=[("cyc3-b", "run", None)])
        repo_builder.add_package("cyc3-b", dependencies=[("cyc3-c", "run", None)])
        repo_builder.add_package("cyc3-c", dependencies=[("cyc3-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("cyc3-a")

            hash_a = spec.dag_hash()
            hash_b = spec["cyc3-b"].dag_hash()
            hash_c = spec["cyc3-c"].dag_hash()

            # All unique
            assert len({hash_a, hash_b, hash_c}) == 3

            # Deterministic from different entry points
            spec_b = spack.concretize.concretize_one("cyc3-b")
            assert spec_b.dag_hash() == hash_b
            assert spec_b["cyc3-a"].dag_hash() == hash_a
            assert spec_b["cyc3-c"].dag_hash() == hash_c

    def test_serialization_to_dict(self, repo_builder: RepoBuilder):
        """Verify to_dict() works with circular dependencies."""
        repo_builder.add_package("ser-a", dependencies=[("ser-b", "run", None)])
        repo_builder.add_package("ser-b", dependencies=[("ser-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("ser-a")

            # Should not hang or raise RecursionError
            spec_dict = spec.to_dict()

            assert "spec" in spec_dict
            assert "nodes" in spec_dict["spec"]

            # Verify both nodes are in the output
            node_names = {node["name"] for node in spec_dict["spec"]["nodes"]}
            assert "ser-a" in node_names
            assert "ser-b" in node_names

    def test_serialization_to_json(self, repo_builder: RepoBuilder):
        """Verify to_json() works with circular dependencies."""
        repo_builder.add_package("json-a", dependencies=[("json-b", "run", None)])
        repo_builder.add_package("json-b", dependencies=[("json-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("json-a")

            # Should not hang or raise RecursionError
            json_str = spec.to_json()

            assert json_str is not None
            parsed = json.loads(json_str)
            assert "spec" in parsed

    def test_serialization_to_yaml(self, repo_builder: RepoBuilder):
        """Verify to_yaml() works with circular dependencies."""
        repo_builder.add_package("yaml-a", dependencies=[("yaml-b", "run", None)])
        repo_builder.add_package("yaml-b", dependencies=[("yaml-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("yaml-a")

            # Should not hang or raise RecursionError
            yaml_str = spec.to_yaml()

            assert yaml_str is not None
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

    def test_cycle_with_external_dependencies(self, repo_builder: RepoBuilder):
        """Verify cycles with external non-circular dependencies work."""
        repo_builder.add_package("ext-dep")
        repo_builder.add_package(
            "ext-cyc-a", dependencies=[("ext-cyc-b", "run", None), ("ext-dep", "link", None)]
        )
        repo_builder.add_package(
            "ext-cyc-b", dependencies=[("ext-cyc-a", "run", None), ("ext-dep", "link", None)]
        )

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("ext-cyc-a")

            # All three specs should have hashes
            hash_a = spec.dag_hash()
            hash_b = spec["ext-cyc-b"].dag_hash()
            hash_ext = spec["ext-dep"].dag_hash()

            assert hash_a is not None
            assert hash_b is not None
            assert hash_ext is not None
            assert len({hash_a, hash_b, hash_ext}) == 3

    def test_backward_compatibility_non_circular(self, repo_builder: RepoBuilder):
        """Verify non-circular specs still work correctly."""
        repo_builder.add_package("compat-b")
        repo_builder.add_package("compat-a", dependencies=[("compat-b", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("compat-a")

            # Should work exactly as before
            hash_a = spec.dag_hash()
            hash_b = spec["compat-b"].dag_hash()

            assert hash_a is not None
            assert hash_b is not None
            assert hash_a != hash_b

            # Should be serializable
            assert spec.to_dict() is not None
            assert spec.to_json() is not None
            assert spec.to_yaml() is not None

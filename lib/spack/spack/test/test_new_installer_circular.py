# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Tests for circular run dependency support in new_installer.py
"""

import pytest

import spack.concretize
import spack.deptypes as dt
import spack.repo
import spack.store
from spack.new_installer import BuildGraph
from spack.test.conftest import RepoBuilder


@pytest.mark.usefixtures("mutable_database")
class TestNewInstallerCircularDeps:
    """Tests for BuildGraph with circular run dependencies."""

    def test_is_ordering_dependency_link(self, repo_builder: RepoBuilder):
        """Test that LINK dependencies are ordering dependencies."""
        repo_builder.add_package("parent")
        repo_builder.add_package("child", dependencies=[("parent", "link", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("child")
            parent_spec = spec["parent"]

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            assert graph._is_ordering_dependency(spec, parent_spec)

    def test_is_ordering_dependency_run_only(self, repo_builder: RepoBuilder):
        """Test that RUN-only dependencies are NOT ordering dependencies."""
        repo_builder.add_package("parent")
        repo_builder.add_package("child", dependencies=[("parent", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("child")
            parent_spec = spec["parent"]

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            assert not graph._is_ordering_dependency(spec, parent_spec)

    def test_build_graph_circular_run_deps(self, repo_builder: RepoBuilder):
        """Test BuildGraph with circular run dependencies A↔B."""
        repo_builder.add_package("circ-a", dependencies=[("circ-b", "run", None)])
        repo_builder.add_package("circ-b", dependencies=[("circ-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("circ-a")
            hash_a = spec_a.dag_hash()
            hash_b = spec_a["circ-b"].dag_hash()

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec_a],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            # Both specs should be in the graph
            assert hash_a in graph.nodes
            assert hash_b in graph.nodes

            # Neither should have ordering children (run-only deps excluded)
            assert hash_a not in graph.parent_to_child or not graph.parent_to_child[hash_a]
            assert hash_b not in graph.parent_to_child or not graph.parent_to_child[hash_b]

            # Both should be ready to install (in pending_builds)
            # We need to check this by looking at what would be in pending_builds
            # after graph construction
            assert not graph.parent_to_child.get(hash_a, set())
            assert not graph.parent_to_child.get(hash_b, set())

    def test_build_graph_mixed_deps_cycle(self, repo_builder: RepoBuilder):
        """Test A→B (link), B→A (run) - only A should wait for B."""
        repo_builder.add_package("mixed-a", dependencies=[("mixed-b", "link", None)])
        repo_builder.add_package("mixed-b", dependencies=[("mixed-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec_a = spack.concretize.concretize_one("mixed-a")
            hash_a = spec_a.dag_hash()
            hash_b = spec_a["mixed-b"].dag_hash()

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec_a],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            # A should have B as ordering child (LINK dep)
            assert hash_b in graph.parent_to_child.get(hash_a, set())

            # B should NOT have A as ordering child (RUN-only dep)
            assert hash_a not in graph.parent_to_child.get(hash_b, set())

    def test_build_graph_three_node_run_cycle(self, repo_builder: RepoBuilder):
        """Test A→B→C→A (all run-only) - all should be ready immediately."""
        repo_builder.add_package("cyc3-a", dependencies=[("cyc3-b", "run", None)])
        repo_builder.add_package("cyc3-b", dependencies=[("cyc3-c", "run", None)])
        repo_builder.add_package("cyc3-c", dependencies=[("cyc3-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("cyc3-a")
            hash_a = spec.dag_hash()
            hash_b = spec["cyc3-b"].dag_hash()
            hash_c = spec["cyc3-c"].dag_hash()

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            # All three should be in the graph
            assert hash_a in graph.nodes
            assert hash_b in graph.nodes
            assert hash_c in graph.nodes

            # None should have ordering children (all run-only)
            assert not graph.parent_to_child.get(hash_a, set())
            assert not graph.parent_to_child.get(hash_b, set())
            assert not graph.parent_to_child.get(hash_c, set())

    def test_build_graph_cycle_with_external_dep(self, repo_builder: RepoBuilder):
        """Test circular run deps with external non-circular dependency."""
        repo_builder.add_package("ext-dep")
        repo_builder.add_package(
            "ext-cyc-a", dependencies=[("ext-cyc-b", "run", None), ("ext-dep", "link", None)]
        )
        repo_builder.add_package(
            "ext-cyc-b", dependencies=[("ext-cyc-a", "run", None), ("ext-dep", "link", None)]
        )

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("ext-cyc-a")
            hash_a = spec.dag_hash()
            hash_b = spec["ext-cyc-b"].dag_hash()
            hash_ext = spec["ext-dep"].dag_hash()

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            # All three should be in the graph
            assert hash_a in graph.nodes
            assert hash_b in graph.nodes
            assert hash_ext in graph.nodes

            # ext-dep should be ordering child of both A and B (LINK deps)
            assert hash_ext in graph.parent_to_child.get(hash_a, set())
            assert hash_ext in graph.parent_to_child.get(hash_b, set())

            # A and B should NOT be ordering children of each other (RUN-only)
            assert hash_b not in graph.parent_to_child.get(hash_a, set())
            assert hash_a not in graph.parent_to_child.get(hash_b, set())

            # ext-dep should have no ordering children
            assert not graph.parent_to_child.get(hash_ext, set())

    def test_build_graph_backward_compatibility(self, repo_builder: RepoBuilder):
        """Test that non-circular specs still work correctly."""
        repo_builder.add_package("normal-b")
        repo_builder.add_package("normal-a", dependencies=[("normal-b", "link", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("normal-a")
            hash_a = spec.dag_hash()
            hash_b = spec["normal-b"].dag_hash()

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            # Both should be in graph
            assert hash_a in graph.nodes
            assert hash_b in graph.nodes

            # A should have B as ordering child
            assert hash_b in graph.parent_to_child.get(hash_a, set())

            # B should have no ordering children
            assert not graph.parent_to_child.get(hash_b, set())

    def test_build_graph_run_only_deps_still_installed(self, repo_builder: RepoBuilder):
        """Verify run-only dependencies are in graph.nodes (will be installed)."""
        repo_builder.add_package("run-dep")
        repo_builder.add_package("with-run-dep", dependencies=[("run-dep", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("with-run-dep")
            hash_main = spec.dag_hash()
            hash_dep = spec["run-dep"].dag_hash()

            db = spack.store.STORE.db
            graph = BuildGraph(
                [spec],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=True,
                database=db,
                tests=False,
            )

            # Both specs must be in nodes (will be installed)
            assert hash_main in graph.nodes
            assert hash_dep in graph.nodes

            # But run-dep should not be in ordering dependencies
            assert hash_dep not in graph.parent_to_child.get(hash_main, set())

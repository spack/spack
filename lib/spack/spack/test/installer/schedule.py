# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the installer.schedule module: BuildGraph and schedule_builds()."""

import sys
import time
from typing import Dict, List, Optional, Set, Tuple

import pytest

import spack.deptypes as dt
import spack.error
import spack.spec
import spack.store
import spack.traverse
from spack.config import Configuration
from spack.database import Database
from spack.installer.base import ExitCode, JobServerBase, NoopJobServer
from spack.installer.schedule import BuildGraph, ScheduleResult, _node_to_roots, schedule_builds
from spack.spec import Spec
from spack.store import Store
from spack.test.conftest import writable
from spack.test.installer.conftest import (
    Script,
    ScriptedLauncher,
    _install,
    _make_concrete,
    _record,
    create_dag,
)

if sys.platform != "win32":
    from spack.installer.posix import PosixJobServer


def install_spec_in_db(spec: Spec, store: Store):
    """Helper to install a spec in the database for testing."""
    prefix = store.layout.path_for_spec(spec)
    spec.set_prefix(prefix)
    # Use the layout to create a proper installation directory structure
    store.layout.create_install_directory(spec)
    store.db.add(spec, explicit=False)


@pytest.fixture
def mock_specs():
    """Create a set of mock specs for testing.

    DAG structure:
        root -> dep1 -> dep2
        root -> dep3
    """
    return create_dag(
        nodes=["root", "dep1", "dep2", "dep3"],
        edges=[
            ("root", "dep1", ("build", "link")),
            ("root", "dep3", ("build", "link")),
            ("dep1", "dep2", ("build", "link")),
        ],
    )


@pytest.fixture
def diamond_dag():
    """Create a diamond-shaped DAG to test shared dependencies.

    DAG structure:
        root -> dep1 -> shared
        root -> dep2 -> shared
    """
    return create_dag(
        nodes=["root", "dep1", "dep2", "shared"],
        edges=[
            ("root", "dep1", ("build", "link")),
            ("root", "dep2", ("build", "link")),
            ("dep1", "shared", ("build", "link")),
            ("dep2", "shared", ("build", "link")),
        ],
    )


@pytest.fixture
def specs_with_build_deps():
    """Create specs with different dependency types for testing build dep filtering.

    DAG structure:
        root -> link_dep (link only)
        root -> build_dep (build only)
        root -> all_dep (build, link, run)
    """
    return create_dag(
        nodes=["root", "link_dep", "build_dep", "all_dep"],
        edges=[
            ("root", "link_dep", "link"),
            ("root", "build_dep", "build"),
            ("root", "all_dep", ("build", "link", "run")),
        ],
    )


@pytest.fixture
def complex_pruning_dag():
    """Create a complex DAG for testing re-parenting logic.

    DAG structure:
        parent1 -> middle -> child1
        parent2 -> middle -> child2

    When 'middle' is installed and pruned, both parent1 and parent2 should
    become direct parents of both child1 and child2 (full Cartesian product).
    """
    return create_dag(
        nodes=["parent1", "parent2", "middle", "child1", "child2"],
        edges=[
            ("parent1", "middle", ("build", "link")),
            ("parent2", "middle", ("build", "link")),
            ("middle", "child1", ("build", "link")),
            ("middle", "child2", ("build", "link")),
        ],
    )


class TestBuildGraph:
    """Tests for the BuildGraph class."""

    def test_basic_graph_construction(self, mock_specs: Dict[str, Spec], temporary_store: Store):
        """Test basic graph construction with all specs to be installed."""
        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # Root should be in roots set
        assert mock_specs["root"].dag_hash() in graph.roots
        # All uninstalled specs should be in nodes
        assert len(graph.nodes) == 4  # root, dep1, dep2, dep3
        # Root should have 2 children (dep1, dep3)
        assert len(graph.parent_to_child[mock_specs["root"].dag_hash()]) == 2

    def test_install_package_only_mode(self, mock_specs: Dict[str, Spec], temporary_store: Store):
        """Test that install_package=False removes root specs from graph."""
        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=False,  # Only install dependencies
            install_deps=True,
            store=temporary_store,
        )

        # Root should NOT be in nodes when install_package=False
        assert mock_specs["root"].dag_hash() not in graph.nodes
        # But its dependencies should be
        assert mock_specs["dep1"].dag_hash() in graph.nodes

    def test_install_deps_false_with_uninstalled_deps(
        self, mock_specs: Dict[str, Spec], temporary_store: Store
    ):
        """Test that install_deps=False raises error when dependencies are not installed."""
        # Should raise error because dependencies are not installed
        with pytest.raises(
            spack.error.InstallError, match="package only mode.*dependency.*not installed"
        ):
            BuildGraph(
                specs=[mock_specs["root"]],
                root_policy="auto",
                dependencies_policy="auto",
                include_build_deps=False,
                install_package=True,
                install_deps=False,  # Don't install dependencies
                store=temporary_store,
            )

    def test_multiple_roots(self, mock_specs: Dict[str, Spec], temporary_store: Store):
        """Test graph construction with multiple root specs."""
        graph = BuildGraph(
            specs=[mock_specs["root"], mock_specs["dep1"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # Both should be in roots
        assert mock_specs["root"].dag_hash() in graph.roots
        assert mock_specs["dep1"].dag_hash() in graph.roots

    def test_parent_child_mappings(self, mock_specs: Dict[str, Spec], temporary_store: Store):
        """Test that parent-child mappings are correctly constructed."""
        spec_root = mock_specs["root"]
        graph = BuildGraph(
            specs=[spec_root],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # Verify parent_to_child and child_to_parent are inverse mappings
        for parent, children in graph.parent_to_child.items():
            for child in children:
                assert child in graph.child_to_parent
                assert parent in graph.child_to_parent[child]

    def test_diamond_dag_with_shared_dependency(
        self, diamond_dag: Dict[str, Spec], temporary_store: Store
    ):
        """Test graph construction with a diamond DAG where a dependency has multiple parents."""
        graph = BuildGraph(
            specs=[diamond_dag["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # Shared dependency should have two parents
        shared_hash = diamond_dag["shared"].dag_hash()
        assert len(graph.child_to_parent[shared_hash]) == 2
        # Both dep1 and dep2 should be parents of shared
        assert diamond_dag["dep1"].dag_hash() in graph.child_to_parent[shared_hash]
        assert diamond_dag["dep2"].dag_hash() in graph.child_to_parent[shared_hash]

    def test_pruning_installed_specs(self, mock_specs: Dict[str, Spec], temporary_store: Store):
        """Test that installed specs are correctly pruned from the graph."""
        # Install dep2 in the database
        dep2 = mock_specs["dep2"]
        install_spec_in_db(dep2, temporary_store)

        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # dep2 should be pruned since it's installed
        assert dep2.dag_hash() not in graph.nodes
        # But dep1 (its parent) should still be in the graph
        assert mock_specs["dep1"].dag_hash() in graph.nodes
        # And dep1 should have no children (since dep2 was pruned)
        assert len(graph.parent_to_child[mock_specs["dep1"].dag_hash()]) == 0

    def test_pruning_with_shared_dependency_partially_installed(
        self, diamond_dag: Dict[str, Spec], temporary_store: Store
    ):
        """Test that pruning a shared dependency correctly updates all parents."""
        # Install the shared dependency
        shared = diamond_dag["shared"]
        install_spec_in_db(shared, temporary_store)
        graph = BuildGraph(
            specs=[diamond_dag["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # Shared should be pruned
        assert shared.dag_hash() not in graph.nodes
        # Both dep1 and dep2 should have no children
        assert len(graph.parent_to_child[diamond_dag["dep1"].dag_hash()]) == 0
        assert len(graph.parent_to_child[diamond_dag["dep2"].dag_hash()]) == 0

    def test_overwrite_set_prevents_pruning(
        self, mock_specs: Dict[str, Spec], temporary_store: Store
    ):
        """Test that specs in overwrite_set are not pruned even if installed."""
        # Install dep2 in the database
        dep2 = mock_specs["dep2"]
        install_spec_in_db(dep2, temporary_store)

        # Create graph with dep2 in the overwrite set
        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
            overwrite_set={dep2.dag_hash()},
        )

        # dep2 should NOT be pruned since it's in overwrite_set
        assert dep2.dag_hash() in graph.nodes
        # dep1 should still have dep2 as a child
        assert dep2.dag_hash() in graph.parent_to_child[mock_specs["dep1"].dag_hash()]
        # dep2 should have dep1 as a parent
        assert mock_specs["dep1"].dag_hash() in graph.child_to_parent[dep2.dag_hash()]

    def test_installed_root_excludes_build_deps_even_when_requested(
        self, specs_with_build_deps: Dict[str, Spec], temporary_store: Store
    ):
        """Test that installed root specs never include build deps, even with
        include_build_deps=True."""
        root = specs_with_build_deps["root"]
        install_spec_in_db(root, temporary_store)

        graph = BuildGraph(
            specs=[root],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=True,  # Should be ignored for installed root
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # build_dep should NOT be in the graph (installed root never needs build deps)
        assert specs_with_build_deps["build_dep"].dag_hash() not in graph.nodes
        # link_dep and all_dep should be in the graph (link/run deps)
        assert specs_with_build_deps["link_dep"].dag_hash() in graph.nodes
        assert specs_with_build_deps["all_dep"].dag_hash() in graph.nodes

    def test_cache_only_excludes_build_deps(
        self, specs_with_build_deps: Dict[str, Spec], temporary_store: Store
    ):
        """Test that cache_only policy excludes build deps when include_build_deps=False."""
        specs = [specs_with_build_deps["root"]]
        graph = BuildGraph(
            specs=specs,
            root_policy="cache_only",
            dependencies_policy="auto",
            include_build_deps=False,  # exclude build deps when possible
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        assert specs_with_build_deps["build_dep"].dag_hash() not in graph.nodes
        assert specs_with_build_deps["link_dep"].dag_hash() in graph.nodes
        assert specs_with_build_deps["all_dep"].dag_hash() in graph.nodes

        # Verify that the entire graph has a prefix assigned, which avoids that the subprocess has
        # to obtain a read lock on the database.
        for s in spack.traverse.traverse_nodes(specs):
            assert s._prefix is not None

    def test_cache_only_includes_build_deps_when_requested(
        self, specs_with_build_deps: Dict[str, Spec], temporary_store: Store
    ):
        """Test that cache_only policy includes build deps when include_build_deps=True."""
        graph = BuildGraph(
            specs=[specs_with_build_deps["root"]],
            root_policy="cache_only",
            dependencies_policy="cache_only",
            include_build_deps=True,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # All dependencies should be in the graph, including build_dep
        assert specs_with_build_deps["build_dep"].dag_hash() in graph.nodes
        assert specs_with_build_deps["link_dep"].dag_hash() in graph.nodes
        assert specs_with_build_deps["all_dep"].dag_hash() in graph.nodes

    def test_install_deps_false_with_all_deps_installed(
        self, mock_specs: Dict[str, Spec], temporary_store: Store
    ):
        """Test successful package-only install when all dependencies are already installed."""
        # Install all dependencies
        for dep_name in ["dep1", "dep2", "dep3"]:
            install_spec_in_db(mock_specs[dep_name], temporary_store)

        # Should succeed since all dependencies are installed
        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=False,
            store=temporary_store,
        )

        # Only the root should be in the graph
        assert len(graph.nodes) == 1
        assert mock_specs["root"].dag_hash() in graph.nodes
        # Root should have no children (all deps pruned)
        assert len(graph.parent_to_child.get(mock_specs["root"].dag_hash(), [])) == 0

    def test_pruning_creates_cartesian_product_of_connections(
        self, complex_pruning_dag: Dict[str, Spec], temporary_store: Store
    ):
        """Test that pruning creates full Cartesian product of parent-child connections.

        When a node with multiple parents and multiple children is pruned,
        all parents should be connected to all children (parents x children).

        DAG structure:
            parent1 -> middle -> child1
            parent2 -> middle -> child2

        After pruning 'middle':
            parent1 -> child1
            parent1 -> child2
            parent2 -> child1
            parent2 -> child2
        """
        # Install the middle node
        middle = complex_pruning_dag["middle"]
        install_spec_in_db(middle, temporary_store)

        # Use parent1 as the root to build the graph
        graph = BuildGraph(
            specs=[complex_pruning_dag["parent1"], complex_pruning_dag["parent2"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        parent1_hash = complex_pruning_dag["parent1"].dag_hash()
        parent2_hash = complex_pruning_dag["parent2"].dag_hash()
        middle_hash = middle.dag_hash()
        child1_hash = complex_pruning_dag["child1"].dag_hash()
        child2_hash = complex_pruning_dag["child2"].dag_hash()

        # middle should be pruned since it's installed
        assert middle_hash not in graph.nodes

        # All other nodes should be in the graph
        assert parent1_hash in graph.nodes
        assert parent2_hash in graph.nodes
        assert child1_hash in graph.nodes
        assert child2_hash in graph.nodes

        # Verify full Cartesian product: each parent should be connected to each child
        # parent1 -> child1, child2
        assert child1_hash in graph.parent_to_child[parent1_hash]
        assert child2_hash in graph.parent_to_child[parent1_hash]

        # parent2 -> child1, child2
        assert child1_hash in graph.parent_to_child[parent2_hash]
        assert child2_hash in graph.parent_to_child[parent2_hash]

        # Verify reverse mapping: each child should have both parents
        # child1 <- parent1, parent2
        assert parent1_hash in graph.child_to_parent[child1_hash]
        assert parent2_hash in graph.child_to_parent[child1_hash]

        # child2 <- parent1, parent2
        assert parent1_hash in graph.child_to_parent[child2_hash]
        assert parent2_hash in graph.child_to_parent[child2_hash]

        # middle should not appear in any parent-child relationships
        assert middle_hash not in graph.parent_to_child
        assert middle_hash not in graph.child_to_parent

    def test_empty_graph_all_specs_installed(
        self, mock_specs: Dict[str, Spec], temporary_store: Store
    ):
        """Test that the graph is empty when all specs are already installed."""
        # Install all specs in the DAG
        for spec_name in ["root", "dep1", "dep2", "dep3"]:
            install_spec_in_db(mock_specs[spec_name], temporary_store)

        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        # All nodes should be pruned, resulting in an empty graph
        assert len(graph.nodes) == 0
        assert len(graph.parent_to_child) == 0
        assert len(graph.child_to_parent) == 0

    def test_empty_graph_install_package_false_all_deps_installed(
        self, mock_specs: Dict[str, Spec], temporary_store: Store
    ):
        """Test empty graph when install_package=False and all dependencies are installed."""
        # Install all dependencies (but not the root)
        for dep_name in ["dep1", "dep2", "dep3"]:
            install_spec_in_db(mock_specs[dep_name], temporary_store)

        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=False,  # Don't install the root
            install_deps=True,
            store=temporary_store,
        )

        # Root is pruned because install_package=False
        # Dependencies are pruned because they're installed
        # Result: empty graph
        assert len(graph.nodes) == 0
        assert len(graph.parent_to_child) == 0
        assert len(graph.child_to_parent) == 0

    def test_pruning_leaf_node(self, mock_specs: Dict[str, Spec], temporary_store: Store):
        """Test that pruning a leaf node (no children) works correctly.

        This ensures the pruning logic handles the boundary condition where
        a node has no children to re-wire.
        """
        # Install dep2, which is a leaf node (no children)
        dep2 = mock_specs["dep2"]
        install_spec_in_db(dep2, temporary_store)

        graph = BuildGraph(
            specs=[mock_specs["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

        dep2_hash = dep2.dag_hash()
        dep1_hash = mock_specs["dep1"].dag_hash()

        # dep2 should be pruned
        assert dep2_hash not in graph.nodes
        # dep1 (parent of dep2) should have no children now
        assert len(graph.parent_to_child[dep1_hash]) == 0
        # dep2 should not appear in any mappings
        assert dep2_hash not in graph.parent_to_child
        assert dep2_hash not in graph.child_to_parent

    def test_pruning_root_node_with_install_package_false(
        self, mock_specs: Dict[str, Spec], temporary_store: Store
    ):
        """Test that pruning a root node (no parents in the context) works correctly.

        When install_package=False, root nodes are marked for pruning. This ensures
        the pruning logic handles the boundary condition where a node has no parents.
        """
        graph = BuildGraph(
            specs=[mock_specs["dep1"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=False,  # Prune the root
            install_deps=True,
            store=temporary_store,
        )

        dep1_hash = mock_specs["dep1"].dag_hash()
        dep2_hash = mock_specs["dep2"].dag_hash()

        # dep1 should be pruned (it's the root and install_package=False)
        assert dep1_hash not in graph.nodes
        # dep2 (child of dep1) should still be in the graph
        assert dep2_hash in graph.nodes
        # dep2 should have no parents now (its only parent was pruned)
        assert not graph.child_to_parent.get(dep2_hash)
        # dep1 should not appear in any mappings
        assert dep1_hash not in graph.parent_to_child
        assert dep1_hash not in graph.child_to_parent


@pytest.fixture
def specs_with_test_deps():
    """Create specs with test-typed dependencies.

    DAG structure:
        root -> dep (link) + test_dep (test)
        dep -> dep_test_dep (test)
    """
    return create_dag(
        nodes=["root", "dep", "test_dep", "dep_test_dep"],
        edges=[
            ("root", "dep", ("build", "link")),
            ("root", "test_dep", "test"),
            ("dep", "dep_test_dep", "test"),
        ],
    )


class TestBuildGraphTestDeps:
    """Tests for BuildGraph handling of TEST-typed dependencies."""

    def test_tests_false_excludes_test_deps(
        self, specs_with_test_deps: Dict[str, Spec], temporary_store: Store
    ):
        """Test that tests=False excludes TEST-typed dependencies."""
        graph = BuildGraph(
            specs=[specs_with_test_deps["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=True,
            install_package=True,
            install_deps=True,
            store=temporary_store,
            tests=False,
        )

        assert specs_with_test_deps["dep"].dag_hash() in graph.nodes
        assert specs_with_test_deps["test_dep"].dag_hash() not in graph.nodes
        assert specs_with_test_deps["dep_test_dep"].dag_hash() not in graph.nodes

    def test_tests_root_includes_test_deps_for_root(
        self, specs_with_test_deps: Dict[str, Spec], temporary_store: Store
    ):
        """Test that tests=[root_name] includes test deps only for the root package."""
        graph = BuildGraph(
            specs=[specs_with_test_deps["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=True,
            install_package=True,
            install_deps=True,
            store=temporary_store,
            tests=["root"],
        )

        assert specs_with_test_deps["dep"].dag_hash() in graph.nodes
        assert specs_with_test_deps["test_dep"].dag_hash() in graph.nodes
        # dep's test dep is NOT included because tests=["root"] only applies to "root"
        assert specs_with_test_deps["dep_test_dep"].dag_hash() not in graph.nodes

    def test_tests_all_includes_test_deps_for_all(
        self, specs_with_test_deps: Dict[str, Spec], temporary_store: Store
    ):
        """Test that tests=True includes TEST-typed deps for all packages."""
        graph = BuildGraph(
            specs=[specs_with_test_deps["root"]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=True,
            install_package=True,
            install_deps=True,
            store=temporary_store,
            tests=True,
        )

        assert specs_with_test_deps["dep"].dag_hash() in graph.nodes
        assert specs_with_test_deps["test_dep"].dag_hash() in graph.nodes
        assert specs_with_test_deps["dep_test_dep"].dag_hash() in graph.nodes

    def test_mark_explicit_spec_excludes_build_only_deps(
        self, specs_with_build_deps: Dict[str, Spec], temporary_store: Store
    ):
        """An installed-implicit spec in explicit_set should only traverse link/run deps,
        not build-only deps."""
        root = specs_with_build_deps["root"]
        install_spec_in_db(root, temporary_store)
        assert temporary_store.db._data[root.dag_hash()].explicit is False
        graph = BuildGraph(
            specs=[root],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=True,
            install_package=True,
            install_deps=True,
            store=temporary_store,
            explicit_set={root.dag_hash()},
        )
        # root should be in graph (not pruned) because it needs to be marked explicit.
        assert root.dag_hash() in graph.nodes
        # build-only dep should NOT be pulled in since root is already installed.
        assert specs_with_build_deps["build_dep"].dag_hash() not in graph.nodes


class TestExpandBuildDeps:
    """Tests for BuildGraph.expand_build_deps after a binary cache miss."""

    def _make_graph(self, specs, root, temporary_store):
        """Helper to create a BuildGraph with include_build_deps=False (auto policy)."""
        return BuildGraph(
            specs=[specs[root]],
            root_policy="auto",
            dependencies_policy="auto",
            include_build_deps=False,
            install_package=True,
            install_deps=True,
            store=temporary_store,
        )

    def _expand(self, graph, dag_hash, pending, db, tests=False):
        """Call expand_build_deps under the DB read lock (as the real caller would)."""
        with db.read_transaction():
            return graph.expand_build_deps([dag_hash], pending, db, tests)

    def test_expand_build_deps_adds_missing_deps(self, temporary_store: Store):
        """A --build--> C --link--> D, A --link--> B.
        Initial graph (auto, no build deps): A, B.
        After expand: C, D added. D is leaf -> in pending_builds."""
        specs = create_dag(
            nodes=["a", "b", "c", "d"],
            edges=[("a", "b", "link"), ("a", "c", "build"), ("c", "d", "link")],
        )
        graph = self._make_graph(specs, "a", temporary_store)
        assert specs["c"].dag_hash() not in graph.nodes
        assert specs["d"].dag_hash() not in graph.nodes

        pending: List[str] = []
        newly_added = self._expand(graph, specs["a"].dag_hash(), pending, temporary_store.db)

        assert specs["c"].dag_hash() in newly_added
        assert specs["d"].dag_hash() in newly_added
        assert specs["c"].dag_hash() in graph.nodes
        assert specs["d"].dag_hash() in graph.nodes
        # D is a leaf (no children), so it should be enqueued
        assert specs["d"].dag_hash() in pending
        # C waits on D, so it should NOT be enqueued
        assert specs["c"].dag_hash() not in pending

    def test_expand_build_deps_shared_dep_already_in_graph(self, temporary_store: Store):
        """A --link--> B, A --build--> C --link--> B.
        Initial graph: A, B. After expand: C added with edge C->B."""
        specs = create_dag(
            nodes=["a", "b", "c"],
            edges=[("a", "b", "link"), ("a", "c", "build"), ("c", "b", "link")],
        )
        graph = self._make_graph(specs, "a", temporary_store)
        assert specs["b"].dag_hash() in graph.nodes
        assert specs["c"].dag_hash() not in graph.nodes

        pending: List[str] = []
        newly_added = self._expand(graph, specs["a"].dag_hash(), pending, temporary_store.db)

        assert specs["c"].dag_hash() in newly_added
        # C depends on B, so C->B edge should exist
        assert specs["b"].dag_hash() in graph.parent_to_child[specs["c"].dag_hash()]
        # B should list C as a parent
        assert specs["c"].dag_hash() in graph.child_to_parent[specs["b"].dag_hash()]
        # C waits on B, so not in pending
        assert specs["c"].dag_hash() not in pending

    def test_expand_build_deps_skips_installed_in_db(self, temporary_store: Store):
        """A --build--> C --link--> D. D installed in DB.
        After expand: C added, D NOT added. No edge C->D. C in pending."""
        specs = create_dag(nodes=["a", "c", "d"], edges=[("a", "c", "build"), ("c", "d", "link")])
        install_spec_in_db(specs["d"], temporary_store)
        graph = self._make_graph(specs, "a", temporary_store)

        pending: List[str] = []
        newly_added = self._expand(graph, specs["a"].dag_hash(), pending, temporary_store.db)

        assert specs["c"].dag_hash() in newly_added
        assert specs["d"].dag_hash() not in newly_added
        assert specs["d"].dag_hash() not in graph.nodes
        # No edge from C to D (installed dep)
        assert specs["d"].dag_hash() not in graph.parent_to_child.get(specs["c"].dag_hash(), set())
        # C has no uninstalled children, so it should be enqueued
        assert specs["c"].dag_hash() in pending

    def test_expand_build_deps_skips_installed_in_session(self, temporary_store: Store):
        """Same as above, but D in graph.done instead of DB."""
        specs = create_dag(nodes=["a", "c", "d"], edges=[("a", "c", "build"), ("c", "d", "link")])
        graph = self._make_graph(specs, "a", temporary_store)
        graph.done.add(specs["d"].dag_hash())

        pending: List[str] = []
        newly_added = self._expand(graph, specs["a"].dag_hash(), pending, temporary_store.db)

        assert specs["c"].dag_hash() in newly_added
        assert specs["d"].dag_hash() not in newly_added
        assert specs["d"].dag_hash() not in graph.nodes
        assert specs["c"].dag_hash() in pending

    def test_expand_build_deps_reenqueues_original_when_all_deps_installed(
        self, temporary_store: Store
    ):
        """A --build--> C. C installed in DB.
        After expand: C NOT added. A re-enqueued (no uninstalled children)."""
        specs = create_dag(nodes=["a", "c"], edges=[("a", "c", "build")])
        install_spec_in_db(specs["c"], temporary_store)
        graph = self._make_graph(specs, "a", temporary_store)

        pending: List[str] = []
        newly_added = self._expand(graph, specs["a"].dag_hash(), pending, temporary_store.db)

        assert len(newly_added) == 0
        assert specs["a"].dag_hash() in pending

    def test_expand_build_deps_no_deadlock_on_installed_dep(self, temporary_store: Store):
        """A --build--> C --link--> D. D installed in DB.
        No edge C->D in parent_to_child. C in pending."""
        specs = create_dag(nodes=["a", "c", "d"], edges=[("a", "c", "build"), ("c", "d", "link")])
        install_spec_in_db(specs["d"], temporary_store)
        graph = self._make_graph(specs, "a", temporary_store)

        pending: List[str] = []
        self._expand(graph, specs["a"].dag_hash(), pending, temporary_store.db)

        # No edge from C to D: installed deps get no edge, otherwise C is never scheduled
        assert specs["d"].dag_hash() not in graph.parent_to_child.get(specs["c"].dag_hash(), set())
        assert specs["c"].dag_hash() in pending

    def test_has_unexpanded_build_deps_true(self, temporary_store: Store):
        """A --build--> C, A --link--> B. With include_build_deps=False, C is not in the graph,
        so has_unexpanded_build_deps returns True."""
        specs = create_dag(nodes=["a", "b", "c"], edges=[("a", "b", "link"), ("a", "c", "build")])
        graph = self._make_graph(specs, "a", temporary_store)
        assert graph.has_unexpanded_build_deps(specs["a"].dag_hash())

    def test_has_unexpanded_build_deps_false_shared(self, temporary_store: Store):
        """A --(build,link)--> B. B is already in graph as link dep,
        so has_unexpanded_build_deps returns False."""
        specs = create_dag(nodes=["a", "b"], edges=[("a", "b", ("build", "link"))])
        graph = self._make_graph(specs, "a", temporary_store)
        assert not graph.has_unexpanded_build_deps(specs["a"].dag_hash())

    def test_expand_build_deps_does_not_mark_in_graph_spec_as_done(self, temporary_store: Store):
        """A --link--> B, A --link--> C, B --build--> C.
        C is in the graph (link dep of A) and installed in DB (simulating an overwrite build
        in progress). Expanding B's build deps should add edge B->C and NOT mark C as done."""
        specs = create_dag(
            nodes=["a", "b", "c"],
            edges=[("a", "b", "link"), ("a", "c", "link"), ("b", "c", "build")],
        )
        graph = self._make_graph(specs, "a", temporary_store)
        # C should be in graph as a link dep of A
        assert specs["c"].dag_hash() in graph.nodes

        # Simulate overwrite: install C in DB after graph creation
        install_spec_in_db(specs["c"], temporary_store)

        pending: List[str] = []
        self._expand(graph, specs["b"].dag_hash(), pending, temporary_store.db)

        c_hash = specs["c"].dag_hash()
        b_hash = specs["b"].dag_hash()
        # C must NOT be marked as done (it's still being overwrite-built)
        assert c_hash not in graph.done
        # Edge B->C must exist
        assert c_hash in graph.parent_to_child[b_hash]
        assert b_hash in graph.child_to_parent[c_hash]
        # B should NOT be in pending (it still waits on C)
        assert b_hash not in pending


class _FakeBuildGraph:
    """Minimal stand-in for BuildGraph in schedule_builds unit tests.

    Provides the two interface points that schedule_builds calls:
      - .nodes  (dict: dag_hash -> Spec)
      - .enqueue_parents(dag_hash, pending_builds)
    """

    def __init__(self, specs):
        self.nodes = {spec.dag_hash(): spec for spec in specs}

    def enqueue_parents(self, dag_hash, pending_builds):
        """Remove dag_hash from nodes; no parents in these simple unit tests."""
        self.nodes.pop(dag_hash, None)


def _schedule(
    pending: List[str],
    build_graph,
    store,
    jobserver: Optional[JobServerBase] = None,
    overwrite: Optional[Set[str]] = None,
    overwrite_time: float = 0.0,
    capacity: int = 2,
    needs_jobserver_token: bool = False,
    explicit: Optional[Set[str]] = None,
) -> ScheduleResult:
    """Call schedule_builds() with inert defaults, so tests spell out only what they are about."""
    return schedule_builds(
        pending,
        build_graph,
        store,
        overwrite=overwrite or set(),
        overwrite_time=overwrite_time,
        capacity=capacity,
        needs_jobserver_token=needs_jobserver_token,
        jobserver=jobserver or NoopJobServer(num_jobs=2),
        explicit=explicit or set(),
    )


class TestScheduleBuilds:
    """Unit tests for the module-level schedule_builds() function."""

    def _make_spec(self, name):
        """Return a minimal concrete spec suitable for locking and DB queries."""
        spec = spack.spec.Spec(name)
        spec._mark_concrete()
        return spec

    def _mark_installed(self, spec, store):
        """Create the install directory structure and register the spec in the DB as installed."""
        store.layout.create_install_directory(spec)
        store.db.add(spec, explicit=True)

    def test_not_installed_no_running_starts_build(self, temporary_store, mock_packages):
        """A fresh spec with no running builds is added to to_start."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert not result.blocked
        assert len(result.to_start) == 1
        assert result.to_start[0][0] == spec.dag_hash()
        assert not result.newly_installed
        assert not pending  # removed from the pending list
        for _, lock in result.to_start:
            lock.release_write()

    def test_already_installed_yields_newly_installed(self, temporary_store, mock_packages):
        """A spec already in the DB is returned in newly_installed, not in to_start."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert not result.blocked
        assert not result.to_start
        assert len(result.newly_installed) == 1
        assert result.newly_installed[0][0] == spec.dag_hash()
        assert not pending  # removed from the pending list
        for _, _, lock in result.newly_installed:
            lock.release_read()

    @pytest.mark.not_on_windows("Windows has no POSIX jobserver, only NoopJobServer")
    def test_no_jobserver_token_returns_empty(self, temporary_store, mock_packages):
        """When has_running_builds=True and no token is available, nothing is started."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        # num_jobs=1 writes 0 tokens to the FIFO. Only the implicit token exists.
        jobserver = PosixJobServer(num_jobs=1, makeflags="")
        try:
            result = _schedule(
                pending,
                _FakeBuildGraph([spec]),
                temporary_store,
                jobserver=jobserver,
                needs_jobserver_token=True,
            )
            assert not result.blocked
            assert not result.to_start
            assert not result.newly_installed
            assert len(pending) == 1
        finally:
            jobserver.close()

    def test_all_locked_returns_blocked(self, temporary_store, mock_packages, monkeypatch):
        """When all pending specs are locked externally, blocked_on_locks is True."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        # Pre-register the lock in the prefix_locker cache, then patch try_acquire to fail.
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        monkeypatch.setattr(lock, "try_acquire_read", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert result.blocked
        assert not result.to_start
        assert not result.newly_installed
        assert len(pending) == 1

    def test_overwrite_installed_spec_is_started(self, temporary_store, mock_packages):
        """A spec in the overwrite set is scheduled even when already installed."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        result = _schedule(
            pending,
            _FakeBuildGraph([spec]),
            temporary_store,
            overwrite={spec.dag_hash()},
            overwrite_time=time.time() + 100,
        )
        assert not result.blocked
        assert len(result.to_start) == 1
        assert result.to_start[0][0] == spec.dag_hash()
        assert not result.newly_installed
        for _, lock in result.to_start:
            lock.release_write()

    def test_mixed_locked_unlocked(self, temporary_store, mock_packages, monkeypatch):
        """Only the unlocked spec enters to_start when one spec is externally locked."""
        spec_a = self._make_spec("trivial-install-test-package")
        spec_b = self._make_spec("trivial-smoke-test")
        pending = [spec_a.dag_hash(), spec_b.dag_hash()]
        # Patch spec_a's lock to always fail, simulating an external write lock.
        lock_a = temporary_store.prefix_locker.lock(spec_a)
        monkeypatch.setattr(lock_a, "try_acquire_write", lambda: False)
        monkeypatch.setattr(lock_a, "try_acquire_read", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec_a, spec_b]), temporary_store)
        assert not result.blocked  # spec_b was schedulable
        started_hashes = {h for h, _ in result.to_start}
        assert spec_b.dag_hash() in started_hashes
        assert spec_a.dag_hash() not in started_hashes
        assert not result.newly_installed
        for _, lock in result.to_start:
            lock.release_write()

    def test_write_locked_read_locked_installed_yields_newly_installed(
        self, temporary_store, mock_packages, monkeypatch
    ):
        """Write lock fails but read lock succeeds and spec is installed: treated as done.

        Simulates the case where another process finished building and downgraded its write lock
        to a read lock. The spec should appear in newly_installed. blocked remains True because no
        write lock was obtained, preventing the jobserver from firing unnecessarily.
        """
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert result.blocked  # no write lock was obtained; jobserver should not fire
        assert not result.to_start
        assert len(result.newly_installed) == 1
        dag_hash, installed_spec, lock = result.newly_installed[0]
        assert dag_hash == spec.dag_hash()
        assert installed_spec == spec
        assert not pending  # spec was removed from pending
        lock.release_read()

    def test_write_locked_read_locked_not_installed_still_blocked(
        self, temporary_store, mock_packages, monkeypatch
    ):
        """Write lock fails, read lock succeeds, but spec is not in DB: retry later.

        Simulates the case where a concurrent process was killed mid-build. The read lock is
        released and the spec stays in pending; blocked should remain True.
        """
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert result.blocked
        assert not result.to_start
        assert not result.newly_installed
        assert pending == [spec.dag_hash()]  # spec stays in pending for retry

    def test_overwrite_handled_by_concurrent_process(self, temporary_store, mock_packages):
        """When a spec in overwrite was installed AFTER overwrite_time, another process did it."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)  # installation_time = now()
        pending = [spec.dag_hash()]
        # the default overwrite_time=0.0 is earlier than now()
        result = _schedule(
            pending, _FakeBuildGraph([spec]), temporary_store, overwrite={spec.dag_hash()}
        )
        assert not result.blocked
        assert not result.to_start
        assert len(result.newly_installed) == 1
        assert result.newly_installed[0][0] == spec.dag_hash()
        for _, _, lock in result.newly_installed:
            lock.release_read()

    def test_installed_implicit_explicit_set_produces_db_update(
        self, temporary_store, mock_packages
    ):
        """An installed-implicit spec in explicit set produces a DbUpdate."""
        spec = self._make_spec("trivial-install-test-package")
        temporary_store.layout.create_install_directory(spec)
        temporary_store.db.add(spec, explicit=False)
        pending = [spec.dag_hash()]
        result = _schedule(
            pending, _FakeBuildGraph([spec]), temporary_store, explicit={spec.dag_hash()}
        )
        assert len(result.to_mark_explicit) == 1
        assert result.to_mark_explicit[0].spec is spec
        assert len(result.newly_installed) == 1
        for _, _, lock in result.newly_installed:
            lock.release_read()

    def test_missing_in_upstream_is_installed_locally(
        self, upstream_and_downstream_db: Tuple[Database, Database], mock_packages
    ):
        """A spec that is referenced but not installed in an upstream database is scheduled for
        a local build, with its prefix repointed to the local store."""
        upstream_db, downstream_db = upstream_and_downstream_db
        dep = self._make_spec("dependency-install")
        parent = spack.spec.Spec("dependent-install")
        parent._add_dependency(dep, depflag=dt.BUILD, virtuals=())
        parent._mark_concrete()

        # Register both specs in the upstream, then uninstall the dep: its record is kept as
        # uninstalled because the parent still references it.
        with writable(upstream_db):
            upstream_db.add(parent, explicit=True)
            upstream_db.remove(dep)

        # Create a Store for schedule_builds based on the downstream database.
        local_store = spack.store.Store(downstream_db.root, upstreams=[upstream_db])
        upstream, record = local_store.db.query_by_spec_hash(dep.dag_hash())
        assert upstream and record is not None and not record.installed

        # Like BuildGraph, start out with the prefix from the upstream record.
        assert upstream_db.layout
        dep.set_prefix(upstream_db.layout.path_for_spec(dep))

        result = _schedule([dep.dag_hash()], _FakeBuildGraph([dep]), local_store)
        assert not result.blocked
        assert [dag_hash for dag_hash, _ in result.to_start] == [dep.dag_hash()]
        # The prefix was repointed from the upstream to the local store.
        assert dep.prefix == local_store.layout.path_for_spec(dep)

        # Cleanup
        for _, lock in result.to_start:
            lock.release_write()

    def test_overwrite_prefix_mismatch_raises(self, temporary_store, mock_packages):
        """An overwrite install cannot proceed when the spec prefix differs from the DB path."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        spec.set_prefix("/some/other/prefix")
        with pytest.raises(spack.error.InstallError, match="Prefix mismatch in overwrite"):
            _schedule(
                [spec.dag_hash()],
                _FakeBuildGraph([spec]),
                temporary_store,
                overwrite={spec.dag_hash()},
                overwrite_time=time.time() + 100,
            )

    def test_prefix_collision_raises(self, temporary_store, mock_packages):
        """A spec cannot be scheduled into a prefix already occupied by another spec."""
        installed = self._make_spec("trivial-install-test-package")
        self._mark_installed(installed, temporary_store)
        colliding = self._make_spec("trivial-smoke-test")
        colliding.set_prefix(temporary_store.layout.path_for_spec(installed))
        with pytest.raises(spack.error.InstallError, match="already exists"):
            _schedule([colliding.dag_hash()], _FakeBuildGraph([colliding]), temporary_store)


def test_cache_miss_expands_build_deps(
    temporary_store: Store, mock_packages, mutable_config: Configuration, tmp_path
):
    """A cache miss on a root with unexpanded build deps schedules those deps (growing the UI
    total) and retries the root as source_only."""
    mutable_config.set(
        "mirrors", {"local": {"url": (tmp_path / "mirror").as_uri(), "binary": True}}
    )
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep], depflag=dt.BUILD)
    launcher = ScriptedLauncher(
        {root.name: [Script(exitcode=ExitCode.BUILD_CACHE_MISS), Script()], dep.name: Script()}
    )
    ui = _install(launcher, root)

    assert [(r.spec.name, r.install_policy) for r in launcher.requests] == [
        (root.name, "cache_only"),
        (dep.name, "cache_only"),
        (root.name, "source_only"),
    ]
    assert ("total_increased", 1) in ui.events
    assert _record(temporary_store, dep) and _record(temporary_store, root)


def test_nodes_to_roots():
    """Independent roots don't reach each other's exclusive nodes."""
    # A - B and C - D are disconnected graphs, A, B and C are "roots".
    specs = create_dag(nodes=["A", "B", "C", "D"], edges=[("A", "B", "all"), ("C", "D", "all")])
    a, b, c, d = specs["A"], specs["B"], specs["C"], specs["D"]
    node_to_roots = _node_to_roots([a, b, c])
    assert node_to_roots[a.dag_hash()] == frozenset([a.dag_hash()])
    assert node_to_roots[b.dag_hash()] == frozenset([a.dag_hash(), b.dag_hash()])
    assert node_to_roots[c.dag_hash()] == frozenset([c.dag_hash()])
    assert node_to_roots[d.dag_hash()] == frozenset([c.dag_hash()])


def test_nodes_to_roots_shared_dependency():
    """A dependency shared by two roots is attributed to both."""
    specs = create_dag(nodes=["A", "B", "C"], edges=[("A", "C", "all"), ("B", "C", "all")])
    a, b, c = specs["A"], specs["B"], specs["C"]
    node_to_roots = _node_to_roots([a, b])
    assert node_to_roots[a.dag_hash()] == frozenset([a.dag_hash()])
    assert node_to_roots[b.dag_hash()] == frozenset([b.dag_hash()])
    assert node_to_roots[c.dag_hash()] == frozenset([a.dag_hash(), b.dag_hash()])


def test_expand_build_deps_source_only_includes_nested_build_deps(temporary_store):
    """When dependencies_policy is source_only, expand_build_deps must include BUILD deps of
    dynamically added specs, not just LINK|RUN. Otherwise those specs attempt to build from source
    without their build tools in the graph."""
    # root --[build]--> build_tool --[build]--> nested_build_tool
    #                              --[link]-->  lib_dep
    specs = create_dag(
        nodes=["root", "build_tool", "nested_build_tool", "lib_dep"],
        edges=[
            ("root", "build_tool", "build"),
            ("build_tool", "nested_build_tool", "build"),
            ("build_tool", "lib_dep", "link"),
        ],
    )
    root = specs["root"]
    for s in specs.values():
        s._mark_concrete()

    # Construct a BuildGraph with root_policy="auto" so root's build deps are deferred.
    build_graph = BuildGraph(
        specs=[root],
        root_policy="auto",
        dependencies_policy="source_only",
        include_build_deps=False,
        install_package=True,
        install_deps=True,
        store=temporary_store,
    )

    # The initial graph should contain only root (build deps deferred for "auto" policy).
    assert root.dag_hash() in build_graph.nodes
    assert specs["build_tool"].dag_hash() not in build_graph.nodes

    # Simulate a cache miss: expand build deps for root.
    pending = []
    with temporary_store.db.read_transaction():
        newly_added = build_graph.expand_build_deps(
            [root.dag_hash()], pending, temporary_store.db, dependencies_policy="source_only"
        )

    added_hashes = set(newly_added)

    # build_tool must be added (direct BUILD dep of root)
    assert specs["build_tool"].dag_hash() in added_hashes

    # lib_dep must be added (LINK dep of build_tool)
    assert specs["lib_dep"].dag_hash() in added_hashes

    # nested_build_tool must also be added (BUILD dep of build_tool). This is the bug: without the
    # fix, expand_build_deps only traverses LINK|RUN, so nested_build_tool is missing.
    assert specs["nested_build_tool"].dag_hash() in added_hashes

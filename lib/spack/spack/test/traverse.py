# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.traverse as traverse
from spack.spec import Spec


def create_dag(nodes, edges):
    """
    Arguments:
        nodes: list of package names
        edges: list of tuples (from, to, deptype)
    Returns:
        dict: mapping from package name to abstract Spec with proper deps.
    """
    specs = {name: Spec(name) for name in nodes}
    for parent, child, deptype in edges:
        specs[parent].add_dependency_edge(specs[child], deptype)
    return specs


@pytest.fixture()
def abstract_specs_dtuse():
    nodes = [
        "dtbuild1",
        "dtbuild2",
        "dtbuild3",
        "dtlink1",
        "dtlink2",
        "dtlink3",
        "dtlink4",
        "dtlink5",
        "dtrun1",
        "dtrun2",
        "dtrun3",
        "dttop",
        "dtuse",
    ]
    edges = [
        ("dtbuild1", "dtbuild2", ("build")),
        ("dtbuild1", "dtlink2", ("build", "link")),
        ("dtbuild1", "dtrun2", ("run")),
        ("dtlink1", "dtlink3", ("build", "link")),
        ("dtlink3", "dtbuild2", ("build")),
        ("dtlink3", "dtlink4", ("build", "link")),
        ("dtrun1", "dtlink5", ("build", "link")),
        ("dtrun1", "dtrun3", ("run")),
        ("dtrun3", "dtbuild3", ("build")),
        ("dttop", "dtbuild1", ("build",)),
        ("dttop", "dtlink1", ("build", "link")),
        ("dttop", "dtrun1", ("run")),
        ("dtuse", "dttop", ("build", "link")),
    ]
    return create_dag(nodes, edges)


@pytest.fixture()
def abstract_specs_dt_diamond():
    nodes = ["dt-diamond", "dt-diamond-left", "dt-diamond-right", "dt-diamond-bottom"]
    edges = [
        ("dt-diamond", "dt-diamond-left", ("build", "link")),
        ("dt-diamond", "dt-diamond-right", ("build", "link")),
        ("dt-diamond-right", "dt-diamond-bottom", ("build", "link", "run")),
        ("dt-diamond-left", "dt-diamond-bottom", ("build")),
    ]
    return create_dag(nodes, edges)


@pytest.fixture()
def abstract_specs_chain():
    # Chain a -> b -> c -> d with skip connections
    # from a -> c and a -> d.
    nodes = ["chain-a", "chain-b", "chain-c", "chain-d"]
    edges = [
        ("chain-a", "chain-b", ("build", "link")),
        ("chain-b", "chain-c", ("build", "link")),
        ("chain-c", "chain-d", ("build", "link")),
        ("chain-a", "chain-c", ("build", "link")),
        ("chain-a", "chain-d", ("build", "link")),
    ]
    return create_dag(nodes, edges)


def test_breadth_first_traversal(abstract_specs_dtuse):
    # That that depth of discovery is non-decreasing
    s = abstract_specs_dtuse["dttop"]
    depths = [
        depth
        for (depth, _) in traverse.traverse_nodes(
            [s], order="breadth", key=lambda s: s.name, depth=True
        )
    ]
    assert depths == sorted(depths)


def test_breadth_first_deptype_traversal(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dtuse"]

    names = [
        "dtuse",
        "dttop",
        "dtbuild1",
        "dtlink1",
        "dtbuild2",
        "dtlink2",
        "dtlink3",
        "dtlink4",
    ]

    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype=("build", "link"))
    assert [x.name for x in traversal] == names


def test_breadth_firsrt_traversal_deptype_with_builddeps(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dttop"]

    names = ["dttop", "dtbuild1", "dtlink1", "dtbuild2", "dtlink2", "dtlink3", "dtlink4"]

    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype=("build", "link"))
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_deptype_full(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dttop"]

    names = [
        "dttop",
        "dtbuild1",
        "dtlink1",
        "dtrun1",
        "dtbuild2",
        "dtlink2",
        "dtrun2",
        "dtlink3",
        "dtlink5",
        "dtrun3",
        "dtlink4",
        "dtbuild3",
    ]

    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype="all")
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_deptype_run(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dttop"]
    names = ["dttop", "dtrun1", "dtrun3"]
    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype="run")
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_reverse(abstract_specs_dt_diamond):
    gen = traverse.traverse_nodes(
        [abstract_specs_dt_diamond["dt-diamond-bottom"]],
        order="breadth",
        key=id,
        direction="parents",
        depth=True,
    )
    assert [(depth, spec.name) for (depth, spec) in gen] == [
        (0, "dt-diamond-bottom"),
        (1, "dt-diamond-left"),
        (1, "dt-diamond-right"),
        (2, "dt-diamond"),
    ]


def test_breadth_first_traversal_multiple_roots(abstract_specs_dt_diamond):
    # With DFS, the branch dt-diamond -> dt-diamond-left -> dt-diamond-bottom
    # is followed, with BFS, dt-diamond-bottom should be traced through the second
    # root dt-diamond-right at depth 1 instead.
    roots = [
        abstract_specs_dt_diamond["dt-diamond"],
        abstract_specs_dt_diamond["dt-diamond-right"],
    ]
    gen = traverse.traverse_edges(roots, order="breadth", key=id, depth=True, root=False)
    assert [(depth, edge.parent.name, edge.spec.name) for (depth, edge) in gen] == [
        (1, "dt-diamond", "dt-diamond-left"),  # edge from first root "to" depth 1
        (1, "dt-diamond-right", "dt-diamond-bottom"),  # edge from second root "to" depth 1
    ]


def test_breadth_first_versus_depth_first_tree(abstract_specs_chain):
    """
    The packages chain-a, chain-b, chain-c, chain-d have the following DAG:
    a --> b --> c --> d # a chain
    a --> c # and "skip" connections
    a --> d
    Here we test at what depth the nodes are discovered when using BFS vs DFS.
    """
    s = abstract_specs_chain["chain-a"]

    # BFS should find all nodes as direct deps
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="nodes", depth_first=False)
    ] == [
        (0, "chain-a"),
        (1, "chain-b"),
        (1, "chain-c"),
        (1, "chain-d"),
    ]

    # DFS will disover all nodes along the chain a -> b -> c -> d.
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="nodes", depth_first=True)
    ] == [
        (0, "chain-a"),
        (1, "chain-b"),
        (2, "chain-c"),
        (3, "chain-d"),
    ]

    # When covering all edges, we should never exceed depth 2 in BFS.
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="edges", depth_first=False)
    ] == [
        (0, "chain-a"),
        (1, "chain-b"),
        (2, "chain-c"),
        (1, "chain-c"),
        (2, "chain-d"),
        (1, "chain-d"),
    ]

    # In DFS we see the chain again.
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="edges", depth_first=True)
    ] == [
        (0, "chain-a"),
        (1, "chain-b"),
        (2, "chain-c"),
        (3, "chain-d"),
        (1, "chain-c"),
        (1, "chain-d"),
    ]


def test_breadth_first_versus_depth_first_printing(abstract_specs_chain):
    """Test breadth-first versus depth-first tree printing."""
    s = abstract_specs_chain["chain-a"]

    args = {"format": "{name}", "color": False}

    dfs_tree_nodes = """\
chain-a
    ^chain-b
        ^chain-c
            ^chain-d
"""
    assert s.tree(depth_first=True, **args) == dfs_tree_nodes

    bfs_tree_nodes = """\
chain-a
    ^chain-b
    ^chain-c
    ^chain-d
"""
    assert s.tree(depth_first=False, **args) == bfs_tree_nodes

    dfs_tree_edges = """\
chain-a
    ^chain-b
        ^chain-c
            ^chain-d
    ^chain-c
    ^chain-d
"""
    assert s.tree(depth_first=True, cover="edges", **args) == dfs_tree_edges

    bfs_tree_edges = """\
chain-a
    ^chain-b
        ^chain-c
    ^chain-c
        ^chain-d
    ^chain-d
"""
    assert s.tree(depth_first=False, cover="edges", **args) == bfs_tree_edges


@pytest.fixture()
def abstract_specs_toposort():
    # Create a graph that both BFS and DFS would not traverse in topo order, assuming
    # edges are ordered by target node name. Roots are {A, E} in forward order and
    # {F, G} in backward order.
    # forward: DFS([A, E]) traverses [A, B, F, G, C, D, E] (not topo since C < B)
    # forward: BFS([A, E]) traverses [A, E, B, C, D, F, G] (not topo since C < B)
    # reverse: DFS([F, G]) traverses [F, B, A, D, C, E, G] (not topo since D < A)
    # reverse: BFS([F, G]) traverses [F, G, B, A, D, C, E] (not topo since D < A)
    # E
    # | A
    # | | \
    # | C |
    # \ | |
    #   D |
    #   | /
    #   B
    #  / \
    # F   G
    return create_dag(
        nodes=["A", "B", "C", "D", "E", "F", "G"],
        edges=(
            ("A", "B", "all"),
            ("A", "C", "all"),
            ("B", "F", "all"),
            ("B", "G", "all"),
            ("C", "D", "all"),
            ("D", "B", "all"),
            ("E", "D", "all"),
        ),
    )


def test_traverse_topo_nodes(abstract_specs_toposort):
    nodes = abstract_specs_toposort

    def test_topo(roots, direction="children"):
        # Ensure the invariant that all parents of specs[i] are in specs[0:i]
        ordered = list(
            traverse.traverse_nodes(roots, order="topo", cover="nodes", direction=direction)
        )
        reverse = "parents" if direction == "children" else "children"
        for i in range(len(ordered)):
            parents = ordered[i].traverse(
                order="pre", cover="nodes", direction=reverse, root=False
            )
            assert set(list(parents)).issubset(set(ordered[:i]))

    # Traverse forward from roots A and E and a non-root D
    test_topo([nodes["D"], nodes["E"], nodes["A"]], direction="children")

    # Traverse reverse from leafs F and G and non-leaf D
    test_topo([nodes["F"], nodes["D"], nodes["G"]], direction="parents")


def test_traverse_topo_edges(abstract_specs_toposort):
    nodes = abstract_specs_toposort
    roots = [nodes["E"], nodes["A"]]

    # Collect pairs of (parent spec name, child spec name)
    edges = [
        (e.parent.name, e.spec.name)
        for e in traverse.traverse_edges(roots, order="topo", cover="edges", root=False)
    ]

    # See figure above, we have 7 edges (excluding artifical ones to the root)
    assert set(edges) == set(
        [
            ("A", "B"),
            ("A", "C"),
            ("B", "F"),
            ("B", "G"),
            ("C", "D"),
            ("D", "B"),
            ("E", "D"),
        ]
    )

    # Verify that all in-edges precede all out-edges
    for node in nodes.keys():
        in_edge_indices = [i for (i, (parent, child)) in enumerate(edges) if node == child]
        out_edge_indices = [i for (i, (parent, child)) in enumerate(edges) if node == parent]
        if in_edge_indices and out_edge_indices:
            assert max(in_edge_indices) < min(out_edge_indices)

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.traverse as traverse
from spack.spec import Spec


def key_by_hash(spec):
    return spec.dag_hash()


def test_breadth_first_traversal(config, mock_packages):
    # That that depth of discovery is non-decreasing
    s = Spec("dttop").concretized()
    depths = [
        depth
        for (depth, _) in traverse.traverse_nodes(
            [s], order="breadth", key=key_by_hash, depth=True
        )
    ]
    assert depths == sorted(depths)


def test_breadth_first_deptype_traversal(config, mock_packages):
    s = Spec("dtuse").concretized()

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

    traversal = traverse.traverse_nodes(
        [s], order="breadth", key=key_by_hash, deptype=("build", "link")
    )
    assert [x.name for x in traversal] == names


def test_breadth_firsrt_traversal_deptype_with_builddeps(config, mock_packages):
    s = Spec("dttop").concretized()

    names = ["dttop", "dtbuild1", "dtlink1", "dtbuild2", "dtlink2", "dtlink3", "dtlink4"]

    traversal = traverse.traverse_nodes(
        [s], order="breadth", key=key_by_hash, deptype=("build", "link")
    )
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_deptype_full(config, mock_packages):
    s = Spec("dttop").concretized()

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

    traversal = traverse.traverse_nodes([s], order="breadth", key=key_by_hash, deptype="all")
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_deptype_run(config, mock_packages):
    s = Spec("dttop").concretized()
    names = ["dttop", "dtrun1", "dtrun3"]
    traversal = traverse.traverse_nodes([s], order="breadth", key=key_by_hash, deptype="run")
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_reverse(config, mock_packages):
    s = Spec("dt-diamond").concretized()
    gen = traverse.traverse_nodes(
        [s["dt-diamond-bottom"]], order="breadth", key=key_by_hash, direction="parents", depth=True
    )
    assert [(depth, spec.name) for (depth, spec) in gen] == [
        (0, "dt-diamond-bottom"),
        (1, "dt-diamond-left"),
        (1, "dt-diamond-right"),
        (2, "dt-diamond"),
    ]


def test_breadth_first_traversal_multiple_roots(config, mock_packages):
    # With DFS, the branch dt-diamond -> dt-diamond-left -> dt-diamond-bottom
    # is followed, with BFS, dt-diamond-bottom should be traced through the second
    # root dt-diamond-right at depth 1 instead.
    s = Spec("dt-diamond").concretized()
    roots = [s["dt-diamond"], s["dt-diamond-right"]]
    gen = traverse.traverse_edges(roots, order="breadth", key=key_by_hash, depth=True, root=False)
    assert [(depth, edge.parent.name, edge.spec.name) for (depth, edge) in gen] == [
        (1, "dt-diamond", "dt-diamond-left"),  # edge from first root "to" depth 1
        (1, "dt-diamond-right", "dt-diamond-bottom"),  # edge from second root "to" depth 1
    ]


def test_breadth_first_versus_depth_first_tree(config, mock_packages):
    """
    The packages chain-a, chain-b, chain-c, chain-d have the following DAG:
    a --> b --> c --> d # a chain
    a --> c # and "skip" connections
    a --> d
    Here we test at what depth the nodes are discovered when using BFS vs DFS.
    """
    s = Spec("chain-a").concretized()

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


def test_breadth_first_versus_depth_first_printing(config, mock_packages):
    """Test breadth-first versus depth-first tree printing."""
    s = Spec("chain-a").concretized()

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

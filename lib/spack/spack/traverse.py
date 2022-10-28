# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict, namedtuple

import spack.spec

# Export only the high-level API.
__all__ = ["traverse_edges", "traverse_nodes", "traverse_tree"]

#: Data class that stores a directed edge together with depth at
#: which the target vertex was found. It is passed to ``accept``
#: and ``neighbors`` of visitors, so they can decide whether to
#: follow the edge or not.
EdgeAndDepth = namedtuple("EdgeAndDepth", ["edge", "depth"])


def sort_edges(edges):
    edges.sort(key=lambda edge: edge.spec.name)
    return edges


class BaseVisitor(object):
    """A simple visitor that accepts all edges unconditionally and follows all
    edges to dependencies of a given ``deptype``."""

    def __init__(self, deptype="all"):
        self.deptype = deptype

    def accept(self, node):
        """
        Arguments:
            node (EdgeAndDepth): Provides the depth and the edge through which the
                node was discovered

        Returns:
            bool: Returns ``True`` if the node is accepted. When ``False``, this
                indicates that the node won't be yielded by iterators and dependencies
                are not followed.
        """
        return True

    def neighbors(self, node):
        return sort_edges(node.edge.spec.edges_to_dependencies(deptype=self.deptype))


class ReverseVisitor(object):
    """A visitor that reverses the arrows in the DAG, following dependents."""

    def __init__(self, visitor, deptype="all"):
        self.visitor = visitor
        self.deptype = deptype

    def accept(self, node):
        return self.visitor.accept(node)

    def neighbors(self, node):
        """Return dependents, note that we actually flip the edge direction to allow
        generic programming"""
        spec = node.edge.spec
        return sort_edges(
            [edge.flip() for edge in spec.edges_from_dependents(deptype=self.deptype)]
        )


class CoverNodesVisitor(object):
    """A visitor that traverses each node once."""

    def __init__(self, visitor, key=id, visited=None):
        self.visitor = visitor
        self.key = key
        self.visited = set() if visited is None else visited

    def accept(self, node):
        # Covering nodes means: visit nodes once and only once.
        key = self.key(node.edge.spec)

        if key in self.visited:
            return False

        accept = self.visitor.accept(node)
        self.visited.add(key)
        return accept

    def neighbors(self, node):
        return self.visitor.neighbors(node)


class CoverEdgesVisitor(object):
    """A visitor that traverses all edges once."""

    def __init__(self, visitor, key=id, visited=None):
        self.visitor = visitor
        self.visited = set() if visited is None else visited
        self.key = key

    def accept(self, node):
        return self.visitor.accept(node)

    def neighbors(self, node):
        # Covering edges means: drop dependencies of visited nodes.
        key = self.key(node.edge.spec)

        if key in self.visited:
            return []

        self.visited.add(key)
        return self.visitor.neighbors(node)


def get_visitor_from_args(cover, direction, deptype, key=id, visited=None, visitor=None):
    """
    Create a visitor object from common keyword arguments.

    Arguments:
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction (str): ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype (str or tuple): allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow (when using cover=nodes/edges)
        visitor: An initial visitor that is used for composition.

    Returns:
        A visitor
    """
    visitor = visitor or BaseVisitor(deptype)
    if cover == "nodes":
        visitor = CoverNodesVisitor(visitor, key, visited)
    elif cover == "edges":
        visitor = CoverEdgesVisitor(visitor, key, visited)
    if direction == "parents":
        visitor = ReverseVisitor(visitor, deptype)
    return visitor


def root_specs(specs):
    """Initialize a list of edges from an imaginary root node to the root specs."""
    return [
        EdgeAndDepth(edge=spack.spec.DependencySpec(parent=None, spec=s, deptypes=()), depth=0)
        for s in specs
    ]


def traverse_depth_first_edges_generator(nodes, visitor, post_order=False, root=True, depth=False):
    # This is a somewhat non-standard implementation, but the reason to start with
    # edges is that we don't have to deal with an artificial root node when doing DFS
    # on multiple (root) specs.
    for node in nodes:
        if not visitor.accept(node):
            continue

        yield_me = root or node.depth > 0

        # Pre
        if yield_me and not post_order:
            yield (node.depth, node.edge) if depth else node.edge

        neighbors = [
            EdgeAndDepth(edge=edge, depth=node.depth + 1) for edge in visitor.neighbors(node)
        ]

        # This extra branch is just for efficiency.
        if len(neighbors) >= 0:
            for item in traverse_depth_first_edges_generator(
                neighbors, visitor, post_order, root, depth
            ):
                yield item

        # Post
        if yield_me and post_order:
            yield (node.depth, node.edge) if depth else node.edge


def traverse_breadth_first_edges_generator(queue, visitor, root=True, depth=False):
    while len(queue) > 0:
        node = queue.pop(0)

        # If the visitor doesn't accept the node, we don't yield it nor follow its edges.
        if not visitor.accept(node):
            continue

        if root or node.depth > 0:
            yield (node.depth, node.edge) if depth else node.edge

        for edge in visitor.neighbors(node):
            queue.append(EdgeAndDepth(edge, node.depth + 1))


def traverse_breadth_first_with_visitor(specs, visitor):
    """Performs breadth first traversal for a list of specs (not a generator).

    Arguments:
        specs (list): List of Spec instances.
        visitor: object that implements accept and neighbors interface, see
            for example BaseVisitor.
    """
    queue = root_specs(specs)
    while len(queue) > 0:
        node = queue.pop(0)

        # If the visitor doesn't accept the node, we don't traverse it further.
        if not visitor.accept(node):
            continue

        for edge in visitor.neighbors(node):
            queue.append(EdgeAndDepth(edge, node.depth + 1))


# Helper functions for generating a tree using breadth-first traversal


def breadth_first_to_tree_edges(roots, deptype="all", key=id):
    """This produces an adjacency list (with edges) and a map of parents.
    There may be nodes that are reached through multiple edges. To print as
    a tree, one should use the parents dict to verify if the path leading to
    the node is through the correct parent. If not, the branch should be
    truncated."""
    edges = defaultdict(list)
    parents = dict()

    for edge in traverse_edges(roots, order="breadth", cover="edges", deptype=deptype, key=key):
        parent_id = None if edge.parent is None else key(edge.parent)
        child_id = key(edge.spec)
        edges[parent_id].append(edge)
        if child_id not in parents:
            parents[child_id] = parent_id

    return edges, parents


def breadth_first_to_tree_nodes(roots, deptype="all", key=id):
    """This produces a list of edges that forms a tree; every node has no more
    that one incoming edge."""
    edges = defaultdict(list)

    for edge in traverse_edges(roots, order="breadth", cover="nodes", deptype=deptype, key=key):
        parent_id = None if edge.parent is None else key(edge.parent)
        edges[parent_id].append(edge)

    return edges


def traverse_breadth_first_tree_edges(parent_id, edges, parents, key=id, depth=0):
    """Do a depth-first search on edges generated by bread-first traversal,
    which can be used to produce a tree."""
    for edge in edges[parent_id]:
        yield (depth, edge)

        child_id = key(edge.spec)

        # Don't follow further if we're not the parent
        if parents[child_id] != parent_id:
            continue

        # yield from ... in Python 3.
        for item in traverse_breadth_first_tree_edges(child_id, edges, parents, key, depth + 1):
            yield item


def traverse_breadth_first_tree_nodes(parent_id, edges, key=id, depth=0):
    for edge in edges[parent_id]:
        yield (depth, edge)
        for item in traverse_breadth_first_tree_nodes(key(edge.spec), edges, key, depth + 1):
            yield item


# High-level API: traverse_edges, traverse_nodes, traverse_tree.


def traverse_edges(
    specs,
    root=True,
    order="pre",
    cover="nodes",
    direction="children",
    deptype="all",
    depth=False,
    key=id,
    visited=None,
):
    """
    Generator that yields edges from the DAG, starting from a list of root specs.

    Arguments:

        specs (list): List of root specs (considered to be depth 0)
        root (bool): Yield the root nodes themselves
        order (str): What order of traversal to use in the DAG. For depth-first
            search this can be ``pre`` or ``post``. For BFS this should be ``breadth``.
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction (str): ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype (str or tuple): allowed dependency types
        depth (bool): When ``False``, yield just edges. When ``True`` yield
            the tuple (depth, edge), where depth corresponds to the depth
            at which edge.spec was discovered.
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow

    Returns:
        A generator that yields ``DependencySpec`` if depth is ``False``
        or a tuple of ``(depth, DependencySpec)`` if depth is ``True``.
    """
    root_edges = root_specs(specs)
    visitor = get_visitor_from_args(cover, direction, deptype, key, visited)

    # Depth-first
    if order in ("pre", "post"):
        return traverse_depth_first_edges_generator(
            root_edges, visitor, order == "post", root, depth
        )

    # Breadth-first
    return traverse_breadth_first_edges_generator(root_edges, visitor, root, depth)


def traverse_nodes(
    specs,
    root=True,
    order="pre",
    cover="nodes",
    direction="children",
    deptype="all",
    depth=False,
    key=id,
    visited=None,
):
    """
    Generator that yields specs from the DAG, starting from a list of root specs.

    Arguments:
        specs (list): List of root specs (considered to be depth 0)
        root (bool): Yield the root nodes themselves
        order (str): What order of traversal to use in the DAG. For depth-first
            search this can be ``pre`` or ``post``. For BFS this should be ``breadth``.
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction (str): ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype (str or tuple): allowed dependency types
        depth (bool): When ``False``, yield just edges. When ``True`` yield
            the tuple ``(depth, edge)``, where depth corresponds to the depth
            at which ``edge.spec`` was discovered.
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow

    Yields:
        By default :class:`~spack.spec.Spec`, or a tuple ``(depth, Spec)`` if depth is
        set to ``True``.
    """
    for item in traverse_edges(specs, root, order, cover, direction, deptype, depth, key, visited):
        yield (item[0], item[1].spec) if depth else item.spec


def traverse_tree(specs, cover="nodes", deptype="all", key=id, depth_first=True):
    """
    Generator that yields ``(depth, DependencySpec)`` tuples in the depth-first
    pre-order, so that a tree can be printed from it.

    Arguments:

        specs (list): List of root specs (considered to be depth 0)
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        deptype (str or tuple): allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        depth_first (bool): Explore the tree in depth-first or breadth-first order.
            When setting ``depth_first=True`` and ``cover=nodes``, each spec only
            occurs once at the shallowest level, which is useful when rendering
            the tree in a terminal.

    Returns:
        A generator that yields ``(depth, DependencySpec)`` tuples in such an order
        that a tree can be printed.
    """
    # BFS only makes sense when going over edges and nodes, for paths the tree is
    # identical to DFS, which is much more efficient then.
    if not depth_first and cover == "edges":
        edges, parents = breadth_first_to_tree_edges(specs, deptype, key)
        return traverse_breadth_first_tree_edges(None, edges, parents)
    elif not depth_first and cover == "nodes":
        edges = breadth_first_to_tree_nodes(specs, deptype, key)
        return traverse_breadth_first_tree_nodes(None, edges)

    return traverse_edges(specs, order="pre", cover=cover, deptype=deptype, key=key, depth=True)

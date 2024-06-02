# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from abc import ABC
from collections import defaultdict
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

import spack.deptypes as dt
import spack.spec

# Export only the high-level API.
__all__ = ["traverse_edges", "traverse_nodes", "traverse_tree"]

EdgeAndDepth = Tuple["spack.spec.DependencySpec", int]
Key = Callable[["spack.spec.Spec"], Any]


def sort_edges(edges: List["spack.spec.DependencySpec"]) -> List["spack.spec.DependencySpec"]:
    edges.sort(key=lambda edge: (edge.spec.name or "", edge.spec.abstract_hash or ""))
    return edges


class AbstractVisitor(ABC):
    """Abstract base class for visitors that traverse the DAG."""

    def accept(self, item: EdgeAndDepth) -> bool:
        """
        Arguments:
            item: the edge through which this node was reached at what depth.

        Returns:
            Iff True, the node is yielded by iterators and dependencies are followed.
        """
        return True

    def neighbors(self, item: EdgeAndDepth) -> List["spack.spec.DependencySpec"]:
        raise NotImplementedError


class AbstractDFSVisitor(AbstractVisitor):
    """Abstract base class for visitors that traverse the DAG in depth-first fashion."""

    def pre(self, item: EdgeAndDepth) -> None:
        pass

    def post(self, item: EdgeAndDepth) -> None:
        pass


class DefaultVisitor(AbstractVisitor):
    def __init__(self, depflag: dt.DepFlag = dt.ALL) -> None:
        self.depflag = depflag

    def neighbors(self, item: EdgeAndDepth) -> List["spack.spec.DependencySpec"]:
        return sort_edges(item[0].spec.edges_to_dependencies(depflag=self.depflag))


class ReverseVisitor(AbstractVisitor):
    """A visitor that reverses the arrows in the DAG, following dependents."""

    def __init__(self, visitor: AbstractVisitor, depflag: dt.DepFlag = dt.ALL) -> None:
        self.visitor = visitor
        self.depflag = depflag

    def accept(self, item: EdgeAndDepth) -> bool:
        return self.visitor.accept(item)

    def neighbors(self, item: EdgeAndDepth) -> List["spack.spec.DependencySpec"]:
        """Return dependents, note that we actually flip the edge direction to allow
        generic programming"""
        spec = item[0].spec
        return sort_edges(
            [edge.flip() for edge in spec.edges_from_dependents(depflag=self.depflag)]
        )


class CoverNodesVisitor(AbstractVisitor):
    """A visitor that traverses each node once."""

    def __init__(
        self, visitor: AbstractVisitor, key: Key = id, visited: Optional[set] = None
    ) -> None:
        self.visitor = visitor
        self.key = key
        self.visited = set() if visited is None else visited

    def accept(self, item: EdgeAndDepth) -> bool:
        # Covering nodes means: visit nodes once and only once.
        key = self.key(item[0].spec)

        if key in self.visited:
            return False

        accept = self.visitor.accept(item)
        self.visited.add(key)
        return accept

    def neighbors(self, item: EdgeAndDepth) -> List["spack.spec.DependencySpec"]:
        return self.visitor.neighbors(item)


class CoverEdgesVisitor(AbstractVisitor):
    """A visitor that traverses all edges once."""

    def __init__(
        self, visitor: AbstractVisitor, key: Key = id, visited: Optional[set] = None
    ) -> None:
        self.visitor = visitor
        self.visited = set() if visited is None else visited
        self.key = key

    def accept(self, item: EdgeAndDepth) -> bool:
        return self.visitor.accept(item)

    def neighbors(self, item: EdgeAndDepth) -> List["spack.spec.DependencySpec"]:
        # Covering edges means: drop dependencies of visited nodes.
        key = self.key(item[0].spec)

        if key in self.visited:
            return []

        self.visited.add(key)
        return self.visitor.neighbors(item)


class TopoVisitor(AbstractDFSVisitor):
    """Visitor that can be used in :py:func:`depth-first traversal
    <spack.traverse.traverse_depth_first_with_visitor>` to generate
    a topologically ordered list of specs.

    Algorithm based on "Section 22.4: Topological sort", Introduction to Algorithms
    (2001, 2nd edition) by Cormen, Thomas H.; Leiserson, Charles E.; Rivest, Ronald L.;
    Stein, Clifford.

    Summary of the algorithm: prepend each vertex to a list in depth-first post-order,
    not following edges to nodes already seen. This ensures all descendants occur after
    their parent, yielding a topological order.

    Note: in this particular implementation we collect the *edges* through which the
    vertices are discovered, meaning that a topological order of *vertices* is obtained
    by taking the specs pointed to: ``map(lambda edge: edge.spec, visitor.edges)``.
    Lastly, ``all_edges=True`` can be used to retrieve a list of all reachable
    edges, with the property that for each vertex all in-edges precede all out-edges.
    """

    def __init__(
        self, visitor: AbstractVisitor, key: Key = id, root: bool = True, all_edges: bool = False
    ):
        """
        Arguments:
            visitor: visitor that implements accept(), pre(), post() and neighbors()
            key: uniqueness key for nodes
            root: Whether to include the root node.
            all_edges: when ``False`` (default): Each node is reached once, and
                ``map(lambda edge: edge.spec, visitor.edges)`` is topologically ordered. When
                ``True``, every edge is listed, ordered such that for each node all in-edges
                precede all out-edges.
        """
        self.visited: set = set()
        self.visitor = visitor
        self.key = key
        self.root = root
        self.reverse_order: List[spack.spec.DependencySpec] = []
        self.all_edges = all_edges

    def accept(self, item: EdgeAndDepth) -> bool:
        if self.key(item[0].spec) not in self.visited:
            return True
        if self.all_edges and (self.root or item[1] > 0):
            self.reverse_order.append(item[0])
        return False

    def post(self, item: EdgeAndDepth) -> None:
        self.visited.add(self.key(item[0].spec))
        if self.root or item[1] > 0:
            self.reverse_order.append(item[0])

    def neighbors(self, item: EdgeAndDepth) -> List["spack.spec.DependencySpec"]:
        return self.visitor.neighbors(item)

    @property
    def edges(self):
        """Return edges in topological order (in-edges precede out-edges)."""
        return list(reversed(self.reverse_order))


def get_visitor_from_args(
    cover, direction, depflag: Union[dt.DepFlag, dt.DepTypes], key=id, visited=None, visitor=None
):
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
        deptype: allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow (when using cover=nodes/edges)
        visitor: An initial visitor that is used for composition.

    Returns:
        A visitor
    """
    if not isinstance(depflag, dt.DepFlag):
        depflag = dt.canonicalize(depflag)
    visitor = visitor or DefaultVisitor(depflag)
    if cover == "nodes":
        visitor = CoverNodesVisitor(visitor, key, visited)
    elif cover == "edges":
        visitor = CoverEdgesVisitor(visitor, key, visited)
    if direction == "parents":
        visitor = ReverseVisitor(visitor, depflag)
    return visitor


def with_artificial_edges(specs):
    """Initialize a list of edges from an imaginary root node to the root specs."""
    return [
        (spack.spec.DependencySpec(parent=None, spec=s, depflag=0, virtuals=()), 0) for s in specs
    ]


def traverse_depth_first_edges_generator(
    edges: List[EdgeAndDepth],
    visitor,
    post_order: bool = False,
    root: bool = True,
    depth: bool = False,
):
    """Generator that takes explores a DAG in depth-first fashion starting from
    a list of edges. Note that typically DFS would take a vertex not a list of edges,
    but the API is like this so we don't have to create an artificial root node when
    traversing from multiple roots in a DAG.

    Arguments:
        edges: List of EdgeAndDepth instances
        visitor: class instance implementing accept() and neigbors()
        post_order: Whether to yield nodes when backtracking
        root: whether to yield at depth 0
        depth: when ``True`` yield a tuple of depth and edge, otherwise only the edge.
    """
    for edge in edges:
        if not visitor.accept(edge):
            continue

        yield_me = root or edge[1] > 0

        # Pre
        if yield_me and not post_order:
            yield (edge[1], edge[0]) if depth else edge[0]

        neighbors = [(n, edge[1] + 1) for n in visitor.neighbors(edge)]

        # This extra branch is just for efficiency.
        if len(neighbors) > 0:
            for item in traverse_depth_first_edges_generator(
                neighbors, visitor, post_order, root, depth
            ):
                yield item

        # Post
        if yield_me and post_order:
            yield (edge[1], edge[0]) if depth else edge[0]


def traverse_breadth_first_edges_generator(
    queue: List[EdgeAndDepth], visitor, root: bool = True, depth: bool = False
):
    while len(queue) > 0:
        edge = queue.pop(0)

        # If the visitor doesn't accept the node, we don't yield it nor follow its edges.
        if not visitor.accept(edge):
            continue

        if root or edge[1] > 0:
            yield (edge[1], edge[0]) if depth else edge[0]

        for e in visitor.neighbors(edge):
            queue.append((e, edge[1] + 1))


def traverse_breadth_first_with_visitor(specs: List[EdgeAndDepth], visitor: AbstractVisitor):
    """Performs breadth first traversal for a list of specs (not a generator).

    Arguments:
        specs: List of Spec instances.
        visitor: object that implements accept and neighbors interface, see
            for example BaseVisitor.
    """
    queue = with_artificial_edges(specs)
    while len(queue) > 0:
        edge = queue.pop(0)

        # If the visitor doesn't accept the node, we don't traverse it further.
        if not visitor.accept(edge):
            continue

        for e in visitor.neighbors(edge):
            queue.append((e, edge[1] + 1))


def traverse_depth_first_with_visitor(edges: List[EdgeAndDepth], visitor: AbstractDFSVisitor):
    """Traverse a DAG in depth-first fashion using a visitor, starting from
    a list of edges. Note that typically DFS would take a vertex not a list of edges,
    but the API is like this so we don't have to create an artificial root node when
    traversing from multiple roots in a DAG."""
    for edge in edges:
        if not visitor.accept(edge):
            continue

        visitor.pre(edge)

        neighbors = [(e, edge[1] + 1) for e in visitor.neighbors(edge)]

        traverse_depth_first_with_visitor(neighbors, visitor)

        visitor.post(edge)


# Helper functions for generating a tree using breadth-first traversal


def breadth_first_to_tree_edges(
    roots: Iterable["spack.spec.Spec"],
    deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    key: Key = id,
):
    """This produces an adjacency list (with edges) and a map of parents. There may be nodes that
    are reached through multiple edges. To print as a tree, one should use the parents dict to
    verify if the path leading to the node is through the correct parent. If not, the branch should
    be truncated."""
    edges = defaultdict(list)
    parents = dict()

    for edge in traverse_edges(roots, order="breadth", cover="edges", deptype=deptype, key=key):
        parent_id = None if edge.parent is None else key(edge.parent)
        child_id = key(edge.spec)
        edges[parent_id].append(edge)
        if child_id not in parents:
            parents[child_id] = parent_id

    return edges, parents


def breadth_first_to_tree_nodes(
    roots: Iterable["spack.spec.Spec"],
    deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    key: Key = id,
):
    """This produces a list of edges that forms a tree; every node has no more
    that one incoming edge."""
    edges = defaultdict(list)

    for edge in traverse_edges(roots, order="breadth", cover="nodes", deptype=deptype, key=key):
        parent_id = None if edge.parent is None else key(edge.parent)
        edges[parent_id].append(edge)

    return edges


def traverse_breadth_first_tree_edges(parent_id, edges, parents, key=id, depth=0):
    """Do a depth-first search on edges generated by breadth-first traversal, which can be used to
    produce a tree."""
    for edge in edges[parent_id]:
        yield (depth, edge)

        child_id = key(edge.spec)

        # Don't follow further if we're not the parent
        if parents[child_id] != parent_id:
            continue

        yield from traverse_breadth_first_tree_edges(child_id, edges, parents, key, depth + 1)


def traverse_breadth_first_tree_nodes(parent_id, edges, key=id, depth=0):
    for edge in edges[parent_id]:
        yield (depth, edge)
        yield from traverse_breadth_first_tree_nodes(key(edge.spec), edges, key, depth + 1)


# Topologic order
def traverse_edges_topo(
    specs: Iterable["spack.spec.Spec"],
    direction: str = "children",
    deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    key: Key = id,
    root: bool = True,
    all_edges: bool = False,
):
    """
    Returns a list of edges in topological order, in the sense that all in-edges of a
    vertex appear before all out-edges. By default with direction=children edges are
    directed from dependent to dependency. With directions=parents, the edges are
    directed from dependency to dependent.

    Arguments:
        specs: List of root specs (considered to be depth 0)
        direction: ``children`` (edges are directed from dependent to dependency)
            or ``parents`` (edges are flipped / directed from dependency to dependent)
        deptype: allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        root: Yield the root nodes themselves
        all_edges: When ``False`` only one in-edge per node is returned, when ``True`` all
            reachable edges are returned.
    """
    if not isinstance(deptype, dt.DepFlag):
        deptype = dt.canonicalize(deptype)
    default = DefaultVisitor(deptype)
    with_dir = ReverseVisitor(default, deptype) if direction == "parents" else default
    topo = TopoVisitor(with_dir, key=key, root=root, all_edges=all_edges)
    traverse_depth_first_with_visitor(with_artificial_edges(specs), topo)
    return topo.edges


# High-level API: traverse_edges, traverse_nodes, traverse_tree.


def traverse_edges(
    specs: Iterable["spack.spec.Spec"],
    root: bool = True,
    order: str = "pre",
    cover: str = "nodes",
    direction: str = "children",
    deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    depth: bool = False,
    key: Key = id,
    visited: Optional[set] = None,
):
    """
    Generator that yields edges from the DAG, starting from a list of root specs.

    Arguments:

        specs: List of root specs (considered to be depth 0)
        root: Yield the root nodes themselves
        order: What order of traversal to use in the DAG. For depth-first
            search this can be ``pre`` or ``post``. For BFS this should be ``breadth``.
            For topological order use ``topo``
        cover: Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction: ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype: allowed dependency types
        depth: When ``False``, yield just edges. When ``True`` yield
            the tuple (depth, edge), where depth corresponds to the depth
            at which edge.spec was discovered.
        key: function that takes a spec and outputs a key for uniqueness test.
        visited: a set of nodes not to follow

    Returns:
        A generator that yields ``DependencySpec`` if depth is ``False``
        or a tuple of ``(depth, DependencySpec)`` if depth is ``True``.
    """

    if order == "topo":
        if cover == "paths":
            raise ValueError("cover=paths not supported for order=topo")
        # TODO: There is no known need for topological ordering of traversals (edge or node)
        # with an initialized "visited" set. Revisit if needed.
        if visited is not None:
            raise ValueError("visited set not implemented for order=topo")
        return traverse_edges_topo(
            specs, direction, deptype, key, root, all_edges=cover == "edges"
        )

    root_edges = with_artificial_edges(specs)
    visitor = get_visitor_from_args(cover, direction, deptype, key, visited)

    # Depth-first
    if order in ("pre", "post"):
        return traverse_depth_first_edges_generator(
            root_edges, visitor, order == "post", root, depth
        )
    elif order == "breadth":
        return traverse_breadth_first_edges_generator(root_edges, visitor, root, depth)

    raise ValueError(f"Unknown order {order}")


def traverse_nodes(
    specs: Iterable["spack.spec.Spec"],
    root: bool = True,
    order: str = "pre",
    cover: str = "nodes",
    direction: str = "children",
    deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    depth: bool = False,
    key: Key = id,
    visited: Optional[set] = None,
):
    """
    Generator that yields specs from the DAG, starting from a list of root specs.

    Arguments:
        specs: List of root specs (considered to be depth 0)
        root: Yield the root nodes themselves
        order: What order of traversal to use in the DAG. For depth-first
            search this can be ``pre`` or ``post``. For BFS this should be ``breadth``.
        cover: Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction: ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype: allowed dependency types
        depth: When ``False``, yield just edges. When ``True`` yield
            the tuple ``(depth, edge)``, where depth corresponds to the depth
            at which ``edge.spec`` was discovered.
        key: function that takes a spec and outputs a key for uniqueness test.
        visited: a set of nodes not to follow

    Yields:
        By default :class:`~spack.spec.Spec`, or a tuple ``(depth, Spec)`` if depth is
        set to ``True``.
    """
    for item in traverse_edges(specs, root, order, cover, direction, deptype, depth, key, visited):
        yield (item[0], item[1].spec) if depth else item.spec


def traverse_tree(
    specs: Iterable["spack.spec.Spec"],
    cover: str = "nodes",
    deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    key: Key = id,
    depth_first: bool = True,
):
    """
    Generator that yields ``(depth, DependencySpec)`` tuples in the depth-first
    pre-order, so that a tree can be printed from it.

    Arguments:

        specs: List of root specs (considered to be depth 0)
        cover: Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        deptype: allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        depth_first: Explore the tree in depth-first or breadth-first order.
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
        return traverse_breadth_first_tree_edges(None, edges, parents, key)
    elif not depth_first and cover == "nodes":
        edges = breadth_first_to_tree_nodes(specs, deptype, key)
        return traverse_breadth_first_tree_nodes(None, edges, key)

    return traverse_edges(specs, order="pre", cover=cover, deptype=deptype, key=key, depth=True)


def by_dag_hash(s: "spack.spec.Spec") -> str:
    """Used very often as a key function for traversals."""
    return s.dag_hash()

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.spec import DependencySpec


class EdgeAndDepth(object):
    def __init__(self, edge, depth):
        self.edge = edge
        self.depth = depth


def sort_edges(edges):
    edges.sort(key=lambda edge: edge.spec.name)
    return edges


class BaseVisitor(object):
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

    def __init__(self, visitor):
        self.visitor = visitor
        self.visited = set()

    def accept(self, node):
        # Covering nodes means: visit nodes once and only once.
        dag_hash = node.edge.spec.dag_hash()

        if dag_hash in self.visited:
            return False

        accept = self.visitor.accept(node)
        self.visited.add(dag_hash)
        return accept

    def neighbors(self, node):
        return self.visitor.neighbors(node)


class CoverEdgesVisitor(object):
    """A visitor that traverses all edges once."""

    def __init__(self, visitor):
        self.visitor = visitor
        self.visited = set()

    def accept(self, node):
        return self.visitor.accept(node)

    def neighbors(self, node):
        # Covering edges means: drop dependencies of visited nodes.
        dag_hash = node.edge.spec.dag_hash()

        if dag_hash in self.visited:
            return []

        self.visited.add(dag_hash)
        return self.visitor.neighbors(node)


def get_visitor_from_args(cover, direction, deptype, visitor=None):
    """
    Create a visitor object from keyword arguments, which simplifies the API
    a bit, as cover, direction, deptype kwargs have been around for long in Spack.

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
        visitor: An initial visitor that is used for composition.

    Returns:
        A visitor
    """
    visitor = visitor or BaseVisitor(deptype)
    if cover == "nodes":
        visitor = CoverNodesVisitor(visitor)
    elif cover == "edges":
        visitor = CoverEdgesVisitor(visitor)
    if direction == "parents":
        visitor = ReverseVisitor(visitor, deptype)
    return visitor


def init_queue(specs):
    """Initialize a queue for breadth-first traversal for given root specs.

    Returns:
        list: A list of edges from "nowhere" to the given specs at depth 0.
    """
    return [
        EdgeAndDepth(edge=DependencySpec(parent=None, spec=s, deptypes=()), depth=0) for s in specs
    ]


def traverse_breadth_first_edges(
    specs, root=True, cover="nodes", direction="children", deptype="all", depth=False
):
    """
    Generator that yields edges from the DAG in breadth-first order, starting
    from a list of root specs.

    Arguments:

        specs (list): List of root specs (considered to be depth 0)
        root (bool): Yield the root nodes themselves
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

    Yields:
        By default DependencySpec, or a tuple of depth and DependencySpec if depth
        was set to ``True``.
    """
    # Initialize the queue with None -> Spec edges, where None indicates it's
    # the root.
    queue = init_queue(specs)
    visitor = get_visitor_from_args(cover, direction, deptype)

    while len(queue) > 0:
        node = queue.pop(0)

        # If the visitor doesn't accept the node, we don't yield it nor follow its edges.
        if not visitor.accept(node):
            continue

        if root or node.depth > 0:
            if depth:
                yield node.depth, node.edge
            else:
                yield node.edge

        for edge in visitor.neighbors(node):
            queue.append(EdgeAndDepth(edge, node.depth + 1))


def traverse_breadth_first_nodes(
    specs, root=True, cover="nodes", direction="children", deptype="all", depth=False
):
    """
    Generator that yields specs from the DAG in breadth-first order, starting
    from a list of root specs.

    Arguments:
        specs (list): List of root specs (considered to be depth 0)
        root (bool): Yield the root nodes themselves
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

    Yields:
        By default Spec, or a tuple of depth and Spec if depth was set to ``True``.
    """
    for item in traverse_breadth_first_edges(specs, root, cover, direction, deptype, depth):
        if depth:
            yield item[0], item[1].spec
        else:
            yield item.spec


def traverse_breadth_first_with_visitor(specs, visitor):
    """Performs breadth first traversal for a list of specs (not a generator).

    Arguments:
        specs (list): List of Spec instances.
        visitor: object that implements accept and neighbors interface, see
            for example BaseVisitor.
    """
    queue = init_queue(specs)
    while len(queue) > 0:
        node = queue.pop(0)

        # If the visitor doesn't accept the node, we don't traverse it further.
        if not visitor.accept(node):
            continue

        for edge in visitor.neighbors(node):
            queue.append(EdgeAndDepth(edge, node.depth + 1))

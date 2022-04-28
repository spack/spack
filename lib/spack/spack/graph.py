# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

r"""Functions for graphing DAGs of dependencies.

This file contains code for graphing DAGs of software packages
(i.e. Spack specs).  There are two main functions you probably care
about:

graph_ascii() will output a colored graph of a spec in ascii format,
kind of like the graph git shows with "git log --graph", e.g.::

    o  mpileaks
    |\
    | |\
    | o |  callpath
    |/| |
    | |\|
    | |\ \
    | | |\ \
    | | | | o  adept-utils
    | |_|_|/|
    |/| | | |
    o | | | |  mpi
     / / / /
    | | o |  dyninst
    | |/| |
    |/|/| |
    | | |/
    | o |  libdwarf
    |/ /
    o |  libelf
     /
    o  boost

graph_dot() will output a graph of a spec (or multiple specs) in dot
format.

Note that ``graph_ascii`` assumes a single spec while ``graph_dot``
can take a number of specs as input.

"""
import heapq
import itertools
import sys

import llnl.util.tty.color

import spack.dependency

__all__ = ['graph_ascii', 'AsciiGraph', 'graph_dot']


def node_label(spec):
    return spec.format('{name}{@version}{/hash:7}')


def topological_sort(spec, deptype='all'):
    """Return a list of dependency specs in topological sorting order.

    The spec argument is not modified in by the function.

    This function assumes specs don't have cycles, i.e. that we are really
    operating with a DAG.

    Args:
        spec (spack.spec.Spec): the spec to be analyzed
        deptype (str or tuple): dependency types to account for when
            constructing the list
    """
    deptype = spack.dependency.canonical_deptype(deptype)

    # Work on a copy so this is nondestructive
    spec = spec.copy(deps=True)
    nodes = spec.index(deptype=deptype)

    def dependencies(specs):
        """Return all the dependencies (including transitive) for a spec."""
        return list(set(itertools.chain.from_iterable(
            s.dependencies(deptype=deptype) for s in specs
        )))

    def dependents(specs):
        """Return all the dependents (including those of transitive dependencies)
        for a spec.
        """
        candidates = list(set(itertools.chain.from_iterable(
            s.dependents(deptype=deptype) for s in specs
        )))
        return [x for x in candidates if x.name in nodes]

    topological_order, children = [], {}

    # Map a spec encoded as (id, name) to a list of its transitive dependencies
    for spec in itertools.chain.from_iterable(nodes.values()):
        children[(id(spec), spec.name)] = [
            x for x in dependencies([spec]) if x.name in nodes
        ]

    # To return a result that is topologically ordered we need to add nodes
    # only after their dependencies. The first nodes we can add are leaf nodes,
    # i.e. nodes that have no dependencies.
    ready = [
        spec for spec in itertools.chain.from_iterable(nodes.values())
        if not dependencies([spec])
    ]
    heapq.heapify(ready)

    while ready:
        # Pop a "ready" node and add it to the topologically ordered list
        s = heapq.heappop(ready)
        topological_order.append(s)

        # Check if adding the last node made other nodes "ready"
        for dep in dependents([s]):
            children[(id(dep), dep.name)].remove(s)
            if not children[(id(dep), dep.name)]:
                heapq.heappush(ready, dep)

    return topological_order


def find(seq, predicate):
    """Find index in seq for which predicate is True.

    Searches the sequence and returns the index of the element for
    which the predicate evaluates to True.  Returns -1 if the
    predicate does not evaluate to True for any element in seq.

    """
    for i, elt in enumerate(seq):
        if predicate(elt):
            return i
    return -1


# Names of different graph line states.  We record previous line
# states so that we can easily determine what to do when connecting.
states = ('node', 'collapse', 'merge-right', 'expand-right', 'back-edge')
NODE, COLLAPSE, MERGE_RIGHT, EXPAND_RIGHT, BACK_EDGE = states


class AsciiGraph(object):

    def __init__(self):
        # These can be set after initialization or after a call to
        # graph() to change behavior.
        self.node_character = 'o'
        self.debug = False
        self.indent = 0
        self.deptype = spack.dependency.all_deptypes

        # These are colors in the order they'll be used for edges.
        # See llnl.util.tty.color for details on color characters.
        self.colors = 'rgbmcyRGBMCY'

        # Internal vars are used in the graph() function and are
        # properly initialized there.
        self._name_to_color = None    # Node name to color
        self._out = None              # Output stream
        self._frontier = None         # frontier
        self._prev_state = None       # State of previous line
        self._prev_index = None       # Index of expansion point of prev line

    def _indent(self):
        self._out.write(self.indent * ' ')

    def _write_edge(self, string, index, sub=0):
        """Write a colored edge to the output stream."""
        # Ignore empty frontier entries (they're just collapsed)
        if not self._frontier[index]:
            return
        name = self._frontier[index][sub]
        edge = "@%s{%s}" % (self._name_to_color[name], string)
        self._out.write(edge)

    def _connect_deps(self, i, deps, label=None):
        """Connect dependencies to existing edges in the frontier.

        ``deps`` are to be inserted at position i in the
        frontier. This routine determines whether other open edges
        should be merged with <deps> (if there are other open edges
        pointing to the same place) or whether they should just be
        inserted as a completely new open edge.

        Open edges that are not fully expanded (i.e. those that point
        at multiple places) are left intact.

        Parameters:

        label    -- optional debug label for the connection.

        Returns: True if the deps were connected to another edge
        (i.e. the frontier did not grow) and False if the deps were
        NOT already in the frontier (i.e. they were inserted and the
        frontier grew).

        """
        if len(deps) == 1 and deps in self._frontier:
            j = self._frontier.index(deps)

            # convert a right connection into a left connection
            if i < j:
                self._frontier.pop(j)
                self._frontier.insert(i, deps)
                return self._connect_deps(j, deps, label)

            collapse = True
            if self._prev_state == EXPAND_RIGHT:
                # Special case where previous line expanded and i is off by 1.
                self._back_edge_line([], j, i + 1, True,
                                     label + "-1.5 " + str((i + 1, j)))
                collapse = False

            else:
                # Previous node also expanded here, so i is off by one.
                if self._prev_state == NODE and self._prev_index < i:
                    i += 1

                if i - j > 1:
                    # We need two lines to connect if distance > 1
                    self._back_edge_line([], j,  i, True,
                                         label + "-1 " + str((i, j)))
                    collapse = False

            self._back_edge_line([j], -1, -1, collapse,
                                 label + "-2 " + str((i, j)))
            return True

        elif deps:
            self._frontier.insert(i, deps)
            return False

    def _set_state(self, state, index, label=None):
        if state not in states:
            raise ValueError("Invalid graph state!")
        self._prev_state = state
        self._prev_index = index

        if self.debug:
            self._out.write(" " * 20)
            self._out.write("%-20s" % (
                str(self._prev_state) if self._prev_state else ''))
            self._out.write("%-20s" % (str(label) if label else ''))
            self._out.write("%s" % self._frontier)

    def _back_edge_line(self, prev_ends, end, start, collapse, label=None):
        """Write part of a backwards edge in the graph.

        Writes single- or multi-line backward edges in an ascii graph.
        For example, a single line edge::

            | | | | o |
            | | | |/ /  <-- single-line edge connects two nodes.
            | | | o |

        Or a multi-line edge (requires two calls to back_edge)::

            | | | | o |
            | |_|_|/ /   <-- multi-line edge crosses vertical edges.
            |/| | | |
            o | | | |

        Also handles "pipelined" edges, where the same line contains
        parts of multiple edges::

                      o start
            | |_|_|_|/|
            |/| | |_|/| <-- this line has parts of 2 edges.
            | | |/| | |
            o   o

        Arguments:

        prev_ends -- indices in frontier of previous edges that need
                     to be finished on this line.

        end -- end of the current edge on this line.

        start -- start index of the current edge.

        collapse -- whether the graph will be collapsing (i.e. whether
                    to slant the end of the line or keep it straight)

        label -- optional debug label to print after the line.

        """
        def advance(to_pos, edges):
            """Write edges up to <to_pos>."""
            for i in range(self._pos, to_pos):
                for e in edges():
                    self._write_edge(*e)
                self._pos += 1

        flen = len(self._frontier)
        self._pos = 0
        self._indent()

        for p in prev_ends:
            advance(p,         lambda: [("| ", self._pos)])
            advance(p + 1,     lambda: [("|/", self._pos)])

        if end >= 0:
            advance(end + 1,   lambda: [("| ", self._pos)])
            advance(start - 1, lambda: [("|",  self._pos), ("_", end)])
        else:
            advance(start - 1, lambda: [("| ", self._pos)])

        if start >= 0:
            advance(start,     lambda: [("|",  self._pos), ("/", end)])

        if collapse:
            advance(flen,      lambda: [(" /", self._pos)])
        else:
            advance(flen,      lambda: [("| ", self._pos)])

        self._set_state(BACK_EDGE, end, label)
        self._out.write("\n")

    def _node_label(self, node):
        return node.format('{name}@@{version}{/hash:7}')

    def _node_line(self, index, node):
        """Writes a line with a node at index."""
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)

        self._out.write("%s " % self.node_character)

        for c in range(index + 1, len(self._frontier)):
            self._write_edge("| ", c)

        self._out.write(self._node_label(node))
        self._set_state(NODE, index)
        self._out.write("\n")

    def _collapse_line(self, index):
        """Write a collapsing line after a node was added at index."""
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)
        for c in range(index, len(self._frontier)):
            self._write_edge(" /", c)

        self._set_state(COLLAPSE, index)
        self._out.write("\n")

    def _merge_right_line(self, index):
        """Edge at index is same as edge to right.  Merge directly with '\'"""
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)
        self._write_edge("|", index)
        self._write_edge("\\", index + 1)
        for c in range(index + 1, len(self._frontier)):
            self._write_edge("| ", c)

        self._set_state(MERGE_RIGHT, index)
        self._out.write("\n")

    def _expand_right_line(self, index):
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)

        self._write_edge("|", index)
        self._write_edge("\\", index + 1)

        for c in range(index + 2, len(self._frontier)):
            self._write_edge(" \\", c)

        self._set_state(EXPAND_RIGHT, index)
        self._out.write("\n")

    def write(self, spec, color=None, out=None):
        """Write out an ascii graph of the provided spec.

        Arguments:
        spec -- spec to graph.  This only handles one spec at a time.

        Optional arguments:

        out -- file object to write out to (default is sys.stdout)

        color -- whether to write in color.  Default is to autodetect
                 based on output file.

        """
        if out is None:
            out = sys.stdout

        if color is None:
            color = out.isatty()

        self._out = llnl.util.tty.color.ColorStream(out, color=color)

        # We'll traverse the spec in topological order as we graph it.
        nodes_in_topological_order = topological_sort(spec, deptype=self.deptype)

        # Work on a copy to be nondestructive
        spec = spec.copy()

        # Colors associated with each node in the DAG.
        # Edges are colored by the node they point to.
        self._name_to_color = {
            spec.full_hash(): self.colors[i % len(self.colors)]
            for i, spec in enumerate(nodes_in_topological_order)
        }

        # Frontier tracks open edges of the graph as it's written out.
        self._frontier = [[spec.full_hash()]]
        while self._frontier:
            # Find an unexpanded part of frontier
            i = find(self._frontier, lambda f: len(f) > 1)

            if i >= 0:
                # Expand frontier until there are enough columns for all children.

                # Figure out how many back connections there are and
                # sort them so we do them in order
                back = []
                for d in self._frontier[i]:
                    b = find(self._frontier[:i], lambda f: f == [d])
                    if b != -1:
                        back.append((b, d))

                # Do all back connections in sorted order so we can
                # pipeline them and save space.
                if back:
                    back.sort()
                    prev_ends = []
                    collapse_l1 = False
                    for j, (b, d) in enumerate(back):
                        self._frontier[i].remove(d)
                        if i - b > 1:
                            collapse_l1 = any(not e for e in self._frontier)
                            self._back_edge_line(
                                prev_ends, b, i, collapse_l1, 'left-1')
                            del prev_ends[:]
                        prev_ends.append(b)

                    # Check whether we did ALL the deps as back edges,
                    # in which case we're done.
                    pop = not self._frontier[i]
                    collapse_l2 = pop
                    if collapse_l1:
                        collapse_l2 = False
                    if pop:
                        self._frontier.pop(i)
                    self._back_edge_line(
                        prev_ends, -1, -1, collapse_l2, 'left-2')

                elif len(self._frontier[i]) > 1:
                    # Expand forward after doing all back connections

                    if (i + 1 < len(self._frontier) and
                            len(self._frontier[i + 1]) == 1 and
                            self._frontier[i + 1][0] in self._frontier[i]):
                        # We need to connect to the element to the right.
                        # Keep lines straight by connecting directly and
                        # avoiding unnecessary expand/contract.
                        name = self._frontier[i + 1][0]
                        self._frontier[i].remove(name)
                        self._merge_right_line(i)

                    else:
                        # Just allow the expansion here.
                        dep_hash = self._frontier[i].pop(0)
                        deps = [dep_hash]
                        self._frontier.insert(i, deps)
                        self._expand_right_line(i)

                        self._frontier.pop(i)
                        self._connect_deps(i, deps, "post-expand")

                # Handle any remaining back edges to the right
                j = i + 1
                while j < len(self._frontier):
                    deps = self._frontier.pop(j)
                    if not self._connect_deps(j, deps, "back-from-right"):
                        j += 1

            else:
                # Nothing to expand; add dependencies for a node.
                node = nodes_in_topological_order.pop()

                # Find the named node in the frontier and draw it.
                i = find(self._frontier, lambda f: node.full_hash() in f)
                self._node_line(i, node)

                # Replace node with its dependencies
                self._frontier.pop(i)
                deps = node.dependencies(deptype=self.deptype)
                if deps:
                    deps = sorted((d.full_hash() for d in deps), reverse=True)
                    self._connect_deps(i, deps, "new-deps")  # anywhere.

                elif self._frontier:
                    self._collapse_line(i)


def graph_ascii(spec, node='o', out=None, debug=False,
                indent=0, color=None, deptype='all'):
    graph = AsciiGraph()
    graph.debug = debug
    graph.indent = indent
    graph.node_character = node
    if deptype:
        graph.deptype = spack.dependency.canonical_deptype(deptype)

    graph.write(spec, color=color, out=out)


def graph_dot(specs, deptype='all', static=False, out=None):
    """Generate a graph in dot format of all provided specs.

    Print out a dot formatted graph of all the dependencies between
    package.  Output can be passed to graphviz, e.g.:

    .. code-block:: console

        spack graph --dot qt | dot -Tpdf > spack-graph.pdf

    """
    if not specs:
        raise ValueError("Must provide specs to graph_dot")

    if out is None:
        out = sys.stdout
    deptype = spack.dependency.canonical_deptype(deptype)

    def static_graph(spec, deptype):
        pkg = spec.package
        possible = pkg.possible_dependencies(
            expand_virtuals=True, deptype=deptype)

        nodes = set()  # elements are (node name, node label)
        edges = set()  # elements are (src key, dest key)
        for name, deps in possible.items():
            nodes.add((name, name))
            edges.update((name, d) for d in deps)
        return nodes, edges

    def dynamic_graph(spec, deptypes):
        nodes = set()  # elements are (node key, node label)
        edges = set()  # elements are (src key, dest key)
        for s in spec.traverse(deptype=deptype):
            nodes.add((s.dag_hash(), node_label(s)))
            for d in s.dependencies(deptype=deptype):
                edge = (s.dag_hash(), d.dag_hash())
                edges.add(edge)
        return nodes, edges

    nodes = set()
    edges = set()
    for spec in specs:
        if static:
            n, e = static_graph(spec, deptype)
        else:
            n, e = dynamic_graph(spec, deptype)
        nodes.update(n)
        edges.update(e)

    out.write('digraph G {\n')
    out.write('  labelloc = "b"\n')
    out.write('  rankdir = "TB"\n')
    out.write('  ranksep = "1"\n')
    out.write('  edge[\n')
    out.write('     penwidth=4')
    out.write('  ]\n')
    out.write('  node[\n')
    out.write('     fontname=Monaco,\n')
    out.write('     penwidth=4,\n')
    out.write('     fontsize=24,\n')
    out.write('     margin=.2,\n')
    out.write('     shape=box,\n')
    out.write('     fillcolor=lightblue,\n')
    out.write('     style="rounded,filled"')
    out.write('  ]\n')

    # write nodes
    out.write('\n')
    for key, label in nodes:
        out.write('  "%s" [label="%s"]\n' % (key, label))

    # write edges
    out.write('\n')
    for src, dest in edges:
        out.write('  "%s" -> "%s"\n' % (src, dest))

    # ensure that roots are all at the top of the plot
    dests = set([d for _, d in edges])
    roots = ['"%s"' % k for k, _ in nodes if k not in dests]
    out.write('\n')
    out.write('  { rank=min; %s; }' % "; ".join(roots))

    out.write('\n')
    out.write('}\n')

##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Functions for graphing DAGs of dependencies.

This file contains code for graphing DAGs of software packages
(i.e. Spack specs).  There are two main functions you probably care
about:

graph_ascii() will output a colored graph of a spec in ascii format,
knd of like the graph git shows with "git log --graph".

graph_dot() will output a graph of a spec (or multiple specs) in dot
format.

Note that ``graph_ascii`` assumes a single spec while ``graph_dot``
can take a number of specs as input.

"""
__all__ = ['topological_sort', 'graph_ascii', 'AsciiGraph', 'graph_dot']

from heapq import *

from llnl.util.lang import *
from llnl.util.tty.color import *

import spack
from spack.spec import Spec


def topological_sort(spec, **kwargs):
    """Topological sort for specs.

    Return a list of dependency specs sorted topologically.  The spec
    argument is not modified in the process.

    """
    reverse = kwargs.get('reverse', False)
    if not reverse:
        parents  = lambda s: s.dependents
        children = lambda s: s.dependencies
    else:
        parents  = lambda s: s.dependencies
        children = lambda s: s.dependents

    # Work on a copy so this is nondestructive.
    spec = spec.copy()
    nodes = spec.index()

    topo_order = []
    remaining = [name for name in nodes.keys() if not parents(nodes[name])]
    heapify(remaining)

    while remaining:
        name = heappop(remaining)
        topo_order.append(name)

        node = nodes[name]
        for dep in children(node).values():
            del parents(dep)[node.name]
            if not parents(dep):
                heappush(remaining, dep.name)

    if any(parents(s) for s in spec.traverse()):
        raise ValueError("Spec has cycles!")
    else:
        return topo_order


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


class AsciiGraph(object):
    def __init__(self):
        # These can be set after initialization or after a call to
        # graph() to change behavior.
        self.node_character = 'o'
        self.debug = False
        self.indent = 0

        # These are colors in the order they'll be used for edges.
        # See llnl.util.tty.color for details on color characters.
        self.colors = 'rgbmcyRGBMCY'

        # Internal vars are used in the graph() function and are
        # properly initialized there.
        self._name_to_color = None    # Node name to color
        self._out = None              # Output stream
        self._frontier = None         # frontier
        self._nodes = None            # dict from name -> node


    def _indent(self):
        self._out.write(self.indent * ' ')


    def _write_edge(self, string, index, sub=0):
        """Write a colored edge to the output stream."""
        name = self._frontier[index][sub]
        edge = "@%s{%s}" % (self._name_to_color[name], string)
        self._out.write(edge)


    def _connect_deps(self, i, deps, collapse, label):
        """Connect dependencies to existing edges in the frontier.

        ``deps`` are to be inserted at position i in the
        frontier. This routine determines whether other open edges
        should be merged with <deps> (if there are other open edges
        pointing to the same place) or whether they should just be
        inserted as a completely new open edge.

        Open edges that are not fully expanded (i.e. those that point
        at multiple places) are left intact.

        Parameters:

        collapse -- whether the frontier is collapsing or staying the
                    same size.

        label    -- optional debug label for the connection.

        Returns: True if the deps were connected to another edge
        (i.e. the frontier did not grow) and False if the deps were
        NOT already in the frontier (i.e. they were inserted and the
        frontier grew).

        """
        if len(deps) == 1 and deps in self._frontier:
            j = self._frontier.index(deps)

            # connect to the left
            if j < i:
                if i-j > 1:   # two lines if distance > 1
                    self._back_edge([], j,  i, True, label)
                self._back_edge([j], -1, -1, (i-j == 1), label)

            # connect to the right
            else:
                if i < j:
                    self._frontier.pop(j)
                    self._frontier.insert(i, deps)
                if j-i > 1:
                    self._back_edge([], i, j+1, collapse, label)
                self._back_edge([i], -1,  -1, not (j-i > 1) and collapse, label)
            return True

        elif deps:
            self._frontier.insert(i, deps)
            return False


    def _add_deps_to_frontier(self, node, i):
        """Add dependencies to frontier.

        Adds the dependencies of <node> to the frontier, and connects
        them to other open edges if they match.  Also deletes parent
        pointers in the node to mark edges as covered.

        """
        deps = sorted((d for d in node.dependencies), reverse=True)
        self._connect_deps(i, deps, True, "add_deps")
        for d in deps:
            del self._nodes[d].dependents[node.name]



    def _back_edge(self, prev_ends, end, start, collapse, label=None):
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
            advance(p,         lambda: [("| ", self._pos)] )
            advance(p+1,       lambda: [("|/", self._pos)] )

        if end >= 0:
            advance(end + 1,   lambda: [("| ", self._pos)] )
            advance(start - 1, lambda: [("|",  self._pos), ("_", end)] )
        else:
            advance(start - 1, lambda: [("| ", self._pos)] )

        if start >= 0:
            advance(start,     lambda: [("|",  self._pos), ("/", end)] )

        if collapse:
            advance(flen,      lambda: [(" /", self._pos)] )
        else:
            advance(flen,      lambda: [("| ", self._pos)] )

        if self.debug:
            self._out.write(" " * 10)
            if label:
                self._out.write(label)
            self._out.write("%s" % self._frontier)

        self._out.write("\n")


    def write(self, spec, **kwargs):
        """Write out an ascii graph of the provided spec.

        Arguments:
        spec -- spec to graph.  This only handles one spec at a time.

        Optional arguments:

        out -- file object to write out to (default is sys.stdout)

        color -- whether to write in color.  Default is to autodetect
                 based on output file.

        """
        out = kwargs.get('out', None)
        if not out:
            out = sys.stdout

        color = kwargs.get('color', None)
        if not color:
            color = out.isatty()
        self._out = ColorStream(sys.stdout, color=color)

        # We'll traverse the spec in topo order as we graph it.
        topo_order = topological_sort(spec, reverse=True)

        # Work on a copy to be nondestructive
        spec = spec.copy()
        self._nodes = spec.index()

        # Colors associated with each node in the DAG.
        # Edges are colored by the node they point to.
        self._name_to_color = dict((name, self.colors[i % len(self.colors)])
                                  for i, name in enumerate(topo_order))

        # This array tracks the open edges at the frontier of the
        # graph we're writing out.
        self._frontier = []

        self._add_deps_to_frontier(spec, 0)
        self._indent()
        self._out.write('%s  %s\n' % (self.node_character, spec.name))
        topo_order.pop()

        while self._frontier:
            # Find an unexpanded part of frontier
            i = find(self._frontier, lambda f: len(f) > 1)

            # Expand frontier until there are enough columns for all children.
            if i >= 0:
                # Figure out how many back connections there are and
                # sort them so we do them in order
                back = []
                for d in self._frontier[i]:
                    b = find(self._frontier[:i], lambda f: f == [d])
                    if b != -1: back.append((b, d))

                # Do all back connections in sorted order so we can
                # pipeline them and save space.
                if back:
                    back.sort()
                    prev_ends = []
                    for j, (b, d) in enumerate(back):
                        self._frontier[i].remove(d)
                        if i-b > 1:
                            self._back_edge(prev_ends, b, i, False)
                            del prev_ends[:]
                        prev_ends.append(b)
                    self._back_edge(prev_ends, -1, -1, False)

                if not self._frontier[i]:
                    self._frontier.pop(i)

                elif len(self._frontier[i]) > 1:
                    # Expand forawrd after doing all back connections
                    self._indent()
                    for c in range(i):
                        self._write_edge("| ", c)
                    self._write_edge("|", i)

                    if (i+1 < len(self._frontier) and len(self._frontier[i+1]) == 1
                        and self._frontier[i+1][0] in self._frontier[i]):
                        # We need to connect to the element to the right.
                        # Keep lines straight by connecting directly and
                        # avoiding immediate expand/contract.
                        name = self._frontier[i+1][0]
                        self._frontier[i].remove(name)

                        self._write_edge("\\", i+1)
                        for c in range(i+1, len(self._frontier)):
                            self._write_edge("| ", c )
                        self._out.write("\n")

                    else:
                        # Just allow the expansion here.
                        name = self._frontier[i].pop(0)
                        deps = [name]
                        self._write_edge("\\", i)
                        for c in range(i+1, len(self._frontier)):
                            self._write_edge(" \\", c)
                        self._out.write("\n")
                        self._connect_deps(i, deps, True, "expansion")

                # Handle any remaining back edges to the right
                j = i+1
                while j < len(self._frontier):
                    deps = self._frontier.pop(j)
                    if not self._connect_deps(j, deps, True, "rem_back"):
                        j += 1

            else:
                name = topo_order.pop()
                node = self._nodes[name]

                # Find the next node in topo order and remove it from
                # the frontier. Since specs are single-rooted DAGs,
                # the node is always there. If the graph had multiple
                # roots, we'd need to handle that case case of a new root.
                i = find(self._frontier, lambda f: name in f)
                self._frontier.pop(i)

                self._indent()
                for c in range(i):
                    self._write_edge("| ", c)
                self._out.write("%s " % self.node_character)
                for c in range(i, len(self._frontier)):
                    self._write_edge("| ", c)
                self._out.write(" %s\n" % name)

                if node.dependencies:
                    self._add_deps_to_frontier(node, i)
                elif self._frontier:
                    self._indent()
                    for c in range(i):
                        self._write_edge("| ", c)
                    for c in range(i, len(self._frontier)):
                        self._write_edge(" /", c)
                    self._out.write("\n")


def graph_ascii(spec, **kwargs):
    node_character = kwargs.get('node', 'o')
    out            = kwargs.pop('out', None)
    debug          = kwargs.pop('debug', False)
    indent         = kwargs.pop('indent', 0)
    color          = kwargs.pop('color', None)
    check_kwargs(kwargs, graph_ascii)

    graph = AsciiGraph()
    graph.debug = debug
    graph.indent = indent
    graph.node_character = node_character

    graph.write(spec, color=color, out=out)



def graph_dot(*specs, **kwargs):
    """Generate a graph in dot format of all provided specs.

    Print out a dot formatted graph of all the dependencies between
    package.  Output can be passed to graphviz, e.g.:

        spack graph --dot qt | dot -Tpdf > spack-graph.pdf

    """
    out = kwargs.pop('out', sys.stdout)
    check_kwargs(kwargs, graph_dot)

    out.write('digraph G {\n')
    out.write('  label = "Spack Dependencies"\n')
    out.write('  labelloc = "b"\n')
    out.write('  rankdir = "LR"\n')
    out.write('  ranksep = "5"\n')
    out.write('\n')

    def quote(string):
        return '"%s"' % string

    if not specs:
        specs = [p.name for p in spack.db.all_packages()]
    else:
        roots = specs
        specs = set()
        for spec in roots:
            specs.update(Spec(s.name) for s in spec.normalized().traverse())

    deps = []
    for spec in specs:
        out.write('  %-30s [label="%s"]\n' % (quote(spec.name), spec.name))

        # Skip virtual specs (we'll find out about them from concrete ones.
        if spec.virtual:
            continue

        # Add edges for each depends_on in the package.
        for dep_name, dep in spec.package.dependencies.iteritems():
            deps.append((spec.name, dep_name))

        # If the package provides something, add an edge for that.
        for provider in set(s.name for s in spec.package.provided):
            deps.append((provider, spec.name))

    out.write('\n')

    for pair in deps:
        out.write('  "%s" -> "%s"\n' % pair)
    out.write('}\n')

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Property-based checking of the laws ``satisfies``, ``intersects`` and ``constrain`` obey.

A spec denotes the set of concrete specs it can be concretized to, which makes the three
operations set operations::

    a.satisfies(b)     a ⊆ b
    a.intersects(b)    a ∩ b ≠ ∅
    a.constrain(b)     a := a ∩ b

Ordered by ⊆ the specs are a preorder instead of a partial order: antisymmetry fails, since two
different states can satisfy each other, ``%foo`` and ``%%foo`` for one. Modulo mutual
satisfaction, the kernel of the preorder, the specs are a meet-semilattice and ``constrain``
computes the greatest lower bound, unique only up to the kernel. The laws are stated at that
level: results are compared with ``denote_the_same_set``, equality in the quotient, and the
``as_state`` laws pin which representative of its class the merge returns. That is a set of
laws, and this module checks them on specs it builds instead of on specs somebody listed. A
spec is drawn as one choice per
dimension out of a small alphabet ordered weakest first, and a term is either such a draw or the
meet of two terms. The meets matter: they are how the states only ``constrain`` produces are
reached, a target range narrowed from both sides or a virtual edge merged into its provider
edge, and those are the operands of the next ``constrain`` everywhere in the solver. Because a
case is a vector of indices and not a string, a failure shrinks to a minimal one by lowering
indices toward zero and by replacing a meet with one of its operands.

There are two passes. ``sweep`` takes one dimension at a time and enumerates its alphabet, which
is exhaustive instead of sampled and is where most of the laws break; it reports a law once per
dimension it breaks on, so a dimension being added is read even while an earlier one is broken.
``sample`` then draws across dimensions to reach the interactions a single dimension cannot show,
with the operands drawn related to each other and not apart, since two specs drawn independently
are almost always disjoint and a law about their meet then holds vacuously.

The greatest lower bound is checked against a universe of atoms: fully specified specs over a
small modelled fragment of the language. Over that fragment the law is a biconditional, an atom is
below the meet exactly when it is below both operands, which catches a meet that admits too much
and not only one that lost a solution.

Run it as a script::

    bin/spack python lib/spack/spack/test/spec_algebra_properties.py
    bin/spack python lib/spack/spack/test/spec_algebra_properties.py --seed 0 --iterations 20000
    bin/spack python lib/spack/spack/test/spec_algebra_properties.py --law exact_glb
    bin/spack python lib/spack/spack/test/spec_algebra_properties.py --list

Laws that are known not to hold are not switched off. Each has a predicate in ``GAPS`` saying
which behaviour accounts for a failure, and only failures no predicate explains are reported, so
the day a gap is closed the predicate stops matching anything and can be deleted.
"""

import argparse
import collections
import itertools
import random
import sys
from typing import Callable, Dict, List, NamedTuple, Optional, Sequence, Set, Tuple, Union

import spack.paths
import spack.repo
from spack.error import SpecError, SpecSyntaxError
from spack.spec import Spec, meet

#: Set by a Ctrl-C during a run. The sweep and sample loops check it between cases and shrinking
#: cuts itself short, so everything found up to the interrupt is still shrunk as far as it got
#: and reported, instead of the run dying with a traceback and no report.
_INTERRUPTED = False


def _note_interrupt() -> None:
    global _INTERRUPTED
    if not _INTERRUPTED:
        print("interrupted, reporting what was found so far", flush=True)
    _INTERRUPTED = True


def denote_the_same_set(lhs: Optional[Spec], rhs: Optional[Spec]) -> bool:
    """Whether two specs denote the same set of concrete specs, or are both undefined. The two are
    not compared by state: an ordering of compiler flags survives the merge, so one set has more
    than one state."""
    if lhs is None or rhs is None:
        return lhs is rhs
    return lhs.satisfies(rhs) and rhs.satisfies(lhs)


class Dimension(NamedTuple):
    """One axis a spec constrains, as an alphabet of spec string fragments.

    ``constraints`` is ordered weakest first and its first entry is empty, meaning the dimension is
    left unconstrained, so shrinking is a matter of moving indices toward zero. ``points`` are the
    fully specified values of the dimension, used to build atoms; a dimension with no points is not
    part of the modelled fragment.
    """

    name: str
    constraints: Tuple[str, ...]
    points: Tuple[str, ...] = ()


#: Every dimension ``constrain`` merges. Fragments are joined with spaces in this order. Order
#: matters in one place: ``%`` binds to the node the last ``^`` introduced, so the dimensions
#: naming a direct dependency come before the ones naming a transitive one, which keeps their
#: fragments on the root. ``dep_shape`` reaches the other binding.
#:
#: A bare git ref, ``@git.main`` or a forty character hash, is left out. Comparing one looks the
#: ref up in the package's git history, and no mock package has one, so every law raises. The
#: ``@git.main=2.0`` form names the version the ref stands for and skips the lookup, so that one
#: is here.
DIMENSIONS: Tuple[Dimension, ...] = (
    Dimension("name", ("", "pkg-a", "builtin_mock.pkg-a", "pkg-b", "mpi", "mpich")),
    Dimension("namespace", ("", "namespace=builtin_mock", "namespace=other")),
    Dimension(
        "version",
        (
            "",
            "@1:3",
            "@:2",
            "@2:",
            "@1,3:4",
            "@=2.0",
            "@develop",
            "@main",
            "@1.2.3",
            "@1.2:1.2.5",
            "@git.main=2.0",
        ),
    ),
    Dimension("hash", ("", "/abc", "/abcdef")),
    Dimension(
        "bool_variant", ("", "+bvv", "~bvv", "++bvv", "~~bvv", "+lorem_ipsum", "~lorem_ipsum")
    ),
    Dimension(
        "single_variant",
        ("", "foobar=bar", "foobar=baz", "foobar=fee", "foobar==bar", "foobar:=bar", "foobar=*"),
    ),
    Dimension(
        "multi_variant",
        (
            "",
            "foo=bar",
            "foo=baz",
            "foo=bar,baz",
            "foo:=bar",
            "foo=none",
            "foo==bar",
            "foo=*",
            "libs=static",
            "libs=shared,static",
        ),
    ),
    Dimension(
        "reserved_variant",
        ("", "dev_path=/a", "dev_path=/b", "dev_path=none", "commit=" + "c" * 40),
    ),
    Dimension(
        "flags",
        (
            "",
            "cflags=-O2",
            "cflags=-g",
            "cflags==-O2",
            "ldflags=-L/x",
            "cxxflags=-O3",
            "cflags='-O2 -g'",
            "cflags='-g -O2'",
        ),
    ),
    Dimension("platform", ("", "platform=*", "platform=test", "platform=linux")),
    Dimension("os", ("", "os=*", "os=debian6", "os=redhat6")),
    Dimension(
        "target",
        (
            "",
            "target=*",
            "target=x86_64:",
            "target=:icelake",
            "target=x86_64:icelake",
            # bounded ranges whose endpoints are incomparable in one family, and a bound in
            # another family, so the range intersection walks its continue branches
            "target=x86_64:zen2",
            "target=:aarch64",
            # lower bounds that are incomparable with each other, one pair with a single least
            # target above both and one with two of them, so the intersection is a list
            "target=cascadelake:",
            "target=cannonlake:",
            "target=armv8.6a:,cortex_a72:",
            "target=haswell",
            "target=zen2",
            "target=haswell,zen2",
            "target=haswell,aarch64",
            "target=x86_64_v2",
            "target=broadwell:skylake",
            "target=aarch64",
        ),
    ),
    Dimension(
        "arch_triple",
        (
            "",
            "arch=test-debian6-haswell",
            "arch=linux-debian6-x86_64",
            "arch=haswell",
            "arch=*-*-x86_64",
        ),
    ),
    Dimension("patches", ("", "patches=abcdef", "patches:=abcdef1234567890")),
    Dimension(
        "direct_dep",
        (
            "",
            "%pkg-e",
            "%%pkg-e",
            "%pkg-e@1",
            "%[deptypes=build] pkg-e",
            "%[deptypes=link] pkg-e",
            "%[deptypes=run] pkg-e",
            "%[deptypes=build,link] pkg-e",
            "%[when='+bvv'] pkg-e",
            "%gcc",
            "%c=gcc",
            "%c,cxx=gcc",
            "%[virtuals=cxx] gcc",
            # the same name and a virtual, under a condition, so that meets draw two edges that
            # would be one node wherever both conditions hold but that no single edge can state
            "%[when='+bvv' virtuals=c] gcc",
            # a differently named provider of the same virtual, so that a meet can put two
            # direct providers of c on one node
            "%[virtuals=c] clang",
            "%%c=gcc",
            "%clang",
            "%gcc/abc",
            "%c=*",
        ),
    ),
    Dimension(
        "anonymous_dep",
        # the key-value states force the formatter to disambiguate the anonymous target from
        # the attributes of the node before it
        ("", "^*+bvv", "^*@1", "%*+bvv", "^* foo=bar", "^* cflags=-O2", "^* target=haswell"),
    ),
    Dimension(
        "transitive_dep",
        (
            "",
            "^pkg-b",
            "^pkg-b@1",
            "^pkg-b@2",
            "^[deptypes=build] pkg-b",
            "^[deptypes=run] pkg-b",
            "^[deptypes=test] pkg-b",
            "^[deptypes=build,link] pkg-b",
            "^pkg-b+bvv",
            "^pkg-b cflags=-O2",
            "^pkg-b target=haswell",
            "^pkg-b/abc",
            "^builtin_mock.pkg-b",
            "^pkg-b patches=abcdef",
        ),
    ),
    Dimension(
        "conditional_dep",
        (
            "",
            "^[when='+bvv'] pkg-c@1",
            "^[when='~bvv'] pkg-c@2",
            "^[when='+bvv' deptypes=build] pkg-c",
            "^[when='foobar=bar'] pkg-c",
            "^[when='@1,2'] pkg-c",
            # conditions that are themselves edges, so activating one is a statement about
            # another dependency instead of about the node
            "^[when='^pkg-b@2'] pkg-c",
            "^[when='%c'] pkg-c",
            # a conditional provider, which contradicts an unconditional provider of the same
            # virtual only where the condition is forced
            "^[when='+bvv' virtuals=mpi] zmpi",
        ),
    ),
    Dimension(
        "virtual_dep",
        (
            "",
            "^mpi",
            "^mpi@3",
            "^mpi+debug",
            "^[virtuals=mpi] mpich",
            "^[virtuals=mpi] mpich@3",
            # a second version of one provider, so that a pair of edges that can only be one node
            # with targets that cannot be one node is drawn at all
            "^[virtuals=mpi] mpich@4",
            # a second virtual from the same provider, and an edge listing both at once: the
            # single edge bridges two parallel edges that share no role with each other, which is
            # the smallest group the pairwise disjointness check does not reach
            "^[virtuals=lapack] mpich@4",
            "^mpi,lapack=mpich",
            "^[virtuals=mpi] mpich+debug",
            "^[virtuals=mpi] zmpi",
            "^mpi@:3",
            "^blas",
            "^blas,lapack=openblas-with-lapack",
            "^[virtuals=blas] openblas",
            "^[virtuals=mpi] mpich2@1.2",
            "^java@11",
        ),
    ),
    Dimension(
        "dep_shape",
        (
            "",
            "^pkg-b %pkg-e",
            "^pkg-b %gcc",
            "^pkg-b %gcc@2",
            "^pkg-b ^pkg-c %pkg-e",
            "%pkg-b ^pkg-b",
            "^[when='+bvv'] pkg-b ^[when='~bvv'] pkg-b",
            "^[deptypes=build] pkg-b ^[deptypes=link] pkg-b",
            "^[virtuals=mpi] mpich ^mpi",
            "^blas,lapack=openblas-with-lapack ^blas",
            "^pkg-b ^pkg-c ^pkg-e",
            # both halves of a bridgeable pair in one leaf, so two-operand laws reach it without
            # having to draw it as a meet
            "^[virtuals=mpi] mpich@3 ^[virtuals=lapack] mpich@4",
            # likewise for two direct providers of one virtual: a node satisfies both conditions
            # only once something narrows it to +bvv, which no single meet of two draws reaches
            "%[when='+bvv' virtuals=c] gcc %[virtuals=c] clang",
        ),
    ),
)

#: The fragment of the language the atoms model. Every dimension here has points, and the points
#: pin the dimension completely, so the product of them is a set of maximal specs. Variant names
#: and types follow the mock package definition of pkg-a: bvv is boolean and foo is multi-valued.
#: As above, ``direct_dep`` comes before ``dep`` so its fragment stays on the root instead of
#: binding to the node the ``^`` introduced.
MODELLED_DIMENSIONS: Tuple[Dimension, ...] = (
    Dimension("name", ("", "pkg-a", "pkg-c"), ("pkg-a", "pkg-c")),
    Dimension(
        "version",
        ("", "@1:2", "@2:", "@:1", "@=1.0", "@=2.0", "@=3.0"),
        ("@=1.0", "@=2.0", "@=3.0"),
    ),
    Dimension("bool_variant", ("", "+bvv", "~bvv"), ("+bvv", "~bvv")),
    Dimension(
        "multi_variant",
        ("", "foo=bar", "foo=baz", "foo=bar,baz", "foo:=bar", "foo:=bar,baz"),
        ("foo:=bar", "foo:=baz", "foo:=bar,baz"),
    ),
    Dimension(
        "target",
        (
            "",
            "target=x86_64:",
            "target=:zen2",
            "target=haswell",
            "target=zen2",
            "target=ppc64le:",
            # incomparable lower bounds, with icelake below among the points as the witness that
            # they overlap
            "target=cascadelake:",
            "target=cannonlake:",
        ),
        ("target=haswell", "target=zen2", "target=power9le", "target=icelake"),
    ),
    Dimension("direct_dep", ("", "%pkg-e", "%pkg-e@1"), ("", "%pkg-e@=1.0")),
    Dimension(
        "dep",
        ("", "^pkg-b", "^pkg-b@1", "^pkg-b@:1", "^pkg-b@2"),
        ("", "^pkg-b@=1.0", "^pkg-b@=2.0"),
    ),
)


#: How many dimensions a drawn spec constrains, as a probability per dimension. One is picked per
#: iteration, so both nearly bare specs and heavily constrained ones come up.
DENSITIES = (0.08, 0.15, 0.3, 0.5)


class Leaf(NamedTuple):
    """One choice per dimension, as indices into their alphabets."""

    indices: Tuple[int, ...]


class Node(NamedTuple):
    """The meet of two terms, which is how a state only ``constrain`` produces is reached."""

    left: "Term"
    right: "Term"


Term = Union[Leaf, Node]


def render(term: Term, dimensions: Sequence[Dimension]) -> str:
    """The term as a readable expression, a spec string or a meet of two of them."""
    if isinstance(term, Node):
        return f"meet({render(term.left, dimensions)}, {render(term.right, dimensions)})"
    return "'{}'".format(spec_string(term, dimensions))


def spec_string(leaf: Leaf, dimensions: Sequence[Dimension]) -> str:
    """The chosen fragments, joined. The parser takes them in any order, so the order of the
    dimensions only affects how a reported case reads."""
    fragments = []
    for dimension, index in zip(dimensions, leaf.indices):
        if dimension.constraints[index]:
            fragments.append(dimension.constraints[index])
    return " ".join(fragments)


def build(term: Term, dimensions: Sequence[Dimension]) -> Optional[Spec]:
    """The spec a term denotes, or None if it does not parse or the meet is empty. Not every
    combination of fragments is a well formed spec, and not every meet is inhabited."""
    if isinstance(term, Node):
        left = build(term.left, dimensions)
        right = build(term.right, dimensions)
        if left is None or right is None:
            return None
        return meet(left, right)
    try:
        return Spec(spec_string(term, dimensions))
    except (SpecError, SpecSyntaxError):
        return None


def draw_leaf(
    rng: random.Random,
    dimensions: Sequence[Dimension],
    density: float,
    focus: Optional[Sequence[int]],
) -> Leaf:
    """A leaf. Under a focus it constrains nothing outside the focused dimensions, which may take
    any value in their alphabet including the empty one. Without a focus every dimension is
    constrained with probability ``density``."""
    indices = []
    for position, dimension in enumerate(dimensions):
        if focus is not None:
            index = rng.randrange(len(dimension.constraints)) if position in focus else 0
        elif rng.random() < density:
            index = rng.randrange(1, len(dimension.constraints))
        else:
            index = 0
        indices.append(index)
    return Leaf(tuple(indices))


def draw_term(
    rng: random.Random,
    dimensions: Sequence[Dimension],
    density: float,
    depth: int,
    focus: Optional[Sequence[int]],
) -> Term:
    """A leaf, or the meet of two shallower terms."""
    if depth <= 0 or rng.random() < 0.5:
        return draw_leaf(rng, dimensions, density, focus)
    left = draw_term(rng, dimensions, density, depth - 1, focus)
    right = draw_term(rng, dimensions, density, depth - 1, focus)
    return Node(left, right)


def draw_focus(rng: random.Random, dimensions: Sequence[Dimension]) -> Optional[Tuple[int, ...]]:
    """The one or two dimensions the next case is confined to, or None to draw across all of them.

    Spreading the budget evenly over a dozen dimensions at once buries the small cases. A law that
    breaks on two target ranges is checked on two specs that both constrain the target in maybe a
    tenth of the draws, and only after everything else they constrain has already agreed. Confining
    a case to one dimension gives each of them its turn at the density where a law with a satisfies
    hypothesis has something to say; confining it to two is what puts a pair of them in a position
    to interact. The rest of the time nothing is confined, which is what reaches the interactions
    nobody thought to pair up.
    """
    if rng.random() < 0.4:
        return None
    first = rng.randrange(len(dimensions))
    if rng.random() < 0.5:
        return (first,)
    return (first, rng.randrange(len(dimensions)))


def draw_operands(
    rng: random.Random,
    law: "Law",
    dimensions: Sequence[Dimension],
    density: float,
    depth: int,
    focus: Optional[Sequence[int]],
) -> List[Term]:
    """The operands to check a law on.

    Drawing them independently finds almost nothing. With a dozen dimensions in play two specs
    drawn apart disagree somewhere almost every time, so they are disjoint, and a law about their
    meet holds vacuously. Operands are therefore drawn related to each other in two ways.

    Half the time they are all narrowings of a shared base, which makes them overlap often
    enough that the meet has something in it. And most of the time the first ``law.chain`` of them
    are built as a descending chain, each the meet of the previous with something fresh, which puts
    them in the order a law whose hypothesis is a satisfies relation is looking for, by
    construction. Not always, though: a chain only ever runs from a spec to a narrowing of it, so a
    law that is broken by two specs comparable for a reason the meet does not produce, an unnamed
    spec against a named one being the case in point, is only reached by drawing them apart.
    """
    base = None
    if rng.random() < 0.5:
        base = draw_term(rng, dimensions, density, depth, focus)

    terms: List[Term] = []
    if law.chain and rng.random() < 0.6:
        chain = [base if base is not None else draw_term(rng, dimensions, density, depth, focus)]
        while len(chain) < law.chain:
            chain.append(Node(chain[-1], draw_term(rng, dimensions, density, depth, focus)))
        terms = list(reversed(chain))

    while len(terms) < law.arity:
        drawn = draw_term(rng, dimensions, density, depth, focus)
        terms.append(drawn if base is None else Node(base, drawn))
    return terms


def smaller_terms(term: Term) -> List[Term]:
    """Terms to try in place of this one while shrinking, roughly smallest first."""
    result: List[Term] = []
    if isinstance(term, Node):
        result.append(term.left)
        result.append(term.right)
        for smaller in smaller_terms(term.left):
            result.append(Node(smaller, term.right))
        for smaller in smaller_terms(term.right):
            result.append(Node(term.left, smaller))
        return result
    for position, index in enumerate(term.indices):
        if index == 0:
            continue
        indices = list(term.indices)
        indices[position] = 0
        result.append(Leaf(tuple(indices)))
        if index > 1:
            indices[position] = index - 1
            result.append(Leaf(tuple(indices)))
    return result


def shrink(terms: List[Term], law: "Law", dimensions: Sequence[Dimension], universe) -> List[Term]:
    """Replace each term with the smallest one that keeps the law failing. Terminates because
    every candidate is strictly smaller than what it replaces.

    A candidate that no longer satisfies the law's hypothesis stops failing it, so shrinking a
    chain of operands cannot silently break the ordering the law was drawn to check.
    """
    current = list(terms)
    improved = True
    try:
        while improved:
            improved = False
            for position in range(len(current)):
                for candidate in smaller_terms(current[position]):
                    attempt = list(current)
                    attempt[position] = candidate
                    if evaluate(law, attempt, dimensions, universe):
                        current = attempt
                        improved = True
                        break
    except KeyboardInterrupt:
        _note_interrupt()
    return current


# Where the laws do not hold. Each predicate says a failure of the law is accounted for by the
# behaviour its docstring describes, and a failure no predicate explains is a finding. They are
# of two kinds, split in ``GAPS`` below: most describe what a spec means, so the law could only
# be closed by changing what a spec is; the last two describe what this checker can represent,
# and could be closed here without touching a spec.


def gap_propagation(specs: Sequence[Spec]) -> bool:
    """A propagating variant constrains transitive dependencies, which satisfies cannot check
    structurally, so it falls back to non-contradiction and the subset laws do not apply."""
    for spec in specs:
        for value in spec.variants.values():
            if value.propagate:
                return True
    return False


def gap_flag_propagation(specs: Sequence[Spec]) -> bool:
    """Whether a flag propagates is invisible to satisfies, and merging a propagating flag with a
    plain one of the same value demotes it, so a spec can be rewritten by a constraint it already
    satisfies."""
    for spec in specs:
        for flags in spec.compiler_flags.values():
            for flag in flags:
                if flag.propagate:
                    return True
    return False


def gap_edge_propagation(specs: Sequence[Spec]) -> bool:
    """Whether an edge propagates is left out of both satisfies and equality, but the merge takes
    the propagating policy of the two, so a spec is rewritten by a constraint it already
    satisfies."""
    policies = set()
    for spec in specs:
        for edge in spec.edges_to_dependencies():
            policies.add(edge.propagation)
    return len(policies) > 1


def gap_nested_direct_edge(specs: Sequence[Spec]) -> bool:
    """A %-edge chains onto whichever ^ dependency last set the anchor, so it can land on a node
    other than the root. satisfies reaches it anyway: its BFS does not stop at the first level.
    constrain only ever compares edges position by position and never descends into a
    dependency's own edges, so the two disagree on a spec built this way."""
    for spec in specs:
        for node in spec.traverse(root=False):
            if any(edge.direct for edge in node.edges_to_dependencies()):
                return True
    return False


def gap_dependency_of_a_direct_dependency(specs: Sequence[Spec]) -> bool:
    """The formatter descends into a dependency it printed with '^' and stops at one it printed
    with '%', so a node reached by a direct edge loses its own dependencies in str(): a spec whose
    root depends directly on pkg-b, which in turn depends on pkg-e, prints as '%pkg-b', which
    denotes more than it does."""
    for spec in specs:
        for node in spec.traverse():
            for edge in node.edges_to_dependencies():
                if edge.direct and edge.spec.edges_to_dependencies():
                    return True
    return False


def gap_split_conditional_edges(specs: Sequence[Spec]) -> bool:
    """Two or more edges to one package under different when conditions can, together, be implied
    by a single broader edge to that package elsewhere - one edge for '+v' and one for '~v'
    together cover every case a single unconditional edge would, say. constrain() does not pair
    edges: it unions the operands' edge lists and drops any edge implied by another, but
    implication is checked pairwise, one edge against one edge, so several of them jointly implying
    a single broader one goes undetected. The union is still correct - the broader edge is still
    there, still true, still existentially satisfied by anything that satisfies the two narrower
    ones - it is just not maximally reduced. This is a deliberate simplicity tradeoff, and the laws
    it is excused from are the ones checking structural minimality, not semantic equivalence."""
    for spec in specs:
        by_name: Dict[str, Set[str]] = collections.defaultdict(set)
        for node in spec.traverse():
            for edge in node.edges_to_dependencies():
                by_name[edge.spec.name].add(str(edge.when))
        for whens in by_name.values():
            if len(whens) > 1:
                return True
    return False


def gap_multiple_instances_of_a_dependency(specs: Sequence[Spec]) -> bool:
    """Two indirect edges to one name play no role in common, so they may be two nodes:
    operands each pinning a different one (e.g. '^pkg-b@1' and '^pkg-b@2') intersect through two
    separate concrete nodes of that name. The atom universe draws one point per dimension, so it
    has no way to build such a multi-instance witness - the gap is in what the atoms can
    represent, not in intersects/constrain, which the non-modelled laws already exercise on such
    specs."""
    seen: Dict[str, Set[str]] = collections.defaultdict(set)
    for spec in specs:
        for node in spec.traverse():
            for edge in node.edges_to_dependencies():
                if not edge.direct:
                    seen[edge.spec.name].add(str(edge.spec))
    return any(len(variants) > 1 for variants in seen.values())


def gap_forced_second_provider(specs: Sequence[Spec]) -> bool:
    """A node that satisfies the conditions of two differently named direct edges providing one
    virtual denotes the empty set: both providers apply in every solution, and a node takes
    each virtual from exactly one of its direct dependencies. Such a spec is constructible all
    the same, because conditions on edges are compared with each other, never evaluated against
    the node, when an edge is added - so intersects honestly reports that nothing is in the
    set, itself included. The laws excused here assume every constructible spec denotes
    something. Indirect edges are exempt: each is matched anywhere in the transitive graph, so
    two providers of one virtual may be two nodes."""
    for spec in specs:
        for node in spec.traverse():
            providers: Dict[str, List] = collections.defaultdict(list)
            for edge in node.edges_to_dependencies():
                if not edge.direct:
                    continue
                for virtual in edge.virtuals:
                    providers[virtual].append(edge)
            for edges in providers.values():
                for lhs, rhs in itertools.combinations(edges, 2):
                    if (
                        lhs.spec.name != rhs.spec.name
                        and node.satisfies(lhs.when, deps=False)
                        and node.satisfies(rhs.when, deps=False)
                    ):
                        return True
    return False


def gap_namespace(specs: Sequence[Spec]) -> bool:
    """A spec that leaves the namespace unset is read as satisfying one that names it, so the
    merge fills the namespace in without the spec having been narrowed. Any node can name a
    namespace, so every node counts, keyed by name so two nodes of one package disagreeing is
    seen and two different packages each naming their own namespace is not. A namespace on an
    anonymous node lands on whatever node it merges into, so it counts against every name."""
    namespaces: Dict[Optional[str], Set[Optional[str]]] = collections.defaultdict(set)
    anonymous: Set[Optional[str]] = set()
    for spec in specs:
        for node in spec.traverse():
            namespaces[node.name].add(node.namespace)
            if not node.name and node.namespace is not None:
                anonymous.add(node.namespace)
    for name, values in namespaces.items():
        if name:
            values = values | anonymous
        if len(values) > 1:
            return True
    return False


def gap_flag_order(specs: Sequence[Spec]) -> bool:
    """Compiler flags merge as an order preserving union, so two operands with different flags of
    the same name meet to different states depending on the order."""
    values: Dict[str, set] = collections.defaultdict(set)
    for spec in specs:
        for name, flags in spec.compiler_flags.items():
            for flag in flags:
                values[name].add(str(flag))
    for name in values:
        if len(values[name]) > 1:
            return True
    return False


GAPS: Dict[str, Callable[[Sequence[Spec]], bool]] = {
    # What a spec means: behaviours, closable only by changing what a spec is.
    "propagation": gap_propagation,
    "flag_propagation": gap_flag_propagation,
    "edge_propagation": gap_edge_propagation,
    "nested_direct_edge": gap_nested_direct_edge,
    "dependency_of_a_direct_dependency": gap_dependency_of_a_direct_dependency,
    "split_conditional_edges": gap_split_conditional_edges,
    "namespace": gap_namespace,
    "flag_order": gap_flag_order,
    # What this checker can represent: the atom universe cannot draw the witness, or the
    # operand denotes the empty set the laws quantify past. Closable here, without touching
    # a spec.
    "multiple_instances_of_a_dependency": gap_multiple_instances_of_a_dependency,
    "forced_second_provider": gap_forced_second_provider,
}


# The laws. Each takes as many specs as its arity and returns None, or a message saying what went
# wrong. Anything a law needs beyond its operands, it computes itself.


def law_reflexive(specs: List[Spec]) -> Optional[str]:
    spec = specs[0]
    if not spec.satisfies(spec):
        return "does not satisfy itself"
    if not spec.intersects(spec):
        return "does not intersect itself"
    return None


def law_self_meet(specs: List[Spec]) -> Optional[str]:
    spec = specs[0]
    before = spec.to_dict()
    try:
        changed = spec.constrain(spec)
    except SpecError as e:
        return f"constraining with itself raised {type(e).__name__}"
    if changed is not False:
        return "constrained with itself reported a change"
    if spec.to_dict() != before:
        return f"constrained with itself became '{spec}'"
    return None


def law_str_round_trip(specs: List[Spec]) -> Optional[str]:
    spec = specs[0]
    printed = str(spec)
    try:
        if denote_the_same_set(spec, Spec(printed)):
            return None
    except Exception as e:
        return f"prints as '{printed}', which does not parse: {type(e).__name__}: {e}"
    return f"prints as '{printed}', which denotes a different set"


def law_dict_round_trip(specs: List[Spec]) -> Optional[str]:
    spec = specs[0]
    reparsed = Spec.from_dict(spec.to_dict())
    if not denote_the_same_set(spec, reparsed):
        return f"comes back from to_dict as '{reparsed}', which denotes a different set"
    return None


def law_satisfies_implies_intersects(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    if lhs.satisfies(rhs) and not lhs.intersects(rhs):
        return "the first is inside the second but does not intersect it"
    return None


def law_intersects_is_symmetric(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    if lhs.intersects(rhs) != rhs.intersects(lhs):
        return f"intersects is {lhs.intersects(rhs)} one way and {rhs.intersects(lhs)} the other"
    return None


def law_intersects_agrees_with_constrain(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    intersects = lhs.intersects(rhs)
    if intersects is (meet(lhs, rhs) is not None):
        return None
    return f"intersects is {intersects} but constrain says {not intersects}"


def law_meet_is_a_lower_bound(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    result = meet(lhs, rhs)
    if result is None:
        return None
    if not result.satisfies(lhs):
        return f"their meet '{result}' is not inside the first"
    if not result.satisfies(rhs):
        return f"their meet '{result}' is not inside the second"
    return None


def law_meet_is_commutative(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    forward, backward = meet(lhs, rhs), meet(rhs, lhs)
    if denote_the_same_set(forward, backward):
        return None
    return f"the meet is '{forward}' one way and '{backward}' the other"


def law_meet_is_commutative_as_state(specs: List[Spec]) -> Optional[str]:
    """Stronger than the law above, and the one edges need. Two specs that denote the same set can
    still hash differently and serialize differently, so a merge whose result depends on the order
    of its operands is a spec whose identity depends on which side of a constrain it was on."""
    lhs, rhs = specs
    forward, backward = meet(lhs, rhs), meet(rhs, lhs)
    if forward is None or backward is None:
        return None
    if forward.to_dict() == backward.to_dict():
        return None
    return f"the meet is '{forward}' one way and '{backward}' the other, in different states"


def reversed_edge_order_copy(spec: Spec) -> Spec:
    """A copy in which every node lists its dependency names in reversed insertion order: the
    same set in a different storage order. This is the axis ``constrain`` iterates over, so a
    merge whose outcome depends on it is caught by meeting both orderings with a third spec."""
    clone = spec.copy(deps=True)
    for node in clone.traverse():
        items = list(node._dependencies.items())
        node._dependencies.clear()
        for name, edges in reversed(items):
            node._dependencies[name] = edges
    return clone


def law_edge_order_invariance(specs: List[Spec]) -> Optional[str]:
    """One spec stored with its edges in either order denotes the same set, gives the same
    intersects answer against a third spec, and meets it to the same state. The commutativity and
    absorption laws do not reach this: they compare two results of one storage order."""
    lhs, rhs = specs
    forward_rhs, backward_rhs = rhs, reversed_edge_order_copy(rhs)
    if not (forward_rhs.satisfies(backward_rhs) and backward_rhs.satisfies(forward_rhs)):
        return f"reversing the edge order changed the set: '{forward_rhs}'"
    if forward_rhs.intersects(lhs) != backward_rhs.intersects(lhs):
        return f"'{forward_rhs}' intersects '{lhs}' in one edge order and not the other"
    forward, backward = meet(lhs, forward_rhs), meet(lhs, backward_rhs)
    if forward is None or backward is None:
        if (forward is None) != (backward is None):
            return f"the meet with '{lhs}' is empty in one edge order and not the other"
        return None
    if forward.to_dict() != backward.to_dict():
        return (
            f"the meet with '{lhs}' is '{forward}' in one edge order and '{backward}', "
            f"in another state, in the other"
        )
    return None


def law_edge_maps_keyed_by_name(specs: List[Spec]) -> Optional[str]:
    """Every dependency map keys its edges by the name of the node the edge points at. A merge
    can rename that node, so the rename has to re-key the map of each dependent. A stale key is
    invisible to the full scans in ``_add_or_merge_edge`` but breaks every keyed lookup, like
    the one in ``_detach_edge``."""
    lhs, rhs = specs
    for spec in (lhs, rhs, meet(lhs, rhs)):
        if spec is None:
            continue
        for node in spec.traverse():
            for key, edges in node._dependencies.items():
                for edge in edges:
                    if edge.spec.name != key:
                        return (
                            f"'{spec}' keeps an edge to '{edge.spec.name}' under the key '{key}'"
                        )
    return None


def law_absorption_as_state(specs: List[Spec]) -> Optional[str]:
    """A spec already inside another is left alone by the merge, down to its state. This is the
    edge-level counterpart of the narrowing dimensions law: an edge the lhs already matches must
    not be copied in beside the edge matching it."""
    lhs, rhs = specs
    if not lhs.satisfies(rhs):
        return None
    before = lhs.to_dict()
    result = meet(lhs, rhs)
    if result is None:
        return "the first is inside the second but their meet is empty"
    if result.to_dict() != before:
        return f"the first is inside the second, but their meet is '{result}', in another state"
    return None


def law_meet_is_idempotent(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    if meet(lhs, rhs) is None:
        return None
    lhs.constrain(rhs)
    before = lhs.to_dict()
    if lhs.constrain(rhs) is not False:
        return "constraining twice reported a change the second time"
    if lhs.to_dict() != before:
        return f"constraining twice changed the result to '{lhs}'"
    return None


def law_absorption(specs: List[Spec]) -> Optional[str]:
    """A spec already inside another has nothing left to intersect."""
    lhs, rhs = specs
    if not lhs.satisfies(rhs):
        return None
    before = lhs.copy()
    result = meet(lhs, rhs)
    if result is None:
        return "the first is inside the second but their meet is empty"
    if not denote_the_same_set(result, before):
        return f"the first is inside the second but their meet is '{result}'"
    return None


def narrowing_dimensions(spec: Spec):
    """The state of the dimensions in which leaving a value unset is an absent constraint rather
    than a constraint satisfied by default, as a comparable snapshot."""
    variants = {}
    for name, value in spec.variants.items():
        variants[name] = str(value)
    flags = {}
    for name, values in spec.compiler_flags.items():
        flags[name] = [str(flag) for flag in values]
    return (str(spec.versions), variants, str(spec.architecture), flags, spec.abstract_hash)


def law_satisfies_leaves_narrowing_dimensions_alone(specs: List[Spec]) -> Optional[str]:
    """Absorption at the level of state instead of denotation. A spec already inside another
    has nothing left to intersect, so constraining it must not rewrite any dimension in which an
    unset value is an absent constraint. Names, namespaces and edges whose when condition
    does not apply are read as satisfied when left unset, so those are not compared."""
    lhs, rhs = specs
    if not lhs.satisfies(rhs):
        return None
    before = narrowing_dimensions(lhs)
    try:
        lhs.constrain(rhs)
    except SpecError:
        return None
    if narrowing_dimensions(lhs) != before:
        return f"the first is inside the second, but constraining rewrote it to '{lhs}'"
    return None


def law_satisfies_matches_the_atoms(specs: List[Spec], atoms: Sequence[Spec]) -> Optional[str]:
    """Satisfaction is subset, so a spec inside another one cannot hold an atom the other does not.
    The converse is not asserted: the modelled fragment does not separate every pair of specs, so
    two of them can hold the same atoms without one being inside the other."""
    lhs, rhs = specs
    if not lhs.satisfies(rhs):
        return None
    for atom in atoms:
        if atom.satisfies(lhs) and not atom.satisfies(rhs):
            return f"the first is inside the second, but holds '{atom}', which the second does not"
    return None


def law_meet_absorbs_itself(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    once = meet(lhs, rhs)
    if once is None:
        return None
    twice = meet(lhs, once)
    if not denote_the_same_set(once, twice):
        return f"meeting the first with their meet '{once}' gives '{twice}'"
    return None


def law_rhs_is_never_mutated(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    before = rhs.to_dict()
    try:
        lhs.constrain(rhs)
    except SpecError:
        pass
    if rhs.to_dict() != before:
        return f"constraining mutated the second into '{rhs}'"
    return None


def law_lhs_is_unchanged_when_constrain_raises(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    before = lhs.to_dict()
    try:
        lhs.constrain(rhs)
    except SpecError:
        if lhs.to_dict() != before:
            return f"a failed constrain left the first as '{lhs}'"
    return None


def law_changed_flag_is_honest(specs: List[Spec]) -> Optional[str]:
    lhs, rhs = specs
    before = lhs.to_dict()
    try:
        changed = lhs.constrain(rhs)
    except SpecError:
        return None
    if changed is not (lhs.to_dict() != before):
        return f"constrain returned {changed} and gave '{lhs}'"
    return None


def law_satisfies_is_transitive(specs: List[Spec]) -> Optional[str]:
    a, b, c = specs
    if a.satisfies(b) and b.satisfies(c) and not a.satisfies(c):
        return "the first is inside the second is inside the third, but not inside the third"
    return None


def law_meet_is_associative(specs: List[Spec]) -> Optional[str]:
    a, b, c = specs
    ab, bc = meet(a, b), meet(b, c)
    left = meet(ab, c) if ab is not None else None
    right = meet(a, bc) if bc is not None else None
    if denote_the_same_set(left, right):
        return None
    return f"grouping to the left gives '{left}' and to the right '{right}'"


def law_meet_is_monotonic(specs: List[Spec]) -> Optional[str]:
    a, b, c = specs
    if not a.satisfies(b):
        return None
    narrowed, widened = meet(a, c), meet(b, c)
    if narrowed is None:
        return None
    if widened is None:
        return "the first is inside the second and meets the third, but the second does not"
    if not narrowed.satisfies(widened):
        return (
            f"their meets with the third, '{narrowed}' and '{widened}', are the other way around"
        )
    return None


def law_congruence(specs: List[Spec]) -> Optional[str]:
    """Two specs denoting the same set meet a third one to the same set, which is what makes the
    meet well defined on the quotient. This is the law a representation that leaks through the
    meet breaks."""
    a, b, c = specs
    if not denote_the_same_set(a, b):
        return None
    left, right = meet(a, c), meet(b, c)
    if denote_the_same_set(left, right):
        return None
    return f"the first two denote the same set but meet the third as '{left}' and '{right}'"


def law_exact_glb(specs: List[Spec], atoms: Sequence[Spec]) -> Optional[str]:
    """An atom is below the meet exactly when it is below both operands. The forward direction
    catches a meet that admits too much, the backward one a meet that lost a solution."""
    lhs, rhs = specs
    result = meet(lhs, rhs)
    for atom in atoms:
        below_both = atom.satisfies(lhs) and atom.satisfies(rhs)
        below_meet = result is not None and atom.satisfies(result)
        if below_meet and not below_both:
            return f"their meet '{result}' admits '{atom}', which is outside one of them"
        if below_both and not below_meet:
            return f"'{atom}' is inside both, but not inside their meet '{result}'"
    return None


def law_intersection_is_witnessed(specs: List[Spec], atoms: Sequence[Spec]) -> Optional[str]:
    """Inside the modelled fragment every non-empty intersection holds an atom, so a claimed
    intersection with no witness means intersects is too permissive."""
    lhs, rhs = specs
    if not lhs.intersects(rhs):
        return None
    for atom in atoms:
        if atom.satisfies(lhs) and atom.satisfies(rhs):
            return None
    return "they claim to intersect, but no atom is inside both"


class Law(NamedTuple):
    name: str
    arity: int
    check: Callable[..., Optional[str]]
    #: Gaps that explain a failure of this law, as keys into GAPS.
    gaps: Tuple[str, ...] = ()
    #: Whether the law is stated over the modelled fragment and needs the atoms.
    modelled: bool = False
    #: How many of the leading operands to draw as a descending chain, for a law whose hypothesis
    #: is that they are ordered. Zero draws every operand independently.
    chain: int = 0


LAWS: Tuple[Law, ...] = (
    Law("reflexive", 1, law_reflexive, gaps=("propagation", "forced_second_provider")),
    Law("self_meet", 1, law_self_meet, gaps=("forced_second_provider",)),
    Law(
        "str_round_trip",
        1,
        law_str_round_trip,
        gaps=("dependency_of_a_direct_dependency", "nested_direct_edge", "propagation"),
    ),
    Law("dict_round_trip", 1, law_dict_round_trip, gaps=("propagation",)),
    Law(
        "satisfies_implies_intersects",
        2,
        law_satisfies_implies_intersects,
        gaps=("forced_second_provider",),
        chain=2,
    ),
    Law("intersects_is_symmetric", 2, law_intersects_is_symmetric),
    Law("intersects_agrees_with_constrain", 2, law_intersects_agrees_with_constrain),
    Law("meet_is_a_lower_bound", 2, law_meet_is_a_lower_bound, gaps=("propagation",)),
    Law("meet_is_commutative", 2, law_meet_is_commutative, gaps=("propagation", "flag_order")),
    Law(
        "meet_is_commutative_as_state",
        2,
        law_meet_is_commutative_as_state,
        gaps=(
            "propagation",
            "flag_propagation",
            "edge_propagation",
            "flag_order",
            "nested_direct_edge",
            "split_conditional_edges",
        ),
    ),
    Law("edge_order_invariance", 2, law_edge_order_invariance, gaps=("propagation",)),
    Law("edge_maps_keyed_by_name", 2, law_edge_maps_keyed_by_name),
    Law(
        "absorption_as_state",
        2,
        law_absorption_as_state,
        gaps=(
            "propagation",
            "flag_propagation",
            "edge_propagation",
            "namespace",
            "nested_direct_edge",
            "split_conditional_edges",
            "forced_second_provider",
        ),
        chain=2,
    ),
    Law("meet_is_idempotent", 2, law_meet_is_idempotent, gaps=("forced_second_provider",)),
    Law(
        "absorption",
        2,
        law_absorption,
        gaps=("propagation", "split_conditional_edges", "forced_second_provider"),
        chain=2,
    ),
    Law(
        "satisfies_leaves_narrowing_dimensions_alone",
        2,
        law_satisfies_leaves_narrowing_dimensions_alone,
        gaps=("propagation",),
        chain=2,
    ),
    Law(
        "meet_absorbs_itself",
        2,
        law_meet_absorbs_itself,
        gaps=("propagation", "forced_second_provider"),
    ),
    Law("rhs_is_never_mutated", 2, law_rhs_is_never_mutated),
    Law("lhs_is_unchanged_when_constrain_raises", 2, law_lhs_is_unchanged_when_constrain_raises),
    Law("changed_flag_is_honest", 2, law_changed_flag_is_honest),
    Law(
        "satisfies_is_transitive",
        3,
        law_satisfies_is_transitive,
        gaps=("propagation", "namespace"),
        chain=3,
    ),
    Law("meet_is_associative", 3, law_meet_is_associative, gaps=("propagation", "flag_order")),
    Law(
        "meet_is_monotonic",
        3,
        law_meet_is_monotonic,
        gaps=("propagation", "namespace", "flag_order"),
        chain=2,
    ),
    Law("congruence", 3, law_congruence, gaps=("propagation", "namespace", "flag_order"), chain=2),
    Law("exact_glb", 2, law_exact_glb, modelled=True),
    Law(
        "intersection_is_witnessed",
        2,
        law_intersection_is_witnessed,
        ("multiple_instances_of_a_dependency",),
        modelled=True,
    ),
    Law("satisfies_matches_the_atoms", 2, law_satisfies_matches_the_atoms, modelled=True, chain=2),
)


def atoms() -> List[Spec]:
    """The fully specified specs of the modelled fragment, one per combination of points."""
    alphabets = []
    for dimension in MODELLED_DIMENSIONS:
        alphabets.append(dimension.points)
    result = []
    for combination in itertools.product(*alphabets):
        fragments = []
        for fragment in combination:
            if fragment:
                fragments.append(fragment)
        result.append(Spec(" ".join(fragments)))
    return result


def unparseable_fragments() -> List[str]:
    """The alphabet entries that do not build a spec on their own.

    ``build`` returns None for anything that does not parse, and a case that does not build is
    not a failure, so a fragment with a typo in it would be drawn forever and checked never. Every
    entry has to stand on its own, since that is how the sweep uses it.
    """
    broken = []
    for dimensions in (DIMENSIONS, MODELLED_DIMENSIONS):
        for dimension in dimensions:
            for fragment in dimension.constraints + dimension.points:
                if not fragment:
                    continue
                try:
                    Spec(fragment)
                except (SpecError, SpecSyntaxError) as e:
                    broken.append(f"{dimension.name}: '{fragment}' ({type(e).__name__})")
    return broken


class Failure(NamedTuple):
    law: str
    terms: List[Term]
    message: str
    dimensions: Tuple[Dimension, ...]
    #: The dimension the case was confined to, for a failure the sweep found.
    dimension: Optional[str] = None

    def report(self) -> str:
        operands = ", ".join(render(term, self.dimensions) for term in self.terms)
        where = f" [{self.dimension}]" if self.dimension else ""
        return f"{self.law}{where}: {operands}\n  {self.message}"


def explained_by_a_gap(law: Law, specs: List[Spec]) -> Optional[str]:
    """The gap that accounts for a failure of this law on these operands, if there is one.

    A predicate that raises is passed over instead of left to propagate: some of them meet their
    operands, and the empty set the meet of two operands can denote is outside the universe a
    predicate reading plain spec state quantifies over.
    """
    for name in law.gaps:
        try:
            matched = GAPS[name](specs)
        except SpecError:
            continue
        if matched:
            return name
    return None


def build_operands(
    terms: Sequence[Term], dimensions: Sequence[Dimension]
) -> Union[List[Spec], str, None]:
    """The specs the terms denote, None if one of them does not build, or a message if building
    one raised something other than a ``SpecError``.

    A term that does not build is not a failure: not every combination of fragments parses, and
    not every meet is inhabited. A term that cannot be built at all is a different matter, since
    parsing a spec string and meeting two specs are the operations under test here as much as the
    laws are.
    """
    specs = []
    for term in terms:
        try:
            spec = build(term, dimensions)
        except Exception as e:  # noqa: BLE001
            return f"building it raised {type(e).__name__}: {str(e).splitlines()[0]}"
        if spec is None:
            return None
        specs.append(spec)
    return specs


def buildable_parts(terms: Sequence[Term], dimensions: Sequence[Dimension]) -> List[Spec]:
    """Every spec a term or a subterm of one denotes and that builds.

    This is what a failure to build is classified with. The operands are not available then, but
    the parts that did build are, and a gap predicate matches on those: a meet that produced a
    spec ``add_dependency_edge`` rejects builds fine on its own and only raises when the meet
    above it tries to copy it.
    """
    specs: List[Spec] = []

    def visit(term: Term) -> None:
        if isinstance(term, Node):
            visit(term.left)
            visit(term.right)
        try:
            spec = build(term, dimensions)
        except Exception:  # noqa: BLE001
            return
        if spec is not None:
            specs.append(spec)

    for term in terms:
        visit(term)
    return specs


def evaluate(law: Law, terms: List[Term], dimensions: Sequence[Dimension], universe) -> bool:
    """Whether the law fails on these terms for a reason no gap explains."""
    built = build_operands(terms, dimensions)
    if built is None:
        return False
    if isinstance(built, str):
        return explained_by_a_gap(law, buildable_parts(terms, dimensions)) is None
    return run(law, built, universe) is not None


def run(law: Law, specs: List[Spec], universe) -> Optional[str]:
    """The law's complaint about these specs, or None if it holds or a gap explains the failure.
    The specs are copied, since several of the laws constrain in place.

    Any exception raised while checking is a failure of the same kind as a law that comes out
    false, so it is turned into a message instead of left to propagate, which would hide every
    case after it and leave it unshrunk. That includes an exception from the copy: a spec that was
    built cannot fail to be duplicated, unless the merge that built it produced a state
    add_dependency_edge rejects, which is a gap like any other and is classified as one below.
    """
    try:
        operands = [spec.copy() for spec in specs]
        if law.modelled:
            message = law.check(operands, universe)
        else:
            message = law.check(operands)
    except Exception as e:  # noqa: BLE001
        message = f"raised {type(e).__name__}: {str(e).splitlines()[0]}"
    if message is None:
        return None
    if explained_by_a_gap(law, specs) is not None:
        return None
    return message


def report_failure(
    law: Law,
    terms: List[Term],
    dimensions: Sequence[Dimension],
    universe,
    dimension: Optional[str] = None,
) -> Failure:
    """Shrink a failing case and describe what is left of it."""
    smallest = shrink(terms, law, dimensions, universe)
    built = build_operands(smallest, dimensions)
    assert built is not None, "a case that failed a law has to build"
    if isinstance(built, str):
        message = built
    else:
        message = run(law, built, universe) or ""
    return Failure(law.name, smallest, message, tuple(dimensions), dimension)


def sweep(
    laws: Sequence[Law],
    universe: Optional[List[Spec]] = None,
    only: Optional[Sequence[str]] = None,
) -> List[Failure]:
    """Check every law on every combination of values of one dimension at a time.

    The alphabets are small enough that one dimension at a time is exhaustive instead of sampled.
    Most of the laws break within a single dimension, and a sweep reports that the first time it
    runs. Two dimensions interacting is what it does not reach, and what ``sample`` is for.

    A law is reported once per dimension it breaks on, not once overall. A law tends to
    break on more than one, and stopping at the first would leave every later dimension unchecked
    for as long as an earlier one is broken, which is exactly when a dimension being added needs
    to be read. ``only`` narrows the sweep to the named dimensions.
    """
    if universe is None:
        universe = atoms()
    failures: List[Failure] = []
    for law in laws:
        dimensions = MODELLED_DIMENSIONS if law.modelled else DIMENSIONS
        for position, dimension in enumerate(dimensions):
            if _INTERRUPTED:
                return failures
            if only is not None and dimension.name not in only:
                continue
            try:
                for choice in itertools.product(
                    range(len(dimension.constraints)), repeat=law.arity
                ):
                    terms: List[Term] = []
                    for index in choice:
                        indices = [0] * len(dimensions)
                        indices[position] = index
                        terms.append(Leaf(tuple(indices)))
                    if not evaluate(law, terms, dimensions, universe):
                        continue
                    failures.append(
                        report_failure(law, terms, dimensions, universe, dimension.name)
                    )
                    break
            except KeyboardInterrupt:
                _note_interrupt()
    return failures


def sample(
    seed: int,
    iterations: int,
    laws: Sequence[Law],
    density: float = 0.0,
    depth: int = 1,
    universe: Optional[List[Spec]] = None,
) -> List[Failure]:
    """Check every law on ``iterations`` generated cases each, shrinking whatever fails. Reports
    one failure per law, since a broken law tends to fail on almost everything.

    A density of zero draws one per iteration. Sparse specs and dense ones fail different laws: a
    spec constraining one dimension is the only kind that ends up comparable to another one, while
    a dense one is what makes two dimensions interact.
    """
    rng = random.Random(seed)
    if universe is None:
        universe = atoms()
    failures: List[Failure] = []
    broken: Set[str] = set()
    heartbeat = max(1, iterations // 20)
    for iteration in range(iterations):
        if _INTERRUPTED:
            break
        if iteration and iteration % heartbeat == 0:
            print(f"  {iteration}/{iterations} cases, {len(broken)} law(s) broken", flush=True)
        try:
            for law in laws:
                if law.name in broken:
                    continue
                dimensions = MODELLED_DIMENSIONS if law.modelled else DIMENSIONS
                chosen = density or rng.choice(DENSITIES)
                focus = draw_focus(rng, dimensions)
                terms = draw_operands(rng, law, dimensions, chosen, depth, focus)
                if not evaluate(law, terms, dimensions, universe):
                    continue
                failures.append(report_failure(law, terms, dimensions, universe))
                broken.add(law.name)
        except KeyboardInterrupt:
            _note_interrupt()
    return failures


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=2000, help="cases per law")
    parser.add_argument("--law", action="append", help="check only this law, repeatable")
    parser.add_argument(
        "--dimension", action="append", help="sweep only this dimension, repeatable"
    )
    parser.add_argument("--list", action="store_true", help="list the laws and exit")
    parser.add_argument(
        "--depth", type=int, default=2, help="how deeply operands may be meets of other operands"
    )
    parser.add_argument(
        "--density",
        type=float,
        default=0.0,
        help="probability that a dimension is constrained, zero to vary it per iteration",
    )
    args = parser.parse_args(argv)

    # Line buffering, so progress and failures land in a pipe or log as they happen and an
    # interrupted run has printed everything it reported.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)

    if args.list:
        for law in LAWS:
            gaps = ", ".join(law.gaps) or "none"
            print(f"{law.name:40s} arity {law.arity}  known gaps: {gaps}")
        return 0

    laws = LAWS
    if args.law:
        by_name = {law.name: law for law in LAWS}
        unknown = [name for name in args.law if name not in by_name]
        if unknown:
            parser.error(f"unknown law(s): {', '.join(unknown)}")
        laws = tuple(by_name[name] for name in args.law)

    if args.dimension:
        known = {d.name for d in DIMENSIONS} | {d.name for d in MODELLED_DIMENSIONS}
        unknown = [name for name in args.dimension if name not in known]
        if unknown:
            parser.error(f"unknown dimension(s): {', '.join(unknown)}")

    with spack.repo.use_repositories(spack.repo.from_path(spack.paths.mock_packages_path)):
        broken_fragments = unparseable_fragments()
        if broken_fragments:
            for fragment in broken_fragments:
                print(f"alphabet entry does not parse: {fragment}")
            return 1

        universe = atoms()
        print(f"{len(laws)} laws, {len(universe)} atoms")
        print("sweeping one dimension at a time")
        failures = sweep(laws, universe, args.dimension)
        if not failures and not _INTERRUPTED:
            print(f"sampling across dimensions, {args.iterations} cases per law")
            failures = sample(
                args.seed, args.iterations, laws, args.density, args.depth, universe=universe
            )

    for failure in failures:
        print(failure.report())
    if failures:
        broken = len({failure.law for failure in failures})
        print(f"\n{len(failures)} failure(s) in {broken} law(s)")
        return 1
    if _INTERRUPTED:
        print("no failures up to the interrupt")
        return 130
    print("no failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())

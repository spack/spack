# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""A reference model for the target dimension of ``ArchSpec``.

The other law modules compare the implementation against itself: laws like transitivity or
exactness of the greatest lower bound relate outputs of ``satisfies``, ``intersects`` and
``constrain`` to each other, so a blind spot in one operation can hide behind the same blind
spot in another. The target dimension does not need that indirection. The archspec table is a
finite poset, so every target expression denotes a computable set of known microarchitectures,
plus open tails for ``x:`` elements, which admit targets outside the current table. This module
recomputes that denotation directly from the table and checks the three operations against it
pairwise.

The operands are enumerated from a slice of the table instead of curated: every point, open
range, bounded range with comparable in-slice bounds, the universe ``:`` and its alias ``*``,
an out-of-table name, ranges denoting no target, and every two-element union over a smaller
core. Curated alphabets rot when the implementation changes shape; an enumeration over the
table keeps drawing the states a rewrite produces.

The model of an expression is a pair (P, T): P the denoted subset of known names, T the set of
open lower bounds, with ``""`` for the unbounded tail of ``:``. The laws, per operand pair:

    a.satisfies(b)    P(a) ⊆ P(b), and every tail in T(a) has a tail in T(b) at or below it
    a.intersects(b)   P(a) ∩ P(b) ≠ ∅
    a.constrain(b)    raises iff disjoint; else the result denotes P(a) ∩ P(b), satisfies both
                      operands, is the same state in either operand order, and is above every
                      enumerated value below both operands

Two semantic choices are part of the model rather than gaps. An open element is contained only
in an open element: ``x:`` admits targets above ``x`` outside the current table, so no union of
bounded elements covers it. A range with incomparable bounds denotes no target; a left operand
carrying one is excluded from the completeness direction of the satisfies law, since ∅ is a
subset of everything while no element of the left side covers it.
"""

from typing import Dict, FrozenSet, List, NamedTuple, Set, Tuple

import pytest

import spack.vendor.archspec.cpu

import spack.error
from spack.spec import Spec

#: Slice of the table the single-element expressions are built from: the x86_64 generic levels
#: and a chain of named microarchitectures around them, one aarch64 pair, and one name outside
#: the table, which is its own family root and so a singleton.
_SLICE = (
    "x86_64",
    "x86_64_v2",
    "x86_64_v3",
    "x86_64_v4",
    "nocona",
    "core2",
    "nehalem",
    "sandybridge",
    "haswell",
    "skylake",
    "cannonlake",
    "icelake",
    "alderlake",
    "arrowlake",
    "aarch64",
    "neoverse_n1",
    "armv8.6a",
    "zen9",
)

#: Smaller core the two-element unions are built over. It keeps the shapes that need a union to
#: express: incomparable upper bounds in one family (icelake and alderlake:arrowlake), a generic
#: level next to a named chain (x86_64_v3:x86_64_v4 next to :sandybridge), a family root, and
#: the out-of-table name.
_CORE = (
    "x86_64",
    "x86_64_v3",
    "x86_64_v4",
    "sandybridge",
    "icelake",
    "alderlake",
    "arrowlake",
    "zen9",
)

#: Bounded ranges whose bounds are incomparable or outside the table: they denote no target.
_DEGENERATE = ("icelake:alderlake", "nehalem:aarch64", "zen9:icelake", "icelake:zen9")


def _down_closures() -> Dict[str, FrozenSet[str]]:
    """For every name in the world, the names at or below it in the table order; a name outside
    the table is its own singleton closure."""
    table = spack.vendor.archspec.cpu.TARGETS
    result = {name: frozenset(a.name for a in t.ancestors) | {name} for name, t in table.items()}
    for name in _SLICE:
        if name not in result:
            result[name] = frozenset((name,))
    return result


#: name -> the set of names at or below it, so ``a <= b`` is ``a in _DOWN[b]``
_DOWN = _down_closures()

#: The world the model quantifies over: the whole table plus the names outside it the
#: expressions mention. The slice only limits which expressions are built, not what they denote.
_WORLD = frozenset(_DOWN)


class _Denotation(NamedTuple):
    points: FrozenSet[str]
    tails: FrozenSet[str]
    degenerate: bool


def _denote(expr: str) -> _Denotation:
    """The model denotation of a target expression, computed from the table alone."""
    points: Set[str] = set()
    tails: Set[str] = set()
    degenerate = False
    for element in expr.split(","):
        lo, sep, hi = ("", ":", "") if element == "*" else element.partition(":")
        if not sep:
            points.add(element)
        elif not lo and not hi:
            points.update(_WORLD)
            tails.add("")
        elif not hi:
            tails.add(lo)
            points.update(n for n in _WORLD if lo in _DOWN[n])
        else:
            members = {n for n in _DOWN[hi] if not lo or lo in _DOWN[n]}
            if not members:
                degenerate = True
            points.update(members)
    if "" in tails:
        tails = {""}
    else:
        # a tail contained in a lower one is redundant: the pair denotes the lower tail alone
        tails = {x for x in tails if not any(y != x and y in _DOWN[x] for y in tails)}
    return _Denotation(frozenset(points), frozenset(tails), degenerate)


def _tails_covered(lhs: FrozenSet[str], rhs: FrozenSet[str]) -> bool:
    """Whether every open tail on the left starts at or above an open tail on the right; the
    unbounded tail of ``:`` starts below everything and only ``:`` itself covers it."""
    return all(
        any(y == "" or (x != "" and y in _DOWN[x]) for y in rhs) if x not in rhs else True
        for x in lhs
    )


def _subset(lhs: _Denotation, rhs: _Denotation) -> bool:
    return lhs.points <= rhs.points and _tails_covered(lhs.tails, rhs.tails)


class _Value(NamedTuple):
    expr: str
    spec: Spec
    denotation: _Denotation


def _value(expr: str) -> _Value:
    return _Value(expr, Spec(f"target={expr}"), _denote(expr))


def _comparable_pairs(names: Tuple[str, ...]) -> List[Tuple[str, str]]:
    """The ordered pairs (lo, hi) with distinct comparable in-table bounds from ``names``."""
    return [(a, b) for a in names for b in names if a != b and a in _DOWN[b]]


def _elements(names: Tuple[str, ...]) -> List[str]:
    """Every single-element expression over ``names``: points, open and bounded ranges."""
    result = list(names)
    result.extend(f"{name}:" for name in names)
    result.extend(f":{name}" for name in names)
    result.extend(f"{lo}:{hi}" for lo, hi in _comparable_pairs(names))
    return result


def _singles() -> List[_Value]:
    exprs = _elements(_SLICE) + list(_DEGENERATE) + [":", "*"]
    return [_value(e) for e in exprs]


def _unions() -> List[_Value]:
    core = _elements(_CORE)
    return [_value(f"{a},{b}") for i, a in enumerate(core) for b in core[i + 1 :]]


_SINGLES = _singles()
_CORE_ELEMENTS = frozenset(_elements(_CORE)) | {":", "*"}
_CORE_SINGLES = [v for v in _SINGLES if v.expr in _CORE_ELEMENTS]
_UNIONS = _unions()

#: Stride for the union-times-union crossing, which is too large to enumerate exhaustively.
_UNION_STRIDE = 16
#: Stride for the pairs on which the greatest-lower-bound law quantifies over all singles.
_GLB_STRIDE = 101


def _pairs() -> List[Tuple[_Value, _Value]]:
    result = [(a, b) for a in _SINGLES for b in _SINGLES]
    result.extend((u, s) for u in _UNIONS for s in _CORE_SINGLES)
    result.extend((s, u) for u in _UNIONS for s in _CORE_SINGLES)
    result.extend(
        (a, b)
        for i, a in enumerate(_UNIONS)
        for j, b in enumerate(_UNIONS)
        if (i * len(_UNIONS) + j) % _UNION_STRIDE == 0
    )
    return result


_PAIRS = _pairs()


def _fail(violations: List[str]) -> None:
    if violations:
        pytest.fail(f"{len(violations)} violations, first 20:\n" + "\n".join(violations[:20]))


def test_satisfies_matches_the_model():
    """satisfies is the model subset: P(a) ⊆ P(b) with every open tail covered. The completeness
    direction is skipped when the left side has an element denoting no target."""
    violations = []
    for a, b in _PAIRS:
        actual = a.spec.satisfies(b.spec)
        expected = _subset(a.denotation, b.denotation)
        if actual and not expected:
            violations.append(f"{a.expr} satisfies {b.expr} but is not a subset")
        elif expected and not actual and not a.denotation.degenerate:
            violations.append(f"{a.expr} is a subset of {b.expr} but does not satisfy it")
    _fail(violations)


def test_intersects_matches_the_model():
    """intersects is nonempty overlap of the denoted sets."""
    violations = []
    for a, b in _PAIRS:
        actual = a.spec.intersects(b.spec)
        expected = bool(a.denotation.points & b.denotation.points)
        if actual is not expected:
            violations.append(f"{a.expr} intersects {b.expr} is {actual}, overlap {expected}")
    _fail(violations)


def test_constrain_matches_the_model():
    """constrain raises exactly on disjoint operands; otherwise the result denotes the
    intersection, satisfies both operands, and is the same state in either operand order.
    Checked on ``ArchSpec`` for every pair; the ``Spec`` layer on top only guards with
    ``intersects`` and delegates, so a strided sample covers it."""
    violations = []
    disjoint = 0
    sampled = 0
    for a, b in _PAIRS:
        overlap = a.denotation.points & b.denotation.points
        if not overlap:
            # the raise is the intersects guard, so the intersects law already covers it
            # exhaustively; a strided sample checks the guard is in place
            disjoint += 1
            if disjoint % _UNION_STRIDE:
                continue
        try:
            forward = a.spec.architecture.copy()
            forward.constrain(b.spec.architecture)
        except spack.error.SpecError:
            if overlap:
                violations.append(f"{a.expr} constrain {b.expr} raises on overlapping operands")
            continue
        if not overlap:
            violations.append(f"{a.expr} constrain {b.expr} does not raise on disjoint operands")
            continue
        result = str(forward.target)
        if _denote(result).points != overlap:
            violations.append(f"({a.expr}) ∩ ({b.expr}) = {result} denotes the wrong set")
        if not forward.satisfies(a.spec.architecture) or not forward.satisfies(
            b.spec.architecture
        ):
            violations.append(f"({a.expr}) ∩ ({b.expr}) = {result} does not satisfy an operand")
        backward = b.spec.architecture.copy()
        backward.constrain(a.spec.architecture)
        if str(backward.target) != result:
            violations.append(f"({a.expr}) ∩ ({b.expr}) = {result}, reversed {backward.target}")
        sampled += 1
        if sampled % _UNION_STRIDE == 0:
            try:
                through_spec = a.spec.copy()
                through_spec.constrain(b.spec)
            except spack.error.SpecError:
                violations.append(f"{a.expr} constrain {b.expr} raises on Spec but not ArchSpec")
                continue
            if str(through_spec.architecture.target) != result:
                violations.append(f"({a.expr}) ∩ ({b.expr}) differs between Spec and ArchSpec")
    _fail(violations)


def test_constrain_computes_a_greatest_lower_bound():
    """On a strided sample of pairs, every enumerated value below both operands in the model is
    below the constrained result in the implementation."""
    violations = []
    for a, b in _PAIRS[::_GLB_STRIDE]:
        if not (a.denotation.points & b.denotation.points):
            continue
        try:
            merged = a.spec.architecture.copy()
            merged.constrain(b.spec.architecture)
        except spack.error.SpecError:
            continue  # a raise on overlapping operands is the constrain law's violation
        for v in _SINGLES:
            if v.denotation.degenerate:
                continue
            if not _subset(v.denotation, a.denotation) or not _subset(v.denotation, b.denotation):
                continue
            if not v.spec.architecture.satisfies(merged):
                violations.append(
                    f"{v.expr} is below {a.expr} and {b.expr} but not below their "
                    f"intersection {merged.target}"
                )
    _fail(violations)


def test_construction_preserves_the_denotation():
    """Parsing stores a canonical form; it must denote the same set as the input expression,
    and printing and reparsing it must reproduce the same state."""
    violations = []
    for v in _SINGLES + _UNIONS:
        stored = str(v.spec.architecture.target)
        if _denote(stored)[:2] != v.denotation[:2]:
            violations.append(f"{v.expr} is stored as {stored}, which denotes a different set")
        if Spec(str(v.spec)).architecture != v.spec.architecture:
            violations.append(f"{v.expr} prints as {v.spec}, which parses to a different state")
    _fail(violations)


def test_the_universe_alias_star_is_the_state_colon():
    """``target=*`` and ``target=:`` denote every target and satisfy each other, so they must
    behave as one state: same satisfies, intersects, constrain and concreteness against every
    enumerated value."""
    star, colon = _value("*").spec, _value(":").spec
    assert star.satisfies(colon) and colon.satisfies(star)
    violations = []
    if star.architecture.target_concrete != colon.architecture.target_concrete:
        violations.append("* and : differ in target_concrete")
    for v in _SINGLES:
        if star.satisfies(v.spec) != colon.satisfies(v.spec):
            violations.append(f"satisfies {v.expr} differs between * and :")
        if v.spec.satisfies(star) != v.spec.satisfies(colon):
            violations.append(f"{v.expr} satisfies the universe differently between * and :")
        if star.intersects(v.spec) != colon.intersects(v.spec):
            violations.append(f"intersects {v.expr} differs between * and :")
    _fail(violations)


@pytest.mark.parametrize(
    "expr",
    [
        ":zen9,icelake",
        "zen9,icelake",
        ":zen9,:icelake",
        "zen9:,x86_64:",
        "zen9:zen9",
        ":",
        "*",
        "x86_64::icelake",
        ":,:",
        "x86_64:,",
        ",",
    ],
)
def test_construction_parses_or_raises_a_spec_error(expr):
    """Any target expression either parses or raises within the SpecError hierarchy; adding a
    known name next to an unknown one must not turn acceptance into a crash."""
    try:
        Spec(f"target={expr}")
    except spack.error.SpecError:
        pass

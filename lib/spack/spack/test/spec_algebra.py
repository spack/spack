# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Algebraic properties of ``Spec.satisfies``, ``Spec.intersects`` and ``Spec.constrain``.

A spec denotes the set of concrete specs it can be concretized to, a concrete spec being a
singleton. That makes the three operations set operations::

    a.satisfies(b)     a ⊆ b
    a.intersects(b)    a ∩ b ≠ ∅
    a.constrain(b)     a := a ∩ b

The sets a spec can denote are closed under ∩ but not under ∪, so ordered by ⊆ they are a
meet-semilattice with ∩ as the meet. Its top is the anonymous spec, which constrains nothing. It
has no bottom: no spec denotes ∅, so ``constrain`` raises instead of producing one, and
``spack.spec.meet`` adjoins one by returning None.

The laws that follow are checked on hand-picked cases, each saying what one of them means on an
example a reader can follow.

Some laws do not hold. Each gap is pinned by its own test, named for what it demonstrates. Some
gaps are what a spec means and say so; the rest are defects that should start failing the day
they are fixed.
"""

import pytest

from spack.spec import Spec, meet
from spack.spec_parser import _parse_toolchain_config


@pytest.mark.parametrize(
    "spec_str",
    [
        "pkg-a",
        "builtin_mock.pkg-a",
        "pkg-a@1:3",
        "pkg-a+foo",
        "pkg-a foo=bar,baz",
        "pkg-a cflags=-O2",
        "pkg-a target=x86_64:",
        "pkg-a/abcdef",
        "pkg-a patches=abcdef",
        "pkg-a ^pkg-b@1 ^pkg-c",
        "pkg-a %pkg-b",
        "mpi",
        "pkg-a ^[virtuals=mpi] mpich",
        "pkg-a platform=* os=* target=*",
    ],
)
def test_satisfies_is_reflexive(spec_str, mock_packages):
    """Every spec is inside itself."""
    spec = Spec(spec_str)
    assert spec.satisfies(spec)


@pytest.mark.parametrize(
    "spec_str",
    [
        "pkg-a",
        "builtin_mock.pkg-a",
        "pkg-a@1:3",
        "pkg-a+foo",
        "pkg-a foo=bar,baz",
        "pkg-a cflags=-O2",
        "pkg-a target=x86_64:",
        "pkg-a/abcdef",
        "pkg-a patches=abcdef",
        "pkg-a ^pkg-b@1 ^pkg-c",
        "pkg-a %pkg-b",
        "mpi",
        "pkg-a ^[virtuals=mpi] mpich",
        "pkg-a platform=* os=* target=*",
    ],
)
def test_intersects_is_reflexive(spec_str, mock_packages):
    """Every spec overlaps itself."""
    spec = Spec(spec_str)
    assert spec.intersects(spec)


@pytest.mark.parametrize(
    "lhs_str,rhs_str",
    [
        # Disjoint and overlapping names
        ("pkg-a", "pkg-b"),
        ("pkg-a", "builtin_mock.pkg-a"),
        # Versions
        ("pkg-a@1:3", "pkg-a@2"),
        ("pkg-a@1:3", "pkg-a@5"),
        # Variants
        ("pkg-a+foo", "pkg-a~foo"),
        ("pkg-a foo=bar", "pkg-a foo=baz"),
        # Compiler flags
        ("pkg-a cflags=-O2", "pkg-a cflags=-g"),
        # Architecture, including two ranges of the same family
        ("pkg-a target=haswell", "pkg-a target=x86_64:"),
        ("pkg-a target=x86_64:", "pkg-a target=:icelake"),
        ("pkg-a target=x86_64:", "pkg-a target=ppc64le:"),
        # Abstract hashes
        ("pkg-a/abcdef", "pkg-a/abc"),
        ("pkg-a/abcdef", "pkg-a/ffffff"),
        # Dependencies and virtuals
        ("pkg-a ^pkg-b@1", "pkg-a ^pkg-b@2"),
        ("mpi", "pkg-a ^[virtuals=mpi] mpich"),
        ("pkg-a", "mpi"),
    ],
)
def test_intersects_is_symmetric(lhs_str, rhs_str, mock_packages):
    """Whether two specs overlap does not depend on the order they're compared in."""
    lhs, rhs = Spec(lhs_str), Spec(rhs_str)
    assert lhs.intersects(rhs) == rhs.intersects(lhs)


@pytest.mark.parametrize(
    "a_str,b_str,c_str",
    [
        ("pkg-a@2", "pkg-a@1:3", "pkg-a@:5"),
        ("pkg-a foo=bar,baz", "pkg-a foo=bar", "pkg-a"),
        ("pkg-a cflags=-O2", "pkg-a cflags=-O2", "pkg-a"),
        ("pkg-a target=haswell", "pkg-a target=x86_64:", "pkg-a"),
        ("pkg-a/abcdef1234", "pkg-a/abcdef", "pkg-a"),
        ("pkg-a ^pkg-b@1", "pkg-a ^pkg-b@1:3", "pkg-a"),
        ("pkg-a %pkg-b", "pkg-a %pkg-b", "pkg-a"),
    ],
)
def test_satisfies_is_transitive(a_str, b_str, c_str, mock_packages):
    """A spec inside a spec that is itself inside a third is inside the third."""
    a, b, c = Spec(a_str), Spec(b_str), Spec(c_str)
    assert a.satisfies(b)
    assert b.satisfies(c)
    assert a.satisfies(c)


@pytest.mark.parametrize(
    "lhs_str,rhs_str",
    [
        ("pkg-a@1:3", "pkg-a@2"),
        ("pkg-a foo=bar,baz", "pkg-a foo=baz"),
        ("pkg-a cflags=-O2", "pkg-a"),
        ("pkg-a target=haswell", "pkg-a target=x86_64:"),
        ("pkg-a/abcdef", "pkg-a/abc"),
        ("pkg-a", "pkg-a ^pkg-b@1"),
        ("pkg-a ^pkg-b@1 ^pkg-c", "pkg-a"),
        ("pkg-a platform=test", "pkg-a os=*"),
    ],
)
def test_constrain_is_commutative(lhs_str, rhs_str, mock_packages):
    """The intersection does not depend on the order of lhs and rhs."""
    lhs, rhs = Spec(lhs_str), Spec(rhs_str)
    forward = meet(lhs, rhs)
    backward = meet(rhs, lhs)
    assert (forward is None) == (backward is None)
    if forward is not None:
        assert forward.to_dict() == backward.to_dict()


@pytest.mark.parametrize(
    "a_str,b_str,c_str",
    [
        ("pkg-a@1:3", "pkg-a@:2", "pkg-a@2"),
        ("pkg-a foo=bar,baz", "pkg-a foo=baz", "pkg-a"),
        ("pkg-a cflags=-O2", "pkg-a", "pkg-a"),
        ("pkg-a target=haswell", "pkg-a target=x86_64:", "pkg-a"),
        ("pkg-a", "pkg-a ^pkg-b@1", "pkg-a"),
    ],
)
def test_constrain_is_associative(a_str, b_str, c_str, mock_packages):
    """Intersecting three specs gives the same result whichever two are intersected first."""
    a, b, c = Spec(a_str), Spec(b_str), Spec(c_str)
    ab, bc = meet(a, b), meet(b, c)
    left = meet(ab, c) if ab is not None else None
    right = meet(a, bc) if bc is not None else None
    assert (left is None) == (right is None)
    if left is not None:
        assert left.to_dict() == right.to_dict()


@pytest.mark.parametrize(
    "lhs_str,rhs_str",
    [
        ("pkg-a@2", "pkg-a@1:3"),
        ("pkg-a foo=bar,baz", "pkg-a foo=bar"),
        ("pkg-a target=haswell", "pkg-a target=x86_64:"),
        ("pkg-a target=:icelake", "pkg-a target=x86_64:"),
        ("pkg-a/abcdef", "pkg-a/abc"),
        ("pkg-a ^pkg-b@1", "pkg-a"),
    ],
)
def test_constrain_absorbs_a_satisfied_constraint(lhs_str, rhs_str, mock_packages):
    """A spec already inside another has nothing left to intersect, so the meet is the spec."""
    lhs, rhs = Spec(lhs_str), Spec(rhs_str)
    assert lhs.satisfies(rhs)
    result = meet(lhs, rhs)
    assert result is not None
    assert result.to_dict() == lhs.to_dict()


@pytest.mark.parametrize(
    "a_str,b_str,c_str",
    [
        ("pkg-a@1:3", "pkg-a@2:5", "pkg-a@2:3"),
        ("pkg-a foo=bar,baz", "pkg-a foo=baz,fee", "pkg-a foo=bar,baz,fee"),
        ("pkg-a target=x86_64:", "pkg-a target=:icelake", "pkg-a target=haswell"),
        ("pkg-a target=cascadelake:", "pkg-a target=cannonlake:", "pkg-a target=icelake"),
        ("pkg-a", "pkg-a ^pkg-b@1", "pkg-a ^pkg-b@1"),
    ],
)
def test_constrain_is_the_greatest_lower_bound(a_str, b_str, c_str, mock_packages):
    """Anything inside both a and b is inside their meet too. That makes the meet the
    intersection, not merely some spec contained in both."""
    a, b, c = Spec(a_str), Spec(b_str), Spec(c_str)
    assert c.satisfies(a)
    assert c.satisfies(b)
    result = meet(a, b)
    assert result is not None
    assert c.satisfies(result)


@pytest.mark.parametrize(
    "a_str,b_str,c_str",
    [
        ("pkg-a@2", "pkg-a@1:3", "pkg-a"),
        ("pkg-a foo=bar,baz", "pkg-a foo=bar", "pkg-a"),
        ("pkg-a target=haswell", "pkg-a target=x86_64:", "pkg-a os=debian6"),
    ],
)
def test_constrain_is_monotonic(a_str, b_str, c_str, mock_packages):
    """Narrowing either spec narrows the meet, so a smaller spec cannot produce a larger
    result."""
    a, b, c = Spec(a_str), Spec(b_str), Spec(c_str)
    assert a.satisfies(b)
    meet_ac, meet_bc = meet(a, c), meet(b, c)
    if meet_ac is None:
        return
    assert meet_bc is not None
    assert meet_ac.satisfies(meet_bc)


# Where the laws above do not hold. Some cases are what a spec means and say so; the rest are
# defects that should start failing the day they are fixed.


def test_a_propagated_variant_follows_non_contradiction(mock_packages):
    """A propagating variant constrains every transitive dependency that has it, which satisfies
    cannot check structurally. It falls back to non-contradiction: a spec with no opinion on the
    variant satisfies the propagation, which breaks transitivity."""
    assert Spec("pkg-a~foo").satisfies("pkg-a")
    assert Spec("pkg-a").satisfies("pkg-a++foo")
    assert not Spec("pkg-a~foo").satisfies("pkg-a++foo")


def test_a_propagated_flag_is_invisible_to_satisfies(mock_packages):
    """A propagating flag is a condition on the whole DAG, which concretization discharges into
    plain flags on every node it reaches, so satisfies is blind to the marker: the plain flag
    satisfies the propagating request too."""
    assert Spec("pkg-a cflags=-O2").satisfies("pkg-a cflags==-O2")


def test_flag_order_is_significant_so_the_meet_is_not_commutative(mock_packages):
    """Flag order is significant to the build, so flags are a sequence, not a set. cflags='-O2 -g'
    and cflags='-g -O2' are two states, and the union that merges them does not commute."""
    lhs, rhs = Spec("pkg-a cflags=-O2"), Spec("pkg-a cflags=-g")
    forward = meet(lhs, rhs)
    backward = meet(rhs, lhs)
    assert forward.to_dict() != backward.to_dict()


# Laws that hold only because of one decision in the merge, pinned on the state that stops
# satisfying them the day it is lost.


def test_implication_does_not_fuse_across_a_nested_dependency(mock_packages):
    """A bare edge to pkg-b does not imply one that itself depends on pkg-e: they are independent
    requirements, and fusing them demands both of a single edge. Kept apart, they leave every merge
    order at the same state."""
    a = Spec("^pkg-b %pkg-e")
    b = Spec("^[deptypes=build] pkg-b ^[deptypes=link] pkg-b")
    c = Spec("%pkg-b ^pkg-b")

    ab, bc = meet(a, b), meet(b, c)
    left, right = meet(ab, c), meet(a, bc)

    assert left is not None and right is not None
    assert left.to_dict() == right.to_dict()
    assert left.satisfies(a)
    assert left.satisfies(b)
    assert left.satisfies(c)


def test_toolchain_config_entries_commute(mock_packages):
    """A toolchain config is folded into one spec entry by entry, so the result must not depend
    on the order the YAML lists them in."""
    a = {"spec": "%pkg-c@1", "when": "%pkg-e@2"}
    b = {"spec": "%pkg-e@1"}
    forward, backward = _parse_toolchain_config([a, b]), _parse_toolchain_config([b, a])
    assert forward.to_dict() == backward.to_dict()

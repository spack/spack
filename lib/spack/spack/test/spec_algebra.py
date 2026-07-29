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
has no bottom: no spec denotes ∅, so ``constrain`` raises rather than producing one, and ``meet``
below adjoins one by returning None.

The laws that follow are checked twice: over hand-picked cases that say what each of them means
on an example a reader can follow, and over the product of a corpus of abstract specs covering
every dimension, which is where a dimension implementing only half of a law shows up.

Some laws do not hold. Each gap is pinned by its own test, named for what it demonstrates, and
the corpus-wide checks say which of them they step around. Some gaps are what a spec means and
say so; the rest are defects that are not fixed yet, and should start failing the day they are.
"""

import itertools
from typing import Optional

import pytest

import spack.version
from spack.error import SpecError
from spack.spec import Spec


def meet(a: Spec, b: Spec) -> Optional[Spec]:
    """The meet of a and b as a new spec, or None when the two are disjoint, since no spec
    denotes the empty set."""
    result = a.copy()
    try:
        result.constrain(b)
    except SpecError:
        return None
    return result


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
    """The intersection does not depend on the order of the operands."""
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
        ("pkg-a", "pkg-a ^pkg-b@1", "pkg-a ^pkg-b@1"),
    ],
)
def test_constrain_is_the_greatest_lower_bound(a_str, b_str, c_str, mock_packages):
    """Anything inside both operands is inside their meet too. This is what makes the meet the
    intersection, rather than merely some spec contained in both."""
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
    """Narrowing an operand narrows the meet, so a smaller spec cannot produce a larger result."""
    a, b, c = Spec(a_str), Spec(b_str), Spec(c_str)
    assert a.satisfies(b)
    meet_ac, meet_bc = meet(a, c), meet(b, c)
    if meet_ac is None:
        return
    assert meet_bc is not None
    assert meet_ac.satisfies(meet_bc)


def test_two_packages_cannot_provide_one_virtual(mock_packages):
    """A package gets a virtual from exactly one of its dependencies, so two specs that name a
    different provider of the same virtual denote disjoint sets."""
    assert not Spec("pkg-a ^[virtuals=mpi] mpich").intersects("pkg-a ^[virtuals=mpi] zmpi")
    assert not Spec("pkg-a ^[virtuals=mpi] zmpi").intersects("pkg-a ^[virtuals=mpi] mpich")


def test_two_providers_under_conditions_that_exclude_each_other_are_fine(mock_packages):
    """Only one provider can be the one at a time, so two of them named under conditions that
    cannot hold together are not in each other's way."""
    lhs = Spec("pkg-a ^[when='+foo' virtuals=mpi] mpich")
    rhs = Spec("pkg-a ^[when='~foo' virtuals=mpi] zmpi")
    assert lhs.intersects(rhs)
    assert rhs.intersects(lhs)


# Where the laws above do not hold. Each case is a minimal, self-contained reproduction named for
# what it demonstrates. Some of them are what a spec means rather than a defect, and say so; the
# rest are defects that are not fixed yet, and should start failing the day they are.


def test_a_propagated_variant_follows_non_contradiction(mock_packages):
    """A propagating variant constrains every transitive dependency that has the variant, which
    is a DAG-wide, package-dependent condition satisfies cannot check structurally. It falls
    back to non-contradiction instead: a spec with no opinion on the variant satisfies the
    propagation, even though it is not really inside the set that denotes, which breaks
    transitivity."""
    assert Spec("pkg-a~foo").satisfies("pkg-a")
    assert Spec("pkg-a").satisfies("pkg-a++foo")
    assert not Spec("pkg-a~foo").satisfies("pkg-a++foo")


def test_flag_order_is_significant_so_the_meet_is_not_commutative(mock_packages):
    """Compiler flags merge as an order-preserving union, so cflags='-O2 -g' and cflags='-g -O2'
    are different states: flag order is significant to the build, so flags are a sequence
    rather than a set, and the meet is not commutative."""
    lhs, rhs = Spec("pkg-a cflags=-O2"), Spec("pkg-a cflags=-g")
    forward = meet(lhs, rhs)
    backward = meet(rhs, lhs)
    assert forward.to_dict() != backward.to_dict()


def test_inactive_when_edge_is_left_out_of_the_merge(mock_packages):
    """An edge whose when condition cannot hold for the lhs states nothing about it, so both
    satisfies and the merge pass over it."""
    lhs = Spec("pkg-a ~foo")
    rhs = Spec("pkg-a ^[when='+foo'] pkg-b@1")
    assert lhs.satisfies(rhs)
    result = meet(lhs, rhs)
    assert result is not None
    assert result.to_dict() == lhs.to_dict()


def test_a_virtual_edge_and_a_provider_edge_are_merged(mock_packages):
    """An edge naming a virtual and an edge naming the package providing it are matched by
    satisfies and merged into one edge, whichever of the two the merge starts from. Which edge
    absorbs which is never in question, since a package gets a virtual from exactly one of its
    dependencies."""
    lhs = Spec("pkg-a ^[virtuals=mpi] mpich")
    rhs = Spec("pkg-a ^mpi")
    assert lhs.satisfies(rhs)

    result = meet(lhs, rhs)
    assert result is not None
    assert result.to_dict() == lhs.to_dict()

    # The other way around, the node named after the virtual becomes the one providing it.
    backward = meet(Spec("pkg-a ^mpi+debug"), Spec("pkg-a ^[virtuals=mpi] mpich"))
    assert backward is not None
    assert len(backward.edges_to_dependencies()) == 1
    assert backward.satisfies("pkg-a ^[virtuals=mpi] mpich+debug")


def test_a_virtual_edge_constraining_a_version_breaks_monotonicity_of_constrain(mock_packages):
    """A version on an edge naming a virtual bounds the version of the virtual rather than of the
    package providing it, and a node has nowhere to record that, so it is the one thing the merge
    cannot absorb into the provider edge. The edge stays beside the provider carrying none of
    what the provider was narrowed with, which lets narrowing an operand widen the meet."""
    narrower = Spec("pkg-a ^[virtuals=mpi] mpich+debug")
    wider = Spec("pkg-a ^mpi+debug")
    assert narrower.satisfies(wider)

    third = Spec("pkg-a ^mpi@3")
    narrowed, widened = meet(narrower, third), meet(wider, third)
    assert widened is not None
    assert narrowed is not None
    assert len(narrowed.edges_to_dependencies()) == 2  # '^mpi@3' and '^[virtuals=mpi] mpich+debug'
    assert not narrowed.satisfies(widened)


def test_target_range_representation_breaks_commutativity_of_constrain(mock_packages):
    """_target_intersection resolves an unbounded end of a range to the other operand's bound
    when there is one, e.g. ':icelake' constrained by 'x86_64:' becomes 'x86_64:icelake' rather
    than staying ':icelake', even though x86_64 is the family root and the two strings denote
    the same range. Constraining in the other order leaves the bound unresolved, so the meet of
    two range targets depends on the order of the operands."""
    lhs, rhs = Spec("pkg-a target=:icelake"), Spec("pkg-a target=x86_64:")
    forward = meet(lhs, rhs)
    backward = meet(rhs, lhs)
    assert forward.architecture.target != backward.architecture.target


#: Abstract specs covering every dimension ``constrain`` merges, used to fuzz the mutation-safety
#: invariants below over many more combinations than the laws above spell out by hand.
CORPUS = [
    "",
    "pkg-a",
    "pkg-b",
    "builtin_mock.pkg-a",
    "pkg-a@1:3",
    "pkg-a@2",
    "pkg-a@1,3:4",
    "pkg-a@=2",
    "pkg-a@develop",
    "@:1",
    "pkg-a+foo",
    "pkg-a~foo",
    "pkg-a++foo",
    "pkg-a foo=bar",
    "pkg-a foo=baz",
    "pkg-a foo=bar,baz",
    "pkg-a foo:=bar",
    "pkg-a cflags=-O2",
    "pkg-a cflags=-g",
    "pkg-a cflags==-O2",
    "pkg-a cflags=-g cflags==-O2",
    "pkg-a ldflags=-L/x",
    "pkg-a target=haswell",
    "pkg-a target=zen2",
    "pkg-a target=x86_64:",
    "pkg-a target=:icelake",
    "pkg-a target=x86_64:icelake",
    "pkg-a target=haswell,zen2",
    "pkg-a os=debian6",
    "pkg-a arch=test-debian6-haswell",
    "pkg-a/abcdef",
    "pkg-a/abc",
    "^pkg-b",
    "^pkg-b@1",
    "^pkg-b@2",
    "pkg-a ^pkg-b@1 ^pkg-c",
    "%pkg-b",
    "%%pkg-b",
    "%[deptypes=build] pkg-b",
    "%[deptypes=link] pkg-b",
    "pkg-a ^[when='+foo'] pkg-b@1",
    "pkg-a ^[when='+bar'] pkg-b@2",
    "pkg-a platform=test",
    "pkg-a platform=*",
    "pkg-a os=*",
    "pkg-a target=*",
    "pkg-a patches=abcdef",
    "pkg-a patches:=abcdef1234567890",
    "pkg-a ^[virtuals=mpi] mpich",
    "pkg-a ^[virtuals=mpi] mpich@3",
    "pkg-a ^[virtuals=mpi] mpich+debug",
    "pkg-a ^[virtuals=mpi] mpich target=haswell",
    "pkg-a ^[virtuals=mpi,lapack] openblas-with-lapack",
    "mpi",
    "pkg-a ^mpi",
    "pkg-a ^mpi@3",
    "pkg-a ^mpi+debug",
    "pkg-a ^mpi target=haswell",
    "pkg-a ^pkg-b",
    "pkg-a %pkg-b",
    "pkg-a %%pkg-b",
    "pkg-a ^[deptypes=build] pkg-b",
    "pkg-a ^[deptypes=link] pkg-b",
    "pkg-a ^pkg-b ^pkg-c ^pkg-d",
    "pkg-a %pkg-b@1 ^pkg-c",
    "pkg-a platform=* os=* target=*",
]


def _pairs():
    for lhs_str, rhs_str in itertools.product(CORPUS, repeat=2):
        yield lhs_str, rhs_str, Spec(lhs_str), Spec(rhs_str)


def _try_constrain(lhs, rhs):
    """Return ``(changed, error)``, exactly one of which is None."""
    try:
        return lhs.constrain(rhs), None
    except SpecError as e:
        return None, e


def _narrowing_dimensions(spec: Spec):
    """The state of the dimensions in which leaving a value unset is an absent constraint rather
    than a constraint satisfied by default, as a comparable snapshot."""
    return (
        str(spec.versions),
        {name: str(value) for name, value in spec.variants.items()},
        str(spec.architecture),
        {name: [str(flag) for flag in flags] for name, flags in spec.compiler_flags.items()},
        spec.abstract_hash,
    )


class TestConstrainMutationSafety:
    """``Spec.constrain`` intersects the left-hand side with the right-hand side in place. It
    must apply the whole intersection or nothing at all, and it must never write to the
    right-hand side, now or through an object the two ends up sharing.

    Specs are snapshotted with ``to_dict()``, which round-trips abstract specs and so compares
    their state directly. ``Spec.__eq__`` is semantic equality instead: it leaves the propagation
    policy of an edge out of the comparison, so ``pkg-a %pkg-b`` and ``pkg-a %%pkg-b`` are equal,
    as they are also mutually satisfying.
    """

    def test_lhs_is_unchanged_when_constrain_raises(self, mock_packages):
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            before = lhs.to_dict()
            _, error = _try_constrain(lhs, rhs)
            if error is not None:
                assert lhs.to_dict() == before, f"'{lhs_str}' mutated by a failed '{rhs_str}'"

    def test_rhs_is_never_mutated(self, mock_packages):
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            before = rhs.to_dict()
            _try_constrain(lhs, rhs)
            assert rhs.to_dict() == before, f"'{lhs_str}'.constrain('{rhs_str}') mutated the rhs"

    def test_rhs_is_not_corrupted_by_later_constraints(self, mock_packages):
        """A successful constrain must not leave the two specs sharing a mutable object, which
        a later constrain on the lhs would then write through into the rhs."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            if _try_constrain(lhs, rhs)[1] is not None:
                continue
            before = rhs.to_dict()
            for extra_str in CORPUS:
                _try_constrain(lhs, Spec(extra_str))
                assert rhs.to_dict() == before, (
                    f"'{lhs_str}'.constrain('{rhs_str}') shares state with the rhs: "
                    f"constraining with '{extra_str}' afterwards changed it"
                )

    def test_returned_changed_flag_is_honest(self, mock_packages):
        """Callers use the return value to decide whether to redo work, so it has to report
        exactly whether the lhs changed."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            before = lhs.to_dict()
            changed, error = _try_constrain(lhs, rhs)
            if error is None:
                assert changed is (lhs.to_dict() != before), (
                    f"'{lhs_str}'.constrain('{rhs_str}') returned {changed}"
                )

    def test_intersects_agrees_with_constrain(self, mock_packages):
        """``intersects`` is the question ``constrain`` answers by raising or not."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            intersects = lhs.intersects(rhs)
            _, error = _try_constrain(lhs, rhs)
            assert intersects is (error is None), (
                f"'{lhs_str}'.intersects('{rhs_str}') is {intersects}, but constrain "
                f"{'raised ' + type(error).__name__ if error else 'succeeded'}"
            )

    def test_constrain_is_idempotent(self, mock_packages):
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            if _try_constrain(lhs, rhs)[1] is None:
                before = lhs.to_dict()
                assert lhs.constrain(rhs) is False, f"'{lhs_str}'.constrain('{rhs_str}') twice"
                assert lhs.to_dict() == before

    def test_constrained_lhs_satisfies_rhs(self, mock_packages):
        """Guards against making constrain atomic by making it do nothing."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            if _try_constrain(lhs, rhs)[1] is None:
                assert lhs.satisfies(rhs), f"'{lhs_str}'.constrain('{rhs_str}') gave '{lhs}'"

    def test_constrain_never_weakens_the_lhs(self, mock_packages):
        """The result is the intersection of both operands, so together with the property above
        this pins that constrain narrows and never drops a constraint."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            if _try_constrain(lhs, rhs)[1] is None:
                assert lhs.satisfies(Spec(lhs_str)), (
                    f"'{lhs_str}'.constrain('{rhs_str}') gave '{lhs}'"
                )

    def test_satisfies_implies_intersects(self, mock_packages):
        """Satisfaction is subset and intersection is non-empty overlap, so a spec that is inside
        another one also overlaps it. Each dimension implements the two separately, which is why
        they can diverge, as they did for patch prefixes and architecture wildcards."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            if lhs.satisfies(rhs):
                assert lhs.intersects(rhs), (
                    f"'{lhs_str}' satisfies '{rhs_str}' but does not intersect it"
                )

    def test_satisfies_implies_constrain_succeeds(self, mock_packages):
        """Constrain is only undefined where the two are disjoint, so it cannot reject a
        constraint the lhs already satisfies."""
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            if lhs.satisfies(rhs):
                _, error = _try_constrain(lhs, rhs)
                assert error is None, (
                    f"'{lhs_str}' satisfies '{rhs_str}' but constrain raised "
                    f"{type(error).__name__}"
                )

    def test_satisfies_implies_the_narrowing_dimensions_are_unchanged(self, mock_packages):
        """An lhs that is already inside the rhs has nothing left to intersect, which is
        absorption over the product of the corpus.

        The dimensions asserted are the ones in which an unset value on the lhs really is an
        absent constraint. Names, namespaces and edges whose when condition does not apply are
        read as satisfied when the lhs leaves them unset, so constrain legitimately fills those
        in without narrowing the set the lhs denotes. Propagated variants follow a
        non-contradiction rule rather than subset semantics: a spec without such a variant
        satisfies one that propagates it, and still acquires it when constrained; see
        test_a_propagated_variant_follows_non_contradiction. Compiler
        flags are compared by value, since merging a propagating flag with a plain one of the
        same value demotes it; see
        test_flag_propagation_is_invisible_to_satisfies_but_demoted_by_constrain.
        """
        for lhs_str, rhs_str, lhs, rhs in _pairs():
            propagating = any(value.propagate for value in rhs.variants.values())
            if lhs.satisfies(rhs) and not propagating:
                before = _narrowing_dimensions(lhs)
                _try_constrain(lhs, rhs)
                assert _narrowing_dimensions(lhs) == before, (
                    f"'{lhs_str}' satisfies '{rhs_str}' but constrain changed it to '{lhs}'"
                )

    def test_constrain_with_itself_is_a_no_op(self, mock_packages):
        """The same object on both sides, which is the case in which a merge that reads its own
        output as it writes it has nothing to stop it."""
        for spec_str in CORPUS:
            spec = Spec(spec_str)
            before = spec.to_dict()
            assert spec.constrain(spec) is False, f"'{spec_str}' constrained with itself"
            assert spec.to_dict() == before, f"'{spec_str}' constrained with itself"


def _ordered_corpus():
    """The corpus entries the laws below are checked over, which is all of them but the specs
    propagating a variant: those follow non-contradiction rather than subset semantics, and a law
    provably fails on them for the reason pinned above in
    test_a_propagated_variant_follows_non_contradiction.
    """
    result = []
    for spec_str in CORPUS:
        spec = Spec(spec_str)
        if not any(value.propagate for value in spec.variants.values()):
            result.append(spec_str)
    return result


def _denote_the_same_set(lhs: Optional[Spec], rhs: Optional[Spec]) -> bool:
    """Whether two meets denote the same set of concrete specs, or are both undefined. The two
    are not compared by state: a spelling of a target range and an ordering of compiler flags
    survive the merge, so the same set comes out in more than one shape depending on the order of
    the operands; see test_target_range_representation_breaks_commutativity_of_constrain and
    test_flag_order_is_significant_so_the_meet_is_not_commutative."""
    if lhs is None or rhs is None:
        return lhs is rhs
    return lhs.satisfies(rhs) and rhs.satisfies(lhs)


def _has_unpaired_virtual_edge(spec: Spec) -> bool:
    """Whether a spec has an edge naming a virtual and constraining its version next to an edge
    naming a package providing that virtual. Those two the merge leaves side by side, since the
    version of a virtual has no home on the node providing it; see
    test_virtual_edge_breaks_monotonicity_of_constrain."""
    edges = spec.edges_to_dependencies()
    provided = {virtual for edge in edges for virtual in edge.virtuals}
    return any(
        edge.spec.name in provided and edge.spec.versions != spack.version.any_version
        for edge in edges
    )


class TestLatticeLaws:
    """The laws checked over hand-picked cases at the top of this file, checked over the corpus
    instead. The hand-picked cases say what each law means on an example a reader can follow; the
    ones here cover the combinations nobody thought to write down, which is where a dimension
    that implements only half of a law shows up.
    """

    def test_satisfies_is_transitive(self, mock_packages):
        corpus = _ordered_corpus()
        satisfies = {
            (a, b): Spec(a).satisfies(Spec(b)) for a, b in itertools.product(corpus, repeat=2)
        }
        for a, b, c in itertools.product(corpus, repeat=3):
            if satisfies[(a, b)] and satisfies[(b, c)]:
                assert satisfies[(a, c)], f"'{a}' is inside '{b}' is inside '{c}'"

    def test_constrain_is_the_greatest_lower_bound(self, mock_packages):
        """Anything inside both operands is inside their meet too, which is what makes the meet
        the intersection rather than merely some spec contained in both."""
        corpus = _ordered_corpus()
        satisfies = {
            (a, b): Spec(a).satisfies(Spec(b)) for a, b in itertools.product(corpus, repeat=2)
        }
        for a, b in itertools.combinations(corpus, 2):
            result = meet(Spec(a), Spec(b))
            for c in corpus:
                if not (satisfies[(c, a)] and satisfies[(c, b)]):
                    continue
                assert result is not None, (
                    f"'{c}' is inside both '{a}' and '{b}', which are disjoint"
                )
                assert Spec(c).satisfies(result), (
                    f"'{c}' is inside both '{a}' and '{b}', but not inside their meet '{result}'"
                )

    def test_constrain_is_commutative(self, mock_packages):
        corpus = _ordered_corpus()
        for a, b in itertools.combinations(corpus, 2):
            forward, backward = meet(Spec(a), Spec(b)), meet(Spec(b), Spec(a))
            assert _denote_the_same_set(forward, backward), (
                f"'{a}' meet '{b}' is '{forward}', the other way around it is '{backward}'"
            )

    def test_constrain_is_associative(self, mock_packages):
        corpus = _ordered_corpus()
        for a, b, c in itertools.combinations(corpus, 3):
            ab, bc = meet(Spec(a), Spec(b)), meet(Spec(b), Spec(c))
            left = meet(ab, Spec(c)) if ab is not None else None
            right = meet(Spec(a), bc) if bc is not None else None
            assert _denote_the_same_set(left, right), (
                f"('{a}' meet '{b}') meet '{c}' is '{left}', "
                f"'{a}' meet ('{b}' meet '{c}') is '{right}'"
            )

    def test_constrain_is_monotonic(self, mock_packages):
        """Narrowing an operand narrows the meet, so a smaller spec cannot produce a larger
        result."""
        corpus = _ordered_corpus()
        for a_str, b_str in itertools.product(corpus, repeat=2):
            a, b = Spec(a_str), Spec(b_str)
            if not a.satisfies(b):
                continue
            for c_str in corpus:
                c = Spec(c_str)
                narrowed, widened = meet(a, c), meet(b, c)
                if narrowed is None:
                    continue
                assert widened is not None, (
                    f"'{a_str}' is inside '{b_str}' and meets '{c_str}', but '{b_str}' does not"
                )
                if _has_unpaired_virtual_edge(narrowed):
                    continue  # see test_virtual_edge_breaks_monotonicity_of_constrain
                assert narrowed.satisfies(widened), (
                    f"'{a_str}' is inside '{b_str}', but their meets with '{c_str}', "
                    f"'{narrowed}' and '{widened}', are the other way around"
                )

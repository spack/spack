# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The algebraic laws of ``satisfies``, ``intersects`` and ``constrain``, over a corpus.

``spec_algebra.py`` checks each law on a hand-picked case that says what it means on an example a
reader can follow. This checks the same laws over the product of a corpus of abstract specs
covering every dimension ``constrain`` merges, which is where a dimension implementing only half
of a law shows up, and where a merge that reads its own output as it writes it is caught.

That product is why this is a script and not a unit test: the checks are quadratic and cubic
in the corpus, and take a minute and a half where the whole of ``spec_algebra.py`` takes under a
second. Run it against a change to the algebra, not on every push::

    bin/spack python lib/spack/spack/test/spec_algebra_corpus.py
    bin/spack python lib/spack/spack/test/spec_algebra_corpus.py --check meet_is_commutative
    bin/spack python lib/spack/spack/test/spec_algebra_corpus.py --list

Nothing here is named ``test_*`` or ``Test*``, since ``pytest.ini`` collects every file in this
directory and these are not meant to be collected.
"""

import argparse
import itertools
import sys
from typing import Callable, List, Optional, Sequence, Tuple

import spack.paths
import spack.repo
from spack.error import SpecError
from spack.spec import Spec, meet

#: Abstract specs covering every dimension ``constrain`` merges. Every check below runs over the
#: product of this list with itself, which makes the checks slow and makes them reach combinations
#: nobody thought to write down.
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
    "pkg-a target=x86_64:zen2",
    "pkg-a target=cascadelake:",
    "pkg-a target=cannonlake:",
    "pkg-a target=icelake",
    "pkg-a target=x86_64_v2",
    "pkg-a target=:aarch64",
    "pkg-a os=debian6",
    "pkg-a arch=test-debian6-haswell",
    "pkg-a/abcdef",
    "pkg-a/abc",
    "^pkg-b",
    "^pkg-b@1",
    "^pkg-b@2",
    "pkg-a ^pkg-b@1 ^pkg-c",
    "pkg-a ^*@2",
    "%pkg-b",
    "%%pkg-b",
    "%[deptypes=build] pkg-b",
    "%[deptypes=link] pkg-b",
    "pkg-a ^[when='+foo'] pkg-b@1",
    "pkg-a ^[when='+bar'] pkg-b@2",
    "pkg-a %[when='+foo'] pkg-e@1",
    "pkg-a %[when='+foo'] pkg-e@2",
    "pkg-a+foo %[when='+foo'] pkg-e@1",
    "pkg-a platform=test",
    "pkg-a platform=*",
    "pkg-a os=*",
    "pkg-a target=*",
    "pkg-a patches=abcdef",
    "pkg-a patches:=abcdef1234567890",
    "pkg-a ^[virtuals=mpi] mpich",
    "pkg-a ^[virtuals=mpi] zmpi",
    "pkg-a ^[virtuals=mpi] mpich@3",
    "pkg-a ^[virtuals=mpi] mpich+debug",
    "pkg-a ^[virtuals=mpi] mpich target=haswell",
    "pkg-a ^[virtuals=mpi,lapack] openblas-with-lapack",
    "mpi",
    "mpich",
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


def _ordered_corpus():
    """The corpus entries the laws below are checked over, which is all of them but the specs
    propagating a variant: those follow non-contradiction instead of subset semantics, and a law
    provably fails on them for the reason pinned in spec_algebra.py's
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
    are not compared by state: an ordering of compiler flags survives the merge, so one set has
    more than one state, depending on the order of the operands; see
    spec_algebra.py's test_flag_order_is_significant_so_the_meet_is_not_commutative."""
    if lhs is None or rhs is None:
        return lhs is rhs
    return lhs.satisfies(rhs) and rhs.satisfies(lhs)


# ``Spec.constrain`` intersects the left-hand side with the right-hand side in place. It must
# apply the whole intersection or nothing at all, and it must never write to the right-hand side,
# now or through an object the two end up sharing.
#
# Specs are snapshotted with ``to_dict()``, which round-trips abstract specs and so compares their
# state directly. ``Spec.__eq__`` is semantic equality instead: it leaves the propagation policy of
# an edge out of the comparison, so ``pkg-a %pkg-b`` and ``pkg-a %%pkg-b`` are equal, as they are
# also mutually satisfying.


def check_lhs_is_unchanged_when_constrain_raises():
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        before = lhs.to_dict()
        _, error = _try_constrain(lhs, rhs)
        if error is not None:
            assert lhs.to_dict() == before, f"'{lhs_str}' mutated by a failed '{rhs_str}'"


def check_rhs_is_never_mutated():
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        before = rhs.to_dict()
        _try_constrain(lhs, rhs)
        assert rhs.to_dict() == before, f"'{lhs_str}'.constrain('{rhs_str}') mutated the rhs"


def check_rhs_is_not_corrupted_by_later_constraints():
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


def check_returned_changed_flag_is_honest():
    """Callers use the return value to decide whether to redo work, so it has to report
    exactly whether the lhs changed."""
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        before = lhs.to_dict()
        changed, error = _try_constrain(lhs, rhs)
        if error is None:
            assert changed is (lhs.to_dict() != before), (
                f"'{lhs_str}'.constrain('{rhs_str}') returned {changed}"
            )


def check_intersects_agrees_with_constrain():
    """``constrain`` raises exactly when ``intersects`` is False."""
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        intersects = lhs.intersects(rhs)
        _, error = _try_constrain(lhs, rhs)
        assert intersects is (error is None), (
            f"'{lhs_str}'.intersects('{rhs_str}') is {intersects}, but constrain "
            f"{'raised ' + type(error).__name__ if error else 'succeeded'}"
        )


def check_constrain_is_idempotent():
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        if _try_constrain(lhs, rhs)[1] is None:
            before = lhs.to_dict()
            assert lhs.constrain(rhs) is False, f"'{lhs_str}'.constrain('{rhs_str}') twice"
            assert lhs.to_dict() == before


def check_constrained_lhs_satisfies_rhs():
    """Guards against making constrain atomic by making it do nothing."""
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        if _try_constrain(lhs, rhs)[1] is None:
            assert lhs.satisfies(rhs), f"'{lhs_str}'.constrain('{rhs_str}') gave '{lhs}'"


def check_constrain_never_weakens_the_lhs():
    """The result is the intersection of both operands, so together with the property above
    this pins that constrain narrows and never drops a constraint."""
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        if _try_constrain(lhs, rhs)[1] is None:
            assert lhs.satisfies(Spec(lhs_str)), f"'{lhs_str}'.constrain('{rhs_str}') gave '{lhs}'"


def check_satisfies_implies_intersects():
    """Satisfaction is subset and intersection is non-empty overlap, so a spec that is inside
    another one also overlaps it. Each dimension implements the two separately, so they can
    diverge, as they did for patch prefixes and architecture wildcards."""
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        if lhs.satisfies(rhs):
            assert lhs.intersects(rhs), (
                f"'{lhs_str}' satisfies '{rhs_str}' but does not intersect it"
            )


def check_satisfies_implies_constrain_succeeds():
    """Constrain is only undefined where the two are disjoint, so it cannot reject a
    constraint the lhs already satisfies."""
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        if lhs.satisfies(rhs):
            _, error = _try_constrain(lhs, rhs)
            assert error is None, (
                f"'{lhs_str}' satisfies '{rhs_str}' but constrain raised {type(error).__name__}"
            )


def check_satisfies_implies_the_narrowing_dimensions_are_unchanged():
    """An lhs that is already inside the rhs has nothing left to intersect, which is
    absorption over the product of the corpus.

    The dimensions asserted are the ones in which an unset value on the lhs is an absent
    constraint. Names, namespaces and edges whose when condition does not apply are
    read as satisfied when the lhs leaves them unset, so constrain legitimately fills those
    in without narrowing the set the lhs denotes. Propagated variants follow a
    non-contradiction rule instead of subset semantics: a spec without such a variant
    satisfies one that propagates it, and still acquires it when constrained; see
    spec_algebra.py's test_a_propagated_variant_follows_non_contradiction. Compiler
    flags are compared by value, since merging a propagating flag with a plain one of the
    same value demotes it; see
    spec_semantics.py's test_flag_propagation_is_invisible_to_satisfies.
    """
    for lhs_str, rhs_str, lhs, rhs in _pairs():
        propagating = any(value.propagate for value in rhs.variants.values())
        if lhs.satisfies(rhs) and not propagating:
            before = _narrowing_dimensions(lhs)
            _try_constrain(lhs, rhs)
            assert _narrowing_dimensions(lhs) == before, (
                f"'{lhs_str}' satisfies '{rhs_str}' but constrain changed it to '{lhs}'"
            )


def check_constrain_with_itself_is_a_no_op():
    """The same object on both sides, which is the case in which a merge that reads its own
    output as it writes it has nothing to stop it."""
    for spec_str in CORPUS:
        spec = Spec(spec_str)
        before = spec.to_dict()
        assert spec.constrain(spec) is False, f"'{spec_str}' constrained with itself"
        assert spec.to_dict() == before, f"'{spec_str}' constrained with itself"


# The order-theoretic laws. ``spec_algebra.py`` says what each of them means on an example; these
# cover the combinations nobody thought to write down.


def check_satisfies_is_transitive():
    corpus = _ordered_corpus()
    satisfies = {
        (a, b): Spec(a).satisfies(Spec(b)) for a, b in itertools.product(corpus, repeat=2)
    }
    for a, b, c in itertools.product(corpus, repeat=3):
        if satisfies[(a, b)] and satisfies[(b, c)]:
            assert satisfies[(a, c)], f"'{a}' is inside '{b}' is inside '{c}'"


def check_constrain_is_the_greatest_lower_bound():
    """Anything inside both operands is inside their meet too. That makes the meet the
    intersection, not merely some spec contained in both."""
    corpus = _ordered_corpus()
    satisfies = {
        (a, b): Spec(a).satisfies(Spec(b)) for a, b in itertools.product(corpus, repeat=2)
    }
    for a, b in itertools.combinations(corpus, 2):
        result = meet(Spec(a), Spec(b))
        for c in corpus:
            if not (satisfies[(c, a)] and satisfies[(c, b)]):
                continue
            assert result is not None, f"'{c}' is inside both '{a}' and '{b}', which are disjoint"
            assert Spec(c).satisfies(result), (
                f"'{c}' is inside both '{a}' and '{b}', but not inside their meet '{result}'"
            )


def check_constrain_is_commutative():
    corpus = _ordered_corpus()
    for a, b in itertools.combinations(corpus, 2):
        forward, backward = meet(Spec(a), Spec(b)), meet(Spec(b), Spec(a))
        assert _denote_the_same_set(forward, backward), (
            f"'{a}' meet '{b}' is '{forward}', the other way around it is '{backward}'"
        )


def check_constrain_is_associative():
    corpus = _ordered_corpus()
    for a, b, c in itertools.combinations(corpus, 3):
        ab, bc = meet(Spec(a), Spec(b)), meet(Spec(b), Spec(c))
        left = meet(ab, Spec(c)) if ab is not None else None
        right = meet(Spec(a), bc) if bc is not None else None
        assert _denote_the_same_set(left, right), (
            f"('{a}' meet '{b}') meet '{c}' is '{left}', "
            f"'{a}' meet ('{b}' meet '{c}') is '{right}'"
        )


def check_constrain_is_monotonic():
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
            assert narrowed.satisfies(widened), (
                f"'{a_str}' is inside '{b_str}', but their meets with '{c_str}', "
                f"'{narrowed}' and '{widened}', are the other way around"
            )


# The laws hold of the state ``constrain`` leaves behind, which only matters if that state
# survives what everything around the algebra does to a spec: printing it and reading it back,
# copying it, and writing it out as a dictionary.


def check_str_round_trips_to_the_same_set():
    for spec_str in CORPUS:
        spec = Spec(spec_str)
        round_tripped = Spec(str(spec))
        assert round_tripped.satisfies(spec) and spec.satisfies(round_tripped), (
            f"'{spec_str}' prints as '{spec}', which reads back as something else"
        )


def check_copy_is_faithful_and_independent():
    for spec_str in CORPUS:
        spec = Spec(spec_str)
        before = spec.to_dict()
        duplicate = spec.copy()
        assert duplicate.to_dict() == before, f"copying '{spec_str}' changed it"
        for other_str in CORPUS:
            _try_constrain(duplicate, Spec(other_str))
            assert spec.to_dict() == before, (
                f"constraining a copy of '{spec_str}' with '{other_str}' reached the original"
            )


def check_dict_round_trips_exactly():
    """Unlike the string form, the dictionary form is the storage format, so it has to keep the
    state itself and not only the set it denotes."""
    for spec_str in CORPUS:
        spec = Spec(spec_str)
        assert Spec.from_dict(spec.to_dict()).to_dict() == spec.to_dict(), spec_str


CHECKS: Tuple[Callable[[], None], ...] = (
    check_lhs_is_unchanged_when_constrain_raises,
    check_rhs_is_never_mutated,
    check_rhs_is_not_corrupted_by_later_constraints,
    check_returned_changed_flag_is_honest,
    check_intersects_agrees_with_constrain,
    check_constrain_is_idempotent,
    check_constrained_lhs_satisfies_rhs,
    check_constrain_never_weakens_the_lhs,
    check_satisfies_implies_intersects,
    check_satisfies_implies_constrain_succeeds,
    check_satisfies_implies_the_narrowing_dimensions_are_unchanged,
    check_constrain_with_itself_is_a_no_op,
    check_satisfies_is_transitive,
    check_constrain_is_the_greatest_lower_bound,
    check_constrain_is_commutative,
    check_constrain_is_associative,
    check_constrain_is_monotonic,
    check_str_round_trips_to_the_same_set,
    check_copy_is_faithful_and_independent,
    check_dict_round_trips_exactly,
)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="append", help="run only this check, repeatable")
    parser.add_argument("--list", action="store_true", help="list the checks and exit")
    args = parser.parse_args(argv)

    if args.list:
        for check in CHECKS:
            print(check.__name__[len("check_") :])
        return 0

    checks: Sequence[Callable[[], None]] = CHECKS
    if args.check:
        by_name = {check.__name__[len("check_") :]: check for check in CHECKS}
        unknown = [name for name in args.check if name not in by_name]
        if unknown:
            parser.error(f"unknown check(s): {', '.join(unknown)}")
        checks = tuple(by_name[name] for name in args.check)

    failures = 0
    with spack.repo.use_repositories(spack.repo.from_path(spack.paths.mock_packages_path)):
        for check in checks:
            name = check.__name__[len("check_") :]
            try:
                check()
            except AssertionError as e:
                failures += 1
                print(f"{name}: FAILED\n  {e}", flush=True)
            else:
                print(f"{name}: ok", flush=True)

    print(f"\n{failures} failure(s) in {len(checks)} check(s)" if failures else "\nno failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

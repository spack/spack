# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""High-level functions to concretize list of specs"""

import contextlib
import importlib
import sys
import time
import traceback
from collections import Counter
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import spack.compilers
import spack.compilers.config
import spack.config
import spack.error
import spack.hash_lookup
import spack.repo
import spack.solver.core
import spack.traverse
import spack.util.parallel
from spack.concretize_ui import (
    DEFAULT_USER_SPEC_GROUP,
    ConcretizerUI,
    HeadlessUI,
    SolveKind,
    concretization_span,
    group_span,
)
from spack.spec import Spec
from spack.util import tty


class SolveOutcome(NamedTuple):
    """What a worker process hands back for one spec, whether the solve worked or not."""

    #: Where the spec was in the input, which the pool does not preserve
    position: int
    #: The concretized spec, or None if the solve raised
    concrete: Optional[Spec]
    #: Seconds spent in the solve
    duration: float
    #: What the solve raised, or None if it succeeded
    error: Optional[Exception]


SpecPairInput = Tuple[Spec, Optional[Spec]]
SpecPair = Tuple[Spec, Spec]
TestsType = Union[bool, Iterable[str]]

if TYPE_CHECKING:
    from spack.solver.reuse import SpecFiltersFactory


def _needs_solving(abstract: Spec, concrete: Optional[Spec]) -> bool:
    """Return whether a spec pair has to go through a solve. A pair that does not is passed
    through unchanged, and is not reported to a frontend.
    """
    return concrete is None and not abstract.concrete


def _concretize_specs_together(
    abstract_specs: Sequence[Spec],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
) -> List[Spec]:
    """Given a number of specs as input, tries to concretize them together.

    Args:
        abstract_specs: abstract specs to be concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
    """
    from spack.solver.asp import Solver

    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    result = Solver(specs_factory=factory).solve(
        abstract_specs, tests=tests, allow_deprecated=allow_deprecated
    )
    return [s.copy() for s in result.specs]


def _concretize_together(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: ConcretizerUI,
) -> List[SpecPair]:
    """Given a number of specs as input, tries to concretize them together.

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        ui: frontend to report progress to. The group these specs belong to is assumed to be
            opened by the caller.
    """
    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]

    start = time.monotonic()
    concrete_specs = _concretize_specs_together(to_concretize, tests=tests, factory=factory)
    duration = time.monotonic() - start

    # A single solve produced all the specs, so they all report the duration of that solve
    result, count = [], 0
    for (abstract, previous), concrete in zip(spec_list, concrete_specs):
        result.append((abstract, concrete))
        if not _needs_solving(abstract, previous):
            continue
        count += 1
        ui.on_spec_concretized(abstract, concrete=concrete, count=count, duration=duration)

    return result


def _concretize_together_when_possible(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: ConcretizerUI,
) -> List[SpecPair]:
    """Given a number of specs as input, tries to concretize them together to the extent possible.

    See documentation for ``unify: when_possible`` concretization for the precise definition of
    "to the extent possible".

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        ui: frontend to report progress to.
    """
    from spack.solver.asp import Solver

    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    old_concrete_to_abstract = {
        concrete: abstract for (abstract, concrete) in spec_list if concrete
    }
    to_report = {
        abstract for abstract, concrete in spec_list if _needs_solving(abstract, concrete)
    }

    result_by_user_spec: Dict[Spec, Spec] = {}
    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    j = 0
    start = time.monotonic()
    for result in Solver(specs_factory=factory).solve_in_rounds(
        to_concretize, tests=tests, allow_deprecated=allow_deprecated
    ):
        now = time.monotonic()
        duration = now - start
        for abstract, concrete in result.specs_by_input.items():
            if abstract not in to_report:
                continue
            j += 1
            ui.on_spec_concretized(abstract, concrete=concrete, count=j, duration=duration)
        result_by_user_spec.update(result.specs_by_input)
        start = now

    # If the "abstract" spec is a concrete spec from the previous concretization
    # translate it back to an abstract spec. Otherwise, keep the abstract spec
    return [
        (old_concrete_to_abstract.get(abstract, abstract), concrete)
        for abstract, concrete in sorted(result_by_user_spec.items())
    ]


def _concretize_separately(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: ConcretizerUI,
    processes: int,
) -> List[SpecPair]:
    """Concretizes the input specs separately from each other.

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        ui: frontend to report progress to.
        processes: size of the process pool
    """
    from spack.bootstrap import (
        ensure_bootstrap_configuration,
        ensure_clingo_importable_or_raise,
        ensure_winsdk_external_or_raise,
    )

    to_concretize = [abstract for abstract, concrete in spec_list if not concrete]
    args = [
        (i, str(abstract), tests, factory)
        for i, abstract in enumerate(to_concretize)
        if not abstract.concrete
    ]
    ret = [(i, abstract) for i, abstract in enumerate(to_concretize) if abstract.concrete]
    try:
        # Ensure we don't try to bootstrap clingo in parallel
        importlib.import_module("clingo")
    except ImportError:
        with ensure_bootstrap_configuration():
            ensure_clingo_importable_or_raise()

    # ensure we don't try to detect winsdk in parallel
    if sys.platform == "win32":
        ensure_winsdk_external_or_raise()

    # Ensure all the indexes have been built or updated, since
    # otherwise the processes in the pool may timeout on waiting
    # for a write lock. We do this indirectly by retrieving the
    # provider index, which should in turn trigger the update of
    # all the indexes if there's any need for that.
    _ = spack.repo.PATH.provider_index

    # Ensure we have compilers in packages.yaml to avoid that
    # processes try to write the config file in parallel
    _ = spack.compilers.config.all_compilers()

    # Solve the environment in parallel on Linux. imap_unordered falls back to a serial map when
    # parallelism is disabled (e.g. Windows), and when there is at most one spec to solve
    for j, outcome in enumerate(
        spack.util.parallel.imap_unordered(
            _concretize_task, args, processes=processes, maxtaskperchild=1, serialize_env=True
        ),
        start=1,
    ):
        if outcome.error is not None:
            raise outcome.error
        if outcome.concrete is None:
            raise spack.error.SpackError(
                f"concretization of {to_concretize[outcome.position]} produced neither a spec nor "
                f"an error"
            )
        ret.append((outcome.position, outcome.concrete))
        ui.on_spec_concretized(
            to_concretize[outcome.position],
            concrete=outcome.concrete,
            count=j,
            duration=outcome.duration,
        )

    # Add specs in original order, then combine the ones passed in as abstract with the ones
    # passed in as pairs
    ret.sort(key=lambda x: x[0])

    return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
        (abstract, concrete) for abstract, concrete in spec_list if concrete
    ]


def _concretize_task(
    packed_arguments: Tuple[int, str, TestsType, Optional["SpecFiltersFactory"]],
) -> SolveOutcome:
    index, spec_str, tests, factory = packed_arguments
    with tty.SuppressOutput(msg_enabled=False):
        start = time.time()
        try:
            spec = concretize_one(Spec(spec_str), tests=tests, factory=factory)
        except Exception as e:
            # Tracebacks don't pickle, so record this one where the parent can print it
            if isinstance(e, spack.error.SpackError):
                e.traceback = traceback.format_exc()
            return SolveOutcome(index, None, time.time() - start, e)
        return SolveOutcome(index, spec, time.time() - start, None)


def concretize_one(
    spec: Union[str, Spec],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: Optional[ConcretizerUI] = None,
) -> Spec:
    """Return a concretized copy of the given spec.

    Args:
        tests: if False disregard test dependencies, if a list of names activate them for
            the packages in the list, if True activate test dependencies for all packages.
        factory: optional factory to produce a list of specs to be reused
        ui: frontend to report the solve to. Defaults to a headless frontend.
    """
    ui = ui or HeadlessUI()
    with concretization_span(ui):
        return _concretize_one(spec, tests=tests, factory=factory, ui=ui)


def _concretize_one(
    spec: Union[str, Spec],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: ConcretizerUI,
) -> Spec:
    """Concretize a single spec, as a group of one, inside a concretization that started."""
    if isinstance(spec, str):
        spec = Spec(spec)
    spec = spack.hash_lookup.lookup_hash(spec)

    # A single spec takes a single solve, whatever "concretizer:unify" prescribes
    with group_span(
        ui,
        group=DEFAULT_USER_SPEC_GROUP,
        kind=SolveKind.TOGETHER,
        total=0 if spec.concrete else 1,
        processes=1,
    ):
        if spec.concrete:
            return spec.copy()

        start = time.monotonic()
        concrete = _solve_one(spec, tests=tests, factory=factory, ui=ui)
        ui.on_spec_concretized(spec, concrete=concrete, count=1, duration=time.monotonic() - start)
        return concrete


def _solve_one(
    spec: Spec, *, tests: TestsType, factory: Optional["SpecFiltersFactory"], ui: ConcretizerUI
) -> Spec:
    """Run the single solve that concretizes ``spec``, and pick its answer."""
    from spack.solver.asp import Solver

    for node in spec.traverse():
        if not node.name:
            raise spack.error.SpecError(
                f"Spec {node} has no name; cannot concretize an anonymous spec"
            )

    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    result = Solver(specs_factory=factory, ui=ui).solve(
        [spec], tests=tests, allow_deprecated=allow_deprecated
    )

    # take the best answer
    opt, i, answer = min(result.answers)
    name = spec.name
    # TODO: Consolidate this code with similar code in solve.py
    if spack.repo.PATH.is_virtual(spec.name):
        providers = [s.name for s in answer.values() if s.package.provides(name)]
        name = providers[0]

    node = spack.solver.core.min_dupe_node(pkg=name)
    assert node in answer, (
        f"cannot find {name} in the list of specs {','.join([n.pkg for n in answer.keys()])}"
    )

    concretized = answer[node]
    return concretized


def solve_kind(unify: Any) -> SolveKind:
    """Return the kind of solve that a ``concretizer:unify`` value prescribes.

    Raises:
        spack.error.ConfigError: if ``unify`` is not a value the schema allows
    """
    if unify == "when_possible":
        return SolveKind.WHEN_POSSIBLE
    if unify not in (True, False):
        raise spack.error.ConfigError(f"concretization strategy not implemented [{unify}]")
    return SolveKind.TOGETHER if unify else SolveKind.SEPARATELY


def _reported_total(spec_list: Sequence[SpecPairInput]) -> int:
    """Return how many specs a group concretizing ``spec_list`` reports as concretized, which is
    the ``total`` a frontend counts against. Only the specs that go through a solve are reported,
    whatever the strategy.
    """
    return sum(1 for abstract, concrete in spec_list if _needs_solving(abstract, concrete))


def _processes_for(kind: SolveKind, total: int) -> int:
    """Return the size of the process pool that concretizing ``total`` specs as ``kind``
    prescribes uses. Only solving separately runs more than one process.
    """
    if kind is not SolveKind.SEPARATELY or not total:
        return 1
    if not spack.util.parallel.ENABLE_PARALLELISM:
        return 1
    return min(total, spack.config.determine_number_of_jobs(parallel=True))


@contextlib.contextmanager
def solve_group(
    ui: ConcretizerUI, *, group: str, kind: SolveKind, spec_list: Sequence[SpecPairInput]
) -> Iterator[int]:
    """Open the group that concretizes ``spec_list`` as ``kind`` prescribes, and yield the size
    of the process pool it announced, so that the pool that runs is the one a frontend was told
    about. A group whose specs need no solve announces a total of zero, and a frontend sees it
    open and close with nothing in between.
    """
    total = _reported_total(spec_list)
    processes = _processes_for(kind, total)
    with group_span(ui, group=group, kind=kind, total=total, processes=processes):
        yield processes


def concretize_spec_pairs(
    to_concretize: List[SpecPairInput],
    *,
    tests: TestsType = False,
    ui: Optional[ConcretizerUI] = None,
) -> List[Spec]:
    """Concretize the abstract specs of a list of (abstract, concrete) pairs.

    Any abstract spec with a concrete spec associated with it concretizes to that spec. Any
    abstract spec with ``None`` for its concrete spec is newly concretized. Respects the
    unification rules from configuration.

    Args:
        to_concretize: list of tuples to concretize. First entry is abstract spec, second entry
            is an already concrete spec, or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        ui: frontend to report progress to. Defaults to a headless frontend.
    """
    ui = ui or HeadlessUI()
    with concretization_span(ui):
        return _dispatch_concretization(to_concretize, tests=tests, ui=ui)


def _dispatch_concretization(
    to_concretize: List[SpecPairInput], *, tests: TestsType, ui: ConcretizerUI
) -> List[Spec]:
    kind = solve_kind(spack.config.CONFIG.get("concretizer:unify", False))

    # Special case for concretizing a single spec
    if len(to_concretize) == 1:
        abstract, concrete = to_concretize[0]
        if concrete is None:
            return [_concretize_one(abstract, tests=tests, ui=ui)]
        # Nothing to solve, so the group reports a total of zero
        with group_span(ui, group=DEFAULT_USER_SPEC_GROUP, kind=kind, total=0, processes=1):
            return [concrete]

    # Special case if every spec is either concrete or has an abstract hash
    if all(
        concrete or abstract.concrete or abstract.abstract_hash
        for abstract, concrete in to_concretize
    ):
        # No spec is solved, so the group reports a total of zero
        with group_span(ui, group=DEFAULT_USER_SPEC_GROUP, kind=kind, total=0, processes=1):
            # Get all the concrete specs
            ret = [
                concrete
                or (abstract if abstract.concrete else spack.hash_lookup.lookup_hash(abstract))
                for abstract, concrete in to_concretize
            ]

            # If unify: true, check that specs don't conflict
            # Since all concrete, "when_possible" is not relevant
            if kind is SolveKind.TOGETHER:
                runtimes = spack.repo.PATH.packages_with_tags("runtime")
                specs_per_name = Counter(
                    spec.name
                    for spec in spack.traverse.traverse_nodes(
                        ret, deptype=("link", "run"), key=spack.traverse.by_dag_hash
                    )
                    if spec.name not in runtimes  # runtimes are allowed multiple times
                )

                conflicts = sorted(name for name, count in specs_per_name.items() if count > 1)
                if conflicts:
                    raise spack.error.SpecError(
                        "Specs conflict and `concretizer:unify` is configured true.",
                        f"    specs depend on multiple versions of {', '.join(conflicts)}",
                    )
            return ret

    # Standard case
    with solve_group(
        ui, group=DEFAULT_USER_SPEC_GROUP, kind=kind, spec_list=to_concretize
    ) as processes:
        if kind is SolveKind.TOGETHER:
            concretized = _concretize_together(to_concretize, tests=tests, ui=ui)
        elif kind is SolveKind.WHEN_POSSIBLE:
            concretized = _concretize_together_when_possible(to_concretize, tests=tests, ui=ui)
        else:
            concretized = _concretize_separately(
                to_concretize, tests=tests, ui=ui, processes=processes
            )
        return [concrete for _, concrete in concretized]

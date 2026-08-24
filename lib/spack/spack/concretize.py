# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""High-level functions to concretize list of specs"""

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
from spack.concretize_ui import BufferedUI, ConcretizerUI, HeadlessUI, SolveKind
from spack.spec import Spec
from spack.util import tty


class SolveReporting(NamedTuple):
    """What a worker process should buffer of the solves it runs, so the owning process can
    replay them into its frontend.
    """

    #: Record the start and the result of each solve
    solves: bool
    #: Also record the generated ASP program, which is tens of MiB per solve
    asp_program: bool


class SolveOutcome(NamedTuple):
    """What a worker process hands back for one spec, whether the solve worked or not."""

    #: Where the spec was in the input, which the pool does not preserve
    position: int
    #: The concretized spec, or None if the solve raised
    concrete: Optional[Spec]
    #: Seconds spent in the solve
    duration: float
    #: The events of the solve, to replay into the frontend, or None if they were not recorded
    buffered: Optional[BufferedUI]
    #: What the solve raised, or None if it succeeded
    error: Optional[Exception]


SpecPairInput = Tuple[Spec, Optional[Spec]]
SpecPair = Tuple[Spec, Spec]
TestsType = Union[bool, Iterable[str]]

if TYPE_CHECKING:
    from spack.solver.reuse import SpecFiltersFactory


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


def concretize_together(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: Optional[ConcretizerUI] = None,
) -> List[SpecPair]:
    """Given a number of specs as input, tries to concretize them together.

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        ui: frontend to report progress to. Defaults to a headless frontend.
    """
    ui = ui or HeadlessUI()

    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    abstract_specs = [abstract for abstract, _ in spec_list]

    ui.on_concretization_started(kind=SolveKind.TOGETHER, total=len(to_concretize), processes=1)
    start = time.monotonic()
    concrete_specs = _concretize_specs_together(to_concretize, tests=tests, factory=factory)
    duration = time.monotonic() - start

    # A single solve produced all the specs, so they all report the duration of that solve
    result = list(zip(abstract_specs, concrete_specs))
    for count, (abstract, concrete) in enumerate(result, start=1):
        ui.on_spec_concretized(abstract, concrete=concrete, count=count, duration=duration)

    return result


def concretize_together_when_possible(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: Optional[ConcretizerUI] = None,
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
        ui: frontend to report progress to. Defaults to a headless frontend.
    """
    from spack.solver.asp import Solver

    ui = ui or HeadlessUI()

    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    old_concrete_to_abstract = {
        concrete: abstract for (abstract, concrete) in spec_list if concrete
    }

    result_by_user_spec: Dict[Spec, Spec] = {}
    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    j = 0
    ui.on_concretization_started(
        kind=SolveKind.WHEN_POSSIBLE, total=len(to_concretize), processes=1
    )
    start = time.monotonic()
    for result in Solver(specs_factory=factory).solve_in_rounds(
        to_concretize, tests=tests, allow_deprecated=allow_deprecated
    ):
        now = time.monotonic()
        duration = now - start
        for abstract, concrete in result.specs_by_input.items():
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


def concretize_separately(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    ui: Optional[ConcretizerUI] = None,
) -> List[SpecPair]:
    """Concretizes the input specs separately from each other.

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        ui: frontend to report progress to. Defaults to a headless frontend.
    """
    from spack.bootstrap import (
        ensure_bootstrap_configuration,
        ensure_clingo_importable_or_raise,
        ensure_winsdk_external_or_raise,
    )

    ui = ui or HeadlessUI()
    to_concretize = [abstract for abstract, concrete in spec_list if not concrete]
    # Workers can't call the frontend, so they buffer their events and we replay them here.
    reporting = SolveReporting(ui.reports_solves, ui.reports_asp_program)
    args = [
        (i, str(abstract), tests, factory, reporting)
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
    # parallelism is disabled (e.g. Windows)
    num_procs = 1
    if args and spack.util.parallel.ENABLE_PARALLELISM:
        num_procs = min(len(args), spack.config.determine_number_of_jobs(parallel=True))
    ui.on_concretization_started(kind=SolveKind.SEPARATELY, total=len(args), processes=num_procs)

    # Early return if there is nothing to do
    if len(args) == 0:
        # Still have to combine the things that were passed in as abstract with the things
        # that were passed in as pairs
        return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
            (abstract, concrete) for abstract, concrete in spec_list if concrete
        ]

    for j, outcome in enumerate(
        spack.util.parallel.imap_unordered(
            _concretize_task, args, processes=num_procs, maxtaskperchild=1, serialize_env=True
        ),
        start=1,
    ):
        # Replay before raising, so a solve that failed still reports what it had to say
        if outcome.buffered is not None:
            outcome.buffered.replay(ui)
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

    # Add specs in original order
    ret.sort(key=lambda x: x[0])

    return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
        (abstract, concrete) for abstract, concrete in spec_list if concrete
    ]


def _concretize_task(
    packed_arguments: Tuple[int, str, TestsType, Optional["SpecFiltersFactory"], "SolveReporting"],
) -> SolveOutcome:
    index, spec_str, tests, factory, reporting = packed_arguments
    # A fresh buffer per task, so the serial fallback doesn't accumulate events across specs
    buffered = BufferedUI(asp_program=reporting.asp_program) if reporting.solves else None
    with tty.SuppressOutput(msg_enabled=False):
        start = time.time()
        try:
            spec = concretize_one(Spec(spec_str), tests=tests, factory=factory, ui=buffered)
        except Exception as e:
            # Tracebacks don't pickle, so record this one where the parent can print it
            if isinstance(e, spack.error.SpackError):
                e.traceback = traceback.format_exc()
            return SolveOutcome(index, None, time.time() - start, buffered, e)
        return SolveOutcome(index, spec, time.time() - start, buffered, None)


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
    from spack.solver.asp import Solver

    if isinstance(spec, str):
        spec = Spec(spec)
    spec = spack.hash_lookup.lookup_hash(spec)

    if spec.concrete:
        return spec.copy()

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
    """Return the kind of solve that a ``concretizer:unify`` value prescribes."""
    if unify == "when_possible":
        return SolveKind.WHEN_POSSIBLE
    return SolveKind.TOGETHER if unify else SolveKind.SEPARATELY


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
    error: Optional[BaseException] = None
    try:
        return _dispatch_concretization(to_concretize, tests=tests, ui=ui)
    except BaseException as e:
        error = e
        raise
    finally:
        ui.on_finished(error=error)


def _dispatch_concretization(
    to_concretize: List[SpecPairInput], *, tests: TestsType, ui: ConcretizerUI
) -> List[Spec]:
    """Run the concretization strategy that ``concretizer:unify`` prescribes."""
    kind = solve_kind(spack.config.CONFIG.get("concretizer:unify", False))

    # Special case for concretizing a single spec
    if len(to_concretize) == 1:
        abstract, concrete = to_concretize[0]
        return [concrete or concretize_one(abstract, tests=tests, ui=ui)]

    # Special case if every spec is either concrete or has an abstract hash
    if all(
        concrete or abstract.concrete or abstract.abstract_hash
        for abstract, concrete in to_concretize
    ):
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
    concretize_method = concretize_separately  # unify: false
    if kind is SolveKind.TOGETHER:
        concretize_method = concretize_together
    elif kind is SolveKind.WHEN_POSSIBLE:
        concretize_method = concretize_together_when_possible

    concretized = concretize_method(to_concretize, tests=tests, ui=ui)
    return [concrete for _, concrete in concretized]

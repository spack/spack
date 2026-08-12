# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""High-level functions to concretize list of specs"""

import importlib
import io
import sys
import time
from collections import Counter
from typing import (
    TYPE_CHECKING,
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
import spack.traverse as traverse
import spack.util.parallel
from spack.spec import Spec
from spack.util import tty
from spack.util.string import comma_and

SpecPairInput = Tuple[Spec, Optional[Spec]]
SpecPair = Tuple[Spec, Spec]
TestsType = Union[bool, Iterable[str]]

if TYPE_CHECKING:
    from spack.solver.asp import OutputConfiguration
    from spack.solver.reuse import SpecFiltersFactory


class _DiagnosticFlags(NamedTuple):
    """Picklable subset of ``OutputConfiguration`` for solves in worker processes.

    Workers can't share the parent's output streams, so they get these flags, capture
    diagnostics in a local buffer, and return the captured text with the result.
    """

    timers: bool = False
    stats: bool = False
    criteria: bool = False
    asp: bool = False
    setup_only: bool = False

    @staticmethod
    def from_output(output: Optional["OutputConfiguration"]) -> Optional["_DiagnosticFlags"]:
        if output is None:
            return None
        flags = _DiagnosticFlags(
            timers=output.timers,
            stats=output.stats,
            criteria=output.criteria,
            asp=output.out is not None,
            setup_only=output.setup_only,
        )
        # all-default flags mean there is nothing to capture
        return flags if any(flags) else None

    def to_output(self, buffer: io.StringIO) -> "OutputConfiguration":
        """Build an ``OutputConfiguration`` that captures all diagnostics in ``buffer``."""
        from spack.solver.asp import OutputConfiguration

        return OutputConfiguration(
            timers=self.timers,
            stats=self.stats,
            criteria=self.criteria,
            out=buffer if self.asp else None,
            setup_only=self.setup_only,
            stream=buffer,
        )


def _concretize_specs_together(
    abstract_specs: Sequence[Spec],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    output: Optional["OutputConfiguration"] = None,
) -> List[Spec]:
    """Given a number of specs as input, tries to concretize them together.

    Args:
        abstract_specs: abstract specs to be concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        output: optional configuration for solver diagnostics
    """
    from spack.solver.asp import Solver

    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    result = Solver(specs_factory=factory).solve(
        abstract_specs, tests=tests, allow_deprecated=allow_deprecated, output=output
    )
    if output is not None and output.setup_only:
        return []
    return [s.copy() for s in result.specs]


def concretize_together(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    output: Optional["OutputConfiguration"] = None,
) -> List[SpecPair]:
    """Given a number of specs as input, tries to concretize them together.

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        output: optional configuration for solver diagnostics. With ``setup_only`` no
            concretization is performed and the result is empty.
    """
    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    abstract_specs = [abstract for abstract, _ in spec_list]
    concrete_specs = _concretize_specs_together(
        to_concretize, tests=tests, factory=factory, output=output
    )
    return list(zip(abstract_specs, concrete_specs))


def concretize_together_when_possible(
    spec_list: Sequence[SpecPairInput],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    output: Optional["OutputConfiguration"] = None,
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
        output: optional configuration for solver diagnostics, applied to every round. With
            ``setup_only`` only the first round is set up and the result is empty.
    """
    from spack.solver.asp import Solver

    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    old_concrete_to_abstract = {
        concrete: abstract for (abstract, concrete) in spec_list if concrete
    }

    result_by_user_spec: Dict[Spec, Spec] = {}
    allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
    j = 0
    start = time.monotonic()
    for result in Solver(specs_factory=factory).solve_in_rounds(
        to_concretize, tests=tests, allow_deprecated=allow_deprecated, output=output
    ):
        if output is not None and output.setup_only:
            return []
        now = time.monotonic()
        duration = now - start
        percentage = int((j + 1) / len(to_concretize) * 100)
        for abstract, concrete in result.specs_by_input.items():
            tty.verbose(
                f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
                f"{abstract.colored_str}"
            )
            j += 1
        sys.stdout.flush()
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
    output: Optional["OutputConfiguration"] = None,
) -> List[SpecPair]:
    """Concretizes the input specs separately from each other.

    Args:
        spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized
        tests: list of package names for which to consider tests dependencies. If True, all nodes
            will have test dependencies. If False, test dependencies will be disregarded.
        factory: optional factory to produce a list of specs to be reused
        output: optional configuration for solver diagnostics. Each solve captures its
            diagnostics in the worker process; they are printed to ``output.stream`` as
            results arrive, labeled with the input spec. With ``setup_only`` no
            concretization is performed and the result is empty.
    """
    from spack.bootstrap import (
        ensure_bootstrap_configuration,
        ensure_clingo_importable_or_raise,
        ensure_winsdk_external_or_raise,
    )

    diag_flags = _DiagnosticFlags.from_output(output)
    to_concretize = [abstract for abstract, concrete in spec_list if not concrete]
    args = [
        (i, str(abstract), tests, factory, diag_flags)
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

    # Early return if there is nothing to do
    if len(args) == 0:
        # Still have to combine the things that were passed in as abstract with the things
        # that were passed in as pairs
        return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
            (abstract, concrete) for abstract, concrete in spec_list if concrete
        ]

    # Solve the environment in parallel on Linux
    num_procs = min(len(args), spack.config.determine_number_of_jobs(parallel=True))

    msg = "Starting concretization"
    # no parallel conc on Windows
    if not sys.platform == "win32" and num_procs > 1:
        msg += f" pool with {num_procs} processes"
    tty.msg(msg)

    diag_stream = (output.stream or sys.stdout) if output is not None else sys.stdout
    for j, (i, concrete, duration, diagnostics) in enumerate(
        spack.util.parallel.imap_unordered(
            _concretize_task,
            args,
            processes=num_procs,
            debug=tty.is_debug(),
            maxtaskperchild=1,
            serialize_env=True,
        )
    ):
        if diagnostics:
            # Blocks are captured atomically per solve, so parallel completion can't
            # interleave lines; they arrive in completion order, hence the spec label.
            print(f"==> Solve diagnostics for {to_concretize[i].colored_str}", file=diag_stream)
            diag_stream.write(diagnostics)
            diag_stream.flush()
        if concrete is None:  # setup only, no answer to record
            continue
        ret.append((i, concrete))
        percentage = int((j + 1) / len(args) * 100)
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
            f"{to_concretize[i].colored_str}"
        )
        sys.stdout.flush()

    if diag_flags is not None and diag_flags.setup_only:
        return []

    # Add specs in original order
    ret.sort(key=lambda x: x[0])

    return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
        (abstract, concrete) for abstract, concrete in spec_list if concrete
    ]


def _concretize_task(
    packed_arguments: Tuple[
        int, str, TestsType, Optional["SpecFiltersFactory"], Optional[_DiagnosticFlags]
    ],
) -> Tuple[int, Optional[Spec], float, str]:
    index, spec_str, tests, factory, diag_flags = packed_arguments
    output = None
    buffer = None
    if diag_flags is not None:
        buffer = io.StringIO()
        output = diag_flags.to_output(buffer)
    with tty.SuppressOutput(msg_enabled=False):
        start = time.time()
        spec: Optional[Spec] = None
        if diag_flags is not None and diag_flags.setup_only:
            # There is no answer to extract, so don't go through concretize_one
            from spack.solver.asp import Solver

            allow_deprecated = spack.config.CONFIG.get("config:deprecated", False)
            Solver(specs_factory=factory).solve(
                [Spec(spec_str)], tests=tests, allow_deprecated=allow_deprecated, output=output
            )
        else:
            spec = concretize_one(Spec(spec_str), tests=tests, factory=factory, output=output)
        diagnostics = buffer.getvalue() if buffer is not None else ""
        return index, spec, time.time() - start, diagnostics


def concretize_one(
    spec: Union[str, Spec],
    *,
    tests: TestsType = False,
    factory: Optional["SpecFiltersFactory"] = None,
    output: Optional["OutputConfiguration"] = None,
) -> Spec:
    """Return a concretized copy of the given spec.

    Args:
        tests: if False disregard test dependencies, if a list of names activate them for
            the packages in the list, if True activate test dependencies for all packages.
        factory: optional factory to produce a list of specs to be reused
        output: optional configuration for solver diagnostics. ``setup_only`` is not
            supported here since there would be no concrete spec to return.
    """
    from spack.solver.asp import Solver, SpecBuilder

    if output is not None and output.setup_only:
        raise ValueError("concretize_one does not support setup-only solves")

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
    result = Solver(specs_factory=factory).solve(
        [spec], tests=tests, allow_deprecated=allow_deprecated, output=output
    )

    # take the best answer
    opt, i, answer = min(result.answers)
    name = spec.name
    # TODO: Consolidate this code with similar code in solve.py
    if spack.repo.PATH.is_virtual(spec.name):
        providers = [s.name for s in answer.values() if s.package.provides(name)]
        name = providers[0]

    node = SpecBuilder.make_node(pkg=name)
    assert node in answer, (
        f"cannot find {name} in the list of specs {','.join([n.pkg for n in answer.keys()])}"
    )

    concretized = answer[node]
    return concretized


def short_circuit_all_concrete(to_concretize: List[SpecPairInput]) -> Optional[List[Spec]]:
    unify = spack.config.CONFIG.get("concretizer:unify", False)

    if all(
        concrete or abstract.concrete or abstract.abstract_hash
        for abstract, concrete in to_concretize
    ):
        ret = [
            concrete
            or (abstract if abstract.concrete else spack.hash_lookup.lookup_hash(abstract))
            for abstract, concrete in to_concretize
        ]

        # If unify: true, check that specs don't conflict
        # Since all concrete, "when_possible" is not relevant
        if unify is True:  # True, "when_possible", False are possible values
            runtimes = spack.repo.PATH.packages_with_tags("runtime")
            specs_per_name = Counter(
                spec.name
                for spec in traverse.traverse_nodes(
                    ret, deptype=("link", "run"), key=traverse.by_dag_hash
                )
                if spec.name not in runtimes  # runtimes are allowed multiple times
            )

            conflicts = sorted(name for name, count in specs_per_name.items() if count > 1)
            if conflicts:
                raise spack.error.SpecError(
                    "Specs conflict and `concretizer:unify` is configured true.",
                    f"    specs depend on multiple versions of {comma_and(conflicts)}",
                )
        return ret
    return None

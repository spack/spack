# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Non-fixture utilities for test code. Must be imported."""

from typing import Dict, List, Optional, Sequence, Tuple

from spack.concretize_ui import ConcretizerUI, SolveKind
from spack.main import make_argument_parser
from spack.solver.result import Result
from spack.spec import Spec
from spack.util.timer import BaseTimer


class SpackCommandArgs:
    """Use this to get an Args object like what is passed into
    a command.

    Useful for emulating args in unit tests that want to check
    helper functions in Spack commands. Ensures that you get all
    the default arg values established by the parser.

    Example usage::

        install_args = SpackCommandArgs("install")("-v", "mpich")
    """

    def __init__(self, command_name):
        self.parser = make_argument_parser()
        self.command_name = command_name

    def __call__(self, *argv, **kwargs):
        self.parser.add_command(self.command_name)
        args, unknown = self.parser.parse_known_args([self.command_name] + list(argv))
        return args


class RecordingUI(ConcretizerUI):
    """Concretizer frontend that records the events it receives, instead of rendering them.

    Each list holds the arguments of the corresponding callback, in the order they were received.

    Example usage::

        ui = RecordingUI()
        spack.concretize.concretize_separately([(Spec("pkg-a"), None)], ui=ui)
        assert ui.started == [(SolveKind.SEPARATELY, 1, 1)]
    """

    def __init__(self) -> None:
        #: (group, is_default) for each group that started
        self.groups: List[Tuple[str, bool]] = []
        #: (kind, total, processes) for each concretization that started
        self.started: List[Tuple[SolveKind, int, int]] = []
        #: (abstract, concrete, count, duration) for each spec that was concretized
        self.concretized: List[Tuple[Spec, Spec, int, float]] = []
        #: the specs of each solve that started
        self.solves: List[List[Spec]] = []
        #: the ASP program of each solve that was set up
        self.programs: List[List[str]] = []
        #: (result, timer, statistics, cached) for each solve that finished
        self.finished: List[Tuple[Result, BaseTimer, Optional[Dict], bool]] = []
        #: (elapsed, models, best_cost) for each progress tick of a running solve
        self.progress: List[Tuple[float, int, Optional[List[int]]]] = []
        #: the error each concretization ended with, None when it succeeded
        self.errors: List[Optional[BaseException]] = []

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        self.groups.append((group, is_default))

    def on_concretization_started(self, *, kind: SolveKind, total: int, processes: int) -> None:
        self.started.append((kind, total, processes))

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        self.concretized.append((abstract, concrete, count, duration))

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        self.solves.append(list(specs))

    def on_asp_program_generated(self, program: List[str]) -> None:
        self.programs.append(program)

    def on_solve_progress(
        self, *, elapsed: float, models: int, best_cost: Optional[List[int]]
    ) -> None:
        self.progress.append((elapsed, models, best_cost))

    def on_solve_finished(
        self, result: Result, *, timer: BaseTimer, statistics: Optional[Dict], cached: bool
    ) -> None:
        self.finished.append((result, timer, statistics, cached))

    def on_finished(self, *, error: Optional[BaseException]) -> None:
        self.errors.append(error)

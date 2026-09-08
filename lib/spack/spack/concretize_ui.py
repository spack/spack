# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a headless no-op base) and the terminal
:class:`TerminalUI` implementation.

Concretization is reported as three nested spans, each with a ``started``/``finished`` pair:

1. the concretization, one per request to concretize a set of specs;
2. the group, inside which the configuration that drives concretization is fixed. Environments
   define groups of user specs, a request without one has a single, default, group;
3. the solve, inside which unification holds. Specs answered by one solve are mutually consistent.

Every span that opens closes exactly once, including when an exception passes through it. A close
signals teardown and reports no outcome, so no callback takes an exception: a diagnostic about
specs belongs on the ``Result``, and anything else propagates to the caller.
"""

import contextlib
import enum
import pickle
import sys
import warnings
import zlib
from typing import Dict, Hashable, Iterator, List, Optional, Sequence, Set, Tuple

from spack.solver.result import Result
from spack.spec import Spec
from spack.util import tty
from spack.util.timer import BaseTimer

#: Name of the group of user specs that every concretization has. An environment can define more,
#: a request without one has only this.
DEFAULT_USER_SPEC_GROUP = "default"


class SolveKind(enum.Enum):
    """How the specs to be concretized are distributed over solves."""

    #: A single solve produces every spec
    TOGETHER = "together"
    #: One solve per set of specs that can be unified
    WHEN_POSSIBLE = "when_possible"
    #: One solve per spec, possibly in parallel
    SEPARATELY = "separately"


class ConcretizerUI:
    """Interface between concretization and a frontend. The methods are no-ops, which makes this
    class usable as a headless frontend.

    Every event is emitted in the process that owns the frontend, and from a single thread.
    Frontends therefore need no locking, and no capture of child output. Work that happens
    elsewhere, in a worker process or in a solver thread, does not call these methods: it hands
    data back to the owning process, which emits the event. Every payload must therefore be
    picklable, since it may cross a process boundary on its way here.
    """

    #: Whether this frontend renders the events of each solve. A solve that runs in a worker
    #: ships them back only when this is set, since that sends a whole Result over a pipe.
    reports_solves = False

    #: Whether this frontend renders the generated ASP program.
    reports_asp_program = False

    def on_concretization_started(self) -> None:
        """A concretization is about to start. Frontends use it to scope the state they keep
        for one request.
        """

    def on_concretization_finished(self) -> None:
        """The concretization that started is over."""

    def on_group_started(self, *, group: str, kind: SolveKind, total: int, processes: int) -> None:
        """The ``group`` of user specs is about to be concretized as ``kind`` prescribes, over
        ``processes`` processes. ``total`` is the number of ``on_spec_concretized`` calls that
        will follow for this group, which frontends may use to show a percentage.
        """

    def on_group_finished(self) -> None:
        """The group that started is over."""

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        """A user spec has been concretized. ``count`` is how many specs of the group have been
        reported so far, including this one, and goes from 1 to the announced ``total``.
        ``duration`` is the time spent in the solve that produced this spec, so specs that come
        out of the same solve report the same duration.
        """

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        """A solve for ``specs`` is about to start. A group takes one solve when its specs are
        unified, and more than one otherwise, so this may be called several times between
        ``on_group_started`` and ``on_group_finished``.
        """

    def on_asp_program_generated(self, program: List[str]) -> None:
        """The ASP program of the solve that started has been generated, before stripping and
        ordering. This is the last event of a solve that is set up but not run.
        """

    def on_solve_progress(
        self, *, elapsed: float, models: int, best_cost: Optional[List[int]]
    ) -> None:
        """A solve that started ``elapsed`` seconds ago is still running, having found ``models``
        models so far, the most recent of which costs ``best_cost``.

        Emitted at most once a second, and only for solves that run in this process. Clingo
        preprocesses the program before its search becomes interruptible, so the first event
        lands well after the first second, and a solve of a few seconds reports none at all.
        """

    def on_solve_finished(
        self,
        result: Optional[Result],
        *,
        timer: BaseTimer,
        statistics: Optional[Dict],
        cached: bool,
    ) -> None:
        """The solve that started is over. ``result`` is None for a solve that was only set up,
        and for one that raised. The timer holds the duration of each phase the solve reached,
        and the statistics are the ones clingo reports, or the ones stored in the concretization
        cache. ``cached`` says which of the two it is: a cached result never ran the solver, so
        it reports no ``on_solve_progress``, and its timer has no solve phases.
        """

    def on_warning(self, message: str, *, key: Optional[Hashable] = None) -> None:
        """A diagnostic that does not stop concretization. ``key`` identifies the fact behind
        the message, so a frontend can report it once even when several solves rediscover it.
        A warning with no key is reported every time. Can be delivered at any point of the
        concretization lifecycle.
        """


#: Frontend that reports nothing. Same class as the contract it implements, aliased so that call
#: sites can say which of the two roles they mean.
HeadlessUI = ConcretizerUI


@contextlib.contextmanager
def concretization_span(ui: ConcretizerUI) -> Iterator[None]:
    """Report the start and the end of a concretization. The end is reported even when the body
    raises, so that a frontend can tear down what it painted. The exception propagates to the
    caller without being passed to the frontend.
    """
    ui.on_concretization_started()
    try:
        yield
    finally:
        ui.on_concretization_finished()


@contextlib.contextmanager
def group_span(
    ui: ConcretizerUI, *, group: str, kind: SolveKind, total: int, processes: int
) -> Iterator[None]:
    """Report the start and the end of one group of user specs. As for ``concretization_span``,
    the end is reported even when the body raises.
    """
    ui.on_group_started(group=group, kind=kind, total=total, processes=processes)
    try:
        yield
    finally:
        ui.on_group_finished()


#: Name of the one event whose payload is buffered compressed, see BufferedUI
ASP_PROGRAM_EVENT = "on_asp_program_generated"


class BufferedUI(ConcretizerUI):
    """Frontend that records what it is told, so that another process can replay it into the
    frontend that owns the terminal.

    A solve that runs in a worker process cannot call a frontend, so it reports to one of these
    instead and the owning process replays what comes back. Only the events a solve emits are
    recorded; the ones that describe the concretization around it are emitted by the owning
    process already.

    Warnings are always recorded, since they are short strings. The events that carry a whole
    Result or an ASP program are recorded only for a frontend that renders them, since those
    are megabytes to send over a pipe.
    """

    def __init__(self, *, solves: bool = True, asp_program: bool = False) -> None:
        self.reports_solves = solves
        self.reports_asp_program = asp_program
        self.events: List[Tuple[str, Sequence, Dict]] = []

    def replay(self, ui: ConcretizerUI) -> None:
        """Emit everything recorded, into ``ui``, in the order it was recorded."""
        for name, args, kwargs in self.events:
            if name == ASP_PROGRAM_EVENT:
                args = (pickle.loads(zlib.decompress(args[0])),)
            getattr(ui, name)(*args, **kwargs)

    def on_warning(self, message: str, *, key: Optional[Hashable] = None) -> None:
        self.events.append(("on_warning", (message,), {"key": key}))

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        if not self.reports_solves:
            return
        self.events.append(("on_solve_started", (list(specs),), {}))

    def on_asp_program_generated(self, program: List[str]) -> None:
        if not self.reports_asp_program:
            return
        # Pickle rather than join the lines: some of them embed a newline, so joining and
        # splitting back is not a round trip.
        blob = zlib.compress(pickle.dumps(program))
        self.events.append((ASP_PROGRAM_EVENT, (blob,), {}))

    def on_solve_progress(
        self, *, elapsed: float, models: int, best_cost: Optional[List[int]]
    ) -> None:
        """Dropped on purpose: a progress tick replayed after the solve is over is worse than
        no tick at all.
        """

    def on_solve_finished(
        self,
        result: Optional[Result],
        *,
        timer: BaseTimer,
        statistics: Optional[Dict],
        cached: bool,
    ) -> None:
        if not self.reports_solves:
            return
        self.events.append(
            (
                "on_solve_finished",
                (result,),
                {"timer": timer, "statistics": statistics, "cached": cached},
            )
        )


class TerminalUI(ConcretizerUI):
    """Terminal frontend: announces groups and solves, and reports per-spec progress."""

    def __init__(self) -> None:
        self.kind = SolveKind.TOGETHER
        self.total = 0
        self.reported_warnings: Set[Hashable] = set()

    def on_concretization_started(self) -> None:
        # A frontend may outlive one concretization, so each starts with a clean slate
        self.reported_warnings = set()

    def on_warning(self, message: str, *, key: Optional[Hashable] = None) -> None:
        if key in self.reported_warnings:
            return
        if key is not None:
            self.reported_warnings.add(key)
        warnings.warn(message)

    def on_group_started(self, *, group: str, kind: SolveKind, total: int, processes: int) -> None:
        self.kind = kind
        self.total = total
        if total == 0:
            return
        if group != DEFAULT_USER_SPEC_GROUP:
            tty.msg(f"Concretizing the '{group}' group of specs")
        if kind is not SolveKind.SEPARATELY:
            return
        msg = "Starting concretization"
        if processes > 1:
            msg += f" pool with {processes} processes"
        tty.msg(msg)

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        if self.kind is SolveKind.TOGETHER:
            return
        percentage = int(count / self.total * 100)
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
            f"{abstract.colored_str}",
            stream=sys.stdout,
        )
        sys.stdout.flush()

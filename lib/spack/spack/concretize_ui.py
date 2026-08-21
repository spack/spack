# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a headless no-op base) and the terminal
:class:`TerminalUI` implementation.
"""

import enum
import pickle
import sys
import zlib
from typing import Dict, List, Optional, Sequence, Tuple

from spack.solver.result import Result
from spack.spec import Spec
from spack.util import tty
from spack.util.timer import BaseTimer


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
    #: buffers its events and ships them back only when this is set, since that sends a whole
    #: Result over a pipe.
    reports_solves = False

    #: Whether this frontend renders the generated ASP program.
    reports_asp_program = False

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        """A group of user specs is about to be concretized."""

    def on_concretization_started(self, *, kind: SolveKind, total: int, processes: int) -> None:
        """``total`` user specs are about to be concretized as ``kind`` prescribes, over
        ``processes`` processes. Called once per group of user specs, before any spec of that
        group is reported, with ``total`` equal to the number of ``on_spec_concretized`` calls
        that will follow for it.
        """

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        """A user spec has been concretized. ``count`` is how many specs of the group have been
        reported so far, including this one, and goes from 1 to the announced ``total``.
        ``duration`` is the time spent in the solve that produced this spec, so specs that come
        out of the same solve report the same duration.
        """

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        """A solve for ``specs`` is about to start. A concretization takes one solve when the
        specs are unified, and more than one otherwise, so this may be called several times
        between ``on_concretization_started`` and the last ``on_spec_concretized``.
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
        self, result: Result, *, timer: BaseTimer, statistics: Optional[Dict], cached: bool
    ) -> None:
        """A solve is over, and produced ``result``. The timer holds the duration of each of its
        phases, and the statistics are the ones clingo reports, or the ones stored in the
        concretization cache. ``cached`` says which of the two it is: a cached result never ran
        the solver, so it reports no ``on_solve_progress``, and its timer has no solve
        phases.

        Not emitted for a solve that was only set up, or one that raised.
        """

    def on_finished(self, *, error: Optional[BaseException]) -> None:
        """Concretization is over, successfully if ``error`` is None. Emitted exactly once per
        concretization, from a ``finally``, so a frontend that renders can rely on it to tear
        down whatever it painted.
        """


#: Frontend that reports nothing. Same class as the contract it implements, aliased so that call
#: sites can say which of the two roles they mean.
HeadlessUI = ConcretizerUI


#: Name of the one event whose payload is buffered compressed, see BufferedUI
ASP_PROGRAM_EVENT = "on_asp_program_generated"


class BufferedUI(ConcretizerUI):
    """Frontend that records what it is told, so that another process can replay it into the
    frontend that owns the terminal.

    A solve that runs in a worker process cannot call a frontend, so it reports to one of these
    instead and the owning process replays what comes back. Only the events a solve emits are
    recorded; the ones that describe the concretization around it are emitted by the owning
    process already.

    A recorded ASP program is held compressed, since it is tens of MiB and has to travel back
    over a pipe.
    """

    def __init__(self, *, asp_program: bool = False) -> None:
        self.reports_solves = True
        self.reports_asp_program = asp_program
        self.events: List[Tuple[str, Sequence, Dict]] = []

    def replay(self, ui: ConcretizerUI) -> None:
        """Emit everything recorded, into ``ui``, in the order it was recorded."""
        for name, args, kwargs in self.events:
            if name == ASP_PROGRAM_EVENT:
                args = (pickle.loads(zlib.decompress(args[0])),)
            getattr(ui, name)(*args, **kwargs)

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
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
        self, result: Result, *, timer: BaseTimer, statistics: Optional[Dict], cached: bool
    ) -> None:
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
        self.pending_group: Optional[str] = None

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        # Held back until we know the group has specs to concretize
        self.pending_group = None if is_default else group

    def on_concretization_started(self, *, kind: SolveKind, total: int, processes: int) -> None:
        self.kind = kind
        self.total = total
        if total == 0:
            return
        if self.pending_group is not None:
            tty.msg(f"Concretizing the '{self.pending_group}' group of specs")
            self.pending_group = None
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

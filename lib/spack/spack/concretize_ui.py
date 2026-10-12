# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a no-op base), the :class:`HeadlessUI` frontend that
only reports warnings, and the terminal :class:`TerminalUI` implementation.

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
import os
import pickle
import shutil
import sys
import threading
import time
import warnings
import zlib
from typing import (
    Callable,
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    TextIO,
    Tuple,
)

import spack.util.tty.color as coloring
from spack.solver.result import Result
from spack.spec import Spec
from spack.util import tty
from spack.util.lang import elide_list
from spack.util.string import plural
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


class ConcretizationPhase(enum.Enum):
    """What the solver is doing, as reported by ``ConcretizerUI.on_phase``."""

    #: Selecting the installed and binary specs that solves may reuse
    REUSE = "reuse"
    #: Translating specs, packages and configuration into an ASP program
    SETUP = "setup"
    #: Grounding the ASP program
    GROUND = "ground"
    #: Searching for the best model
    SOLVE = "solve"
    #: Building concrete specs from the best model, or from a cached result
    BUILD = "build"


class ConcretizerUI:
    """Interface between concretization and a frontend. The methods are no-ops, which makes this
    class usable as a frontend that reports nothing, warnings included.

    Every event is emitted in the process that owns the frontend, and from a single thread.
    Frontends therefore need no locking, and no capture of child output. Work that happens
    elsewhere, in a worker process or in a solver thread, does not call these methods: it
    returns data to the owning process, which emits the event. Every payload must therefore be
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
        self,
        abstract: Spec,
        *,
        concrete: Spec,
        count: int,
        duration: float,
        task: Optional[int] = None,
    ) -> None:
        """A user spec has been concretized. ``count`` is how many specs of the group have been
        reported so far, including this one, and goes from 1 to the announced ``total``.
        ``duration`` is the time spent in the solve that produced this spec, so specs that come
        out of the same solve report the same duration. In a group that concretizes separately,
        ``task`` is the task that solved the spec, as in ``on_phase``, and is None otherwise.
        """

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        """A solve for ``specs`` is about to start. A group takes one solve when its specs are
        unified, and more than one otherwise, so this may be called several times between
        ``on_group_started`` and ``on_group_finished``.
        """

    def on_phase(
        self,
        phase: ConcretizationPhase,
        *,
        task: Optional[int] = None,
        spec: Optional[Spec] = None,
    ) -> None:
        """The solver entered ``phase``. Phases are reported inside a group, but not only inside
        a solve (e.g. reuse selection happens before the solve that uses it starts, and once for
        all the solves of a group that unifies when possible)

        In a group that concretizes separately, the solves of the user specs run as tasks, some of
        them at the same time, and are reported with no solve span. There ``task`` identifies the
        task in the group, ``spec`` is the user spec it solves, and the task is over when
        ``on_spec_concretized`` reports the same ``task``. Two tasks may solve equal specs.

        Phases of a task are reported as they are observed, so some may be skipped.
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
        """

    def on_solve_finished(
        self,
        result: Optional[Result],
        *,
        timer: BaseTimer,
        statistics: Optional[Dict],
        cached: bool,
    ) -> None:
        """The solve that started is over. For a solve that was only set up, and for one that
        raised, ``result`` and ``statistics`` are None and ``cached`` is False. The timer holds
        the duration of each phase the solve reached, and the statistics are the ones clingo
        reports, or the ones stored in the concretization cache. ``cached`` says which of the two
        it is: a cached result never ran the solver, so it reports no ``on_solve_progress``, and
        its timer has no solve phases.
        """

    def on_warning(self, message: str, *, key: Optional[Hashable] = None) -> None:
        """A diagnostic that does not stop concretization. ``key`` identifies the fact behind
        the message, so a frontend can report it once even when several solves rediscover it.
        A warning with no key is reported every time. Can be delivered at any point of the
        concretization lifecycle.
        """


class HeadlessUI(ConcretizerUI):
    """Frontend that shows no progress, and reports each warning once per key, through
    ``warnings.warn``.
    """

    def __init__(self) -> None:
        self.reported_warnings: Set[Hashable] = set()
        #: How many warnings were reported in the current concretization
        self.warning_count = 0

    def on_concretization_started(self) -> None:
        # A frontend can be reused, so warnings reported by a previous concretization are reset
        self.reported_warnings = set()
        self.warning_count = 0

    def on_warning(self, message: str, *, key: Optional[Hashable] = None) -> None:
        if key in self.reported_warnings:
            return
        if key is not None:
            self.reported_warnings.add(key)
        self.warning_count += 1
        warnings.warn(message)


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

    Warnings are always recorded, since they are short strings. The events whose payload is a
    whole Result or an ASP program are recorded only for a frontend that renders them, since
    those are megabytes to send over a pipe.
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
        """Not recorded: a replayed tick would arrive after the solve is over."""

    def on_phase(
        self,
        phase: ConcretizationPhase,
        *,
        task: Optional[int] = None,
        spec: Optional[Spec] = None,
    ) -> None:
        """Not recorded: a replayed phase would arrive after the solve is over."""

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


#: Seconds between two redraws of the status line or the rows
REDRAW_INTERVAL = 0.1

#: What the status line and the rows show for each phase
PHASE_LABELS = {
    ConcretizationPhase.REUSE: "reuse",
    ConcretizationPhase.SETUP: "setup",
    ConcretizationPhase.GROUND: "grounding",
    ConcretizationPhase.SOLVE: "solving",
    ConcretizationPhase.BUILD: "building",
}

#: Width of the phase column of the rows, so that the specs of all rows start in the same column
PHASE_COLUMN = max(len(label) for label in PHASE_LABELS.values()) + 2


class _TaskRow(NamedTuple):
    """What the row of a task running in a group that concretizes separately shows."""

    #: The spec the task solves, colored if the frontend is
    label: str
    #: The phase the task is in
    phase: ConcretizationPhase
    #: When the row appeared, from which its elapsed time is counted
    start: float


class TerminalUI(HeadlessUI):
    """Terminal frontend: announces groups and solves, and reports per-spec progress.

    When ``live``, it also draws a status line, or a row per task in a group that concretizes
    separately. The main thread is blocked while the solver runs, so a thread of this frontend
    redraws them. It writes with ``os.write``, so that a process forked meanwhile never inherits a
    stream lock held by it.

    Output written to ``sys.stdout`` or ``sys.stderr`` while the lines are drawn is printed above
    them.
    """

    def __init__(
        self,
        *,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
        live: Optional[bool] = None,
        get_time: Callable[[], float] = time.monotonic,
        get_terminal_size: Callable[[], os.terminal_size] = shutil.get_terminal_size,
        redraw_interval: Optional[float] = REDRAW_INTERVAL,
        color: Optional[bool] = None,
    ) -> None:
        """
        Args:
            stdout: stream for the status line and the rows, defaults to ``sys.stdout``
            stderr: stream that replaces ``sys.stderr`` while the status line or the rows are
                drawn, defaults to ``sys.stderr``
            live: whether to draw the status line and the rows. Defaults to True if ``stdout`` is
                interactive and debug output is off, since debug messages would scroll them away.
            get_time: clock for the elapsed time of a solve
            get_terminal_size: size of the terminal, to truncate the status line and the rows
            redraw_interval: seconds between redraws by the redraw thread, or None to start no
                thread and redraw only on events and on ``render``
            color: whether to color the status line and the rows. Defaults to what ``--color`` and
                ``SPACK_COLOR`` prescribe for ``stdout``.
        """
        super().__init__()
        self.kind = SolveKind.TOGETHER
        self.total = 0
        self.stdout = stdout if stdout is not None else sys.stdout
        self.stderr = stderr if stderr is not None else sys.stderr
        if live is None:
            live = self.stdout.isatty() and not tty.is_debug()
        self.live = live
        self.get_time = get_time
        self.get_terminal_size = get_terminal_size
        self.redraw_interval = redraw_interval
        self.color = coloring.get_color_when(self.stdout) if color is None else color
        #: How many solves the current group took
        self.rounds = 0
        #: Name of the running group, when it started, how many processes it runs on, and how
        #: many of its specs were concretized
        self.group = DEFAULT_USER_SPEC_GROUP
        self.group_start = 0.0
        self.processes = 1
        self.concretized = 0
        #: Line kept by a finished default group, printed only when another group starts
        self.held_line: Optional[str] = None

        #: Specs of the running solve, colored if the frontend is, the phase the solver is in,
        #: and when the solve started
        self.label = ""
        self.phase: Optional[ConcretizationPhase] = None
        self.solve_start = 0.0
        #: Row of each running task of the group, in the order they appeared
        self.rows: Dict[int, _TaskRow] = {}
        #: Widest label and widest time of the rows of the group so far, which the rows are padded
        #: to, so that the times never move left
        self.label_width = 0
        self.time_width = 0
        #: How many specs of the group the tasks concretized
        self.done = 0
        #: How many lines of the status line or of the rows are on the terminal
        self.drawn_lines = 0
        # Held while the status line or the rows, or output above them, are written
        self.lock = threading.Lock()
        self.stop_redraw = threading.Event()
        self.redraw_thread: Optional[threading.Thread] = None
        self.proxies: List[_StatusLineStream] = []
        self.saved_streams: Tuple[TextIO, TextIO] = (sys.stdout, sys.stderr)

    def on_concretization_started(self) -> None:
        super().on_concretization_started()
        self.held_line = None

        if not self.live:
            return

        self.stdout.flush()
        self.saved_streams = (sys.stdout, sys.stderr)
        self.proxies = [_StatusLineStream(self.stdout, self), _StatusLineStream(self.stderr, self)]
        sys.stdout, sys.stderr = self.proxies

        # If we have a redraw interval start the re-draw loop in a thread
        if self.redraw_interval is not None:
            self.stop_redraw.clear()
            self.redraw_thread = threading.Thread(target=self._redraw_loop, daemon=True)
            self.redraw_thread.start()

    def on_concretization_finished(self) -> None:

        if not self.live:
            return

        if self.redraw_thread is not None:
            self.stop_redraw.set()
            self.redraw_thread.join()
            self.redraw_thread = None

        self._update_line("", None)
        if self.warning_count:
            tty.msg(f"{plural(self.warning_count, 'warning')} reported above")

        with self.lock:
            sys.stdout, sys.stderr = self.saved_streams
            for proxy in self.proxies:
                if proxy.pending:
                    proxy.stream.write(proxy.pending)
                    proxy.stream.flush()
            self.proxies = []

    def on_group_started(self, *, group: str, kind: SolveKind, total: int, processes: int) -> None:
        self.kind = kind
        self.total = total
        self.rounds = 0
        self.group, self.processes, self.concretized = group, processes, 0
        self.group_start = self.get_time()
        if total == 0:
            return
        # In live mode a group is reported by the line it keeps when it finishes
        if self.live:
            if self.held_line is not None:
                self.print_above(self.stdout, self.held_line)
                self.held_line = None
            return
        if group != DEFAULT_USER_SPEC_GROUP:
            tty.msg(f"Concretizing the '{group}' group of specs")
        if kind is not SolveKind.SEPARATELY:
            return
        msg = "Starting concretization"
        if processes > 1:
            msg += f" pool with {processes} processes"
        tty.msg(msg)

    def on_group_finished(self) -> None:
        line = self._group_line() if self.live and self.total else None
        with self.lock:
            self.rows = {}
            self.label_width, self.time_width = 0, 0
            self.done = 0
            self.label, self.phase = "", None
            self._draw()

        if line is None:
            return
        # A concretization with only the default group leaves nothing, as a single solve does
        if self.group == DEFAULT_USER_SPEC_GROUP:
            self.held_line = line
        else:
            self.print_above(self.stdout, line)

    def on_solve_started(self, specs: Sequence[Spec]) -> None:
        with coloring.color_when(self.color):
            label = ", ".join(elide_list([s.colored_str for s in specs], 4))
        self._update_line(label, self.phase)

    def on_phase(
        self,
        phase: ConcretizationPhase,
        *,
        task: Optional[int] = None,
        spec: Optional[Spec] = None,
    ) -> None:
        # Single solve with a single line to update
        if task is None:
            self._update_line(self.label, phase)
            return

        # Parallel solves, e.g. for separate concretization
        with self.lock:
            row = self.rows.get(task)
            if row is None:
                label = ""
                if spec is not None:
                    with coloring.color_when(self.color):
                        label = spec.colored_str
                self.rows[task] = _TaskRow(label, phase, self.get_time())
                self.label_width = max(self.label_width, coloring.clen(label))
            else:
                self.rows[task] = row._replace(phase=phase)
            self._draw()

    def on_solve_finished(
        self,
        result: Optional[Result],
        *,
        timer: BaseTimer,
        statistics: Optional[Dict],
        cached: bool,
    ) -> None:
        self._update_line("", None)
        if result is not None and self.kind is SolveKind.WHEN_POSSIBLE:
            self.rounds += 1

    def on_spec_concretized(
        self,
        abstract: Spec,
        *,
        concrete: Spec,
        count: int,
        duration: float,
        task: Optional[int] = None,
    ) -> None:
        self.concretized = count

        # Parallel tasks
        if task is not None:
            with self.lock:
                self.rows.pop(task, None)
                self.done = count
                self._draw()

        if self.kind is SolveKind.TOGETHER:
            return

        # Verbose output, if requested
        percentage = int(count / self.total * 100)
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
            f"{abstract.colored_str}",
            stream=sys.stdout,
        )
        sys.stdout.flush()

    def render(self) -> None:
        """Redraw the status line or the rows, if any."""
        with self.lock:
            self._draw()

    def print_above(self, stream: TextIO, text: str) -> None:
        """Write ``text`` and a newline to ``stream`` above the status line or the rows."""
        with self.lock:
            self._clear()
            stream.write(text)
            stream.flush()
            self._draw()

    def _group_line(self) -> str:
        """Return the line a finished group keeps on the terminal."""
        specs = plural(self.total, "spec")
        if self.concretized < self.total:
            specs = f"{self.concretized} of {specs}"
        details = ""
        if self.rounds > 1:
            details = f"  ({self.rounds} rounds)"
        elif self.kind is SolveKind.SEPARATELY and self.processes > 1:
            details = f"  ({self.processes} processes)"
        elapsed = f"{self.get_time() - self.group_start:.1f}s"
        # As in the installer, names are bold and secondary details are gray
        colors = coloring.get_colors(self.color)
        name = f"{colors.BOLD}{self.group}{colors.RESET}{' ' * (12 - len(self.group))}"
        time_text = f"{colors.BOLD}{elapsed:>6}{colors.RESET}"
        details = f"{colors.BLACK_BRIGHT}{details}{colors.RESET}" if details else ""
        return f"{colors.BLUE_BRIGHT}==>{colors.RESET} {name} {specs:<9} {time_text}{details}\n"

    def _redraw_loop(self) -> None:
        while not self.stop_redraw.wait(self.redraw_interval):
            self.render()

    def _update_line(self, label: str, phase: Optional[ConcretizationPhase]) -> None:
        with self.lock:
            # Reuse selection happens before the solve starts, and counts as part of it
            if self.phase is None and phase is not None:
                self.solve_start = self.get_time()

            self.label, self.phase = label, phase
            self._draw()

    def _lines(self) -> List[str]:
        """Return the lines to draw: while a group that concretizes separately has tasks left, a
        counter and the rows of the running tasks, otherwise the status line of the running solve.
        Both are under the name of the group, unless it is the default one.
        """
        columns, height = self.get_terminal_size()
        if self.rows or 0 < self.done < self.total:
            return self._task_lines(columns, height)
        if self.phase is None:
            return []
        elapsed = self._elapsed(self.solve_start)
        lines = [self._format(self.phase, self.label, elapsed, columns=columns)]
        if self.group != DEFAULT_USER_SPEC_GROUP:
            header = self._group_tag()
            if self.rounds:
                header += f" round {self.rounds + 1}"
            lines.insert(0, self._cut(header, columns))
        return lines

    def _task_lines(self, columns: int, height: int) -> List[str]:
        counter = f"[{self.done}/{self.total} done]"
        if self.group != DEFAULT_USER_SPEC_GROUP:
            counter = f"{self._group_tag()} {counter}"
        lines = [self._cut(counter, columns)]
        rows = list(self.rows.values())
        # The cursor cannot move up past the top of the terminal to erase a line, so the rows
        # that do not fit are counted on a line of their own
        shown = len(rows) if len(rows) + 1 < height else max(height - 3, 0)
        hidden, rows = len(rows) - shown, rows[:shown]
        times = [self._elapsed(row.start) for row in rows]
        self.time_width = max([self.time_width, *(len(x) for x in times)])
        lines.extend(
            self._format(
                row.phase,
                row.label,
                elapsed.rjust(self.time_width),
                columns=columns,
                column=PHASE_COLUMN,
                label_width=self.label_width,
            )
            for row, elapsed in zip(rows, times)
        )
        if hidden:
            lines.append(f"{hidden} more...")
        return lines

    def _group_tag(self) -> str:
        colors = coloring.get_colors(self.color)
        gray, bold, reset = colors.BLACK_BRIGHT, colors.BOLD, colors.RESET
        return f"{gray}[group:{reset} {bold}{self.group}{reset}{gray}]{reset}"

    def _cut(self, text: str, columns: int) -> str:
        """Return ``text`` cut to fit a line of the terminal, since a line that wraps takes more
        rows than the cursor moves up to erase it.
        """
        if columns <= 1 or coloring.clen(text) < columns:
            return text
        cut = coloring.cmapping(text).plain_to_color(columns - 1)
        return f"{text[:cut]}{coloring.get_colors(self.color).RESET}"

    def _elapsed(self, start: float) -> str:
        return f"{self.get_time() - start:.1f}s"

    def _format(
        self,
        phase: ConcretizationPhase,
        label: str,
        elapsed: str,
        *,
        columns: int,
        column: int = 0,
        label_width: int = 0,
    ) -> str:
        """Return a line with ``phase``, padded to ``column`` characters, ``label``, padded to
        ``label_width`` characters, and ``elapsed``.
        """
        colors = coloring.get_colors(self.color)
        tag = f"[{PHASE_LABELS[phase]}]"
        phase_text = f"{colors.BLUE_BRIGHT}{tag}{colors.RESET}{' ' * (column - len(tag))}"
        elapsed = f"  {elapsed}"
        label = f" {label}" if label else ""
        # A line that wraps takes more rows than the cursor moves up to erase it, so the label is
        # cut to fit, keeping the phase and the elapsed time in view
        room = columns - 1 - coloring.clen(phase_text) - coloring.clen(elapsed)
        if columns > 1 and coloring.clen(label) > room:
            cut = coloring.cmapping(label).plain_to_color(max(room, 0))
            label = f"{label[:cut]}{colors.RESET}"
        # The label has a leading space, which label_width does not count
        width = label_width + 1 if label_width else 0
        if columns > 1:
            width = min(width, room)
        padding = " " * max(width - coloring.clen(label), 0)
        return f"{phase_text}{label}{padding}{elapsed}"

    def _draw(self) -> None:
        """Redraw the status line or the rows, or erase them if there is nothing to show. The
        cursor is left at the end of the last line.
        """
        if not self.live:
            return
        lines = self._lines()
        if not lines:
            self._clear()
            return
        # \033[K erases what is left of a longer old line, \033[J the old lines below the last one
        self._write(self._to_first_line() + "\033[K\n".join(lines) + "\033[J")
        self.drawn_lines = len(lines)

    def _clear(self) -> None:
        if self.drawn_lines:
            self._write(f"{self._to_first_line()}\033[J")
            self.drawn_lines = 0

    def _to_first_line(self) -> str:
        """Return what moves the cursor to the start of the first line drawn."""
        up = f"\033[{self.drawn_lines - 1}A" if self.drawn_lines > 1 else ""
        return f"{up}\r"

    def _write(self, text: str) -> None:
        encoding = getattr(self.stdout, "encoding", None) or "utf-8"
        os.write(self.stdout.fileno(), text.encode(encoding, errors="replace"))


class _StatusLineStream:
    """Stands in for ``sys.stdout`` or ``sys.stderr`` while a ``TerminalUI`` draws its status
    line. Complete lines are written to ``stream`` above the status line. A partial line is held
    until its newline, or until the line is erased, since the next redraw would overwrite it.
    """

    def __init__(self, stream: TextIO, ui: TerminalUI) -> None:
        self.stream = stream
        self.ui = ui
        self.pending = ""
        # A child forked while the line is drawn inherits this object, but not the redraw
        # thread, which may hold the lock of the frontend at the time of the fork
        self.pid = os.getpid()

    def write(self, text: str) -> int:
        if os.getpid() != self.pid:
            return self.stream.write(text)
        head, newline, tail = text.rpartition("\n")
        if not newline:
            self.pending += text
            return len(text)
        complete, self.pending = self.pending + head + newline, tail
        self.ui.print_above(self.stream, complete)
        return len(text)

    def writelines(self, lines: Iterable[str]) -> None:
        for line in lines:
            self.write(line)

    def flush(self) -> None:
        # Complete lines are flushed as they are written, partial ones are held
        if os.getpid() != self.pid:
            self.stream.flush()

    def __getattr__(self, name: str):
        return getattr(self.stream, name)

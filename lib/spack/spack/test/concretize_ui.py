# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the status line and the rows of the terminal frontend of concretization."""

import os
import re
import sys
from typing import List, TextIO

import pytest

import spack.concretize
import spack.environment as ev
from spack.concretize_ui import ConcretizationPhase, SolveKind, TerminalUI, concretization_span
from spack.solver.result import Result
from spack.spec import Spec
from spack.util import tty
from spack.util.timer import Timer
from spack.util.tty.color import csub

#: Cursor up, erase to the end of the line, and erase to the end of the screen
CURSOR_SEQUENCE = re.compile(r"\033\[(\d*)([AKJ])")


def screen(output: str) -> List[str]:
    """Return the lines a terminal shows after printing ``output``, which may contain carriage
    returns, and sequences that move the cursor up or erase to the end of the line or screen.
    """
    lines, row, column = [""], 0, 0
    i = 0
    while i < len(output):
        match = CURSOR_SEQUENCE.match(output, i)
        if match:
            count, command = match.groups()
            if command == "A":
                row = max(row - int(count or 1), 0)
            else:
                lines[row] = lines[row][:column]
                if command == "J":
                    del lines[row + 1 :]
            i = match.end()
            continue
        char = output[i]
        if char == "\r":
            column = 0
        elif char == "\n":
            row += 1
            column = 0
            if row == len(lines):
                lines.append("")
        else:
            line = lines[row].ljust(column)
            lines[row] = line[:column] + char + line[column + 1 :]
            column += 1
        i += 1
    return lines


class Terminal:
    """A terminal that stdout and stderr both write to, and a live frontend drawing on it, with a
    clock that moves only when a test says so.
    """

    def __init__(self, stdout: TextIO, stderr: TextIO) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.now = 0.0
        self.ui = self.frontend()

    def frontend(self, *, columns: int = 80, lines: int = 24, **kwargs) -> TerminalUI:
        """Return a live frontend drawing on this terminal, with no redraw thread and no color
        unless ``kwargs`` say otherwise.
        """
        arguments = {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "live": True,
            "get_time": lambda: self.now,
            "get_terminal_size": lambda: os.terminal_size((columns, lines)),
            "redraw_interval": None,
            "color": False,
            **kwargs,
        }
        return TerminalUI(**arguments)

    def output(self) -> str:
        # Without newline="", a carriage return would be read as a newline
        with open(self.stdout.name, encoding="utf-8", newline="") as f:
            return f.read()

    def screen(self) -> List[str]:
        return screen(self.output())


@pytest.fixture()
def terminal(tmp_path):
    path = tmp_path / "terminal"
    with open(path, "a", encoding="utf-8") as stdout, open(path, "a", encoding="utf-8") as stderr:
        yield Terminal(stdout, stderr)


def shows(line: str, *parts: str) -> bool:
    """Return whether ``line`` contains every one of ``parts``, in any order and layout."""
    return all(part in line for part in parts)


def start_solve(ui: TerminalUI, spec: str) -> None:
    ui.on_group_started(group="default", kind=SolveKind.TOGETHER, total=1, processes=1)
    ui.on_phase(ConcretizationPhase.REUSE)
    ui.on_solve_started([Spec(spec)])


def test_status_line_shows_the_phase_and_is_erased_at_the_end(terminal):
    """Tests that the status line shows the specs of the solve, its phase and the time since
    the solve started, reuse selection included, and that nothing of it is left on the terminal
    once concretization is over.
    """
    ui = terminal.ui
    with concretization_span(ui):
        start_solve(ui, "zlib")
        terminal.now = 0.5
        ui.on_phase(ConcretizationPhase.GROUND)
        terminal.now = 1.4
        ui.render()
        assert shows(terminal.screen()[-1], "grounding", "zlib", "1.4s")

        terminal.now = 2.0
        ui.on_phase(ConcretizationPhase.SOLVE)
        assert shows(terminal.screen()[-1], "solving", "zlib", "2.0s")

    assert terminal.screen() == [""]


def test_elapsed_time_restarts_with_each_solve(terminal):
    """Tests that a group taking several solves times each of them from its own start."""
    ui = terminal.ui
    with concretization_span(ui):
        start_solve(ui, "pkg-a@1.0")
        ui.on_phase(ConcretizationPhase.SOLVE)
        terminal.now = 3.0
        ui.on_solve_finished(None, timer=Timer(), statistics=None, cached=False)

        terminal.now = 4.0
        ui.on_solve_started([Spec("pkg-a@2.0")])
        ui.on_phase(ConcretizationPhase.SETUP)
        terminal.now = 4.5
        ui.render()
        assert shows(terminal.screen()[-1], "setup", "pkg-a@2.0", "0.5s")


def test_output_is_printed_above_the_status_line(terminal):
    """Tests that output written to stdout or stderr while the status line is drawn goes above
    it, and that the streams are put back at the end.
    """
    stdout, stderr = sys.stdout, sys.stderr
    ui = terminal.ui
    with concretization_span(ui):
        start_solve(ui, "zlib")
        ui.on_phase(ConcretizationPhase.SETUP)
        print("==> Warning: first")
        print("==> Warning: second", file=sys.stderr)
        assert terminal.screen()[:2] == ["==> Warning: first", "==> Warning: second"]
        assert shows(terminal.screen()[-1], "setup", "zlib")

    assert (sys.stdout, sys.stderr) == (stdout, stderr)
    assert terminal.screen() == ["==> Warning: first", "==> Warning: second", ""]


def test_partial_line_is_printed_when_complete(terminal):
    """Tests that text with no newline is not overwritten by the status line, and is printed
    once its line is complete, or at the end of concretization.
    """
    ui = terminal.ui
    with concretization_span(ui):
        start_solve(ui, "zlib")
        sys.stdout.write("first ")
        ui.render()
        sys.stdout.write("line\nsecond")
        assert terminal.screen()[0] == "first line"

    assert terminal.screen() == ["first line", "second"]


def test_warning_count_is_reported_at_the_end(terminal):
    """Tests that the number of warnings printed during concretization is reported at its end,
    counting a warning reported twice under the same key once.
    """
    ui = terminal.ui
    with pytest.warns(UserWarning):
        with concretization_span(ui):
            ui.on_warning("mirror foo has no index", key=("no-index", "foo"))
            ui.on_warning("mirror foo has no index", key=("no-index", "foo"))
            ui.on_warning("mirror bar has no index", key=("no-index", "bar"))

    assert terminal.screen()[-2].endswith("2 warnings reported above")


def test_frontend_that_is_not_live_draws_nothing(terminal):
    """Tests that a frontend that is not live leaves the standard streams alone and does not
    draw a status line.
    """
    stdout, stderr = sys.stdout, sys.stderr
    ui = terminal.frontend(live=False)
    with concretization_span(ui):
        start_solve(ui, "zlib")
        ui.on_phase(ConcretizationPhase.SOLVE)
        ui.render()
        assert (sys.stdout, sys.stderr) == (stdout, stderr)

    assert terminal.screen() == [""]


@pytest.mark.parametrize("color", [False, True])
def test_status_line_is_truncated_to_the_terminal_width(color, terminal):
    """Tests that the status line does not wrap, since a wrapped line cannot be erased, and
    that the specs are cut to fit, so the phase and the elapsed time stay in view.
    """
    ui = terminal.frontend(columns=30, color=color)
    with concretization_span(ui):
        start_solve(ui, "a-package-with-a-long-name")
        ui.on_phase(ConcretizationPhase.GROUND)
        line = csub(terminal.screen()[-1])
        assert len(line) < 30
        assert shows(line, "grounding", "0.0s")


@pytest.mark.not_on_windows("pseudo-terminals are POSIX only")
@pytest.mark.parametrize("debug,expected", [(0, True), (1, False)])
def test_frontend_is_live_on_a_terminal_unless_debugging(debug, expected):
    """Tests that the frontend draws the status line by default on a terminal, and not in debug
    mode, whose messages would scroll it away.
    """
    master, slave = os.openpty()
    level = tty.debug_level()
    tty.set_debug(debug)
    try:
        with os.fdopen(slave, "w") as stdout:
            assert TerminalUI(stdout=stdout).live is expected
    finally:
        tty.set_debug(level)
        os.close(master)


def test_frontend_is_not_live_off_a_terminal(tmp_path):
    """Tests that output redirected to a file gets no status line."""
    with open(tmp_path / "out", "w", encoding="utf-8") as stdout:
        assert TerminalUI(stdout=stdout).live is False


@pytest.mark.parametrize("color", [False, True])
def test_status_line_is_colored_only_with_color(color, terminal):
    """Tests that the status line is colored when the frontend has color, and plain otherwise."""
    ui = terminal.frontend(color=color)
    with concretization_span(ui):
        start_solve(ui, "zlib@1.2+shared")
        ui.on_phase(ConcretizationPhase.SOLVE)
        line = terminal.screen()[-1]

    assert shows(csub(line), "solving", "zlib@1.2+shared")
    assert (csub(line) != line) is color


def test_single_group_leaves_no_line(terminal, mutable_config, mock_packages):
    """Tests that a concretization with only the default group leaves nothing on the terminal,
    as a single solve does, even when the group takes more than one round.
    """
    mutable_config.set("concretizer:unify", "when_possible")
    spack.concretize.concretize_spec_pairs(
        [(Spec("pkg-a@1.0"), None), (Spec("pkg-a@2.0"), None)], ui=terminal.ui
    )

    assert terminal.screen() == [""]


def test_groups_leave_one_line_each(tmp_path, terminal, mutable_mock_env_path, mock_packages):
    """Tests that, in an environment with more than one group, each group leaves a line with its
    name and how many specs it concretized, and the number of rounds of a group concretized
    "when possible" in more than one.
    """
    (tmp_path / "spack.yaml").write_text(
        """\
spack:
  concretizer:
    unify: true
  specs:
  - pkg-a
  - group: extra
    specs: [pkg-b]
  - group: rounds
    override:
      concretizer:
        unify: when_possible
    specs: [pkg-a@1.0, pkg-a@2.0]
"""
    )
    with ev.Environment(tmp_path) as env:
        env.concretize(ui=terminal.ui)

    *kept, last = terminal.screen()
    assert len(kept) == 3 and last == ""
    default, extra, rounds = (
        next(line for line in kept if shows(line, name)) for name in ("default", "extra", "rounds")
    )
    assert shows(default, "1 spec") and not shows(default, "rounds)")
    assert shows(extra, "1 spec") and not shows(extra, "rounds)")
    assert shows(rounds, "2 specs", "(2 rounds)")


def start_tasks(ui: TerminalUI, *specs: str) -> List[Spec]:
    """Open a group that concretizes ``specs`` separately, and start a task for each of them."""
    ui.on_group_started(
        group="default", kind=SolveKind.SEPARATELY, total=len(specs), processes=len(specs)
    )
    abstract = [Spec(x) for x in specs]
    for i, spec in enumerate(abstract):
        ui.on_phase(ConcretizationPhase.REUSE, task=i, spec=spec)
    return abstract


def finish_task(ui: TerminalUI, task: int, spec: Spec, count: int) -> None:
    ui.on_spec_concretized(spec, concrete=spec, count=count, duration=1.0, task=task)


def test_rows_show_each_running_task_under_a_counter(terminal):
    """Tests that each running task of a group that concretizes separately has a row with its
    spec, its phase and the time since it started, with the specs in one column, under a count
    of the specs done. A row goes away when its task is done, and nothing is left at the end.
    """
    ui = terminal.ui
    with concretization_span(ui):
        abstract = start_tasks(ui, "zlib", "bzip2", "xz")
        terminal.now = 1.0
        ui.on_phase(ConcretizationPhase.GROUND, task=1, spec=abstract[1])
        ui.render()
        counter, *rows = terminal.screen()
        assert counter == "[0/3 done]"
        assert shows(rows[0], "reuse", "zlib", "1.0s")
        assert shows(rows[1], "grounding", "bzip2", "1.0s")
        assert shows(rows[2], "reuse", "xz", "1.0s")
        assert len({row.index(name) for row, name in zip(rows, ("zlib", "bzip2", "xz"))}) == 1

        finish_task(ui, 1, abstract[1], count=1)
        counter, *rows = terminal.screen()
        assert counter == "[1/3 done]"
        assert [shows(row, "zlib") or shows(row, "xz") for row in rows] == [True, True]
        ui.on_group_finished()

    assert terminal.screen() == [""]


def test_rows_of_equal_specs_are_kept_apart(terminal):
    """Tests that two tasks solving equal specs have a row each, and that the one still running
    keeps its row, and its start time, when the other is done.
    """
    ui = terminal.ui
    first, second = Spec("zlib"), Spec("zlib")
    with concretization_span(ui):
        ui.on_group_started(group="default", kind=SolveKind.SEPARATELY, total=2, processes=2)
        ui.on_phase(ConcretizationPhase.REUSE, task=0, spec=first)
        terminal.now = 2.0
        ui.on_phase(ConcretizationPhase.REUSE, task=1, spec=second)
        ui.on_phase(ConcretizationPhase.SOLVE, task=0, spec=first)
        assert len([row for row in terminal.screen() if shows(row, "zlib")]) == 2

        terminal.now = 3.0
        finish_task(ui, 0, first, count=1)
        rows = [row for row in terminal.screen() if shows(row, "zlib")]
        assert len(rows) == 1 and shows(rows[0], "reuse", "1.0s")


def test_rows_that_do_not_fit_the_terminal_are_counted(terminal):
    """Tests that the rows never take the whole height of the terminal, since the lines that
    scroll off cannot be erased, and that the tasks left out are counted.
    """
    ui = terminal.frontend(lines=6)
    with concretization_span(ui):
        start_tasks(ui, *[f"pkg-{x}" for x in "abcdefgh"])
        lines = terminal.screen()
        assert len(lines) < 6
        assert lines[0] == "[0/8 done]"
        shown = [line for line in lines if shows(line, "reuse")]
        assert lines[-1] == f"{8 - len(shown)} more..."


def test_output_is_printed_above_the_rows(terminal):
    """Tests that output written while the rows are drawn goes above all of them."""
    ui = terminal.ui
    with concretization_span(ui):
        start_tasks(ui, "zlib", "bzip2")
        print("==> Warning: first")
        lines = terminal.screen()
        assert lines[:2] == ["==> Warning: first", "[0/2 done]"]
        assert shows(lines[2], "zlib") and shows(lines[3], "bzip2")


@pytest.mark.parametrize("color", [False, True])
def test_rows_show_the_times_in_one_column(color, terminal):
    """Tests that the elapsed times of all rows are right-aligned in one column, whatever the
    length of their specs and of the times themselves.
    """
    ui = terminal.frontend(color=color)
    with concretization_span(ui):
        ui.on_group_started(group="default", kind=SolveKind.SEPARATELY, total=3, processes=3)
        ui.on_phase(ConcretizationPhase.REUSE, task=0, spec=Spec("zlib"))
        terminal.now = 10.0
        ui.on_phase(ConcretizationPhase.SOLVE, task=1, spec=Spec("py-numpy@2+blas"))
        ui.on_phase(ConcretizationPhase.GROUND, task=2, spec=Spec("xz"))
        terminal.now = 12.5
        ui.render()
        _, *rows = [csub(line) for line in terminal.screen()]

    assert [row.split()[-1] for row in rows] == ["12.5s", "2.5s", "2.5s"]
    assert len({len(row) for row in rows}) == 1


def test_times_do_not_move_left_when_rows_go_away(terminal):
    """Tests that the elapsed times stay in their column when the row with the longest spec and
    the longest time is done.
    """
    ui = terminal.ui
    with concretization_span(ui):
        ui.on_group_started(group="default", kind=SolveKind.SEPARATELY, total=2, processes=2)
        long_spec = Spec("py-numpy@2+blas")
        ui.on_phase(ConcretizationPhase.SOLVE, task=0, spec=long_spec)
        terminal.now = 10.0
        ui.on_phase(ConcretizationPhase.SOLVE, task=1, spec=Spec("xz"))
        ui.render()
        before = terminal.screen()[-1]

        finish_task(ui, 0, long_spec, count=1)
        after = terminal.screen()[-1]

    assert shows(before, "xz") and shows(after, "xz")
    assert len(after) == len(before)


def start_solve_phase(ui: TerminalUI, spec: str) -> None:
    ui.on_phase(ConcretizationPhase.REUSE)
    ui.on_solve_started([Spec(spec)])
    ui.on_phase(ConcretizationPhase.SOLVE)


def test_named_group_is_shown_above_its_solve(terminal, mock_packages):
    """Tests that the solve of a group other than the default one is drawn under the name of the
    group, which from the second round of a group concretized "when possible" says the round.
    """
    ui = terminal.ui
    with concretization_span(ui):
        ui.on_group_started(group="tools", kind=SolveKind.WHEN_POSSIBLE, total=2, processes=1)
        start_solve_phase(ui, "zlib")
        header, line = terminal.screen()
        assert header == "[group: tools]" and shows(line, "solving", "zlib")

        result = Result([Spec("zlib")], repo=mock_packages)
        ui.on_solve_finished(result, timer=Timer(), statistics=None, cached=False)
        start_solve_phase(ui, "zlib")
        header, line = terminal.screen()
        assert header == "[group: tools] round 2" and shows(line, "solving", "zlib")


def test_named_group_is_shown_above_its_rows(terminal):
    """Tests that the counter of the rows of a group other than the default one starts with the
    name of the group, and that the pool is reported on the line the group keeps, not when it
    starts.
    """
    ui = terminal.ui
    with concretization_span(ui):
        ui.on_group_started(group="apps", kind=SolveKind.SEPARATELY, total=2, processes=2)
        abstract = [Spec("zlib"), Spec("bzip2")]
        for i, spec in enumerate(abstract):
            ui.on_phase(ConcretizationPhase.REUSE, task=i, spec=spec)
        counter, *_ = terminal.screen()
        assert counter == "[group: apps] [0/2 done]"

        for i, spec in enumerate(abstract):
            finish_task(ui, i, spec, count=i + 1)
        ui.on_group_finished()

    kept, last = terminal.screen()
    assert shows(kept, "apps", "2 specs", "(2 processes)") and last == ""

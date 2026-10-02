# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the status line of the terminal frontend of concretization."""

import os
import sys
from typing import List, TextIO

import pytest

import spack.concretize
import spack.environment as ev
from spack.concretize_ui import ConcretizationPhase, SolveKind, TerminalUI, concretization_span
from spack.spec import Spec
from spack.util import tty
from spack.util.timer import Timer
from spack.util.tty.color import csub


def screen(output: str) -> List[str]:
    """Return the lines a terminal shows after printing ``output``, which may contain carriage
    returns and erase-to-end-of-line sequences.
    """
    lines, column = [""], 0
    i = 0
    while i < len(output):
        if output.startswith("\033[K", i):
            lines[-1] = lines[-1][:column]
            i += 3
            continue
        char = output[i]
        if char == "\r":
            column = 0
        elif char == "\n":
            lines.append("")
            column = 0
        else:
            line = lines[-1].ljust(column)
            lines[-1] = line[:column] + char + line[column + 1 :]
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

    def frontend(self, *, columns: int = 80, **kwargs) -> TerminalUI:
        """Return a live frontend drawing on this terminal, with no redraw thread and no color
        unless ``kwargs`` say otherwise.
        """
        arguments = {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "live": True,
            "get_time": lambda: self.now,
            "get_terminal_size": lambda: os.terminal_size((columns, 24)),
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

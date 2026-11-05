# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the TerminalUI terminal UI in installer.ui"""

import functools
import io
import os
from typing import List, Optional, Tuple, cast

import pytest

import spack.installer.ui as inst
from spack.installer.base import StdinReader
from spack.installer.streaming.ui import LOG_HISTORY_SIZE
from spack.installer.streaming.ui import StreamingTerminalUI as TerminalUI


def _fd_reader(fd: int) -> StdinReader:
    """StdinReader reading from a raw fd, as PosixTerminalState's stdin_reader does."""
    return StdinReader(functools.partial(os.read, fd, 1024))


class SimpleTextIOWrapper(io.TextIOWrapper):
    """TextIOWrapper around a BytesIO buffer for testing of stdout behavior"""

    def __init__(self, tty: bool) -> None:
        self._buffer = io.BytesIO()
        self._tty = tty
        super().__init__(self._buffer, encoding="utf-8", newline="", line_buffering=True)

    def isatty(self) -> bool:
        return self._tty

    def getvalue(self) -> str:
        self.flush()
        return self._buffer.getvalue().decode("utf-8")

    def clear(self):
        self.flush()
        self._buffer.truncate(0)
        self._buffer.seek(0)


def create_tui(
    is_tty: bool = True,
    terminal_cols: int = 80,
    terminal_rows: int = 24,
    total: int = 0,
    verbose: bool = False,
    filter_padding: bool = False,
    color: Optional[bool] = None,
    show_log_on_error: bool = False,
) -> Tuple[TerminalUI, List[float], SimpleTextIOWrapper]:
    """Helper function to create TerminalUI with mocked dependencies"""
    fake_stdout = SimpleTextIOWrapper(tty=is_tty)
    # Easy way to set the current time in tests before running UI updates
    time_values = [0.0]

    def mock_get_time():
        return time_values[-1]

    def mock_get_terminal_size():
        return os.terminal_size((terminal_cols, terminal_rows))

    tui = TerminalUI(
        total=total,
        stdout=fake_stdout,
        stderr=SimpleTextIOWrapper(tty=False),
        get_terminal_size=mock_get_terminal_size,
        get_time=mock_get_time,
        is_tty=is_tty,
        verbose=verbose,
        filter_padding=filter_padding,
        color=color,
        show_log_on_error=show_log_on_error,
    )

    return tui, time_values, fake_stdout


def get_stderr(tui: TerminalUI) -> SimpleTextIOWrapper:
    """The fake stderr that create_tui installed on the UI."""
    return cast(SimpleTextIOWrapper, tui.stderr)


def on_build_added(
    tui: TerminalUI,
    build_id: str,
    *,
    name: Optional[str] = None,
    version: str = "1.0",
    external: bool = False,
    prefix: Optional[str] = None,
    explicit: bool = True,
    log_path: Optional[str] = None,
) -> None:
    """Add a build with plain data, defaulting name and prefix from the build id."""
    name = name if name is not None else build_id
    tui.on_build_added(
        inst.BuildInfo(
            build_id,
            name=name,
            version=version,
            external=external,
            prefix=prefix if prefix is not None else f"/fake/prefix/{name}",
            explicit=explicit,
            log_path=log_path,
        )
    )


def add_mock_builds(tui: TerminalUI, count: int) -> List[str]:
    """Helper function to add builds to a TerminalUI instance. Returns the build ids."""
    build_ids = [f"pkg{i}" for i in range(count)]
    for i, build_id in enumerate(build_ids):
        on_build_added(tui, build_id, version=f"{i}.0")
    # The real installer event loop drains UI commands after handling each callback. Tests do
    # not run that event loop, so emulate the drain to keep setup commands out of assertions.
    tui.commands.clear()
    return build_ids


class TestLogFollowing:
    def test_verbose_tty_continues_partial_log_line(self):
        tui, _, fake_stdout = create_tui(total=1, verbose=True)
        on_build_added(tui, "pkg0")
        tui.render()
        fake_stdout.clear()

        tui.on_log_output("pkg0", b"checking for boost...")
        assert fake_stdout.getvalue() == ""
        tui.on_log_output("pkg0", b"yes\n")

        assert "checking for boost...yes\n" in fake_stdout.getvalue()
        assert "Progress:" in fake_stdout.getvalue()

    def test_non_verbose_tty_forwards_every_build(self):
        tui, _, _ = create_tui(is_tty=True, verbose=False)
        on_build_added(tui, "first")
        on_build_added(tui, "second")

        assert tui.tracked_build_id == ""
        assert tui.commands == [inst.SetEcho("first", True), inst.SetEcho("second", True)]

    @pytest.mark.parametrize(
        "is_tty,headless,overview,expected",
        [
            (True, False, True, inst.SPINNER_INTERVAL),
            (True, True, True, None),
            (True, False, False, None),
            (False, False, True, None),
        ],
    )
    def test_refresh_interval_modes(self, is_tty, headless, overview, expected):
        tui, _, _ = create_tui(is_tty=is_tty)
        tui.headless = headless
        tui.overview_mode = overview

        assert tui.refresh_interval() == expected

    @pytest.mark.parametrize("is_tty,headless", [(True, True), (False, False), (False, True)])
    def test_log_history_redraw_suppressed(self, is_tty, headless):
        tui, _, fake_stdout = create_tui(total=1, is_tty=is_tty)
        [build_id] = add_mock_builds(tui, 1)
        tui.headless = headless
        tui.dirty = False
        tui.active_area_rows = 3

        tui._redraw_overview_with_log_history(build_id, b"hidden log\n")

        assert fake_stdout.getvalue() == ""
        assert tui.active_area_rows == 3
        assert tui.dirty is False

    @pytest.mark.parametrize("is_tty", [True, False])
    @pytest.mark.parametrize("overview_mode", [True, False])
    def test_navigate_to_failed_build_without_log_file(self, is_tty, overview_mode):
        tui, _, fake_stdout = create_tui(total=1, is_tty=is_tty, color=False)
        [build_id] = add_mock_builds(tui, 1)
        tui.on_state_changed(build_id, "failed")
        tui.overview_mode = overview_mode
        fake_stdout.clear()

        tui.next()

        output = fake_stdout.getvalue()
        assert "==> Log summary of pkg0@0.0\n" in output
        assert "Full log:" not in output
        assert tui.tracked_build_id == build_id
        assert tui.log_streaming is False
        assert tui.log_ends_with_newline is True
        assert tui.commands == []

    @pytest.mark.parametrize("render_first", [True, False])
    def test_verbose_tty_streams_logs_above_overview(self, render_first):
        """Verbose TTY mode streams tracked logs above the overview display."""
        tui, time_values, fake_stdout = create_tui(total=1, verbose=True)
        on_build_added(tui, "pkg0")
        tui.on_jobs_changed(16, 16)

        assert tui.overview_mode is True
        assert tui.tracked_build_id == "pkg0"

        if render_first:
            tui.render()
        fake_stdout.clear()
        tui.on_log_output("pkg0", b"-- Configuring done\n")
        time_values.append(1.0)
        tui.on_log_output("pkg0", b"-- Generating done\n")

        output = fake_stdout.getvalue()
        assert "-- Configuring done\n" in output
        assert "-- Generating done\n" in output
        assert "Progress:" in output
        assert "pkg0" in output
        assert "@1.0" in output
        assert "starting" in output
        assert output.index("-- Configuring done") < output.rindex("Progress:")

    def test_verbose_tty_toggle_off_clears_streamed_log(self):
        """Turning streaming off clears the screen and restores the overview position."""
        tui, _, fake_stdout = create_tui(total=1, verbose=True)
        on_build_added(tui, "pkg0")
        tui.render()
        tui.on_log_output("pkg0", b"-- Configuring done\n")
        fake_stdout.clear()

        tui.toggle()

        output = fake_stdout.getvalue()
        assert output.startswith("\0337\033[2J\0338\033[2A\r")
        assert "Progress:" in output
        assert "-- Configuring done" not in output

        fake_stdout.clear()
        tui.toggle()

        output = fake_stdout.getvalue()
        assert output.startswith("\0337\033[2J\033[3A\r-- Configuring done\n\0338\033[2A\r")
        assert "Progress:" in output

    def test_verbose_tty_switching_builds_shows_cached_log_tail(self):
        """Switching streamed builds shows the saved recent log tail for the new build."""
        tui, _, fake_stdout = create_tui(total=2, verbose=True)
        build_a, build_b = add_mock_builds(tui, 2)
        tui.render()
        tui.on_log_output(build_a, b"a: configure\n")
        for index in range(LOG_HISTORY_SIZE + 1):
            tui.on_log_output(build_b, f"b: line {index}\n".encode())
        fake_stdout.clear()

        tui.next(1)

        output = fake_stdout.getvalue()
        assert "b: line 0\n" not in output
        for index in range(1, LOG_HISTORY_SIZE + 1):
            assert f"b: line {index}\n" in output
        assert "a: configure\n" not in output
        assert "Progress:" in output

    @pytest.mark.not_on_windows("Padding functionality unsupported on Windows")
    def test_cached_log_tail_filters_padding(self):
        """Switching builds does not replay path-padding placeholders."""
        tui, _, fake_stdout = create_tui(total=2, verbose=True, filter_padding=True)
        _, build_b = add_mock_builds(tui, 2)
        tui.render()
        tui.on_log_output(
            build_b,
            b"--with-foo=/base/__spack_path_placeholder__/__spack_path_placeholder__/bin\n",
        )
        fake_stdout.clear()

        tui.next(1)

        output = fake_stdout.getvalue()
        assert "__spack_path_placeholder__" not in output
        assert "--with-foo=/base/[padded-to-59-chars]/bin" in output

    def test_unselected_overview_logs_are_cached_without_output(self):
        """Unselected overview logs are cached without being written immediately."""
        tui, _, fake_stdout = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Stay in overview mode
        assert tui.overview_mode is True

        # Try to print logs
        log_data = b"Should not be printed\n"
        tui.on_log_output(build_id, log_data)

        # Nothing should be printed
        assert fake_stdout.getvalue() == ""

    def test_unselected_streamed_logs_are_cached_without_output(self):
        """Logs from an unselected build are cached without being written immediately."""
        tui, _, fake_stdout = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Switch to log-following mode for the first build
        tui.overview_mode = False
        tui.tracked_build_id = build_ids[0]

        # Try to print logs from the second build (not tracked)
        log_data = b"Logs from pkg2\n"
        tui.on_log_output(build_ids[1], log_data)

        # Nothing should be printed since we're tracking pkg0, not pkg1
        assert fake_stdout.getvalue() == ""

    @pytest.mark.parametrize("is_tty", [True, False])
    @pytest.mark.parametrize("overview_mode", [True, False])
    @pytest.mark.parametrize("already_tracked", [True, False])
    def test_toggle_to_failed_build_keeps_summary_after_redraw(
        self, tmp_path, is_tty, overview_mode, already_tracked
    ):
        """Enabling log view redraws a failed build's summary above the overview."""
        tui, _, fake_stdout = create_tui(total=1, is_tty=is_tty)
        [build_id] = add_mock_builds(tui, 1)
        log_file = tmp_path / "pkg0.log"
        log_file.write_text("error: something went wrong\n")
        tui.builds[build_id].log_path = str(log_file)
        tui.on_state_changed(build_id, "failed")
        tui.render()
        tui.overview_mode = overview_mode
        if already_tracked:
            tui.tracked_build_id = build_id
        fake_stdout.clear()

        tui.toggle()

        output = fake_stdout.getvalue()
        after_clear = output.rsplit("\033[2J", 1)[-1]
        assert "Log summary of pkg0" in after_clear
        assert "> error: something went wrong" in after_clear
        assert f"Full log: {log_file}" in after_clear
        assert after_clear.count("Log summary of pkg0") == 1
        assert ("Progress:" in after_clear) == (is_tty and overview_mode)
        assert tui.log_streaming is False
        assert tui.commands == []


class TestNavigationIntegration:
    @pytest.mark.parametrize("is_tty", [True, False])
    @pytest.mark.parametrize("log_streaming", [True, False])
    def test_next_controls_log_forwarding(self, is_tty, log_streaming):
        tui, _, fake_stdout = create_tui(total=2, is_tty=is_tty, verbose=log_streaming)
        first_id, next_id = add_mock_builds(tui, 2)
        if not log_streaming:
            tui.next()

        tui.next()

        expected_commands = []
        if log_streaming:
            if not is_tty:
                expected_commands.append(inst.SetEcho(first_id, False))
            expected_commands.append(inst.SetEcho(next_id, True))
        assert tui.commands == expected_commands
        assert tui.tracked_build_id == next_id
        assert tui.overview_mode is True
        assert bool(fake_stdout.getvalue()) == (is_tty and log_streaming)

    def test_next_selects_tracked_build_in_overview(self):
        """Test that next() selects a tracked build without leaving overview mode."""
        tui, _, fake_stdout = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Start in overview mode
        assert tui.overview_mode is True
        assert tui.tracked_build_id == ""

        # Call next() to start following first build
        tui.next()

        # Should have selected the first build while staying in overview mode
        assert tui.overview_mode is True
        assert tui.log_streaming is False
        assert tui.tracked_build_id == build_ids[0]
        assert tui.commands == []
        assert fake_stdout.getvalue() == ""

    def test_next_cycles_through_builds(self):
        """Test that next() cycles through multiple builds"""
        tui, _, fake_stdout = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Start following first build
        tui.next()
        assert tui.tracked_build_id == build_ids[0]

        fake_stdout.clear()

        # Navigate to next
        tui.next(1)
        assert tui.tracked_build_id == build_ids[1]
        assert fake_stdout.getvalue() == ""
        # TTY overview mode already keeps build logs enabled so progress parsing still works.
        assert tui.commands == []

        fake_stdout.clear()

        # Navigate to next (third build)
        tui.next(1)
        assert tui.tracked_build_id == build_ids[2]
        assert fake_stdout.getvalue() == ""

        fake_stdout.clear()

        # Navigate to next (should wrap to first)
        tui.next(1)
        assert tui.tracked_build_id == build_ids[0]
        assert fake_stdout.getvalue() == ""


class TestToggle:
    @pytest.mark.parametrize("count", [0, 1])
    def test_toggle_without_unfinished_build_does_not_start_streaming(self, count):
        tui, _, _ = create_tui(total=count)
        for build_id in add_mock_builds(tui, count):
            tui.on_state_changed(build_id, "finished")

        tui.toggle()

        assert tui.tracked_build_id == ""
        assert tui.log_streaming is False
        assert tui.commands == []

    def test_non_tty_toggle_enables_and_disables_log_forwarding(self):
        tui, _, fake_stdout = create_tui(total=1, is_tty=False)
        [build_id] = add_mock_builds(tui, 1)

        tui.toggle()

        assert tui.commands == [inst.SetEcho(build_id, True)]
        assert tui.log_streaming is True
        tui.commands.clear()
        tui.on_log_output(build_id, b"partial log")
        assert fake_stdout.getvalue() == "partial log"

        tui.toggle()

        assert tui.commands == [inst.SetEcho(build_id, False)]
        assert tui.log_streaming is False
        assert tui.tracked_build_id == build_id
        assert tui.log_ends_with_newline is True
        assert fake_stdout.getvalue() == "partial log\n"

    @pytest.mark.parametrize("is_tty", [True, False])
    def test_toggle_stops_streaming_without_selected_build(self, is_tty):
        tui, _, _ = create_tui(is_tty=is_tty, verbose=True)

        tui.toggle()

        assert tui.log_streaming is False
        assert tui.tracked_build_id == ""
        assert tui.commands == []

    def test_toggle_from_overview_starts_streaming(self):
        """Test that toggle() from overview mode starts streaming the tracked build."""
        tui, _, fake_stdout = create_tui(total=2)
        add_mock_builds(tui, 2)

        # Start in overview mode
        assert tui.overview_mode is True

        # Toggle should call next()
        tui.toggle()

        # Log streaming now keeps the overview visible.
        assert tui.overview_mode is True
        assert tui.log_streaming is True
        assert tui.tracked_build_id != ""
        assert "Progress:" in fake_stdout.getvalue()

    def test_toggle_from_streaming_stops_streaming(self):
        """Test that toggle() stops log streaming but keeps the tracked build selected."""
        tui, _, _ = create_tui(total=2)
        add_mock_builds(tui, 2)

        # Switch to log-following mode first
        tui.toggle()
        assert tui.overview_mode is True
        assert tui.log_streaming is True
        tracked_id = tui.tracked_build_id
        assert tracked_id != ""

        # Set some search state to verify cleanup
        tui.search_term = "test"
        tui.search_mode = True
        tui.active_area_rows = 5

        # Toggle back to overview
        tui.toggle()

        # Should be back in overview mode with cleaned state
        assert tui.overview_mode is True
        assert tui.log_streaming is False
        assert tui.tracked_build_id == tracked_id
        assert tui.search_term == ""
        assert tui.search_mode is False
        assert tui.dirty is False
        # TTY overview mode keeps build logs enabled so progress parsing still works later.
        assert inst.SetEcho(tracked_id, False) not in tui.commands

    @pytest.mark.parametrize("is_tty", [True, False])
    @pytest.mark.parametrize("char", ["q", "\x1b"])
    def test_legacy_log_view_exit_restores_overview(self, is_tty, char):
        tui, _, fake_stdout = create_tui(total=1, is_tty=is_tty)
        [build_id] = add_mock_builds(tui, 1)
        tui.tracked_build_id = build_id
        tui.overview_mode = False
        tui.log_ends_with_newline = False
        tui.active_area_rows = 5
        tui.search_mode = True
        tui.search_term = "pkg"

        tui.on_input(char)

        assert tui.overview_mode is True
        assert tui.tracked_build_id == ""
        assert tui.log_ends_with_newline is True
        assert tui.active_area_rows == 0
        assert tui.search_mode is False
        assert tui.search_term == ""
        assert fake_stdout.getvalue() == "\n"
        assert tui.commands == ([] if is_tty else [inst.SetEcho(build_id, False)])

    def test_legacy_overview_toggle_selects_next_build(self):
        tui, _, _ = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)

        tui._toggle_overview()

        assert tui.overview_mode is True
        assert tui.tracked_build_id == build_id
        assert tui.log_streaming is False

    def test_tty_logs_remain_enabled_after_returning_to_overview(self):
        """Returning from full-screen log view keeps TTY log delivery enabled."""
        tui, _, _ = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)

        tui.toggle()
        tui.toggle()

        assert tui.overview_mode is True
        assert inst.SetEcho(build_id, False) not in tui.commands

    def test_on_state_changed_finished_continues_streaming_next_build(self):
        """Finishing a streamed build follows the next unfinished build."""
        tui, _, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Start tracking first build
        tui.toggle()
        assert tui.overview_mode is True
        assert tui.log_streaming is True
        assert tui.tracked_build_id == build_ids[0]

        # Mark the tracked build as finished
        tui.on_state_changed(build_ids[0], "finished")

        # Successful builds keep streaming active and advance the tracked build.
        assert tui.overview_mode is True
        assert tui.log_streaming is True
        assert tui.tracked_build_id == build_ids[1]

    def test_on_state_changed_failed_stops_streaming(self):
        tui, _, _ = create_tui(total=2, verbose=True)
        build_id, _ = add_mock_builds(tui, 2)

        tui.on_state_changed(build_id, "failed")

        assert tui.log_streaming is False
        assert tui.tracked_build_id == ""
        assert tui.commands == []

    def test_streaming_resumes_when_next_build_is_added(self):
        """A later build is tracked when streaming outlives the previous build wave."""
        tui, _, _ = create_tui(total=2)
        [build_id] = add_mock_builds(tui, 1)

        tui.toggle()
        tui.on_state_changed(build_id, "finished")

        assert tui.log_streaming is True
        assert tui.tracked_build_id == ""

        on_build_added(tui, "next")

        assert tui.log_streaming is True
        assert tui.tracked_build_id == "next"

    def test_partial_line_newline_on_toggle_and_next(self):
        """Mode transitions do not display incomplete fragments from another build."""
        tui, _, fake_stdout = create_tui(total=2)
        build_a, build_b = add_mock_builds(tui, 2)

        # Toggle log streaming on and off while receiving logs that may or may not end with
        # newlines.
        tui.toggle()
        tui.on_log_output(build_a, b"checking for foo...")
        tui.toggle()
        tui.toggle()
        tui.on_log_output(build_a, b"checking for bar... yes\n")
        tui.next(1)
        tui.on_log_output(build_b, b"checking for baz...")
        tui.next(-1)

        written = fake_stdout.getvalue()

        # There shouldn't be any double newlines:
        assert "\n\n" not in written

        # All partial and newline-terminated logs should be present with appropriate newlines:
        assert "checking for foo...\n" in written
        assert "checking for bar... yes\n" in written
        assert "checking for baz..." not in written


class TestSearchFilteringIntegration:
    def test_search_input_enter_navigates_to_next(self):
        """Test that pressing enter in search mode navigates to next match"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Enter search mode
        tui.enter_search()
        for character in "pkg":
            tui.search_input(character)

        # Press enter (should navigate to first match)
        tui.search_input("\r")

        # Should have started following first matching build
        assert tui.overview_mode is True
        assert tui.tracked_build_id == build_ids[0]


class TestHandleInput:
    def test_toggle_and_navigation_keys(self):
        """'v' toggles log following, 'n'/'p' navigate, 'q' returns to overview."""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        tui.on_input("v")
        # Log streaming now keeps the overview visible.
        assert tui.overview_mode is True
        assert tui.log_streaming is True
        assert tui.tracked_build_id == build_ids[0]

        tui.on_input("n")
        assert tui.tracked_build_id == build_ids[1]

        tui.on_input("p")
        assert tui.tracked_build_id == build_ids[0]

        tui.on_input("q")
        # q unconditionally stops streaming without clearing the selection.
        assert tui.overview_mode is True
        assert tui.log_streaming is False
        assert tui.tracked_build_id == build_ids[0]


class TestEdgeCases:
    def test_finalize_keeps_overview_mode(self):
        """render(finalize=True) keeps the overview mode even while logs are streaming."""
        tui, _, _ = create_tui(total=2)
        add_mock_builds(tui, 2)
        tui.toggle()
        assert tui.overview_mode is True
        assert tui.log_streaming is True

        tui.render(finalize=True)
        assert tui.overview_mode is True


class TestTerminalUIVerbose:
    def test_verbose_tty_tracks_first_build(self):
        """Verbose mode selects the first TTY build while keeping the overview visible."""
        tui, _, _ = create_tui(is_tty=True, verbose=True, total=4)

        on_build_added(tui, "trivial-install-test-package")
        assert tui.overview_mode is True
        assert tui.tracked_build_id == "trivial-install-test-package"
        assert tui.commands == [inst.SetEcho("trivial-install-test-package", True)]


class TestTargetJobs:
    def test_header_shows_tracked_package_name(self):
        """The overview header shows the currently tracked package in gray."""
        tui, _, fake_stdout = create_tui(total=1, color=True)
        [build_id] = add_mock_builds(tui, 1)
        tui.tracked_build_id = build_id
        tui.render()
        output = fake_stdout.getvalue()
        assert "next/prev" in output
        assert f"\033[0;90m({build_id})\033[0m" in output


class TestLineRendering:
    def test_persisted_finished_line_keeps_prefix_in_narrow_terminal(self):
        """A persisted completed build always shows its install prefix."""
        tui, fake_time, fake_stdout = create_tui(total=1, terminal_cols=30, color=False)
        on_build_added(tui, "pkg", prefix="/quite/long/prefix/path")
        tui.on_state_changed("pkg", "finished")
        fake_time.append(inst.CLEANUP_TIMEOUT + 0.1)

        tui.render()

        lines = [line for line in fake_stdout.getvalue().splitlines() if "pkg@1.0" in line]
        assert lines
        assert "/quite/long/prefix/path" in fake_stdout.getvalue()

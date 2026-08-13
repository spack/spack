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
import spack.util.tty.color
from spack.installer.base import StdinReader
from spack.installer.ui import TerminalUI


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


class TestBasicStateManagement:
    """Test basic state management operations"""

    def test_on_resize(self):
        """Test that on_resize sets terminal_size_changed and render() fetches lazily"""
        sizes = [os.terminal_size((80, 24))]
        fake_stdout = SimpleTextIOWrapper(tty=True)
        tui = TerminalUI(
            total=0, stdout=fake_stdout, get_terminal_size=lambda: sizes[-1], is_tty=True
        )
        # terminal_size_changed is True from __init__; terminal_size is placeholder
        assert tui.terminal_size_changed is True

        # After on_resize the flag stays set and dirty is True
        sizes.append(os.terminal_size((120, 40)))
        tui.on_resize()
        assert tui.terminal_size_changed is True
        assert tui.dirty is True

        # The actual size is fetched lazily on the first render()
        tui.render()
        assert tui.terminal_size == os.terminal_size((120, 40))
        assert tui.terminal_size_changed is False

    def test_on_build_added(self):
        """Test that on_build_added adds builds correctly"""
        tui, _, _ = create_tui(total=2)

        on_build_added(tui, "pkg1", explicit=True)
        assert len(tui.builds) == 1
        assert "pkg1" in tui.builds
        assert tui.builds["pkg1"].name == "pkg1"
        assert tui.builds["pkg1"].explicit is True
        assert tui.dirty is True

        on_build_added(tui, "pkg2", version="2.0", explicit=False)
        assert len(tui.builds) == 2
        assert "pkg2" in tui.builds
        assert tui.builds["pkg2"].explicit is False

    def test_on_state_changed_transitions(self):
        """Test that on_state_changed transitions states properly"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Update to 'building' state
        tui.on_state_changed(build_id, "building")
        assert tui.builds[build_id].state == "building"
        assert tui.builds[build_id].progress is None
        assert tui.completed == 0

        # Update to 'finished' state
        tui.on_state_changed(build_id, "finished")
        assert tui.builds[build_id].state == "finished"
        assert tui.completed == 1
        assert tui.builds[build_id].finished_time == fake_time[0] + inst.CLEANUP_TIMEOUT

    def test_on_state_changed_failed(self):
        """Test that failed state increments completed counter"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        tui.on_state_changed(build_id, "failed")
        assert tui.builds[build_id].state == "failed"
        assert tui.completed == 1
        assert tui.builds[build_id].finished_time == fake_time[0] + inst.CLEANUP_TIMEOUT

    def test_on_build_removed(self):
        """Test that on_build_removed removes the build from the display."""
        tui, _, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        tui.dirty = False
        tui.on_build_removed(build_ids[0])
        assert build_ids[0] not in tui.builds
        assert len(tui.builds) == 1
        assert tui.dirty is True

    def test_on_build_removed_resets_tracked(self):
        """Test that removing the tracked build resets tracking to overview mode."""
        tui, _, _ = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)

        tui.tracked_build_id = build_id
        tui.overview_mode = False
        tui.on_build_removed(build_id)
        assert tui.tracked_build_id == ""
        assert tui.overview_mode is True

    def test_failed_state_parses_log_summary(self, tmp_path):
        """A build transitioning to "failed" parses the build log and stores the summary."""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Create a fake log file with an error
        log_file = tmp_path / "build.log"
        log_file.write_text("error: something went wrong\n")

        tui.builds[build_id].log_path = str(log_file)
        tui.on_state_changed(build_id, "failed")
        assert tui.builds[build_id].log_summary is not None
        assert "error" in tui.builds[build_id].log_summary.lower()

    def test_failed_state_no_log_path(self):
        """No summary is stored for a failed build without a log path."""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        tui.on_state_changed(build_id, "failed")
        assert tui.builds[build_id].log_summary is None

    def test_failed_state_missing_log_file(self, tmp_path):
        """No summary is stored for a failed build whose log file doesn't exist."""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        tui.builds[build_id].log_path = str(tmp_path / "nonexistent.log")
        tui.on_state_changed(build_id, "failed")
        assert tui.builds[build_id].log_summary is None

    def test_print_failure_summaries(self, tmp_path):
        """on_finished writes the stored summaries to stderr, skipping builds without a summary
        and unknown build ids."""
        tui, _, _ = create_tui()
        build_ids = add_mock_builds(tui, 2)

        log_file = tmp_path / "build.log"
        log_file.write_text("error: nope\n")
        tui.builds[build_ids[0]].log_path = str(log_file)
        tui.on_state_changed(build_ids[0], "failed")

        tui.on_finished([*build_ids, "unknown"])
        assert get_stderr(tui).getvalue() == "-- lines 1 to 1 --\n> error: nope\n"

    def test_show_log_on_error_writes_whole_log(self, tmp_path):
        """With show_log_on_error every line of the log is written."""
        lines = [f"line {i}" for i in range(1, 101)]
        lines[49] = "error: something went wrong"
        log_file = tmp_path / "build.log"
        log_file.write_text("\n".join(lines) + "\n")

        tui, _, _ = create_tui(show_log_on_error=True)
        [build_id] = add_mock_builds(tui, 1)
        tui.builds[build_id].log_path = str(log_file)
        tui.on_state_changed(build_id, "failed")
        tui.on_finished([build_id])

        err = get_stderr(tui).getvalue()
        assert "-- lines 1 to 100 --" in err
        assert "  line 1\n" in err and "  line 100\n" in err
        assert "> error: something went wrong\n" in err

    def test_without_show_log_on_error_the_log_is_windowed(self, tmp_path):
        """Without the flag, lines far away from the error and the tail are dropped."""
        lines = [f"line {i}" for i in range(1, 101)]
        lines[49] = "error: something went wrong"
        log_file = tmp_path / "build.log"
        log_file.write_text("\n".join(lines) + "\n")

        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)
        tui.builds[build_id].log_path = str(log_file)
        tui.on_state_changed(build_id, "failed")
        tui.on_finished([build_id])

        err = get_stderr(tui).getvalue()
        assert "> error: something went wrong\n" in err
        assert "  line 1\n" not in err  # far from the error and outside the tail
        assert "  line 100\n" in err  # in the tail

    def test_show_log_on_error_without_any_match(self, tmp_path):
        """With show_log_on_error the log is written even when nothing matched."""
        log_file = tmp_path / "build.log"
        log_file.write_text("".join(f"line {i}\n" for i in range(1, 101)))

        tui, _, _ = create_tui(show_log_on_error=True)
        [build_id] = add_mock_builds(tui, 1)
        tui.builds[build_id].log_path = str(log_file)
        tui.on_state_changed(build_id, "failed")
        tui.on_finished([build_id])

        err = get_stderr(tui).getvalue()
        assert "  line 1\n" in err and "  line 100\n" in err

    def test_on_progress(self):
        """on_progress stores fetching percentages and marks only changed values dirty."""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Update progress
        tui.on_progress(build_id, 50, 100)
        assert tui.builds[build_id].progress == inst.BuildProgress("50%", "fetching")
        assert tui.dirty is True

        # Same percentage shouldn't mark dirty again
        tui.dirty = False
        tui.on_progress(build_id, 50, 100)
        assert tui.dirty is False

        # Different percentage should mark dirty
        tui.on_progress(build_id, 75, 100)
        assert tui.builds[build_id].progress == inst.BuildProgress("75%", "fetching")
        assert tui.dirty is True

    def test_completion_counter(self):
        """Test that completion counter increments correctly"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        assert tui.completed == 0

        tui.on_state_changed(build_ids[0], "finished")
        assert tui.completed == 1

        tui.on_state_changed(build_ids[1], "failed")
        assert tui.completed == 2

        tui.on_state_changed(build_ids[2], "finished")
        assert tui.completed == 3


class TestOutputRendering:
    """Test output rendering for TTY and non-TTY modes"""

    def test_non_tty_output(self):
        """Test that non-TTY mode prints simple state changes"""
        tui, _, fake_stdout = create_tui(is_tty=False)

        on_build_added(tui, "mypackage")
        tui.on_state_changed("mypackage", "finished")

        output = fake_stdout.getvalue()
        assert "[+]" in output
        assert "mypackage" in output
        assert "1.0" in output
        assert "/fake/prefix/mypackage" in output  # prefix is shown for finished builds
        # Non-TTY output should not contain ANSI escape codes
        assert "\033[" not in output

    def test_tty_output_contains_ansi(self):
        """Test that TTY mode produces ANSI codes"""
        tui, _, fake_stdout = create_tui()
        add_mock_builds(tui, 1)

        # Call update to render
        tui.render()

        output = fake_stdout.getvalue()
        # Should contain ANSI escape sequences
        assert "\033[" in output
        # Should contain progress header
        assert "Progress:" in output

    def test_no_output_when_not_dirty(self):
        """Test that render() skips rendering when not dirty"""
        tui, _, fake_stdout = create_tui()
        add_mock_builds(tui, 1)
        tui.render()

        # Clear stdout and mark not dirty
        fake_stdout.clear()
        tui.dirty = False

        # Update should not produce output
        tui.render()
        assert fake_stdout.getvalue() == ""

    def test_render_throttling(self):
        """Test that render() throttles redraws"""
        tui, fake_time, fake_stdout = create_tui()
        add_mock_builds(tui, 1)

        # First update at time 0
        fake_time[0] = 0.0
        tui.render()
        first_output = fake_stdout.getvalue()
        assert first_output != ""

        # Mark dirty and try to update immediately
        fake_stdout.clear()
        tui.dirty = True
        fake_time[0] = 0.01  # Very small time advance

        # Should be throttled (next_update not reached)
        tui.render()
        assert fake_stdout.getvalue() == ""

        # Advance time past throttle and try again
        fake_time[0] = 1.0
        tui.render()
        assert fake_stdout.getvalue() != ""

    def test_cursor_movement_vs_newlines(self):
        """Test that finished builds get newlines, active builds get cursor movements"""
        tui, fake_time, fake_stdout = create_tui(total=5)
        build_ids = add_mock_builds(tui, 3)

        # First update renders 3 active builds
        fake_time[0] = 0.0
        tui.render()
        output1 = fake_stdout.getvalue()

        # Count newlines (\n) and cursor movements (\033[1B\r = move down 1 line)
        newlines1 = output1.count("\n")
        cursor_moves1 = output1.count("\033[1B\r")

        # Initially all lines should be newlines (nothing in history yet)
        assert newlines1 > 0
        assert cursor_moves1 == 0

        # Now finish 2 builds and add 2 more
        fake_stdout.clear()
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.1
        tui.on_state_changed(build_ids[0], "finished")
        tui.on_state_changed(build_ids[1], "finished")

        on_build_added(tui, "pkg3", version="3.0")
        on_build_added(tui, "pkg4", version="4.0")

        # Second update: finished builds persist (newlines), active area updates (cursor moves)
        tui.render()
        output2 = fake_stdout.getvalue()

        newlines2 = output2.count("\n")
        cursor_moves2 = output2.count("\033[1B\r")

        # Should have newlines for the 2 finished builds persisted to history
        # and cursor movements for the active area (header + 3 active builds)
        assert newlines2 > 0, "Should have newlines for finished builds"
        assert cursor_moves2 > 0, "Should have cursor movements for active area"

        # Finished builds should be printed with newlines
        assert "pkg0" in output2
        assert "pkg1" in output2


class TestTimeBasedBehavior:
    """Test time-based behaviors like spinner and cleanup"""

    def test_spinner_updates(self):
        """Test that spinner advances over time"""
        tui, fake_time, _ = create_tui()
        add_mock_builds(tui, 1)

        # Initial spinner index
        initial_index = tui.spinner_index

        # Advance time past spinner interval
        fake_time[0] = inst.SPINNER_INTERVAL + 0.01
        tui.render()

        # Spinner should have advanced
        assert tui.spinner_index == (initial_index + 1) % len(inst.SPINNER_CHARS)

    def test_no_redraw_when_nothing_changed(self):
        """render() renders nothing when the display is clean and the spinner is not due"""
        tui, fake_time, fake_stdout = create_tui()
        add_mock_builds(tui, 1)
        tui.render()
        fake_stdout.clear()

        # Past the redraw throttle but before the next spinner advance, with no state changes
        fake_time[0] = inst.SPINNER_INTERVAL * 0.6
        tui.render()
        assert fake_stdout.getvalue() == ""

    def test_finished_package_cleanup(self):
        """Test that finished packages are cleaned up after timeout"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Mark as finished
        fake_time[0] = 0.0
        tui.on_state_changed(build_id, "finished")

        # Build should still be in active builds
        assert build_id in tui.builds
        assert len(tui.finished_builds) == 0

        # Advance time past cleanup timeout
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        tui.render()

        # Build should now be moved to finished_builds and removed from active
        assert build_id not in tui.builds
        # Note: finished_builds is cleared after rendering, so check it happened via side effects
        assert tui.dirty or build_id not in tui.builds

    def test_failed_packages_not_cleaned_up(self):
        """Test that failed packages stay in active builds"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Mark as failed
        fake_time[0] = 0.0
        tui.on_state_changed(build_id, "failed")

        # Advance time past cleanup timeout
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        tui.render()

        # Failed build should remain in active builds
        assert build_id in tui.builds


class TestSearchAndFilter:
    """Test search mode and filtering"""

    def test_enter_search_mode(self):
        """Test that enter_search enables search mode"""
        tui, _, _ = create_tui()
        assert tui.search_mode is False

        tui.enter_search()
        assert tui.search_mode is True
        assert tui.dirty is True

    def test_search_input_printable(self):
        """Test that printable characters are added to search term"""
        tui, _, _ = create_tui()
        tui.enter_search()

        tui.search_input("a")
        assert tui.search_term == "a"

        tui.search_input("b")
        assert tui.search_term == "ab"

        tui.search_input("c")
        assert tui.search_term == "abc"

    def test_search_input_backspace(self):
        """Test that backspace removes characters"""
        tui, _, _ = create_tui()
        tui.enter_search()

        tui.search_input("a")
        tui.search_input("b")
        tui.search_input("c")
        assert tui.search_term == "abc"

        tui.search_input("\x7f")  # Backspace
        assert tui.search_term == "ab"

        tui.search_input("\b")  # Alternative backspace
        assert tui.search_term == "a"

    def test_search_input_escape(self):
        """Test that escape exits search mode"""
        tui, _, _ = create_tui()
        tui.enter_search()
        tui.search_input("test")

        tui.search_input("\x1b")  # Escape
        assert tui.search_mode is False
        assert tui.search_term == ""

    def test_is_displayed_filters_by_name(self):
        """Test that _is_displayed filters by package name"""
        tui, _, _ = create_tui(total=3)

        on_build_added(tui, "package-foo")
        on_build_added(tui, "package-bar")
        on_build_added(tui, "other")

        build1 = tui.builds["package-foo"]
        build2 = tui.builds["package-bar"]
        build3 = tui.builds["other"]

        # No search term: all displayed
        tui.search_term = ""
        assert tui._is_displayed(build1)
        assert tui._is_displayed(build2)
        assert tui._is_displayed(build3)

        # Search for "package"
        tui.search_term = "package"
        assert tui._is_displayed(build1)
        assert tui._is_displayed(build2)
        assert not tui._is_displayed(build3)

        # Search for "foo"
        tui.search_term = "foo"
        assert tui._is_displayed(build1)
        assert not tui._is_displayed(build2)
        assert not tui._is_displayed(build3)

    def test_is_displayed_filters_by_hash(self):
        """Test that _is_displayed filters by hash prefix"""
        tui, _, _ = create_tui(total=2)

        on_build_added(tui, "abc123", name="pkg1")
        on_build_added(tui, "def456", name="pkg2")

        build1 = tui.builds["abc123"]
        build2 = tui.builds["def456"]

        # Search by hash prefix
        tui.search_term = "abc"
        assert tui._is_displayed(build1)
        assert not tui._is_displayed(build2)

        tui.search_term = "def"
        assert not tui._is_displayed(build1)
        assert tui._is_displayed(build2)


class TestNavigation:
    """Test navigation between builds"""

    def test_get_next_basic(self):
        """Test basic next/previous navigation"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Get first build
        first_id = tui._get_next(1)
        assert first_id == build_ids[0]

        # Set tracked and get next
        tui.tracked_build_id = first_id
        next_id = tui._get_next(1)
        assert next_id == build_ids[1]

        # Get next again
        tui.tracked_build_id = next_id
        next_id = tui._get_next(1)
        assert next_id == build_ids[2]

        # Wrap around
        tui.tracked_build_id = next_id
        next_id = tui._get_next(1)
        assert next_id == build_ids[0]

    def test_get_next_previous(self):
        """Test backward navigation"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Start at second build
        tui.tracked_build_id = build_ids[1]

        # Go backward
        prev_id = tui._get_next(-1)
        assert prev_id == build_ids[0]

        # Go backward again (wrap around)
        tui.tracked_build_id = prev_id
        prev_id = tui._get_next(-1)
        assert prev_id == build_ids[2]

    def test_get_next_with_filter(self):
        """Test navigation respects search filter"""
        tui, _, _ = create_tui(total=4)

        build_ids = ["package-a", "package-b", "other-c", "package-d"]
        for build_id in build_ids:
            on_build_added(tui, build_id)

        # Filter to only "package-*"
        tui.search_term = "package"

        # Should only navigate through matching builds
        first_id = tui._get_next(1)
        assert first_id and first_id == build_ids[0]

        tui.tracked_build_id = first_id
        next_id = tui._get_next(1)
        assert next_id and next_id == build_ids[1]

        tui.tracked_build_id = next_id
        next_id = tui._get_next(1)
        # Should skip "other-c" and go to "package-d"
        assert next_id and next_id == build_ids[3]

    def test_get_next_skips_finished(self):
        """Test that navigation skips finished builds"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Mark middle build as finished
        tui.on_state_changed(build_ids[1], "finished")

        # Navigate from first
        tui.tracked_build_id = build_ids[0]
        next_id = tui._get_next(1)
        # Should skip finished build and go to third
        assert next_id == build_ids[2]

    def test_get_next_no_matching(self):
        """Test that _get_next returns None when no builds match"""
        tui, _, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Mark both as finished
        for build_id in build_ids:
            tui.on_state_changed(build_id, "finished")

        # Should return None since no unfinished builds
        result = tui._get_next(1)
        assert result is None

    def test_get_next_fallback_when_tracked_filtered_out(self):
        """Test that _get_next falls back correctly when tracked build no longer matches filter"""
        tui, _, _ = create_tui(total=3)

        build_ids = ["package-a", "package-b", "other-c"]
        for build_id in build_ids:
            on_build_added(tui, build_id)

        # Start tracking "other-c"
        tui.tracked_build_id = build_ids[2]

        # Now apply a filter that excludes the tracked build
        tui.search_term = "package"

        # _get_next should fall back to first matching build (forward)
        next_id = tui._get_next(1)
        assert next_id == build_ids[0]

        # Test backward direction, should fall back to last matching build
        tui.tracked_build_id = build_ids[2]  # Reset to filtered-out build
        prev_id = tui._get_next(-1)
        assert prev_id == build_ids[1]


class TestTerminalSizes:
    """Test behavior with different terminal sizes"""

    def test_small_terminal_truncation(self):
        """Test that output is truncated for small terminals"""
        tui, _, fake_stdout = create_tui(total=10, terminal_cols=80, terminal_rows=10)

        # Add more builds than can fit on screen
        add_mock_builds(tui, 10)

        tui.render()
        output = fake_stdout.getvalue()

        # Should contain "more..." message indicating truncation
        assert "more..." in output

    def test_large_terminal_no_truncation(self):
        """Test that all builds shown on large terminal"""
        tui, _, fake_stdout = create_tui(total=3, terminal_cols=120)
        add_mock_builds(tui, 3)

        tui.render()
        output = fake_stdout.getvalue()

        # Should not contain truncation message
        assert "more..." not in output
        # Should contain all package names
        for i in range(3):
            assert f"pkg{i}" in output

    def test_narrow_terminal_short_header(self):
        """Test that narrow terminals get shortened header"""
        tui, _, fake_stdout = create_tui(total=1, terminal_cols=40)
        add_mock_builds(tui, 1)

        tui.render()
        output = fake_stdout.getvalue()

        # Should not contain the full header with hints
        assert "filter" not in output
        # But should contain progress
        assert "Progress:" in output


class TestBuildInfo:
    """Test the BuildInfo dataclass"""

    def test_build_info_creation(self):
        """Test that BuildInfo is created correctly"""
        build_info = inst.BuildInfo(
            "mypackage",
            name="mypackage",
            version="1.0",
            external=False,
            prefix="/fake/prefix/mypackage",
            explicit=True,
        )

        assert build_info.name == "mypackage"
        assert build_info.version == "1.0"
        assert build_info.explicit is True
        assert build_info.external is False
        assert build_info.state == "starting"
        assert build_info.finished_time is None
        assert build_info.progress is None

    def test_build_info_external_package(self):
        """Test BuildInfo for external package"""
        build_info = inst.BuildInfo(
            "external-pkg",
            name="external-pkg",
            version="1.0",
            external=True,
            prefix="/usr",
            explicit=False,
        )

        assert build_info.external is True


class TestLogFollowing:
    """Test log following and on_log_output functionality"""

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

    def test_print_logs_when_following(self):
        """Test that logs are printed when following a specific build"""
        tui, _, fake_stdout = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Switch to log-following mode
        tui.overview_mode = False
        tui.tracked_build_id = build_id

        # Send some log data
        log_data = b"Building package...\nRunning tests...\n"
        tui.on_log_output(build_id, log_data)

        # Check that logs were echoed to stdout
        assert fake_stdout._buffer.getvalue() == log_data

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

    def test_verbose_tty_continues_partial_log_line(self):
        """A later log chunk completes a buffered fragment before display above the overview."""
        tui, _, fake_stdout = create_tui(total=1, verbose=True)
        on_build_added(tui, "pkg0")
        tui.render()
        fake_stdout.clear()

        tui.on_log_output("pkg0", b"checking for boost...")
        assert fake_stdout.getvalue() == ""

        tui.on_log_output("pkg0", b"yes\n")

        output = fake_stdout.getvalue()
        assert "checking for boost...yes\n" in output
        assert "Progress:" in output

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
        for index in range(inst.LOG_HISTORY_SIZE + 1):
            tui.on_log_output(build_b, f"b: line {index}\n".encode())
        fake_stdout.clear()

        tui.next(1)

        output = fake_stdout.getvalue()
        assert "b: line 0\n" not in output
        for index in range(1, inst.LOG_HISTORY_SIZE + 1):
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

    def test_can_navigate_to_failed_build(self, tmp_path):
        """Test that navigating to a failed build shows log summary and path"""
        tui, _, fake_stdout = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        log_file = tmp_path / "pkg1.log"
        log_file.write_text("error: something went wrong\n")

        # Set log info before marking the middle build as failed, since that parses the log
        tui.builds[build_ids[1]].log_path = str(log_file)
        tui.on_state_changed(build_ids[1], "failed")

        # Navigate from pkg0 to next -- should land on failed pkg1
        tui.tracked_build_id = build_ids[0]
        next_id = tui._get_next(1)
        assert next_id == build_ids[1]

        # Actually navigate to it
        tui.next(1)
        output = fake_stdout.getvalue()
        assert "Log summary of pkg1" in output
        assert "> error: something went wrong" in output
        assert f"Full log: {log_file}" in output

    def test_navigate_to_failed_build_without_summary(self):
        """Navigating to a failed build with no parsed errors points at the full log."""
        tui, _, fake_stdout = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        tui.on_state_changed(build_ids[1], "failed")
        build_info = tui.builds[build_ids[1]]
        assert build_info.log_summary is None  # no log file, so nothing was parsed
        build_info.log_path = "/tmp/spack/pkg1.log"

        tui.tracked_build_id = build_ids[0]
        tui.next(1)
        assert "No errors parsed from log, see full log: /tmp/spack/pkg1.log" in (
            fake_stdout.getvalue()
        )

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

    def test_navigation_skips_finished_build(self):
        """Test that navigation skips successfully finished builds"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Mark the middle build as finished (successful)
        tui.on_state_changed(build_ids[1], "finished")

        # Try to get next build, should skip the finished one
        tui.tracked_build_id = build_ids[0]
        next_id = tui._get_next(1)

        assert next_id == build_ids[2]


class TestNavigationIntegration:
    """Test the next() method and navigation between builds"""

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

    def test_next_backward_navigation(self):
        """Test that next(-1) navigates backward"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Start at first build
        tui.next()
        assert tui.tracked_build_id == build_ids[0]

        # Go backward (should wrap to last)
        tui.next(-1)
        assert tui.tracked_build_id == build_ids[2]

        # Go backward again
        tui.next(-1)
        assert tui.tracked_build_id == build_ids[1]

    def test_next_does_nothing_when_no_builds(self):
        """Test that next() does nothing when no unfinished builds exist"""
        tui, _, _ = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)

        # Mark as finished
        tui.on_state_changed(build_id, "finished")

        # Try to navigate
        initial_mode = tui.overview_mode
        initial_tracked = tui.tracked_build_id

        tui.next()

        # Nothing should change
        assert tui.overview_mode == initial_mode
        assert tui.tracked_build_id == initial_tracked

    def test_next_does_nothing_when_same_build(self):
        """Test that next() doesn't re-print when already on the same build"""
        tui, _, fake_stdout = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)

        # Start following
        tui.next()
        assert tui.tracked_build_id == build_id

        # Clear output
        fake_stdout.clear()

        # Try to navigate to "next" (which is the same build)
        tui.next()

        # Should not print anything
        assert fake_stdout.getvalue() == ""


class TestToggle:
    """Test toggling selected-build log streaming above the overview."""

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

    def test_non_tty_return_to_overview_disables_log_forwarding(self):
        tui, _, _ = create_tui(total=1, is_tty=False)
        [build_id] = add_mock_builds(tui, 1)
        tui.tracked_build_id = build_id
        tui.overview_mode = False

        tui.on_input("\x1b")

        assert tui.commands == [inst.SetEcho(build_id, False)]

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

    def test_partial_line_handling_on_toggle_and_next(self):
        """Mode transitions preserve complete lines and discard unselected fragments."""
        tui, _, fake_stdout = create_tui(total=2)
        build_a, build_b = add_mock_builds(tui, 2)

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

        # Switching builds must not join an incomplete fragment from another build.
        assert "checking for foo...\n" in written
        assert "checking for bar... yes\n" in written
        assert "checking for baz..." not in written

    @pytest.mark.not_on_windows("Padding functionality unsupported on Windows")
    @pytest.mark.parametrize("filter_padding", [True, False])
    def test_print_logs_filters_padding(self, filter_padding):
        """on_log_output strips path-padding placeholders before writing to stdout."""
        tui, _, fake_stdout = create_tui(filter_padding=filter_padding)
        [build_id] = add_mock_builds(tui, 1)
        log_output = b"--with-foo=/base/__spack_path_placeholder__/__spack_path_placeholder__/bin"

        # track the build and print logs with the relevant path.
        tui.overview_mode = False
        tui.tracked_build_id = build_id
        tui.on_log_output(build_id, log_output)
        written = fake_stdout._buffer.getvalue()

        if filter_padding:
            assert written == b"--with-foo=/base/[padded-to-59-chars]/bin"
        else:
            assert written == log_output

    @pytest.mark.not_on_windows("Padding functionality unsupported on Windows")
    @pytest.mark.parametrize("filter_padding", [True, False])
    def test_prefix_padding_filter_in_status(self, filter_padding):
        """Test that prefix in status indicator applies padding filter."""
        padded_prefix = "/base/__spack_path_placeholder__/__spack_path_placeholder__/mypackage"
        tui, _, fake_stdout = create_tui(is_tty=False, filter_padding=filter_padding)
        build_id = "mypackage"
        on_build_added(tui, build_id, prefix=padded_prefix)
        tui.on_state_changed(build_id, "finished")
        output = fake_stdout.getvalue()
        common = f"[+] {build_id[:7]} mypackage@1.0"
        if filter_padding:
            assert output == f"{common} /base/[padded-to-59-chars]/mypackage\n"
        else:
            assert output == f"{common} {padded_prefix}\n"


class TestSearchFilteringIntegration:
    """Test search mode with display filtering"""

    def test_search_mode_filters_displayed_builds(self):
        """Test that search mode actually filters what's displayed"""
        tui, _, fake_stdout = create_tui(total=4)

        on_build_added(tui, "package-foo")
        on_build_added(tui, "package-bar", version="2.0")
        on_build_added(tui, "other-thing", version="3.0")
        on_build_added(tui, "package-baz", version="4.0")

        # Enter search mode and search for "package"
        tui.enter_search()
        assert tui.search_mode is True

        for character in "package":
            tui.search_input(character)

        assert tui.search_term == "package"

        # Update to render
        tui.render()
        output = fake_stdout.getvalue()

        # Should contain filtered builds
        assert "package-foo" in output
        assert "package-bar" in output
        assert "package-baz" in output
        # Should not contain the filtered-out build
        assert "other-thing" not in output

        # Should show filter prompt
        assert "filter>" in output
        assert tui.search_term in output

    def test_search_mode_with_navigation(self):
        """Test that navigation respects search filter"""
        tui, _, _ = create_tui(total=4)

        build_ids = ["package-a", "other-b", "package-c", "other-d"]
        for build_id in build_ids:
            on_build_added(tui, build_id)

        # Set search term to filter for "package"
        tui.search_term = "package"

        # Start navigating,  should only go through "package-a" and "package-c"
        tui.next()
        assert tui.tracked_build_id == build_ids[0]  # package-a

        tui.next(1)
        # Should skip other-b and go to package-c
        assert tui.tracked_build_id == build_ids[2]  # package-c

        tui.next(1)
        # Should wrap around to package-a
        assert tui.tracked_build_id == build_ids[0]  # package-a

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

    def test_clearing_search_shows_all_builds(self):
        """Test that clearing search term shows all builds again"""
        tui, _, fake_stdout = create_tui(total=3)

        on_build_added(tui, "package-a")
        on_build_added(tui, "other-b", version="2.0")
        on_build_added(tui, "package-c", version="3.0")

        # Enter search and type something
        tui.enter_search()
        tui.search_input("p")
        tui.search_input("a")
        tui.search_input("c")
        assert tui.search_term == "pac"

        # Clear it with backspace
        tui.search_input("\x7f")  # backspace
        tui.search_input("\x7f")  # backspace
        tui.search_input("\x7f")  # backspace
        assert tui.search_term == ""

        # Update to render
        tui.render()
        output = fake_stdout.getvalue()

        # All builds should be visible now
        assert "package-a" in output
        assert "other-b" in output
        assert "package-c" in output


class TestHandleInput:
    """Test the on_input keyboard dispatch."""

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

    def test_search_keys(self):
        """'/' enters search mode; subsequent characters build the search term."""
        tui, _, _ = create_tui(total=2)
        add_mock_builds(tui, 2)

        tui.on_input("/abc")
        assert tui.search_mode is True
        assert tui.search_term == "abc"

        tui.on_input("\x1b")  # Escape exits search mode
        assert tui.search_mode is False

    def test_parallelism_keys(self):
        """'+' and '-' produce ChangeJobs commands for the event loop."""
        tui, _, _ = create_tui(total=1)
        add_mock_builds(tui, 1)

        tui.on_input("++-")
        assert tui.commands == [inst.ChangeJobs(1), inst.ChangeJobs(1), inst.ChangeJobs(-1)]


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_build_list(self):
        """Test update with no builds"""
        tui, _, fake_stdout = create_tui(total=0)

        tui.render()
        output = fake_stdout.getvalue()

        # Should render header but no builds
        assert "Progress:" in output
        assert "0/0" in output

    def test_no_header_with_finalize(self):
        """Test that we don't print a header with finalize=True"""
        tui, _, fake_stdout = create_tui(total=2, color=False)
        build_a, build_b = add_mock_builds(tui, 2)
        tui.on_state_changed(build_a, "finished")
        tui.on_state_changed(build_b, "failed")
        tui.render(finalize=True)

        output = fake_stdout.getvalue()

        # Should not contain header
        assert "Progress:" not in output

        # Should contain final status lines for both builds
        assert f"[+] {build_a[:7]} pkg0@0.0" in output
        assert f"[x] {build_b[:7]} pkg1@1.0" in output

    def test_finalize_keeps_overview_mode(self):
        """render(finalize=True) keeps the overview mode even while logs are streaming."""
        tui, _, _ = create_tui(total=2)
        add_mock_builds(tui, 2)
        tui.toggle()
        assert tui.overview_mode is True
        assert tui.log_streaming is True

        tui.render(finalize=True)
        assert tui.overview_mode is True

    def test_all_builds_finished(self):
        """Test when all builds are finished"""
        tui, fake_time, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Mark all as finished
        for build_id in build_ids:
            tui.on_state_changed(build_id, "finished")

        # Advance time and update
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        tui.render()

        # All should be cleaned up
        assert len(tui.builds) == 0
        assert tui.completed == 2

    def test_on_progress_rounds_correctly(self):
        """Test that progress percentage rounding works"""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Test truncation
        # Test rounding
        tui.on_progress(build_id, 1, 3)
        assert tui.builds[build_id].progress == inst.BuildProgress("33%", "fetching")

        tui.on_progress(build_id, 2, 3)
        assert tui.builds[build_id].progress == inst.BuildProgress("66%", "fetching")

        tui.on_progress(build_id, 3, 3)
        assert tui.builds[build_id].progress == inst.BuildProgress("100%", "fetching")


class TestTerminalUIVerbose:
    """Tests for verbose non-TTY log tracking in TerminalUI."""

    def test_verbose_tracks_first_build(self):
        """First on_build_added for verbose non-TTY sets tracked_build_id and enables echoing."""
        tui, _, _ = create_tui(is_tty=False, verbose=True, total=4)

        on_build_added(tui, "trivial-install-test-package")

        assert tui.tracked_build_id == "trivial-install-test-package"
        assert tui.commands == [inst.SetEcho("trivial-install-test-package", True)]

    def test_verbose_does_not_track_when_already_tracking(self):
        """Second on_build_added() while already tracking does not switch tracking."""
        tui, _, _ = create_tui(is_tty=False, verbose=True, total=4)

        on_build_added(tui, "pkg1")
        first_tracked = tui.tracked_build_id

        on_build_added(tui, "pkg2", explicit=False)
        assert tui.tracked_build_id == first_tracked
        assert tui.tracked_build_id == "pkg1"

        # Echoing should not have been enabled for the second build
        assert tui.commands == [inst.SetEcho("pkg1", True)]

    def test_verbose_switches_on_finish(self):
        """After the tracked build finishes, tracked_build_id is cleared."""
        tui, _, _ = create_tui(is_tty=False, verbose=True, total=4)

        on_build_added(tui, "trivial-install-test-package")
        assert tui.tracked_build_id == "trivial-install-test-package"

        tui.on_state_changed("trivial-install-test-package", "finished")
        assert tui.tracked_build_id == ""

    def test_verbose_print_logs_tracked(self):
        """on_log_output() for the tracked build writes to stdout."""
        tui, _, stdout = create_tui(is_tty=False, verbose=True, total=1)

        on_build_added(tui, "trivial-install-test-package")
        tui.on_log_output("trivial-install-test-package", b"hello log\n")

        stdout.flush()
        assert stdout.buffer.getvalue() == b"hello log\n"

    def test_verbose_print_logs_untracked(self):
        """on_log_output() for an untracked build discards data."""
        tui, _, stdout = create_tui(is_tty=False, verbose=True, total=2)

        on_build_added(tui, "pkg1")
        on_build_added(tui, "pkg2", explicit=False)

        # Only pkg1 is tracked; pkg2 logs should be discarded
        tui.on_log_output("pkg2", b"ignored\n")

        stdout.flush()
        assert stdout.buffer.getvalue() == b""

    def test_verbose_tty_tracks_first_build(self):
        """Verbose mode selects the first TTY build while keeping the overview visible."""
        tui, _, _ = create_tui(is_tty=True, verbose=True, total=4)

        on_build_added(tui, "trivial-install-test-package")
        assert tui.overview_mode is True
        assert tui.tracked_build_id == "trivial-install-test-package"
        assert tui.commands == [inst.SetEcho("trivial-install-test-package", True)]


class TestTerminalUIColor:
    """Tests that TerminalUI respects the explicit color=True/False parameter."""

    def test_non_tty_finished_color_true_emits_green(self):
        """color=True in non-TTY mode: finished line has per-component ANSI colors."""
        tui, _, stdout = create_tui(is_tty=False, total=1, color=True)
        on_build_added(tui, "pkg")
        tui.on_state_changed("pkg", "finished")
        # green indicator, reset, dark-gray hash
        expected = spack.util.tty.color.colorize("@g[+]@. @K", color=True)
        assert stdout.getvalue().startswith(expected)

    def test_non_tty_failed_color_true_emits_red(self):
        """color=True in non-TTY mode: failed line has per-component ANSI colors."""
        tui, _, stdout = create_tui(is_tty=False, total=1, color=True)
        on_build_added(tui, "pkg")
        tui.on_state_changed("pkg", "failed")
        # red indicator, reset, dark-gray hash
        expected = spack.util.tty.color.colorize("@r[x]@. @K", color=True)
        assert stdout.getvalue().startswith(expected)

    def test_non_tty_finished_color_false_no_ansi(self):
        """color=False in non-TTY mode: finished line has no ANSI escape codes."""
        tui, _, stdout = create_tui(is_tty=False, total=1, color=False)
        on_build_added(tui, "pkg")
        tui.on_state_changed("pkg", "finished")
        assert "\033[" not in stdout.getvalue()


class TestTargetJobs:
    """Test on_jobs_changed and its effect on the header."""

    def test_on_jobs_changed_marks_dirty(self):
        """on_jobs_changed with a new value should update target_jobs and mark dirty."""
        tui, _, _ = create_tui()
        tui.dirty = False
        tui.on_jobs_changed(3, 2)
        assert tui.actual_jobs == 3
        assert tui.target_jobs == 2
        assert tui.dirty is True
        tui.on_jobs_changed(2, 2)
        assert tui.actual_jobs == 2
        assert tui.target_jobs == 2

    def test_on_jobs_changed_same_value_no_dirty(self):
        """on_jobs_changed with the same value should not mark dirty."""
        tui, _, _ = create_tui()
        tui.on_jobs_changed(5, 5)
        tui.dirty = False
        tui.on_jobs_changed(5, 5)
        assert tui.dirty is False

    def test_header_shows_target_jobs(self):
        """The rendered header should contain the target_jobs count and the word 'jobs'."""
        tui, _, fake_stdout = create_tui(total=1)
        add_mock_builds(tui, 1)
        tui.on_jobs_changed(4, 4)
        tui.render()
        output = fake_stdout.getvalue()
        assert "4" in output
        assert "jobs" in output

    def test_header_shows_arrow_when_pending(self):
        """When actual != target, the header should show 'actual=>target jobs'."""
        tui, _, fake_stdout = create_tui(total=1)
        add_mock_builds(tui, 1)
        tui.on_jobs_changed(4, 2)
        tui.render()
        output = fake_stdout.getvalue()
        assert "4=>2" in output

    def test_header_shows_tracked_package_name(self):
        """The overview header shows the currently tracked package in gray."""
        tui, _, fake_stdout = create_tui(total=1, color=True)
        [build_id] = add_mock_builds(tui, 1)
        tui.tracked_build_id = build_id
        tui.render()
        output = fake_stdout.getvalue()
        assert "next/prev" in output
        assert f"\033[0;90m({build_id})\033[0m" in output


class TestHeadlessMode:
    """Test that headless mode suppresses terminal output."""

    def test_on_headless_changed_transitions(self):
        """on_headless_changed(True) invalidates the display area; on_headless_changed(False)
        marks dirty."""
        tui, _, _ = create_tui(is_tty=True)
        tui.active_area_rows = 5
        tui.on_headless_changed(True)
        assert tui.headless is True
        assert tui.active_area_rows == 0

        tui.dirty = False
        tui.on_headless_changed(False)
        assert tui.headless is False
        assert tui.dirty is True

    def test_render_suppressed_when_headless(self):
        """render() should not write anything when headless is True."""
        tui, time_values, stdout = create_tui(is_tty=True, total=1)
        add_mock_builds(tui, 1)
        tui.headless = True
        time_values.append(10.0)
        tui.render()
        assert stdout.getvalue() == ""

    def test_print_logs_suppressed_when_headless(self):
        """on_log_output() should discard data when headless is True."""
        tui, _, stdout = create_tui(is_tty=True, total=1)
        build_ids = add_mock_builds(tui, 1)
        tui.tracked_build_id = build_ids[0]
        tui.headless = True
        tui.on_log_output(build_ids[0], b"hello world\n")
        assert stdout.getvalue() == ""

    def test_on_state_changed_non_tty_suppressed_when_headless(self):
        """on_state_changed() non-TTY output should be suppressed when headless."""
        tui, _, stdout = create_tui(is_tty=False, total=1)
        on_build_added(tui, "pkg")
        tui.headless = True
        stdout.clear()
        tui.on_state_changed("pkg", "finished")
        assert stdout.getvalue() == ""

    def test_render_works_after_headless_cleared(self):
        """render() should work normally once headless is cleared."""
        tui, time_values, stdout = create_tui(is_tty=True, total=1, color=False)
        add_mock_builds(tui, 1)
        tui.headless = True
        time_values.append(10.0)
        tui.render()
        assert stdout.getvalue() == ""
        # Clear headless and verify output resumes
        tui.headless = False
        tui.dirty = True
        tui.render()
        assert "[/] pkg0 pkg0@0.0 starting" in stdout.getvalue()

    def test_refresh_interval_modes(self):
        """Only a foreground TTY overview requests periodic redraws."""
        tui, _, _ = create_tui(is_tty=True)
        assert tui.refresh_interval() == inst.SPINNER_INTERVAL
        tui.headless = True
        assert tui.refresh_interval() is None
        tui.headless = False
        tui.overview_mode = False
        assert tui.refresh_interval() is None
        non_tty, _, _ = create_tui(is_tty=False)
        assert non_tty.refresh_interval() is None


class TestBlockedIndicator:
    """Test set_blocked and the blocked message in the overview."""

    def test_on_blocked_changed_marks_dirty_once(self):
        """set_blocked marks dirty on a change, but not when the value is unchanged."""
        tui, _, _ = create_tui()
        tui.dirty = False
        tui.on_blocked_changed(True)
        assert tui.blocked is True
        assert tui.dirty is True

        tui.dirty = False
        tui.on_blocked_changed(True)
        assert tui.dirty is False

    def test_blocked_message_rendered(self):
        """When blocked and nothing is running, the overview shows a waiting message."""
        tui, _, fake_stdout = create_tui()
        tui.on_blocked_changed(True)
        tui.render()
        assert "Waiting for other Spack install process" in fake_stdout.getvalue()


class TestLineRendering:
    """Test individual build-line components in the rendered output."""

    @pytest.mark.parametrize(
        "progress,expected",
        [
            (None, None),
            (inst.BuildProgress(message="configuring"), None),
            (inst.BuildProgress("50%", "fetching"), "50%"),
        ],
    )
    def test_progress_prefix(self, progress, expected):
        tui, _, _ = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)
        build_info = tui.builds[build_id]
        build_info.progress = progress

        assert tui._progress_prefix(build_info) == expected

    def test_fetch_progress_rendered(self):
        """A build with fetch progress shows its percentage alongside the state."""
        tui, _, fake_stdout = create_tui(total=1, color=False)
        [build_id] = add_mock_builds(tui, 1)
        tui.on_progress(build_id, 50, 100)
        tui.render()
        assert "(50%) fetching" in fake_stdout.getvalue()

    def test_failed_line_shows_log_path(self):
        """A failed build's line includes the path to its log file."""
        tui, _, fake_stdout = create_tui(is_tty=False, total=1)
        on_build_added(tui, "pkg", log_path="/tmp/pkg.log")
        tui.on_state_changed("pkg", "failed")
        assert "failed: /tmp/pkg.log" in fake_stdout.getvalue()

    def test_external_indicator(self):
        """External packages are rendered with the [e] indicator."""
        tui, _, fake_stdout = create_tui(is_tty=False, total=1)
        on_build_added(tui, "pkg", external=True)
        tui.on_state_changed("pkg", "finished")
        assert "[e]" in fake_stdout.getvalue()

    def test_non_tty_running_build_static_indicator(self):
        """Non-TTY state lines use the static [ ] indicator for builds still in progress, and
        render implicit builds with a plain (non-bold) name."""
        tui, _, fake_stdout = create_tui(is_tty=False, total=1, color=False)
        on_build_added(tui, "pkg", explicit=False)
        tui.on_state_changed("pkg", "installing")
        line = fake_stdout.getvalue()
        assert line.startswith("[ ] ")
        assert "pkg@1.0" in line

    def test_line_truncated_to_terminal_width(self):
        """Build lines are cut off at the terminal width in the interactive overview."""
        tui, _, fake_stdout = create_tui(total=1, terminal_cols=30, color=False)
        on_build_added(tui, "pkg", prefix="/quite/long/prefix/path")
        tui.on_state_changed("pkg", "finished")
        tui.render()
        output = fake_stdout.getvalue()
        assert "pkg@1.0" in output
        # The prefix would exceed the terminal width, so it is not rendered.
        assert "/quite/long/prefix/path" not in output

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


class TestStdinReader:
    def test_basic_ascii(self):
        r, w = os.pipe()
        try:
            reader = _fd_reader(r)
            os.write(w, b"abc")
            assert reader.read() == "abc"
        finally:
            os.close(r)
            os.close(w)

    def test_ansi_stripping(self):
        r, w = os.pipe()
        try:
            reader = _fd_reader(r)
            os.write(w, b"hello\x1b[Aworld\x1b[B!")
            assert reader.read() == "helloworld!"
        finally:
            os.close(r)
            os.close(w)

    def test_multibyte_utf8(self):
        r, w = os.pipe()
        try:
            reader = _fd_reader(r)
            encoded = "é".encode("utf-8")  # 0xc3 0xa9
            os.write(w, encoded[:1])
            # First read: incomplete char, decoder buffers it
            result1 = reader.read()
            os.write(w, encoded[1:])
            result2 = reader.read()
            assert result1 + result2 == "é"
        finally:
            os.close(r)
            os.close(w)

    def test_oserror_returns_empty(self):
        r, w = os.pipe()
        os.close(w)
        os.close(r)
        reader = _fd_reader(r)
        assert reader.read() == ""

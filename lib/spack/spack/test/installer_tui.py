# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the TerminalUI terminal UI in new_installer.py"""

import sys

import pytest

if sys.platform == "win32":
    pytest.skip("No Windows support", allow_module_level=True)


import functools
import io
import os
from typing import List, Optional, Tuple

import spack.new_installer as inst
from spack.new_installer import TerminalUI
from spack.new_installer_base import StdinReader


def _fd_reader(fd: int) -> StdinReader:
    """StdinReader reading from a raw fd, as PosixTerminalState.create_stdin_reader does."""
    return StdinReader(functools.partial(os.read, fd, 1024))


class SimpleTextIOWrapper(io.TextIOWrapper):
    """TextIOWrapper around a BytesIO buffer for testing of stdout behavior"""

    def __init__(self, tty: bool) -> None:
        self._buffer = io.BytesIO()
        self._tty = tty
        super().__init__(self._buffer, encoding="utf-8", line_buffering=True)

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
        get_terminal_size=mock_get_terminal_size,
        get_time=mock_get_time,
        is_tty=is_tty,
        verbose=verbose,
        filter_padding=filter_padding,
        color=color,
    )
    tui.controller = _NoopController()

    return tui, time_values, fake_stdout


class _NoopController:
    """No-op controller for view tests that don't inspect controller calls."""

    def set_echo(self, build_id: str, echo: bool) -> None: ...

    def increase_jobs(self) -> None: ...

    def decrease_jobs(self) -> None: ...


def add_build(
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
    tui.add_build(
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
        add_build(tui, build_id, version=f"{i}.0")
    return build_ids


def record_echo(tui: TerminalUI) -> List[Tuple[str, bool]]:
    """Replace the tui's controller with one that records set_echo calls."""
    calls: List[Tuple[str, bool]] = []

    class Recorder:
        def set_echo(self, build_id: str, echo: bool) -> None:
            calls.append((build_id, echo))

        def increase_jobs(self) -> None: ...

        def decrease_jobs(self) -> None: ...

    tui.controller = Recorder()
    return calls


class TestBasicStateManagement:
    """Test basic state management operations"""

    def test_on_resize(self):
        """Test that on_resize sets terminal_size_changed and update() fetches lazily"""
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

        # The actual size is fetched lazily on the first update()
        tui.render()
        assert tui.terminal_size == os.terminal_size((120, 40))
        assert tui.terminal_size_changed is False

    def test_add_build(self):
        """Test that add_build adds builds correctly"""
        tui, _, _ = create_tui(total=2)

        add_build(tui, "pkg1", explicit=True)
        assert len(tui.builds) == 1
        assert "pkg1" in tui.builds
        assert tui.builds["pkg1"].name == "pkg1"
        assert tui.builds["pkg1"].explicit is True
        assert tui.dirty is True

        add_build(tui, "pkg2", version="2.0", explicit=False)
        assert len(tui.builds) == 2
        assert "pkg2" in tui.builds
        assert tui.builds["pkg2"].explicit is False

    def test_update_state_transitions(self):
        """Test that update_state transitions states properly"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Update to 'building' state
        tui.update_state(build_id, "building")
        assert tui.builds[build_id].state == "building"
        assert tui.builds[build_id].progress_percent is None
        assert tui.completed == 0

        # Update to 'finished' state
        tui.update_state(build_id, "finished")
        assert tui.builds[build_id].state == "finished"
        assert tui.completed == 1
        assert tui.builds[build_id].finished_time == fake_time[0] + inst.CLEANUP_TIMEOUT

    def test_update_state_failed(self):
        """Test that failed state increments completed counter"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        tui.update_state(build_id, "failed")
        assert tui.builds[build_id].state == "failed"
        assert tui.completed == 1
        assert tui.builds[build_id].finished_time == fake_time[0] + inst.CLEANUP_TIMEOUT

    def test_remove_build(self):
        """Test that remove_build removes the build from the display."""
        tui, _, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        tui.dirty = False
        tui.remove_build(build_ids[0])
        assert build_ids[0] not in tui.builds
        assert len(tui.builds) == 1
        assert tui.dirty is True

    def test_remove_build_resets_tracked(self):
        """Test that removing the tracked build resets tracking to overview mode."""
        tui, _, _ = create_tui(total=1)
        [build_id] = add_mock_builds(tui, 1)

        tui.tracked_build_id = build_id
        tui.overview_mode = False
        tui.remove_build(build_id)
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
        tui.update_state(build_id, "failed")
        assert tui.builds[build_id].log_summary is not None
        assert "error" in tui.builds[build_id].log_summary.lower()

    def test_failed_state_no_log_path(self):
        """No summary is stored for a failed build without a log path."""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        tui.update_state(build_id, "failed")
        assert tui.builds[build_id].log_summary is None

    def test_failed_state_missing_log_file(self, tmp_path):
        """No summary is stored for a failed build whose log file doesn't exist."""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        tui.builds[build_id].log_path = str(tmp_path / "nonexistent.log")
        tui.update_state(build_id, "failed")
        assert tui.builds[build_id].log_summary is None

    def test_update_progress(self):
        """Test that update_progress updates percentages"""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Update progress
        tui.update_progress(build_id, 50, 100)
        assert tui.builds[build_id].progress_percent == 50
        assert tui.dirty is True

        # Same percentage shouldn't mark dirty again
        tui.dirty = False
        tui.update_progress(build_id, 50, 100)
        assert tui.dirty is False

        # Different percentage should mark dirty
        tui.update_progress(build_id, 75, 100)
        assert tui.builds[build_id].progress_percent == 75
        assert tui.dirty is True

    def test_completion_counter(self):
        """Test that completion counter increments correctly"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        assert tui.completed == 0

        tui.update_state(build_ids[0], "finished")
        assert tui.completed == 1

        tui.update_state(build_ids[1], "failed")
        assert tui.completed == 2

        tui.update_state(build_ids[2], "finished")
        assert tui.completed == 3


class TestOutputRendering:
    """Test output rendering for TTY and non-TTY modes"""

    def test_non_tty_output(self):
        """Test that non-TTY mode prints simple state changes"""
        tui, _, fake_stdout = create_tui(is_tty=False)

        add_build(tui, "mypackage")
        tui.update_state("mypackage", "finished")

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
        """Test that update() skips rendering when not dirty"""
        tui, _, fake_stdout = create_tui()
        add_mock_builds(tui, 1)
        tui.render()

        # Clear stdout and mark not dirty
        fake_stdout.clear()
        tui.dirty = False

        # Update should not produce output
        tui.render()
        assert fake_stdout.getvalue() == ""

    def test_update_throttling(self):
        """Test that update() throttles redraws"""
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
        tui.update_state(build_ids[0], "finished")
        tui.update_state(build_ids[1], "finished")

        add_build(tui, "pkg3", version="3.0")
        add_build(tui, "pkg4", version="4.0")

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
        assert tui.spinner_index == (initial_index + 1) % len(tui.spinner_chars)

    def test_finished_package_cleanup(self):
        """Test that finished packages are cleaned up after timeout"""
        tui, fake_time, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Mark as finished
        fake_time[0] = 0.0
        tui.update_state(build_id, "finished")

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
        tui.update_state(build_id, "failed")

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

        add_build(tui, "package-foo")
        add_build(tui, "package-bar")
        add_build(tui, "other")

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

        add_build(tui, "abc123", name="pkg1")
        add_build(tui, "def456", name="pkg2")

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
            add_build(tui, build_id)

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
        tui.update_state(build_ids[1], "finished")

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
            tui.update_state(build_id, "finished")

        # Should return None since no unfinished builds
        result = tui._get_next(1)
        assert result is None

    def test_get_next_fallback_when_tracked_filtered_out(self):
        """Test that _get_next falls back correctly when tracked build no longer matches filter"""
        tui, _, _ = create_tui(total=3)

        build_ids = ["package-a", "package-b", "other-c"]
        for build_id in build_ids:
            add_build(tui, build_id)

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
        assert build_info.progress_percent is None

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
    """Test log following and print_logs functionality"""

    def test_print_logs_when_following(self):
        """Test that logs are printed when following a specific build"""
        tui, _, fake_stdout = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Switch to log-following mode
        tui.overview_mode = False
        tui.tracked_build_id = build_id

        # Send some log data
        log_data = b"Building package...\nRunning tests...\n"
        tui.print_logs(build_id, log_data)

        # Check that logs were echoed to stdout
        assert fake_stdout._buffer.getvalue() == log_data

    def test_print_logs_discarded_when_in_overview_mode(self):
        """Test that logs are discarded when in overview mode"""
        tui, _, fake_stdout = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Stay in overview mode
        assert tui.overview_mode is True

        # Try to print logs
        log_data = b"Should not be printed\n"
        tui.print_logs(build_id, log_data)

        # Nothing should be printed
        assert fake_stdout.getvalue() == ""

    def test_print_logs_discarded_when_not_tracked(self):
        """Test that logs from non-tracked builds are discarded"""
        tui, _, fake_stdout = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Switch to log-following mode for the first build
        tui.overview_mode = False
        tui.tracked_build_id = build_ids[0]

        # Try to print logs from the second build (not tracked)
        log_data = b"Logs from pkg2\n"
        tui.print_logs(build_ids[1], log_data)

        # Nothing should be printed since we're tracking pkg0, not pkg1
        assert fake_stdout.getvalue() == ""

    def test_can_navigate_to_failed_build(self):
        """Test that navigating to a failed build shows log summary and path"""
        tui, _, fake_stdout = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Mark the middle build as failed and set log info
        tui.update_state(build_ids[1], "failed")
        build_info = tui.builds[build_ids[1]]
        build_info.log_summary = "Error: something went wrong\n"
        build_info.log_path = "/tmp/spack/pkg1.log"

        # Navigate from pkg0 to next -- should land on failed pkg1
        tui.tracked_build_id = build_ids[0]
        next_id = tui._get_next(1)
        assert next_id == build_ids[1]

        # Actually navigate to it
        tui.next(1)
        output = fake_stdout.getvalue()
        assert "Log summary of pkg1" in output
        assert "Error: something went wrong" in output
        assert "/tmp/spack/pkg1.log" in output

    def test_navigation_skips_finished_build(self):
        """Test that navigation skips successfully finished builds"""
        tui, _, _ = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)

        # Mark the middle build as finished (successful)
        tui.update_state(build_ids[1], "finished")

        # Try to get next build, should skip the finished one
        tui.tracked_build_id = build_ids[0]
        next_id = tui._get_next(1)

        assert next_id == build_ids[2]


class TestNavigationIntegration:
    """Test the next() method and navigation between builds"""

    def test_next_switches_from_overview_to_logs(self):
        """Test that next() switches from overview mode to log-following mode"""
        tui, _, fake_stdout = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)
        echo_calls = record_echo(tui)

        # Start in overview mode
        assert tui.overview_mode is True
        assert tui.tracked_build_id == ""

        # Call next() to start following first build
        tui.next()

        # Should have switched to log-following mode
        assert tui.overview_mode is False
        assert tui.tracked_build_id == build_ids[0]
        assert echo_calls == [(build_ids[0], True)]

        # Should have printed "Following logs" message
        output = fake_stdout.getvalue()
        assert "Following logs of" in output
        assert "pkg0" in output

    def test_next_cycles_through_builds(self):
        """Test that next() cycles through multiple builds"""
        tui, _, fake_stdout = create_tui(total=3)
        build_ids = add_mock_builds(tui, 3)
        echo_calls = record_echo(tui)

        # Start following first build
        tui.next()
        assert tui.tracked_build_id == build_ids[0]

        fake_stdout.clear()

        # Navigate to next
        tui.next(1)
        assert tui.tracked_build_id == build_ids[1]
        assert "pkg1" in fake_stdout.getvalue()
        # Echoing stopped for the previous build and started for the new one
        assert echo_calls[-2:] == [(build_ids[0], False), (build_ids[1], True)]

        fake_stdout.clear()

        # Navigate to next (third build)
        tui.next(1)
        assert tui.tracked_build_id == build_ids[2]
        assert "pkg2" in fake_stdout.getvalue()

        fake_stdout.clear()

        # Navigate to next (should wrap to first)
        tui.next(1)
        assert tui.tracked_build_id == build_ids[0]
        assert "pkg0" in fake_stdout.getvalue()

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
        tui.update_state(build_id, "finished")

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
    """Test toggle() method for switching between overview and log-following modes"""

    def test_toggle_from_overview_calls_next(self):
        """Test that toggle() from overview mode calls next()"""
        tui, _, fake_stdout = create_tui(total=2)
        add_mock_builds(tui, 2)

        # Start in overview mode
        assert tui.overview_mode is True

        # Toggle should call next()
        tui.toggle()

        # Should now be following logs
        assert tui.overview_mode is False
        assert tui.tracked_build_id != ""
        assert "Following logs of" in fake_stdout.getvalue()

    def test_toggle_from_logs_returns_to_overview(self):
        """Test that toggle() from log-following mode returns to overview"""
        tui, _, _ = create_tui(total=2)
        add_mock_builds(tui, 2)
        echo_calls = record_echo(tui)

        # Switch to log-following mode first
        tui.next()
        assert tui.overview_mode is False
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
        assert tui.tracked_build_id == ""
        assert tui.search_term == ""
        assert tui.search_mode is False
        assert tui.active_area_rows == 0
        assert tui.dirty is True
        # Echoing was stopped for the previously tracked build
        assert echo_calls[-1] == (tracked_id, False)

    def test_update_state_finished_triggers_toggle_when_tracking(self):
        """Test that finishing a tracked build triggers toggle back to overview"""
        tui, _, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Start tracking first build
        tui.next()
        assert tui.overview_mode is False
        assert tui.tracked_build_id == build_ids[0]

        # Mark the tracked build as finished
        tui.update_state(build_ids[0], "finished")

        # Should have toggled back to overview mode
        assert tui.overview_mode is True
        assert tui.tracked_build_id == ""

    def test_partial_line_newline_on_toggle_and_next(self):
        """Ensure newline is inserted before mode transitions when log doesn't end with newline."""
        tui, _, fake_stdout = create_tui(total=2)
        build_a, build_b = add_mock_builds(tui, 2)

        # Follow a build, toggle back and forth between logs and overview mode, and receive logs
        # that may or may not end with newlines.
        tui.next()
        tui.print_logs(build_a, b"checking for foo...")
        tui.toggle()
        tui.next()
        tui.print_logs(build_a, b"checking for bar... yes\n")
        tui.next(1)
        tui.print_logs(build_b, b"checking for baz...")
        tui.next(-1)

        written = fake_stdout.getvalue()

        # There shouldn't be any double newlines:
        assert "\n\n" not in written

        # All partial and newline-terminated logs should be present with appropriate newlines:
        assert "checking for foo...\n" in written
        assert "checking for bar... yes\n" in written
        assert "checking for baz...\n" in written

    @pytest.mark.parametrize("filter_padding", [True, False])
    def test_print_logs_filters_padding(self, filter_padding):
        """print_logs strips path-padding placeholders before writing to stdout."""
        tui, _, fake_stdout = create_tui(filter_padding=filter_padding)
        [build_id] = add_mock_builds(tui, 1)
        log_output = b"--with-foo=/base/__spack_path_placeholder__/__spack_path_placeholder__/bin"

        # track the build and print logs with the relevant path.
        tui.overview_mode = False
        tui.tracked_build_id = build_id
        tui.print_logs(build_id, log_output)
        written = fake_stdout._buffer.getvalue()

        if filter_padding:
            assert written == b"--with-foo=/base/[padded-to-59-chars]/bin"
        else:
            assert written == log_output

    @pytest.mark.parametrize("filter_padding", [True, False])
    def test_prefix_padding_filter_in_status(self, filter_padding):
        """Test that prefix in status indicator applies padding filter."""
        padded_prefix = "/base/__spack_path_placeholder__/__spack_path_placeholder__/mypackage"
        tui, _, fake_stdout = create_tui(is_tty=False, filter_padding=filter_padding)
        build_id = "mypackage"
        add_build(tui, build_id, prefix=padded_prefix)
        tui.update_state(build_id, "finished")
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

        add_build(tui, "package-foo")
        add_build(tui, "package-bar", version="2.0")
        add_build(tui, "other-thing", version="3.0")
        add_build(tui, "package-baz", version="4.0")

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
            add_build(tui, build_id)

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
        assert tui.overview_mode is False
        assert tui.tracked_build_id == build_ids[0]

    def test_clearing_search_shows_all_builds(self):
        """Test that clearing search term shows all builds again"""
        tui, _, fake_stdout = create_tui(total=3)

        add_build(tui, "package-a")
        add_build(tui, "other-b", version="2.0")
        add_build(tui, "package-c", version="3.0")

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
        tui.update_state(build_a, "finished")
        tui.update_state(build_b, "failed")
        tui.render(finalize=True)

        output = fake_stdout.getvalue()

        # Should not contain header
        assert "Progress:" not in output

        # Should contain final status lines for both builds
        assert f"[+] {build_a[:7]} pkg0@0.0" in output
        assert f"[x] {build_b[:7]} pkg1@1.0" in output

    def test_all_builds_finished(self):
        """Test when all builds are finished"""
        tui, fake_time, _ = create_tui(total=2)
        build_ids = add_mock_builds(tui, 2)

        # Mark all as finished
        for build_id in build_ids:
            tui.update_state(build_id, "finished")

        # Advance time and update
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        tui.render()

        # All should be cleaned up
        assert len(tui.builds) == 0
        assert tui.completed == 2

    def test_update_progress_rounds_correctly(self):
        """Test that progress percentage rounding works"""
        tui, _, _ = create_tui()
        [build_id] = add_mock_builds(tui, 1)

        # Test rounding
        tui.update_progress(build_id, 1, 3)
        assert tui.builds[build_id].progress_percent == 33  # int(100/3)

        tui.update_progress(build_id, 2, 3)
        assert tui.builds[build_id].progress_percent == 66  # int(200/3)

        tui.update_progress(build_id, 3, 3)
        assert tui.builds[build_id].progress_percent == 100


class TestTerminalUIVerbose:
    """Tests for verbose non-TTY log tracking in TerminalUI."""

    def test_verbose_tracks_first_build(self):
        """First add_build() in verbose non-TTY mode sets tracked_build_id and enables echoing."""
        tui, _, _ = create_tui(is_tty=False, verbose=True, total=4)
        echo_calls = record_echo(tui)

        add_build(tui, "trivial-install-test-package")

        assert tui.tracked_build_id == "trivial-install-test-package"
        assert echo_calls == [("trivial-install-test-package", True)]

    def test_verbose_does_not_track_when_already_tracking(self):
        """Second add_build() while already tracking does not switch tracking."""
        tui, _, _ = create_tui(is_tty=False, verbose=True, total=4)
        echo_calls = record_echo(tui)

        add_build(tui, "pkg1")
        first_tracked = tui.tracked_build_id

        add_build(tui, "pkg2", explicit=False)
        assert tui.tracked_build_id == first_tracked
        assert tui.tracked_build_id == "pkg1"

        # Echoing should not have been enabled for the second build
        assert echo_calls == [("pkg1", True)]

    def test_verbose_switches_on_finish(self):
        """After the tracked build finishes, tracked_build_id is cleared."""
        tui, _, _ = create_tui(is_tty=False, verbose=True, total=4)

        add_build(tui, "trivial-install-test-package")
        assert tui.tracked_build_id == "trivial-install-test-package"

        tui.update_state("trivial-install-test-package", "finished")
        assert tui.tracked_build_id == ""

    def test_verbose_print_logs_tracked(self):
        """print_logs() for the tracked build writes to stdout."""
        tui, _, stdout = create_tui(is_tty=False, verbose=True, total=1)

        add_build(tui, "trivial-install-test-package")
        tui.print_logs("trivial-install-test-package", b"hello log\n")

        stdout.flush()
        assert stdout.buffer.getvalue() == b"hello log\n"

    def test_verbose_print_logs_untracked(self):
        """print_logs() for an untracked build discards data."""
        tui, _, stdout = create_tui(is_tty=False, verbose=True, total=2)

        add_build(tui, "pkg1")
        add_build(tui, "pkg2", explicit=False)

        # Only pkg1 is tracked; pkg2 logs should be discarded
        tui.print_logs("pkg2", b"ignored\n")

        stdout.flush()
        assert stdout.buffer.getvalue() == b""

    def test_verbose_tty_no_effect(self):
        """In TTY mode, add_build() does not set tracked_build_id automatically."""
        tui, _, _ = create_tui(is_tty=True, verbose=True, total=4)
        echo_calls = record_echo(tui)

        add_build(tui, "trivial-install-test-package")
        assert tui.tracked_build_id == ""
        assert echo_calls == []


class TestTerminalUIColor:
    """Tests that TerminalUI respects the explicit color=True/False parameter."""

    def test_non_tty_finished_color_true_emits_green(self):
        """color=True in non-TTY mode: finished line has per-component ANSI colors."""
        tui, _, stdout = create_tui(is_tty=False, total=1, color=True)
        add_build(tui, "pkg")
        tui.update_state("pkg", "finished")
        # green indicator, reset, dark-gray hash
        assert stdout.getvalue().startswith("\033[32m[+]\033[0m \033[0;90m")

    def test_non_tty_failed_color_true_emits_red(self):
        """color=True in non-TTY mode: failed line has per-component ANSI colors."""
        tui, _, stdout = create_tui(is_tty=False, total=1, color=True)
        add_build(tui, "pkg")
        tui.update_state("pkg", "failed")
        # red indicator, reset, dark-gray hash
        assert stdout.getvalue().startswith("\033[31m[x]\033[0m \033[0;90m")

    def test_non_tty_finished_color_false_no_ansi(self):
        """color=False in non-TTY mode: finished line has no ANSI escape codes."""
        tui, _, stdout = create_tui(is_tty=False, total=1, color=False)
        add_build(tui, "pkg")
        tui.update_state("pkg", "finished")
        assert "\033[" not in stdout.getvalue()


class TestTargetJobs:
    """Test set_jobs and its effect on the header."""

    def test_set_jobs_marks_dirty(self):
        """set_jobs with a new value should update target_jobs and mark dirty."""
        tui, _, _ = create_tui()
        tui.dirty = False
        tui.set_jobs(3, 2)
        assert tui.actual_jobs == 3
        assert tui.target_jobs == 2
        assert tui.dirty is True
        tui.set_jobs(2, 2)
        assert tui.actual_jobs == 2
        assert tui.target_jobs == 2

    def test_set_jobs_same_value_no_dirty(self):
        """set_jobs with the same value should not mark dirty."""
        tui, _, _ = create_tui()
        tui.set_jobs(5, 5)
        tui.dirty = False
        tui.set_jobs(5, 5)
        assert tui.dirty is False

    def test_header_shows_target_jobs(self):
        """The rendered header should contain the target_jobs count and the word 'jobs'."""
        tui, _, fake_stdout = create_tui(total=1)
        add_mock_builds(tui, 1)
        tui.set_jobs(4, 4)
        tui.render()
        output = fake_stdout.getvalue()
        assert "4" in output
        assert "jobs" in output

    def test_header_shows_arrow_when_pending(self):
        """When actual != target, the header should show 'actual=>target jobs'."""
        tui, _, fake_stdout = create_tui(total=1)
        add_mock_builds(tui, 1)
        tui.set_jobs(4, 2)
        tui.render()
        output = fake_stdout.getvalue()
        assert "4=>2" in output


class TestHeadlessMode:
    """Test that headless mode suppresses terminal output."""

    def test_update_suppressed_when_headless(self):
        """update() should not write anything when headless is True."""
        tui, time_values, stdout = create_tui(is_tty=True, total=1)
        add_mock_builds(tui, 1)
        tui.headless = True
        time_values.append(10.0)
        tui.render()
        assert stdout.getvalue() == ""

    def test_print_logs_suppressed_when_headless(self):
        """print_logs() should discard data when headless is True."""
        tui, _, stdout = create_tui(is_tty=True, total=1)
        build_ids = add_mock_builds(tui, 1)
        tui.tracked_build_id = build_ids[0]
        tui.headless = True
        tui.print_logs(build_ids[0], b"hello world\n")
        assert stdout.getvalue() == ""

    def test_update_state_non_tty_suppressed_when_headless(self):
        """update_state() non-TTY output should be suppressed when headless."""
        tui, _, stdout = create_tui(is_tty=False, total=1)
        add_build(tui, "pkg")
        tui.headless = True
        stdout.clear()
        tui.update_state("pkg", "finished")
        assert stdout.getvalue() == ""

    def test_update_works_after_headless_cleared(self):
        """update() should work normally once headless is cleared."""
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

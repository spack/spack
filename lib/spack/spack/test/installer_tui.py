# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the BuildStatus terminal UI in new_installer.py"""

import io
import os
import sys
from typing import List, Optional, Tuple

import pytest

if sys.platform == "win32":
    pytest.skip("No Windows support", allow_module_level=True)

import spack.new_installer as inst
from spack.new_installer import BuildStatus


class MockConnection:
    """Mock multiprocessing.Connection for testing"""

    def fileno(self):
        return -1


class MockSpec:
    """Minimal mock for spack.spec.Spec"""

    def __init__(
        self, name: str, version: str = "1.0", external: bool = False, prefix: Optional[str] = None
    ) -> None:
        self.name = name
        self.version = version
        self.external = external
        self.prefix = prefix or f"/fake/prefix/{name}"
        self._hash = name  # Simple hash based on name

    def dag_hash(self, length: Optional[int] = None) -> str:
        if length:
            return self._hash[:length]
        return self._hash


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


def create_build_status(
    is_tty: bool = True, terminal_cols: int = 80, terminal_rows: int = 24, total: int = 0
) -> Tuple[BuildStatus, List[float], SimpleTextIOWrapper]:
    """Helper function to create BuildStatus with mocked dependencies"""
    fake_stdout = SimpleTextIOWrapper(tty=is_tty)
    # Easy way to set the current time in tests before running UI updates
    time_values = [0.0]

    def mock_get_time():
        return time_values[-1]

    def mock_get_terminal_size():
        return os.terminal_size((terminal_cols, terminal_rows))

    status = BuildStatus(
        total=total,
        stdout=fake_stdout,
        get_terminal_size=mock_get_terminal_size,
        get_time=mock_get_time,
        is_tty=is_tty,
    )

    return status, time_values, fake_stdout


def add_mock_builds(status: BuildStatus, count: int) -> List[MockSpec]:
    """Helper function to add builds to a BuildStatus instance"""
    specs = [MockSpec(f"pkg{i}", f"{i}.0") for i in range(count)]
    for spec in specs:
        status.add_build(spec, explicit=True, control_w_conn=MockConnection())  # type: ignore
    return specs


class TestBasicStateManagement:
    """Test basic state management operations"""

    def test_add_build(self):
        """Test that add_build adds builds correctly"""
        status, _, _ = create_build_status(total=2)
        spec1 = MockSpec("pkg1", "1.0")
        spec2 = MockSpec("pkg2", "2.0")

        status.add_build(spec1, explicit=True, control_w_conn=MockConnection())
        assert len(status.builds) == 1
        assert spec1.dag_hash() in status.builds
        assert status.builds[spec1.dag_hash()].name == "pkg1"
        assert status.builds[spec1.dag_hash()].explicit is True
        assert status.dirty is True

        status.add_build(spec2, explicit=False, control_w_conn=MockConnection())
        assert len(status.builds) == 2
        assert spec2.dag_hash() in status.builds
        assert status.builds[spec2.dag_hash()].explicit is False

    def test_update_state_transitions(self):
        """Test that update_state transitions states properly"""
        status, fake_time, _ = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Update to 'building' state
        status.update_state(build_id, "building")
        assert status.builds[build_id].state == "building"
        assert status.builds[build_id].progress_percent is None
        assert status.completed == 0

        # Update to 'finished' state
        status.update_state(build_id, "finished")
        assert status.builds[build_id].state == "finished"
        assert status.completed == 1
        assert status.builds[build_id].finished_time == fake_time[0] + inst.CLEANUP_TIMEOUT

    def test_update_state_failed(self):
        """Test that failed state increments completed counter"""
        status, fake_time, _ = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        status.update_state(build_id, "failed")
        assert status.builds[build_id].state == "failed"
        assert status.completed == 1
        assert status.builds[build_id].finished_time == fake_time[0] + inst.CLEANUP_TIMEOUT

    def test_update_progress(self):
        """Test that update_progress updates percentages"""
        status, _, _ = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Update progress
        status.update_progress(build_id, 50, 100)
        assert status.builds[build_id].progress_percent == 50
        assert status.dirty is True

        # Same percentage shouldn't mark dirty again
        status.dirty = False
        status.update_progress(build_id, 50, 100)
        assert status.dirty is False

        # Different percentage should mark dirty
        status.update_progress(build_id, 75, 100)
        assert status.builds[build_id].progress_percent == 75
        assert status.dirty is True

    def test_completion_counter(self):
        """Test that completion counter increments correctly"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        assert status.completed == 0

        status.update_state(specs[0].dag_hash(), "finished")
        assert status.completed == 1

        status.update_state(specs[1].dag_hash(), "failed")
        assert status.completed == 2

        status.update_state(specs[2].dag_hash(), "finished")
        assert status.completed == 3


class TestOutputRendering:
    """Test output rendering for TTY and non-TTY modes"""

    def test_non_tty_output(self):
        """Test that non-TTY mode prints simple state changes"""
        status, _, fake_stdout = create_build_status(is_tty=False)
        spec = MockSpec("mypackage", "1.0")

        status.add_build(spec, explicit=True, control_w_conn=MockConnection())
        build_id = spec.dag_hash()

        status.update_state(build_id, "finished")

        output = fake_stdout.getvalue()
        assert "mypackage" in output
        assert "1.0" in output
        assert "finished" in output
        # Non-TTY output should not contain ANSI escape codes
        assert "\033[" not in output

    def test_tty_output_contains_ansi(self):
        """Test that TTY mode produces ANSI codes"""
        status, _, fake_stdout = create_build_status()
        add_mock_builds(status, 1)

        # Call update to render
        status.update()

        output = fake_stdout.getvalue()
        # Should contain ANSI escape sequences
        assert "\033[" in output
        # Should contain progress header
        assert "Progress:" in output

    def test_no_output_when_not_dirty(self):
        """Test that update() skips rendering when not dirty"""
        status, _, fake_stdout = create_build_status()
        add_mock_builds(status, 1)
        status.update()

        # Clear stdout and mark not dirty
        fake_stdout.clear()
        status.dirty = False

        # Update should not produce output
        status.update()
        assert fake_stdout.getvalue() == ""

    def test_update_throttling(self):
        """Test that update() throttles redraws"""
        status, fake_time, fake_stdout = create_build_status()
        add_mock_builds(status, 1)

        # First update at time 0
        fake_time[0] = 0.0
        status.update()
        first_output = fake_stdout.getvalue()
        assert first_output != ""

        # Mark dirty and try to update immediately
        fake_stdout.clear()
        status.dirty = True
        fake_time[0] = 0.01  # Very small time advance

        # Should be throttled (next_update not reached)
        status.update()
        assert fake_stdout.getvalue() == ""

        # Advance time past throttle and try again
        fake_time[0] = 1.0
        status.update()
        assert fake_stdout.getvalue() != ""

    def test_cursor_movement_vs_newlines(self):
        """Test that finished builds get newlines, active builds get cursor movements"""
        status, fake_time, fake_stdout = create_build_status(total=5)
        specs = add_mock_builds(status, 3)

        # First update renders 3 active builds
        fake_time[0] = 0.0
        status.update()
        output1 = fake_stdout.getvalue()

        # Count newlines (\n) and cursor movements (\033[1E = move down 1 line)
        newlines1 = output1.count("\n")
        cursor_moves1 = output1.count("\033[1E")

        # Initially all lines should be newlines (nothing in history yet)
        assert newlines1 > 0
        assert cursor_moves1 == 0

        # Now finish 2 builds and add 2 more
        fake_stdout.clear()
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.1
        status.update_state(specs[0].dag_hash(), "finished")
        status.update_state(specs[1].dag_hash(), "finished")

        spec4 = MockSpec("pkg3", "3.0")
        spec5 = MockSpec("pkg4", "4.0")
        status.add_build(spec4, explicit=True, control_w_conn=MockConnection())
        status.add_build(spec5, explicit=True, control_w_conn=MockConnection())

        # Second update: finished builds persist (newlines), active area updates (cursor moves)
        status.update()
        output2 = fake_stdout.getvalue()

        newlines2 = output2.count("\n")
        cursor_moves2 = output2.count("\033[1E")

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
        status, fake_time, _ = create_build_status()
        add_mock_builds(status, 1)

        # Initial spinner index
        initial_index = status.spinner_index

        # Advance time past spinner interval
        fake_time[0] = inst.SPINNER_INTERVAL + 0.01
        status.update()

        # Spinner should have advanced
        assert status.spinner_index == (initial_index + 1) % len(status.spinner_chars)

    def test_finished_package_cleanup(self):
        """Test that finished packages are cleaned up after timeout"""
        status, fake_time, _ = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Mark as finished
        fake_time[0] = 0.0
        status.update_state(build_id, "finished")

        # Build should still be in active builds
        assert build_id in status.builds
        assert len(status.finished_builds) == 0

        # Advance time past cleanup timeout
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        status.update()

        # Build should now be moved to finished_builds and removed from active
        assert build_id not in status.builds
        # Note: finished_builds is cleared after rendering, so check it happened via side effects
        assert status.dirty or build_id not in status.builds

    def test_failed_packages_not_cleaned_up(self):
        """Test that failed packages stay in active builds"""
        status, fake_time, _ = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Mark as failed
        fake_time[0] = 0.0
        status.update_state(build_id, "failed")

        # Advance time past cleanup timeout
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        status.update()

        # Failed build should remain in active builds
        assert build_id in status.builds


class TestSearchAndFilter:
    """Test search mode and filtering"""

    def test_enter_search_mode(self):
        """Test that enter_search enables search mode"""
        status, _, _ = create_build_status()
        assert status.search_mode is False

        status.enter_search()
        assert status.search_mode is True
        assert status.dirty is True

    def test_search_input_printable(self):
        """Test that printable characters are added to search term"""
        status, _, _ = create_build_status()
        status.enter_search()

        status.search_input("a")
        assert status.search_term == "a"

        status.search_input("b")
        assert status.search_term == "ab"

        status.search_input("c")
        assert status.search_term == "abc"

    def test_search_input_backspace(self):
        """Test that backspace removes characters"""
        status, _, _ = create_build_status()
        status.enter_search()

        status.search_input("a")
        status.search_input("b")
        status.search_input("c")
        assert status.search_term == "abc"

        status.search_input("\x7f")  # Backspace
        assert status.search_term == "ab"

        status.search_input("\b")  # Alternative backspace
        assert status.search_term == "a"

    def test_search_input_escape(self):
        """Test that escape exits search mode"""
        status, _, _ = create_build_status()
        status.enter_search()
        status.search_input("test")

        status.search_input("\x1b")  # Escape
        assert status.search_mode is False
        assert status.search_term == ""

    def test_is_displayed_filters_by_name(self):
        """Test that _is_displayed filters by package name"""
        status, _, _ = create_build_status(total=3)

        spec1 = MockSpec("package-foo", "1.0")
        spec2 = MockSpec("package-bar", "1.0")
        spec3 = MockSpec("other", "1.0")

        status.add_build(spec1, explicit=True, control_w_conn=MockConnection())
        status.add_build(spec2, explicit=True, control_w_conn=MockConnection())
        status.add_build(spec3, explicit=True, control_w_conn=MockConnection())

        build1 = status.builds[spec1.dag_hash()]
        build2 = status.builds[spec2.dag_hash()]
        build3 = status.builds[spec3.dag_hash()]

        # No search term: all displayed
        status.search_term = ""
        assert status._is_displayed(build1)
        assert status._is_displayed(build2)
        assert status._is_displayed(build3)

        # Search for "package"
        status.search_term = "package"
        assert status._is_displayed(build1)
        assert status._is_displayed(build2)
        assert not status._is_displayed(build3)

        # Search for "foo"
        status.search_term = "foo"
        assert status._is_displayed(build1)
        assert not status._is_displayed(build2)
        assert not status._is_displayed(build3)

    def test_is_displayed_filters_by_hash(self):
        """Test that _is_displayed filters by hash prefix"""
        status, _, _ = create_build_status(total=2)

        spec1 = MockSpec("pkg1", "1.0")
        spec1._hash = "abc123"
        spec2 = MockSpec("pkg2", "1.0")
        spec2._hash = "def456"

        status.add_build(spec1, explicit=True, control_w_conn=MockConnection())
        status.add_build(spec2, explicit=True, control_w_conn=MockConnection())

        build1 = status.builds[spec1.dag_hash()]
        build2 = status.builds[spec2.dag_hash()]

        # Search by hash prefix
        status.search_term = "abc"
        assert status._is_displayed(build1)
        assert not status._is_displayed(build2)

        status.search_term = "def"
        assert not status._is_displayed(build1)
        assert status._is_displayed(build2)


class TestNavigation:
    """Test navigation between builds"""

    def test_get_next_basic(self):
        """Test basic next/previous navigation"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Get first build
        first_id = status._get_next(1)
        assert first_id == specs[0].dag_hash()

        # Set tracked and get next
        status.tracked_build_id = first_id
        next_id = status._get_next(1)
        assert next_id == specs[1].dag_hash()

        # Get next again
        status.tracked_build_id = next_id
        next_id = status._get_next(1)
        assert next_id == specs[2].dag_hash()

        # Wrap around
        status.tracked_build_id = next_id
        next_id = status._get_next(1)
        assert next_id == specs[0].dag_hash()

    def test_get_next_previous(self):
        """Test backward navigation"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Start at second build
        status.tracked_build_id = specs[1].dag_hash()

        # Go backward
        prev_id = status._get_next(-1)
        assert prev_id == specs[0].dag_hash()

        # Go backward again (wrap around)
        status.tracked_build_id = prev_id
        prev_id = status._get_next(-1)
        assert prev_id == specs[2].dag_hash()

    def test_get_next_with_filter(self):
        """Test navigation respects search filter"""
        status, _, _ = create_build_status(total=4)

        specs = [
            MockSpec("package-a", "1.0"),
            MockSpec("package-b", "1.0"),
            MockSpec("other-c", "1.0"),
            MockSpec("package-d", "1.0"),
        ]
        for spec in specs:
            status.add_build(spec, explicit=True, control_w_conn=MockConnection())

        # Filter to only "package-*"
        status.search_term = "package"

        # Should only navigate through matching builds
        first_id = status._get_next(1)
        assert first_id and first_id == specs[0].dag_hash()

        status.tracked_build_id = first_id
        next_id = status._get_next(1)
        assert next_id and next_id == specs[1].dag_hash()

        status.tracked_build_id = next_id
        next_id = status._get_next(1)
        # Should skip "other-c" and go to "package-d"
        assert next_id and next_id == specs[3].dag_hash()

    def test_get_next_skips_finished(self):
        """Test that navigation skips finished builds"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Mark middle build as finished
        status.update_state(specs[1].dag_hash(), "finished")

        # Navigate from first
        status.tracked_build_id = specs[0].dag_hash()
        next_id = status._get_next(1)
        # Should skip finished build and go to third
        assert next_id == specs[2].dag_hash()

    def test_get_next_no_matching(self):
        """Test that _get_next returns None when no builds match"""
        status, _, _ = create_build_status(total=2)
        specs = add_mock_builds(status, 2)

        # Mark both as finished
        for spec in specs:
            status.update_state(spec.dag_hash(), "finished")

        # Should return None since no unfinished builds
        result = status._get_next(1)
        assert result is None

    def test_get_next_fallback_when_tracked_filtered_out(self):
        """Test that _get_next falls back correctly when tracked build no longer matches filter"""
        status, _, _ = create_build_status(total=3)

        specs = [
            MockSpec("package-a", "1.0"),
            MockSpec("package-b", "1.0"),
            MockSpec("other-c", "1.0"),
        ]
        for spec in specs:
            status.add_build(spec, explicit=True, control_w_conn=MockConnection())

        # Start tracking "other-c"
        status.tracked_build_id = specs[2].dag_hash()

        # Now apply a filter that excludes the tracked build
        status.search_term = "package"

        # _get_next should fall back to first matching build (forward)
        next_id = status._get_next(1)
        assert next_id == specs[0].dag_hash()

        # Test backward direction, should fall back to last matching build
        status.tracked_build_id = specs[2].dag_hash()  # Reset to filtered-out build
        prev_id = status._get_next(-1)
        assert prev_id == specs[1].dag_hash()


class TestTerminalSizes:
    """Test behavior with different terminal sizes"""

    def test_small_terminal_truncation(self):
        """Test that output is truncated for small terminals"""
        status, _, fake_stdout = create_build_status(total=10, terminal_cols=80, terminal_rows=10)

        # Add more builds than can fit on screen
        add_mock_builds(status, 10)

        status.update()
        output = fake_stdout.getvalue()

        # Should contain "more..." message indicating truncation
        assert "more..." in output

    def test_large_terminal_no_truncation(self):
        """Test that all builds shown on large terminal"""
        status, _, fake_stdout = create_build_status(total=3, terminal_cols=120)
        add_mock_builds(status, 3)

        status.update()
        output = fake_stdout.getvalue()

        # Should not contain truncation message
        assert "more..." not in output
        # Should contain all package names
        for i in range(3):
            assert f"pkg{i}" in output

    def test_narrow_terminal_short_header(self):
        """Test that narrow terminals get shortened header"""
        status, _, fake_stdout = create_build_status(total=1, terminal_cols=40)
        add_mock_builds(status, 1)

        status.update()
        output = fake_stdout.getvalue()

        # Should not contain the full header with hints
        assert "filter" not in output
        # But should contain progress
        assert "Progress:" in output


class TestBuildInfo:
    """Test the BuildInfo dataclass"""

    def test_build_info_creation(self):
        """Test that BuildInfo is created correctly"""
        spec = MockSpec("mypackage", "1.0")

        build_info = inst.BuildInfo(spec, explicit=True, control_w_conn=MockConnection())

        assert build_info.name == "mypackage"
        assert build_info.version == "1.0"
        assert build_info.explicit is True
        assert build_info.external is False
        assert build_info.state == "starting"
        assert build_info.finished_time is None
        assert build_info.progress_percent is None

    def test_build_info_external_package(self):
        """Test BuildInfo for external package"""
        spec = MockSpec("external-pkg", "1.0", external=True)

        build_info = inst.BuildInfo(spec, explicit=False, control_w_conn=MockConnection())

        assert build_info.external is True


class TestLogFollowing:
    """Test log following and print_logs functionality"""

    def test_print_logs_when_following(self):
        """Test that logs are printed when following a specific build"""
        status, _, fake_stdout = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Switch to log-following mode
        status.overview_mode = False
        status.tracked_build_id = build_id

        # Send some log data
        log_data = b"Building package...\nRunning tests...\n"
        status.print_logs(build_id, log_data)

        # Check that logs were echoed to stdout
        assert fake_stdout._buffer.getvalue() == log_data

    def test_print_logs_discarded_when_in_overview_mode(self):
        """Test that logs are discarded when in overview mode"""
        status, _, fake_stdout = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Stay in overview mode
        assert status.overview_mode is True

        # Try to print logs
        log_data = b"Should not be printed\n"
        status.print_logs(build_id, log_data)

        # Nothing should be printed
        assert fake_stdout.getvalue() == ""

    def test_print_logs_discarded_when_not_tracked(self):
        """Test that logs from non-tracked builds are discarded"""
        status, _, fake_stdout = create_build_status(total=2)
        spec1, spec2 = add_mock_builds(status, 2)

        # Switch to log-following mode for spec1
        status.overview_mode = False
        status.tracked_build_id = spec1.dag_hash()

        # Try to print logs from spec2 (not tracked)
        log_data = b"Logs from pkg2\n"
        status.print_logs(spec2.dag_hash(), log_data)

        # Nothing should be printed since we're tracking pkg1, not pkg2
        assert fake_stdout.getvalue() == ""

    def test_cannot_follow_failed_build(self):
        """Test that navigation skips failed builds"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Mark the middle build as failed
        status.update_state(specs[1].dag_hash(), "failed")

        # The failed build should have finished_time set
        assert status.builds[specs[1].dag_hash()].finished_time is not None

        # Try to get next build, should skip the failed one
        status.tracked_build_id = specs[0].dag_hash()
        next_id = status._get_next(1)

        # Should skip pkg1 (failed) and return pkg2
        assert next_id == specs[2].dag_hash()


class TestNavigationIntegration:
    """Test the next() method and navigation between builds"""

    def test_next_switches_from_overview_to_logs(self):
        """Test that next() switches from overview mode to log-following mode"""
        status, _, fake_stdout = create_build_status(total=2)
        specs = add_mock_builds(status, 2)

        # Start in overview mode
        assert status.overview_mode is True
        assert status.tracked_build_id == ""

        # Call next() to start following first build
        status.next()

        # Should have switched to log-following mode
        assert status.overview_mode is False
        assert status.tracked_build_id == specs[0].dag_hash()

        # Should have printed "Following logs" message
        output = fake_stdout.getvalue()
        assert "Following logs of" in output
        assert "pkg0" in output

    def test_next_cycles_through_builds(self):
        """Test that next() cycles through multiple builds"""
        status, _, fake_stdout = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Start following first build
        status.next()
        assert status.tracked_build_id == specs[0].dag_hash()

        fake_stdout.clear()

        # Navigate to next
        status.next(1)
        assert status.tracked_build_id == specs[1].dag_hash()
        assert "pkg1" in fake_stdout.getvalue()

        fake_stdout.clear()

        # Navigate to next (third build)
        status.next(1)
        assert status.tracked_build_id == specs[2].dag_hash()
        assert "pkg2" in fake_stdout.getvalue()

        fake_stdout.clear()

        # Navigate to next (should wrap to first)
        status.next(1)
        assert status.tracked_build_id == specs[0].dag_hash()
        assert "pkg0" in fake_stdout.getvalue()

    def test_next_backward_navigation(self):
        """Test that next(-1) navigates backward"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Start at first build
        status.next()
        assert status.tracked_build_id == specs[0].dag_hash()

        # Go backward (should wrap to last)
        status.next(-1)
        assert status.tracked_build_id == specs[2].dag_hash()

        # Go backward again
        status.next(-1)
        assert status.tracked_build_id == specs[1].dag_hash()

    def test_next_does_nothing_when_no_builds(self):
        """Test that next() does nothing when no unfinished builds exist"""
        status, _, _ = create_build_status(total=1)
        (spec,) = add_mock_builds(status, 1)

        # Mark as finished
        status.update_state(spec.dag_hash(), "finished")

        # Try to navigate
        initial_mode = status.overview_mode
        initial_tracked = status.tracked_build_id

        status.next()

        # Nothing should change
        assert status.overview_mode == initial_mode
        assert status.tracked_build_id == initial_tracked

    def test_next_does_nothing_when_same_build(self):
        """Test that next() doesn't re-print when already on the same build"""
        status, _, fake_stdout = create_build_status(total=1)
        (spec,) = add_mock_builds(status, 1)

        # Start following
        status.next()
        assert status.tracked_build_id == spec.dag_hash()

        # Clear output
        fake_stdout.clear()

        # Try to navigate to "next" (which is the same build)
        status.next()

        # Should not print anything
        assert fake_stdout.getvalue() == ""


class TestToggle:
    """Test toggle() method for switching between overview and log-following modes"""

    def test_toggle_from_overview_calls_next(self):
        """Test that toggle() from overview mode calls next()"""
        status, _, fake_stdout = create_build_status(total=2)
        add_mock_builds(status, 2)

        # Start in overview mode
        assert status.overview_mode is True

        # Toggle should call next()
        status.toggle()

        # Should now be following logs
        assert status.overview_mode is False
        assert status.tracked_build_id != ""
        assert "Following logs of" in fake_stdout.getvalue()

    def test_toggle_from_logs_returns_to_overview(self):
        """Test that toggle() from log-following mode returns to overview"""
        status, _, _ = create_build_status(total=2)
        add_mock_builds(status, 2)

        # Switch to log-following mode first
        status.next()
        assert status.overview_mode is False
        tracked_id = status.tracked_build_id
        assert tracked_id != ""

        # Set some search state to verify cleanup
        status.search_term = "test"
        status.search_mode = True
        status.active_area_rows = 5

        # Toggle back to overview
        status.toggle()

        # Should be back in overview mode with cleaned state
        assert status.overview_mode is True
        assert status.tracked_build_id == ""
        assert status.search_term == ""
        assert status.search_mode is False
        assert status.active_area_rows == 0
        assert status.dirty is True

    def test_update_state_finished_triggers_toggle_when_tracking(self):
        """Test that finishing a tracked build triggers toggle back to overview"""
        status, _, _ = create_build_status(total=2)
        specs = add_mock_builds(status, 2)

        # Start tracking first build
        status.next()
        assert status.overview_mode is False
        assert status.tracked_build_id == specs[0].dag_hash()

        # Mark the tracked build as finished
        status.update_state(specs[0].dag_hash(), "finished")

        # Should have toggled back to overview mode
        assert status.overview_mode is True
        assert status.tracked_build_id == ""


class TestSearchFilteringIntegration:
    """Test search mode with display filtering"""

    def test_search_mode_filters_displayed_builds(self):
        """Test that search mode actually filters what's displayed"""
        status, _, fake_stdout = create_build_status(total=4)

        specs = [
            MockSpec("package-foo", "1.0"),
            MockSpec("package-bar", "2.0"),
            MockSpec("other-thing", "3.0"),
            MockSpec("package-baz", "4.0"),
        ]
        for spec in specs:
            status.add_build(spec, explicit=True, control_w_conn=MockConnection())

        # Enter search mode and search for "package"
        status.enter_search()
        assert status.search_mode is True

        for character in "package":
            status.search_input(character)

        assert status.search_term == "package"

        # Update to render
        status.update()
        output = fake_stdout.getvalue()

        # Should contain filtered builds
        assert "package-foo" in output
        assert "package-bar" in output
        assert "package-baz" in output
        # Should not contain the filtered-out build
        assert "other-thing" not in output

        # Should show filter prompt
        assert "filter>" in output
        assert status.search_term in output

    def test_search_mode_with_navigation(self):
        """Test that navigation respects search filter"""
        status, _, _ = create_build_status(total=4)

        specs = [
            MockSpec("package-a", "1.0"),
            MockSpec("other-b", "2.0"),
            MockSpec("package-c", "3.0"),
            MockSpec("other-d", "4.0"),
        ]
        for spec in specs:
            status.add_build(spec, explicit=True, control_w_conn=MockConnection())

        # Set search term to filter for "package"
        status.search_term = "package"

        # Start navigating,  should only go through "package-a" and "package-c"
        status.next()
        assert status.tracked_build_id == specs[0].dag_hash()  # package-a

        status.next(1)
        # Should skip other-b and go to package-c
        assert status.tracked_build_id == specs[2].dag_hash()  # package-c

        status.next(1)
        # Should wrap around to package-a
        assert status.tracked_build_id == specs[0].dag_hash()  # package-a

    def test_search_input_enter_navigates_to_next(self):
        """Test that pressing enter in search mode navigates to next match"""
        status, _, _ = create_build_status(total=3)
        specs = add_mock_builds(status, 3)

        # Enter search mode
        status.enter_search()
        for character in "pkg":
            status.search_input(character)

        # Press enter (should navigate to first match)
        status.search_input("\r")

        # Should have started following first matching build
        assert status.overview_mode is False
        assert status.tracked_build_id == specs[0].dag_hash()

    def test_clearing_search_shows_all_builds(self):
        """Test that clearing search term shows all builds again"""
        status, _, fake_stdout = create_build_status(total=3)

        specs = [
            MockSpec("package-a", "1.0"),
            MockSpec("other-b", "2.0"),
            MockSpec("package-c", "3.0"),
        ]
        for spec in specs:
            status.add_build(spec, explicit=True, control_w_conn=MockConnection())

        # Enter search and type something
        status.enter_search()
        status.search_input("p")
        status.search_input("a")
        status.search_input("c")
        assert status.search_term == "pac"

        # Clear it with backspace
        status.search_input("\x7f")  # backspace
        status.search_input("\x7f")  # backspace
        status.search_input("\x7f")  # backspace
        assert status.search_term == ""

        # Update to render
        status.update()
        output = fake_stdout.getvalue()

        # All builds should be visible now
        assert "package-a" in output
        assert "other-b" in output
        assert "package-c" in output


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_build_list(self):
        """Test update with no builds"""
        status, _, fake_stdout = create_build_status(total=0)

        status.update()
        output = fake_stdout.getvalue()

        # Should render header but no builds
        assert "Progress:" in output
        assert "0/0" in output

    def test_all_builds_finished(self):
        """Test when all builds are finished"""
        status, fake_time, _ = create_build_status(total=2)
        specs = add_mock_builds(status, 2)

        # Mark all as finished
        for spec in specs:
            status.update_state(spec.dag_hash(), "finished")

        # Advance time and update
        fake_time[0] = inst.CLEANUP_TIMEOUT + 0.01
        status.update()

        # All should be cleaned up
        assert len(status.builds) == 0
        assert status.completed == 2

    def test_update_progress_rounds_correctly(self):
        """Test that progress percentage rounding works"""
        status, _, _ = create_build_status()
        (spec,) = add_mock_builds(status, 1)
        build_id = spec.dag_hash()

        # Test rounding
        status.update_progress(build_id, 1, 3)
        assert status.builds[build_id].progress_percent == 33  # int(100/3)

        status.update_progress(build_id, 2, 3)
        assert status.builds[build_id].progress_percent == 66  # int(200/3)

        status.update_progress(build_id, 3, 3)
        assert status.builds[build_id].progress_percent == 100

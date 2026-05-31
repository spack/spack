# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for Windows-specific TUI components: ConsoleReader and WindowsTerminalState.

All tests in this module are Windows-only and use unittest.mock to avoid real Win32 API calls.
"""

import selectors
import sys
import time

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

import socket
from ctypes import wintypes
from unittest.mock import MagicMock, patch

import spack.llnl.util.win_io as win_io
from spack.llnl.util.win_io import ConsoleReader
from spack.new_installer import WindowsTerminalState


def _make_socket_pair():
    """Return a (read_sock, write_sock) socket pair both in blocking mode."""
    r, w = socket.socketpair()
    return r, w


def _drain(sock, timeout=0.5):
    """Read all available bytes from a non-blocking socket within a timeout."""
    sock.setblocking(False)
    data = b""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except BlockingIOError:
            time.sleep(0.01)
    return data


class TestConsoleReader:
    """Tests for ConsoleReader — the bridge between Windows console and the selector."""

    def test_resize_event_payload_defined(self):
        assert isinstance(ConsoleReader.RESIZE_EVENT_PAYLOAD, bytes)
        assert len(ConsoleReader.RESIZE_EVENT_PAYLOAD) > 0

    def test_keystroke_forwarded_to_stdin_wsock(self):
        """A keystroke from msvcrt.getch() should appear on stdin_wsock."""
        stdin_r, stdin_w = _make_socket_pair()
        sigwinch_r, sigwinch_w = _make_socket_pair()

        with patch("spack.llnl.util.win_io.msvcrt") as mock_msvcrt:
            # Simulate one keypress
            call_count = [0]

            def kbhit_side_effect():
                call_count[0] += 1
                return call_count[0] == 1  # True only for first call

            mock_msvcrt.kbhit.side_effect = kbhit_side_effect
            mock_msvcrt.getch.return_value = b"v"

            reader = ConsoleReader(stdin_w, sigwinch_w)
            # Give the thread a moment to process the first poll cycle
            time.sleep(0.15)
            reader.close()
            reader.thread.join(timeout=1.0)

        data = _drain(stdin_r)
        assert b"v" in data

        for s in (stdin_r, stdin_w, sigwinch_r, sigwinch_w):
            s.close()

    def test_resize_event_sent_on_size_change(self):
        """A terminal resize should inject RESIZE_EVENT_PAYLOAD on sigwinch_wsock."""
        stdin_r, stdin_w = _make_socket_pair()
        sigwinch_r, sigwinch_w = _make_socket_pair()

        original_size = (80, 24)
        new_size = (100, 30)

        with patch("spack.llnl.util.win_io.msvcrt") as mock_msvcrt, patch(
            "spack.llnl.util.win_io.shutil.get_terminal_size"
        ) as mock_size:
            mock_msvcrt.kbhit.return_value = False
            sizes = iter([original_size, original_size, new_size, new_size])

            def get_size():
                try:
                    w, h = next(sizes)
                    return type("ts", (), {"columns": w, "lines": h})()
                except StopIteration:
                    return type("ts", (), {"columns": new_size[0], "lines": new_size[1]})()

            mock_size.side_effect = get_size

            reader = ConsoleReader(stdin_w, sigwinch_w)
            # Seed the initial size so the first call establishes baseline
            reader._last_size = type(
                "ts", (), {"columns": original_size[0], "lines": original_size[1]}
            )()
            time.sleep(0.15)
            reader.close()
            reader.thread.join(timeout=1.0)

        data = _drain(sigwinch_r)
        assert b"\x00" in data

        for s in (stdin_r, stdin_w, sigwinch_r, sigwinch_w):
            s.close()

    def test_close_stops_thread(self):
        """close() should stop the polling thread cleanly."""
        stdin_r, stdin_w = _make_socket_pair()
        sigwinch_r, sigwinch_w = _make_socket_pair()

        with patch("spack.llnl.util.win_io.msvcrt") as mock_msvcrt, patch(
            "spack.llnl.util.win_io.shutil.get_terminal_size",
            return_value=type("ts", (), {"columns": 80, "lines": 24})(),
        ):
            mock_msvcrt.kbhit.return_value = False
            reader = ConsoleReader(stdin_w, sigwinch_w)
            assert reader.thread.is_alive()
            reader.close()
            reader.thread.join(timeout=1.0)
            assert not reader.thread.is_alive()

        for s in (stdin_r, stdin_w, sigwinch_r, sigwinch_w):
            s.close()

    def test_extended_key_reads_two_bytes(self):
        """Extended keys (e.g. arrow keys) that start with 0x00 or 0xe0 read a second byte."""
        stdin_r, stdin_w = _make_socket_pair()
        sigwinch_r, sigwinch_w = _make_socket_pair()

        with patch("spack.llnl.util.win_io.msvcrt") as mock_msvcrt:
            call_count = [0]

            def kbhit():
                call_count[0] += 1
                return call_count[0] == 1

            mock_msvcrt.kbhit.side_effect = kbhit
            # Simulate an extended key: 0xe0 followed by up-arrow code 0x48
            mock_msvcrt.getch.side_effect = [b"\xe0", b"\x48"]

            reader = ConsoleReader(stdin_w, sigwinch_w)
            time.sleep(0.15)
            reader.close()
            reader.thread.join(timeout=1.0)

        data = _drain(stdin_r)
        assert b"\xe0\x48" in data

        for s in (stdin_r, stdin_w, sigwinch_r, sigwinch_w):
            s.close()


def _make_mock_selector():
    """Return a MagicMock that behaves like a BaseSelector for registration tracking."""
    sel = MagicMock(spec=selectors.BaseSelector)
    registered = {}

    def register(fileobj, events, data=None):
        fd = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        registered[fd] = (fileobj, events, data)
        key = MagicMock()
        key.fd = fd
        key.fileobj = fileobj
        key.data = data
        return key

    def unregister(fileobj):
        fd = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        if fd in registered:
            del registered[fd]

    def get_map():
        return registered

    sel.register.side_effect = register
    sel.unregister.side_effect = unregister
    sel.get_map.side_effect = get_map
    return sel


def _make_mock_build_status():
    bs = MagicMock()
    bs.headless = True
    bs.dirty = False
    return bs


class TestWindowsTerminalState:
    """Tests for WindowsTerminalState — console mode management and socket lifecycle."""

    def _make_state(self, selector=None, build_status=None):
        sel = selector or _make_mock_selector()
        bs = build_status or _make_mock_build_status()

        stdin_mode = wintypes.DWORD(0x0007)

        with patch.object(win_io, "GetStdHandle", return_value=MagicMock()), patch.object(
            win_io, "GetConsoleMode"
        ) as mock_get_mode, patch.object(win_io, "SetConsoleMode"):
            # Populate old_*_settings DWORDs via the mock
            def _get_mode(handle, dword_ptr):
                dword_ptr._obj.value = stdin_mode.value

            mock_get_mode.side_effect = _get_mode
            state = WindowsTerminalState(sel, bs)

        return state, sel, bs

    def test_setup_enables_vt100_on_stdout(self):
        """setup() should call SetConsoleMode with the VT100 flag ORed in."""
        state, sel, bs = self._make_state()

        with patch.object(win_io, "SetConsoleMode") as mock_set, patch.object(
            win_io, "GetConsoleMode"
        ):
            state.setup()

        # At least one SetConsoleMode call should include ENABLE_VIRTUAL_TERMINAL_PROCESSING
        vt_flag = win_io.ENABLE_VIRTUAL_TERMINAL_PROCESSING
        assert any((args[1] & vt_flag) == vt_flag for args, _ in mock_set.call_args_list), (
            "VT100 flag was not set during setup()"
        )

    def test_setup_registers_sigwinch_socket(self):
        """setup() should register sigwinch_r in the selector."""
        state, sel, bs = self._make_state()

        with patch.object(win_io, "SetConsoleMode"), patch.object(win_io, "GetConsoleMode"):
            state.setup()

        registered_data = [call_args[0][2] for call_args in sel.register.call_args_list]
        assert "sigwinch" in registered_data

    def test_teardown_restores_console_mode_value(self):
        """teardown() must pass .value (int), not the DWORD struct, to SetConsoleMode."""
        state, sel, bs = self._make_state()

        calls = []
        with patch.object(win_io, "SetConsoleMode", side_effect=lambda h, v: calls.append(v)):
            state.teardown()

        # All mode arguments should be plain integers, not ctypes instances
        for v in calls:
            assert isinstance(v, int), f"SetConsoleMode got non-int argument: {type(v)}"

    def test_enter_foreground_registers_stdin_and_starts_reader(self):
        """enter_foreground() should register stdin_r and create a ConsoleReader."""
        state, sel, bs = self._make_state()
        bs.headless = True

        with patch.object(win_io, "GetConsoleMode"), patch.object(win_io, "SetConsoleMode"), patch(
            "spack.llnl.util.win_io.ConsoleReader"
        ) as MockReader, patch.object(sys.stdin, "isatty", return_value=True):
            state.enter_foreground()

        # stdin_r should have been registered
        registered_data = [call_args[0][2] for call_args in sel.register.call_args_list]
        assert "stdin" in registered_data

        # ConsoleReader should have been instantiated
        MockReader.assert_called_once()
        assert bs.headless is False

    def test_enter_foreground_noop_when_already_foreground(self):
        """enter_foreground() should do nothing if headless is already False."""
        state, sel, bs = self._make_state()
        bs.headless = False

        with patch.object(win_io, "SetConsoleMode") as mock_set:
            state.enter_foreground()

        mock_set.assert_not_called()

    def test_enter_background_stops_reader(self):
        """enter_background() should stop ConsoleReader and mark headless=True."""
        state, sel, bs = self._make_state()
        mock_reader = MagicMock()
        state.console_reader = mock_reader
        bs.headless = False

        state.enter_background()

        mock_reader.close.assert_called_once()
        assert state.console_reader is None
        assert bs.headless is True

    def test_teardown_closes_sockets(self):
        """teardown() should close stdin_r and sigwinch_r sockets."""
        state, sel, bs = self._make_state()

        stdin_r_mock = MagicMock(spec=socket.socket)
        stdin_r_mock.fileno.return_value = -1
        sigwinch_r_mock = MagicMock(spec=socket.socket)
        sigwinch_r_mock.fileno.return_value = -2

        state.stdin_r = stdin_r_mock
        state.sigwinch_r = sigwinch_r_mock

        with patch.object(win_io, "SetConsoleMode"):
            state.teardown()

        stdin_r_mock.close.assert_called_once()
        sigwinch_r_mock.close.assert_called_once()

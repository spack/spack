# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for Windows-specific TUI components in new_installer.py.

WindowsTerminalState uses two daemon threads (_input_thread, _resize_thread) and
a pair of socketpairs (stdin_r/w, sigwinch_r/w) to bridge Win32 console events
into the selector-based event loop.  All tests here use unittest.mock so that
no real Win32 API calls are required.
"""

import selectors
import socket
import sys
import threading
import time
from unittest.mock import MagicMock, patch

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

from ctypes import wintypes

from spack.new_installer import (
    ENABLE_ECHO_INPUT,
    ENABLE_EXTENDED_FLAGS,
    ENABLE_LINE_INPUT,
    ENABLE_QUICK_EDIT_MODE,
    ENABLE_VIRTUAL_TERMINAL_PROCESSING,
    WindowsTerminalState,
)


def _drain(sock, timeout=0.5):
    """Read all available bytes from a socket within *timeout* seconds."""
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


def _make_mock_selector():
    sel = MagicMock(spec=selectors.BaseSelector)
    _reg = {}

    def _register(fileobj, events, data=None):
        key = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        _reg[key] = (fileobj, events, data)
        k = MagicMock()
        k.fd = key
        k.fileobj = fileobj
        k.data = data
        return k

    def _unregister(fileobj):
        key = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        _reg.pop(key, None)

    sel.register.side_effect = _register
    sel.unregister.side_effect = _unregister
    sel.get_map.side_effect = lambda: _reg
    return sel


def _make_mock_build_status(headless=True):
    bs = MagicMock()
    bs.headless = headless
    bs.dirty = False
    return bs


def _make_state(headless=True):
    """Create a WindowsTerminalState bypassing __init__ to avoid real Win32 calls.

    All kernel32 calls go through a MagicMock; real socket pairs are created so
    that thread tests can send/receive actual bytes.
    """
    sel = _make_mock_selector()
    bs = _make_mock_build_status(headless=headless)
    mock_k32 = MagicMock()
    mock_k32.GetStdHandle.return_value = MagicMock()
    mock_k32.GetConsoleMode.return_value = True
    mock_k32.SetConsoleMode.return_value = True

    state = object.__new__(WindowsTerminalState)
    state.selector = sel
    state.build_status = bs
    state.on_suspend = None
    state.on_resume = None
    state.kernel32 = mock_k32
    state.hStdin = MagicMock()
    state.hStdout = MagicMock()
    # ENABLE_PROCESSED_INPUT | ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT
    state.old_stdin_settings = wintypes.DWORD(0x0007)
    state.old_stdout_settings = wintypes.DWORD(0x0003)
    state.stdin_r, state.stdin_w = socket.socketpair()
    state.stdin_r.setblocking(False)
    state.sigwinch_r, state.sigwinch_w = socket.socketpair()
    state.sigwinch_r.setblocking(False)
    state._running = False
    return state, sel, bs, mock_k32


class TestSetupTeardown:
    def test_setup_enables_vt100_on_stdout(self):
        """setup() ORs ENABLE_VIRTUAL_TERMINAL_PROCESSING into the stdout console mode."""
        state, sel, bs, k32 = _make_state()

        with patch("spack.new_installer.threading.Thread"), patch.object(
            state, "enter_foreground"
        ):
            state.setup()

        vt_flag = ENABLE_VIRTUAL_TERMINAL_PROCESSING
        vt_calls = [
            args[1]
            for args, _ in k32.SetConsoleMode.call_args_list
            if args and isinstance(args[1], int) and (args[1] & vt_flag)
        ]
        assert vt_calls, "VT100 flag not set in any SetConsoleMode call during setup()"

    def test_setup_registers_sigwinch_socket(self):
        """setup() registers sigwinch_r in the selector with tag 'sigwinch'."""
        state, sel, bs, k32 = _make_state()

        with patch("spack.new_installer.threading.Thread"), patch.object(
            state, "enter_foreground"
        ):
            state.setup()

        tags = [call_args[0][2] for call_args in sel.register.call_args_list]
        assert "sigwinch" in tags

    def test_setup_starts_two_daemon_threads(self):
        """setup() starts exactly two daemon threads."""
        state, sel, bs, k32 = _make_state()
        threads = []

        class _FakeThread:
            def __init__(self, target, daemon):
                threads.append(self)
                self.daemon = daemon

            def start(self):
                pass

        with patch("spack.new_installer.threading.Thread", _FakeThread), patch.object(
            state, "enter_foreground"
        ):
            state.setup()

        assert len(threads) == 2
        assert all(t.daemon for t in threads)

    def test_teardown_restores_console_mode_with_int_values(self):
        """teardown() passes plain ints (not DWORD structs) to SetConsoleMode."""
        state, sel, bs, k32 = _make_state()
        captured = []
        k32.SetConsoleMode.side_effect = lambda h, v: captured.append(v)

        state.teardown()

        assert captured, "SetConsoleMode not called during teardown()"
        for v in captured:
            assert isinstance(v, int), f"Expected int, got {type(v)}: {v!r}"

    def test_teardown_closes_stdin_and_sigwinch_sockets(self):
        """teardown() closes stdin_r and sigwinch_r."""
        state, sel, bs, k32 = _make_state()
        stdin_mock = MagicMock(spec=socket.socket)
        stdin_mock.fileno.return_value = 99
        sigwinch_mock = MagicMock(spec=socket.socket)
        sigwinch_mock.fileno.return_value = 100
        state.stdin_r = stdin_mock
        state.sigwinch_r = sigwinch_mock
        sel.get_map.side_effect = lambda: {}

        state.teardown()

        stdin_mock.close.assert_called_once()
        sigwinch_mock.close.assert_called_once()

    def test_teardown_sets_running_false(self):
        """teardown() sets _running=False to stop background threads."""
        state, sel, bs, k32 = _make_state()
        state._running = True

        state.teardown()

        assert not state._running


class TestForegroundBackground:
    def test_enter_foreground_noop_when_already_foreground(self):
        """enter_foreground() is a no-op when headless is already False."""
        state, sel, bs, k32 = _make_state(headless=False)

        state.enter_foreground()

        k32.SetConsoleMode.assert_not_called()

    def test_enter_foreground_disables_line_echo_quickedit(self):
        """enter_foreground() clears LINE_INPUT, ECHO_INPUT, QUICK_EDIT_MODE."""
        state, sel, bs, k32 = _make_state(headless=True)

        with patch.object(WindowsTerminalState, "stdin_is_interactive", return_value=True):
            state.enter_foreground()

        set_calls = k32.SetConsoleMode.call_args_list
        assert set_calls, "SetConsoleMode not called"
        new_mode = set_calls[0][0][1]
        disable = ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_QUICK_EDIT_MODE
        assert (new_mode & disable) == 0, f"Disabled flags still set: {new_mode:#010x}"
        assert new_mode & ENABLE_EXTENDED_FLAGS, "ENABLE_EXTENDED_FLAGS not set"

    def test_enter_foreground_registers_stdin_when_interactive(self):
        """enter_foreground() registers stdin_r with tag 'stdin' when interactive."""
        state, sel, bs, k32 = _make_state(headless=True)

        with patch.object(WindowsTerminalState, "stdin_is_interactive", return_value=True):
            state.enter_foreground()

        tags = [c[0][2] for c in sel.register.call_args_list]
        assert "stdin" in tags
        assert bs.headless is False

    def test_enter_foreground_skips_stdin_when_not_interactive(self):
        """enter_foreground() does not register stdin_r when not interactive."""
        state, sel, bs, k32 = _make_state(headless=True)

        with patch.object(WindowsTerminalState, "stdin_is_interactive", return_value=False):
            state.enter_foreground()

        tags = [c[0][2] for c in sel.register.call_args_list]
        assert "stdin" not in tags

    def test_enter_background_unregisters_stdin_and_sets_headless(self):
        """enter_background() unregisters stdin_r and sets headless=True."""
        state, sel, bs, k32 = _make_state(headless=False)
        sel.get_map.side_effect = lambda: {state.stdin_r.fileno(): object()}

        state.enter_background()

        sel.unregister.assert_called()
        assert bs.headless is True


class TestInputThread:
    """Tests for WindowsTerminalState._input_thread."""

    def _run_thread(self, state, mock_msvcrt, *, timeout=0.5):
        """Run _input_thread in a daemon thread and return bytes received on stdin_r."""
        state._running = True
        state.build_status.headless = False
        with patch("spack.new_installer.msvcrt", mock_msvcrt):
            t = threading.Thread(target=state._input_thread, daemon=True)
            t.start()
            t.join(timeout=timeout)
        return _drain(state.stdin_r)

    def test_keystroke_forwarded_to_stdin_r(self):
        """A normal keypress is sent to stdin_r."""
        state, sel, bs, k32 = _make_state()
        call_count = [0]
        mock_msvcrt = MagicMock()

        def kbhit():
            call_count[0] += 1
            if call_count[0] == 1:
                return True
            state._running = False
            return False

        mock_msvcrt.kbhit.side_effect = kbhit
        mock_msvcrt.getwch.return_value = "v"

        data = self._run_thread(state, mock_msvcrt)
        assert b"v" in data

    def test_extended_key_e0_reads_two_bytes(self):
        """The 0xe0 prefix (arrow/nav keys) triggers a second getwch() call."""
        state, sel, bs, k32 = _make_state()
        call_count = [0]
        mock_msvcrt = MagicMock()

        def kbhit():
            call_count[0] += 1
            if call_count[0] == 1:
                return True
            state._running = False
            return False

        mock_msvcrt.kbhit.side_effect = kbhit
        mock_msvcrt.getwch.side_effect = ["\xe0", "H"]  # up-arrow

        data = self._run_thread(state, mock_msvcrt)
        assert "\xe0H".encode("utf-8") in data

    def test_extended_key_null_reads_two_bytes(self):
        """The 0x00 prefix (F-keys) triggers a second getwch() call."""
        state, sel, bs, k32 = _make_state()
        call_count = [0]
        mock_msvcrt = MagicMock()

        def kbhit():
            call_count[0] += 1
            if call_count[0] == 1:
                return True
            state._running = False
            return False

        mock_msvcrt.kbhit.side_effect = kbhit
        mock_msvcrt.getwch.side_effect = ["\x00", "K"]  # left-arrow via null prefix

        data = self._run_thread(state, mock_msvcrt)
        assert b"\x00K" in data

    def test_no_keypress_when_headless(self):
        """_input_thread does not call kbhit when headless=True."""
        state, sel, bs, k32 = _make_state()
        state.build_status.headless = True
        mock_msvcrt = MagicMock()
        mock_msvcrt.kbhit.return_value = False

        state._running = True

        def stop():
            time.sleep(0.15)
            state._running = False

        threading.Thread(target=stop, daemon=True).start()
        with patch("spack.new_installer.msvcrt", mock_msvcrt):
            state._input_thread()

        mock_msvcrt.kbhit.assert_not_called()


class TestResizeThread:
    """Tests for WindowsTerminalState._resize_thread."""

    def test_resize_event_sent_on_size_change(self):
        """_resize_thread sends b'\\x00' to sigwinch_w when terminal dimensions change."""
        import os

        state, sel, bs, k32 = _make_state()
        state._running = True
        call_count = [0]
        sizes = [
            os.terminal_size((80, 24)),
            os.terminal_size((80, 24)),
            os.terminal_size((100, 30)),
        ]

        def get_size():
            idx = call_count[0]
            call_count[0] += 1
            if idx >= len(sizes):
                state._running = False
                return sizes[-1]
            return sizes[idx]

        with patch("spack.new_installer.shutil.get_terminal_size", side_effect=get_size):
            state._resize_thread()

        data = _drain(state.sigwinch_r)
        assert b"\x00" in data

    def test_no_resize_event_on_same_size(self):
        """_resize_thread does not send if dimensions are unchanged."""
        import os

        state, sel, bs, k32 = _make_state()
        state._running = True
        call_count = [0]

        def get_size():
            call_count[0] += 1
            if call_count[0] > 4:
                state._running = False
            return os.terminal_size((80, 24))

        with patch("spack.new_installer.shutil.get_terminal_size", side_effect=get_size):
            state._resize_thread()

        data = _drain(state.sigwinch_r)
        assert data == b""

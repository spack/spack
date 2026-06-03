# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for Windows-specific TUI components in new_installer.py.

WindowsTerminalState uses two daemon threads (_input_thread, _resize_thread) and
a pair of socketpairs (stdin_r/w, sigwinch_r/w) to bridge Win32 console events
into the selector-based event loop.  All tests here use pytest's monkeypatch and
plain fake objects so that no real Win32 API calls are required.
"""

import os
import selectors
import shutil
import socket
import sys
import threading
import time
import types

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

from ctypes import wintypes

import spack.new_installer as _ni
from spack.new_installer import (
    ENABLE_ECHO_INPUT,
    ENABLE_EXTENDED_FLAGS,
    ENABLE_LINE_INPUT,
    ENABLE_QUICK_EDIT_MODE,
    ENABLE_VIRTUAL_TERMINAL_PROCESSING,
    StdinReader,
    WindowsTerminalState,
)


class _FakeSelector:
    """Selector that records register/unregister calls without OS involvement."""

    def __init__(self):
        self._reg = {}
        self.register_calls = []  # [(fileobj, events, data), ...]
        self.unregister_calls = []  # [fileobj, ...]

    def register(self, fileobj, events, data=None):
        key = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        self._reg[key] = (fileobj, events, data)
        self.register_calls.append((fileobj, events, data))

    def unregister(self, fileobj):
        key = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        self._reg.pop(key, None)
        self.unregister_calls.append(fileobj)

    def get_map(self):
        return self._reg


class _FakeKernel32:
    """Minimal kernel32 stand-in that records SetConsoleMode calls."""

    def __init__(self):
        self.set_console_mode_calls = []  # [(handle, value), ...]

    def GetStdHandle(self, handle_id):
        return object()

    def GetConsoleMode(self, handle, byref_mode):
        return True

    def SetConsoleMode(self, handle, mode):
        self.set_console_mode_calls.append((handle, mode))
        return True


class _FakeSocket:
    """Socket stand-in that counts close() calls."""

    def __init__(self, fd):
        self._fd = fd
        self.close_count = 0

    def fileno(self):
        return self._fd

    def close(self):
        self.close_count += 1


class _NoopThread:
    """Thread replacement that records daemon flag but never starts a real thread."""

    def __init__(self, target=None, daemon=None):
        self.daemon = daemon

    def start(self):
        pass


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


def _make_state(headless=True):
    """Create a WindowsTerminalState bypassing __init__ to avoid real Win32 calls.

    All kernel32 calls go through _FakeKernel32; real socket pairs are created so
    that thread tests can send/receive actual bytes.
    """
    sel = _FakeSelector()
    bs = types.SimpleNamespace(headless=headless, dirty=False)
    k32 = _FakeKernel32()

    state = object.__new__(WindowsTerminalState)
    state.selector = sel
    state.build_status = bs
    state.on_suspend = None
    state.on_resume = None
    state.kernel32 = k32
    state.hStdin = object()
    state.hStdout = object()
    # ENABLE_PROCESSED_INPUT | ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT
    state.old_stdin_settings = wintypes.DWORD(0x0007)
    state.old_stdout_settings = wintypes.DWORD(0x0003)
    state.stdin_r, state.stdin_w = socket.socketpair()
    state.stdin_r.setblocking(False)
    state.sigwinch_r, state.sigwinch_w = socket.socketpair()
    state.sigwinch_r.setblocking(False)
    state._running = False
    return state, sel, bs, k32


class TestSetupTeardown:
    def test_setup_enables_vt100_on_stdout(self, monkeypatch):
        """setup() ORs ENABLE_VIRTUAL_TERMINAL_PROCESSING into the stdout console mode."""
        state, sel, bs, k32 = _make_state()
        monkeypatch.setattr(_ni.threading, "Thread", _NoopThread)
        monkeypatch.setattr(state, "enter_foreground", lambda: None)

        state.setup()

        vt_flag = ENABLE_VIRTUAL_TERMINAL_PROCESSING
        vt_calls = [v for _, v in k32.set_console_mode_calls if v & vt_flag]
        assert vt_calls, "VT100 flag not set in any SetConsoleMode call during setup()"

    def test_setup_registers_sigwinch_socket(self, monkeypatch):
        """setup() registers sigwinch_r in the selector with tag 'sigwinch'."""
        state, sel, bs, k32 = _make_state()
        monkeypatch.setattr(_ni.threading, "Thread", _NoopThread)
        monkeypatch.setattr(state, "enter_foreground", lambda: None)

        state.setup()

        tags = [data for _, _, data in sel.register_calls]
        assert "sigwinch" in tags

    def test_setup_starts_two_daemon_threads(self, monkeypatch):
        """setup() starts exactly two daemon threads."""
        state, sel, bs, k32 = _make_state()
        threads = []

        class _FakeThread:
            def __init__(self, target, daemon):
                threads.append(self)
                self.daemon = daemon

            def start(self):
                pass

        monkeypatch.setattr(_ni.threading, "Thread", _FakeThread)
        monkeypatch.setattr(state, "enter_foreground", lambda: None)

        state.setup()

        assert len(threads) == 2
        assert all(t.daemon for t in threads)

    def test_teardown_restores_console_mode_with_int_values(self):
        """teardown() passes plain ints (not DWORD structs) to SetConsoleMode."""
        state, sel, bs, k32 = _make_state()

        state.teardown()

        assert k32.set_console_mode_calls, "SetConsoleMode not called during teardown()"
        for _, v in k32.set_console_mode_calls:
            assert isinstance(v, int), f"Expected int, got {type(v)}: {v!r}"

    def test_teardown_closes_stdin_and_sigwinch_sockets(self):
        """teardown() closes stdin_r and sigwinch_r."""
        state, sel, bs, k32 = _make_state()
        stdin_fake = _FakeSocket(99)
        sigwinch_fake = _FakeSocket(100)
        state.stdin_r = stdin_fake
        state.sigwinch_r = sigwinch_fake

        state.teardown()

        assert stdin_fake.close_count == 1
        assert sigwinch_fake.close_count == 1

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

        assert not k32.set_console_mode_calls

    def test_enter_foreground_disables_line_echo_quickedit(self, monkeypatch):
        """enter_foreground() clears LINE_INPUT, ECHO_INPUT, QUICK_EDIT_MODE."""
        state, sel, bs, k32 = _make_state(headless=True)
        monkeypatch.setattr(
            WindowsTerminalState, "stdin_is_interactive", staticmethod(lambda: True)
        )

        state.enter_foreground()

        assert k32.set_console_mode_calls, "SetConsoleMode not called"
        new_mode = k32.set_console_mode_calls[0][1]
        disable = ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_QUICK_EDIT_MODE
        assert (new_mode & disable) == 0, f"Disabled flags still set: {new_mode:#010x}"
        assert new_mode & ENABLE_EXTENDED_FLAGS, "ENABLE_EXTENDED_FLAGS not set"

    def test_enter_foreground_registers_stdin_when_interactive(self, monkeypatch):
        """enter_foreground() registers stdin_r with tag 'stdin' when interactive."""
        state, sel, bs, k32 = _make_state(headless=True)
        monkeypatch.setattr(
            WindowsTerminalState, "stdin_is_interactive", staticmethod(lambda: True)
        )

        state.enter_foreground()

        tags = [data for _, _, data in sel.register_calls]
        assert "stdin" in tags
        assert bs.headless is False

    def test_enter_foreground_skips_stdin_when_not_interactive(self, monkeypatch):
        """enter_foreground() does not register stdin_r when not interactive."""
        state, sel, bs, k32 = _make_state(headless=True)
        monkeypatch.setattr(
            WindowsTerminalState, "stdin_is_interactive", staticmethod(lambda: False)
        )

        state.enter_foreground()

        tags = [data for _, _, data in sel.register_calls]
        assert "stdin" not in tags

    def test_enter_background_unregisters_stdin_and_sets_headless(self):
        """enter_background() unregisters stdin_r and sets headless=True."""
        state, sel, bs, k32 = _make_state(headless=False)
        sel._reg[state.stdin_r.fileno()] = (state.stdin_r, selectors.EVENT_READ, "stdin")

        state.enter_background()

        assert sel.unregister_calls
        assert bs.headless is True


class TestInputThread:
    """Tests for WindowsTerminalState._input_thread."""

    def _run_thread(self, state, fake_msvcrt, monkeypatch, *, timeout=0.5):
        """Run _input_thread in a daemon thread and return bytes received on stdin_r."""
        state._running = True
        state.build_status.headless = False
        monkeypatch.setattr(_ni, "msvcrt", fake_msvcrt)
        t = threading.Thread(target=state._input_thread, daemon=True)
        t.start()
        t.join(timeout=timeout)
        return _drain(state.stdin_r)

    def test_keystroke_forwarded_to_stdin_r(self, monkeypatch):
        """A normal keypress is sent to stdin_r."""
        state, sel, bs, k32 = _make_state()
        call_count = [0]

        def kbhit():
            call_count[0] += 1
            if call_count[0] == 1:
                return True
            state._running = False
            return False

        fake_msvcrt = types.SimpleNamespace(kbhit=kbhit, getwch=lambda: "v")

        data = self._run_thread(state, fake_msvcrt, monkeypatch)
        assert b"v" in data

    def test_extended_key_e0_reads_two_bytes_and_discards(self, monkeypatch):
        """The 0xe0 prefix (arrow/nav keys) reads a second byte but discards both."""
        state, sel, bs, k32 = _make_state()
        call_count = [0]
        getwch_results = ["\xe0", "H"]
        getwch_calls = [0]

        def kbhit():
            call_count[0] += 1
            if call_count[0] == 1:
                return True
            state._running = False
            return False

        def getwch():
            v = getwch_results[getwch_calls[0]]
            getwch_calls[0] += 1
            return v

        fake_msvcrt = types.SimpleNamespace(kbhit=kbhit, getwch=getwch)

        data = self._run_thread(state, fake_msvcrt, monkeypatch)
        assert getwch_calls[0] == 2
        assert data == b""

    def test_extended_key_null_reads_two_bytes_and_discards(self, monkeypatch):
        """The 0x00 prefix (F-keys) reads a second byte but discards both."""
        state, sel, bs, k32 = _make_state()
        call_count = [0]
        getwch_results = ["\x00", "K"]
        getwch_calls = [0]

        def kbhit():
            call_count[0] += 1
            if call_count[0] == 1:
                return True
            state._running = False
            return False

        def getwch():
            v = getwch_results[getwch_calls[0]]
            getwch_calls[0] += 1
            return v

        fake_msvcrt = types.SimpleNamespace(kbhit=kbhit, getwch=getwch)

        data = self._run_thread(state, fake_msvcrt, monkeypatch)
        assert getwch_calls[0] == 2
        assert data == b""

    def test_no_keypress_when_headless(self, monkeypatch):
        """_input_thread does not call kbhit when headless=True."""
        state, sel, bs, k32 = _make_state()
        state.build_status.headless = True
        kbhit_calls = []

        def kbhit():
            kbhit_calls.append(None)
            return False

        fake_msvcrt = types.SimpleNamespace(kbhit=kbhit, getwch=lambda: "")

        state._running = True

        def stop():
            time.sleep(0.15)
            state._running = False

        threading.Thread(target=stop, daemon=True).start()
        monkeypatch.setattr(_ni, "msvcrt", fake_msvcrt)
        state._input_thread()

        assert not kbhit_calls


class TestResizeThread:
    """Tests for WindowsTerminalState._resize_thread."""

    def test_resize_event_sent_on_size_change(self, monkeypatch):
        """_resize_thread sends b'\\x00' to sigwinch_w when terminal dimensions change."""
        state, sel, bs, k32 = _make_state()
        state._running = True
        call_count = [0]
        sizes = [
            os.terminal_size((80, 24)),
            os.terminal_size((80, 24)),
            os.terminal_size((100, 30)),
        ]

        def get_size(**_kwargs):
            idx = call_count[0]
            call_count[0] += 1
            if idx >= len(sizes):
                state._running = False
                return sizes[-1]
            return sizes[idx]

        monkeypatch.setattr(shutil, "get_terminal_size", get_size)
        state._resize_thread()

        data = _drain(state.sigwinch_r)
        assert b"\x00" in data

    def test_no_resize_event_on_same_size(self, monkeypatch):
        """_resize_thread does not send if dimensions are unchanged."""
        state, sel, bs, k32 = _make_state()
        state._running = True
        call_count = [0]

        def get_size(**_kwargs):
            call_count[0] += 1
            if call_count[0] > 4:
                state._running = False
            return os.terminal_size((80, 24))

        monkeypatch.setattr(shutil, "get_terminal_size", get_size)
        state._resize_thread()

        data = _drain(state.sigwinch_r)
        assert data == b""


class TestStdinReaderSocketPath:
    """Tests for StdinReader when constructed with a socket (Windows path)."""

    def _make_reader(self):
        r, w = socket.socketpair()
        # Keep blocking so recv() returns data immediately, mirroring production behaviour
        # where read() is only called after the selector has already signalled data ready.
        reader = StdinReader(r.fileno(), sock=r)
        return reader, r, w

    def test_basic_ascii_via_socket(self):
        """Bytes sent through the socket are decoded and returned."""
        reader, r, w = self._make_reader()
        try:
            w.sendall(b"hello")
            assert reader.read() == "hello"
        finally:
            r.close()
            w.close()

    def test_ansi_stripping_via_socket(self):
        """ANSI escape sequences are stripped when reading from the socket."""
        reader, r, w = self._make_reader()
        try:
            w.sendall(b"go\x1b[Aup\x1b[B!")
            assert reader.read() == "goup!"
        finally:
            r.close()
            w.close()

    def test_multibyte_utf8_via_socket(self):
        """Multi-byte UTF-8 characters split across two recvs are reassembled correctly."""
        reader, r, w = self._make_reader()
        try:
            encoded = "é".encode("utf-8")  # 0xc3 0xa9
            w.sendall(encoded[:1])
            result1 = reader.read()
            w.sendall(encoded[1:])
            result2 = reader.read()
            assert result1 + result2 == "é"
        finally:
            r.close()
            w.close()

    def test_oserror_returns_empty_via_socket(self):
        """A closed socket raises OSError on recv(); read() returns '' rather than propagating."""
        reader, r, w = self._make_reader()
        r.close()
        w.close()
        assert reader.read() == ""

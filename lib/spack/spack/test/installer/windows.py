# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for Windows-specific TUI components and the jobserver in installer.windows.

WindowsTerminalState uses two daemon threads (_input_thread, _resize_thread) and
a pair of socketpairs (stdin_r/w, sigwinch_r/w) to bridge Win32 console events
into the selector-based event loop.  The terminal-state tests here use pytest's
monkeypatch and plain fake objects so that no real Win32 API calls are required.

The WindowsJobServer tests do exercise real Win32 named semaphores, since the
token accounting is only meaningful against the actual kernel object.
"""

import functools
import os
import shutil
import socket
import sys
import types

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

from ctypes import wintypes

import spack.installer.windows as _niw
from spack.installer.base import StdinReader
from spack.installer.windows import (
    ENABLE_ECHO_INPUT,
    ENABLE_EXTENDED_FLAGS,
    ENABLE_LINE_INPUT,
    ENABLE_QUICK_EDIT_MODE,
    ENABLE_VIRTUAL_TERMINAL_PROCESSING,
    WAIT_OBJECT_0,
    WindowsJobServer,
    WindowsTerminalState,
    get_jobserver_semaphore_name,
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


class _FakePipe:
    """In-process unidirectional byte pipe.

    sendall() on one end places bytes directly into the peer's buffer; recv() on the
    other end returns them immediately or raises BlockingIOError if the buffer is empty.
    """

    def __init__(self, fd: int) -> None:
        self._fd = fd
        self._buf = bytearray()
        self._peer: "_FakePipe"

    def fileno(self) -> int:
        return self._fd

    def sendall(self, data: bytes) -> None:
        self._peer._buf.extend(data)

    def recv(self, n: int) -> bytes:
        if not self._buf:
            raise BlockingIOError
        chunk, self._buf = bytes(self._buf[:n]), self._buf[n:]
        return chunk

    def setblocking(self, flag: bool) -> None:
        pass

    def settimeout(self, timeout: object) -> None:
        pass

    def close(self) -> None:
        pass


def _fakepair(fd1: int, fd2: int) -> tuple:
    """Return a connected (_FakePipe, _FakePipe) pair (analogous to socket.socketpair)."""
    a, b = _FakePipe(fd1), _FakePipe(fd2)
    a._peer = b
    b._peer = a
    return a, b


def _recv(sock) -> bytes:
    """Read all available bytes from a socket without blocking."""
    sock.setblocking(False)
    try:
        return sock.recv(4096)
    except BlockingIOError:
        return b""


def _make_state(monkeypatch, headless=True):
    """Create a WindowsTerminalState bypassing __init__ to avoid real Win32 calls.

    The module-level _k32 handle is swapped for a _FakeKernel32, so no real console mode is
    touched; _FakePipe pairs replace real OS sockets.
    """
    sel = _FakeSelector()
    k32 = _FakeKernel32()
    monkeypatch.setattr(_niw, "_k32", k32)

    state = object.__new__(WindowsTerminalState)
    state.selector = sel
    state.on_headless = None
    state.headless = headless
    state.on_suspend = None
    state.on_resume = None
    state.hStdin = object()
    state.hStdout = object()
    # ENABLE_PROCESSED_INPUT | ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT
    state.old_stdin_settings = wintypes.DWORD(0x0007)
    state.old_stdout_settings = wintypes.DWORD(0x0003)
    state.stdin_r, state.stdin_w = _fakepair(10, 11)
    state.sigwinch_r, state.sigwinch_w = _fakepair(12, 13)
    state.stdin_reader = StdinReader(functools.partial(state.stdin_r.recv, 1024))
    state._running = False
    return state, sel, k32


class TestSetupTeardown:
    def test_setup_enables_vt100_on_stdout(self, monkeypatch):
        """setup() ORs ENABLE_VIRTUAL_TERMINAL_PROCESSING into the stdout console mode."""
        state, sel, k32 = _make_state(monkeypatch)
        monkeypatch.setattr(_niw.threading, "Thread", _NoopThread)
        monkeypatch.setattr(state, "enter_foreground", lambda: None)

        state.setup()

        vt_flag = ENABLE_VIRTUAL_TERMINAL_PROCESSING
        vt_calls = [v for _, v in k32.set_console_mode_calls if v & vt_flag]
        assert vt_calls, "VT100 flag not set in any SetConsoleMode call during setup()"

    def test_setup_registers_sigwinch_socket(self, monkeypatch):
        """setup() registers sigwinch_r in the selector with tag 'sigwinch'."""
        state, sel, k32 = _make_state(monkeypatch)
        monkeypatch.setattr(_niw.threading, "Thread", _NoopThread)
        monkeypatch.setattr(state, "enter_foreground", lambda: None)

        state.setup()

        tags = [data for _, _, data in sel.register_calls]
        assert "sigwinch" in tags

    def test_setup_starts_two_daemon_threads(self, monkeypatch):
        """setup() starts exactly two daemon threads."""
        state, sel, k32 = _make_state(monkeypatch)
        threads = []

        class _FakeThread:
            def __init__(self, target, daemon):
                threads.append(self)
                self.daemon = daemon

            def start(self):
                pass

        monkeypatch.setattr(_niw.threading, "Thread", _FakeThread)
        monkeypatch.setattr(state, "enter_foreground", lambda: None)

        state.setup()

        assert len(threads) == 2
        assert all(t.daemon for t in threads)

    def test_teardown_restores_console_mode_with_int_values(self, monkeypatch):
        """teardown() passes plain ints (not DWORD structs) to SetConsoleMode."""
        state, sel, k32 = _make_state(monkeypatch)

        state.teardown()

        assert k32.set_console_mode_calls, "SetConsoleMode not called during teardown()"
        for _, v in k32.set_console_mode_calls:
            assert isinstance(v, int), f"Expected int, got {type(v)}: {v!r}"

    def test_teardown_closes_stdin_and_sigwinch_sockets(self, monkeypatch):
        """teardown() closes stdin_r and sigwinch_r."""
        state, sel, k32 = _make_state(monkeypatch)
        stdin_fake = _FakeSocket(99)
        sigwinch_fake = _FakeSocket(100)
        state.stdin_r = stdin_fake
        state.sigwinch_r = sigwinch_fake

        state.teardown()

        assert stdin_fake.close_count == 1
        assert sigwinch_fake.close_count == 1

    def test_teardown_sets_running_false(self, monkeypatch):
        """teardown() sets _running=False to stop background threads."""
        state, sel, k32 = _make_state(monkeypatch)
        state._running = True

        state.teardown()

        assert not state._running


class TestForegroundBackground:
    def test_enter_foreground_noop_when_already_foreground(self, monkeypatch):
        """enter_foreground() is a no-op when headless is already False."""
        state, sel, k32 = _make_state(monkeypatch, headless=False)

        state.enter_foreground()

        assert not k32.set_console_mode_calls

    def test_enter_foreground_disables_line_echo_quickedit(self, monkeypatch):
        """enter_foreground() clears LINE_INPUT, ECHO_INPUT, QUICK_EDIT_MODE."""
        state, sel, k32 = _make_state(monkeypatch, headless=True)
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
        state, sel, k32 = _make_state(monkeypatch, headless=True)
        monkeypatch.setattr(
            WindowsTerminalState, "stdin_is_interactive", staticmethod(lambda: True)
        )

        state.enter_foreground()

        tags = [data for _, _, data in sel.register_calls]
        assert "stdin" in tags
        assert state.headless is False

    def test_enter_foreground_skips_stdin_when_not_interactive(self, monkeypatch):
        """enter_foreground() does not register stdin_r when not interactive."""
        state, sel, k32 = _make_state(monkeypatch, headless=True)
        monkeypatch.setattr(
            WindowsTerminalState, "stdin_is_interactive", staticmethod(lambda: False)
        )

        state.enter_foreground()

        tags = [data for _, _, data in sel.register_calls]
        assert "stdin" not in tags


class TestInputThread:
    """Tests for WindowsTerminalState._input_thread."""

    def _run_thread(self, state, fake_msvcrt, monkeypatch):
        """Call _input_thread directly and return bytes received on stdin_r."""
        state._running = True
        state.headless = False
        monkeypatch.setattr(_niw, "msvcrt", fake_msvcrt)
        monkeypatch.setattr(_niw.time, "sleep", lambda _: None)
        state._input_thread()
        return _recv(state.stdin_r)

    def test_keystroke_forwarded_to_stdin_r(self, monkeypatch):
        """A normal keypress is sent to stdin_r."""
        state, sel, k32 = _make_state(monkeypatch)
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
        state, sel, k32 = _make_state(monkeypatch)
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
        state, sel, k32 = _make_state(monkeypatch)
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
        state, sel, k32 = _make_state(monkeypatch)
        state.headless = True
        kbhit_calls = []

        def fake_sleep(_):
            state._running = False  # stop the loop on first sleep in the headless branch

        fake_msvcrt = types.SimpleNamespace(
            kbhit=lambda: kbhit_calls.append(None) or False, getwch=lambda: ""
        )

        state._running = True
        monkeypatch.setattr(_niw, "msvcrt", fake_msvcrt)
        monkeypatch.setattr(_niw.time, "sleep", fake_sleep)
        state._input_thread()

        assert not kbhit_calls


class TestResizeThread:
    """Tests for WindowsTerminalState._resize_thread."""

    def test_resize_event_sent_on_size_change(self, monkeypatch):
        """_resize_thread sends b'\\x00' to sigwinch_w when terminal dimensions change."""
        state, sel, k32 = _make_state(monkeypatch)
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
        monkeypatch.setattr(_niw.time, "sleep", lambda _: None)
        state._resize_thread()

        assert b"\x00" in _recv(state.sigwinch_r)

    def test_no_resize_event_on_same_size(self, monkeypatch):
        """_resize_thread does not send if dimensions are unchanged."""
        state, sel, k32 = _make_state(monkeypatch)
        state._running = True
        call_count = [0]

        def get_size(**_kwargs):
            call_count[0] += 1
            if call_count[0] > 4:
                state._running = False
            return os.terminal_size((80, 24))

        monkeypatch.setattr(shutil, "get_terminal_size", get_size)
        monkeypatch.setattr(_niw.time, "sleep", lambda _: None)
        state._resize_thread()

        assert _recv(state.sigwinch_r) == b""


class TestStdinReaderSocketPath:
    """Tests for StdinReader when constructed with a socket (Windows path)."""

    def _make_reader(self):
        r, w = socket.socketpair()
        # Keep blocking so recv() returns data immediately, mirroring production behaviour
        # where read() is only called after the selector has already signalled data ready.
        reader = StdinReader(functools.partial(r.recv, 1024))
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


#: Larger than the number of jobs in any test; used to drain the semaphore completely.
ALL_TOKENS = 100


def _new_jobserver(num_jobs: int) -> WindowsJobServer:
    """Create a jobserver that always owns a fresh semaphore.

    Passing an empty MAKEFLAGS keeps the test isolated from an ambient jobserver, which would
    otherwise be inherited when the suite itself runs under make.
    """
    return WindowsJobServer(num_jobs, makeflags="")


def _drain(js: WindowsJobServer) -> int:
    """Acquire all available tokens; return the count acquired."""
    count = 0
    for _ in range(ALL_TOKENS):
        if not js.acquire(1):
            break
        count += 1
    return count


class TestGetJobserverSemaphoreName:
    def test_empty_makeflags(self):
        assert get_jobserver_semaphore_name("") is None

    def test_no_jobserver_flag(self):
        assert get_jobserver_semaphore_name(" -j4 --silent") is None

    def test_fifo_format_skipped(self):
        assert get_jobserver_semaphore_name(" -j4 --jobserver-auth=fifo:/tmp/fifo") is None

    def test_pipe_comma_format_skipped(self):
        assert get_jobserver_semaphore_name(" -j4 --jobserver-auth=3,4") is None

    def test_plain_name_matched(self):
        assert get_jobserver_semaphore_name(" -j4 --jobserver-auth=my-semaphore") == "my-semaphore"

    def test_multiple_flags_last_plain_wins(self):
        makeflags = (
            " --jobserver-auth=fifo:/tmp/fifo --jobserver-auth=3,4"
            " --jobserver-auth=spack-jobserver-99"
        )
        assert get_jobserver_semaphore_name(makeflags) == "spack-jobserver-99"

    def test_plain_before_pipe_returns_plain(self):
        makeflags = " --jobserver-auth=spack-jobserver-1 --jobserver-auth=3,4"
        # last win: 3,4 is a pipe format (skipped), so the last *plain* is spack-jobserver-1
        assert get_jobserver_semaphore_name(makeflags) == "spack-jobserver-1"

    def test_no_leading_space_matched(self):
        # MAKEFLAGS may start directly with --jobserver-auth (no preceding -j flag)
        assert get_jobserver_semaphore_name("--jobserver-auth=bare-name") == "bare-name"

    def test_reads_environment_when_makeflags_is_none(self, monkeypatch):
        """Passing None (the default) falls back to the MAKEFLAGS environment variable."""
        monkeypatch.setenv("MAKEFLAGS", " -j4 --jobserver-auth=from-the-env")
        assert get_jobserver_semaphore_name() == "from-the-env"


class TestWindowsJobServer:
    def test_creates_new_jobserver(self):
        js = _new_jobserver(4)
        try:
            assert js.created is True
            assert js.semaphore_name.startswith("spack-jobserver-")
            assert js.semaphore != 0
        finally:
            js.close()

    def test_initial_token_count(self):
        js = _new_jobserver(4)
        try:
            assert _drain(js) == js.num_jobs - 1
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_single_job_server_has_no_tokens(self):
        js = _new_jobserver(1)
        try:
            assert js.acquire(1) == 0
        finally:
            js.close()

    def test_attaches_to_existing_semaphore(self):
        js1 = _new_jobserver(4)
        try:
            js2 = WindowsJobServer(4, makeflags=f" -j4 --jobserver-auth={js1.semaphore_name}")
            try:
                assert js2.created is False
                assert js2.semaphore_name == js1.semaphore_name
                assert js2.semaphore != 0
            finally:
                js2.close()
        finally:
            js1.close()

    def test_attaches_via_environment(self, monkeypatch):
        """With no explicit makeflags, the jobserver attaches to the one named in MAKEFLAGS."""
        js1 = _new_jobserver(4)
        try:
            monkeypatch.setenv("MAKEFLAGS", f" -j4 --jobserver-auth={js1.semaphore_name}")
            js2 = WindowsJobServer(4)
            try:
                assert js2.created is False
                assert js2.semaphore_name == js1.semaphore_name
            finally:
                js2.close()
        finally:
            js1.close()

    def test_attaches_shares_token_pool(self):
        js1 = _new_jobserver(3)  # 2 tokens
        try:
            js2 = WindowsJobServer(3, makeflags=f" -j3 --jobserver-auth={js1.semaphore_name}")
            try:
                assert js2.acquire(1) == 1
                assert js2.acquire(1) == 1
                assert js2.acquire(1) == 0  # pool exhausted
                assert js1.acquire(1) == 0  # js1 sees the same empty pool
            finally:
                js2.release()
                js2.release()
                js2.close()
        finally:
            js1.close()

    def test_warns_when_parent_semaphore_cannot_be_opened(self):
        """A MAKEFLAGS name that does not resolve falls back to creating a fresh semaphore."""
        with pytest.warns(UserWarning, match="Could not open parent jobserver semaphore"):
            js = WindowsJobServer(4, makeflags=" -j4 --jobserver-auth=spack-no-such-semaphore")
        try:
            assert js.created is True
            assert js.semaphore_name.startswith("spack-jobserver-")
        finally:
            js.close()

    def test_makeflags_and_data(self):
        """The emitted MAKEFLAGS pins -j and the semaphore name, and parses back to that name
        (a child Spack process re-parses it through get_jobserver_semaphore_name)."""
        js = _new_jobserver(8)
        try:
            info = js.makeflags_and_data(None)
            assert info.makeflags == f" -j8 --jobserver-auth={js.semaphore_name}"
            assert get_jobserver_semaphore_name(info.makeflags) == js.semaphore_name
            # The semaphore is inherited by name, so there is no side-band data to pass along.
            assert info.data is None
        finally:
            js.close()

    def test_acquire(self):
        js = _new_jobserver(5)
        try:
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 2
        finally:
            js.release()
            js.release()
            js.close()

    def test_acquire_multiple_tokens_at_once(self):
        """acquire(n) takes up to n tokens in one call, as the POSIX implementation does."""
        js = _new_jobserver(5)  # 4 tokens
        try:
            assert js.acquire(3) == 3
            assert js.tokens_acquired == 3
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_acquire_returns_short_count_when_pool_runs_dry(self):
        """Asking for more tokens than remain returns only what was available."""
        js = _new_jobserver(4)  # 3 tokens
        try:
            assert js.acquire(10) == 3
            assert js.tokens_acquired == 3
            assert js.acquire(10) == 0
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_acquire_returns_zero_when_empty(self):
        js = _new_jobserver(2)
        try:
            # 2-job server has 1 token; second acquire should fail
            assert js.acquire(1) == 1
            assert js.acquire(1) == 0
            assert js.tokens_acquired == 1
        finally:
            js.release()
            js.close()

    def test_release(self):
        js = _new_jobserver(5)
        try:
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
            js.release()
            assert js.tokens_acquired == 0
            assert js.acquire(1) == 1
            assert js.tokens_acquired == 1
        finally:
            js.release()
            js.close()

    def test_close_closes_handle(self):
        js = _new_jobserver(4)
        assert js.semaphore != 0
        js.close()
        # After CloseHandle, WaitForSingleObject returns WAIT_FAILED (0xFFFFFFFF as DWORD)
        assert _niw._k32.WaitForSingleObject(js.semaphore, 0) == 0xFFFFFFFF

    def test_close_warns_spack_holds_tokens(self):
        js = _new_jobserver(4)
        js.acquire(1)
        with pytest.warns(UserWarning, match="Spack failed to release jobserver tokens"):
            js.close()

    def test_close_warns_subprocess_holds_tokens_one(self):
        js = _new_jobserver(4)
        # Simulate a subprocess consuming a token directly (bypassing acquire())
        assert _niw._k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0
        with pytest.warns(UserWarning, match="1 jobserver token was not released"):
            js.close()

    def test_close_warns_subprocess_holds_tokens_two(self):
        js = _new_jobserver(4)
        assert _niw._k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0
        assert _niw._k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0
        with pytest.warns(UserWarning, match="2 jobserver tokens were not released"):
            js.close()

    def test_increase_parallelism_not_created(self):
        """When attached to a parent jobserver, Spack must not resize the shared token pool."""
        js1 = _new_jobserver(3)
        try:
            js2 = WindowsJobServer(3, makeflags=f" -j3 --jobserver-auth={js1.semaphore_name}")
            try:
                assert js2.created is False
                js2.increase_parallelism()
                assert js2.num_jobs == 3
                assert js2.target_jobs == 3
                js2.decrease_parallelism()
                assert js2.num_jobs == 3
                assert js2.target_jobs == 3
            finally:
                js2.close()
        finally:
            js1.close()

    def test_increase_parallelism(self):
        js = _new_jobserver(3)
        try:
            original_num = js.num_jobs
            original_target = js.target_jobs
            js.increase_parallelism()
            assert js.num_jobs == original_num + 1
            assert js.target_jobs == original_target + 1
            # Verify the "num_jobs - 1 tokens in the semaphore" invariant.
            assert _drain(js) + 1 == js.num_jobs
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_decrease_parallelism_at_floor(self):
        js = _new_jobserver(1)
        try:
            assert js.target_jobs == 1
            js.decrease_parallelism()
            assert js.target_jobs == 1
        finally:
            js.close()

    def test_decrease_parallelism_token_available(self):
        js = _new_jobserver(3)
        try:
            original_num = js.num_jobs
            js.decrease_parallelism()
            assert js.target_jobs == original_num - 1
            assert js.num_jobs == original_num - 1
            assert _drain(js) + 1 == js.num_jobs
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_decrease_parallelism_no_token_available(self):
        js = _new_jobserver(3)
        try:
            # Drain the semaphore so no tokens are available for immediate discard.
            assert _drain(js) == js.num_jobs - 1
            original_num = js.num_jobs
            js.decrease_parallelism()
            # target_jobs decremented but num_jobs unchanged (no token to discard yet).
            assert js.target_jobs == original_num - 1
            assert js.num_jobs == original_num
            # increase should cancel the pending decrease, not add a new token.
            js.increase_parallelism()
            assert js.target_jobs == original_num
            assert js.num_jobs == original_num
        finally:
            while js.tokens_acquired:
                js.release()
            js.close()

    def test_maybe_discard_tokens_discards_when_available(self):
        js = _new_jobserver(4)
        try:
            js.target_jobs = js.num_jobs - 2
            js.maybe_discard_tokens()
            assert js.num_jobs == js.target_jobs
        finally:
            js.close()

    def test_release_discards_token_when_target_below_num(self):
        js = _new_jobserver(4)
        drained = 0
        try:
            assert js.acquire(1) == 1
            js.target_jobs = js.num_jobs - 1
            original_num = js.num_jobs
            # Drain remaining free tokens from semaphore so we can verify nothing is put back.
            while _niw._k32.WaitForSingleObject(js.semaphore, 0) == WAIT_OBJECT_0:
                drained += 1
            js.release()
            assert js.tokens_acquired == 0
            assert js.num_jobs == original_num - 1
            # Semaphore should still be empty (token was discarded, not returned).
            assert _niw._k32.WaitForSingleObject(js.semaphore, 0) != WAIT_OBJECT_0
        finally:
            # Restore drained tokens so close() can clean up cleanly.
            if drained > 0:
                _niw._k32.ReleaseSemaphore(js.semaphore, drained, None)
            js.close()

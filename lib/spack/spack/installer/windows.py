# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows-specific terminal state, stdin reader, IPC channels, and job scheduling."""

import sys

if sys.platform != "win32":
    # Also lets mypy skip this module when run on other platforms.
    raise ImportError("spack.installer.windows can only be imported on Windows")

import ctypes
import functools
import io
import msvcrt
import os
import re
import selectors
import shutil
import socket
import threading
import time
import warnings
from ctypes import wintypes
from multiprocessing import Process
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple

from spack.installer.base import (
    OUTPUT_BUFFER_SIZE,
    SIGWINCH_EVENT,
    STDIN_EVENT,
    BaseTerminalState,
    BuildChannels,
    JobServerBase,
    ProcessExitNotifier,
    StdinReader,
    Tee,
)

if TYPE_CHECKING:
    import spack.spec
    from spack.installer.base import BuildStatus

# Windows console mode flags
ENABLE_LINE_INPUT = 0x0002
ENABLE_ECHO_INPUT = 0x0004
ENABLE_QUICK_EDIT_MODE = 0x0040
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004  # for stdout handle
WIN_STD_INPUT_HANDLE = -10
WIN_STD_OUTPUT_HANDLE = -11
WIN_STD_ERROR_HANDLE = -12

# Semaphore / synchronization constants
SYNCHRONIZE = 0x00100000
SEMAPHORE_MODIFY_STATE = 0x00000002
WAIT_OBJECT_0 = 0
SEMAPHORE_MAX_COUNT = 65536

# Module-level kernel32 handle with fully typed Win32 API signatures.
_k32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

_k32.GetStdHandle.restype = wintypes.HANDLE
_k32.GetStdHandle.argtypes = [wintypes.DWORD]

_k32.GetConsoleMode.restype = wintypes.BOOL
_k32.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]

_k32.SetConsoleMode.restype = wintypes.BOOL
_k32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]

_k32.SetStdHandle.restype = wintypes.BOOL
_k32.SetStdHandle.argtypes = [wintypes.DWORD, wintypes.HANDLE]

_k32.OpenSemaphoreW.restype = wintypes.HANDLE
_k32.OpenSemaphoreW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]

_k32.CreateSemaphoreW.restype = wintypes.HANDLE
_k32.CreateSemaphoreW.argtypes = [ctypes.c_void_p, wintypes.LONG, wintypes.LONG, wintypes.LPCWSTR]

_k32.WaitForSingleObject.restype = wintypes.DWORD
_k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]

_k32.ReleaseSemaphore.restype = wintypes.BOOL
_k32.ReleaseSemaphore.argtypes = [wintypes.HANDLE, wintypes.LONG, ctypes.c_void_p]

_k32.CloseHandle.restype = wintypes.BOOL
_k32.CloseHandle.argtypes = [wintypes.HANDLE]


def _handle_is_console(handle_id: int) -> bool:
    """Use GetConsoleMode so this works correctly through Windows Terminal's ConPTY."""
    mode = wintypes.DWORD()
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(handle_id)
    return bool(kernel32.GetConsoleMode(handle, ctypes.byref(mode)))


class WindowsTerminalState(BaseTerminalState):
    """Terminal State management class for Windows.

    Enables VT100/ANSI processing on stdout via SetConsoleMode and bridges keyboard input
    (_input_thread / msvcrt.kbhit) and terminal-resize events (_resize_thread /
    shutil.get_terminal_size) to socketpairs that the selector-based event loop can watch.

    teardown_input() stops the input threads and restores hStdin, but intentionally leaves
    VT100 output processing active so that the final UI render can use ANSI escape sequences
    without leaking raw control characters to the output stream."""

    @classmethod
    def stdout_is_interactive(cls) -> bool:
        return _handle_is_console(WIN_STD_OUTPUT_HANDLE)

    @classmethod
    def stdin_is_interactive(cls) -> bool:
        return _handle_is_console(WIN_STD_INPUT_HANDLE)

    def __init__(
        self,
        selector: selectors.BaseSelector,
        on_headless: Optional[Callable[[bool], None]] = None,
        on_suspend: Optional[Callable[[], None]] = None,
        on_resume: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(selector, on_headless, on_suspend, on_resume)
        self.kernel32 = ctypes.windll.kernel32
        self.hStdin = self.kernel32.GetStdHandle(WIN_STD_INPUT_HANDLE)
        self.hStdout = self.kernel32.GetStdHandle(WIN_STD_OUTPUT_HANDLE)
        self.old_stdin_settings = wintypes.DWORD()
        self.old_stdout_settings = wintypes.DWORD()
        _k32.GetConsoleMode(self.hStdin, ctypes.byref(self.old_stdin_settings))
        _k32.GetConsoleMode(self.hStdout, ctypes.byref(self.old_stdout_settings))

        self.stdin_r, self.stdin_w = socket.socketpair()
        self.stdin_r.setblocking(False)
        self.sigwinch_r, self.sigwinch_w = socket.socketpair()
        self.sigwinch_r.setblocking(False)
        self.stdin_reader = StdinReader(functools.partial(self.stdin_r.recv, 1024))

    def setup(self) -> None:
        # Enable VT100 ANSI escapes on stdout
        new_out_mode = self.old_stdout_settings.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        _k32.SetConsoleMode(self.hStdout, new_out_mode)

        self.selector.register(self.sigwinch_r, selectors.EVENT_READ, SIGWINCH_EVENT)
        self._set_headless(True)

        self._running = True
        threading.Thread(target=self._input_thread, daemon=True).start()
        threading.Thread(target=self._resize_thread, daemon=True).start()

        self.enter_foreground()

    def teardown_input(self) -> None:
        self._running = False
        _k32.SetConsoleMode(self.hStdin, self.old_stdin_settings.value)

        for sock in (self.stdin_r, self.sigwinch_r, self.stdin_w, self.sigwinch_w):
            try:
                self.selector.unregister(sock)
            except KeyError:
                pass
            sock.close()

    def teardown_output(self) -> None:
        _k32.SetConsoleMode(self.hStdout, self.old_stdout_settings.value)

    def enter_foreground(self) -> None:
        if not self.headless:
            return

        _k32.GetConsoleMode(self.hStdin, ctypes.byref(self.old_stdin_settings))

        disable = ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_QUICK_EDIT_MODE
        new_in_mode = (self.old_stdin_settings.value & ~disable) | ENABLE_EXTENDED_FLAGS
        _k32.SetConsoleMode(self.hStdin, new_in_mode)

        if self.stdin_is_interactive() and self.stdin_r.fileno() not in self.selector.get_map():
            self.selector.register(self.stdin_r, selectors.EVENT_READ, STDIN_EVENT)

        self._set_headless(False)

    def drain_sigwinch(self) -> None:
        self.sigwinch_r.recv(64)

    def _input_thread(self) -> None:
        while self._running:
            if self.headless:
                time.sleep(0.1)
                continue
            if msvcrt.kbhit():
                char = msvcrt.getwch()
                if char in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    continue
                try:
                    self.stdin_w.sendall(char.encode("utf-8"))
                except OSError:
                    pass
            else:
                time.sleep(0.05)

    def _resize_thread(self) -> None:
        last_size = shutil.get_terminal_size()
        while self._running:
            time.sleep(0.1)
            curr = shutil.get_terminal_size()
            if curr != last_size:
                last_size = curr
                try:
                    self.sigwinch_w.sendall(b"\x00")
                except OSError:
                    pass


class WindowsSentinelBridge(ProcessExitNotifier):
    """Process-exit notifier for Windows: a thread joins the process and pokes a socket so the
    selector wakes up (Windows process handles cannot be registered with the selector directly)."""

    def __init__(self, proc: Process) -> None:
        self.rsock, self.wsock = socket.socketpair()
        self.rsock.setblocking(False)
        self.proc = proc
        self.thread = threading.Thread(target=self._wait, daemon=True)
        self.thread.start()

    def _wait(self) -> None:
        self.proc.join()
        try:
            self.wsock.sendall(b"x")
        except OSError:
            pass
        self.wsock.close()

    @property
    def fileobj(self) -> socket.socket:
        return self.rsock

    def close(self) -> None:
        self.rsock.close()


def create_build_channels() -> BuildChannels:
    """Create the channel pairs of a build. The state and output read ends are non-blocking so
    the selector-based loop never blocks. The worker's tee thread is stopped by closing the
    control socket rather than through a write end."""
    state_r, state_w = socket.socketpair()
    output_r, output_w = socket.socketpair()
    control_r, control_w = socket.socketpair()
    output_r.setblocking(False)
    state_r.setblocking(False)
    return BuildChannels(state_r, state_w, output_r, output_w, control_r, control_w, None)


class WindowsTee(Tee):
    """Tee for Windows: control and parent channels are sockets; stdout/stderr handles are
    redirected via SetStdHandle so the child process inherits the write end of the pipe."""

    def run(self, log_r: int, log_file: io.BufferedWriter) -> None:
        self._echo = False
        threading.Thread(target=self._control_reader, daemon=True).start()
        try:
            with log_file:
                while True:
                    try:
                        data = os.read(log_r, OUTPUT_BUFFER_SIZE)
                    except OSError:
                        break
                    if not data:
                        break
                    log_file.write(data)
                    log_file.flush()
                    if self._echo:
                        try:
                            self.parent.sendall(data)
                        except OSError:
                            pass
        finally:
            os.close(log_r)

    def _control_reader(self) -> None:
        """Enable or disable echoing based on control bytes sent by the parent."""
        while True:
            try:
                data = self.control_r.recv(1)
            except OSError:
                break
            if not data:
                break
            self._echo = data == b"1"

    def _setup_handles(self) -> None:
        kernel32 = ctypes.windll.kernel32
        self._saved_win32_stdout = kernel32.GetStdHandle(WIN_STD_OUTPUT_HANDLE)
        self._saved_win32_stderr = kernel32.GetStdHandle(WIN_STD_ERROR_HANDLE)
        h_write = msvcrt.get_osfhandle(1)
        os.set_handle_inheritable(h_write, True)
        kernel32.SetStdHandle(WIN_STD_OUTPUT_HANDLE, h_write)
        kernel32.SetStdHandle(WIN_STD_ERROR_HANDLE, h_write)

    def _restore_handles(self) -> None:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetStdHandle(WIN_STD_OUTPUT_HANDLE, self._saved_win32_stdout)
        kernel32.SetStdHandle(WIN_STD_ERROR_HANDLE, self._saved_win32_stderr)


SYNCHRONIZE = 0x00100000
SEMAPHORE_MODIFY_STATE = 0x00000002
WAIT_OBJECT_0 = 0
SEMAPHORE_MAX_COUNT = 65536


def get_jobserver_semaphore_name(makeflags: Optional[str] = None) -> Optional[str]:
    """Parse MAKEFLAGS for a Windows named-semaphore jobserver name.
    Returns None for FIFO (fifo:path) or pipe (r,w) formats."""
    makeflags = os.environ.get("MAKEFLAGS", "") if makeflags is None else makeflags
    if not makeflags:
        return None
    for match in reversed(re.findall(r"(?:^| )--jobserver-auth=([^ ]+)", makeflags)):
        if not match.startswith("fifo:") and "," not in match:
            return match
    return None


class WindowsJobServer(JobServerBase):
    """Win32 named-semaphore jobserver: attaches to a parent semaphore named in MAKEFLAGS,
    or creates one for child processes to inherit via their environment."""

    def __init__(self, num_jobs: int) -> None:
        super().__init__(num_jobs)
        self.tokens_acquired = 0
        self._created = False
        self.semaphore_name: str = ""
        self.semaphore: int = 0
        self.wake_r, self.wake_w = socket.socketpair()
        self.wake_r.setblocking(False)
        self._stop_event = threading.Event()
        self._watcher_lock = threading.Lock()
        self._watcher_active = False
        self._watcher_generation = 0
        self._watcher_thread: Optional[threading.Thread] = None
        self._setup()

    def _setup(self) -> None:
        existing = get_jobserver_semaphore_name()
        if existing:
            h = _k32.OpenSemaphoreW(SYNCHRONIZE | SEMAPHORE_MODIFY_STATE, False, existing)
            if h:
                self.semaphore, self.semaphore_name = h, existing
                return
            warnings.warn(
                f"Could not open parent jobserver semaphore {existing!r}: {ctypes.WinError()!s}; "
                "creating a new semaphore instead",
                stacklevel=3,
            )
        name = f"spack-jobserver-{os.getpid()}"
        h = _k32.CreateSemaphoreW(None, max(0, self.num_jobs - 1), SEMAPHORE_MAX_COUNT, name)
        if not h:
            raise OSError(ctypes.WinError())
        self.semaphore, self.semaphore_name, self._created = h, name, True

    def makeflags_and_data(self, gmake: "Optional[spack.spec.Spec]") -> Tuple[Optional[str], Any]:
        return (f" -j{self.num_jobs} --jobserver-auth={self.semaphore_name}", None)

    def acquire(self, jobs: int) -> int:
        # WaitForSingleObject takes exactly one token at a time; `jobs` is advisory only.
        if _k32.WaitForSingleObject(self.semaphore, 0) == WAIT_OBJECT_0:
            self.tokens_acquired += 1
            return 1
        return 0

    def release(self) -> None:
        if self.tokens_acquired == 0:
            return
        self.tokens_acquired -= 1
        if self.target_jobs < self.num_jobs:
            self.num_jobs -= 1
        else:
            _k32.ReleaseSemaphore(self.semaphore, 1, None)

    def _maybe_discard_tokens(self) -> None:
        to_discard = self.num_jobs - self.target_jobs
        while to_discard > 0:
            if _k32.WaitForSingleObject(self.semaphore, 0) != WAIT_OBJECT_0:
                break
            self.num_jobs -= 1
            to_discard -= 1

    def increase_parallelism(self) -> None:
        if not self._created:
            return
        self.target_jobs += 1
        if self.target_jobs > self.num_jobs:
            _k32.ReleaseSemaphore(self.semaphore, 1, None)
            self.num_jobs += 1

    def decrease_parallelism(self) -> None:
        if not self._created or self.target_jobs <= 1:
            return
        self.target_jobs -= 1
        self._maybe_discard_tokens()

    def update_selector(self, selector: selectors.BaseSelector, wake: bool) -> None:
        if wake:
            try:
                self.wake_r.recv(64)
            except OSError:
                pass
            with self._watcher_lock:
                # Also spawn when the stop event is set: the old thread is winding down and
                # will exit without clearing _watcher_active for the new generation.
                if not self._watcher_active or self._stop_event.is_set():
                    self._watcher_generation += 1
                    gen = self._watcher_generation
                    self._watcher_active = True
                    self._stop_event.clear()
                    t = threading.Thread(target=self._wake_watcher, args=(gen,), daemon=True)
                    self._watcher_thread = t
                    t.start()
            if self.wake_r not in selector.get_map():
                selector.register(self.wake_r, selectors.EVENT_READ, "jobserver")
        else:
            self._stop_event.set()
            try:
                selector.unregister(self.wake_r)
            except KeyError:
                pass

    def _wake_watcher(self, gen: int) -> None:
        while not self._stop_event.is_set():
            if _k32.WaitForSingleObject(self.semaphore, 200) == WAIT_OBJECT_0:
                _k32.ReleaseSemaphore(self.semaphore, 1, None)
                try:
                    self.wake_w.sendall(b"j")
                except OSError:
                    pass
                break
        with self._watcher_lock:
            if self._watcher_generation == gen:
                self._watcher_active = False

    def close(self) -> None:
        self._stop_event.set()
        self.wake_r.close()
        self.wake_w.close()
        with self._watcher_lock:
            thread = self._watcher_thread
        if thread is not None:
            thread.join(timeout=0.5)
        if self._created:
            total = self.num_jobs - 1
            if self.tokens_acquired != 0:
                warnings.warn("Spack failed to release jobserver tokens", stacklevel=2)
            elif total > 0:
                drained = sum(
                    1
                    for _ in range(total)
                    if _k32.WaitForSingleObject(self.semaphore, 0) == WAIT_OBJECT_0
                )
                if drained != total:
                    n = total - drained
                    warnings.warn(
                        f"{n} jobserver tokens were not released by the build processes. "
                        "This can indicate that the build ran with limited parallelism.",
                        stacklevel=2,
                    )
        if self.semaphore:
            _k32.CloseHandle(self.semaphore)


def make_state_stream(state: socket.socket) -> io.TextIOWrapper:
    """Wrap the write end of the state socketpair as a line-buffered text stream."""
    buffer = state.makefile("wb")
    return io.TextIOWrapper(buffer, encoding="utf-8", newline="\n", line_buffering=True)


def read_connection(conn: socket.socket, max_size: int = 4096) -> bytes:
    return conn.recv(max_size)


def write_connection(conn: socket.socket, data: bytes) -> None:
    conn.sendall(data)

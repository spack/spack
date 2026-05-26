# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utility classes for logging the output of blocks of code."""

import atexit
import collections
import ctypes
import ctypes.wintypes as wintypes
import errno
import io
import multiprocessing
import multiprocessing.connection
import os
import re
import select
import selectors
import signal
import socket
import sys
import time
import traceback
from contextlib import contextmanager
from ctypes import wintypes
from multiprocessing.connection import Connection
from threading import Thread
from typing import IO, Callable, List, Optional, Tuple


import spack.llnl.util.tty as tty

if sys.platform == "win32":
    import ctypes.wintypes as wintypes
    import msvcrt

    kernel32 = ctypes.windll.kernel32

try:
    import termios
except ImportError:
    termios = None  # type: ignore[assignment]

# win32api constants
DUPLICATE_SAME_ACCESS = 0x00000002

esc, bell, lbracket, bslash, newline = r"\x1b", r"\x07", r"\[", r"\\", r"\n"
# Ansi Control Sequence Introducers (CSI) are a well-defined format
# Standard ECMA-48: Control Functions for Character-Imaging I/O Devices, section 5.4
# https://www.ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf
csi_pre = f"{esc}{lbracket}"
csi_param, csi_inter, csi_post = r"[0-?]", r"[ -/]", r"[@-~]"
ansi_csi = f"{csi_pre}{csi_param}*{csi_inter}*{csi_post}"
# General ansi escape sequences have well-defined prefixes,
#  but content and suffixes are less reliable.
# Conservatively assume they end with either "<ESC>\" or "<BELL>",
#  with no intervening "<ESC>"/"<BELL>" keys or newlines
esc_pre = f"{esc}[@-_]"
esc_content = f"[^{esc}{bell}{newline}]"
esc_post = f"(?:{esc}{bslash}|{bell})"
ansi_esc = f"{esc_pre}{esc_content}*{esc_post}"
# Use this to strip escape sequences
_escape = re.compile(f"{ansi_csi}|{ansi_esc}")

# control characters for enabling/disabling echo
#
# We use control characters to ensure that echo enable/disable are inline
# with the other output.  We always follow these with a newline to ensure
# one per line the following newline is ignored in output.
xon, xoff = "\x11\n", "\x13\n"
control = re.compile("(\x11\n|\x13\n)")


@contextmanager
def ignore_signal(signum):
    """Context manager to temporarily ignore a signal."""
    old_handler = signal.signal(signum, signal.SIG_IGN)
    try:
        yield
    finally:
        signal.signal(signum, old_handler)


def _is_background_tty(stdin: IO[str]) -> bool:
    """True if the stream is a tty and calling process is in the background."""
    return stdin.isatty() and os.getpgrp() != os.tcgetpgrp(stdin.fileno())


def _strip(line: str) -> str:
    """Strip color and control characters from a line."""
    return _escape.sub("", line)


class preserve_terminal_settings:
    """Context manager to preserve terminal settings on a stream.

    Stores terminal settings before the context and ensures they are restored after.
    Ensures that things like echo and canonical line mode are not left disabled if
    terminal settings in the context are not properly restored.
    """

    def __init__(self, stdin: Optional[IO[str]]) -> None:
        """Create a context manager that preserves terminal settings on a stream.

        Args:
            stream: keyboard input stream, typically sys.stdin
        """
        self.stdin = stdin

    def _restore_default_terminal_settings(self) -> None:
        """Restore the original input configuration on ``self.stdin``."""
        # Can be called in foreground or background. When called in the background, tcsetattr
        # triggers SIGTTOU, which we must ignore, or the process will be stopped.
        assert self.stdin is not None and self.old_cfg is not None and termios is not None
        with ignore_signal(signal.SIGTTOU):
            termios.tcsetattr(self.stdin, termios.TCSANOW, self.old_cfg)

    def __enter__(self) -> "preserve_terminal_settings":
        """Store terminal settings."""
        self.old_cfg = None

        # Ignore all this if the input stream is not a tty.
        if not self.stdin or not self.stdin.isatty() or not termios:
            return self

        # save old termios settings to restore later
        self.old_cfg = termios.tcgetattr(self.stdin)

        # add an atexit handler to ensure the terminal is restored
        atexit.register(self._restore_default_terminal_settings)

        return self

    def __exit__(self, exc_type, exception, traceback):
        """If termios was available, restore old settings."""
        if self.old_cfg:
            self._restore_default_terminal_settings()
            atexit.unregister(self._restore_default_terminal_settings)

kernel32 = ctypes.windll.kernel32

HANDLE = ctypes.c_void_p
LPHANDLE = ctypes.POINTER(HANDLE)

# Define ULONG_PTR for 32/64 bit compatibility
if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

INVALID_HANDLE_VALUE = HANDLE(-1).value 
INFINITE = 0xFFFFFFFF
WAIT_TIMEOUT = 258
ERROR_MORE_DATA = 234
ERROR_IO_PENDING = 997
ERROR_BROKEN_PIPE = 109
ERROR_OPERATION_ABORTED = 995
ERROR_INVALID_HANDLE = 6
ERROR_HANDLE_EOF = 38
READ_BUFFER_SIZE = 65536
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
ENABLE_PROCESSED_INPUT = 0x0001
ENABLE_LINE_INPUT = 0x0002
ENABLE_ECHO_INPUT = 0x0004
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004  # For stdout

INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value


class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", ULONG_PTR),
        ("InternalHigh", ULONG_PTR),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", HANDLE)
    ]

CreateIoCompletionPort = kernel32.CreateIoCompletionPort
CreateIoCompletionPort.argtypes = [HANDLE, HANDLE, ULONG_PTR, wintypes.DWORD]
CreateIoCompletionPort.restype = HANDLE

GetQueuedCompletionStatus = kernel32.GetQueuedCompletionStatus
GetQueuedCompletionStatus.argtypes = [
    HANDLE, 
    ctypes.POINTER(wintypes.DWORD), 
    ctypes.POINTER(ULONG_PTR), 
    ctypes.POINTER(ctypes.POINTER(OVERLAPPED)), 
    wintypes.DWORD
]
GetQueuedCompletionStatus.restype = wintypes.BOOL

PostQueuedCompletionStatus = kernel32.PostQueuedCompletionStatus
PostQueuedCompletionStatus.argtypes = [HANDLE, wintypes.DWORD, ULONG_PTR, ctypes.POINTER(OVERLAPPED)]
PostQueuedCompletionStatus.restype = wintypes.BOOL

ReadFile = kernel32.ReadFile
ReadFile.argtypes = [HANDLE, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(OVERLAPPED)]
ReadFile.restype = wintypes.BOOL

CancelIoEx = kernel32.CancelIoEx
CancelIoEx.argtypes = [HANDLE, ctypes.POINTER(OVERLAPPED)]
CancelIoEx.restype = wintypes.BOOL

PeekNamedPipe = kernel32.PeekNamedPipe
PeekNamedPipe.argtypes = [
    HANDLE, 
    ctypes.c_void_p, 
    wintypes.DWORD, 
    ctypes.POINTER(wintypes.DWORD), 
    ctypes.POINTER(wintypes.DWORD), 
    ctypes.POINTER(wintypes.DWORD)
]
PeekNamedPipe.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = wintypes.BOOL


GetStdHandle = kernel32.GetStdHandle
GetStdHandle.argtypes = [wintypes.DWORD]
GetStdHandle.restype = wintypes.HANDLE

GetConsoleMode = kernel32.GetConsoleMode
GetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.LPDWORD]
GetConsoleMode.restype = wintypes.BOOL

SetConsoleMode = kernel32.SetConsoleMode
SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
SetConsoleMode.restype = wintypes.BOOL


class BufferedPipe:
    """A pipe wrapper that buffers data received by the IOCP Selector."""
    def __init__(self, raw_fd):
        self.fileno_val = raw_fd
        self._buffer = collections.deque()
        self._closed = False

    @property
    def has_data(self):
        return bool(self._buffer) or self._closed

    def fileno(self):
        return self.fileno_val

    def recv(self, max_size=-1):
        if not self._buffer and self._closed:
            raise EOFError
        if not self._buffer:
            return b""
        if len(self._buffer) == 1:
            chunk = self._buffer[0]
            if max_size < 0 or len(chunk) <= max_size:
                self._buffer.popleft()
                return chunk
            else:
                data = chunk[:max_size]
                self._buffer[0] = chunk[max_size:]
                return data
        out = io.BytesIO()
        remaining = max_size if max_size >= 0 else float("inf")
        while self._buffer and remaining > 0:
            chunk = self._buffer[0]
            if len(chunk) > remaining:
                out.write(chunk[:remaining])
                self._buffer[0] = chunk[remaining:]
                remaining = 0
            else:
                out.write(chunk)
                self._buffer.popleft()
                remaining -= len(chunk)
        return out.getvalue()

    def read(self, max_size=-1):
        return self.recv(max_size=max_size)

    def _push_data(self, data):
        if data:
            self._buffer.append(data)

    def _mark_closed(self):
        self._closed = True

class IOCPSelector(selectors.BaseSelector):
    """IO multiplexor class that works with win32 named pipes

    Note: the selectors documentation claims they only work
    with sockets on Windows, this class explicitly supports
    only named pipes, not sockets
    """

    def __init__(self, jobs=0):
        self._iocp = CreateIoCompletionPort(wintypes.HANDLE(INVALID_HANDLE_VALUE), wintypes.HANDLE(0), 0, jobs)
        if not self._iocp:
            raise OSError(f"Failed to create IOCP: {ctypes.GetLastError()}")
        self._fd_to_key = {}
        self._fd_to_handle = {}
        self._valid_ov_addrs = set()

    def register(self, fileobj, events, data=None):
        if (not events) or (events & ~(selectors.EVENT_WRITE | selectors.EVENT_READ)):
            raise ValueError("Invalid event")
        fd = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        if fd in self._fd_to_key:
            raise KeyError(f"{fileobj!r} (FD {fd}) is already registered")

        try:
            f_handle = msvcrt.get_osfhandle(fd)
            f_handle = wintypes.HANDLE(f_handle)
        except OSError as e:
            if e.errno == 9:
                f_handle = wintypes.HANDLE(fd)
            else:
                raise ValueError(f"Invalid file descriptor: {fd}") from e

        bf = BufferedPipe(fd)
        key = selectors.SelectorKey(bf, fd, events, data)
        self._fd_to_key[fd] = key

        res = CreateIoCompletionPort(f_handle, self._iocp, fd, 0)
        if not res:
            raise OSError(f"Failed to associate handle with IOCP: {ctypes.GetLastError()}")

        ov = OVERLAPPED()
        ov_addr = ctypes.addressof(ov)
        self._valid_ov_addrs.add(ov_addr)
        read_buffer = ctypes.create_string_buffer(READ_BUFFER_SIZE)

        self._fd_to_handle[fd] = {
            "handle": f_handle,
            "overlapped": ov,
            "addr": ov_addr,
            "buffer": read_buffer,
            "wrapper": bf,
        }
        self._issue_real_read(fd)
        return key

    def _issue_real_read(self, fd):
        if fd not in self._fd_to_handle:
            return
        handle = self._fd_to_handle[fd]["handle"]
        ov = self._fd_to_handle[fd]["overlapped"]
        buf = self._fd_to_handle[fd]["buffer"]

        ov.Offset = 0
        ov.OffsetHigh = 0
        ov.Internal = 0
        ov.InternalHigh = 0

        bytes_read = wintypes.DWORD()
        res = ReadFile(handle, buf, READ_BUFFER_SIZE, ctypes.byref(bytes_read), ctypes.byref(ov))

        if res:
            PostQueuedCompletionStatus(self._iocp, bytes_read.value, fd, ctypes.byref(ov))
            return

        err = ctypes.GetLastError()
        if err == ERROR_IO_PENDING:
            return
        if err in (ERROR_BROKEN_PIPE, ERROR_INVALID_HANDLE, ERROR_HANDLE_EOF):
            PostQueuedCompletionStatus(self._iocp, 0, fd, ctypes.byref(ov))
            return
        raise OSError(f"ReadFile failed: {err}")

    def unregister(self, fileobj):
        fd = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        try:
            key = self._fd_to_key.pop(fd)
        except KeyError:
            raise KeyError(f"{fileobj!r} is not registered")

        if fd in self._fd_to_handle:
            handle = self._fd_to_handle[fd]["handle"]
            ov = self._fd_to_handle[fd]["overlapped"]
            ov_addr = self._fd_to_handle[fd]["addr"]
            CancelIoEx(handle, ctypes.byref(ov))
            if ov_addr in self._valid_ov_addrs:
                self._valid_ov_addrs.remove(ov_addr)
            del self._fd_to_handle[fd]
        return key

    def select(self, timeout=None):
        ready_keys = []
        has_buffered_data = False

        for fd, key in self._fd_to_key.items():
            if key.fileobj.has_data:
                ready_keys.append((key, selectors.EVENT_READ))
                has_buffered_data = True

        ms = 0 if has_buffered_data else (INFINITE if timeout is None else int(timeout * 1000))
        current_ms = ms
        seen_keys = set()

        c_nbytes = wintypes.DWORD()
        c_key = ULONG_PTR()
        c_ov_ptr = ctypes.POINTER(OVERLAPPED)()

        while True:
            res = GetQueuedCompletionStatus(
                self._iocp, ctypes.byref(c_nbytes), ctypes.byref(c_key), ctypes.byref(c_ov_ptr), current_ms
            )
            rc = 0 if res else ctypes.GetLastError()
            try:
                overlapped = c_ov_ptr.contents if c_ov_ptr else None
            except ValueError:
                overlapped = None

            if rc == WAIT_TIMEOUT:
                break
            if rc and not overlapped:
                raise OSError(f"GetQueuedCompletionStatus failed. Error {rc}")

            ov_addr = ctypes.cast(c_ov_ptr, ctypes.c_void_p).value
            if ov_addr not in self._valid_ov_addrs:
                if ready_keys or has_buffered_data:
                    current_ms = 0
                continue

            key_fd = c_key.value
            if key_fd in self._fd_to_key:
                if key_fd not in seen_keys:
                    bytes_transferred = c_nbytes.value
                    if bytes_transferred:
                        read_buffer = self._fd_to_handle[key_fd]["buffer"]
                        chunk = read_buffer.raw[:bytes_transferred]
                        self._fd_to_handle[key_fd]["wrapper"]._push_data(chunk)
                    if rc in (ERROR_BROKEN_PIPE, ERROR_HANDLE_EOF):
                        self._fd_to_handle[key_fd]["wrapper"]._mark_closed()

                    key = self._fd_to_key[key_fd]
                    is_new = all(rk is not key for rk, _ in ready_keys)
                    if is_new:
                        ready_keys.append((key, selectors.EVENT_READ))
                    seen_keys.add(key_fd)
            current_ms = 0

        for key_fd in seen_keys:
            self._issue_real_read(key_fd)

        return ready_keys

    def get_map(self):
        return self._fd_to_key

    def close(self):
        for fd in list(self._fd_to_handle.keys()):
            self.unregister(fd)
        self._fd_to_handle.clear()
        if self._iocp:
            CloseHandle(self._iocp)
            self._iocp = None
        super().close()


class HybridWindowsSelector(selectors.BaseSelector):
    """Windows IO multiplexor supporting sockets AND fds"""

    def __init__(self):
        self._socket_selector = selectors.SelectSelector()
        self._pipe_selector = IOCPSelector()
        self._map = {}

    def register(self, fileobj, events, data=None):
        is_socket = isinstance(fileobj, socket.socket) or hasattr(fileobj, "family")
        if is_socket:
            key = self._socket_selector.register(fileobj, events, data)
        else:
            key = self._pipe_selector.register(fileobj, events, data)
        self._map[key.fd] = key
        return key

    def unregister(self, fileobj):
        fd = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
        key = self._map.pop(fd)
        try:
            self._socket_selector.unregister(fileobj)
        except KeyError:
            pass
        try:
            self._pipe_selector.unregister(fileobj)
        except KeyError:
            pass
        return key

    def select(self, timeout=None):
        start_time = time.time()
        POLL_INTERVAL = 0.05
        while True:
            ready_keys = []
            if self._socket_selector.get_map():
                ready_keys.extend(self._socket_selector.select(timeout=0))
            if self._pipe_selector.get_map():
                ready_keys.extend(self._pipe_selector.select(timeout=0))

            if ready_keys:
                return ready_keys
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return []
                wait_time = min(POLL_INTERVAL, timeout - elapsed)
                if wait_time < 0:
                    wait_time = 0
            else:
                wait_time = POLL_INTERVAL
            time.sleep(wait_time)

    def close(self):
        self._socket_selector.close()
        self._pipe_selector.close()

    def get_map(self):
        return self._map


class keyboard_input(preserve_terminal_settings):
    """Context manager to disable line editing and echoing.

    Use this with ``sys.stdin`` for keyboard input, e.g.::

        with keyboard_input(sys.stdin) as kb:
            while True:
                kb.check_fg_bg()
                r, w, x = select.select([sys.stdin], [], [])
                # ... do something with keypresses ...

    The ``keyboard_input`` context manager disables canonical
    (line-based) input and echoing, so that keypresses are available on
    the stream immediately, and they are not printed to the
    terminal. Typically, standard input is line-buffered, which means
    keypresses won't be sent until the user hits return. In this mode, a
    user can hit, e.g., ``v``, and it will be read on the other end of the
    pipe immediately but not printed.

    The handler takes care to ensure that terminal changes only take
    effect when the calling process is in the foreground. If the process
    is backgrounded, canonical mode and echo are re-enabled. They are
    disabled again when the calling process comes back to the foreground.

    This context manager works through a single signal handler for
    ``SIGTSTP``, along with a poolling routine called ``check_fg_bg()``.
    Here are the relevant states, transitions, and POSIX signals::

        [Running] -------- Ctrl-Z sends SIGTSTP ------------.
        [ in FG ] <------- fg sends SIGCONT --------------. |
           ^                                              | |
           | fg (no signal)                               | |
           |                                              | v
        [Running] <------- bg sends SIGCONT ---------- [Stopped]
        [ in BG ]                                      [ in BG ]

    We handle all transitions except for ``SIGTSTP`` generated by Ctrl-Z
    by periodically calling ``check_fg_bg()``.  This routine notices if
    we are in the background with canonical mode or echo disabled, or if
    we are in the foreground without canonical disabled and echo enabled,
    and it fixes the terminal settings in response.

    ``check_fg_bg()`` works *except* for when the process is stopped with
    ``SIGTSTP``.  We cannot rely on a periodic timer in this case, as it
    may not rrun before the process stops.  We therefore restore terminal
    settings in the ``SIGTSTP`` handler.

    Additional notes:

    * We mostly use polling here instead of a SIGARLM timer or a
      thread. This is to avoid the complexities of many interrupts, which
      seem to make system calls (like I/O) unreliable in older Python
      versions (2.6 and 2.7).  See these issues for details:

      1. https://www.python.org/dev/peps/pep-0475/
      2. https://bugs.python.org/issue8354

      There are essentially too many ways for asynchronous signals to go
      wrong if we also have to support older Python versions, so we opt
      not to use them.

    * ``SIGSTOP`` can stop a process (in the foreground or background),
      but it can't be caught. Because of this, we can't fix any terminal
      settings on ``SIGSTOP``, and the terminal will be left with
      ``ICANON`` and ``ECHO`` disabled until it is resumes execution.

    * Technically, a process *could* be sent ``SIGTSTP`` while running in
      the foreground, without the shell backgrounding that process. This
      doesn't happen in practice, and we assume that ``SIGTSTP`` always
      means that defaults should be restored.

    * We rely on ``termios`` support.  Without it, or if the stream isn't
      a TTY, ``keyboard_input`` has no effect.

    """

    def __init__(self, stdin: Optional[IO[str]]) -> None:
        """Create a context manager that will enable keyboard input on stream.

        Args:
            stdin: text io wrapper of stdin (keyboard input)

        Note that stdin can be None, in which case ``keyboard_input`` will do nothing.
        """
        super().__init__(stdin)

    def _is_background(self) -> bool:
        """True iff calling process is in the background."""
        assert self.stdin is not None, "stdin should be available"
        return _is_background_tty(self.stdin)

    def _get_canon_echo_flags(self) -> Tuple[bool, bool]:
        """Get current termios canonical and echo settings."""
        assert termios is not None and self.stdin is not None
        cfg = termios.tcgetattr(self.stdin)
        return (bool(cfg[3] & termios.ICANON), bool(cfg[3] & termios.ECHO))

    def _enable_keyboard_input(self) -> None:
        """Disable canonical input and echoing on ``self.stdin``."""
        # "enable" input by disabling canonical mode and echo
        assert termios is not None and self.stdin is not None
        new_cfg = termios.tcgetattr(self.stdin)
        new_cfg[3] &= ~termios.ICANON
        new_cfg[3] &= ~termios.ECHO

        # Apply new settings for terminal
        with ignore_signal(signal.SIGTTOU):
            termios.tcsetattr(self.stdin, termios.TCSANOW, new_cfg)

    def _tstp_handler(self, signum, frame):
        self._restore_default_terminal_settings()
        os.kill(os.getpid(), signal.SIGSTOP)

    def check_fg_bg(self) -> None:
        # old_cfg is set up in __enter__ and indicates that we have
        # termios and a valid stream.
        if not self.old_cfg:
            return

        # query terminal flags and fg/bg status
        flags = self._get_canon_echo_flags()
        bg = self._is_background()

        # restore sanity if flags are amiss -- see diagram in class docs
        if not bg and any(flags):  # fg, but input not enabled
            self._enable_keyboard_input()
        elif bg and not all(flags):  # bg, but input enabled
            self._restore_default_terminal_settings()

    def __enter__(self) -> "keyboard_input":
        """Enable immediate keypress input, while this process is foreground.

        If the stream is not a TTY or the system doesn't support termios,
        do nothing.
        """
        super().__enter__()
        self.old_handlers = {}

        # Ignore all this if the input stream is not a tty.
        if not self.stdin or not self.stdin.isatty():
            return self

        if termios:
            # Install a signal handler to disable/enable keyboard input
            # when the process moves between foreground and background.
            self.old_handlers[signal.SIGTSTP] = signal.signal(signal.SIGTSTP, self._tstp_handler)

            # enable keyboard input initially (if foreground)
            if not self._is_background():
                self._enable_keyboard_input()

        return self

    def __exit__(self, exc_type, exception, traceback):
        """If termios was available, restore old settings."""
        super().__exit__(exc_type, exception, traceback)

        # restore SIGSTP and SIGCONT handlers
        if self.old_handlers:
            for signum, old_handler in self.old_handlers.items():
                signal.signal(signum, old_handler)


class Unbuffered:
    """Wrapper for Python streams that forces them to be unbuffered.

    This is implemented by forcing a flush after each write.
    """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def log_output(*args, **kwargs):
    """Context manager that logs its output to a file.

    In the simplest case, the usage looks like this::

        with log_output('logfile.txt'):
            # do things ... output will be logged

    Any output from the with block will be redirected to ``logfile.txt``.
    If you also want the output to be echoed to ``stdout``, use the
    ``echo`` parameter::

        with log_output('logfile.txt', echo=True):
            # do things ... output will be logged and printed out

    The following is available on Unix only. No-op on Windows.
    And, if you just want to echo *some* stuff from the parent, use
    ``force_echo``::

        with log_output('logfile.txt', echo=False) as logger:
            # do things ... output will be logged

            with logger.force_echo():
                # things here will be echoed *and* logged

    See individual log classes for more information.


    This method is actually a factory serving a per platform
    (unix vs windows) log_output class
    """
    if sys.platform == "win32":
        return winlog(*args, **kwargs)
    else:
        return nixlog(*args, **kwargs)



def forward_stdin(write_pipe, _kill_sig):
    """Run in a thread, recieves stdin from parent process and forwards to child via pipe"""
    # Loop until thread is dead
    try:
        while True:
            stopped = _kill_sig.wait(0.1)
            # ensure write pipe is writable
            assert write_pipe.writable()
            write_pipe.flush()
            stdin_info = sys.stdin.read(4096)
            # chunk stdin so to avoid ValueErrors on
            # large stdin inputs (max is 32mib or less)
            # need to figure out how to stream chunked data
            # so the reader knows its chunked
            write_pipe.send(stdin_info)
            if stopped:
                break
    finally:
        write_pipe.close()


class nixlog:
    """
    Under the hood, we spawn a daemon and set up a pipe between this
    process and the daemon.  The daemon writes our output to both the
    file and to stdout (if echoing).  The parent process can communicate
    with the daemon to tell it when and when not to echo; this is what
    force_echo does.  You can also enable/disable echoing by typing ``v``.

    We use OS-level file descriptors to do the redirection, which
    redirects output for subprocesses and system calls.
    """

    def __init__(
        self,
        filename: str,
        echo=False,
        debug=0,
        buffer=False,
        env=None,
        filter_fn=None,
        append=False,
    ):
        """Create a new output log context manager.

        Args:
            filename (str): path to file where output should be logged
            echo (bool): whether to echo output in addition to logging it
            debug (int): positive to enable tty debug mode during logging
            buffer (bool): pass buffer=True to skip unbuffering output; note
                this doesn't set up any *new* buffering
            filter_fn (callable, optional): Callable[str] -> str to filter each
                line of output
            append (bool): whether to append to file ('a' mode)

        The filename will be opened and closed entirely within ``__enter__``
        and ``__exit__``.

        By default, we unbuffer sys.stdout and sys.stderr because the
        logger will include output from executed programs and from python
        calls.  If stdout and stderr are buffered, their output won't be
        printed in the right place w.r.t. output from commands.

        Logger daemon is not started until ``__enter__()``.

        """
        self.filename = filename
        self.echo = echo
        self.debug = debug
        self.buffer = buffer
        self.filter_fn = filter_fn
        self.append = append

        self._active = False  # used to prevent re-entry
        self.input_forward_thread = None

    def __enter__(self):
        if self._active:
            raise RuntimeError("Can't re-enter the same log_output!")

        # record parent color settings before redirecting.  We do this
        # because color output depends on whether the *original* stdout
        # is a TTY.  New stdout won't be a TTY so we force colorization.
        self._saved_color = tty.color._force_color
        forced_color = tty.color.get_color_when()

        # also record parent debug settings -- in case the logger is
        # forcing debug output.
        self._saved_debug = tty._debug

        # Pipe for redirecting output to logger
        read_fd, self.write_fd = multiprocessing.Pipe(duplex=False)

        # Pipe for communication back from the daemon
        # Currently only used to save echo value between uses
        self.parent_pipe, child_pipe = multiprocessing.Pipe(duplex=False)

        stdin_fd = None
        stdout_fd = None
        try:
            # need to pass this b/c multiprocessing closes stdin in child.
            try:
                if sys.stdin.isatty() and not sys.platform == "win32":
                    stdin_fd = Connection(os.dup(sys.stdin.fileno()))
                else:
                    stdin_fd, stdin_write = multiprocessing.Pipe(duplex=True)
                    self._in_kill = threading.Event()
                    self.input_forward_thread = threading.Thread(target=forward_stdin, args=(stdin_write, ) )
                    self.input_forward_thread.start()
            except BaseException:
                # just don't forward input if this fails
                pass

            # If our process has redirected stdout after the forkserver was started, we need to
            # make the forked processes use the new file descriptors.
            if multiprocessing.get_start_method() == "forkserver":
                stdout_fd = Connection(os.dup(sys.stdout.fileno()))

            self.process = multiprocessing.Process(
                target=_writer_daemon,
                args=(
                    stdin_fd,
                    stdout_fd,
                    read_fd,
                    self.write_fd,
                    self.echo,
                    self.filename,
                    self.append,
                    child_pipe,
                    self.filter_fn,
                ),
            )
            self.process.daemon = True  # must set before start()
            self.process.start()
        except Exception:
            self._in_kill.set()
        finally:
            if stdin_fd:
                stdin_fd.close()
            if stdout_fd:
                stdout_fd.close()
            read_fd.close()

        # Flush immediately before redirecting so that anything buffered
        # goes to the original stream
        sys.stdout.flush()
        sys.stderr.flush()

        # Now do the actual output redirection.
        # We use OS-level file descriptors, as this
        # redirects output for subprocesses and system calls.
        self._redirected_fds = {}

        # sys.stdout and sys.stderr may have been replaced with file objects under pytest, so
        # redirect their file descriptors in addition to the original fds 1 and 2.
        fds = {sys.stdout.fileno(), sys.stderr.fileno(), 1, 2}
        for fd in fds:
            self._redirected_fds[fd] = os.dup(fd)
            os.dup2(self.write_fd.fileno(), fd)

        self.write_fd.close()

        # Unbuffer stdout and stderr at the Python level
        if not self.buffer:
            sys.stdout = Unbuffered(sys.stdout)
            sys.stderr = Unbuffered(sys.stderr)

        # Force color and debug settings now that we have redirected.
        tty.color.set_color_when(forced_color)
        tty._debug = self.debug

        # track whether we're currently inside this log_output
        self._active = True

        # return this log_output object so that the user can do things
        # like temporarily echo some output.
        return self
    

    def redirect_streams(self):
        """Redirects fds to standard buffers"""


    def __exit__(self, exc_type, exc_val, exc_tb):
        # Flush any buffered output to the logger daemon.
        sys.stdout.flush()
        sys.stderr.flush()

        # kill the windows stdin stream
        self._in_kill.set()

        # restore previous output settings using the OS-level way
        for fd, saved_fd in self._redirected_fds.items():
            os.dup2(saved_fd, fd)
            os.close(saved_fd)

        # recover and store echo settings from the child before it dies
        try:
            self.echo = self.parent_pipe.recv()
        except EOFError:
            # This may occur if some exception prematurely terminates the
            # _writer_daemon. An exception will have already been generated.
            pass

        # now that the write pipe is closed (in this __exit__, when we restore
        # stdout with dup2), the logger daemon process loop will terminate. We
        # wait for that here.
        self.process.join()

        # restore old color and debug settings
        tty.color._force_color = self._saved_color
        tty._debug = self._saved_debug

        self._active = False  # safe to enter again

    @contextmanager
    def force_echo(self):
        """Context manager to force local echo, even if echo is off."""
        if not self._active:
            raise RuntimeError("Can't call force_echo() outside log_output region!")

        # This uses the xon/xoff to highlight regions to be echoed in the
        # output. We us these control characters rather than, say, a
        # separate pipe, because they're in-band and assured to appear
        # exactly before and after the text we want to echo.
        sys.stdout.write(xon)
        sys.stdout.flush()
        try:
            yield
        finally:
            sys.stdout.write(xoff)
            sys.stdout.flush()


class StreamWrapper:
    """Wrapper class to handle redirection of io streams"""

    def __init__(self, sys_attr):
        self.sys_attr = sys_attr
        self.saved_stream = None

        kernel32.SetStdHandle.argtypes = [wintypes.DWORD, wintypes.HANDLE]  # nStdHandle  # hHandle

        kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
        kernel32.GetStdHandle.restype = wintypes.HANDLE

        # https://docs.microsoft.com/en-us/windows/console/getstdhandle
        if self.sys_attr == "stdout":
            self.STD_HANDLE = -11
        elif self.sys_attr == "stderr":
            self.STD_HANDLE = -12
        else:
            raise KeyError(self.sys_attr)

        self.saved_stream = getattr(sys, self.sys_attr)
        self.std_fd = self.saved_stream.fileno()
        self.saved_std_handle = kernel32.GetStdHandle(self.STD_HANDLE)
        self.saved_stream_fd = os.dup(self.std_fd)
        self.redirect_fd = None

    def redirect_stream(self, writer):
        """Redirect stdout to the given file descriptor."""
        self.flush()
        # Get fd for new stream
        # new stream is file object
        redirect_fd = writer.fileno()
        # get windows file handle
        redirect_h = msvcrt.get_osfhandle(redirect_fd)
        # duplicate handle for local copy we own
        dup_redirect_h = dup_fh(redirect_h)
        self.redirect_fd = msvcrt.open_osfhandle(dup_redirect_h, os.O_WRONLY)
        kernel32.SetStdHandle(self.STD_HANDLE, wintypes.HANDLE(dup_redirect_h))
        os.dup2(self.redirect_fd, self.std_fd)
        setattr(
            sys,
            self.sys_attr,
            os.fdopen(
                self.std_fd,
                "w",
                encoding="utf-8",
                buffering=1,
                errors="replace",
                closefd=False,
                newline="\n",
            ),
        )

    def flush(self):
        # get current system stream for the standard fd we're redirecting
        sys_stream = getattr(sys, self.sys_attr)
        try:
            if sys_stream:
                # Flush the system stream before redirection
                sys_stream.flush()
        except BaseException as e:
            # swallow flush errors
            tty.debug(f"Encountered error flushing stream: {e}")
            pass

    def close(self):
        """Redirect back to the original system stream, and close stream"""
        try:
            self.flush()
            if self.saved_stream_fd is not None:
                # restore os handle
                kernel32.SetStdHandle(self.STD_HANDLE, self.saved_std_handle)
                # restore c fd
                os.dup2(self.saved_stream_fd, self.std_fd)
                # python level
                setattr(sys, self.sys_attr, self.saved_stream)
        finally:
            if self.redirect_fd is not None:
                os.close(self.redirect_fd)
            if self.saved_stream_fd is not None:
                os.close(self.saved_stream_fd)


class winlog:
    """
    Similar to nixlog, with underlying
    functionality ported to support Windows.

    Does not support the use of ``v`` toggling as nixlog does.
    """

    def __init__(
        self, filename: str, echo=False, debug=0, buffer=False, filter_fn=None, append=False
    ):
        self.debug = debug
        self.echo = echo
        self.logfile = filename
        self.stdout = StreamWrapper("stdout")
        self.stderr = StreamWrapper("stderr")
        self._active = False
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.append = append
        self.filter_fn = filter_fn
        self.read_p, self.write_p = None, None
        self._thread = None

    def __enter__(self):
        if self._active:
            raise RuntimeError("Can't re-enter the same log_output!")

        read_fd, write_fd = os.pipe()
        self.read_p = read_fd
        self.write_p = os.fdopen(write_fd, "wb", buffering=0)

        # Dup stdout so we can still write to it after redirection
        original_stdout_fd = sys.stdout.fileno()
        echo_writer = os.fdopen(os.dup(original_stdout_fd), "w", encoding="utf-8", newline="\n")

        self._active = True
        self._thread = Thread(
            target=self._background_reader,
            args=(self.read_p, self.logfile, echo_writer, self.append, self.echo, self.filter_fn),
        )
        self._thread.start()
        # Redirect stdout and stderr to write to logfile
        self.stderr.redirect_stream(self.write_p)
        self.stdout.redirect_stream(self.write_p)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stdout.close()
        self.stderr.close()
        self.write_p.close()
        self._thread.join()
        self._active = False

    @contextmanager
    def force_echo(self):
        """Context manager to force local echo, even if echo is off."""
        if not self._active:
            raise RuntimeError("Can't call force_echo() outside log_output region!")
        sys.stdout.write(xon)
        sys.stdout.flush()
        try:
            yield
        finally:
            sys.stdout.write(xoff)
            sys.stdout.flush()

    @staticmethod
    def _background_reader(
        read_fd: int,
        logfile: str,
        stdout: io.TextIOWrapper,
        append: bool,
        echo: bool,
        filter_fn: Optional[Callable],
    ):
        force_echo = False
        write_mode = "a" if append else "w"
        read_file = os.fdopen(read_fd, "r", encoding="utf-8", errors="replace", buffering=1)

        def process_message(message):
            nonlocal force_echo
            clean_line, num_controls = control.subn("", message)
            log_writer.write(_strip(clean_line))
            log_writer.flush()
            if echo or force_echo:
                output = clean_line
                if filter_fn:
                    output = filter_fn(output)
                enc = stdout.encoding
                if enc != "utf-8":
                    output = output.encode(enc, "replace").decode(enc)
                stdout.write(output)
                stdout.flush()
            if num_controls > 0:
                controls = control.findall(message)
                force_echo = force_echo_on(force_echo, controls)

        try:
            with open(logfile, mode=write_mode, encoding="utf-8") as log_writer:
                while True:
                    line = read_file.readline(4096)
                    if not line:
                        break
                    process_message(line)

        except Exception as e:
            tty.error(f"Exception in log writer thread! {e}", stream=stdout)
            traceback.print_exc(file=stdout)
        finally:
            read_file.close()
            stdout.close()


def _writer_daemon(
    stdin_fd: Optional[Connection],
    stdout_fd: Optional[Connection],
    read_fd: Connection,
    write_fd: Connection,
    echo: bool,
    log_filename: str,
    append: bool,
    control_fd: Connection,
    filter_fn: Optional[Callable[[str], str]],
) -> None:
    """Daemon used by ``log_output`` to write to a log file and to ``stdout``.

    The daemon receives output from the parent process and writes it both
    to a log and, optionally, to ``stdout``.  The relationship looks like
    this::

        Terminal
           |
           |          +-------------------------+
           |          | Parent Process          |
           +--------> |   with log_output():    |
           | stdin    |     ...                 |
           |          +-------------------------+
           |            ^             | write_fd (parent's redirected stdout)
           |            | control     |
           |            | pipe        |
           |            |             v read_fd
           |          +-------------------------+   stdout
           |          | Writer daemon           |------------>
           +--------> |   read from read_fd     |   log_file
             stdin    |   write to out and log  |------------>
                      +-------------------------+

    Within the ``log_output`` handler, the parent's output is redirected
    to a pipe from which the daemon reads.  The daemon writes each line
    from the pipe to a log file and (optionally) to ``stdout``.  The user
    can hit ``v`` to toggle output on ``stdout``.

    In addition to the input and output file descriptors, the daemon
    interacts with the parent via ``control_pipe``.  It reports whether
    ``stdout`` was enabled or disabled when it finished.

    Arguments:
        stdin_fd: optional input from the terminal
        read_fd: pipe for reading from parent's redirected stdout
        echo: initial echo setting -- controlled by user and preserved across multiple writer
            daemons
        log_filename: filename where output should be logged
        append: whether to append to the file or overwrite it
        control_pipe: multiprocessing pipe on which to send control information to the parent
        filter_fn: optional function to filter each line of output

    """
    # This process depends on closing all instances of write_pipe to terminate the reading loop
    write_fd.close()

    # 1. Use line buffering (3rd param = 1) since Python 3 has a bug
    #    that prevents unbuffered text I/O. [needs citation]
    # 2. Enforce a UTF-8 interpretation of build process output with errors replaced by '?'.
    #    The downside is that the log file will not contain the exact output of the build process.
    # 3. closefd=False because Connection has "ownership"
    read_file = os.fdopen(
        read_fd.fileno(), "r", 1, encoding="utf-8", errors="replace", closefd=False
    )

    if stdin_fd:
        stdin_file = os.fdopen(stdin_fd.fileno(), closefd=False)
    else:
        stdin_file = None

    if stdout_fd:
        os.dup2(stdout_fd.fileno(), sys.stdout.fileno())
        stdout_fd.close()

    # list of streams to select from
    istreams = [read_file, stdin_file] if stdin_file else [read_file]
    force_echo = False  # parent can force echo for certain output
    log_file = open(log_filename, mode="a" if append else "w", encoding="utf-8")

    try:
        with keyboard_input(stdin_file) as kb:
            while True:
                # fix the terminal settings if we recently came to
                # the foreground
                kb.check_fg_bg()

                # wait for input from any stream. use a coarse timeout to
                # allow other checks while we wait for input
                rlist, _, _ = select.select(istreams, [], [], 0.1)

                # Allow user to toggle echo with 'v' key.
                # Currently ignores other chars.
                # only read stdin if we're in the foreground
                if stdin_file and stdin_file in rlist and not _is_background_tty(stdin_file):
                    # it's possible to be backgrounded between the above
                    # check and the read, so we ignore SIGTTIN here.
                    with ignore_signal(signal.SIGTTIN):
                        try:
                            if stdin_file.read(1) == "v":
                                echo = not echo
                        except OSError as e:
                            # If SIGTTIN is ignored, the system gives EIO
                            # to let the caller know the read failed b/c it
                            # was in the bg. Ignore that too.
                            if e.errno != errno.EIO:
                                raise

                if read_file in rlist:
                    line_count = 0
                    try:
                        while line_count < 100:
                            # Handle output from the calling process.
                            line = read_file.readline()

                            if not line:
                                return
                            line_count += 1

                            # find control characters and strip them.
                            clean_line, num_controls = control.subn("", line)

                            # Echo to stdout if requested or forced.
                            if echo or force_echo:
                                output_line = clean_line
                                if filter_fn:
                                    output_line = filter_fn(clean_line)
                                enc = sys.stdout.encoding
                                if enc != "utf-8":
                                    # On Python 3.6 and 3.7-3.14 with non-{utf-8,C} locale stdout
                                    # may not be able to handle utf-8 output. We do an inefficient
                                    # dance of re-encoding with errors replaced, so stdout.write
                                    # does not raise.
                                    output_line = output_line.encode(enc, "replace").decode(enc)
                                sys.stdout.write(output_line)

                            # Stripped output to log file.
                            log_file.write(_strip(clean_line))

                            if num_controls > 0:
                                controls = control.findall(line)
                                force_echo = force_echo_on(force_echo, controls)

                            if not _input_available(read_file):
                                break
                    finally:
                        if line_count > 0:
                            if echo or force_echo:
                                sys.stdout.flush()
                            log_file.flush()

    except BaseException:
        tty.error("Exception occurred in writer daemon!")
        traceback.print_exc()

    finally:
        log_file.close()
        read_fd.close()
        if stdin_fd:
            stdin_fd.close()

        # send echo value back to the parent so it can be preserved.
        control_fd.send(echo)

def dup_fh(fh:int) -> int:
    # Define function signatures for safety
    kernel32.DuplicateHandle.argtypes = [
        wintypes.HANDLE, # hSourceProcessHandle
        wintypes.HANDLE, # hSourceHandle
        wintypes.HANDLE, # hTargetProcessHandle
        ctypes.POINTER(wintypes.HANDLE), # lpTargetHandle
        wintypes.DWORD,  # dwDesiredAccess
        wintypes.BOOL,   # bInheritHandle
        wintypes.DWORD   # dwOptions
    ]
    current_process = ctypes.windll.kernel32.GetCurrentProcess()
    target_handle = wintypes.HANDLE()
    
    success = ctypes.windll.kernel32.DuplicateHandle(
        current_process,
        wintypes.HANDLE(fh),
        current_process,
        ctypes.byref(target_handle),
        0,
        True,
        DUPLICATE_SAME_ACCESS
    )
    
    if not success:
        raise ctypes.WinError()
    
    if not target_handle.value:
        raise ctypes.WinError()

    return target_handle.value


def force_echo_on(force_echo: bool, controls: List[str]):
    if xon in controls:
        return True
    if xoff in controls:
        return False
    return force_echo


if sys.platform == "win32":
    # dont define this outside windows, otherwise mypy complains
    # or we'd have to # type: ignore on basically every line of
    # this method
    def dup_fh(fh: int) -> int:
        """Windows Only
        Duplicates Windows file handles. Useful when
        we need multiple references to a single file handle
        that all can be closed independently

        uses DuplicateHandle from the win32 api

        Arguments:
            fh: OS level file handle to be duplicated

        Returns: integer representing the new, identical file handle
        """
        # Define function signatures for safety
        kernel32.DuplicateHandle.argtypes = [
            wintypes.HANDLE,  # hSourceProcessHandle
            wintypes.HANDLE,  # hSourceHandle
            wintypes.HANDLE,  # hTargetProcessHandle
            ctypes.POINTER(wintypes.HANDLE),  # lpTargetHandle
            wintypes.DWORD,  # dwDesiredAccess
            wintypes.BOOL,  # bInheritHandle
            wintypes.DWORD,  # dwOptions
        ]
        current_process = kernel32.GetCurrentProcess()
        target_handle = wintypes.HANDLE()

        success = kernel32.DuplicateHandle(
            current_process,
            wintypes.HANDLE(fh),
            current_process,
            ctypes.byref(target_handle),
            0,
            True,
            DUPLICATE_SAME_ACCESS,
        )

        if not success or not target_handle.value:
            raise ctypes.WinError()

        return target_handle.value


def force_echo_on(force_echo: bool, controls: List[str]):
    if xon in controls:
        return True
    if xoff in controls:
        return False
    return force_echo


def _input_available(f):
    return f in select.select([f], [], [], 0)[0]

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows-specific I/O: Win32 API bindings, IOCP selector, console I/O bridging.

This module is win32-only.  Import it only inside ``if sys.platform == "win32":`` guards.
"""

import sys

if sys.platform != "win32":  # pragma: no cover
    raise ImportError("spack.llnl.util.win_io is only available on Windows")

import collections
import ctypes
import ctypes.wintypes as wintypes
import io
import msvcrt
import os
import selectors
import shutil
import socket
import threading
import time
from typing import Optional

import spack.llnl.util.tty as tty

# win32 api setup and constants

kernel32 = ctypes.windll.kernel32

HANDLE = ctypes.c_void_p
LPHANDLE = ctypes.POINTER(HANDLE)

ULONG_PTR: type
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
STD_ERROR_HANDLE = -12
ENABLE_PROCESSED_INPUT = 0x0001
ENABLE_LINE_INPUT = 0x0002
ENABLE_ECHO_INPUT = 0x0004
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004  # For stdout

DUPLICATE_SAME_ACCESS = 0x00000002

# Overlapped struct definition, needed for async
# io on Windows


class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", ULONG_PTR),
        ("InternalHigh", ULONG_PTR),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", HANDLE),
    ]


# Ctypes argument typing
# required or win32api calls tend to fail

CreateIoCompletionPort = kernel32.CreateIoCompletionPort
CreateIoCompletionPort.argtypes = [HANDLE, HANDLE, ULONG_PTR, wintypes.DWORD]
CreateIoCompletionPort.restype = HANDLE

GetQueuedCompletionStatus = kernel32.GetQueuedCompletionStatus
GetQueuedCompletionStatus.argtypes = [
    HANDLE,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.POINTER(ULONG_PTR),
    ctypes.POINTER(ctypes.POINTER(OVERLAPPED)),
    wintypes.DWORD,
]
GetQueuedCompletionStatus.restype = wintypes.BOOL

PostQueuedCompletionStatus = kernel32.PostQueuedCompletionStatus
PostQueuedCompletionStatus.argtypes = [
    HANDLE,
    wintypes.DWORD,
    ULONG_PTR,
    ctypes.POINTER(OVERLAPPED),
]
PostQueuedCompletionStatus.restype = wintypes.BOOL

ReadFile = kernel32.ReadFile
ReadFile.argtypes = [
    HANDLE,
    ctypes.c_void_p,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.POINTER(OVERLAPPED),
]
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
    ctypes.POINTER(wintypes.DWORD),
]
PeekNamedPipe.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = wintypes.BOOL

GetStdHandle = kernel32.GetStdHandle
GetStdHandle.argtypes = [wintypes.DWORD]
GetStdHandle.restype = wintypes.HANDLE

SetStdHandle = kernel32.SetStdHandle
SetStdHandle.argtypes = [wintypes.DWORD, wintypes.HANDLE]
SetStdHandle.restype = wintypes.BOOL

GetConsoleMode = kernel32.GetConsoleMode
GetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.LPDWORD]
GetConsoleMode.restype = wintypes.BOOL

SetConsoleMode = kernel32.SetConsoleMode
SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
SetConsoleMode.restype = wintypes.BOOL

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
WaitForSingleObject.restype = wintypes.DWORD

DuplicateHandle = kernel32.DuplicateHandle
DuplicateHandle.argtypes = [
    wintypes.HANDLE,  # hSourceProcessHandle
    wintypes.HANDLE,  # hSourceHandle
    wintypes.HANDLE,  # hTargetProcessHandle
    ctypes.POINTER(wintypes.HANDLE),  # lpTargetHandle
    wintypes.DWORD,  # dwDesiredAccess
    wintypes.BOOL,  # bInheritHandle
    wintypes.DWORD,  # dwOptions
]
DuplicateHandle.restype = wintypes.BOOL


def dup_fh(fh: int) -> int:
    """Duplicate a Win32 HANDLE so each copy can be closed independently."""
    current_process = kernel32.GetCurrentProcess()
    target_handle = wintypes.HANDLE()
    success = DuplicateHandle(
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


def _pipe_bytes_available(fd: int) -> int:
    """Return bytes immediately readable from a Windows pipe without blocking."""
    handle = msvcrt.get_osfhandle(fd)
    available = wintypes.DWORD(0)
    if PeekNamedPipe(handle, None, 0, None, ctypes.byref(available), None):
        return available.value
    return 0


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
        self._iocp = CreateIoCompletionPort(
            wintypes.HANDLE(INVALID_HANDLE_VALUE), wintypes.HANDLE(0), 0, jobs
        )
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
                self._iocp,
                ctypes.byref(c_nbytes),
                ctypes.byref(c_key),
                ctypes.byref(c_ov_ptr),
                current_ms,
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
    """Windows IO multiplexor supporting sockets, IOCP pipes, and waitable handles.

    Three internal selectors:
    * _socket_selector  – socket.socket objects, polled via select()
    * _pipe_selector    – overlapped pipe handles, driven by IOCP
    * _waitable         – everything else (process sentinels, non-overlapped handles),
                          checked with WaitForSingleObject(handle, 0) each poll tick
    """

    # WAIT_OBJECT_0 from winbase.h
    _WAIT_OBJECT_0 = 0

    def __init__(self):
        self._socket_selector = selectors.SelectSelector()
        self._pipe_selector = IOCPSelector()
        self._waitable = {}  # fd (Windows HANDLE as int) → SelectorKey
        self._map = {}

    def register(self, fileobj, events, data=None):
        is_socket = isinstance(fileobj, socket.socket) or hasattr(fileobj, "family")
        if is_socket:
            key = self._socket_selector.register(fileobj, events, data)
        else:
            try:
                key = self._pipe_selector.register(fileobj, events, data)
            except OSError:
                # Handle is not IOCP-compatible (e.g., process sentinel, anonymous pipe).
                # Fall back to WaitForSingleObject polling.
                fd = fileobj.fileno() if hasattr(fileobj, "fileno") else fileobj
                key = selectors.SelectorKey(fileobj=fileobj, fd=fd, events=events, data=data)
                self._waitable[fd] = key
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
        self._waitable.pop(fd, None)
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
            # Poll waitable handles (process sentinels etc.) with a non-blocking wait.
            for fd, key in list(self._waitable.items()):
                res = WaitForSingleObject(wintypes.HANDLE(fd), 0)
                if res == self._WAIT_OBJECT_0:
                    ready_keys.append((key, selectors.EVENT_READ))

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


class ConsoleReader:
    """Bridges blocking Windows console input to the Hybrid Selector via a socket pair.

    Polls msvcrt for keypresses and writes them to ``stdin_wsock``. Also polls for terminal
    resize events and writes a sentinel to ``sigwinch_wsock`` when the size changes.
    Socket registration in the selector is the responsibility of the caller (WindowsTerminalState).
    """

    #: Injected into the stdin socket stream to signal a resize event.
    RESIZE_EVENT_PAYLOAD: bytes = b"\x00\xff\xfeRESIZE"

    def __init__(self, stdin_wsock: socket.socket, sigwinch_wsock: socket.socket) -> None:
        self.stdin_wsock = stdin_wsock
        self.sigwinch_wsock = sigwinch_wsock
        self._running = True
        self._last_size = shutil.get_terminal_size()
        self.thread = threading.Thread(target=self._read_console_and_poll_size, daemon=True)
        self.thread.start()

    def _read_console_and_poll_size(self) -> None:
        while self._running:
            try:
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    if char in (b"\x00", b"\xe0"):
                        char += msvcrt.getch()
                    self.stdin_wsock.sendall(char)
                else:
                    # Poll for Resizes
                    current_size = shutil.get_terminal_size()
                    if current_size != self._last_size:
                        self._last_size = current_size
                        self.sigwinch_wsock.sendall(b"\x00")
                    time.sleep(0.01)
            except Exception:
                break

    def close(self) -> None:
        self._running = False
        self.thread.join(timeout=1.0)


class StreamWrapper:
    """Wrapper class to handle redirection of io streams"""

    def __init__(self, sys_attr):
        self.sys_attr = sys_attr
        self.saved_stream = None

        # https://docs.microsoft.com/en-us/windows/console/getstdhandle
        if self.sys_attr == "stdout":
            self.STD_HANDLE = -11
        elif self.sys_attr == "stderr":
            self.STD_HANDLE = -12
        else:
            raise KeyError(self.sys_attr)

        self.saved_stream = getattr(sys, self.sys_attr)
        self.std_fd = self.saved_stream.fileno()
        self.saved_std_handle = GetStdHandle(self.STD_HANDLE)
        self.saved_stream_fd = os.dup(self.std_fd)
        self.redirect_fd: Optional[int] = None

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

    def close(self):
        """Redirect back to the original system stream, and close stream"""
        try:
            self.flush()
            if self.saved_stream_fd is not None:
                # win32 level
                SetStdHandle(self.STD_HANDLE, self.saved_std_handle)
                # crt level
                os.dup2(self.saved_stream_fd, self.std_fd)
                # python level
                setattr(sys, self.sys_attr, self.saved_stream)
        finally:
            if self.redirect_fd is not None:
                os.close(self.redirect_fd)
            if self.saved_stream_fd is not None:
                os.close(self.saved_stream_fd)

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows-specific I/O: Win32 API bindings, IOCP selector, console I/O bridging.

This module is win32-only.  Import it only inside ``if sys.platform == "win32":`` guards.
"""

import sys

if sys.platform != "win32":  # pragma: no cover
    raise ImportError("spack.llnl.util.win_io is only available on Windows")

import ctypes
import ctypes.wintypes as wintypes
import msvcrt
import os
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

DUPLICATE_SAME_ACCESS = 0x00000002


# Ctypes argument typing
# required or win32api calls tend to fail

GetStdHandle = kernel32.GetStdHandle
GetStdHandle.argtypes = [wintypes.DWORD]
GetStdHandle.restype = wintypes.HANDLE

SetStdHandle = kernel32.SetStdHandle
SetStdHandle.argtypes = [wintypes.DWORD, wintypes.HANDLE]
SetStdHandle.restype = wintypes.BOOL

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

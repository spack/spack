# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows-specific terminal state and stdin reader for the new_installer TUI."""

import ctypes
import msvcrt
import selectors
import shutil
import socket
import threading
import time
from ctypes import wintypes
from typing import TYPE_CHECKING, Callable, Optional

from spack.new_installer_terminal import BaseTerminalState, StdinReaderBase

if TYPE_CHECKING:
    from spack.new_installer import BuildStatus

# Windows console mode flags
ENABLE_LINE_INPUT = 0x0002
ENABLE_ECHO_INPUT = 0x0004
ENABLE_QUICK_EDIT_MODE = 0x0040
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004  # for stdout handle


class WindowsStdinReader(StdinReaderBase):
    """Non-blocking stdin reader for Windows using socket.recv() on the stdin socketpair."""

    def __init__(self, fd: int, sock: socket.socket) -> None:
        super().__init__()
        self.fd = fd
        self.sock = sock

    def read(self) -> str:
        try:
            return self._decode(self.sock.recv(1024))
        except OSError:
            return ""


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
        """Use GetConsoleMode so this works correctly through Windows Terminal's ConPTY."""
        mode = wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.GetStdHandle(-11)
        return bool(kernel32.GetConsoleMode(handle, ctypes.byref(mode)))

    @classmethod
    def stdin_is_interactive(cls) -> bool:
        mode = wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.GetStdHandle(-10)
        return bool(kernel32.GetConsoleMode(handle, ctypes.byref(mode)))

    def __init__(
        self,
        selector: selectors.BaseSelector,
        build_status: "BuildStatus",
        on_suspend: Optional[Callable[[], None]] = None,
        on_resume: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(selector, build_status, on_suspend, on_resume)
        self.kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        self.hStdin = self.kernel32.GetStdHandle(-10)
        self.hStdout = self.kernel32.GetStdHandle(-11)
        self.old_stdin_settings = wintypes.DWORD()
        self.old_stdout_settings = wintypes.DWORD()
        self.kernel32.GetConsoleMode(self.hStdin, ctypes.byref(self.old_stdin_settings))
        self.kernel32.GetConsoleMode(self.hStdout, ctypes.byref(self.old_stdout_settings))

        self.stdin_r, self.stdin_w = socket.socketpair()
        self.stdin_r.setblocking(False)
        self.sigwinch_r, self.sigwinch_w = socket.socketpair()
        self.sigwinch_r.setblocking(False)

    def create_stdin_reader(self) -> WindowsStdinReader:
        return WindowsStdinReader(self.stdin_r.fileno(), sock=self.stdin_r)

    def setup(self) -> None:
        # Enable VT100 ANSI escapes on stdout
        new_out_mode = self.old_stdout_settings.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        self.kernel32.SetConsoleMode(self.hStdout, new_out_mode)

        self.selector.register(self.sigwinch_r, selectors.EVENT_READ, "sigwinch")
        self.build_status.headless = True

        self._running = True
        threading.Thread(target=self._input_thread, daemon=True).start()
        threading.Thread(target=self._resize_thread, daemon=True).start()

        self.enter_foreground()

    def teardown_input(self) -> None:
        self._running = False
        self.kernel32.SetConsoleMode(self.hStdin, self.old_stdin_settings.value)

        for sock in (self.stdin_r, self.sigwinch_r, self.stdin_w, self.sigwinch_w):
            try:
                self.selector.unregister(sock)
            except KeyError:
                pass
            sock.close()

    def teardown_output(self) -> None:
        self.kernel32.SetConsoleMode(self.hStdout, self.old_stdout_settings.value)

    def enter_foreground(self) -> None:
        if not self.build_status.headless:
            return

        self.kernel32.GetConsoleMode(self.hStdin, ctypes.byref(self.old_stdin_settings))

        disable = ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_QUICK_EDIT_MODE
        new_in_mode = (self.old_stdin_settings.value & ~disable) | ENABLE_EXTENDED_FLAGS
        self.kernel32.SetConsoleMode(self.hStdin, new_in_mode)

        if self.stdin_is_interactive() and self.stdin_r.fileno() not in self.selector.get_map():
            self.selector.register(self.stdin_r, selectors.EVENT_READ, "stdin")

        self.build_status.headless = False
        self.build_status.dirty = True

    def enter_background(self) -> None:
        if self.stdin_r.fileno() in self.selector.get_map():
            self.selector.unregister(self.stdin_r)
        self.build_status.headless = True

    def handle_continue(self) -> None:
        self.enter_foreground()

    def drain_sigwinch(self) -> None:
        self.sigwinch_r.recv(64)

    def should_enter_foreground(self) -> bool:
        return True

    def _input_thread(self) -> None:
        while self._running:
            if self.build_status.headless:
                time.sleep(0.1)
                continue
            if msvcrt.kbhit():  # type: ignore[attr-defined]
                char = msvcrt.getwch()  # type: ignore[attr-defined]
                if char in ("\x00", "\xe0"):
                    msvcrt.getwch()  # type: ignore[attr-defined]
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

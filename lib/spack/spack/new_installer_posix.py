# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""POSIX-specific terminal state and stdin reader for the new_installer TUI."""

import os
import selectors
import signal
import sys
import termios
import tty
from typing import TYPE_CHECKING, Callable, Optional

import spack.llnl.util.tty
from spack.llnl.util.tty.log import _is_background_tty, ignore_signal
from spack.new_installer_terminal import BaseTerminalState, StdinReaderBase

if TYPE_CHECKING:
    from spack.new_installer import BuildStatus


class PosixStdinReader(StdinReaderBase):
    """Non-blocking stdin reader for POSIX"""

    def __init__(self, fd: int) -> None:
        super().__init__()
        self.fd = fd

    def read(self) -> str:
        try:
            return self._decode(os.read(self.fd, 1024))
        except OSError:
            return ""


class PosixTerminalState(BaseTerminalState):
    """Manages terminal settings, stdin selector registration, and suspend/resume signals.

    Installs a SIGTSTP handler that restores the terminal before suspending and re-applies it
    on resume. After waking up it checks whether the process is in the foreground or background
    and enables or suppresses interactive output accordingly.

    Optional ``on_suspend`` / ``on_resume`` hooks are called just before the process suspends
    and just after it wakes, allowing callers to pause and resume child processes."""

    def __init__(
        self,
        selector: selectors.BaseSelector,
        build_status: "BuildStatus",
        on_suspend: Optional[Callable[[], None]] = None,
        on_resume: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(selector, build_status, on_suspend, on_resume)
        self.old_stdin_settings = termios.tcgetattr(sys.stdin)
        self.sigwinch_r = -1
        self.sigwinch_w = -1

    def create_stdin_reader(self) -> PosixStdinReader:
        return PosixStdinReader(sys.stdin.fileno())

    def setup(self) -> None:
        """Set cbreak mode, register stdin and signal pipes in the selector."""

        # SIGWINCH self-pipe (stdout must be a tty too)
        if sys.stdout.isatty():
            self.sigwinch_r, self.sigwinch_w = os.pipe()
            os.set_blocking(self.sigwinch_r, False)
            os.set_blocking(self.sigwinch_w, False)
            self.selector.register(self.sigwinch_r, selectors.EVENT_READ, "sigwinch")
            self.old_sigwinch = signal.signal(signal.SIGWINCH, self._handle_sigwinch)
        else:
            self.old_sigwinch = None

        self.old_sigtstp = signal.signal(signal.SIGTSTP, self._handle_sigtstp)

        # Start correctly depending on whether we're foregrounded or backgrounded
        self.build_status.headless = True
        if not _is_background_tty(sys.stdin):
            self.enter_foreground()

    def teardown_input(self) -> None:
        """Restore terminal settings and signal handlers, close pipes."""
        with ignore_signal(signal.SIGTTOU):
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_stdin_settings)

        for sig, old in ((signal.SIGTSTP, self.old_sigtstp), (signal.SIGWINCH, self.old_sigwinch)):
            if old is not None:
                try:
                    signal.signal(sig, old)
                except Exception as e:
                    spack.llnl.util.tty.debug(f"Failed to restore signal handler for {sig}: {e}")

        if sys.stdin.fileno() in self.selector.get_map():
            self.selector.unregister(sys.stdin.fileno())

        for fd in (self.sigwinch_r, self.sigwinch_w):
            if fd < 0:
                continue
            if fd in self.selector.get_map():
                self.selector.unregister(fd)
            try:
                os.close(fd)
            except Exception as e:
                spack.llnl.util.tty.debug(f"Failed to close sigwinch pipe {fd}: {e}")

    def teardown_output(self) -> None:
        pass

    def _handle_sigtstp(self, signum: int, frame: object) -> None:
        """Restore terminal before suspending, then re-install handler after resume."""

        # Reset so the first redraw after resume doesn't overwrite the shell's
        # prompt / "$ fg" line.
        self.build_status.active_area_rows = 0

        # Restore terminal so the user's shell works normally while we're stopped.
        with ignore_signal(signal.SIGTTOU):
            termios.tcsetattr(sys.stdin, termios.TCSANOW, self.old_stdin_settings)

        # Force headless mode before suspending so that enter_foreground() doesn't
        # exit early when we resume, ensuring terminal settings are re-applied.
        self.build_status.headless = True

        # Actually suspend: reset to default handler then re-send SIGTSTP.
        if self.on_suspend is not None:
            self.on_suspend()
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)
        os.kill(os.getpid(), signal.SIGTSTP)

        # Execution resumes here after SIGCONT. Re-install our handler.
        signal.signal(signal.SIGTSTP, self._handle_sigtstp)

        if self.on_resume is not None:
            self.on_resume()
        self.handle_continue()

    def _handle_sigwinch(self, signum: int, frame: object) -> None:
        try:
            os.write(self.sigwinch_w, b"\x00")
        except OSError:
            pass

    def enter_foreground(self) -> None:
        """Restore interactive terminal mode."""
        if not self.build_status.headless:
            return

        # We save old settings right before applying cbreak.
        # If we started in the background, bash may have had the terminal in its own
        # readline (raw) mode when __init__ ran. Waiting until we are foregrounded
        # ensures we capture the shell's exported 'sane' configuration for this job.
        self.old_stdin_settings = termios.tcgetattr(sys.stdin)

        with ignore_signal(signal.SIGTTOU):
            tty.setcbreak(sys.stdin.fileno())

        if sys.stdin.fileno() not in self.selector.get_map():
            self.selector.register(sys.stdin.fileno(), selectors.EVENT_READ, "stdin")
        self.build_status.headless = False
        self.build_status.dirty = True

    def enter_background(self) -> None:
        """Suppress output and stop reading stdin to avoid SIGTTIN/SIGTTOU."""
        if sys.stdin.fileno() in self.selector.get_map():
            self.selector.unregister(sys.stdin.fileno())
        self.build_status.headless = True

    def handle_continue(self) -> None:
        """Detect whether the process is in the foreground or background and adjust accordingly."""
        if _is_background_tty(sys.stdin):
            self.enter_background()
        else:
            self.enter_foreground()

    def drain_sigwinch(self) -> None:
        os.read(self.sigwinch_r, 64)

    def should_enter_foreground(self) -> bool:
        return not _is_background_tty(sys.stdin)

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""POSIX-specific terminal state, stdin reader, IPC channels, and job scheduling."""

import fcntl
import io
import os
import re
import selectors
import signal
import sys
import tempfile
import termios
import tty
import warnings
from multiprocessing import Process
from multiprocessing.connection import Connection
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Union

import spack.llnl.util.tty
import spack.spec
from spack.llnl.util.tty.log import _is_background_tty, ignore_signal
from spack.new_installer_base import (
    OUTPUT_BUFFER_SIZE,
    BaseTerminalState,
    JobServerBase,
    ProcessExitNotifier,
    StdinReaderBase,
    Tee,
)

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


class PosixExitNotifier(ProcessExitNotifier):
    """Process-exit notifier for POSIX: the multiprocessing sentinel fd is selector-watchable."""

    def __init__(self, proc: Process) -> None:
        self.proc = proc

    @property
    def fileobj(self) -> int:
        return self.proc.sentinel


class PosixTee(Tee):
    def run(self, log_r: int, log_file: io.BufferedWriter) -> None:
        """Forward log_r to log_file and parent (if echoing is enabled).
        Echoing is enabled and disabled by reading from control."""
        control_r = self.control.fileno()
        parent_w = self.parent.fileno()
        echo_on = False
        selector = selectors.DefaultSelector()
        selector.register(log_r, selectors.EVENT_READ)
        selector.register(control_r, selectors.EVENT_READ)

        try:
            with log_file, open(parent_w, "wb", closefd=False) as parent:
                while True:
                    for key, _ in selector.select():
                        if key.fd == log_r:
                            data = os.read(log_r, OUTPUT_BUFFER_SIZE)
                            if not data:  # EOF: exit the thread
                                return
                            log_file.write(data)
                            log_file.flush()
                            if echo_on:
                                parent.write(data)
                                parent.flush()

                        elif key.fd == control_r:
                            control_data = os.read(control_r, 1)
                            if not control_data:
                                return
                            else:
                                echo_on = control_data == b"1"
        except OSError:  # do not raise
            pass
        finally:
            os.close(log_r)


class PosixJobServer(JobServerBase):
    """Attach to an existing POSIX jobserver or create a FIFO-based one."""

    def __init__(self, num_jobs: int) -> None:
        super().__init__(num_jobs)
        #: Keep track of how many tokens Spack itself has acquired, which is used to release them.
        self.tokens_acquired = 0
        self.fifo_path: Optional[str] = None
        self.created = False
        self._setup()
        # Ensure that Executable()(...) in build processes ultimately inherit jobserver fds.
        os.set_inheritable(self.r, True)
        os.set_inheritable(self.w, True)
        # r_conn and w_conn are used to make build processes inherit the jobserver fds if needed.
        # Connection objects close the fd as they are garbage collected, so store them.
        self.r_conn = Connection(self.r)
        self.w_conn = Connection(self.w)

    def _setup(self) -> None:

        fifo_config = get_jobserver_config()

        if type(fifo_config) is str:
            # FIFO-based jobserver. Try to open the FIFO.
            open_attempt = open_existing_jobserver_fifo(fifo_config)
            if open_attempt:
                self.r, self.w = open_attempt
                self.fifo_path = fifo_config
                return
        elif type(fifo_config) is tuple:
            # Old style pipe-based jobserver. Validate the fds before using them.
            r, w = fifo_config
            try:
                fcntl.fcntl(r, fcntl.F_GETFD)
                fcntl.fcntl(w, fcntl.F_GETFD)
                self.r, self.w = r, w
                return
            except OSError:  # raised if invalid
                pass

        # No existing jobserver we can connect to: create a FIFO-based one.
        self.r, self.w, self.fifo_path = create_jobserver_fifo(self.num_jobs)
        self.created = True

    def makeflags_and_data(self, gmake: Optional[spack.spec.Spec]) -> Tuple[Optional[str], Any]:
        if self.fifo_path and (not gmake or gmake.satisfies("@4.4:")):
            return f" -j{self.num_jobs} --jobserver-auth=fifo:{self.fifo_path}", None
        # For non-FIFO jobservers, ensure the pipes are inherited by the child process
        pipes = (self.r_conn, self.w_conn)
        if not gmake or gmake.satisfies("@4.0:"):
            return f" -j{self.num_jobs} --jobserver-auth={self.r},{self.w}", pipes
        else:
            return f" -j{self.num_jobs} --jobserver-fds={self.r},{self.w}", pipes

    def update_selector(self, selector: selectors.BaseSelector, wake: bool) -> None:
        if wake and self.r not in selector.get_map():
            selector.register(self.r, selectors.EVENT_READ, "jobserver")
        elif not wake and self.r in selector.get_map():
            selector.unregister(self.r)

    def increase_parallelism(self) -> None:
        if not self.created:
            return
        self.target_jobs += 1
        # If a decrease was pending, don't add a token.
        if self.target_jobs <= self.num_jobs:
            return
        os.write(self.w, b"+")
        self.num_jobs += 1

    def decrease_parallelism(self) -> None:
        if not self.created or self.target_jobs <= 1:
            return
        self.target_jobs -= 1
        self._maybe_discard_tokens()

    def _maybe_discard_tokens(self) -> None:
        """Try to get reduce parallelism by discarding tokens."""
        to_discard = self.num_jobs - self.target_jobs
        if to_discard <= 0:
            return
        try:
            # The read may return zero or just fewer bytes than requested; we'll try again later.
            self.num_jobs -= len(os.read(self.r, to_discard))
        except BlockingIOError:
            pass

    def acquire(self, jobs: int) -> int:
        try:
            num_acquired = len(os.read(self.r, jobs))
            self.tokens_acquired += num_acquired
            return num_acquired
        except BlockingIOError:
            return 0

    def release(self) -> None:
        # The last job to quit has an implicit token, so don't release if we have none.
        if self.tokens_acquired == 0:
            return
        self.tokens_acquired -= 1
        if self.target_jobs < self.num_jobs:
            # If a decrease in parallelism is requested, discard a token instead of releasing it.
            self.num_jobs -= 1
        else:
            os.write(self.w, b"+")

    def close(self) -> None:
        if self.created and self.num_jobs > 1:
            if self.tokens_acquired != 0:
                # It's a non-fatal internal error to close the jobserver with acquired tokens.
                warnings.warn("Spack failed to release jobserver tokens", stacklevel=2)
            else:
                # Verify that all build processes released the tokens they acquired.
                total = self.num_jobs - 1
                drained = self.acquire(total)
                if drained != total:
                    n = total - drained
                    warnings.warn(
                        f"{n} jobserver {'token was' if n == 1 else 'tokens were'} not released "
                        "by the build processes. This can indicate that the build ran with "
                        "limited parallelism.",
                        stacklevel=2,
                    )

        self.r_conn.close()
        self.w_conn.close()

        # Remove the FIFO if we created it.
        if self.created and self.fifo_path:
            try:
                os.unlink(self.fifo_path)
            except OSError:
                pass
            try:
                os.rmdir(os.path.dirname(self.fifo_path))
            except OSError:
                pass


def get_jobserver_config(makeflags: Optional[str] = None) -> Optional[Union[str, Tuple[int, int]]]:
    """Parse MAKEFLAGS for jobserver. Either it's a FIFO or (r, w) pair of file descriptors.

    Args:
        makeflags: MAKEFLAGS string to parse. If None, reads from os.environ.
    """
    makeflags = os.environ.get("MAKEFLAGS", "") if makeflags is None else makeflags
    if not makeflags:
        return None
    # We can have the following flags:
    # --jobserver-fds=R,W (before GNU make 4.2)
    # --jobserver-auth=fifo:PATH or --jobserver-auth=R,W (after GNU make 4.2)
    # In case of multiple, the last one wins.
    matches = re.findall(r" --jobserver-[^=]+=([^ ]+)", makeflags)
    if not matches:
        return None
    last_match: str = matches[-1]
    assert isinstance(last_match, str)
    if last_match.startswith("fifo:"):
        return last_match[5:]
    parts = last_match.split(",", 1)
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def create_jobserver_fifo(num_jobs: int) -> Tuple[int, int, str]:
    """Create a new jobserver FIFO with the specified number of job tokens."""
    tmpdir = tempfile.mkdtemp()
    fifo_path = os.path.join(tmpdir, "jobserver_fifo")

    try:
        os.mkfifo(fifo_path, 0o600)
        read_fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        write_fd = os.open(fifo_path, os.O_WRONLY)
        # write num_jobs - 1 tokens, because the first job is implicit
        os.write(write_fd, b"+" * (num_jobs - 1))
        return read_fd, write_fd, fifo_path
    except Exception:
        try:
            os.unlink(fifo_path)
        except OSError as e:
            spack.llnl.util.tty.debug(f"Failed to remove POSIX jobserver FIFO: {e}", level=3)
            pass
        try:
            os.rmdir(tmpdir)
        except OSError as e:
            spack.llnl.util.tty.debug(f"Failed to remove POSIX jobserver FIFO dir: {e}", level=3)
            pass
        raise


def open_existing_jobserver_fifo(fifo_path: str) -> Optional[Tuple[int, int]]:
    """Open an existing jobserver FIFO for reading and writing."""
    try:
        read_fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        write_fd = os.open(fifo_path, os.O_WRONLY)
        return read_fd, write_fd
    except OSError:
        return None


def make_state_stream(state: Connection) -> io.TextIOWrapper:
    """Wrap the write end of the state Pipe as a line-buffered text stream."""
    return os.fdopen(state.fileno(), "w", buffering=1, closefd=False)


def read_connection(conn: Connection, max_size: int = 4096) -> bytes:
    return os.read(conn.fileno(), max_size)


def write_connection(conn: Connection, data: bytes) -> None:
    os.write(conn.fileno(), data)

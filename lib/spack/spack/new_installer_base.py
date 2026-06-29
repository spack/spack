# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Abstract base classes for new_installer:
TUI terminal state, IPC channels, and job scheduling."""

import abc
import codecs
import io
import os
import re
import selectors
import socket
import sys
import threading
from multiprocessing.connection import Connection
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Union

import spack.spec

if TYPE_CHECKING:
    from spack.new_installer import BuildStatus

# Inter-process communication type
if sys.platform == "win32":
    IpcChannel = socket.socket
else:
    IpcChannel = Connection

#: Size of the output buffer for child processes
OUTPUT_BUFFER_SIZE = 32768

#: Control byte that stops the tee thread
TEE_STOP = b"2"


class StdinReader:
    """Non-blocking stdin reading with UTF-8 decoding, on top of a platform-specific function
    that reads raw bytes.

    Raw bytes are read from the backing file descriptor or socket for stdin (instead of the
    TextIOWrapper) to avoid double buffering issues: the event loop triggers when the fd is ready
    to read, and if we do a partial read from the TextIOWrapper, it will likely drain the fd and
    buffer the remainder internally, which the event loop is not aware of, and user input doesn't
    come through."""

    def __init__(self, read_raw: Callable[[], bytes]) -> None:
        #: Platform-specific function that reads available raw bytes from stdin
        self.read_raw = read_raw
        #: Handle multi-byte UTF-8 characters
        self.decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        #: For stripping out arrow and navigation keys
        self.ansi_escape_re = re.compile(r"\x1b\[[0-9;]*[A-Za-z~]")

    def _decode(self, raw: bytes) -> str:
        return self.ansi_escape_re.sub("", self.decoder.decode(raw))

    def read(self) -> str:
        try:
            return self._decode(self.read_raw())
        except OSError:
            return ""


class BaseTerminalState(abc.ABC):
    """Abstract base for platform-specific terminal state management."""

    def __init__(
        self,
        selector: selectors.BaseSelector,
        build_status: "BuildStatus",
        on_suspend: Optional[Callable[[], None]] = None,
        on_resume: Optional[Callable[[], None]] = None,
    ) -> None:
        self.selector = selector
        self.build_status = build_status
        self.on_suspend = on_suspend
        self.on_resume = on_resume

    @classmethod
    def stdout_is_interactive(cls) -> bool:
        return sys.stdout.isatty()

    @classmethod
    def stdin_is_interactive(cls) -> bool:
        return sys.stdin.isatty()

    @abc.abstractmethod
    def create_stdin_reader(self) -> StdinReader:
        pass

    @abc.abstractmethod
    def setup(self) -> None:
        pass

    @abc.abstractmethod
    def teardown_input(self) -> None:
        """Restore input settings and signal handlers. Called before the final UI render."""
        pass

    def teardown_output(self) -> None:
        """Restore output settings. Called after the final UI render."""

    def teardown(self) -> None:
        self.teardown_input()
        self.teardown_output()

    @abc.abstractmethod
    def enter_foreground(self) -> None:
        pass

    @abc.abstractmethod
    def drain_sigwinch(self) -> None:
        """Drain the platform-specific sigwinch notification channel."""
        pass

    # The methods below are job-control hooks: a platform with suspend/resume support (SIGTSTP/
    # SIGCONT on POSIX) overrides them to transition between foreground and headless mode. The
    # defaults are for platforms without job control, where the process never goes headless after
    # setup().

    def enter_background(self) -> None:
        pass

    def handle_continue(self) -> None:
        pass

    def should_enter_foreground(self) -> bool:
        """Return True if the process should switch from headless to foreground mode."""
        return False


class FdInfo:
    """Information about a file descriptor mapping."""

    __slots__ = ("pid", "name")

    def __init__(self, pid: int, name: str) -> None:
        self.pid = pid
        self.name = name


class ProcessExitNotifier(abc.ABC):
    """Selector-watchable handle that becomes readable when the child process exits."""

    @property
    @abc.abstractmethod
    def fileobj(self) -> Union[int, socket.socket]:
        """Object/fd to register with the selector to detect process exit."""

    def close(self) -> None:
        """Release any resources. Default: nothing to release."""


class JobServerBase(abc.ABC):
    """Abstract base for controlling build concurrency."""

    def __init__(self, num_jobs: int) -> None:
        #: The number of jobs to run concurrently
        self.num_jobs = num_jobs
        #: The target number of jobs to run concurrently, which may differ from num_jobs if the
        #: user has requested a decrease in parallelism, but we haven't consumed enough tokens to
        #: reflect that yet. This value is used in the UI. The value self.target_jobs can only be
        #: modified if Spack owns the jobserver, and not when it's attached to a parent jobserver.
        self.target_jobs = num_jobs

    def has_target_parallelism(self) -> bool:
        return self.num_jobs == self.target_jobs

    @abc.abstractmethod
    def makeflags_and_data(self, gmake: Optional[spack.spec.Spec]) -> Tuple[Optional[str], Any]:
        """Return a tuple of (makeflags, data) to be passed to the child process. The makeflags are
        meant to be set in the child process's environment, and the data is implementation specific
        data serialized and sent to the child process for jobserver support."""

    @abc.abstractmethod
    def update_selector(self, selector: selectors.BaseSelector, wake: bool) -> None:
        """Listen or stop listening for jobserver events on the given selector."""

    @abc.abstractmethod
    def increase_parallelism(self) -> None:
        """Increase the target parallelism by one."""

    @abc.abstractmethod
    def decrease_parallelism(self) -> None:
        """Decrease the target parallelism by one."""

    @abc.abstractmethod
    def acquire(self, jobs: int) -> int:
        """Try and acquire at most 'jobs' tokens from the jobserver. Returns the number of tokens
        actually acquired (may be less than requested, or zero)."""

    @abc.abstractmethod
    def release(self) -> None:
        """Release a token back to the jobserver."""

    @abc.abstractmethod
    def close(self) -> None:
        """Close any resources associated with the jobserver."""


class NoopJobServer(JobServerBase):
    """Dummy jobserver for platforms lacking jobserver support."""

    def makeflags_and_data(self, gmake: Optional[spack.spec.Spec]) -> Tuple[Optional[str], Any]:
        return (None, None)

    def update_selector(self, selector: selectors.BaseSelector, wake: bool) -> None: ...

    def increase_parallelism(self) -> None: ...

    def decrease_parallelism(self) -> None: ...

    def acquire(self, jobs: int) -> int:
        return jobs

    def release(self) -> None: ...

    def close(self) -> None: ...


class Tee(abc.ABC):
    """Emulates ./build 2>&1 | tee build.log. Output is sent to a log file and the parent
    process (if echoing is enabled). The control channel is used to enable/disable echoing."""

    def __init__(
        self,
        control_r: IpcChannel,
        control_w: Optional[IpcChannel],
        parent: IpcChannel,
        log_path: str,
    ) -> None:
        # Read end: the parent sends echo on/off here.
        self.control_r = control_r
        self.parent = parent
        # Write end, used by tee itself to stop the thread (and by parent to toggle echoing).
        self.control_w = control_w
        # sys.stdout and sys.stderr may have been replaced with file objects under pytest, so
        # redirect their file descriptors in addition to the original fds 1 and 2.
        fds = {sys.stdout.fileno(), sys.stderr.fileno(), 1, 2}
        self.saved_fds = {fd: os.dup(fd) for fd in fds}
        #: The path of the log file
        self.log_path = log_path
        log_file = open(self.log_path, "ab")
        r, w = os.pipe()
        self.tee_thread = threading.Thread(target=self.run, args=(r, log_file), daemon=True)
        self.tee_thread.start()
        for fd in fds:
            os.dup2(w, fd)
        self._setup_handles()
        os.close(w)

    def _setup_handles(self) -> None:
        pass

    def _restore_handles(self) -> None:
        pass

    @abc.abstractmethod
    def run(self, log_r: int, log_file: io.BufferedWriter) -> None:
        """Read from log_r, write to log_file; echo to parent when enabled. Runs in a thread."""
        pass

    def close(self) -> None:
        # We restore stdout and stderr, because between sys.exit and the actual process exit
        # buffers may be flushed, and can cause exit code 120 (witnessed under pytest+coverage on
        # macOS).
        sys.stdout.flush()
        sys.stderr.flush()
        for fd, saved_fd in self.saved_fds.items():
            os.dup2(saved_fd, fd)
            os.close(saved_fd)
        if self.control_w is not None:
            # Send a control byte to stop the tee thread.
            try:
                os.write(self.control_w.fileno(), TEE_STOP)
            except OSError:
                pass
        self.tee_thread.join()
        # Only then close the other fds.
        if self.control_w is not None:
            self.control_w.close()
        self.control_r.close()
        self.parent.close()
        self._restore_handles()

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
from multiprocessing import Process
from multiprocessing.connection import Connection
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Union

import spack.database
import spack.spec
import spack.util.lock

if TYPE_CHECKING:
    from spack.new_installer import BuildStatus

#: Size of the output buffer for child processes
OUTPUT_BUFFER_SIZE = 32768


class StdinReaderBase:
    """Base class for platform-specific non-blocking stdin reading with UTF-8 decoding.

    The input is the backing file descriptor for stdin (instead of the TextIOWrapper) to
    avoid double buffering issues: the event loop triggers when the fd is ready to read, and if we
    do a partial read from the TextIOWrapper, it will likely drain the fd and buffer the remainder
    internally, which the event loop is not aware of, and user input doesn't come through."""

    def __init__(self) -> None:
        #: Handle multi-byte UTF-8 characters
        self.decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        #: For stripping out arrow and navigation keys
        self.ansi_escape_re = re.compile(r"\x1b\[[0-9;]*[A-Za-z~]")

    def _decode(self, raw: bytes) -> str:
        return self.ansi_escape_re.sub("", self.decoder.decode(raw))

    def read(self) -> str:
        raise NotImplementedError


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
    def create_stdin_reader(self) -> StdinReaderBase:
        pass

    @abc.abstractmethod
    def setup(self) -> None:
        pass

    @abc.abstractmethod
    def teardown_input(self) -> None:
        """Restore input settings and signal handlers. Called before the final UI render."""
        pass

    @abc.abstractmethod
    def teardown_output(self) -> None:
        """Restore output settings. Called after the final UI render."""
        pass

    def teardown(self) -> None:
        self.teardown_input()
        self.teardown_output()

    @abc.abstractmethod
    def enter_foreground(self) -> None:
        pass

    @abc.abstractmethod
    def enter_background(self) -> None:
        pass

    @abc.abstractmethod
    def handle_continue(self) -> None:
        pass

    @abc.abstractmethod
    def drain_sigwinch(self) -> None:
        """Drain the platform-specific sigwinch notification channel."""
        pass

    @abc.abstractmethod
    def should_enter_foreground(self) -> bool:
        """Return True if the process should switch from headless to foreground mode."""
        pass


#: Size of the output buffer for child processes
OUTPUT_BUFFER_SIZE = 32768


class DatabaseAction:
    """Base class for objects that need to be persisted to the database."""

    __slots__ = ("spec", "prefix_lock")

    spec: spack.spec.Spec
    prefix_lock: Optional[spack.util.lock.Lock]

    def save_to_db(self, db: spack.database.Database) -> None: ...

    def release_prefix_lock(self) -> None:
        if self.prefix_lock is not None:
            try:
                self.prefix_lock.release_write()
            except Exception:
                pass
        self.prefix_lock = None


class FdInfo:
    """Information about a file descriptor mapping."""

    __slots__ = ("pid", "name")

    def __init__(self, pid: int, name: str) -> None:
        self.pid = pid
        self.name = name


class ChildInfo(DatabaseAction):
    """Base class for child process info. Subclassed per platform for IPC channel types."""

    __slots__ = ("proc", "output_r_conn", "state_r_conn", "control_w_conn", "explicit", "log_path")

    def __init__(
        self,
        proc: Process,
        spec: spack.spec.Spec,
        output_r_conn: Connection,
        state_r_conn: Connection,
        control_w_conn: Connection,
        log_path: str,
        explicit: bool = False,
    ) -> None:
        self.proc = proc
        self.spec = spec
        self.output_r_conn = output_r_conn
        self.state_r_conn = state_r_conn
        self.control_w_conn = control_w_conn
        self.log_path = log_path
        self.explicit = explicit
        self.prefix_lock: Optional[spack.util.lock.Lock] = None

    def save_to_db(self, db: spack.database.Database) -> None:
        return db._add(self.spec, explicit=self.explicit)

    def register_with_selector(self, selector: selectors.BaseSelector, pid: int) -> None:
        """Register output, state, and sentinel channels with the selector."""
        selector.register(self.output_r_conn.fileno(), selectors.EVENT_READ, FdInfo(pid, "output"))
        selector.register(self.state_r_conn.fileno(), selectors.EVENT_READ, FdInfo(pid, "state"))
        selector.register(self.proc.sentinel, selectors.EVENT_READ, FdInfo(pid, "sentinel"))

    def close(self, selector: selectors.BaseSelector) -> int:
        """Unregister and close file descriptors, and join the child process.
        Returns the exit code of the child process."""
        try:
            selector.unregister(self.output_r_conn.fileno())
        except KeyError:
            pass
        try:
            selector.unregister(self.state_r_conn.fileno())
        except KeyError:
            pass
        try:
            selector.unregister(self.proc.sentinel)
        except (KeyError, ValueError):
            pass
        self.output_r_conn.close()
        self.state_r_conn.close()
        self.control_w_conn.close()
        self.proc.join()
        exit_code = self.proc.exitcode
        assert exit_code is not None, "Finished build should have exit code set"
        if hasattr(self.proc, "close"):  # No known equivalent in Python 3.6
            self.proc.close()
        return exit_code


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
        return 0

    def release(self) -> None: ...

    def close(self) -> None: ...


class Tee(abc.ABC):
    """Emulates ./build 2>&1 | tee build.log. Output is sent to a log file and the parent
    process (if echoing is enabled). The control socket is used to enable/disable echoing."""

    def __init__(
        self,
        control: Union[Connection, socket.socket],
        parent: Union[Connection, socket.socket],
        log_path: str,
    ) -> None:
        self.control = control
        self.parent = parent
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
        os.close(w)

    @abc.abstractmethod
    def run(self, log_r: int, log_file: io.BufferedWriter) -> None:
        """Read from log_r, write to log_file; echo to parent when enabled. Runs in a thread."""
        pass

    def close(self) -> None:
        # Closing stdout and stderr should close the last reference to the write end of the pipe,
        # causing the tee thread to wake up, flush the last data, and exit. We restore stdout and
        # stderr, because between sys.exit and the actual process exit buffers may be flushed, and
        # can cause exit code 120 (witnessed under pytest+coverage on macOS).
        sys.stdout.flush()
        sys.stderr.flush()
        for fd, saved_fd in self.saved_fds.items():
            os.dup2(saved_fd, fd)
            os.close(saved_fd)
        self.tee_thread.join()
        # Only then close the other fds.
        self.control.close()
        self.parent.close()

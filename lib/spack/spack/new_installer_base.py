# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Abstract base classes for the new_installer TUI terminal state and stdin reading.

Kept in a leaf module (no imports from new_installer.py or the platform modules) so that
new_installer_posix and new_installer_windows can import from here without introducing a
circular dependency."""

import abc
import codecs
import re
import selectors
import sys
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple

import spack.spec

if TYPE_CHECKING:
    from spack.new_installer import BuildStatus


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


class FdInfo:
    """Information about a file descriptor mapping."""

    __slots__ = ("pid", "name")

    def __init__(self, pid: int, name: str) -> None:
        self.pid = pid
        self.name = name


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

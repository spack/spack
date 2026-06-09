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
from typing import TYPE_CHECKING, Callable, Optional

import spack.database
import spack.util.lock

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


class DatabaseAction:
    """Base class for objects that need to be persisted to the database."""

    __slots__ = ("spec", "prefix_lock")

    spec: "spack.spec.Spec"
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

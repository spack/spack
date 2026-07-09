# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Terminal UI for the new installer.

Defines the :class:`InstallerUI` frontend contract (a headless no-op base) and the interactive
:class:`TerminalUI` implementation, plus the plain :class:`BuildInfo` record and the
:data:`UiCommand` messages the UI produces for the event loop. See :mod:`spack.installer`
for the overall design."""

import io
import os
import sys
import time
from typing import Callable, Dict, Generator, List, NamedTuple, Optional, Union, cast

import spack.config
import spack.util.tty.color
from spack.util.lang import pretty_duration
from spack.util.log_parse import make_log_context, parse_log_events
from spack.util.path import padding_filter, padding_filter_bytes

if sys.platform == "win32":
    from spack.installer.windows import WindowsTerminalState as TerminalState
else:
    from spack.installer.posix import PosixTerminalState as TerminalState


class SetEcho(NamedTuple):
    """Command that enables/disables log forwarding from a build."""

    build_id: str
    echo: bool


class ChangeJobs(NamedTuple):
    """Command that increments/decrements job server tokens when positive/negative respectively."""

    delta: int


#: A command produced by the UI and executed by the event loop.
UiCommand = Union[SetEcho, ChangeJobs]

#: How often to update a spinner in seconds
SPINNER_INTERVAL = 0.1

#: Characters the spinner cycles through
SPINNER_CHARS = "|/-\\"

#: How long to display finished packages before graying them out
CLEANUP_TIMEOUT = 2.0


class BuildInfo:
    """Plain data about a package being built: the payload of ``InstallerUI.on_build_added`` and
    the per-build record of the terminal UI."""

    __slots__ = (
        "id",
        "state",
        "explicit",
        "version",
        "hash",
        "name",
        "external",
        "prefix",
        "finished_time",
        "start_time",
        "duration",
        "progress_percent",
        "log_path",
        "log_summary",
    )

    def __init__(
        self,
        build_id: str,
        *,
        name: str,
        version: str,
        external: bool,
        prefix: str,
        explicit: bool,
        log_path: Optional[str] = None,
    ) -> None:
        self.id: str = build_id
        self.state: str = "starting"
        self.explicit: bool = explicit
        self.version: str = version
        self.hash: str = build_id[:7]
        self.name: str = name
        self.external: bool = external
        self.prefix: str = prefix
        self.finished_time: Optional[float] = None
        self.start_time: float = 0.0
        self.duration: Optional[float] = None
        self.progress_percent: Optional[int] = None
        self.log_path = log_path
        self.log_summary: Optional[str] = None


class InstallerUI:
    """Interface between the installer event loop and a frontend. The methods are no-ops, which
    makes this class usable as a headless frontend.

    The event loop calls methods to notify the frontend of build events, and the frontend can
    append to ``self.commands`` to request actions from the event loop."""

    def __init__(self) -> None:
        #: Whether the frontend renders interactively; determines the event loop wake interval.
        self.is_tty = False
        #: Whether the frontend renders to and reads keyboard input from the controlling
        #: terminal. If True, the event loop manages terminal state (cbreak mode, suspend/resume
        #: signals, stdin registration) and feeds keyboard input to ``on_input``.
        self.reads_terminal_input = False
        #: The frontend appends commands to this list to request actions from the event loop.
        self.commands: List[UiCommand] = []

    def on_build_added(self, info: BuildInfo) -> None:
        """A build was started, or a spec was found installed by another process."""

    def on_build_removed(self, build_id: str) -> None:
        """A build was removed after a binary cache miss; it is added back via
        ``on_build_added`` once it is rescheduled as a source build."""

    def on_state_changed(self, build_id: str, state: str) -> None:
        """A build transitioned to a new state (e.g. ``"staging"``, ``"finished"``)."""

    def on_progress(self, build_id: str, current: int, total: int) -> None:
        """Fetch progress of a build changed."""

    def on_total_increased(self, count: int) -> None:
        """The total number of scheduled builds increased (e.g. build dep expansion)."""

    def on_log_output(self, build_id: str, data: bytes) -> None:
        """Raw log output received from a build whose echoing is enabled."""

    def on_finished(self, failures: List[str]) -> None:
        """The whole installation finished. Called once at the end of the run, and is different
        from ``on_state_changed(build_id, "finished")`` which is called after each successful
        package installation. ``failures`` is a list of failed build ids (empty on success). The
        frontend may print a failure summary."""

    def on_jobs_changed(self, actual: int, target: int) -> None:
        """The actual and/or target number of concurrent jobs changed."""

    def on_blocked_changed(self, blocked: bool) -> None:
        """Whether all pending builds are blocked by another Spack process."""

    def on_input(self, chars: str) -> None:
        """Keyboard input received (only called for interactive frontends)."""

    def on_resize(self) -> None:
        """The terminal was resized (only called for interactive frontends)."""

    def on_headless_changed(self, headless: bool) -> None:
        """The process moved to the background (True) or foreground (False); the frontend should
        suppress rendering while headless. Called only through the terminal path."""

    def render(self, finalize: bool = False) -> None:
        """Periodic tick to redraw; ``finalize`` is True for the final render."""

    def refresh_interval(self) -> Optional[float]:
        """How often the frontend needs a periodic ``render`` tick, or None if it never does. The
        event loop bounds its sleep by this together with its own database-flush cadence."""
        return None


class TerminalUI(InstallerUI):
    """Terminal frontend: renders an interactive build overview and follows build logs."""

    def __init__(
        self,
        total: int,
        stdout: Optional[io.TextIOWrapper] = None,
        get_terminal_size: Callable[[], os.terminal_size] = os.get_terminal_size,
        get_time: Callable[[], float] = time.monotonic,
        is_tty: Optional[bool] = None,
        color: Optional[bool] = None,
        verbose: bool = False,
        filter_padding: bool = False,
    ) -> None:
        super().__init__()
        self.reads_terminal_input = True
        if stdout is None:
            stdout = cast(io.TextIOWrapper, sys.stdout)
            if is_tty is None:
                # For the real stdout, use GetConsoleMode-based detection on Windows, which is
                # correct through ConPTY where isatty() is not.
                is_tty = TerminalState.stdout_is_interactive()
        #: Ordered dict of build ID -> info
        self.total = total
        self.completed = 0
        self.builds: Dict[str, BuildInfo] = {}
        self.finished_builds: List[BuildInfo] = []
        self.spinner_index = 0
        self.dirty = True  # Start dirty to draw initial state
        self.active_area_rows = 0
        self.total_lines = 0
        self.next_spinner_update = 0.0
        self.next_update = 0.0
        self.overview_mode = True  # Whether to draw the package overview
        self.tracked_build_id = ""  # identifier of the package whose logs we follow
        self.search_term = ""
        self.search_mode = False
        self.log_ends_with_newline = True
        self.actual_jobs: int = 0
        self.target_jobs: int = 0
        self.blocked: bool = False

        self.stdout = stdout
        self.get_terminal_size = get_terminal_size
        self.terminal_size = os.terminal_size((0, 0))
        self.terminal_size_changed: bool = True
        self.get_time = get_time
        self.is_tty = is_tty if is_tty is not None else stdout.isatty()
        if color is None:
            color = spack.util.tty.color.get_color_when(stdout)
        # ANSI escape codes used for rendering; empty strings when color is disabled.
        if color:
            self.red, self.green, self.cyan = "\033[31m", "\033[32m", "\033[0;36m"
            self.gray, self.bold, self.reset = "\033[0;90m", "\033[1m", "\033[0m"
        else:
            self.red = self.green = self.cyan = self.gray = self.bold = self.reset = ""
        #: Verbose mode only applies to non-TTY where we want to track a single build log.
        self.verbose = verbose and not self.is_tty
        self.filter_padding = filter_padding
        #: When True, suppress all terminal output (process is in background).
        self.headless = False
        self.term_title = spack.config.get("config:install_status", True) and self.is_tty

    def on_resize(self) -> None:
        """Refresh cached terminal size and trigger a redraw."""
        self.terminal_size_changed = True
        self.dirty = True

    def on_headless_changed(self, headless: bool) -> None:
        if headless:
            # The display is invalidated: the shell may print over it while we're suspended or in
            # the background, so the next render must append instead of moving the cursor up.
            self.active_area_rows = 0
        else:
            self.dirty = True
        self.headless = headless

    def refresh_interval(self) -> Optional[float]:
        # Only an interactive, foreground terminal animates the spinner; a suppressed (headless)
        # or non-tty frontend needs no periodic redraw.
        if self.headless or not self.is_tty:
            return None
        return SPINNER_INTERVAL

    def on_build_added(self, info: BuildInfo) -> None:
        """Add a new build to the display and mark the display as dirty."""
        info.start_time = int(self.get_time())
        self.builds[info.id] = info
        self.dirty = True
        # Track the new build's logs when we're not already following another build. This applies
        # only in non-TTY verbose mode.
        if self.verbose and not self.tracked_build_id:
            self.tracked_build_id = info.id
            self.commands.append(SetEcho(info.id, True))

    def on_build_removed(self, build_id: str) -> None:
        """Remove a build from the display (e.g. after a binary cache miss before retry)."""
        self.builds.pop(build_id, None)
        if self.tracked_build_id == build_id:
            self.tracked_build_id = ""
            self.overview_mode = True
        self.dirty = True

    def toggle(self) -> None:
        """Toggle between overview mode and following a specific build."""
        if self.overview_mode:
            self.next()
        else:
            if not self.log_ends_with_newline:
                self.stdout.buffer.write(b"\n")
                self.log_ends_with_newline = True
            self.active_area_rows = 0
            self.search_term = ""
            self.search_mode = False
            self.overview_mode = True
            self.dirty = True
            self.commands.append(SetEcho(self.tracked_build_id, False))
            self.tracked_build_id = ""

    def search_input(self, char: str) -> None:
        """Handle keyboard input when in search mode"""
        if char in ("\r", "\n"):
            self.log_ends_with_newline = False
            self.next(1)
        elif char == "\x1b":  # Escape
            self.search_mode = False
            self.search_term = ""
            self.dirty = True
        elif char in ("\x7f", "\b"):  # Backspace
            self.search_term = self.search_term[:-1]
            self.dirty = True
        elif char.isprintable():
            self.search_term += char
            self.dirty = True

    def enter_search(self) -> None:
        self.search_mode = True
        self.dirty = True

    def on_input(self, chars: str) -> None:
        """Dispatch keyboard input to search, navigation, and parallelism actions."""
        for char in chars:
            overview = self.overview_mode
            if overview and self.search_mode:
                self.search_input(char)
            elif overview and char == "/":
                self.enter_search()
            elif char == "v" or char in ("q", "\x1b") and not overview:
                self.toggle()
            elif char == "n":
                self.next(1)
            elif char == "p" or char == "N":
                self.next(-1)
            elif char == "+":
                self.commands.append(ChangeJobs(1))
            elif char == "-":
                self.commands.append(ChangeJobs(-1))

    def _is_displayed(self, build: BuildInfo) -> bool:
        """Returns true if the build matches the search term, or when no search term is set."""
        # When not in search mode, the search_term is "", which always evaluates to True below
        return self.search_term in build.name or build.hash.startswith(self.search_term)

    def _get_next(self, direction: int) -> Optional[str]:
        """Returns the next or previous unfinished build ID matching the search term, or None if
        none found. Direction should be 1 for next, -1 for previous."""
        matching = [
            build_id
            for build_id, build in self.builds.items()
            if (build.finished_time is None or build.state == "failed")
            and self._is_displayed(build)
        ]
        if not matching:
            return None
        try:
            idx = matching.index(self.tracked_build_id)
        except ValueError:
            return matching[0] if direction == 1 else matching[-1]

        return matching[(idx + direction) % len(matching)]

    def next(self, direction: int = 1) -> None:
        """Follow the logs of the next build in the list."""
        new_build_id = self._get_next(direction)

        if not new_build_id or self.tracked_build_id == new_build_id:
            return

        new_build = self.builds[new_build_id]

        self.overview_mode = False

        # Stop following the previous and start following the new build.
        if self.tracked_build_id:
            self.commands.append(SetEcho(self.tracked_build_id, False))

        self.tracked_build_id = new_build_id

        version_str = f"{self.cyan}@{new_build.version}{self.reset}"
        prefix = "" if self.log_ends_with_newline else "\n"

        if new_build.state == "failed":
            # For failed builds, show the stored log summary instead of following live logs.
            self.stdout.write(f"{prefix}==> Log summary of {new_build.name}{version_str}\n")
            self.log_ends_with_newline = True
            if new_build.log_summary:
                self.stdout.write(new_build.log_summary)
            if new_build.log_path:
                if not new_build.log_summary:
                    self.stdout.write("No errors parsed from log, see full log: ")
                else:
                    self.stdout.write("Full log: ")
                self.stdout.write(f"{new_build.log_path}\n")
            self.stdout.flush()
        else:
            # Tell the user we're following new logs, and instruct the child to start sending.
            self.stdout.write(f"{prefix}==> Following logs of {new_build.name}{version_str}\n")
            self.log_ends_with_newline = True
            self.stdout.flush()
            self.commands.append(SetEcho(new_build_id, True))

    def on_blocked_changed(self, blocked: bool) -> None:
        """Set whether all pending builds are blocked by another Spack process."""
        if blocked == self.blocked:
            return
        self.blocked = blocked
        self.dirty = True

    def _update_terminal_title(self, clear: bool = False) -> None:
        if not self.term_title or self.headless:
            return

        term_title = ""

        if not clear:
            term_title = f"Spack: {self.completed}/{self.total} - {self.actual_jobs} jobs"

        self.stdout.write(f"\x1b]0;{term_title}\x07")
        self.stdout.flush()

    def on_jobs_changed(self, actual: int, target: int) -> None:
        """Set the actual and target number of jobs to run concurrently."""
        if actual == self.actual_jobs and target == self.target_jobs:
            return
        self.actual_jobs = actual
        self.target_jobs = target
        self.dirty = True
        self._update_terminal_title()

    def on_state_changed(self, build_id: str, state: str) -> None:
        """Update the state of a package and mark the display as dirty."""
        now = self.get_time()
        build_info = self.builds[build_id]
        build_info.state = state
        build_info.progress_percent = None

        if state == "failed":
            # Store the log summary for interactive browsing and the final failure printout.
            self._parse_log_summary(build_info)

        if state in ("finished", "failed"):
            self.completed += 1
            build_info.duration = now - build_info.start_time
            build_info.finished_time = now + CLEANUP_TIMEOUT

            # Stop tracking the finished build's logs.
            if build_id == self.tracked_build_id:
                if not self.overview_mode:
                    self.toggle()
                if self.verbose:
                    self.tracked_build_id = ""

        self.dirty = True
        self._update_terminal_title()

        # For non-TTY output, print state changes immediately
        if not self.is_tty and not self.headless:
            line = "".join(self._generate_line_components(build_info, static=True, now=now))
            self.stdout.write(line + "\n")
            self.stdout.flush()

    def _parse_log_summary(self, build_info: BuildInfo) -> None:
        """Parse the build log for errors/warnings and store the summary."""
        if not build_info.log_path or not os.path.exists(build_info.log_path):
            return
        errors, warnings, tail_event = parse_log_events(build_info.log_path, tail=20)
        events = [*errors, *warnings]
        if tail_event is not None:
            events.append(tail_event)
        if events:
            build_info.log_summary = make_log_context(events)

    def on_finished(self, failures: List[str]) -> None:
        """Write the stored log summaries of the failed builds to stderr."""
        for build_id in failures:
            build_info = self.builds.get(build_id)
            if build_info is not None and build_info.log_summary:
                sys.stderr.write(build_info.log_summary)

    def on_total_increased(self, count: int) -> None:
        self.total += count

    def on_progress(self, build_id: str, current: int, total: int) -> None:
        """Update the progress of a package and mark the display as dirty."""
        percent = int((current / total) * 100)
        build_info = self.builds[build_id]
        if build_info.progress_percent != percent:
            build_info.progress_percent = percent
            self.dirty = True

    def render(self, finalize: bool = False) -> None:
        """Redraw the interactive display."""
        if finalize:
            self.overview_mode = True
        if self.headless or not self.is_tty or not self.overview_mode:
            return

        now = self.get_time()

        # Avoid excessive redraws
        if not finalize and now < self.next_update:
            return

        has_unfinished = any(pkg.finished_time is None for pkg in self.builds.values())

        # Only update the spinner if there are still running packages
        if has_unfinished and now >= self.next_spinner_update:
            self.spinner_index = (self.spinner_index + 1) % len(SPINNER_CHARS)
            self.dirty = True
            self.next_spinner_update = now + SPINNER_INTERVAL

        for build_id in list(self.builds):
            build_info = self.builds[build_id]
            if build_info.state == "failed" or build_info.finished_time is None:
                continue

            if finalize or now >= build_info.finished_time:
                self.finished_builds.append(build_info)
                del self.builds[build_id]
                self.dirty = True

        if not self.dirty and not finalize:
            return

        # Build the overview output in a buffer and print all at once to avoid flickering.
        buffer = io.StringIO()

        # Move cursor up to the start of the display area assuming the same terminal width. If the
        # terminal resized, lines may have wrapped, and we should've moved up further. We do not
        # try to track that (would require keeping track of each line's width).
        if self.active_area_rows > 0:
            buffer.write(f"\033[{self.active_area_rows}A\r")

        if self.terminal_size_changed:
            self.terminal_size = self.get_terminal_size()
            self.terminal_size_changed = False
            # After resize, active_area_rows is invalidated due to possible line wrapping. Set to
            # 0 to force newlines instead of cursor movement.
            self.active_area_rows = 0
        max_width, max_height = self.terminal_size

        # First flush the finished builds. These are "persisted" in terminal history.
        if self.finished_builds:
            for build in self.finished_builds:
                self._render_build(build, buffer, now=now)
                self._println(buffer, force_newline=True)  # should scroll the terminal
            self.finished_builds.clear()
            # Finished builds can span multiple lines, overlapping our "active area", invalidating
            # active_area_rows. Set to 0 to force newlines instead of cursor movement.
            self.active_area_rows = 0

        # Then a header followed by the active builds. This is the "mutable" part of the display.
        self.total_lines = 0

        if not finalize:
            if self.actual_jobs != self.target_jobs:
                jobs_str = f"{self.actual_jobs}=>{self.target_jobs}"
            else:
                jobs_str = str(self.target_jobs)
            bold, reset, cyan = self.bold, self.reset, self.cyan
            long_header = (
                f"{bold}Progress:{reset} {self.completed}/{self.total}"
                f"  {cyan}+{reset}/{cyan}-{reset}: "
                f"{jobs_str} jobs"
                f"  {cyan}/{reset}: filter  {cyan}v{reset}: logs"
                f"  {cyan}n{reset}/{cyan}p{reset}: next/prev"
            )
            if spack.util.tty.color.clen(long_header) < max_width:
                self._println(buffer, long_header)
            else:
                self._println(buffer, f"{bold}Progress:{reset} {self.completed}/{self.total}")

        if self.blocked and not has_unfinished:
            self._println(buffer, "Waiting for other Spack install process...")

        displayed_builds = (
            [b for b in self.builds.values() if self._is_displayed(b)]
            if self.search_term
            else self.builds.values()
        )
        len_builds = len(displayed_builds)

        # Truncate if we have more builds than fit on the screen. In that case we have to reserve
        # an additional line for the "N more..." message.
        truncate_at = max_height - 3 if len_builds + 2 > max_height else len_builds

        for i, build in enumerate(displayed_builds, 1):
            if i > truncate_at:
                self._println(buffer, f"{len_builds - i + 1} more...")
                break
            self._render_build(build, buffer, max_width, now=now)
            self._println(buffer)

        if self.search_mode:
            buffer.write(f"filter> {self.search_term}\033[K")

        # Clear any remaining lines from previous display
        buffer.write("\033[0J")

        # Print everything at once to avoid flickering
        self.stdout.write(buffer.getvalue())
        self.stdout.flush()

        # Update the number of lines drawn for next time. It reflects the number of active builds.
        self.active_area_rows = self.total_lines
        self.dirty = False

        # Schedule next UI update
        self.next_update = now + SPINNER_INTERVAL / 2

        if finalize:
            self._update_terminal_title(True)

    def _println(self, buffer: io.StringIO, line: str = "", force_newline: bool = False) -> None:
        """Print a line to the buffer, handling line clearing and cursor movement."""
        self.total_lines += 1
        if line:
            buffer.write(line)
        if self.total_lines > self.active_area_rows or force_newline:
            buffer.write("\033[0m\033[K\n")  # reset, clear to EOL, newline
        else:
            buffer.write("\033[0m\033[K\033[1B\r")  # reset, clear to EOL, move to next line

    def on_log_output(self, build_id: str, data: bytes) -> None:
        if self.headless:
            return
        # Discard logs we are not following. Generally this should not happen as we tell the child
        # to only send logs when we are following it. It could maybe happen while transitioning
        # between builds.
        if build_id != self.tracked_build_id:
            return
        if self.filter_padding:
            data = padding_filter_bytes(data)
        self.stdout.buffer.write(data)
        self.stdout.flush()
        self.log_ends_with_newline = data.endswith(b"\n")

    def _render_build(
        self, build_info: BuildInfo, buffer: io.StringIO, max_width: int = 0, now: float = 0.0
    ) -> None:
        """Print a single build line to the buffer, truncating to max_width (if > 0)."""
        line_width = 0
        for component in self._generate_line_components(build_info, now=now):
            # ANSI escape sequence(s), does not contribute to width
            if not component.startswith("\033") and max_width > 0:
                line_width += len(component)
                if line_width > max_width:
                    break
            buffer.write(component)

    def _generate_line_components(
        self, build_info: BuildInfo, static: bool = False, now: float = 0.0
    ) -> Generator[str, None, None]:
        """Yield formatted line components for a package. Escape sequences are yielded as separate
        strings so they do not contribute to the line width."""
        if build_info.external:
            indicator = "[e]"
        elif build_info.state == "finished":
            indicator = "[+]"
        elif build_info.state == "failed":
            indicator = "[x]"
        elif static:
            indicator = "[ ]"
        else:
            indicator = f"[{SPINNER_CHARS[self.spinner_index]}]"

        gray, reset = self.gray, self.reset

        if build_info.state == "failed":
            yield self.red
        elif build_info.state == "finished":
            yield self.green

        yield indicator
        yield reset
        yield " "
        yield gray
        yield build_info.hash
        yield reset
        yield " "

        # Package name in bold if explicit, default otherwise
        if build_info.explicit:
            yield self.bold
            yield build_info.name
            yield reset
        else:
            yield build_info.name

        yield self.cyan
        yield f"@{build_info.version}"
        yield reset

        # progress or state
        if build_info.progress_percent is not None:
            yield " fetching"
            yield f": {build_info.progress_percent}%"
        elif build_info.state == "finished":
            prefix = build_info.prefix
            yield f" {padding_filter(prefix) if self.filter_padding else prefix}"
        elif build_info.state == "failed":
            yield " failed"
            if build_info.log_path:
                yield f": {build_info.log_path}"
        else:
            yield f" {build_info.state}"

        # Duration
        elapsed = (
            build_info.duration
            if build_info.duration is not None
            else (now - build_info.start_time)
        )
        if elapsed > 0:
            yield gray
            yield f" ({pretty_duration(elapsed)})"
            yield reset

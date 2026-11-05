# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Terminal installer UI with selected logs above the progress overview."""

import io
from collections import deque
from typing import Deque, Dict, Generator, NamedTuple, Optional

from spack.installer.ui import SPINNER_INTERVAL, BuildInfo, ChangeJobs, SetEcho, TerminalUI
from spack.util.lang import pretty_duration
from spack.util.path import padding_filter, padding_filter_bytes

LOG_HISTORY_SIZE = 15


class BuildProgress(NamedTuple):
    percent: Optional[str] = None
    message: Optional[str] = None


def setup() -> type:
    """Return the streaming UI when the required terminal UI API is available."""
    required = ("_render_overview", "_tracked_build_finished", "_generate_state_components")
    missing = [name for name in required if not callable(getattr(TerminalUI, name, None))]
    if missing:
        raise RuntimeError(f"incompatible terminal UI API: missing {', '.join(missing)}")
    return StreamingTerminalUI


class StreamingTerminalUI(TerminalUI):
    """Keep the progress overview visible while following build logs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_streaming = kwargs.get("verbose", args[7] if len(args) > 7 else False)
        self.log_history: Dict[str, Deque[bytes]] = {}
        self.progress: Dict[str, BuildProgress] = {}
        self.log_stream_buffer = b""

    def refresh_interval(self) -> Optional[float]:
        # Periodic redraws only advance a visible spinner; other modes have nothing to redraw.
        if self.overview_mode and self.is_tty and not self.headless:
            return SPINNER_INTERVAL
        return None

    def on_build_added(self, info: BuildInfo) -> None:
        """Add a build, initialize its log history, and enable required log forwarding."""
        info.start_time = int(self.get_time())
        self.builds[info.id] = info
        self.log_history[info.id] = deque(maxlen=LOG_HISTORY_SIZE)
        self.dirty = True
        if self.log_streaming and not self.tracked_build_id:
            self.log_stream_buffer = b""
            self.log_ends_with_newline = True
            self.tracked_build_id = info.id
            self.commands.append(SetEcho(info.id, True))
        # TTY builds forward logs so the overview can parse progress after mode changes.
        elif self.is_tty:
            self.commands.append(SetEcho(info.id, True))

    def on_build_removed(self, build_id: str) -> None:
        """Remove a build, its retained log history, and any tracking state."""
        if self.tracked_build_id == build_id:
            self.log_stream_buffer = b""
            self.log_ends_with_newline = True
        super().on_build_removed(build_id)
        self.log_history.pop(build_id, None)
        self.progress.pop(build_id, None)

    def on_state_changed(self, build_id: str, state: str) -> None:
        self.progress.pop(build_id, None)
        super().on_state_changed(build_id, state)

    def on_progress(self, build_id: str, current: int, total: int) -> None:
        self._set_progress(build_id, BuildProgress(f"{int(current / total * 100)}%", "fetching"))

    def _set_progress(self, build_id: str, progress: Optional[BuildProgress]) -> None:
        if self.progress.get(build_id) != progress:
            if progress is None:
                self.progress.pop(build_id, None)
            else:
                self.progress[build_id] = progress
            self.dirty = True

    def _progress_prefix(self, build_info: BuildInfo) -> Optional[str]:
        progress = self.progress.get(build_info.id)
        return progress.percent if progress else None

    def _generate_state_components(
        self, build_info: BuildInfo, now: float
    ) -> Generator[str, None, None]:
        if build_info.state == "finished":
            prefix = build_info.prefix
            yield f" {padding_filter(prefix) if self.filter_padding else prefix}"
        elif build_info.state == "failed":
            yield " failed"
            if build_info.log_path:
                yield f": {build_info.log_path}"
        else:
            yield f" {build_info.state}"

        progress = self.progress.get(build_info.id)
        if build_info.state in ("finished", "failed"):
            progress = None
        elapsed = (
            build_info.duration if build_info.duration is not None else now - build_info.start_time
        )
        timing = [pretty_duration(elapsed)] if elapsed > 0 else []
        if progress and progress.percent:
            timing.append(progress.percent)
        if timing:
            yield f"{self.color.BLACK_BRIGHT} ({', '.join(timing)}){self.color.RESET}"
        if progress and progress.message:
            yield f" {progress.message}"

    def toggle(self) -> None:
        """Toggle selected-log streaming, showing stored summaries for failed builds."""
        if not self.log_streaming:
            already_tracked = bool(self.tracked_build_id)
            if not self.tracked_build_id:
                self.next()
            if not self.tracked_build_id:
                return
            tracked_build = self.builds.get(self.tracked_build_id)
            if tracked_build is not None and tracked_build.state == "failed":
                if already_tracked:
                    summary = self._failed_log_summary(tracked_build)
                    if self.is_tty and self.overview_mode:
                        self._redraw_overview_with_log_history(
                            self.tracked_build_id, summary.encode()
                        )
                    else:
                        self.stdout.write(summary)
                        self.stdout.flush()
                return
            self.log_streaming = True
            self.dirty = True
            if not self.is_tty:
                self.commands.append(SetEcho(self.tracked_build_id, True))
            else:
                self._redraw_overview_with_log_history(self.tracked_build_id)
        else:
            if self.log_stream_buffer:
                self.log_stream_buffer = b""
                self.log_ends_with_newline = True
            elif not self.log_ends_with_newline:
                self.stdout.buffer.write(b"\n")
                self.log_ends_with_newline = True
            self.search_term = ""
            self.search_mode = False
            self.log_streaming = False
            self.dirty = True
            if self.tracked_build_id and not self.is_tty:
                self.commands.append(SetEcho(self.tracked_build_id, False))
            elif self.is_tty:
                self._redraw_overview_with_log_history("")

    def _toggle_overview(self) -> None:
        """Return from the legacy full-screen log display to the overview."""
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
            if not self.is_tty:
                self.commands.append(SetEcho(self.tracked_build_id, False))
            self.tracked_build_id = ""

    def on_input(self, chars: str) -> None:
        """Dispatch keyboard input to search, navigation, and parallelism actions."""
        for char in chars:
            overview = self.overview_mode
            if overview and self.search_mode:
                self.search_input(char)
            elif overview and char == "/":
                self.enter_search()
            elif char == "v":
                self.toggle()
            elif char == "q" and self.log_streaming:
                self.toggle()
            elif char in ("q", "\x1b") and not overview:
                self._toggle_overview()
            elif char == "n":
                self.next(1)
            elif char == "p" or char == "N":
                self.next(-1)
            elif char == "+":
                self.commands.append(ChangeJobs(1))
            elif char == "-":
                self.commands.append(ChangeJobs(-1))

    def next(self, direction: int = 1) -> None:
        """Select another unfinished or failed build and show its logs when streaming."""
        new_build_id = self._get_next(direction)

        if not new_build_id or self.tracked_build_id == new_build_id:
            return

        self.log_stream_buffer = b""
        new_build = self.builds[new_build_id]

        # Non-TTY output must stop forwarding the previous build before switching.
        if self.tracked_build_id and self.log_streaming and not self.is_tty:
            self.commands.append(SetEcho(self.tracked_build_id, False))

        self.tracked_build_id = new_build_id

        prefix = "" if self.log_ends_with_newline else "\n"

        if new_build.state == "failed":
            summary = self._failed_log_summary(new_build, prefix=prefix)
            if self.is_tty and self.overview_mode:
                self._redraw_overview_with_log_history(new_build_id, summary.encode())
            else:
                self.stdout.write(summary)
                self.stdout.flush()
        elif self.log_streaming:
            self.commands.append(SetEcho(new_build_id, True))
            if self.is_tty:
                self._redraw_overview_with_log_history(new_build_id)

    def _failed_log_summary(self, build: BuildInfo, prefix: str = "") -> str:
        """Format a failed build's stored summary and mark output as newline-terminated."""
        version = f"{self.color.CYAN}@{build.version}{self.color.RESET}"
        output = io.StringIO()
        output.write(f"{prefix}==> Log summary of {build.name}{version}\n")
        if build.log_summary:
            output.write(build.log_summary)
        if build.log_path:
            output.write(
                "Full log: " if build.log_summary else "No errors parsed from log, see full log: "
            )
            output.write(f"{build.log_path}\n")
        self.log_ends_with_newline = True
        return output.getvalue()

    def _tracked_build_finished(self, state: str) -> None:
        self.log_stream_buffer = b""
        self.log_ends_with_newline = True
        self.tracked_build_id = ""
        if state == "finished" and self.log_streaming:
            self.next()
        else:
            self.log_streaming = False

    def _overview_header_suffix(self) -> str:
        tracked_build = self.builds.get(self.tracked_build_id)
        if tracked_build:
            return f"  {self.color.BLACK_BRIGHT}({tracked_build.name}){self.color.RESET}"
        return ""

    def on_log_output(self, build_id: str, data: bytes) -> None:
        """Cache forwarded log chunks and stream selected output above the TTY overview."""
        if self.headless:
            return
        if self.filter_padding:
            data = padding_filter_bytes(data)
        self.log_history.setdefault(build_id, deque(maxlen=LOG_HISTORY_SIZE)).append(data)
        if self.overview_mode and self.is_tty:
            if not (self.log_streaming and build_id == self.tracked_build_id):
                return
        # Do not write output from an unselected build. TTY output has already been retained above
        # for replay and progress processing.
        if build_id != self.tracked_build_id:
            return
        if self.overview_mode and self.is_tty:
            data = self.log_stream_buffer + data
            last_newline = data.rfind(b"\n")
            if last_newline < 0:
                self.log_stream_buffer = data
                self.log_ends_with_newline = False
                return
            self.log_stream_buffer = data[last_newline + 1 :]
            data = data[: last_newline + 1]
            self.log_ends_with_newline = not self.log_stream_buffer
            now = self.get_time()
            if self.active_area_rows > 0:
                self.stdout.write(f"\033[{self.active_area_rows}A\r\033[0J")
            self.stdout.flush()
        self.stdout.buffer.write(data)
        if self.overview_mode and self.is_tty:
            self.dirty = True
            self.active_area_rows = 0
            has_unfinished = any(pkg.finished_time is None for pkg in self.builds.values())
            self._render_overview(now=now, has_unfinished=has_unfinished)
        else:
            self.log_ends_with_newline = data.endswith(b"\n")
        self.stdout.flush()

    def _redraw_overview_with_log_history(
        self, build_id: str, output: Optional[bytes] = None
    ) -> None:
        """Clear the TTY, replay cached output with a final newline, and redraw the overview."""
        if self.headless or not self.is_tty:
            return
        self.log_stream_buffer = b""
        history = (output,) if output is not None else self.log_history.get(build_id, ())
        history_rows = sum(chunk.count(b"\n") for chunk in history)
        history_needs_newline = bool(history and not history[-1].endswith(b"\n"))

        # Wrapped log lines make relative clearing unreliable. Preserve the cursor below the
        # overview, clear the full display, and restore that exact position before redrawing it.
        self.stdout.write("\0337\033[2J")
        if history:
            rows_above = self.active_area_rows + history_rows + int(history_needs_newline)
            self.stdout.write(f"\033[{rows_above}A\r")
        self.stdout.flush()
        for chunk in history:
            self.stdout.buffer.write(chunk)
        if history_needs_newline:
            self.stdout.buffer.write(b"\n")
        self.log_ends_with_newline = True
        self.stdout.write("\0338")
        now = self.get_time()
        self.dirty = True
        has_unfinished = any(pkg.finished_time is None for pkg in self.builds.values())
        self._render_overview(now=now, has_unfinished=has_unfinished)
        self.stdout.flush()

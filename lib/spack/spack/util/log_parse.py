# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
from typing import List, TextIO, Tuple, Union

from spack.llnl.util.tty.color import cescape, colorize
from spack.util.ctest_log_parser import BuildError, BuildWarning, CTestLogParser, LogEvent

__all__ = ["parse_log_events", "make_log_context"]


def parse_log_events(
    stream: Union[str, TextIO], context: int = 6, profile: bool = False, tail: int = 0
) -> Tuple[List[BuildError], List[BuildWarning], Union[LogEvent, None]]:
    """Extract interesting events from a log file.

    Args:
        stream: build log name or file object
        context: lines of context to extract around each log event
        profile: print out profile information for parsing
        tail: if > 0, also return the last ``tail`` lines

    Returns:
        two lists containing :class:`~spack.util.ctest_log_parser.BuildError` and
        :class:`~spack.util.ctest_log_parser.BuildWarning` objects, plus an optional
        :class:`~spack.util.ctest_log_parser.LogEvent` for the tail (None when ``tail=0``).

    This is a wrapper around :class:`~spack.util.ctest_log_parser.CTestLogParser` that
    lazily constructs a single ``CTestLogParser`` object.  This ensures
    that all the regex compilation is only done once.
    """
    parser = getattr(parse_log_events, "ctest_parser", None)
    if parser is None:
        parser = CTestLogParser(profile=profile)
        setattr(parse_log_events, "ctest_parser", parser)

    result = parser.parse(stream, context, tail)
    if profile:
        parser.print_timings()
    return result


#: lazily constructed CTest log parser
parse_log_events.ctest_parser = None  # type: ignore[attr-defined]


def make_log_context(log_events: List[LogEvent]) -> str:
    """Get error context from a log file.

    Args:
        log_events: list of events created by ``ctest_log_parser.parse()``

    Returns:
        str: context from the build log with errors highlighted

    Parses the log file for lines containing errors, and prints them out with context.
    Errors are highlighted in red and warnings in yellow. Events are sorted by line number.
    """
    event_colors = {e.line_no: e.color for e in log_events if e.color}
    log_events = sorted(log_events, key=lambda e: e.line_no)

    out = io.StringIO()
    next_line = 1
    block_start = -1
    block_lines: List[str] = []

    def flush_block():
        block_end = block_start + len(block_lines) - 1
        out.write(colorize("@c{-- lines %d to %d --}\n" % (block_start, block_end)))
        out.writelines(block_lines)
        block_lines.clear()

    for event in log_events:
        start = event.start

        if start < next_line:
            start = next_line
        elif block_lines:
            flush_block()

        if not block_lines:
            block_start = start

        for i in range(start, event.end):
            if i in event_colors:
                color = event_colors[i]
                block_lines.append(colorize("@%s{> %s}\n" % (color, cescape(event[i]))))
            else:
                block_lines.append("  %s\n" % event[i])

        next_line = event.end

    if block_lines:
        flush_block()

    return out.getvalue()

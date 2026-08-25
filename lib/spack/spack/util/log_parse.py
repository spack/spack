# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Container, Iterator, List, Optional, TextIO, Union

from spack.util.ctest_log_parser import ALL_SEVERITIES, Block, CTestLogParser, Severity
from spack.util.tty.color import cescape, colorize

__all__ = ["scan_log", "write_block", "write_log_context"]


_PARSER: Optional[CTestLogParser] = None


def scan_log(
    stream: Union[str, TextIO, List[str]],
    context: int = 6,
    tail: int = 0,
    severities: Container[Severity] = ALL_SEVERITIES,
    profile: bool = False,
) -> Iterator[Block]:
    """Scan a build log for errors and warnings and yield the blocks worth showing.

    Args:
        stream: build log name or file object
        context: lines of context to show around each matched line
        tail: also show the last this many lines, whether or not anything matched
        severities: only match lines of these severities
        profile: print out profile information for parsing

    Yields:
        :class:`~spack.util.ctest_log_parser.Block` objects in increasing line order.
    """
    global _PARSER
    if profile:
        parser = CTestLogParser(profile=True)
    elif _PARSER is None:
        _PARSER = parser = CTestLogParser()
    else:
        parser = _PARSER

    yield from parser.scan(stream, context, tail, severities)

    if profile:
        parser.print_timings()


def write_block(out: TextIO, block: Block) -> None:
    """Write a block of log lines to a stream, under a header giving its line range.

    Matched lines are prefixed with a ``>``, red for errors and yellow for warnings; the lines of
    context around them are indented instead.
    """
    out.write(colorize("@c{-- lines %d to %d --}\n" % (block.start, block.end)))
    for line_no, text in enumerate(block.lines, block.start):
        match = block.matches.get(line_no)
        if match is None:
            out.write("  %s\n" % text)
        else:
            out.write(colorize("@%s{> %s}\n" % (match.severity.value, cescape(text))))


def write_log_context(
    out: TextIO, stream: Union[str, TextIO, List[str]], context: int = 6, tail: int = 0
) -> None:
    """Write the interesting parts of a build log to a stream."""
    for block in scan_log(stream, context, tail):
        write_block(out, block)

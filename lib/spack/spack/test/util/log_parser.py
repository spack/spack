# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import pathlib
import re
from typing import List

import pytest

from spack.util.ctest_log_parser import Block, CTestLogParser, Severity, _optimize_regexes
from spack.util.log_parse import write_log_context
from spack.util.tty.color import color_when


def render(stream, **kwargs) -> str:
    """Render a log the way the installer and spack log-parse do."""
    out = io.StringIO()
    write_log_context(out, stream, **kwargs)
    return out.getvalue()


def severities(blocks: List[Block]) -> List[Severity]:
    """All matched severities of a list of blocks, in line order."""
    return [match.severity for block in blocks for match in block.matches.values()]


def test_log_parser(tmp_path: pathlib.Path):
    log_file = tmp_path / "log.txt"

    with log_file.open("w") as f:
        f.write(
            """#!/bin/sh\n
checking build system type... x86_64-apple-darwin16.6.0
checking host system type... x86_64-apple-darwin16.6.0
error: weird_error.c:145: something weird happened                          E
checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang
checking whether the C compiler works... yes
/var/tmp/build/foo.py:60: warning: some weird warning                       W
checking for C compiler default output file name... a.out
ld: fatal: linker thing happened                                            E
checking for suffix of executables...
configure: error: in /path/to/some/file:                                    E
configure: error: cannot run C compiled programs.                           E
"""
        )

    parser = CTestLogParser()
    blocks = list(parser.scan(str(log_file)))

    assert severities(blocks) == [
        Severity.ERROR,
        Severity.WARNING,
        Severity.ERROR,
        Severity.ERROR,
        Severity.ERROR,
    ]

    # every matched line is the one the log marks with a trailing E or W
    for block in blocks:
        for line_no in block.matches:
            assert block.lines[line_no - block.start].endswith(("E", "W"))


def test_log_parser_stream():
    """scan() accepts a file-like object."""
    log = io.StringIO(
        "error: weird_error.c:145: something weird happened                 E\n"
        "checking for gcc... irrelevant line\n"
        "/var/tmp/build/foo.py:60: warning: some weird warning              W\n"
    )
    blocks = list(CTestLogParser().scan(log))

    assert severities(blocks) == [Severity.ERROR, Severity.WARNING]


def test_log_parser_preserves_leading_whitespace():
    """Leading whitespace (e.g. compiler caret underlines) must not be stripped."""
    log = io.StringIO(
        "/path/to/file.c:10: error: use of undeclared identifier 'x'\n"
        "    int y = x + 1;\n"
        "            ^\n"
    )
    (block,) = CTestLogParser().scan(log, context=6)

    assert block.lines == [
        "/path/to/file.c:10: error: use of undeclared identifier 'x'",
        "    int y = x + 1;",
        "            ^",
    ]


def test_source_file_of_match():
    """A match records the file and line number the compiler pointed at."""
    log = io.StringIO("/path/to/file.c:10: error: use of undeclared identifier 'x'\n")
    (block,) = CTestLogParser().scan(log, context=0)

    assert block.matches[1].source_file == "/path/to/file.c"
    assert block.matches[1].source_line_no == "10"


def test_merges_overlapping_events(tmp_path: pathlib.Path):
    """Overlapping or adjacent context windows should produce a single merged block."""

    # Two errors close together: lines 5 and 10 with context=3 means windows overlap.
    lines = [f"line {i}\n" for i in range(1, 21)]
    lines[4] = "error: first problem\n"  # line 5
    lines[9] = "error: second problem\n"  # line 10

    log_file = tmp_path / "log.txt"
    log_file.write_text("".join(lines))

    (block,) = CTestLogParser().scan(str(log_file), context=3)

    assert (block.start, block.end) == (2, 13)
    assert sorted(block.matches) == [5, 10]

    # Should be exactly one header for the merged block, not two.
    output = render(str(log_file), context=3)
    assert output.count("-- lines") == 1
    assert "-- lines 2 to 13 --" in output


def test_separate_blocks_when_windows_do_not_touch(tmp_path: pathlib.Path):
    """Errors far apart get one block each."""
    lines = [f"line {i}\n" for i in range(1, 41)]
    lines[4] = "error: first problem\n"  # line 5
    lines[34] = "error: second problem\n"  # line 35

    log_file = tmp_path / "log.txt"
    log_file.write_text("".join(lines))

    first, second = CTestLogParser().scan(str(log_file), context=3)

    assert (first.start, first.end) == (2, 8)
    assert (second.start, second.end) == (32, 38)


def test_warning_in_error_context_keeps_yellow(tmp_path: pathlib.Path):
    """A warning line inside an error's context window must be highlighted yellow, not red."""
    # Line 5 = error, line 8 = warning, context=3 so error window covers lines 2-11
    # meaning the warning at line 8 falls inside the error's context.
    lines = [f"line {i}\n" for i in range(1, 16)]
    lines[4] = "error: something broke\n"  # line 5
    lines[7] = "/tmp/foo.c:1: warning: something fishy\n"  # line 8

    log_file = tmp_path / "log.txt"
    log_file.write_text("".join(lines))

    with color_when("always"):
        output = render(str(log_file), context=3)

    # The error line should be red (ANSI 91), the warning yellow (ANSI 93).
    assert "\x1b[0;91m> " in output and "something broke" in output
    assert "\x1b[0;93m> " in output and "something fishy" in output


def test_severity_filter(tmp_path: pathlib.Path):
    """Filtering by severity drops the other severity's matches and their context."""
    lines = [f"line {i}\n" for i in range(1, 41)]
    lines[4] = "error: something broke\n"  # line 5
    lines[34] = "/tmp/foo.c:1: warning: something fishy\n"  # line 35

    log_file = tmp_path / "log.txt"
    log_file.write_text("".join(lines))

    (block,) = CTestLogParser().scan(str(log_file), context=3, severities={Severity.WARNING})

    assert (block.start, block.end) == (32, 38)
    assert severities([block]) == [Severity.WARNING]


def test_log_parser_non_utf8_bytes(tmp_path: pathlib.Path):
    """scan() does not raise UnicodeDecodeError on non-UTF-8 log files."""
    log_file = tmp_path / "log.bin"
    log_file.write_bytes(b"checking things...\nerror: \x80\xff something broke\ndone\n")

    (block,) = CTestLogParser().scan(str(log_file))

    assert severities([block]) == [Severity.ERROR]


def test_tail_renders_as_plain_context():
    """Tail lines with no match render as plain context with no highlighting."""
    log = io.StringIO("".join(f"tail line {i}\n" for i in range(1, 4)))

    with color_when(False):
        output = render(log, tail=3)

    assert "-- lines 1 to 3 --" in output
    # All lines should be plain context (indented with two spaces, no "> " prefix)
    assert "  tail line 1\n" in output
    assert "  tail line 2\n" in output
    assert "  tail line 3\n" in output
    assert "> " not in output


def test_tail_overlapping_with_error():
    """Tail lines overlapping with an error's context should not be duplicated."""
    log = io.StringIO("line 1\nline 2\nline 3\nerror: something broke\nline 5\nline 6\nline 7\n")

    with color_when(False):
        output = render(log, context=2, tail=3)

    # "line 5" and "line 6" appear in both the error context and the tail,
    # but should only appear once in the output
    assert output.count("line 5") == 1
    assert output.count("line 6") == 1
    assert output.count("line 7") == 1
    assert output.count("-- lines") == 1


def test_tail_detached_from_error():
    """A tail far away from the last match is a block of its own."""
    lines = [f"line {i}\n" for i in range(1, 41)]
    lines[4] = "error: something broke\n"  # line 5

    first, second = CTestLogParser().scan(lines, context=2, tail=3)

    assert (first.start, first.end) == (3, 7)
    assert (second.start, second.end) == (38, 40)


def test_tail_only():
    """A log with no errors or warnings renders its tail."""
    log = io.StringIO("final line 1\nfinal line 2\n")

    with color_when(False):
        output = render(log, tail=2)

    assert "-- lines 1 to 2 --" in output
    assert "  final line 1\n" in output
    assert "  final line 2\n" in output


def test_empty_log():
    """An empty log produces no blocks and no output."""
    assert list(CTestLogParser().scan(io.StringIO(""), tail=20)) == []
    assert render(io.StringIO(""), tail=20) == ""


def test_negative_context_or_tail_raises():
    with pytest.raises(ValueError, match="non-negative"):
        list(CTestLogParser().scan(io.StringIO("error: nope\n"), context=-1))
    with pytest.raises(ValueError, match="non-negative"):
        list(CTestLogParser().scan(io.StringIO("error: nope\n"), tail=-1))


class TestOptimizeRegexes:
    def test_groups_by_first_char(self):
        """Regexes sharing a first character are combined into one."""
        result = _optimize_regexes(["bar", "far", "foo"])
        assert len(result) == 2
        assert result == ["bar", "far|foo"]

    def test_singletons_unchanged(self):
        """A regex that is the only one with its prefix is kept as-is."""
        result = _optimize_regexes(["^unique pattern"])
        assert result == ["^unique pattern"]

    def test_escaping(self):
        """Regexes starting with the same metacharacter are grouped too."""
        result = _optimize_regexes(["\\(foo\\)", "\\(bar\\)", "\\*", "[abc]"])
        assert len(result) == 3
        assert "\\(bar\\)|\\(foo\\)" in result
        assert "\\*" in result
        assert "[abc]" in result

    def test_semantics_preserved(self):
        """Optimized regexes match the same strings as the originals."""
        originals = [
            "^FAIL: ",
            "^FATAL: ",
            "^failed ",
            ": error",
            ": warning",
            "make: Fatal error",
            "make\\[.*\\]: \\*\\*\\*",
        ]
        test_lines = [
            "FAIL: test_something",
            "FATAL: crash",
            "failed to build",
            "foo.c: error: syntax",
            "foo.c: warning: unused",
            "make: Fatal error in target",
            "make[1]: *** Error 1",
            "this matches nothing",
        ]
        compiled_orig = [re.compile(r) for r in originals]
        compiled_opt = [re.compile(r) for r in _optimize_regexes(originals)]

        for line in test_lines:
            orig_match = any(r.search(line) for r in compiled_orig)
            opt_match = any(r.search(line) for r in compiled_opt)
            assert orig_match == opt_match, f"mismatch on {line!r}"

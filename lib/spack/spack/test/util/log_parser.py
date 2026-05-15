# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import pathlib
import re

from spack.llnl.util.tty.color import color_when
from spack.util.ctest_log_parser import CTestLogParser, LogEvent, _optimize_regexes
from spack.util.log_parse import make_log_context


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
    errors, warnings, _ = parser.parse(str(log_file))

    assert len(errors) == 4
    assert all(e.text.endswith("E") for e in errors)

    assert len(warnings) == 1
    assert all(w.text.endswith("W") for w in warnings)


def test_log_parser_stream():
    """parse() accepts a file-like object."""
    log = io.StringIO(
        "error: weird_error.c:145: something weird happened                 E\n"
        "checking for gcc... irrelevant line\n"
        "/var/tmp/build/foo.py:60: warning: some weird warning              W\n"
    )
    parser = CTestLogParser()
    errors, warnings, _ = parser.parse(log)

    assert len(errors) == 1
    assert errors[0].text.endswith("E")
    assert len(warnings) == 1
    assert warnings[0].text.endswith("W")


def test_log_parser_preserves_leading_whitespace():
    """Leading whitespace (e.g. compiler caret underlines) must not be stripped."""
    log = io.StringIO(
        "/path/to/file.c:10: error: use of undeclared identifier 'x'\n"
        "    int y = x + 1;\n"
        "            ^\n"
    )
    parser = CTestLogParser()
    errors, _, _ = parser.parse(log, context=6)

    assert len(errors) == 1
    assert errors[0].post_context[0] == "    int y = x + 1;"
    assert errors[0].post_context[1] == "            ^"


def test_make_log_context_merges_overlapping_events(tmp_path: pathlib.Path):
    """Overlapping or adjacent context windows should produce a single merged block."""

    # Two errors close together: lines 5 and 10 with context=3 means windows overlap.
    lines = [f"line {i}\n" for i in range(1, 21)]
    lines[4] = "error: first problem\n"  # line 5
    lines[9] = "error: second problem\n"  # line 10

    log_file = tmp_path / "log.txt"
    log_file.write_text("".join(lines))

    parser = CTestLogParser()
    errors, warnings, _ = parser.parse(str(log_file), context=3)

    log_events = sorted([*errors, *warnings], key=lambda e: e.line_no)
    output = make_log_context(log_events)

    # Should be exactly one header for the merged block, not two.
    assert output.count("-- lines") == 1

    # The header should cover the full merged range.
    assert "-- lines 2 to 13 --" in output


def test_make_log_context_warning_in_error_context_keeps_yellow(tmp_path: pathlib.Path):
    """A warning line inside an error's context window must be highlighted yellow, not red."""
    # Line 5 = error, line 8 = warning, context=3 so error window covers lines 2-11
    # meaning the warning at line 8 falls inside the error's context.
    lines = [f"line {i}\n" for i in range(1, 16)]
    lines[4] = "error: something broke\n"  # line 5
    lines[7] = "/tmp/foo.c:1: warning: something fishy\n"  # line 8

    log_file = tmp_path / "log.txt"
    log_file.write_text("".join(lines))

    parser = CTestLogParser()
    errors, warnings, _ = parser.parse(str(log_file), context=3)

    assert len(errors) == len(warnings) == 1

    log_events = sorted([*errors, *warnings], key=lambda e: e.line_no)

    with color_when("always"):
        output = make_log_context(log_events)

    # The error line should be red (ANSI 91), the warning yellow (ANSI 93).
    assert "\x1b[0;91m> " in output and "something broke" in output
    assert "\x1b[0;93m> " in output and "something fishy" in output


def test_log_parser_non_utf8_bytes(tmp_path: pathlib.Path):
    """parse() does not raise UnicodeDecodeError on non-UTF-8 log files."""
    log_file = tmp_path / "log.bin"
    log_file.write_bytes(b"checking things...\nerror: \x80\xff something broke\ndone\n")
    parser = CTestLogParser()
    errors, _, _ = parser.parse(str(log_file))
    assert len(errors) == 1


def test_tail_renders_as_plain_context():
    """A LogEvent should render all lines as plain context with no highlighting."""
    lines = ["tail line 1", "tail line 2", "tail line 3"]
    section = LogEvent(text=lines[-1], line_no=100, pre_context=lines[:-1])

    with color_when(False):
        output = make_log_context([section])

    assert "-- lines 98 to 100 --" in output
    # All lines should be plain context (indented with two spaces, no "> " prefix)
    assert "  tail line 1\n" in output
    assert "  tail line 2\n" in output
    assert "  tail line 3\n" in output
    assert "> " not in output


def test_tail_overlapping_with_error():
    """Tail lines overlapping with an error's context should not be duplicated."""
    log = io.StringIO("line 1\nline 2\nline 3\nerror: something broke\nline 5\nline 6\nline 7\n")
    parser = CTestLogParser()
    errors, _, tail = parser.parse(log, context=2, tail=3)
    assert len(errors) == 1
    assert tail is not None

    with color_when(False):
        output = make_log_context([*errors, tail])

    # "line 5" and "line 6" appear in both the error context and the tail,
    # but should only appear once in the output
    assert output.count("line 5") == 1
    assert output.count("line 6") == 1
    assert output.count("line 7") == 1


def test_tail_only():
    """A LogEvent with no errors/warnings renders correctly."""
    lines = ["final line 1", "final line 2"]
    section = LogEvent(text=lines[-1], line_no=51, pre_context=lines[:-1])

    with color_when(False):
        output = make_log_context([section])

    assert "-- lines 50 to 51 --" in output
    assert "  final line 1\n" in output
    assert "  final line 2\n" in output


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

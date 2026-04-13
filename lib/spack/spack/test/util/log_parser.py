# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import pathlib

from spack.util.ctest_log_parser import CTestLogParser


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
    errors, warnings = parser.parse(str(log_file))

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
    errors, warnings = parser.parse(log)

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
    errors, _ = parser.parse(log, context=6)

    assert len(errors) == 1
    assert errors[0].post_context[0] == "    int y = x + 1;"
    assert errors[0].post_context[1] == "            ^"


def test_log_parser_non_utf8_bytes(tmp_path: pathlib.Path):
    """parse() does not raise UnicodeDecodeError on non-UTF-8 log files."""
    log_file = tmp_path / "log.bin"
    log_file.write_bytes(b"checking things...\nerror: \x80\xff something broke\ndone\n")
    parser = CTestLogParser()
    errors, _ = parser.parse(str(log_file))
    assert len(errors) == 1

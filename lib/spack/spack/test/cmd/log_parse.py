# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import pathlib
import sys

from spack.main import SpackCommand

log_parse = SpackCommand("log-parse")

LOG = b"""line 1
line 2
/path/to/file.c:10: error: use of undeclared identifier 'x'
line 4
line 5
/tmp/foo.c:1: warning: unused variable 'z'
line 7
"""


class FakeStdin:
    """Just enough of sys.stdin for the command to read bytes from it."""

    def __init__(self, data: bytes) -> None:
        self.buffer = io.BytesIO(data)


def test_log_parse_file(tmp_path: pathlib.Path):
    log_file = tmp_path / "build.log"
    log_file.write_bytes(LOG)

    out = log_parse("--show", "errors,warnings", "-c", "1", str(log_file))

    assert "> /path/to/file.c:10: error: use of undeclared identifier 'x'" in out
    assert "> /tmp/foo.c:1: warning: unused variable 'z'" in out
    # Counts are reported after the log, since it is written as it is scanned.
    assert out.rstrip().endswith("1 errors\n1 warnings")


def test_log_parse_stdin(monkeypatch):
    """The log can be read from stdin with -."""
    monkeypatch.setattr(sys, "stdin", FakeStdin(LOG))

    out = log_parse("--show", "warnings", "-c", "1", "-")

    assert "> /tmp/foo.c:1: warning: unused variable 'z'" in out
    assert "1 warnings" in out
    # Only warnings were asked for, so the error is context at most, never highlighted.
    assert "> /path/to/file.c:10:" not in out


def test_log_parse_stdin_non_utf8(monkeypatch):
    """Undecodable bytes on stdin are replaced rather than raising."""
    monkeypatch.setattr(sys, "stdin", FakeStdin(b"ok\nerror: \x80\xff broke\ndone\n"))

    out = log_parse("-c", "1", "-")

    assert "> error:" in out
    assert "1 errors" in out

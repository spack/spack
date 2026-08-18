# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

from spack.util import tty


def test_get_timestamp(monkeypatch):
    """Ensure the results of get_timestamp are reasonable."""

    # Debug disabled should return an empty string
    monkeypatch.setattr(tty, "_debug", 0)
    assert not tty.get_timestamp(False), "Expected an empty string"

    # Debug disabled but force the timestamp should return a string
    assert tty.get_timestamp(True), "Expected a timestamp/non-empty string"

    pid_str = " {0}".format(os.getpid())

    # Level 1 debugging should return a timestamp WITHOUT the pid
    monkeypatch.setattr(tty, "_debug", 1)
    out_str = tty.get_timestamp(False)
    assert out_str and pid_str not in out_str, "Expected no PID in results"

    # Level 2 debugging should also return a timestamp WITH the pid
    monkeypatch.setattr(tty, "_debug", 2)
    out_str = tty.get_timestamp(False)
    assert out_str and pid_str in out_str, "Expected PID in results"


@pytest.mark.parametrize(
    "msg,enabled,trace,newline",
    [
        ("", False, False, False),  # Nothing is output
        (Exception(""), True, False, True),  # Exception  output
        ("trace", True, True, False),  # stacktrace output
        ("newline", True, False, True),  # newline in output
        ("no newline", True, False, False),  # no newline output
    ],
)
def test_msg(capfd, monkeypatch, enabled, msg, trace, newline):
    """Ensure the output from msg with options is appropriate."""

    # temporarily use the parameterized settings
    monkeypatch.setattr(tty, "_msg_enabled", enabled)
    monkeypatch.setattr(tty, "_stacktrace", trace)

    expected = [msg if isinstance(msg, str) else "Exception: "]
    if newline:
        expected[0] = "{0}\n".format(expected[0])
    if trace:
        expected.insert(0, ".py")

    tty.msg(msg, newline=newline)
    out = capfd.readouterr()[0]
    for msg in expected:
        assert msg in out


@pytest.mark.parametrize(
    "msg,trace,wrap",
    [
        (Exception(""), False, False),  # Exception  output
        ("trace", True, False),  # stacktrace output
        ("wrap", False, True),  # wrap in output
    ],
)
def test_info(capfd, monkeypatch, msg, trace, wrap):
    """Ensure the output from info with options is appropriate."""

    # temporarily use the parameterized settings
    monkeypatch.setattr(tty, "_stacktrace", trace)

    expected = [msg if isinstance(msg, str) else "Exception: "]
    if trace:
        expected.insert(0, ".py")

    extra = (
        "This extra argument *should* make for a sufficiently long line"
        " that needs to be wrapped if the option is enabled."
    )
    args = [msg, extra]

    num_newlines = 3 if wrap else 2

    tty.info(*args, wrap=wrap, countback=3)
    out = capfd.readouterr()[0]
    for msg in expected:
        assert msg in out

    assert out.count("\n") == num_newlines


def test_band_fills_the_width_with_dashes():
    """Tests that dashes run out to the requested width."""
    line = tty.band("label", 40, indent=2)
    assert line == "  -- label " + "-" * 29
    assert len(line) == 40


def test_band_omits_the_dashes_when_there_is_no_room_for_them():
    """Tests that an empty run of dashes must not be colorized."""
    line = tty.band("a label wider than the width it is given", 20, indent=2)
    assert line == "  -- a label wider than the width it is given"

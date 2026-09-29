# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import re
import sys
import textwrap

import pytest

from spack.util.tty import color
from spack.util.tty.color import cescape, colorize, csub

#: "red" with and without ANSI codes, as written by ``cwrite("@r{red}")``
RED = "\033[0;31mred\033[0m"
PLAIN = "red"

test_text = [
    "@r{The quick brown fox jumps over the lazy yellow dog.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
    "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco "
    "laboris nisi ut aliquip ex ea commodo consequat.}",
    "@c{none, gfx1010, gfx1011, gfx1012, gfx1013, gfx1030, gfx1031, gfx1032, gfx1033, gfx1034}",
    "none, @c{gfx1010}, gfx1011, @r{gfx1012}, gfx1013, @b{gfx1030}, gfx1031, gfx1032, gfx1033",
    "@c{none, 10, 100, 100a, 100f, 101, 101a, 101f, 103, 103a, 103f, 11, 12, 120, 120a, 120f}",
    "@c{none, 10,     100, 100a,   100f, 101, 101a, 101f,    103, 103a,    103f, 11, 12, 120}",
    "none, @c{10},     @b{100}, 100a,   @r{100f}, 101, @g{101a}, 101f,    @c{103}, 103a,    103f"
    "@g{build}, @c{link}, @r{run}",
]


@pytest.mark.parametrize("cols", list(range(30, 101, 10)))
@pytest.mark.parametrize("text", test_text)
@pytest.mark.parametrize("indent", [0, 4, 8])
def test_color_wrap(cols, text, indent):
    colorized = color.colorize(text, color=True)  # True to force color
    plain = color.csub(colorized)

    spaces = indent * " "

    color_wrapped = " ".join(
        color.cwrap(colorized, width=cols, initial_indent=spaces, subsequent_indent=spaces)
    )
    plain_cwrapped = " ".join(
        color.cwrap(plain, width=cols, initial_indent=spaces, subsequent_indent=spaces)
    )
    wrapped = " ".join(
        textwrap.wrap(plain, width=cols, initial_indent=spaces, subsequent_indent=spaces)
    )

    # make sure the concatenated, non-indented wrapped version is the same as the
    # original, modulo any spaces consumed while wrapping.
    assert re.sub(r"\s+", " ", color_wrapped).lstrip() == re.sub(r"\s+", " ", colorized)

    # make sure we wrap the same as textwrap
    assert color.csub(color_wrapped) == wrapped
    assert plain_cwrapped == wrapped


def test_cescape_at_sign_roundtrip():
    """cescape followed by colorize should not double-escape '@' inside color blocks."""
    raw = 'if spec.satisfies("@:25.1"):'
    colorized = colorize("@R{%s}" % cescape(raw), color=True)
    assert csub(colorized) == raw


def test_cescape_multiple_at_signs_roundtrip():
    """Multiple consecutive '@' characters should survive a cescape/colorize roundtrip."""
    raw = "foo @@@@@bar"
    colorized = colorize("@R{%s}" % cescape(raw), color=True)
    assert csub(colorized) == raw


def test_colorize_top_level_consecutive_escaped_ats():
    """Consecutive @@ at the top level (outside braces) must each unescape independently."""
    assert colorize("@@@@", color=False) == "@@"
    assert colorize("@@@@@@", color=False) == "@@@"


class MockStream(io.StringIO):
    """A stream whose ``isatty()`` can be set independently of the underlying buffer."""

    def __init__(self, isatty: bool) -> None:
        super().__init__()
        self._isatty = isatty

    def isatty(self) -> bool:
        return self._isatty


@pytest.mark.parametrize("when,expected", [(True, RED), (False, PLAIN), (None, PLAIN)])
def test_cwrite_follows_the_stream_it_writes_to(monkeypatch, when, expected):
    """Tests that cwrite decides on color from its own stream, not from sys.stdout."""
    monkeypatch.setattr(sys, "stdout", MockStream(isatty=True))
    stream = MockStream(isatty=False)

    with color.color_when(when):
        color.cwrite("@r{red}", stream=stream)

    assert stream.getvalue() == expected


@pytest.mark.parametrize("when,expected", [(True, RED), (False, PLAIN), (None, RED)])
def test_cwrite_color_setting_overrides_a_tty_stream(when, expected):
    stream = MockStream(isatty=True)

    with color.color_when(when):
        color.cwrite("@r{red}", stream=stream)

    assert stream.getvalue() == expected


@pytest.mark.parametrize("when,expected", [(True, RED), (False, PLAIN), (None, PLAIN)])
def test_color_stream_follows_the_stream_it_wraps(monkeypatch, when, expected):
    monkeypatch.setattr(sys, "stdout", MockStream(isatty=True))
    stream = MockStream(isatty=False)

    with color.color_when(when):
        color.ColorStream(stream).write("@r{red}")

    assert stream.getvalue() == expected


class MockFdStream(MockStream):
    """A stream with a file descriptor number and a counting ``isatty()``."""

    def __init__(self, isatty: bool, fd: int) -> None:
        super().__init__(isatty)
        self._fd = fd
        self.isatty_calls = 0

    def fileno(self) -> int:
        return self._fd

    def isatty(self) -> bool:
        self.isatty_calls += 1
        return self._isatty


def test_get_color_when_caches_isatty_of_std_fds():
    """isatty() of fds 0-2 is queried once and re-queried after invalidation."""
    stream = MockFdStream(isatty=True, fd=1)
    try:
        with color.color_when(None):
            assert color.get_color_when(stream) is True
            assert color.get_color_when(stream) is True
        assert stream.isatty_calls == 1

        color.clear_isatty_cache()
        with color.color_when(None):
            assert color.get_color_when(stream) is True
        assert stream.isatty_calls == 2
    finally:
        color.clear_isatty_cache()


def test_get_color_when_does_not_cache_high_fds():
    """Streams on fds above 2 are queried every time and stay out of the cache."""
    stream = MockFdStream(isatty=True, fd=7)
    try:
        with color.color_when(None):
            assert color.get_color_when(stream) is True
            assert color.get_color_when(stream) is True
        assert stream.isatty_calls == 2
        assert 7 not in color._isatty_cache
    finally:
        color.clear_isatty_cache()


def test_get_color_when_does_not_cache_fd_less_streams():
    """Streams without a file descriptor (StringIO) are queried every time, not cached."""
    stream = MockStream(isatty=True)
    try:
        with color.color_when(None):
            assert color.get_color_when(stream) is True
            assert color.get_color_when(stream) is True
        assert not color._isatty_cache
    finally:
        color.clear_isatty_cache()

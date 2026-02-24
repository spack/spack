# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import textwrap

import pytest

import spack.llnl.util.tty.color as color

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

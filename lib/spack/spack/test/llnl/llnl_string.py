# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.llnl.string


@pytest.mark.parametrize(
    "arguments,expected",
    [
        ((0, "thing"), "0 things"),
        ((1, "thing"), "1 thing"),
        ((2, "thing"), "2 things"),
        ((1, "thing", "wombats"), "1 thing"),
        ((2, "thing", "wombats"), "2 wombats"),
        ((2, "thing", "wombats", False), "wombats"),
    ],
)
def test_plural(arguments, expected):
    assert spack.llnl.string.plural(*arguments) == expected


@pytest.mark.parametrize(
    "arguments,expected",
    [((["one", "two"],), ["'one'", "'two'"]), ((["one", "two"], "^"), ["^one^", "^two^"])],
)
def test_quote(arguments, expected):
    assert spack.llnl.string.quote(*arguments) == expected


@pytest.mark.parametrize(
    "input,expected_and,expected_or",
    [
        (["foo"], "foo", "foo"),
        (["foo", "bar"], "foo and bar", "foo or bar"),
        (["foo", "bar", "baz"], "foo, bar, and baz", "foo, bar, or baz"),
    ],
)
def test_comma_and_or(input, expected_and, expected_or):
    assert spack.llnl.string.comma_and(input) == expected_and
    assert spack.llnl.string.comma_or(input) == expected_or

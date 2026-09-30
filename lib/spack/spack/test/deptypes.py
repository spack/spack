# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.deptypes as dt


def test_flag_from_string():
    assert dt.flag_from_string("build") == dt.BUILD
    assert dt.flag_from_string("link") == dt.LINK
    assert dt.flag_from_string("run") == dt.RUN
    assert dt.flag_from_string("test") == dt.TEST

    with pytest.raises(ValueError, match="Invalid dependency type: invalid"):
        dt.flag_from_string("invalid")


def test_flag_from_strings():
    assert dt.flag_from_strings(["build", "link"]) == dt.BUILD | dt.LINK
    assert dt.flag_from_strings(("run", "test")) == dt.RUN | dt.TEST
    assert dt.flag_from_strings([]) == dt.NONE


def test_canonicalize():
    assert dt.canonicalize("all") == dt.ALL
    assert dt.canonicalize(all) == dt.ALL
    assert dt.canonicalize("build") == dt.BUILD
    assert dt.canonicalize(["build", "link"]) == dt.BUILD | dt.LINK

    with pytest.raises(ValueError, match="Invalid dependency type"):
        dt.canonicalize(123)


def test_flag_to_tuple():
    assert dt.flag_to_tuple(dt.BUILD | dt.LINK) == ("build", "link")
    assert dt.flag_to_tuple(dt.ALL) == ("build", "link", "run", "test")
    assert dt.flag_to_tuple(dt.NONE) == ()


def test_flag_to_string():
    assert dt.flag_to_string(dt.BUILD) == "build"
    assert dt.flag_to_string(dt.LINK) == "link"
    assert dt.flag_to_string(dt.RUN) == "run"
    assert dt.flag_to_string(dt.TEST) == "test"

    with pytest.raises(ValueError, match="Invalid dependency type flag"):
        dt.flag_to_string(dt.BUILD | dt.LINK)


def test_flag_to_chars():
    assert dt.flag_to_chars(dt.BUILD) == "b   "
    assert dt.flag_to_chars(dt.LINK) == " l  "
    assert dt.flag_to_chars(dt.RUN) == "  r "
    assert dt.flag_to_chars(dt.TEST) == "   t"
    assert dt.flag_to_chars(dt.BUILD | dt.LINK) == "bl  "
    assert dt.flag_to_chars(dt.ALL) == "blrt"
    assert dt.flag_to_chars(dt.NONE) == "    "

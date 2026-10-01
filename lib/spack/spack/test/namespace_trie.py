# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.util.naming


@pytest.fixture()
def trie():
    return spack.util.naming.NamespaceTrie()


def test_add_single(trie):
    trie["foo"] = "bar"

    assert trie.is_prefix("foo")
    assert trie.has_value("foo")
    assert trie["foo"] == "bar"


def test_add_multiple(trie):
    trie["foo.bar"] = "baz"

    assert not trie.has_value("foo")
    assert trie.is_prefix("foo")

    assert trie.is_prefix("foo.bar")
    assert trie.has_value("foo.bar")
    assert trie["foo.bar"] == "baz"

    assert not trie.is_prefix("foo.bar.baz")
    assert not trie.has_value("foo.bar.baz")


def test_add_three(trie):
    # add a three-level namespace
    trie["foo.bar.baz"] = "quux"

    assert trie.is_prefix("foo")
    assert not trie.has_value("foo")

    assert trie.is_prefix("foo.bar")
    assert not trie.has_value("foo.bar")

    assert trie.is_prefix("foo.bar.baz")
    assert trie.has_value("foo.bar.baz")
    assert trie["foo.bar.baz"] == "quux"

    assert not trie.is_prefix("foo.bar.baz.quux")
    assert not trie.has_value("foo.bar.baz.quux")

    # Try to add a second element in a prefix namespace
    trie["foo.bar"] = "blah"

    assert trie.is_prefix("foo")
    assert not trie.has_value("foo")

    assert trie.is_prefix("foo.bar")
    assert trie.has_value("foo.bar")
    assert trie["foo.bar"] == "blah"

    assert trie.is_prefix("foo.bar.baz")
    assert trie.has_value("foo.bar.baz")
    assert trie["foo.bar.baz"] == "quux"

    assert not trie.is_prefix("foo.bar.baz.quux")
    assert not trie.has_value("foo.bar.baz.quux")


def test_add_none_single(trie):
    trie["foo"] = None
    assert trie.is_prefix("foo")
    assert trie.has_value("foo")
    assert trie["foo"] is None

    assert not trie.is_prefix("foo.bar")
    assert not trie.has_value("foo.bar")


def test_add_none_multiple(trie):
    trie["foo.bar"] = None

    assert trie.is_prefix("foo")
    assert not trie.has_value("foo")

    assert trie.is_prefix("foo.bar")
    assert trie.has_value("foo.bar")
    assert trie["foo.bar"] is None

    assert not trie.is_prefix("foo.bar.baz")
    assert not trie.has_value("foo.bar.baz")


@pytest.mark.parametrize(
    ("name", "simplified"),
    (
        ("simple", "simple"),
        ("with-hyphen", "with-hyphen"),
        ("with_underscore", "with-underscore"),
        ("MixEdCAsE", "mixedcase"),
        ("0", "0"),
        ("plus+", "plus-plus"),
        ("tinkle++", "tinklepp"),
        ("-leading-dash", "leading-dash"),
        ("_leading_underscore", "leading-underscore"),
        ("__leading_underscore", "leading-underscore"),
        ("_0leading_underscore_num", "0leading-underscore-num"),
        ("l_intel_download", "intel-download"),
        ("luapkg", "lua-pkg"),
        ("b++pkg", "bpp-pkg"),
        ("bpppkg", "bpp-pkg"),
    ),
)
def test_naming_simplify_name(name, simplified):
    assert spack.util.naming.simplify_name(name) == simplified


def test_naming_simplify_name_bad_char():
    name = "mm"
    # Assert the test base name good and already simplified
    assert spack.util.naming.is_valid_name(name)
    assert spack.util.naming.simplify_name(name) == name

    for bad_char in (
        "!",
        "#",
        "$",
        "'",
        "(",
        ")",
        "*",
        ",",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "?",
        "@",
        '"',
        "\\",
        "^",
        "`",
        "{",
        "|",
        "}",
        "~",
    ):
        # Bad character prefix
        bad_name = bad_char + name
        simplified_bad_name = spack.util.naming.simplify_name(bad_name)
        assert not spack.util.naming.is_valid_name(bad_name)
        assert simplified_bad_name == bad_name

        # Bad character suffix
        bad_name = bad_char + name
        simplified_bad_name = spack.util.naming.simplify_name(bad_name)
        assert not spack.util.naming.is_valid_name(bad_name)
        assert simplified_bad_name == bad_name

        # Bad character in the middle
        bad_name = name[:1] + bad_char + name[1:]
        simplified_bad_name = spack.util.naming.simplify_name(bad_name)
        assert not spack.util.naming.is_valid_name(bad_name)
        assert simplified_bad_name == bad_name


def test_naming_simplify_name_empty_string():
    assert not spack.util.naming.is_valid_name("")
    assert not spack.util.naming.is_valid_name(spack.util.naming.simplify_name(""))

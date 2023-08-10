# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests various features of :py:class:`spack.util.prefix.Prefix`"""

import os
from pathlib import PurePath

from spack.util.prefix import Prefix


def test_prefix_attributes():
    """Test normal prefix attributes like ``prefix.bin``"""
    prefix = Prefix(os.sep + "usr")
    prefix_path = PurePath("usr")

    assert prefix.bin == os.sep + str(prefix_path / "bin")
    assert prefix.lib == os.sep + str(prefix_path / "lib")
    assert prefix.include == os.sep + str(prefix_path / "include")


def test_prefix_join():
    """Test prefix join  ``prefix.join(...)``"""
    prefix = Prefix(os.sep + "usr")
    prefix_path = PurePath("usr")

    a1 = prefix.join("a_{0}".format(1)).lib64
    a2 = prefix.join("a-{0}".format(1)).lib64
    a3 = prefix.join("a.{0}".format(1)).lib64

    assert a1 == os.sep + str(prefix_path / "a_1" / "lib64")
    assert a2 == os.sep + str(prefix_path / "a-1" / "lib64")
    assert a3 == os.sep + str(prefix_path / "a.1" / "lib64")

    assert isinstance(a1, Prefix)
    assert isinstance(a2, Prefix)
    assert isinstance(a3, Prefix)

    p1 = prefix.bin.join("executable.sh")
    p2 = prefix.share.join("pkg-config").join("foo.pc")
    p3 = prefix.join("dashed-directory").foo

    assert p1 == os.sep + str(prefix_path / "bin" / "executable.sh")
    assert p2 == os.sep + str(prefix_path / "share" / "pkg-config" / "foo.pc")
    assert p3 == os.sep + str(prefix_path / "dashed-directory" / "foo")

    assert isinstance(p1, Prefix)
    assert isinstance(p2, Prefix)
    assert isinstance(p3, Prefix)


def test_multilevel_attributes():
    """Test attributes of attributes, like ``prefix.share.man``"""
    prefix = Prefix(os.sep + "usr" + os.sep)
    prefix_path = PurePath("usr")

    assert prefix.share.man == os.sep + str(prefix_path / "share" / "man")
    assert prefix.man.man8 == os.sep + str(prefix_path / "man" / "man8")
    assert prefix.foo.bar.baz == os.sep + str(prefix_path / "foo" / "bar" / "baz")

    share = prefix.share

    assert isinstance(share, Prefix)
    assert share.man == os.sep + str(prefix_path / "share" / "man")


def test_string_like_behavior():
    """Test string-like behavior of the prefix object"""
    prefix = Prefix(os.sep + "usr")

    assert prefix == os.sep + "usr"
    assert isinstance(prefix, str)

    assert prefix + os.sep + "bin" == os.sep + "usr" + os.sep + "bin"
    assert "--prefix=%s" % prefix == "--prefix=" + prefix
    assert "--prefix={0}".format(prefix) == "--prefix=" + prefix

    assert prefix.find("u", 1)
    assert prefix.upper() == os.sep + "USR"
    assert prefix.lstrip(os.sep) == "usr"

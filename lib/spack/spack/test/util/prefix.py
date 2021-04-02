# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests various features of :py:class:`spack.util.prefix.Prefix`"""

from spack.util.prefix import Prefix
import os


def test_prefix_attributes():
    """Test normal prefix attributes like ``prefix.bin``"""
    prefix = Prefix(os.sep+'usr')

    assert prefix.bin     == os.sep+'usr'+os.sep+'bin'
    assert prefix.lib     == os.sep+'usr'+os.sep+'lib'
    assert prefix.include == os.sep+'usr'+os.sep+'include'


def test_prefix_join():
    """Test prefix join  ``prefix.join(...)``"""
    prefix = Prefix(os.sep+'usr')

    a1 = prefix.join('a_{0}'.format(1)).lib64
    a2 = prefix.join('a-{0}'.format(1)).lib64
    a3 = prefix.join('a.{0}'.format(1)).lib64

    assert a1 == os.sep+'usr'+os.sep+'a_1'+os.sep+'lib64'
    assert a2 == os.sep+'usr'+os.sep+'a-1'+os.sep+'lib64'
    assert a3 == os.sep+'usr'+os.sep+'a.1'+os.sep+'lib64'

    assert isinstance(a1, Prefix)
    assert isinstance(a2, Prefix)
    assert isinstance(a3, Prefix)

    p1 = prefix.bin.join('executable.sh')
    p2 = prefix.share.join('pkg-config').join('foo.pc')
    p3 = prefix.join('dashed-directory').foo

    assert p1 == os.sep+'usr'+os.sep+'bin'+os.sep+'executable.sh'
    assert p2 == os.sep+'usr'+os.sep+'share'+os.sep+'pkg-config'+os.sep+'foo.pc'
    assert p3 == os.sep+'usr'+os.sep+'dashed-directory'+os.sep+'foo'

    assert isinstance(p1, Prefix)
    assert isinstance(p2, Prefix)
    assert isinstance(p3, Prefix)


def test_multilevel_attributes():
    """Test attributes of attributes, like ``prefix.share.man``"""
    prefix = Prefix(os.sep+'usr'+os.sep)

    assert prefix.share.man   == os.sep+'usr'+os.sep+'share'+os.sep+'man'
    assert prefix.man.man8    == os.sep+'usr'+os.sep+'man'+os.sep+'man8'
    assert prefix.foo.bar.baz == os.sep+'usr'+os.sep+'foo'+os.sep+'bar'+os.sep+'baz'

    share = prefix.share

    assert isinstance(share, Prefix)
    assert share.man == os.sep+'usr'+os.sep+'share'+os.sep+'man'


def test_string_like_behavior():
    """Test string-like behavior of the prefix object"""
    prefix = Prefix('/usr')

    assert prefix == '/usr'
    assert isinstance(prefix, str)

    assert prefix + '/bin' == '/usr/bin'
    assert '--prefix=%s' % prefix == '--prefix=/usr'
    assert '--prefix={0}'.format(prefix) == '--prefix=/usr'

    assert prefix.find('u', 1)
    assert prefix.upper() == '/USR'
    assert prefix.lstrip('/') == 'usr'

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest

import spack.util.naming


@pytest.fixture()
def trie():
    return spack.util.naming.NamespaceTrie()


def test_add_single(trie):
    trie['foo'] = 'bar'

    assert trie.is_prefix('foo')
    assert trie.has_value('foo')
    assert trie['foo'] == 'bar'


def test_add_multiple(trie):
    trie['foo.bar'] = 'baz'

    assert not trie.has_value('foo')
    assert trie.is_prefix('foo')

    assert trie.is_prefix('foo.bar')
    assert trie.has_value('foo.bar')
    assert trie['foo.bar'] == 'baz'

    assert not trie.is_prefix('foo.bar.baz')
    assert not trie.has_value('foo.bar.baz')


def test_add_three(trie):
    # add a three-level namespace
    trie['foo.bar.baz'] = 'quux'

    assert trie.is_prefix('foo')
    assert not trie.has_value('foo')

    assert trie.is_prefix('foo.bar')
    assert not trie.has_value('foo.bar')

    assert trie.is_prefix('foo.bar.baz')
    assert trie.has_value('foo.bar.baz')
    assert trie['foo.bar.baz'] == 'quux'

    assert not trie.is_prefix('foo.bar.baz.quux')
    assert not trie.has_value('foo.bar.baz.quux')

    # Try to add a second element in a prefix namespace
    trie['foo.bar'] = 'blah'

    assert trie.is_prefix('foo')
    assert not trie.has_value('foo')

    assert trie.is_prefix('foo.bar')
    assert trie.has_value('foo.bar')
    assert trie['foo.bar'] == 'blah'

    assert trie.is_prefix('foo.bar.baz')
    assert trie.has_value('foo.bar.baz')
    assert trie['foo.bar.baz'] == 'quux'

    assert not trie.is_prefix('foo.bar.baz.quux')
    assert not trie.has_value('foo.bar.baz.quux')


def test_add_none_single(trie):
    trie['foo'] = None
    assert trie.is_prefix('foo')
    assert trie.has_value('foo')
    assert trie['foo'] is None

    assert not trie.is_prefix('foo.bar')
    assert not trie.has_value('foo.bar')


def test_add_none_multiple(trie):
    trie['foo.bar'] = None

    assert trie.is_prefix('foo')
    assert not trie.has_value('foo')

    assert trie.is_prefix('foo.bar')
    assert trie.has_value('foo.bar')
    assert trie['foo.bar'] is None

    assert not trie.is_prefix('foo.bar.baz')
    assert not trie.has_value('foo.bar.baz')

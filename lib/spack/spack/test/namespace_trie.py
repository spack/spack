##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import unittest

from spack.util.naming import NamespaceTrie


class NamespaceTrieTest(unittest.TestCase):

    def setUp(self):
        self.trie = NamespaceTrie()


    def test_add_single(self):
        self.trie['foo'] = 'bar'

        self.assertTrue(self.trie.is_prefix('foo'))
        self.assertTrue(self.trie.has_value('foo'))
        self.assertEqual(self.trie['foo'], 'bar')


    def test_add_multiple(self):
        self.trie['foo.bar'] = 'baz'

        self.assertFalse(self.trie.has_value('foo'))
        self.assertTrue(self.trie.is_prefix('foo'))

        self.assertTrue(self.trie.is_prefix('foo.bar'))
        self.assertTrue(self.trie.has_value('foo.bar'))
        self.assertEqual(self.trie['foo.bar'], 'baz')

        self.assertFalse(self.trie.is_prefix('foo.bar.baz'))
        self.assertFalse(self.trie.has_value('foo.bar.baz'))


    def test_add_three(self):
        # add a three-level namespace
        self.trie['foo.bar.baz'] = 'quux'

        self.assertTrue(self.trie.is_prefix('foo'))
        self.assertFalse(self.trie.has_value('foo'))

        self.assertTrue(self.trie.is_prefix('foo.bar'))
        self.assertFalse(self.trie.has_value('foo.bar'))

        self.assertTrue(self.trie.is_prefix('foo.bar.baz'))
        self.assertTrue(self.trie.has_value('foo.bar.baz'))
        self.assertEqual(self.trie['foo.bar.baz'], 'quux')

        self.assertFalse(self.trie.is_prefix('foo.bar.baz.quux'))
        self.assertFalse(self.trie.has_value('foo.bar.baz.quux'))

        # Try to add a second element in a prefix namespace
        self.trie['foo.bar'] = 'blah'

        self.assertTrue(self.trie.is_prefix('foo'))
        self.assertFalse(self.trie.has_value('foo'))

        self.assertTrue(self.trie.is_prefix('foo.bar'))
        self.assertTrue(self.trie.has_value('foo.bar'))
        self.assertEqual(self.trie['foo.bar'], 'blah')

        self.assertTrue(self.trie.is_prefix('foo.bar.baz'))
        self.assertTrue(self.trie.has_value('foo.bar.baz'))
        self.assertEqual(self.trie['foo.bar.baz'], 'quux')

        self.assertFalse(self.trie.is_prefix('foo.bar.baz.quux'))
        self.assertFalse(self.trie.has_value('foo.bar.baz.quux'))


    def test_add_none_single(self):
        self.trie['foo'] = None
        self.assertTrue(self.trie.is_prefix('foo'))
        self.assertTrue(self.trie.has_value('foo'))
        self.assertEqual(self.trie['foo'], None)

        self.assertFalse(self.trie.is_prefix('foo.bar'))
        self.assertFalse(self.trie.has_value('foo.bar'))



    def test_add_none_multiple(self):
        self.trie['foo.bar'] = None

        self.assertTrue(self.trie.is_prefix('foo'))
        self.assertFalse(self.trie.has_value('foo'))

        self.assertTrue(self.trie.is_prefix('foo.bar'))
        self.assertTrue(self.trie.has_value('foo.bar'))
        self.assertEqual(self.trie['foo.bar'], None)

        self.assertFalse(self.trie.is_prefix('foo.bar.baz'))
        self.assertFalse(self.trie.has_value('foo.bar.baz'))

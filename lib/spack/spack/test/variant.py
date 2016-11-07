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
import numbers

from spack.variant import *


class VariantSpecTest(unittest.TestCase):

    def test_value_property(self):
        # Multiple values
        a = VariantSpec('foo', 'bar,baz')
        # Spaces are trimmed
        b = VariantSpec('foo', 'bar, baz')
        self.assertEqual(a.value, ('bar', 'baz'))
        self.assertEqual(a, b)
        self.assertTrue('bar' in a and 'baz' in a)
        # Boolean - True
        for x in (True, 'True', 'TRUE', 'TrUe'):
            a.value = x
            self.assertEqual(a.value, True)
            self.assertTrue(True in a)
        # Boolean - False
        for x in (False, 'False', 'FALSE', 'FaLsE'):
            a.value = x
            self.assertEqual(a.value, False)
            self.assertTrue(False in a)

    def test_copy(self):
        a = VariantSpec('foo', 'bar,baz')
        b = a.copy()
        self.assertTrue(a == b and a is not b)

    def test_empty_string(self):
        # Tests that an empty string will be
        # transformed in a tuple containing
        # an empty string
        a = VariantSpec('foo', '')
        self.assertEqual(a._value, ('',))

    def test_repr_and_str(self):
        a = VariantSpec('foo', 'bar,baz')
        b = eval(repr(a))
        self.assertEqual(a, b)
        self.assertEqual(str(a), ' foo=bar,baz')
        b = VariantSpec('foo', True)
        self.assertEqual(str(b), '+foo')
        b.value = False
        self.assertEqual(str(b), '~foo')

    def test_hash(self):
        # Check that hashing does not depend on the order
        # of the values given
        a = VariantSpec('foo', 'bar,baz,bac')
        b = VariantSpec('foo', 'bar,bac,baz')
        c = VariantSpec('foo', 'baz,bac,bar')
        self.assertEqual(hash(a), hash(b))
        self.assertEqual(hash(a), hash(c))


class VariantTest(unittest.TestCase):

    def test_validation(self):
        a = Variant(
            'foo',
            default='',
            description='',
            values=('bar', 'baz', 'foobar'),
            exclusive=True
        )
        # Valid vspec, shouldn't raise
        vspec = VariantSpec('foo', 'bar')
        a.validate_or_raise(vspec)
        # Multiple values are not allowed
        vspec.value = 'bar,baz'
        self.assertRaises(
            MultipleValuesInExclusiveVariantError,
            a.validate_or_raise,
            vspec
        )
        # Inconsistent vspec
        vspec.name = 'FOO'
        self.assertRaises(
            InconsistentValidationError,
            a.validate_or_raise,
            vspec
        )
        # Valid multi-value vspec
        a.exclusive = False
        vspec.name = 'foo'
        a.validate_or_raise(vspec)
        # Add an invalid value
        vspec.value = 'bar,baz,barbaz'
        self.assertRaises(
            InvalidVariantValueError,
            a.validate_or_raise,
            vspec
        )

    def test_callable_validator(self):

        def validator(x):
            return isinstance(int(x), numbers.Integral)

        a = Variant(
            'foo',
            default=1024,
            description='',
            values=validator,
            exclusive=True
        )
        vspec = VariantSpec('foo', a.default)
        a.validate_or_raise(vspec)
        vspec.value = 2056
        a.validate_or_raise(vspec)


class VariantMapTest(unittest.TestCase):

    def test_invalid_values(self):
        # Value with invalid type
        a = VariantMap(None)
        self.assertRaises(TypeError, a.__setitem__, 'foo', 2)
        # Duplicate variant
        a['foo'] = VariantSpec('foo', 'bar,baz')
        self.assertRaises(
            DuplicateVariantError,
            a.__setitem__,
            'foo',
            VariantSpec('foo', 'bar')
        )
        # Non matching names between key and vspec.name
        self.assertRaises(
            KeyError,
            a.__setitem__,
            'bar',
            VariantSpec('foo', 'bar')
        )
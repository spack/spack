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
"""
These version tests were taken from the RPM source code.
We try to maintain compatibility with RPM's version semantics
where it makes sense.
"""
import unittest

from spack.version import *


class VersionsTest(unittest.TestCase):

    def assert_ver_lt(self, a, b):
        a, b = ver(a), ver(b)
        self.assertTrue(a < b)
        self.assertTrue(a <= b)
        self.assertTrue(a != b)
        self.assertFalse(a == b)
        self.assertFalse(a > b)
        self.assertFalse(a >= b)

    def assert_ver_gt(self, a, b):
        a, b = ver(a), ver(b)
        self.assertTrue(a > b)
        self.assertTrue(a >= b)
        self.assertTrue(a != b)
        self.assertFalse(a == b)
        self.assertFalse(a < b)
        self.assertFalse(a <= b)

    def assert_ver_eq(self, a, b):
        a, b = ver(a), ver(b)
        self.assertFalse(a > b)
        self.assertTrue(a >= b)
        self.assertFalse(a != b)
        self.assertTrue(a == b)
        self.assertFalse(a < b)
        self.assertTrue(a <= b)

    def assert_in(self, needle, haystack):
        self.assertTrue(ver(needle) in ver(haystack))

    def assert_not_in(self, needle, haystack):
        self.assertFalse(ver(needle) in ver(haystack))

    def assert_canonical(self, canonical_list, version_list):
        self.assertEqual(ver(canonical_list), ver(version_list))

    def assert_overlaps(self, v1, v2):
        self.assertTrue(ver(v1).overlaps(ver(v2)))

    def assert_no_overlap(self, v1, v2):
        self.assertFalse(ver(v1).overlaps(ver(v2)))

    def assert_satisfies(self, v1, v2):
        self.assertTrue(ver(v1).satisfies(ver(v2)))

    def assert_does_not_satisfy(self, v1, v2):
        self.assertFalse(ver(v1).satisfies(ver(v2)))

    def check_intersection(self, expected, a, b):
        self.assertEqual(ver(expected), ver(a).intersection(ver(b)))

    def check_union(self, expected, a, b):
        self.assertEqual(ver(expected), ver(a).union(ver(b)))

    def test_two_segments(self):
        self.assert_ver_eq('1.0', '1.0')
        self.assert_ver_lt('1.0', '2.0')
        self.assert_ver_gt('2.0', '1.0')
        self.assert_ver_eq('develop', 'develop')
        self.assert_ver_lt('1.0', 'develop')
        self.assert_ver_gt('develop', '1.0')

    def test_three_segments(self):
        self.assert_ver_eq('2.0.1', '2.0.1')
        self.assert_ver_lt('2.0',   '2.0.1')
        self.assert_ver_gt('2.0.1', '2.0')

    def test_alpha(self):
        # TODO: not sure whether I like this.  2.0.1a is *usually*
        # TODO: less than 2.0.1, but special-casing it makes version
        # TODO: comparison complicated.  See version.py
        self.assert_ver_eq('2.0.1a', '2.0.1a')
        self.assert_ver_gt('2.0.1a', '2.0.1')
        self.assert_ver_lt('2.0.1',  '2.0.1a')

    def test_patch(self):
        self.assert_ver_eq('5.5p1',  '5.5p1')
        self.assert_ver_lt('5.5p1',  '5.5p2')
        self.assert_ver_gt('5.5p2',  '5.5p1')
        self.assert_ver_eq('5.5p10', '5.5p10')
        self.assert_ver_lt('5.5p1',  '5.5p10')
        self.assert_ver_gt('5.5p10', '5.5p1')

    def test_num_alpha_with_no_separator(self):
        self.assert_ver_lt('10xyz',   '10.1xyz')
        self.assert_ver_gt('10.1xyz', '10xyz')
        self.assert_ver_eq('xyz10',   'xyz10')
        self.assert_ver_lt('xyz10',   'xyz10.1')
        self.assert_ver_gt('xyz10.1', 'xyz10')

    def test_alpha_with_dots(self):
        self.assert_ver_eq('xyz.4', 'xyz.4')
        self.assert_ver_lt('xyz.4', '8')
        self.assert_ver_gt('8',     'xyz.4')
        self.assert_ver_lt('xyz.4', '2')
        self.assert_ver_gt('2',     'xyz.4')

    def test_nums_and_patch(self):
        self.assert_ver_lt('5.5p2', '5.6p1')
        self.assert_ver_gt('5.6p1', '5.5p2')
        self.assert_ver_lt('5.6p1', '6.5p1')
        self.assert_ver_gt('6.5p1', '5.6p1')

    def test_rc_versions(self):
        self.assert_ver_gt('6.0.rc1', '6.0')
        self.assert_ver_lt('6.0',     '6.0.rc1')

    def test_alpha_beta(self):
        self.assert_ver_gt('10b2', '10a1')
        self.assert_ver_lt('10a2', '10b2')

    def test_double_alpha(self):
        self.assert_ver_eq('1.0aa', '1.0aa')
        self.assert_ver_lt('1.0a',  '1.0aa')
        self.assert_ver_gt('1.0aa', '1.0a')

    def test_padded_numbers(self):
        self.assert_ver_eq('10.0001', '10.0001')
        self.assert_ver_eq('10.0001', '10.1')
        self.assert_ver_eq('10.1',    '10.0001')
        self.assert_ver_lt('10.0001', '10.0039')
        self.assert_ver_gt('10.0039', '10.0001')

    def test_close_numbers(self):
        self.assert_ver_lt('4.999.9', '5.0')
        self.assert_ver_gt('5.0',     '4.999.9')

    def test_date_stamps(self):
        self.assert_ver_eq('20101121', '20101121')
        self.assert_ver_lt('20101121', '20101122')
        self.assert_ver_gt('20101122', '20101121')

    def test_underscores(self):
        self.assert_ver_eq('2_0', '2_0')
        self.assert_ver_eq('2.0', '2_0')
        self.assert_ver_eq('2_0', '2.0')

    def test_rpm_oddities(self):
        self.assert_ver_eq('1b.fc17', '1b.fc17')
        self.assert_ver_lt('1b.fc17', '1.fc17')
        self.assert_ver_gt('1.fc17',  '1b.fc17')
        self.assert_ver_eq('1g.fc17', '1g.fc17')
        self.assert_ver_gt('1g.fc17', '1.fc17')
        self.assert_ver_lt('1.fc17',  '1g.fc17')

    # Stuff below here is not taken from RPM's tests and is
    # unique to spack
    def test_version_ranges(self):
        self.assert_ver_lt('1.2:1.4', '1.6')
        self.assert_ver_gt('1.6', '1.2:1.4')
        self.assert_ver_eq('1.2:1.4', '1.2:1.4')
        self.assertNotEqual(ver('1.2:1.4'), ver('1.2:1.6'))

        self.assert_ver_lt('1.2:1.4', '1.5:1.6')
        self.assert_ver_gt('1.5:1.6', '1.2:1.4')

    def test_contains(self):
        self.assert_in('1.3', '1.2:1.4')
        self.assert_in('1.2.5', '1.2:1.4')
        self.assert_in('1.3.5', '1.2:1.4')
        self.assert_in('1.3.5-7', '1.2:1.4')
        self.assert_not_in('1.1', '1.2:1.4')
        self.assert_not_in('1.5', '1.2:1.4')

        self.assert_in('1.4.2', '1.2:1.4')
        self.assert_not_in('1.4.2', '1.2:1.4.0')

        self.assert_in('1.2.8', '1.2.7:1.4')
        self.assert_in('1.2.7:1.4', ':')
        self.assert_not_in('1.2.5', '1.2.7:1.4')

        self.assert_in('1.4.1', '1.2.7:1.4')
        self.assert_not_in('1.4.1', '1.2.7:1.4.0')

    def test_in_list(self):
        self.assert_in('1.2', ['1.5', '1.2', '1.3'])
        self.assert_in('1.2.5', ['1.5', '1.2:1.3'])
        self.assert_in('1.5', ['1.5', '1.2:1.3'])
        self.assert_not_in('1.4', ['1.5', '1.2:1.3'])

        self.assert_in('1.2.5:1.2.7', [':'])
        self.assert_in('1.2.5:1.2.7', ['1.5', '1.2:1.3'])
        self.assert_not_in('1.2.5:1.5', ['1.5', '1.2:1.3'])
        self.assert_not_in('1.1:1.2.5', ['1.5', '1.2:1.3'])

    def test_ranges_overlap(self):
        self.assert_overlaps('1.2', '1.2')
        self.assert_overlaps('1.2.1', '1.2.1')
        self.assert_overlaps('1.2.1b', '1.2.1b')

        self.assert_overlaps('1.2:1.7', '1.6:1.9')
        self.assert_overlaps(':1.7', '1.6:1.9')
        self.assert_overlaps(':1.7', ':1.9')
        self.assert_overlaps(':1.7', '1.6:')
        self.assert_overlaps('1.2:', '1.6:1.9')
        self.assert_overlaps('1.2:', ':1.9')
        self.assert_overlaps('1.2:', '1.6:')
        self.assert_overlaps(':', ':')
        self.assert_overlaps(':', '1.6:1.9')
        self.assert_overlaps('1.6:1.9', ':')

    def test_overlap_with_containment(self):
        self.assert_in('1.6.5', '1.6')
        self.assert_in('1.6.5', ':1.6')

        self.assert_overlaps('1.6.5', ':1.6')
        self.assert_overlaps(':1.6', '1.6.5')

        self.assert_not_in(':1.6', '1.6.5')
        self.assert_in('1.6.5', ':1.6')

    def test_lists_overlap(self):
        self.assert_overlaps('1.2b:1.7,5', '1.6:1.9,1')
        self.assert_overlaps('1,2,3,4,5', '3,4,5,6,7')
        self.assert_overlaps('1,2,3,4,5', '5,6,7')
        self.assert_overlaps('1,2,3,4,5', '5:7')
        self.assert_overlaps('1,2,3,4,5', '3, 6:7')
        self.assert_overlaps('1, 2, 4, 6.5', '3, 6:7')
        self.assert_overlaps('1, 2, 4, 6.5', ':, 5, 8')
        self.assert_overlaps('1, 2, 4, 6.5', ':')
        self.assert_no_overlap('1, 2, 4', '3, 6:7')
        self.assert_no_overlap('1,2,3,4,5', '6,7')
        self.assert_no_overlap('1,2,3,4,5', '6:7')

    def test_canonicalize_list(self):
        self.assert_canonical(['1.2', '1.3', '1.4'],
                              ['1.2', '1.3', '1.3', '1.4'])

        self.assert_canonical(['1.2', '1.3:1.4'],
                              ['1.2', '1.3', '1.3:1.4'])

        self.assert_canonical(['1.2', '1.3:1.4'],
                              ['1.2', '1.3:1.4', '1.4'])

        self.assert_canonical(['1.3:1.4'],
                              ['1.3:1.4', '1.3', '1.3.1', '1.3.9', '1.4'])

        self.assert_canonical(['1.3:1.4'],
                              ['1.3', '1.3.1', '1.3.9', '1.4', '1.3:1.4'])

        self.assert_canonical(['1.3:1.5'],
                              ['1.3', '1.3.1', '1.3.9', '1.4:1.5', '1.3:1.4'])

        self.assert_canonical(['1.3:1.5'],
                              ['1.3, 1.3.1,1.3.9,1.4:1.5,1.3:1.4'])

        self.assert_canonical(['1.3:1.5'],
                              ['1.3, 1.3.1,1.3.9,1.4 : 1.5 , 1.3 : 1.4'])

        self.assert_canonical([':'],
                              [':,1.3, 1.3.1,1.3.9,1.4 : 1.5 , 1.3 : 1.4'])

    def test_intersection(self):
        self.check_intersection('2.5',
                                '1.0:2.5', '2.5:3.0')
        self.check_intersection('2.5:2.7',
                                '1.0:2.7', '2.5:3.0')
        self.check_intersection('0:1', ':', '0:1')

        self.check_intersection(['1.0', '2.5:2.7'],
                                ['1.0:2.7'], ['2.5:3.0', '1.0'])
        self.check_intersection(['2.5:2.7'],
                                ['1.1:2.7'], ['2.5:3.0', '1.0'])
        self.check_intersection(['0:1'], [':'], ['0:1'])

    def test_intersect_with_containment(self):
        self.check_intersection('1.6.5', '1.6.5', ':1.6')
        self.check_intersection('1.6.5', ':1.6', '1.6.5')

        self.check_intersection('1.6:1.6.5', ':1.6.5', '1.6')
        self.check_intersection('1.6:1.6.5', '1.6', ':1.6.5')

    def test_union_with_containment(self):
        self.check_union(':1.6', '1.6.5', ':1.6')
        self.check_union(':1.6', ':1.6', '1.6.5')

        self.check_union(':1.6', ':1.6.5', '1.6')
        self.check_union(':1.6', '1.6', ':1.6.5')

        self.check_union(':', '1.0:', ':2.0')

        self.check_union('1:4', '1:3', '2:4')
        self.check_union('1:4', '2:4', '1:3')

        # Tests successor/predecessor case.
        self.check_union('1:4', '1:2', '3:4')

    def test_basic_version_satisfaction(self):
        self.assert_satisfies('4.7.3',   '4.7.3')

        self.assert_satisfies('4.7.3',   '4.7')
        self.assert_satisfies('4.7.3b2', '4.7')
        self.assert_satisfies('4.7b6',   '4.7')

        self.assert_satisfies('4.7.3',   '4')
        self.assert_satisfies('4.7.3b2', '4')
        self.assert_satisfies('4.7b6',   '4')

        self.assert_does_not_satisfy('4.8.0', '4.9')
        self.assert_does_not_satisfy('4.8',   '4.9')
        self.assert_does_not_satisfy('4',     '4.9')

    def test_basic_version_satisfaction_in_lists(self):
        self.assert_satisfies(['4.7.3'],   ['4.7.3'])

        self.assert_satisfies(['4.7.3'],   ['4.7'])
        self.assert_satisfies(['4.7.3b2'], ['4.7'])
        self.assert_satisfies(['4.7b6'],   ['4.7'])

        self.assert_satisfies(['4.7.3'],   ['4'])
        self.assert_satisfies(['4.7.3b2'], ['4'])
        self.assert_satisfies(['4.7b6'],   ['4'])

        self.assert_does_not_satisfy(['4.8.0'], ['4.9'])
        self.assert_does_not_satisfy(['4.8'],   ['4.9'])
        self.assert_does_not_satisfy(['4'],     ['4.9'])

    def test_version_range_satisfaction(self):
        self.assert_satisfies('4.7b6', '4.3:4.7')
        self.assert_satisfies('4.3.0', '4.3:4.7')
        self.assert_satisfies('4.3.2', '4.3:4.7')

        self.assert_does_not_satisfy('4.8.0', '4.3:4.7')
        self.assert_does_not_satisfy('4.3',   '4.4:4.7')

        self.assert_satisfies('4.7b6',        '4.3:4.7')
        self.assert_does_not_satisfy('4.8.0', '4.3:4.7')

    def test_version_range_satisfaction_in_lists(self):
        self.assert_satisfies(['4.7b6'], ['4.3:4.7'])
        self.assert_satisfies(['4.3.0'], ['4.3:4.7'])
        self.assert_satisfies(['4.3.2'], ['4.3:4.7'])

        self.assert_does_not_satisfy(['4.8.0'], ['4.3:4.7'])
        self.assert_does_not_satisfy(['4.3'],   ['4.4:4.7'])

        self.assert_satisfies(['4.7b6'],        ['4.3:4.7'])
        self.assert_does_not_satisfy(['4.8.0'], ['4.3:4.7'])

    def test_satisfaction_with_lists(self):
        self.assert_satisfies('4.7',     '4.3, 4.6, 4.7')
        self.assert_satisfies('4.7.3',   '4.3, 4.6, 4.7')
        self.assert_satisfies('4.6.5',   '4.3, 4.6, 4.7')
        self.assert_satisfies('4.6.5.2', '4.3, 4.6, 4.7')

        self.assert_does_not_satisfy('4',     '4.3, 4.6, 4.7')
        self.assert_does_not_satisfy('4.8.0', '4.2, 4.3:4.7')

        self.assert_satisfies('4.8.0', '4.2, 4.3:4.8')
        self.assert_satisfies('4.8.2', '4.2, 4.3:4.8')

    def test_formatted_strings(self):
        versions = '1.2.3', '1_2_3', '1-2-3'
        for item in versions:
            v = Version(item)
            self.assertEqual(v.dotted, '1.2.3')
            self.assertEqual(v.dashed, '1-2-3')
            self.assertEqual(v.underscored, '1_2_3')

    def test_repr_and_str(self):

        def check_repr_and_str(vrs):
            a = Version(vrs)
            self.assertEqual(repr(a), 'Version(\'' + vrs + '\')')
            b = eval(repr(a))
            self.assertEqual(a, b)
            self.assertEqual(str(a), vrs)
            self.assertEqual(str(a), str(b))

        check_repr_and_str('1.2.3')
        check_repr_and_str('R2016a')
        check_repr_and_str('R2016a.2-3_4')

    def test_get_item(self):
        a = Version('0.1_2-3')
        self.assertTrue(isinstance(a[1], int))
        # Test slicing
        b = a[0:2]
        self.assertTrue(isinstance(b, Version))
        self.assertEqual(b, Version('0.1'))
        self.assertEqual(repr(b), 'Version(\'0.1\')')
        self.assertEqual(str(b), '0.1')
        b = a[0:3]
        self.assertTrue(isinstance(b, Version))
        self.assertEqual(b, Version('0.1_2'))
        self.assertEqual(repr(b), 'Version(\'0.1_2\')')
        self.assertEqual(str(b), '0.1_2')
        b = a[1:]
        self.assertTrue(isinstance(b, Version))
        self.assertEqual(b, Version('1_2-3'))
        self.assertEqual(repr(b), 'Version(\'1_2-3\')')
        self.assertEqual(str(b), '1_2-3')
        # Raise TypeError on tuples
        self.assertRaises(TypeError, b.__getitem__, 1, 2)

if __name__ == '__main__':
    unittest.main()

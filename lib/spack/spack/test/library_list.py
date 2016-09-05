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

from llnl.util.filesystem import LibraryList


class LibraryListTest(unittest.TestCase):
    def setUp(self):
        l = [
            '/dir1/liblapack.a',
            '/dir2/libfoo.dylib',
            '/dir1/libblas.a',
            '/dir3/libbar.so',
            'libbaz.so'
        ]
        self.liblist = LibraryList(l)

    def test_repr(self):
        x = eval(repr(self.liblist))
        self.assertEqual(self.liblist, x)

    def test_joined_and_str(self):
        s1 = self.liblist.joined()
        self.assertEqual(
            s1,
            '/dir1/liblapack.a /dir2/libfoo.dylib /dir1/libblas.a /dir3/libbar.so libbaz.so'  # NOQA: ignore=E501
        )
        s2 = str(self.liblist)
        self.assertEqual(s1, s2)
        s3 = self.liblist.joined(';')
        self.assertEqual(
            s3,
            '/dir1/liblapack.a;/dir2/libfoo.dylib;/dir1/libblas.a;/dir3/libbar.so;libbaz.so'  # NOQA: ignore=E501
        )

    def test_flags(self):
        search_flags = self.liblist.search_flags
        self.assertTrue('-L/dir1' in search_flags)
        self.assertTrue('-L/dir2' in search_flags)
        self.assertTrue('-L/dir3' in search_flags)
        self.assertTrue(isinstance(search_flags, str))

        link_flags = self.liblist.link_flags
        self.assertEqual(
            link_flags,
            '-llapack -lfoo -lblas -lbar -lbaz'
        )

        ld_flags = self.liblist.ld_flags
        self.assertEqual(ld_flags, search_flags + ' ' + link_flags)

    def test_paths_manipulation(self):
        names = self.liblist.names
        self.assertEqual(names, ['lapack', 'foo', 'blas', 'bar', 'baz'])

        directories = self.liblist.directories
        self.assertEqual(directories, ['/dir1', '/dir2', '/dir3'])

    def test_get_item(self):
        a = self.liblist[0]
        self.assertEqual(a, '/dir1/liblapack.a')

        b = self.liblist[:]
        self.assertEqual(type(b), type(self.liblist))
        self.assertEqual(self.liblist, b)
        self.assertTrue(self.liblist is not b)

    def test_add(self):
        pylist = [
            '/dir1/liblapack.a',  # removed from the final list
            '/dir2/libbaz.so',
            '/dir4/libnew.a'
        ]
        another = LibraryList(pylist)
        l = self.liblist + another
        self.assertEqual(len(l), 7)
        # Invariant : l == l + l
        self.assertEqual(l, l + l)
        # Always produce an instance of LibraryList
        self.assertEqual(
            type(self.liblist),
            type(self.liblist + pylist)
        )
        self.assertEqual(
            type(pylist + self.liblist),
            type(self.liblist)
        )

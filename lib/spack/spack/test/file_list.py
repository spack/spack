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

from llnl.util.filesystem import LibraryList, HeaderList


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
        self.assertEqual(
            search_flags,
            '-L/dir1 -L/dir2 -L/dir3'
        )

        link_flags = self.liblist.link_flags
        self.assertTrue('-llapack' in link_flags)
        self.assertTrue('-lfoo'    in link_flags)
        self.assertTrue('-lblas'   in link_flags)
        self.assertTrue('-lbar'    in link_flags)
        self.assertTrue('-lbaz'    in link_flags)
        self.assertTrue(isinstance(link_flags, str))
        self.assertEqual(
            link_flags,
            '-llapack -lfoo -lblas -lbar -lbaz'
        )

        ld_flags = self.liblist.ld_flags
        self.assertTrue(isinstance(ld_flags, str))
        self.assertEqual(
            ld_flags,
            search_flags + ' ' + link_flags
        )

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


class HeaderListTest(unittest.TestCase):
    def setUp(self):
        h = [
            '/dir1/Python.h',
            '/dir2/datetime.h',
            '/dir1/pyconfig.h',
            '/dir3/core.h',
            'pymem.h'
        ]
        headlist = HeaderList(h)
        headlist.add_macro('-DBOOST_LIB_NAME=boost_regex')
        headlist.add_macro('-DBOOST_DYN_LINK')
        self.headlist = headlist

    def test_repr(self):
        x = eval(repr(self.headlist))
        self.assertEqual(self.headlist, x)

    def test_joined_and_str(self):
        s1 = self.headlist.joined()
        self.assertEqual(
            s1,
            '/dir1/Python.h /dir2/datetime.h /dir1/pyconfig.h /dir3/core.h pymem.h'  # NOQA: ignore=E501
        )
        s2 = str(self.headlist)
        self.assertEqual(s1, s2)
        s3 = self.headlist.joined(';')
        self.assertEqual(
            s3,
            '/dir1/Python.h;/dir2/datetime.h;/dir1/pyconfig.h;/dir3/core.h;pymem.h'  # NOQA: ignore=E501
        )

    def test_flags(self):
        include_flags = self.headlist.include_flags
        self.assertTrue('-I/dir1' in include_flags)
        self.assertTrue('-I/dir2' in include_flags)
        self.assertTrue('-I/dir3' in include_flags)
        self.assertTrue(isinstance(include_flags, str))
        self.assertEqual(
            include_flags,
            '-I/dir1 -I/dir2 -I/dir3'
        )

        macros = self.headlist.macro_definitions
        self.assertTrue('-DBOOST_LIB_NAME=boost_regex' in macros)
        self.assertTrue('-DBOOST_DYN_LINK' in macros)
        self.assertTrue(isinstance(macros, str))
        self.assertEqual(
            macros,
            '-DBOOST_LIB_NAME=boost_regex -DBOOST_DYN_LINK'
        )

        cpp_flags = self.headlist.cpp_flags
        self.assertTrue(isinstance(cpp_flags, str))
        self.assertEqual(
            cpp_flags,
            include_flags + ' ' + macros
        )

    def test_paths_manipulation(self):
        names = self.headlist.names
        self.assertEqual(
            names,
            ['Python', 'datetime', 'pyconfig', 'core', 'pymem']
        )

        directories = self.headlist.directories
        self.assertEqual(directories, ['/dir1', '/dir2', '/dir3'])

    def test_get_item(self):
        a = self.headlist[0]
        self.assertEqual(a, '/dir1/Python.h')

        b = self.headlist[:]
        self.assertEqual(type(b), type(self.headlist))
        self.assertEqual(self.headlist, b)
        self.assertTrue(self.headlist is not b)

    def test_add(self):
        pylist = [
            '/dir1/Python.h',  # removed from the final list
            '/dir2/pyconfig.h',
            '/dir4/datetime.h'
        ]
        another = HeaderList(pylist)
        h = self.headlist + another
        self.assertEqual(len(h), 7)
        # Invariant : l == l + l
        self.assertEqual(h, h + h)
        # Always produce an instance of HeaderList
        self.assertEqual(
            type(self.headlist),
            type(self.headlist + pylist)
        )
        self.assertEqual(
            type(pylist + self.headlist),
            type(self.headlist)
        )

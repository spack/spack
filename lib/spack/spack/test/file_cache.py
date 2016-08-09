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
Test Spack's FileCache.
"""
import os
import shutil
import tempfile
import unittest

from spack.file_cache import FileCache


class FileCacheTest(unittest.TestCase):
    """Ensure that a file cache can properly write to a file and recover its
       contents."""

    def setUp(self):
        self.scratch_dir = tempfile.mkdtemp()
        self.cache = FileCache(self.scratch_dir)

    def tearDown(self):
        shutil.rmtree(self.scratch_dir)

    def test_write_and_read_cache_file(self):
        """Test writing then reading a cached file."""
        with self.cache.write_transaction('test.yaml') as (old, new):
            self.assertTrue(old is None)
            self.assertTrue(new is not None)
            new.write("foobar\n")

        with self.cache.read_transaction('test.yaml') as stream:
            text = stream.read()
            self.assertEqual("foobar\n", text)

    def test_remove(self):
        """Test removing an entry from the cache."""
        self.test_write_and_write_cache_file()

        self.cache.remove('test.yaml')

        self.assertFalse(os.path.exists(self.cache.cache_path('test.yaml')))
        self.assertFalse(os.path.exists(self.cache._lock_path('test.yaml')))

    def test_write_and_write_cache_file(self):
        """Test two write transactions on a cached file."""
        with self.cache.write_transaction('test.yaml') as (old, new):
            self.assertTrue(old is None)
            self.assertTrue(new is not None)
            new.write("foobar\n")

        with self.cache.write_transaction('test.yaml') as (old, new):
            self.assertTrue(old is not None)
            text = old.read()
            self.assertEqual("foobar\n", text)
            self.assertTrue(new is not None)
            new.write("barbaz\n")

        with self.cache.read_transaction('test.yaml') as stream:
            text = stream.read()
            self.assertEqual("barbaz\n", text)

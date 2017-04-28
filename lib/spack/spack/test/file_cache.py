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
"""Test Spack's FileCache."""
import os

import pytest
from spack.file_cache import FileCache


@pytest.fixture()
def file_cache(tmpdir):
    """Returns a properly initialized FileCache instance"""
    return FileCache(str(tmpdir))


def test_write_and_read_cache_file(file_cache):
    """Test writing then reading a cached file."""
    with file_cache.write_transaction('test.yaml') as (old, new):
        assert old is None
        assert new is not None
        new.write("foobar\n")

    with file_cache.read_transaction('test.yaml') as stream:
        text = stream.read()
        assert text == "foobar\n"


def test_write_and_remove_cache_file(file_cache):
    """Test two write transactions on a cached file. Then try to remove an
    entry from it.
    """

    with file_cache.write_transaction('test.yaml') as (old, new):
        assert old is None
        assert new is not None
        new.write("foobar\n")

    with file_cache.write_transaction('test.yaml') as (old, new):
        assert old is not None
        text = old.read()
        assert text == "foobar\n"
        assert new is not None
        new.write("barbaz\n")

    with file_cache.read_transaction('test.yaml') as stream:
        text = stream.read()
        assert text == "barbaz\n"

    file_cache.remove('test.yaml')

    # After removal both the file and the lock file should not exist
    assert not os.path.exists(file_cache.cache_path('test.yaml'))
    assert not os.path.exists(file_cache._lock_path('test.yaml'))

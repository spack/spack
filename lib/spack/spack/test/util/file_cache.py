# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's FileCache."""
import os

import pytest

from spack.util.file_cache import FileCache


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

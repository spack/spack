# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's FileCache."""
import os
import pathlib

import pytest

import spack.llnl.util.filesystem as fs
from spack.util.file_cache import CacheError, FileCache


@pytest.fixture()
def file_cache(tmp_path: pathlib.Path):
    """Returns a properly initialized FileCache instance"""
    return FileCache(str(tmp_path))


def test_write_and_read_cache_file(file_cache):
    """Test writing then reading a cached file."""
    with file_cache.write_transaction("test.yaml") as (old, new):
        assert old is None
        assert new is not None
        new.write("foobar\n")

    with file_cache.read_transaction("test.yaml") as stream:
        text = stream.read()
        assert text == "foobar\n"


def test_read_before_init(file_cache):
    with file_cache.read_transaction("test.yaml") as stream:
        assert stream is None


@pytest.mark.not_on_windows("Locks not supported on Windows")
def test_failed_write_and_read_cache_file(file_cache):
    """Test failing to write then attempting to read a cached file."""
    with pytest.raises(RuntimeError, match=r"^foobar$"):
        with file_cache.write_transaction("test.yaml") as (old, new):
            assert old is None
            assert new is not None
            raise RuntimeError("foobar")

    # Cache dir should have exactly one (lock) file
    assert os.listdir(file_cache.root) == [".lock"]

    # File does not exist
    assert not os.path.exists(file_cache.cache_path("test.yaml"))


def test_write_and_remove_cache_file(file_cache):
    """Test two write transactions on a cached file. Then try to remove an
    entry from it.
    """

    with file_cache.write_transaction("test.yaml") as (old, new):
        assert old is None
        assert new is not None
        new.write("foobar\n")

    with file_cache.write_transaction("test.yaml") as (old, new):
        assert old is not None
        text = old.read()
        assert text == "foobar\n"
        assert new is not None
        new.write("barbaz\n")

    with file_cache.read_transaction("test.yaml") as stream:
        text = stream.read()
        assert text == "barbaz\n"

    file_cache.remove("test.yaml")

    # After removal the file should not exist
    assert not os.path.exists(file_cache.cache_path("test.yaml"))

    # Whether the lock file exists is more of an implementation detail, on Linux they
    # continue to exist, on Windows they don't.
    # assert os.path.exists(file_cache._lock_path('test.yaml'))


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.skipif(fs.getuid() == 0, reason="user is root")
def test_bad_cache_permissions(file_cache, request):
    """Test that transactions raise CacheError on permission problems."""
    relpath = fs.join_path("test-dir", "read-only-file.txt")
    cachefile = file_cache.cache_path(relpath)
    fs.touchp(cachefile)

    # A directory where a file is expected raises CacheError on read
    with pytest.raises(CacheError, match="not a file"):
        with file_cache.read_transaction(os.path.dirname(relpath)) as _:
            pass

    # A directory where a file is expected raises CacheError on write
    with pytest.raises(CacheError, match="not a file"):
        with file_cache.write_transaction(os.path.dirname(relpath)) as _:
            pass

    # A non-readable file raises CacheError on read
    os.chmod(cachefile, 0o200)
    request.addfinalizer(lambda c=cachefile: os.chmod(c, 0o600))
    with pytest.raises(CacheError, match="Cannot access cache file"):
        with file_cache.read_transaction(relpath) as _:
            pass

    # A read-only parent directory raises CacheError on write
    relpath2 = fs.join_path("test-dir", "another-file.txxt")
    parent = str(file_cache.cache_path(relpath2).parent)
    os.chmod(parent, 0o400)
    request.addfinalizer(lambda p=parent: os.chmod(p, 0o700))
    with pytest.raises(CacheError):
        with file_cache.write_transaction(relpath2) as _:
            pass


@pytest.mark.regression("31475")
def test_delete_is_idempotent(file_cache):
    """Deleting a non-existent key should be idempotent, to simplify life when
    running delete with multiple processes"""
    file_cache.remove("test.yaml")

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import math
import os
import pathlib
import shutil
from typing import Dict, Union

from spack.error import SpackError
from spack.util.lock import Lock, ReadTransaction, WriteTransaction


class Cache:
    """This class manages cached data in the filesystem.

    - Cache files are fetched and stored by unique keys.  Keys can be relative
      paths, so that there can be some hierarchy in the cache.

    """

    def __init__(self, root: Union[str, pathlib.Path], timeout=120):
        """Create a cache object.

        This will create the cache directory if it does not exist yet.

        Args:
            root: specifies the root directory where the cache stores files

            timeout: when there is contention among multiple Spack processes
                for cache files, this specifies how long Spack should wait
                before assuming that there is a deadlock.
        """
        if isinstance(root, str):
            root = pathlib.Path(root)
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

        self._locks: Dict[Union[pathlib.Path, str], Lock] = {}
        self.lock_timeout = timeout

    def destroy(self):
        """Remove all files under the cache root."""
        for f in self.root.iterdir():
            if f.is_dir():
                shutil.rmtree(f, True)
            else:
                f.unlink()

    def cache_path(self, key: Union[str, pathlib.Path]):
        """Path to the file in the cache for a particular key."""
        return self.root / key

    def _lock_path(self, key: Union[str, pathlib.Path]):
        """Path to the file in the cache for a particular key."""
        keyfile = os.path.basename(key)
        keydir = os.path.dirname(key)

        return self.root / keydir / ("." + keyfile + ".lock")

    def _get_lock(self, key: Union[str, pathlib.Path]):
        """Create a lock for a key, if necessary, and return a lock object."""
        if key not in self._locks:
            self._locks[key] = Lock(str(self._lock_path(key)), default_timeout=self.lock_timeout)
        return self._locks[key]

    def _entry_validation(self, cache_path: pathlib.Path) -> bool:
        """Validates a given potential cache key"""
        raise NotImplementedError("Must be implemented by subclass")

    def _rm_cache_entry(self, cache_path: pathlib.Path):
        """Removes a cache entry"""
        raise NotImplementedError("Must be implemented by subclass")

    def _acquire_read_fn(self, path: pathlib.Path):
        """Returns a function pointer to be used as a callback when acquiring
        a read lock during a read transaction"""
        raise NotImplementedError("Must be implemented by subclass")

    def _acquire_write_fn(self, path: pathlib.Path):
        """Returns a functin pointer to be used as a callback when acquring a read lock
        during a write transaction"""
        raise NotImplementedError("Must be implemented by subclass")

    def init_entry(self, key: Union[str, pathlib.Path]):
        """Ensure we can access a cache file. Create a lock for it if needed.

        Return whether the cache file exists yet or not.
        """
        cache_path = self.cache_path(key)
        validation_result = self._entry_validation(cache_path)
        # ensure lock is created for this key
        self._get_lock(key)
        return validation_result

    def read_transaction(self, key: Union[str, pathlib.Path]):
        """Get a read transaction on a file cache item.

        Returns a ReadTransaction context manager and opens the cache file for
        reading.  You can use it like this:

           with file_cache_object.read_transaction(key) as cache_file:
               cache_file.read()

        """
        path = self.cache_path(key)
        return ReadTransaction(
            self._get_lock(key), acquire=self._acquire_read_fn(path)  # type: ignore
        )

    def write_transaction(self, key: Union[str, pathlib.Path]):
        """Get a write transaction on a file cache item.

        Returns a WriteTransaction context manager that opens a temporary file
        for writing.  Once the context manager finishes, if nothing went wrong,
        moves the file into place on top of the old file atomically.

        """
        path = self.cache_path(key)
        if os.path.exists(path) and not os.access(path, os.W_OK):
            raise CacheError(f"Insufficient permissions to write to file cache at {path}")

        return WriteTransaction(
            self._get_lock(key), acquire=self._acquire_write_fn(path)  # type: ignore
        )

    def mtime(self, key: Union[str, pathlib.Path]) -> float:
        """Return modification time of cache key, or -inf if it does not exist.

        Time is in units returned by os.stat in the mtime field, which is
        platform-dependent.

        """
        if not self.init_entry(key):
            return -math.inf
        else:
            return self.cache_path(key).stat().st_mtime

    def remove(self, key: Union[str, pathlib.Path]):
        entry = self.cache_path(key)
        lock = self._get_lock(key)
        try:
            lock.acquire_write()
            self._rm_cache_entry(entry)
        except OSError as e:
            # File not found is OK, so remove is idempotent.
            if e.errno != errno.ENOENT:
                raise
        finally:
            lock.release_write()


class CacheError(SpackError):
    pass

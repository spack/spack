# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import math
import os
import shutil

from llnl.util.filesystem import mkdirp, rename

from spack.error import SpackError
from spack.util.lock import Lock, ReadTransaction, WriteTransaction


class FileCache:
    """This class manages cached data in the filesystem.

    - Cache files are fetched and stored by unique keys.  Keys can be relative
      paths, so that there can be some hierarchy in the cache.

    - The FileCache handles locking cache files for reading and writing, so
      client code need not manage locks for cache entries.

    """

    def __init__(self, root, timeout=120):
        """Create a file cache object.

        This will create the cache directory if it does not exist yet.

        Args:
            root: specifies the root directory where the cache stores files

            timeout: when there is contention among multiple Spack processes
                for cache files, this specifies how long Spack should wait
                before assuming that there is a deadlock.
        """
        self.root = root.rstrip(os.path.sep)
        if not os.path.exists(self.root):
            mkdirp(self.root)

        self._locks = {}
        self.lock_timeout = timeout

    def destroy(self):
        """Remove all files under the cache root."""
        for f in os.listdir(self.root):
            path = os.path.join(self.root, f)
            if os.path.isdir(path):
                shutil.rmtree(path, True)
            else:
                os.remove(path)

    def cache_path(self, key):
        """Path to the file in the cache for a particular key."""
        return os.path.join(self.root, key)

    def _lock_path(self, key):
        """Path to the file in the cache for a particular key."""
        keyfile = os.path.basename(key)
        keydir = os.path.dirname(key)

        return os.path.join(self.root, keydir, "." + keyfile + ".lock")

    def _get_lock(self, key):
        """Create a lock for a key, if necessary, and return a lock object."""
        if key not in self._locks:
            self._locks[key] = Lock(self._lock_path(key), default_timeout=self.lock_timeout)
        return self._locks[key]

    def init_entry(self, key):
        """Ensure we can access a cache file. Create a lock for it if needed.

        Return whether the cache file exists yet or not.
        """
        cache_path = self.cache_path(key)

        exists = os.path.exists(cache_path)
        if exists:
            if not os.path.isfile(cache_path):
                raise CacheError("Cache file is not a file: %s" % cache_path)

            if not os.access(cache_path, os.R_OK):
                raise CacheError("Cannot access cache file: %s" % cache_path)
        else:
            # if the file is hierarchical, make parent directories
            parent = os.path.dirname(cache_path)
            if parent.rstrip(os.path.sep) != self.root:
                mkdirp(parent)

            if not os.access(parent, os.R_OK | os.W_OK):
                raise CacheError("Cannot access cache directory: %s" % parent)

            # ensure lock is created for this key
            self._get_lock(key)
        return exists

    def read_transaction(self, key):
        """Get a read transaction on a file cache item.

        Returns a ReadTransaction context manager and opens the cache file for
        reading.  You can use it like this:

           with file_cache_object.read_transaction(key) as cache_file:
               cache_file.read()

        """
        return ReadTransaction(self._get_lock(key), acquire=lambda: open(self.cache_path(key)))

    def write_transaction(self, key):
        """Get a write transaction on a file cache item.

        Returns a WriteTransaction context manager that opens a temporary file
        for writing.  Once the context manager finishes, if nothing went wrong,
        moves the file into place on top of the old file atomically.

        """
        filename = self.cache_path(key)
        if os.path.exists(filename) and not os.access(filename, os.W_OK):
            raise CacheError(
                "Insufficient permissions to write to file cache at {0}".format(filename)
            )

        # TODO: this nested context manager adds a lot of complexity and
        # TODO: is pretty hard to reason about in llnl.util.lock. At some
        # TODO: point we should just replace it with functions and simplify
        # TODO: the locking code.
        class WriteContextManager:
            def __enter__(cm):
                cm.orig_filename = self.cache_path(key)
                cm.orig_file = None
                if os.path.exists(cm.orig_filename):
                    cm.orig_file = open(cm.orig_filename, "r")

                cm.tmp_filename = self.cache_path(key) + ".tmp"
                cm.tmp_file = open(cm.tmp_filename, "w")

                return cm.orig_file, cm.tmp_file

            def __exit__(cm, type, value, traceback):
                if cm.orig_file:
                    cm.orig_file.close()
                cm.tmp_file.close()

                if value:
                    os.remove(cm.tmp_filename)

                else:
                    rename(cm.tmp_filename, cm.orig_filename)

        return WriteTransaction(self._get_lock(key), acquire=WriteContextManager)

    def mtime(self, key) -> float:
        """Return modification time of cache file, or -inf if it does not exist.

        Time is in units returned by os.stat in the mtime field, which is
        platform-dependent.

        """
        if not self.init_entry(key):
            return -math.inf
        else:
            return os.stat(self.cache_path(key)).st_mtime

    def remove(self, key):
        file = self.cache_path(key)
        lock = self._get_lock(key)
        try:
            lock.acquire_write()
            os.unlink(file)
        except OSError as e:
            # File not found is OK, so remove is idempotent.
            if e.errno != errno.ENOENT:
                raise
        finally:
            lock.release_write()


class CacheError(SpackError):
    pass

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import os
import pathlib
import shutil
from typing import IO, Optional, Tuple, Union

from llnl.util.filesystem import rename

from spack.util.cache import Cache, CacheError


def _maybe_open(path: Union[str, pathlib.Path]) -> Optional[IO[str]]:
    try:
        return open(path, "r", encoding="utf-8")
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
        return None


class ReadContextManager:
    def __init__(self, path: Union[str, pathlib.Path]) -> None:
        self.path = path

    def __enter__(self) -> Optional[IO[str]]:
        """Return a file object for the cache if it exists."""
        self.cache_file = _maybe_open(self.path)
        return self.cache_file

    def __exit__(self, type, value, traceback):
        if self.cache_file:
            self.cache_file.close()


class WriteContextManager:
    def __init__(self, path: Union[str, pathlib.Path]) -> None:
        self.path = path
        self.tmp_path = f"{self.path}.tmp"

    def __enter__(self) -> Tuple[Optional[IO[str]], IO[str]]:
        """Return (old_file, new_file) file objects, where old_file is optional."""
        self.old_file = _maybe_open(self.path)
        self.new_file = open(self.tmp_path, "w", encoding="utf-8")
        return self.old_file, self.new_file

    def __exit__(self, type, value, traceback):
        if self.old_file:
            self.old_file.close()
        self.new_file.close()

        if value:
            os.remove(self.tmp_path)
        else:
            rename(self.tmp_path, self.path)


class FileCache(Cache):
    """This class manages cached data per file

    - The FileCache handles locking cache files for reading and writing, so
      client code need not manage locks for cache entries.
    """

    def _acquire_read_fn(self, path):
        return lambda: ReadContextManager(path)

    def _acquire_write_fn(self, path):
        return lambda: WriteContextManager(path)

    def _entry_validation(self, cache_path):
        # Avoid using pathlib here to allow the logic below to
        # function as is
        # TODO: Maybe refactor the following logic for pathlib
        exists = os.path.exists(cache_path)
        if exists:
            if not cache_path.is_file():
                raise CacheError(f"Cache file is not a file: {cache_path}")

            if not os.access(cache_path, os.R_OK):
                raise CacheError(f"Cannot access cache file: {cache_path}")
        else:
            # if the file is hierarchical, make parent directories
            parent = cache_path.parent
            if parent != self.root:
                parent.mkdir(parents=True, exist_ok=True)

            if not os.access(parent, os.R_OK | os.W_OK):
                raise CacheError("Cannot access cache directory: %s" % parent)
        return exists

    def _rm_cache_entry(self, cache_path):
        cache_path.unlink()


class DirectoryFileCache(Cache):
    """This class manages cached data on a per directory level"""

    def _acquire_read_fn(self, path):
        return lambda: path.exists()

    def _acquire_write_fn(self, path):
        return lambda: path.exists()

    def _entry_validation(self, cache_path):
        if cache_path.exists() and not cache_path.is_dir():
            raise CacheError(
                "Entry must refer to directory (bucket) not a file. "
                "If a File level cache is required, use FileCache"
            )
        cache_path.mkdir(parents=True, exist_ok=True)
        if not os.access(cache_path, os.R_OK | os.W_OK):
            raise CacheError(f"Cannot read/write from cache bucket {cache_path}")
        return True

    def _rm_cache_entry(self, cache_path):
        shutil.rmtree(cache_path)

    def purge_lock(self, key):
        # cleanup lockfile itself
        lock = self._get_lock(key)
        lock.cleanup()
        # remove from lock dict
        self._locks.pop(key)

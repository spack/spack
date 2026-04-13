# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import os
import pathlib
import shutil
import tempfile
from contextlib import contextmanager
from typing import IO, Dict, Iterator, Optional, Tuple, Union

from spack.error import SpackError
from spack.llnl.util.filesystem import rename
from spack.util.lock import Lock


def _maybe_open(path: Union[str, pathlib.Path]) -> Optional[IO[str]]:
    try:
        return open(path, "r", encoding="utf-8")
    except IsADirectoryError:
        raise CacheError("Cache file is not a file: %s" % path)
    except PermissionError:
        raise CacheError("Cannot access cache file: %s" % path)
    except FileNotFoundError:
        return None


def _open_temp(context_dir: Union[str, pathlib.Path]) -> Tuple[IO[str], str]:
    """Open a temporary file in a directory

    This implementation minimizes the number of system calls for the case
    the target directory already exists.
    """
    try:
        fd, path = tempfile.mkstemp(dir=context_dir)
    except FileNotFoundError:
        os.makedirs(context_dir, exist_ok=True)
        fd, path = tempfile.mkstemp(dir=context_dir)

    stream = os.fdopen(fd, "w", encoding="utf-8")
    return stream, path


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

    def __enter__(self) -> Tuple[Optional[IO[str]], IO[str]]:
        """Return (old_file, new_file) file objects, where old_file is optional."""
        try:
            self.old_file = _maybe_open(self.path)
            self.new_file, self.tmp_path = _open_temp(os.path.dirname(self.path))
        except PermissionError:
            if self.old_file:
                self.old_file.close()
            raise CacheError(f"Insufficient permissions to write to file cache at {self.path}")
        return self.old_file, self.new_file

    def __exit__(self, type, value, traceback):
        if self.old_file:
            self.old_file.close()
        self.new_file.close()

        if value:
            try:
                os.remove(self.tmp_path)
            except OSError:
                pass
        else:
            rename(self.tmp_path, self.path)


class FileCache:
    """This class manages cached data in the filesystem.

    - Cache files are fetched and stored by unique keys.  Keys can be relative
      paths, so that there can be some hierarchy in the cache.

    - The FileCache handles locking cache files for reading and writing, so
      client code need not manage locks for cache entries.

    """

    def __init__(self, root: Union[str, pathlib.Path], timeout=120):
        """Create a file cache object.

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

        self.lock_path = self.root / ".lock"
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

    def _get_lock_offsets(self, key: str) -> Tuple[int, int]:
        """Hash function to determine byte-range offsets for a key. Returns (start, length) for
        the lock."""
        hasher = hashlib.sha256(key.encode("utf-8"))
        hash_int = int.from_bytes(hasher.digest()[:8], "little")
        start_offset = hash_int % (2**63 - 1)
        return start_offset, 1

    def _get_lock(self, key: Union[str, pathlib.Path]):
        """Create a lock for a key using byte-range offsets."""
        key_str = str(key)

        if key_str not in self._locks:
            start, length = self._get_lock_offsets(key_str)
            self._locks[key_str] = Lock(
                str(self.lock_path),
                start=start,
                length=length,
                default_timeout=self.lock_timeout,
                desc=f"key:{key_str}",
            )
        return self._locks[key_str]

    @contextmanager
    def read_transaction(self, key: Union[str, pathlib.Path]) -> Iterator[Optional[IO[str]]]:
        """Get a read transaction on a file cache item.

        Returns a context manager that yields an open file object for reading,
        or None if the cache file does not exist.  You can use it like this::

           with file_cache_object.read_transaction(key) as cache_file:
               if cache_file is not None:
                   cache_file.read()

        """
        lock = self._get_lock(key)
        lock.acquire_read()
        try:
            with ReadContextManager(self.cache_path(key)) as f:
                yield f
        finally:
            lock.release_read()

    @contextmanager
    def write_transaction(
        self, key: Union[str, pathlib.Path]
    ) -> Iterator[Tuple[Optional[IO[str]], IO[str]]]:
        """Get a write transaction on a file cache item.

        Returns a context manager that yields (old_file, new_file) where old_file
        is the existing cache file (or None), and new_file is a writable temporary
        file.  Once the context manager exits cleanly, moves the temporary file
        into place atomically.

        """
        path = self.cache_path(key)
        lock = self._get_lock(key)
        try:
            lock.acquire_write()
        except PermissionError:
            raise CacheError(f"Insufficient permissions to write to file cache at {path}")
        try:
            with WriteContextManager(str(path)) as (old, new):
                yield old, new
        finally:
            lock.release_write()

    def remove(self, key: Union[str, pathlib.Path]):
        file = self.cache_path(key)
        lock = self._get_lock(key)
        lock.acquire_write()
        try:
            file.unlink()
        except FileNotFoundError:
            pass
        finally:
            lock.release_write()


class CacheError(SpackError):
    pass

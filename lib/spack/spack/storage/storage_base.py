# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib
import urllib.parse
import uuid
from contextlib import contextmanager
from datetime import datetime
from typing import IO, Callable, Dict, Iterator, Optional, Type, Union

import spack.error


class StatResult:
    """Result from stating a key in Storage."""

    def __init__(
        self,
        size: int,
        mtime: datetime,
        created_at: Optional[datetime] = None,
        accessed_at: Optional[datetime] = None,
    ):
        self.size = size
        self.mtime = mtime
        self.ctime = created_at
        self.atime = accessed_at

    size: int
    mtime: datetime
    ctime: Optional[datetime]
    atime: Optional[datetime]

    def __str__(self):
        return f"{self.size} bytes, {self.mtime}"


class StorageBase:
    """Storage is an abstract class that implements APIs with the guarentee
    of atomic reads and writes to a backing storage location.
    """

    def __init__(self, url: Union[str, urllib.parse.ParseResult]):
        if not isinstance(url, urllib.parse.ParseResult):
            self.url = urllib.parse.urlparse(url)
        else:
            self.url = url

        self._can_write: Optional[bool] = None

    def try_read(self, key: Union[str, pathlib.Path]) -> Optional[IO[str]]:
        """Attempt to get object from storage. On failure return None.

        Args:
            key: key of the item in the store
        """
        try:
            return self.read(key)
        except Exception:
            return None

    def read(self, key: Union[str, pathlib.Path]) -> IO[str]:
        """Read object from storage without locking guarentees.

        Args:
            key: key of the item in the store
        """
        raise UnimplementedStorageInterface("read")

    @contextmanager
    def read_transaction(self, key: Union[str, pathlib.Path]):
        """Create a reading context. If storage 'is_lockable' this guarantees
        no write occurs during read. Otherwise guarentees atomic read.

            Args:
                key: key of the item in the store

            Return:
                reading context that yields an Optional[IO[str]]
        """
        yield self.try_read(key)

    def write(self, key: Union[str, pathlib.Path], stream: Optional[IO[str]] = None):
        """Write object into storage. This operation is generally atomic.

        Args:
            key: key of the item in the store
            steam (optional): stream of data to write.
                If this is none than the file simply created in the store.
        """
        raise UnimplementedStorageInterface("write")

    @contextmanager
    def write_transaction(self, key: Union[str, pathlib.Path]):
        """Create a write transaction context. If storage 'is_lockable' this
        guarantees single writer. Otherwise guarentees an atomic write.

            Args:
                key: key of the item in the store

            Returns:
                A Context manager the produces a tuple of two streams.
                    1. A stream to the current content stored at the key if it exists or None.
                    2. A local stream that will be written to the key when exiting the context.
        """
        from io import StringIO

        # Create a local write buffer
        write_buffer = StringIO()
        yield self.read(key), write_buffer  # type: ignore

        write_buffer.seek(0)
        self.write(key, write_buffer)

    def list(self, filter_fn: Optional[Callable[[str], bool]] = None) -> Iterator[str]:
        """List objects in storage with prefix.

        Args:
            filter_fn: A callback to filter the results of the list
        """

        if not filter_fn:
            filter_fn = lambda x: True

        for item in self._list():
            if filter_fn(item):
                yield item

    def list_prefix(self, prefix: Union[str, pathlib.Path]) -> Iterator[str]:
        prefix_filter = lambda key: str(key).lstrip("/").startswith(str(prefix).lstrip("/"))
        for item in self.list(prefix_filter):
            yield item

    def _list(self) -> Iterator[str]:
        """List all objects in the store"""
        raise UnimplementedStorageInterface("_list")

    def delete(self, key: Union[str, pathlib.Path]):
        """Delete a key from the storage."""
        raise UnimplementedStorageInterface("delete")

    def stat(self, key: Union[str, pathlib.Path]) -> Optional[StatResult]:
        raise UnimplementedStorageInterface("stat")

    @property
    def is_lockable(self) -> bool:
        """Check if the key in the storage is lockable."""
        return False

    @property
    def can_write(self) -> bool:
        if self._can_write is not None:
            return self._can_write

        # Probe writing to the store.
        # All storage should raise on failure to write
        test_key = str(uuid.uuid4())
        try:
            with self.write_transaction(test_key) as (_, new):
                new.write(".")
            self.delete(test_key)
            self._can_write = True
        except Exception:
            self._can_write = False
            pass

        return self._can_write


_storage_types: Dict[str, Dict[str, Type[StorageBase]]] = {}


def storage(storage_type: str, storage_id: Optional[str] = None):
    """Register a new storage type.

    Args:
        storage_type: The primary key denoting the type of the underlying store.
        storage_id (optional): a way to override the storage implementation for kwown
            netlocs with more advanced query capabilities (ie. binaries.spack.io)
    """

    def register(cls):
        if storage_type not in _storage_types:
            _storage_types[storage_type] = {}

        stores = _storage_types[storage_type]
        name = storage_id or "__default__"

        if name in stores:
            raise DuplicateStorageSchema(f"{name} was previously registered as {storage_type}")

        assert issubclass(cls, StorageBase)

        stores[name] = cls
        return cls

    return register


def from_url(url: Union[str, urllib.parse.ParseResult], **kwargs) -> StorageBase:
    """Construct a registered storage object from a URL"""
    if not isinstance(url, urllib.parse.ParseResult):
        url = urllib.parse.urlparse(url)

    storage_type = url.scheme
    storage_name = "__default__"

    try:
        stores = _storage_types.get(url.scheme, {})
        if stores:
            if url.netloc and url.netloc in stores:
                storage_name = url.netloc

            return stores[storage_name](url, **kwargs)
        else:
            return _storage_types.get("__default__", {})[storage_name](url, **kwargs)

    except KeyError as e:
        raise UnknownStorageTypeError(f"type: {storage_type}, name: {storage_name}") from e


class DuplicateStorageSchema(spack.error.SpackError):
    """Duplicate names registered under the same storage scheme"""


class UnknownStorageTypeError(spack.error.SpackError):
    """Unknown storage type and or name detected"""


class UnimplementedStorageInterface(spack.error.SpackError):
    """Storage interface not implemented"""

    def __init__(self, interface):
        super().__init__(f"Unimplemented interface: {interface}")

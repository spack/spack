# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib
from datetime import datetime
from typing import IO, Iterator, Optional, Union

import spack.util.file_cache as fc

from .storage_base import StatResult, StorageBase, storage


@storage("file")
class LocalFileSystem(StorageBase):
    def __init__(self, url, **kwargs):
        super().__init__(url)

        timeout = kwargs.get("timeout", 120)
        self.file_cache = fc.FileCache(self.url.path, timeout)

    def read(self, key: Union[str, pathlib.Path]) -> IO[str]:
        return open(key, "r", encoding="utf-8")

    def read_transaction(self, key: Union[str, pathlib.Path]):
        return self.file_cache.read_transaction(key)

    def write(self, key: Union[str, pathlib.Path], data: Optional[IO[str]] = None):
        if not data:
            self.file_cache.init_entry(key)
        else:
            with self.file_cache.write_transaction(key) as (old, out):
                out.write(data.read())

    def write_transaction(self, key: Union[str, pathlib.Path]):
        return self.file_cache.write_transaction(key)

    def _list(self) -> Iterator[str]:
        root = pathlib.Path(self.url.path)
        for node in self._list_node(root, recursive=True):
            yield str(node.relative_to(self.url.path))

    def _list_node(self, root: pathlib.Path, recursive: bool = True) -> Iterator[pathlib.Path]:
        dirstack = []
        for node in root.iterdir():
            if node.is_dir():
                dirstack.append(node)
            else:
                yield node

        if recursive:
            for dnode in dirstack:
                for node in self._list_node(dnode, recursive):
                    yield node

    def delete(self, key: Union[str, pathlib.Path], prune: bool = False):
        node = self.file_cache.cache_path(key)

        if node.is_file():
            node.unlink(missing_ok=True)
        if node.is_dir():
            node.rmdir()

    def stat(self, key: Union[str, pathlib.Path]) -> Optional[StatResult]:
        node = self.file_cache.cache_path(key)
        if node.exists():
            result = node.stat()
            return StatResult(
                result.st_size,
                datetime.fromtimestamp(result.st_mtime),
                datetime.fromtimestamp(result.st_ctime),
                datetime.fromtimestamp(result.st_atime),
            )
        return None

    @property
    def is_lockable(self) -> bool:
        return True

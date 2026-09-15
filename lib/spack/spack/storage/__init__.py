# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Import any modules with storage implementions from here,
# so they get registered without introducing any import
# cycles.
from .gcs import GCS  # noqa: F401
from .localfs import LocalFileSystem  # noqa: F401
from .s3 import S3  # noqa: F401
from .storage_base import (
    DuplicateStorageSchema,
    StorageBase,
    UnimplementedStorageInterface,
    UnknownStorageTypeError,
    from_url,
    storage,
)
from .url_generic import URLStore  # noqa: F401

__all__ = [
    "storage",
    "StorageBase",
    "from_url",
    "DuplicateStorageSchema",
    "UnknownStorageTypeError",
    "UnimplementedStorageInterface",
]

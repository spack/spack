# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import io
import pathlib
import re
import urllib
from datetime import datetime
from typing import IO, Iterator, Optional, Union

import spack.util.gcs as gcs

from .storage_base import StatResult, StorageBase, storage


@storage("gs")
@storage("gcs")
class GCS(StorageBase):
    def __init__(self, url, **kwargs):
        super().__init__(url)
        self.client = gcs.gcs_client()

    def _blob_url(self, key: Union[str, pathlib.Path]) -> str:
        prefix = re.sub(r"^/*", "/", self.url.path)
        blob_path = str(pathlib.PurePosixPath(pathlib.Path(prefix) / key)).lstrip("/")
        return urllib.parse.urljoin(urllib.parse.urlunparse(self.url), blob_path)

    def read(self, key: Union[str, pathlib.Path]) -> IO[str]:
        blob = gcs.GCSBlob(self._blob_url(key), self.client)
        return blob.get_blob_byte_stream()

    def write(self, key: Union[str, pathlib.Path], data: Optional[IO[str]] = None):
        if not data:
            data = io.StringIO()

        bucket = gcs.GCSBucket(self.url, self.client)
        blob_path = urllib.parse.urlparse(self._blob_url(key)).path
        blob = bucket.blob(blob_path)
        blob.upload_from_file(data)

    def _list(self) -> Iterator[str]:
        bucket = gcs.GCSBucket(self.url)
        return bucket.get_all_blobs(recursive=True)

    def delete(self, key: Union[str, pathlib.Path]):
        blob = gcs.GCSBlob(self._blob_url(key), self.client)
        blob.delete_blob()

    def stat(self, key: Union[str, pathlib.Path]) -> StatResult:
        blob = gcs.GCSBlob(self._blob_url(key), self.client)
        header = blob.get_blob_headers()
        return StatResult(
            int(header["Content-Length"]),
            datetime.strptime(header["Last-Modified"], "%Y-%m-%d-%H:%M:%S.%f"),
            created_at=datetime.strptime(header["Created-At"], "%Y-%m-%d-%H:%M:%S.%f"),
        )

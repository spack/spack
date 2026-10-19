# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains the definition of the GCS Blob storage Class used to
integrate GCS Blob storage with spack buildcache.
"""

import functools
import posixpath
import sys
import urllib.parse
import urllib.response
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import URLError
from urllib.request import BaseHandler

from spack.util import tty


def gcs_command(command):
    @functools.wraps(command)
    def _gcs_command_wrapped(*args, **kwargs):
        client = gcs_client()
        try:
            return command(*args, **kwargs)
        except client.GoogleAPIError as e:
            raise urllib.error.URLError(e) from e

    return _gcs_command_wrapped


GCS_CLIENT_CACHE: Optional[Any] = None


def gcs_client():
    """Create a GCS client
    Creates an authenticated GCS client to access GCS buckets and blobs
    """

    global GCS_CLIENT_CACHE
    if GCS_CLIENT_CACHE is not None:
        return GCS_CLIENT_CACHE

    try:
        import google.auth
        from google.api_core.exceptions import GoogleAPIError
        from google.cloud import storage
        from google.cloud.exceptions import ClientError, NotFound
    except ImportError as ex:
        tty.error(
            "{0}, google-cloud-storage python module is missing.".format(ex)
            + " Please install to use the gs:// backend."
        )
        sys.exit(1)

    storage_credentials, storage_project = google.auth.default()
    storage_client = storage.Client(storage_project, storage_credentials)
    setattr(storage_client, "ClientError", ClientError)
    setattr(storage_client, "NotFound", NotFound)
    setattr(storage_client, "GoogleAPIError", GoogleAPIError)

    GCS_CLIENT_CACHE = storage_client
    return storage_client


GCS_BUCKET_CACHE: Dict[str, Any] = {}


class GCSBucket:
    """GCS Bucket Object
    Create a wrapper object for a GCS Bucket. Provides methods to wrap spack
    related tasks, such as destroy.
    """

    def __init__(self, url, client=None):
        """Constructor for GCSBucket objects

        Args:
          url (str): The url pointing to the GCS bucket to build an object out of
          client (google.cloud.storage.client.Client): A pre-defined storage
                 client that will be used to access the GCS bucket.
        """
        if url.scheme != "gs":
            raise ValueError(
                "Can not create GCS bucket connection with scheme {SCHEME}".format(
                    SCHEME=url.scheme
                )
            )
        self.url = url
        self.name = self.url.netloc
        self.prefix = self.url.path.lstrip("/")

        self.client = client or gcs_client()

        self._bucket = None
        tty.debug("New GCS bucket:")
        tty.debug("    name: {0}".format(self.name))
        tty.debug("    prefix: {0}".format(self.prefix))

    @property
    def bucket(self):
        if self._bucket is not None:
            return self._bucket

        global GCS_BUCKET_CACHE
        if self.name in GCS_BUCKET_CACHE:
            self._bucket = GCS_BUCKET_CACHE[self.name]
            return self._bucket

        try:
            self._bucket = self.client.bucket(self.name)
            if self._bucket is not None:
                GCS_BUCKET_CACHE[self.name] = self._bucket
        except self.client.NotFound as ex:
            tty.error("{0}, Failed to get GCS bucket".format(ex))

        return self._bucket

    @gcs_command
    def exists(self):
        return self.bucket is not None

    @gcs_command
    def create(self):
        global GCS_BUCKET_CACHE
        if not self.bucket:
            self.bucket = self.client.create_bucket(self.name)
            if self.bucket is not None:
                GCS_BUCKET_CACHE[self.name] = self.bucket

    @gcs_command
    def get_blob(self, blob_path):
        if self.exists():
            return self.bucket.get_blob(blob_path)
        return None

    @gcs_command
    def blob(self, blob_path):
        if self.exists():
            return self.bucket.blob(blob_path)
        return None

    @gcs_command
    def get_all_blobs(self, recursive: bool = True, relative: bool = True) -> List[str]:
        """Get a list of all blobs

        Returns: a list of all blobs within this bucket.

        Args:
            relative: If true (default), print blob paths relative to 'build_cache' directory.
                If false, print absolute blob paths (useful for destruction of bucket)
        """
        tty.debug("Getting GCS blobs... Recurse {0} -- Rel: {1}".format(recursive, relative))

        converter = self._relative_blob_name if relative else str

        blob_list: List[str] = []

        if self.exists():
            all_blobs = self.bucket.list_blobs(prefix=self.prefix)

            base_dirs = len(self.prefix.split("/")) + 1

            for blob in all_blobs:
                if not recursive:
                    num_dirs = len(blob.name.split("/"))
                    if num_dirs <= base_dirs:
                        blob_list.append(converter(blob.name))
                else:
                    blob_list.append(converter(blob.name))

        return blob_list

    def _relative_blob_name(self, blob_name):
        return posixpath.relpath(blob_name, self.prefix)

    @gcs_command
    def destroy(self, recursive=False, **kwargs):
        """Bucket destruction method

        Deletes all blobs within the bucket, and then deletes the bucket itself.

        Uses GCS Batch operations to bundle several delete operations together.
        """
        tty.debug("Bucket.destroy(recursive={0})".format(recursive))
        try:
            bucket_blobs = self.get_all_blobs(recursive=recursive, relative=False)
            batch_size = 1000

            num_blobs = len(bucket_blobs)
            for i in range(0, num_blobs, batch_size):
                with self.client.batch():
                    for j in range(i, min(i + batch_size, num_blobs)):
                        blob = self.blob(bucket_blobs[j])
                        blob.delete()
        except self.client.NotFound as ex:
            tty.error("{0}, Could not delete a blob in bucket {1}.".format(ex, self.name))


class GCSBlob:
    """GCS Blob object

    Wraps some blob methods for spack functionality
    """

    def __init__(self, url, client=None):
        self.url = url
        if url.scheme != "gs":
            raise ValueError(
                "Can not create GCS blob connection with scheme: {SCHEME}".format(
                    SCHEME=url.scheme
                )
            )

        self.client = client or gcs_client()

        self.bucket = GCSBucket(url)

        self.blob_path = self.url.path.lstrip("/")

        tty.debug("New GCSBlob")
        tty.debug("  blob_path = {0}".format(self.blob_path))

        if not self.bucket.exists():
            tty.warn("The bucket {0} does not exist, it will be created".format(self.bucket.name))
            self.bucket.create()

    @gcs_command
    def get(self):
        return self.bucket.get_blob(self.blob_path)

    @gcs_command
    def exists(self):
        try:
            blob = self.bucket.blob(self.blob_path)
            exists = blob.exists()
        except self.client.NotFound:
            return False

        return exists

    @gcs_command
    def delete_blob(self):
        try:
            blob = self.bucket.blob(self.blob_path)
            blob.delete()
        except self.client.NotFound as ex:
            tty.error("{0}, Could not delete gcs blob {1}".format(ex, self.blob_path))

    @gcs_command
    def upload_to_blob(self, local_file_path):
        blob = self.bucket.blob(self.blob_path)
        blob.upload_from_filename(local_file_path)

    @gcs_command
    def get_blob_byte_stream(self):
        return self.bucket.get_blob(self.blob_path).open(mode="rb")

    @gcs_command
    def get_blob_headers(self):
        blob = self.bucket.get_blob(self.blob_path)

        if not blob:
            return {}

        headers = {
            "Content-type": blob.content_type,
            "Content-encoding": blob.content_encoding,
            "Content-language": blob.content_language,
            "MD5Hash": blob.md5_hash,
        }

        return headers

    @gcs_command
    def stat(self) -> Optional[Tuple[int, float]]:
        blob = self.bucket.get_blob(self.blob_path)
        if not blob:
            return None
        return blob.size, blob.time_created.timestamp()


def gcs_open(req, *args, **kwargs):
    """Open a reader stream to a blob object on GCS"""
    url = urllib.parse.urlparse(req.get_full_url())
    client = gcs_client()
    try:
        gcsblob = GCSBlob(url)

        if not gcsblob.exists():
            raise URLError("GCS blob {0} does not exist".format(gcsblob.blob_path))
        stream = gcsblob.get_blob_byte_stream()
        headers = gcsblob.get_blob_headers()
    except client.GoogleAPIError as e:
        raise URLError(e) from e

    return urllib.response.addinfourl(stream, headers, url)


class GCSHandler(BaseHandler):
    def gs_open(self, req):
        return gcs_open(req)

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains the definition of the GCS Blob storage Class used to
integrate GCS Blob storage with spack buildcache.
"""

import email.message
import functools
import posixpath
import sys
import urllib.error
import urllib.parse
import urllib.response
from typing import Any, Dict, List, Optional, Tuple
from urllib.request import BaseHandler

from spack.util import tty


def _to_urllib_error(e, url: str) -> urllib.error.URLError:
    """Translate a google.api_core GoogleAPICallError into a urllib error."""
    code = getattr(e, "code", None)
    if code is None:
        # No HTTP status (e.g. gRPC-only error)
        return urllib.error.URLError(e)

    hdrs = email.message.Message()
    response = getattr(e, "response", None)
    for k, v in getattr(response, "headers", {}).items():
        hdrs[k] = v

    return urllib.error.HTTPError(url, int(code), str(e.message), hdrs, None)


def gcs_command(command):
    """Translate GCS API errors raised by ``command`` into urllib errors"""

    @functools.wraps(command)
    def _gcs_command_wrapped(*args, **kwargs):
        obj = args[0]
        client = obj.client
        try:
            return command(*args, **kwargs)
        except client.GoogleAPICallError as e:
            raise _to_urllib_error(e, obj.url.geturl()) from e
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
        from google.api_core.exceptions import GoogleAPICallError, GoogleAPIError
        from google.cloud import storage
    except ImportError as ex:
        tty.error(
            "{0}, google-cloud-storage python module is missing.".format(ex)
            + " Please install to use the gs:// backend."
        )
        sys.exit(1)

    storage_credentials, storage_project = google.auth.default()
    storage_client = storage.Client(storage_project, storage_credentials)
    # Error types translated to urllib errors by gcs_command
    setattr(storage_client, "GoogleAPICallError", GoogleAPICallError)
    setattr(storage_client, "GoogleAPIError", GoogleAPIError)

    GCS_CLIENT_CACHE = storage_client
    return storage_client


GCS_BUCKET_CACHE: Dict[str, Any] = {}


class GCSBucket:
    """GCS Bucket Object
    Create a wrapper object for a GCS Bucket. Provides methods to wrap spack
    related tasks, such as destroy.
    """

    def __init__(self, url):
        """Constructor for GCSBucket objects

        Args:
          url (str): The url pointing to the GCS bucket to build an object out of
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

        self.client = gcs_client()

        self._bucket = None
        tty.debug("New GCS bucket:")
        tty.debug("    name: {0}".format(self.name))
        tty.debug("    prefix: {0}".format(self.prefix))

    @property
    def bucket(self):
        if self._bucket is not None:
            return self._bucket

        if self.name in GCS_BUCKET_CACHE:
            self._bucket = GCS_BUCKET_CACHE[self.name]
            return self._bucket

        # client.bucket() does not make an API call, it only creates the bucket handle
        self._bucket = self.client.bucket(self.name)
        GCS_BUCKET_CACHE[self.name] = self._bucket

        return self._bucket

    @gcs_command
    def exists(self):
        return self.bucket.exists()

    @gcs_command
    def create(self):
        self._bucket = self.client.create_bucket(self.name)
        GCS_BUCKET_CACHE[self.name] = self._bucket

    @gcs_command
    def get_blob(self, blob_path):
        return self.bucket.get_blob(blob_path)

    @gcs_command
    def blob(self, blob_path):
        return self.bucket.blob(blob_path)

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
        bucket_blobs = self.get_all_blobs(recursive=recursive, relative=False)
        batch_size = 1000

        num_blobs = len(bucket_blobs)
        for i in range(0, num_blobs, batch_size):
            with self.client.batch():
                for j in range(i, min(i + batch_size, num_blobs)):
                    blob = self.blob(bucket_blobs[j])
                    blob.delete()


class GCSBlob:
    """GCS Blob object

    Wraps some blob methods for spack functionality
    """

    def __init__(self, url):
        self.url = url
        if url.scheme != "gs":
            raise ValueError(
                "Can not create GCS blob connection with scheme: {SCHEME}".format(
                    SCHEME=url.scheme
                )
            )

        self.client = gcs_client()

        self.bucket = GCSBucket(url)

        self.blob_path = self.url.path.lstrip("/")

        tty.debug("New GCSBlob")
        tty.debug("  blob_path = {0}".format(self.blob_path))

    @gcs_command
    def ensure_bucket_exists(self):
        if not self.bucket.exists():
            tty.warn("The bucket {0} does not exist, it will be created".format(self.bucket.name))
            self.bucket.create()

    @gcs_command
    def get(self):
        return self.bucket.get_blob(self.blob_path)

    @gcs_command
    def exists(self):
        # blob.exists() reports a missing blob or bucket as False rather than raising
        return self.bucket.blob(self.blob_path).exists()

    @gcs_command
    def delete_blob(self):
        try:
            blob = self.bucket.blob(self.blob_path)
            blob.delete()
        except self.client.GoogleAPICallError as ex:
            if ex.code != 404:
                raise
            tty.error("{0}, Could not delete gcs blob {1}".format(ex, self.blob_path))

    @gcs_command
    def upload_to_blob(self, local_file_path):
        self.ensure_bucket_exists()

        blob = self.bucket.blob(self.blob_path)
        blob.upload_from_filename(local_file_path)

    @gcs_command
    def stat(self) -> Optional[Tuple[int, float]]:
        # get_blob() returns None for a missing blob or bucket
        blob = self.get()
        if blob is None:
            return None
        return blob.size, blob.time_created.timestamp()

    @gcs_command
    def urllib_open(self):
        """Open a reader stream to this blob as a urllib response"""
        blob = self.get()
        if blob is None:
            raise urllib.error.HTTPError(
                self.url.geturl(),
                404,
                "GCS blob {0} does not exist".format(self.blob_path),
                email.message.Message(),
                None,
            )

        headers = {
            "Content-type": blob.content_type,
            "Content-encoding": blob.content_encoding,
            "Content-language": blob.content_language,
            "MD5Hash": blob.md5_hash,
        }

        return urllib.response.addinfourl(blob.open(mode="rb"), headers, self.url)


def gcs_open(req, *args, **kwargs):
    """Open a reader stream to a blob object on GCS"""
    return GCSBlob(urllib.parse.urlparse(req.get_full_url())).urllib_open()


class GCSHandler(BaseHandler):
    def gs_open(self, req):
        return gcs_open(req)

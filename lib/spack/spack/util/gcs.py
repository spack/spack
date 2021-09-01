# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains the definition of the GCS Blob storage Class used to
integrate GCS Blob storage with spack buildcache.
"""

import os
import sys

import llnl.util.tty as tty

class GCSBlob:
    def __init__(self, url):
        from google.cloud import storage
        import google.auth

        self.url = url
        (self.bucket_name, self.blob_path) = self.get_bucket_blob_path()
        if url.scheme != 'gs':
            raise ValueError('Can not create GCS blob connection with scheme: {SCHEME}'
                             .format(SCHEME=url.scheme))

        self.storage_credentials, self.storage_project = google.auth.default()
        self.storage_client = storage.Client(self.storage_project,
                                             self.storage_credentials)
        if not self.gcs_bucket_exists():
            tty.warn("The bucket {} does not exist, it will be created"
                     .format(self.bucket_name))
            self.storage_client.create_bucket(self.bucket_name)

    def get_bucket_blob_path(self):
        blob_path = self.url.path
        if blob_path[0] == '/':
            blob_path = blob_path[1:]
        bucket_name = self.url.netloc
        tty.debug("bucket_name = {}, blob_path = {}".format(bucket_name, blob_path))
        return (bucket_name, blob_path)

    def get_blob(self):
        return self.storage_client.get_bucket(self.bucket_name).get_blob(self.blob_path)

    def is_https(self):
        return False

    def gcs_bucket_exists(self):
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
        except Exception as ex:
            tty.error("{}, Failed check for bucket existence".format(ex))
            sys.exit(1)
        return (bucket is not None)

    def gcs_blob_exists(self):
        from google.cloud import storage
        try:
            blob = self.storage_client.bucket(self.bucket_name).blob(self.blob_path)
            blob_exists = blob.exists()
        except Exception:
            return False

        return blob_exists

    def gcs_delete_blob(self):
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.blob_path)
            blob.delete()
        except Exception as ex:
            tty.error("{}, Could not delete gcs blob {}".format(ex, self.blob_path))

    def gcs_upload_to_blob(self, local_file_path):
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.blob_path.lstrip("/"))
            blob.upload_from_filename(local_file_path)
        except Exception as ex:
            tty.error("{}, Could not upload {} to gcs blob storage"
                      .format(ex, local_file_path))
            sys.exit(1)

    def gcs_list_blobs(self):
        try:
            blobs = self.storage_client.list_blobs(self.bucket_name,
                                                   prefix=self.blob_path)
            blob_list = []
            for blob in blobs:
                p = blob.name.split('/')
                build_cache_index = p.index('build_cache')
                blob_list.append(os.path.join(*p[build_cache_index + 1:]))
            return blob_list

        except Exception as ex:
            tty.error("{}, Could not get a list of gcs blobs".format(ex))
            sys.exit(1)

    def get_blob_byte_stream(self):
        return self.get_blob().open(mode='rb')

    def get_blob_headers(self):
        blob = self.get_blob()

        headers = {}
        headers['Content-type'] = blob.content_type
        headers['Content-encoding'] = blob.content_encoding
        headers['Content-language'] = blob.content_language
        headers['MD5Hash'] = blob.md5_hash

        return headers

    def gcs_url(self):
        import os
        from google.auth.transport import requests
        from google.auth import compute_engine
        from datetime import datetime, timedelta

        try:
            auth_request = requests.Request()
            data_bucket = self.storage_client.lookup_bucket(self.bucket_name)
            blob = data_bucket.get_blob(self.blob_path)

            if blob is not None:
                return blob.path()
            return None

        except Exception as ex:
            tty.error("{}, Could not generate a URL for GCS blob storage"
                      .format(ex))
            sys.exit(1)


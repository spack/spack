# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import urllib.parse
import urllib.response
from urllib.error import URLError
from urllib.request import BaseHandler


def gcs_open(req, *args, **kwargs):
    """Open a reader stream to a blob object on GCS"""
    import spack.util.gcs as gcs_util

    url = urllib.parse.urlparse(req.get_full_url())
    gcsblob = gcs_util.GCSBlob(url)

    if not gcsblob.exists():
        raise URLError("GCS blob {0} does not exist".format(gcsblob.blob_path))
    stream = gcsblob.get_blob_byte_stream()
    headers = gcsblob.get_blob_headers()

    return urllib.response.addinfourl(stream, headers, url)


class GCSHandler(BaseHandler):
    def gs_open(self, req):
        return gcs_open(req)

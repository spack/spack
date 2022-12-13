# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import urllib.parse
import urllib.response

import spack.util.web as web_util


def gcs_open(req, *args, **kwargs):
    """Open a reader stream to a blob object on GCS"""
    import spack.util.gcs as gcs_util

    url = urllib.parse.urlparse(req.get_full_url())
    gcsblob = gcs_util.GCSBlob(url)

    if not gcsblob.exists():
        raise web_util.SpackWebError("GCS blob {0} does not exist".format(gcsblob.blob_path))
    stream = gcsblob.get_blob_byte_stream()
    headers = gcsblob.get_blob_headers()

    return urllib.response.addinfourl(stream, headers, url)

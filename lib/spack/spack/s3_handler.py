# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from io import BufferedReader, BytesIO

import spack.util.s3 as s3_util


def _s3_open(url, method="GET"):
    parsed = urllib.parse.urlparse(url)
    s3 = s3_util.get_s3_session(url, method="fetch")

    bucket = parsed.netloc
    key = parsed.path

    if key.startswith("/"):
        key = key[1:]

    if method not in ("GET", "HEAD"):
        raise urllib.error.URLError(
            "Only GET and HEAD verbs are currently supported for the s3:// scheme"
        )

    try:
        if method == "GET":
            obj = s3.get_object(Bucket=bucket, Key=key)
            # Note: botocore composes StreamingBody(raw_stream), which for old
            # versions does not inherit anything, making it cumbersome to use
            # as a stream. The wrapper does the following:
            # 1. Allow users to set a timeout on read()
            # 2. Throw when content-length is incorrect.
            # Right now the benefits of using this class and having and adapter
            # for old versions etc does not outweigh the benefits.  Instead, we
            # can use raw_stream directly, which is a
            # urllib3.response.HTTPResponse object. Unlike
            # http.client.HTTPResponse it does *not* support peek() out of the
            # box, so we wrap it in BufferedReader. There's again a caveat, namely
            # https://github.com/urllib3/urllib3/commit/f0d9ebc41e51c4c4c9990b1eed02d297fd1b20d8
            # is required for this wrapper to work. Thefore we end up needing
            # urllib3 v1.25.4, which is required from botocore >= 1.19,
            # or py-boto3 >= 1.16, and a *possible dependency* from botocore >= 1.12,
            # or py-boto3 >= 1.9.
            stream = obj["Body"]._raw_stream
            stream.auto_close = False
        elif method == "HEAD":
            obj = s3.head_object(Bucket=bucket, Key=key)
            stream = BytesIO()
    except s3.ClientError as e:
        raise urllib.error.URLError(e) from e

    headers = obj["ResponseMetadata"]["HTTPHeaders"]

    # Wrap in BufferedReader to make it peekable like http.client.HTTPResponse.
    return url, headers, BufferedReader(stream)


class UrllibS3Handler(urllib.request.BaseHandler):
    def s3_open(self, req):
        orig_url = req.get_full_url()
        url, headers, stream = _s3_open(orig_url, method=req.get_method())
        return urllib.response.addinfourl(stream, headers, url)

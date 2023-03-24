# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from io import BufferedReader, BytesIO, IOBase

import spack.util.s3 as s3_util


# NOTE(opadron): Workaround issue in boto where its StreamingBody
# implementation is missing several APIs expected from IOBase.  These missing
# APIs prevent the streams returned by boto from being passed as-are along to
# urllib.
#
# https://github.com/boto/botocore/issues/879
# https://github.com/python/cpython/pull/3249
class WrapStream(BufferedReader):
    def __init__(self, raw):
        # In botocore >=1.23.47, StreamingBody inherits from IOBase, so we
        # only add missing attributes in older versions.
        # https://github.com/boto/botocore/commit/a624815eabac50442ed7404f3c4f2664cd0aa784
        if not isinstance(raw, IOBase):
            raw.readable = lambda: True
            raw.writable = lambda: False
            raw.seekable = lambda: False
            raw.closed = False
            raw.flush = lambda: None
        super(WrapStream, self).__init__(raw)

    def detach(self):
        self.raw = None

    def read(self, *args, **kwargs):
        return self.raw.read(*args, **kwargs)

    def __getattr__(self, key):
        return getattr(self.raw, key)


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
            # NOTE(opadron): Apply workaround here (see above)
            stream = WrapStream(obj["Body"])
        elif method == "HEAD":
            obj = s3.head_object(Bucket=bucket, Key=key)
            stream = BytesIO()
    except s3.ClientError as e:
        raise urllib.error.URLError(e) from e

    headers = obj["ResponseMetadata"]["HTTPHeaders"]

    return url, headers, stream


class UrllibS3Handler(urllib.request.BaseHandler):
    def s3_open(self, req):
        orig_url = req.get_full_url()
        url, headers, stream = _s3_open(orig_url, method=req.get_method())
        return urllib.response.addinfourl(stream, headers, url)

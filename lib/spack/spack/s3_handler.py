# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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


def client_error_to_http_error(url, e):
    """Adaptor to transform S3 ClientError errors into HTTPError.
    This makes error handling easier, since the call-site can deal
    uniformly with status codes. In particular it's easier to
    deal specifically with 404 Not Found or 304 Not Modified
    errors without having to worry about the protocol."""
    metadata = e.response.get("ResponseMetadata", None)

    if not metadata:
        return urllib.error.URLError(e)

    code = metadata.get("HTTPStatusCode", None)

    if code:
        error = e.response.get("Error", {})
        return urllib.error.HTTPError(
            url=url,
            code=code,
            msg=error.get("Message", ""),
            hdrs=metadata.get("HTTPHeaders", {}),
            fp=None,
        )

    return urllib.error.URLError(e)


def request_to_s3_client_kwargs(req: urllib.request.Request):
    """Adaptor for Request -> s3 get_*(...) kwargs.
    This allows us to translate HTTP headers like If-None-Match: <tag>
    to the approriate key."""
    url = urllib.parse.urlparse(req.get_full_url())
    kwargs = {"Bucket": url.netloc, "Key": url.path.lstrip("/")}

    # Maybe this can be more efficient as header keys are
    # case-normalized. Right now we only handle If-None-Match.
    for name, value in req.header_items():
        if name.lower() == "if-none-match":
            # HTTP rfc's require quotes, s3 does not.
            kwargs["IfNoneMatch"] = value.replace('"', "")
    return kwargs


def _s3_open(url, method="GET", **kwargs):
    client = s3_util.get_s3_session(url, method="fetch")

    if method not in ("GET", "HEAD"):
        raise urllib.error.URLError(
            "Only GET and HEAD verbs are currently supported for the s3:// scheme"
        )

    try:
        if method == "GET":
            obj = client.get_object(**kwargs)
            # NOTE(opadron): Apply workaround here (see above)
            stream = WrapStream(obj["Body"])
        elif method == "HEAD":
            obj = client.head_object(**kwargs)
            stream = BytesIO()
    except client.ClientError as e:
        raise client_error_to_http_error(url, e) from e

    headers = obj["ResponseMetadata"]["HTTPHeaders"]

    return url, headers, stream


class UrllibS3Handler(urllib.request.BaseHandler):
    def s3_open(self, req):
        orig_url = req.get_full_url()
        url, headers, stream = _s3_open(
            url=orig_url, method=req.get_method(), **request_to_s3_client_kwargs(req)
        )
        return urllib.response.addinfourl(stream, headers, url)

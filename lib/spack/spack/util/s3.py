# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import posixpath
import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from io import BufferedReader, BytesIO, IOBase
from typing import Any, Dict, List, Optional, Tuple

import spack.config
import spack.error
from spack.util import tty

#: Map (mirror name, method) tuples to s3 client instances.
s3_client_cache: Dict[Tuple[str, str], Any] = dict()


def get_s3_session(url, method="fetch"):
    # import boto and friends as late as possible.  We don't want to require boto as a
    # dependency unless the user actually wants to access S3 mirrors.
    from boto3 import Session
    from botocore import UNSIGNED
    from botocore.client import Config
    from botocore.exceptions import ClientError

    # translate method to fetch/push
    method = method.lower()
    if method not in ("fetch", "push"):
        method = "fetch" if method in ("get", "head") else "push"

    # Circular dependency
    from spack.mirrors.mirror import MirrorCollection

    global s3_client_cache

    # Parse the URL if not already done.
    if not isinstance(url, urllib.parse.ParseResult):
        url = urllib.parse.urlparse(url)
    url_str = url.geturl()

    def get_mirror_url(mirror):
        return mirror.fetch_url if method == "fetch" else mirror.push_url

    # Get all configured mirrors that could match.
    all_mirrors = MirrorCollection()
    mirrors = [
        (name, mirror)
        for name, mirror in all_mirrors.items()
        if url_str.startswith(get_mirror_url(mirror))
    ]

    if not mirrors:
        name, mirror = None, {}
    else:
        # In case we have more than one mirror, we pick the longest matching url.
        # The heuristic being that it's more specific, and you can have different
        # credentials for a sub-bucket (if that is a thing).
        name, mirror = max(
            mirrors, key=lambda name_and_mirror: len(get_mirror_url(name_and_mirror[1]))
        )

    key = (name, method)

    # Did we already create a client for this? Then return it.
    if key in s3_client_cache:
        return s3_client_cache[key], url

    # Otherwise, create it.
    s3_connection, s3_client_args = get_mirror_s3_connection_info(mirror, method)

    session = Session(**s3_connection)
    # if no access credentials provided above, then access anonymously
    if not session.get_credentials():
        s3_client_args["config"] = Config(signature_version=UNSIGNED)

    client = session.client("s3", **s3_client_args)
    client.ClientError = ClientError

    # Cache the client.
    s3_client_cache[key] = client
    return client, url


def _parse_s3_endpoint_url(endpoint_url):
    if not urllib.parse.urlparse(endpoint_url, scheme="").scheme:
        endpoint_url = f"https://{endpoint_url}"

    return endpoint_url


def get_mirror_s3_connection_info(mirror, method):
    """Create s3 config for session/client from a Mirror instance (or just set defaults
    when no mirror is given.)"""
    from spack.mirrors.mirror import Mirror

    s3_connection = {}
    s3_client_args = {"use_ssl": spack.config.CONFIG.get("config:verify_ssl")}

    # access token
    if isinstance(mirror, Mirror):
        credentials = mirror.get_credentials(method)
        if credentials:
            if "access_token" in credentials:
                s3_connection["aws_session_token"] = credentials["access_token"]

            if "access_pair" in credentials:
                s3_connection["aws_access_key_id"] = credentials["access_pair"][0]
                s3_connection["aws_secret_access_key"] = credentials["access_pair"][1]

            if "profile" in credentials:
                s3_connection["profile_name"] = credentials["profile"]

        # endpoint url
        endpoint_url = mirror.get_endpoint_url(method) or os.environ.get("S3_ENDPOINT_URL")
    else:
        endpoint_url = os.environ.get("S3_ENDPOINT_URL")

    if endpoint_url:
        s3_client_args["endpoint_url"] = _parse_s3_endpoint_url(endpoint_url)
    return s3_connection, s3_client_args


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
        super().__init__(raw)

    def detach(self):
        self.raw = None

    def read(self, *args, **kwargs):
        return self.raw.read(*args, **kwargs)

    def __getattr__(self, key):
        return getattr(self.raw, key)


def _s3_open(url, method="GET"):
    s3, parsed = get_s3_session(url, method=method)

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


def s3_command(method: str):
    """Bind the correct S3 session and capture errors from Boto3."""

    def _s3_decorate_command(command):
        def _s3_command_wrapped(url, *args, **kwargs):
            s3, url = get_s3_session(url, method=method)
            try:
                return command(s3, url, *args, **kwargs)
            except s3.ClientError as e:
                raise urllib.error.URLError(e) from e

        return _s3_command_wrapped

    return _s3_decorate_command


class UrllibS3Handler(urllib.request.BaseHandler):
    def s3_open(self, req):
        orig_url = req.get_full_url()
        url, headers, stream = _s3_open(orig_url, method=req.get_method())
        return urllib.response.addinfourl(stream, headers, url)


def _relative_key(key, prefix):
    if not key.startswith("/"):
        key = "/" + key

    if not prefix.startswith("/"):
        prefix = "/" + prefix

    # S3 keys are always POSIX-style, regardless of the host OS.
    key = posixpath.relpath(key, prefix)

    if key == ".":
        return None

    return key


def _iter_s3_prefix(s3, url, num_entries=1024):
    bucket = url.netloc
    prefix = url.path.strip("/") + "/"
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    for item in pages.search("Contents"):
        key = _relative_key(item["Key"], prefix)
        if key is not None:
            yield key


@s3_command("fetch")
def list_objects(s3, url: urllib.parse.ParseResult, recursive: bool = False):
    """List contents under a url.

    Args:
        url: S3 URL (ie. s3://bucket/some/prefix/)
        recursive: List prefix recursively.
    Returns:
        List of keys under the bucket/prefix.
    """
    if recursive:
        return list(_iter_s3_prefix(s3, url))

    return list({key.split("/", 1)[0] for key in _iter_s3_prefix(s3, url)})


def _debug_print_delete_results(result):
    if "Deleted" in result:
        for d in result["Deleted"]:
            tty.debug("Deleted {0}".format(d["Key"]))
    if "Errors" in result:
        for e in result["Errors"]:
            tty.debug("Failed to delete {0} ({1})".format(e["Key"], e["Message"]))


@s3_command("push")
def delete_objects(s3, url: urllib.parse.ParseResult, recursive: bool = False):
    # Try to find a mirror for potential connection information
    bucket = url.netloc
    if recursive:
        # Because list_objects_v2 can only return up to 1000 items
        # at a time, we have to paginate to make sure we get it all
        prefix = url.path.strip("/")
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        delete_request: Dict[str, List[Dict[str, str]]] = {"Objects": []}
        for item in pages.search("Contents"):
            if not item:
                continue

            delete_request["Objects"].append({"Key": item["Key"]})

            # Make sure we do not try to hit S3 with a list of more
            # than 1000 items
            if len(delete_request["Objects"]) >= 1000:
                r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                _debug_print_delete_results(r)
                delete_request = {"Objects": []}

        # Delete any items that remain
        if len(delete_request["Objects"]):
            r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
            _debug_print_delete_results(r)
    else:
        s3.delete_object(Bucket=bucket, Key=url.path.lstrip("/"))


@s3_command("fetch")
def stat_object(s3, url: urllib.parse.ParseResult) -> Optional[Tuple[int, float]]:
    """Get stat result for a URL.

    Args:
        url: URL to get stat result for
    Returns:
        A tuple of (size, mtime) if the URL exists, None otherwise.
    """
    s3_bucket = url.netloc
    s3_key = url.path.lstrip("/")
    try:
        head_request = s3.head_object(Bucket=s3_bucket, Key=s3_key)
    except s3.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return None
        raise e

    mtime = head_request["LastModified"].timestamp()
    size = head_request["ContentLength"]
    return size, mtime


@s3_command("psuh")
def push_object(s3, url: urllib.parse.ParseResult, local_file_path, extra_args):
    if extra_args is None:
        extra_args = {}

    remote_path = url.path
    while remote_path.startswith("/"):
        remote_path = remote_path[1:]

    if extra_args.get("IfMatch") is not None:
        # IfMatch is only supported by put_object which has additional limitations
        if os.stat(local_file_path).st_size >= 5e9:
            raise spack.error.SpackError(f"File too large (max. 5GB): {local_file_path}")

        with open(local_file_path, "rb") as fd:
            s3.put_object(Bucket=url.netloc, Key=remote_path, Body=fd, **extra_args)
    else:
        s3.upload_file(local_file_path, url.netloc, remote_path, ExtraArgs=extra_args)

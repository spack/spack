# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import functools
import os
import posixpath
import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from io import BufferedReader, BytesIO, IOBase
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from spack.vendor.typing_extensions import Literal

import spack.error
from spack.util import tty

if TYPE_CHECKING:
    import spack.mirrors.mirror
    import spack.util.web

#: Session and client arguments an s3 client is created with, each sorted by name.
S3ClientKey = Tuple[Tuple[Tuple[str, Any], ...], Tuple[Tuple[str, Any], ...]]

#: Map the arguments an s3 client is created with to the client.
s3_client_cache: Dict[S3ClientKey, Any] = {}

#: Allowed HTTP request methods
S3OpenMethod = Literal["get", "head", "GET", "HEAD"]

#: Allowed mirror direction selection names for S3 Mirrors
MirrorDirection = Literal["push", "fetch"]


def _get_s3_session(
    url,
    method: Literal[S3OpenMethod, MirrorDirection] = "fetch",
    *,
    client: "spack.util.web.NetworkClient",
):
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

    # Parse the URL if not already done.
    if not isinstance(url, urllib.parse.ParseResult):
        url = urllib.parse.urlparse(url)
    url_str = url.geturl()

    def get_mirror_url(mirror):
        return mirror.fetch_url if method == "fetch" else mirror.push_url

    # Get all configured mirrors that could match.
    mirrors = [mirror for mirror in client.mirrors if url_str.startswith(get_mirror_url(mirror))]

    # In case we have more than one mirror, we pick the longest matching url.
    # The heuristic being that it's more specific, and you can have different
    # credentials for a sub-bucket (if that is a thing).
    mirror = max(mirrors, key=lambda m: len(get_mirror_url(m))) if mirrors else None

    s3_connection, s3_client_args = get_mirror_s3_connection_info(
        mirror, method, verify_ssl=client.verify_ssl
    )
    key = (tuple(sorted(s3_connection.items())), tuple(sorted(s3_client_args.items())))

    # Did we already create a client for this? Then return it.
    if key in s3_client_cache:
        return s3_client_cache[key], url

    session = Session(**s3_connection)
    # if no access credentials provided above, then access anonymously
    if not session.get_credentials():
        s3_client_args["config"] = Config(signature_version=UNSIGNED)

    s3_client = session.client("s3", **s3_client_args)
    s3_client.ClientError = ClientError

    # Cache the client.
    s3_client_cache[key] = s3_client
    return s3_client, url


def _parse_s3_endpoint_url(endpoint_url):
    if not urllib.parse.urlparse(endpoint_url, scheme="").scheme:
        endpoint_url = f"https://{endpoint_url}"

    return endpoint_url


def get_mirror_s3_connection_info(
    mirror: Optional["spack.mirrors.mirror.Mirror"], method, *, verify_ssl: bool
):
    """Create s3 config for session/client from a Mirror instance (or just set defaults
    when no mirror is given.)"""
    s3_connection = {}
    s3_client_args: Dict[str, Any] = {"use_ssl": verify_ssl}

    # access token
    if mirror is not None:
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


def _s3_open(url, method: S3OpenMethod = "GET", *, client: "spack.util.web.NetworkClient"):
    s3, parsed = _get_s3_session(url, method=method, client=client)

    bucket = parsed.netloc
    key = parsed.path

    if key.startswith("/"):
        key = key[1:]

    if method not in ("GET", "HEAD"):
        raise urllib.error.URLError(
            "Only GET and HEAD verbs are currently supported for the s3:// scheme"
        )

    stream: IOBase
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


def s3_command(method: MirrorDirection):
    """Bind the correct S3 session and capture errors from Boto3."""

    def _s3_decorate_command(command):
        @functools.wraps(command)
        def _s3_command_wrapped(url, *args, client: "spack.util.web.NetworkClient", **kwargs):
            s3, url = _get_s3_session(url, method=method, client=client)
            try:
                return command(s3, url, *args, **kwargs)
            except s3.ClientError as e:
                raise urllib.error.URLError(e) from e

        return _s3_command_wrapped

    return _s3_decorate_command


class UrllibS3Handler(urllib.request.BaseHandler):
    def __init__(self, client: "spack.util.web.NetworkClient") -> None:
        self.client = client

    def s3_open(self, req):
        orig_url = req.get_full_url()
        url, headers, stream = _s3_open(orig_url, method=req.get_method(), client=self.client)
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


def _iter_s3_prefix(s3, url, relative: bool = False, num_entries: int = 1024):
    bucket = url.netloc
    stripped_path = url.path.strip("/")
    prefix = f"{stripped_path}/" if stripped_path else ""
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix, MaxKeys=num_entries)

    for item in pages.search("Contents"):
        if not item:
            continue

        if relative:
            key = _relative_key(item["Key"], prefix)
        else:
            key = item["Key"]

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
        return list(_iter_s3_prefix(s3, url, relative=True))

    return list({key.split("/", 1)[0] for key in _iter_s3_prefix(s3, url, relative=True)})


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
    if not recursive:
        s3.delete_object(Bucket=bucket, Key=url.path.lstrip("/"))
        return

    # Because list_objects_v2 can only return up to 1000 items
    # at a time, we have to paginate to make sure we get it all
    delete_request: Dict[str, List[Dict[str, str]]] = {"Objects": []}
    for key in _iter_s3_prefix(s3, url, relative=False):
        delete_request["Objects"].append({"Key": key})

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


@s3_command("push")
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

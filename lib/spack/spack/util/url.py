# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import os
import pathlib
import posixpath
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional, Union

from llnl.util import tty

import spack.util.spack_yaml as syaml
from spack.util.path import sanitize_filename, substitute_path_variables


def validate_scheme(scheme):
    """Returns true if the URL scheme is generally known to Spack. This function
    helps mostly in validation of paths vs urls, as Windows paths such as
    C:/x/y/z (with backward not forward slash) may parse as a URL with scheme
    C and path /x/y/z."""
    return scheme in ("file", "http", "https", "ftp", "s3", "gs", "ssh", "git", "oci")


def local_file_path(url):
    """Get a local file path from a url.

    If url is a ``file://`` URL, return the absolute path to the local
    file or directory referenced by it.  Otherwise, return None.
    """
    if isinstance(url, str):
        url = urllib.parse.urlparse(url)

    if url.scheme == "file":
        return urllib.request.url2pathname(url.path)

    return None


def path_to_file_url(path):
    return Path(path).absolute().as_uri()


def file_url_string_to_path(url):
    return urllib.request.url2pathname(urllib.parse.urlparse(url).path)


def is_path_instead_of_url(path_or_url):
    """Historically some config files and spack commands used paths
    where urls should be used. This utility can be used to validate
    and promote paths to urls."""
    return not validate_scheme(urllib.parse.urlparse(path_or_url).scheme)


def format(parsed_url):
    """Format a URL string

    Returns a canonicalized format of the given URL as a string.
    """
    if isinstance(parsed_url, str):
        parsed_url = urllib.parse.urlparse(parsed_url)

    return parsed_url.geturl()


def join(base: str, *components: str, resolve_href: bool = False, **kwargs) -> str:
    """Convenience wrapper around :func:`urllib.parse.urljoin`, with a few differences:

    1. By default ``resolve_href=False``, which makes the function like :func:`os.path.join`.
       For example ``https://example.com/a/b + c/d = https://example.com/a/b/c/d``. If
       ``resolve_href=True``, the behavior is how a browser would resolve the URL:
       ``https://example.com/a/c/d``.
    2. ``s3://``, ``gs://``, ``oci://`` URLs are joined like ``http://`` URLs.
    3. It accepts multiple components for convenience. Note that ``components[1:]`` are treated as
       literal path components and appended to ``components[0]`` separated by slashes."""
    # Ensure a trailing slash in the path component of the base URL to get os.path.join-like
    # behavior instead of web browser behavior.
    if not resolve_href:
        parsed = urllib.parse.urlparse(base)
        if not parsed.path.endswith("/"):
            base = parsed._replace(path=f"{parsed.path}/").geturl()
    old_netloc = urllib.parse.uses_netloc
    old_relative = urllib.parse.uses_relative
    try:
        # NOTE: we temporarily modify urllib internals so s3 and gs schemes are treated like http.
        # This is non-portable, and may be forward incompatible with future cpython versions.
        urllib.parse.uses_netloc = [*old_netloc, "s3", "gs", "oci", "oci+http"]  # type: ignore
        urllib.parse.uses_relative = [*old_relative, "s3", "gs", "oci", "oci+http"]  # type: ignore
        return urllib.parse.urljoin(base, "/".join(components), **kwargs)
    finally:
        urllib.parse.uses_netloc = old_netloc  # type: ignore
        urllib.parse.uses_relative = old_relative  # type: ignore


def default_download_filename(url: str) -> str:
    """This method computes a default file name for a given URL.
    Note that it makes no request, so this is not the same as the
    option curl -O, which uses the remote file name from the response
    header."""
    parsed_url = urllib.parse.urlparse(url)
    # Only use the last path component + params + query + fragment
    name = urllib.parse.urlunparse(
        parsed_url._replace(scheme="", netloc="", path=posixpath.basename(parsed_url.path))
    )
    valid_name = sanitize_filename(name)

    # Don't download to hidden files please
    if valid_name[0] == ".":
        valid_name = "_" + valid_name[1:]

    return valid_name


def parse_link_rel_next(link_value: str) -> Optional[str]:
    """Return the next link from a Link header value, if any."""

    # Relaxed version of RFC5988
    uri = re.compile(r"\s*<([^>]+)>\s*")
    param_key = r"[^;=\s]+"
    quoted_string = r"\"([^\"]+)\""
    unquoted_param_value = r"([^;,\s]+)"
    param = re.compile(rf";\s*({param_key})\s*=\s*(?:{quoted_string}|{unquoted_param_value})\s*")

    data = link_value

    # Parse a list of <url>; key=value; key=value, <url>; key=value; key=value, ... links.
    while True:
        uri_match = re.match(uri, data)
        if not uri_match:
            break
        uri_reference = uri_match.group(1)
        data = data[uri_match.end() :]

        # Parse parameter list
        while True:
            param_match = re.match(param, data)
            if not param_match:
                break
            key, quoted_value, unquoted_value = param_match.groups()
            value = quoted_value or unquoted_value
            data = data[param_match.end() :]

            if key == "rel" and value == "next":
                return uri_reference

        if not data.startswith(","):
            break

        data = data[1:]

    return None


def handle_windows_file_urls(url: str) -> str:
    """Handles file urls with Windows style paths.
    Colons are present in both network paths as well as
    Windows drive separators.
    A proper Windows file url will have any drive
    delineators prefixed with a forward slash to prevent
    the file path component of the url from being interpreted
    a network location.

    Many file urls with Windows style paths are naively and inccorectly
    composed as 'file://' + path, which results in incorrect parsing

    This method contains some heuristics to detect a Windows file url,
    and marshall it so it's properly formed and thus can be reasoned about

    Arguments:
        url: url being evalulated as a potential Windows file url

    Returns: url if url is not a Windows file url, a properly formated
    Windows file url if it is.
    """
    processed_url = urllib.parse.urlparse(url)
    if not processed_url.scheme:
        # definitely not a url, file or otherwise
        return url
    is_file_url = processed_url.scheme == "file"
    if not is_file_url:
        # not a file url, no need to process
        return url
    if processed_url.path and pathlib.PureWindowsPath(processed_url.path.lstrip("/")).drive:
        # url was actually properly formed
        return url
    if processed_url.netloc and pathlib.PureWindowsPath(processed_url.netloc):
        # A file url shouldn't have a netloc, but a poorly formed Windows url will
        return "file:///" + processed_url.netloc

    # if the above didn't catch this, this is likely a relative path, and requires no
    # special handling w.r.t. Windows
    return url


def make_file_url(path: Union[str, pathlib.Path]) -> str:
    """Create properly formatted file url"""
    check_path = pathlib.PureWindowsPath(str(path))
    url_path = str(path)
    if check_path.drive:
        url_path = "/" + url_path
    return urllib.parse.urlunparse(("file", "", url_path, "", "", ""))


def canonicalize_url(url: str, default_wd: Optional[pathlib.Path] = None) -> str:
    """Same as substitute_path_variables, but for urls.

    If the url is a file url:
        If represented by a yaml object with file annotations,
        make absolute paths relative to that file's directory.
        Otherwise, use ``default_wd`` if specified, otherwise
        ``os.getcwd()``

    Arguments:
        url: url being converted as needed
        default_wd: optional working directory/root for non-yaml file urls

    Returns: A canonicalized url. File urls are returned as absolute file urls.
    """
    c_url = substitute_path_variables(url)

    # Now process linux-like paths and remote URLs
    p_url = urllib.parse.urlparse(c_url)
    path = pathlib.PurePath(urllib.request.url2pathname(p_url.path))

    if not p_url.scheme:
        # url argument is not a valid url
        raise RuntimeError("Attempting to canonicalize a non url object from url canonicalization")

    if p_url.scheme != "file":
        # Have a remote URL so simply return it with substitutions
        return c_url

    # Get file in which path was written in case we need to make it absolute
    # relative to that path.

    filename = None
    if isinstance(url, syaml.syaml_str):
        filename = pathlib.Path(
            os.path.dirname(url._start_mark.name)  # type: ignore[attr-defined]
        )
        assert url._start_mark.name == url._end_mark.name  # type: ignore[attr-defined]

    if path.is_absolute():
        return urllib.parse.urlunparse(("file", "", os.path.normpath(path), "", "", ""))

    # Have a relative path so prepend the appropriate dir to make it absolute
    if filename:
        # Prepend the directory of the syaml path
        return urllib.parse.urlunparse(("file", "", os.path.normpath(filename / path), "", "", ""))

    # Prepend the default, if provided, or current working directory.
    base = default_wd or pathlib.Path.cwd()
    tty.debug(f"Using working directory {base} as base for abspath")
    return urllib.parse.urlunparse(("file", "", os.path.normpath(base / path), "", "", ""))

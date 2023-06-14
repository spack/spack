# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def validate_scheme(scheme):
    """Returns true if the URL scheme is generally known to Spack. This function
    helps mostly in validation of paths vs urls, as Windows paths such as
    C:/x/y/z (with backward not forward slash) may parse as a URL with scheme
    C and path /x/y/z."""
    return scheme in ("file", "http", "https", "ftp", "s3", "gs", "ssh", "git")


def local_file_path(url):
    """Get a local file path from a url.

    If url is a file:// URL, return the absolute path to the local
    file or directory referenced by it.  Otherwise, return None.
    """
    if isinstance(url, str):
        url = urllib.parse.urlparse(url)

    if url.scheme == "file":
        return urllib.request.url2pathname(url.path)

    return None


def path_to_file_url(path):
    path = Path(path)
    if not path.is_absolute():
        path = path.absolute()
    return urllib.parse.urljoin("file:", urllib.request.pathname2url(str(path)))


def file_url_string_to_path(url):
    return urllib.request.url2pathname(urllib.parse.urlparse(url).path)


def is_path_instead_of_url(path_or_url):
    """Historically some config files and spack commands used paths
    where urls should be used. This utility can be used to validate
    and promote paths to urls."""
    scheme = urllib.parse.urlparse(path_or_url).scheme

    # On non-Windows, no scheme means it's likely a path
    if not sys.platform == "win32":
        return not scheme

    # On Windows, we may have drive letters.
    return "A" <= scheme <= "Z"


def format(parsed_url):
    """Format a URL string

    Returns a canonicalized format of the given URL as a string.
    """
    if isinstance(parsed_url, str):
        parsed_url = urllib.parse.urlparse(parsed_url)

    return parsed_url.geturl()


def join(base_url, in_path, *extra, **kwargs):
    resolve_href = kwargs.get("resolve_href", False)
    absolute_path = False
    if in_path.startswith("/"):
        in_path = in_path.lstrip("/")
        absolute_path = True

    in_path = Path(in_path, *extra).as_posix()

    if base_url.startswith(("s3", "file")):
        return file_url_join(base_url, in_path, resolve_href, absolute_path)  # file_url_join
    else:
        return real_url_join(base_url, in_path, resolve_href, absolute_path)  # web_url_join


def file_url_join(base_url, in_path, resolve_href, absolute_path):
    (scheme, netloc, path, params, query, fragment) = urllib.parse.urlparse(base_url)

    if netloc:
        path = Path(netloc) / path.lstrip("/")
    else:
        path = Path(path.lstrip("/"))

    if absolute_path:
        base_path = Path()
        in_path = in_path.lstrip("/")
    elif resolve_href:
        base_path = Path(path).parent
    else:
        base_path = Path(path)

    in_path = Path(in_path)

    new_path = join_url_path_segments(base_path, in_path)

    parts = list(new_path.parts)

    if netloc:
        netloc = parts.pop(0)
    path = Path(*parts).as_posix()

    return urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))


def real_url_join(base_url, in_path, resolve_href, absolute_path):
    if resolve_href:
        return urllib.parse.urljoin(base_url, in_path)
    else:
        (scheme, netloc, path, params, query, fragment) = urllib.parse.urlparse(base_url)

        if resolve_href or absolute_path:
            base_path = Path()
            in_path = in_path.lstrip("/")
        else:
            base_path = Path(path)

        in_path = Path(in_path)

        path = join_url_path_segments(base_path, in_path).as_posix()

        return urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))


def join_url_path_segments(base_path, in_path):
    url_parts = base_path.parts + in_path.parts

    final_parts = []
    for part in url_parts:
        if part == "..":
            try:
                final_parts.pop()
            except IndexError:
                continue
        else:
            final_parts.append(part)

    return Path(*final_parts)


git_re = (
    r"^(?:([a-z]+)://)?"  # 1. optional scheme
    r"(?:([^@]+)@)?"  # 2. optional user
    r"([^:/~]+)?"  # 3. optional hostname
    r"(?(1)(?::([^:/]+))?|:)"  # 4. :<optional port> if scheme else :
    r"(.*[^/])/?$"  # 5. path
)


def parse_git_url(url):
    """Parse git URL into components.

    This parses URLs that look like:

    * ``https://host.com:443/path/to/repo.git``, or
    * ``git@host.com:path/to/repo.git``

    Anything not matching those patterns is likely a local
    file or invalid.

    Returned components are as follows (optional values can be ``None``):

    1. ``scheme`` (optional): git, ssh, http, https
    2. ``user`` (optional): ``git@`` for github, username for http or ssh
    3. ``hostname``: domain of server
    4. ``port`` (optional): port on server
    5. ``path``: path on the server, e.g. spack/spack

    Returns:
        (tuple): tuple containing URL components as above

    Raises ``ValueError`` for invalid URLs.
    """
    match = re.match(git_re, url)
    if not match:
        raise ValueError("bad git URL: %s" % url)

    # initial parse
    scheme, user, hostname, port, path = match.groups()

    # special handling for ~ paths (they're never absolute)
    if path.startswith("/~"):
        path = path[1:]

    if port is not None:
        try:
            port = int(port)
        except ValueError:
            raise ValueError("bad port in git url: %s" % url)

    return (scheme, user, hostname, port, path)

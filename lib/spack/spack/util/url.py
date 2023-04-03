# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import itertools
import os
import posixpath
import re
import sys
import urllib.parse
import urllib.request

from spack.util.path import convert_to_posix_path


def validate_scheme(scheme):
    """Returns true if the URL scheme is generally known to Spack. This function
    helps mostly in validation of paths vs urls, as Windows paths such as
    C:/x/y/z (with backward not forward slash) may parse as a URL with scheme
    C and path /x/y/z."""
    return scheme in ("file", "http", "https", "ftp", "s3", "gs", "ssh", "git")


def _split_all(path):
    """Split path into its atomic components.

    Returns the shortest list, L, of strings such that posixpath.join(*L) ==
    path and posixpath.split(element) == ('', element) for every element in L
    except possibly the first.  This first element may possibly have the value
    of '/'.
    """
    result = []
    a = path
    old_a = None
    while a != old_a:
        (old_a, (a, b)) = a, posixpath.split(a)

        if a or b:
            result.insert(0, b or "/")

    return result


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
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return urllib.parse.urljoin("file:", urllib.request.pathname2url(path))


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


def join(base_url, path, *extra, **kwargs):
    """Joins a base URL with one or more local URL path components

    If resolve_href is True, treat the base URL as though it where the locator
    of a web page, and the remaining URL path components as though they formed
    a relative URL to be resolved against it (i.e.: as in posixpath.join(...)).
    The result is an absolute URL to the resource to which a user's browser
    would navigate if they clicked on a link with an "href" attribute equal to
    the relative URL.

    If resolve_href is False (default), then the URL path components are joined
    as in posixpath.join().

    Note: file:// URL path components are not canonicalized as part of this
    operation.  To canonicalize, pass the joined url to format().

    Examples:
      base_url = 's3://bucket/index.html'
      body = fetch_body(prefix)
      link = get_href(body) # link == '../other-bucket/document.txt'

      # wrong - link is a local URL that needs to be resolved against base_url
      spack.util.url.join(base_url, link)
      's3://bucket/other_bucket/document.txt'

      # correct - resolve local URL against base_url
      spack.util.url.join(base_url, link, resolve_href=True)
      's3://other_bucket/document.txt'

      prefix = 'https://mirror.spack.io/build_cache'

      # wrong - prefix is just a URL prefix
      spack.util.url.join(prefix, 'my-package', resolve_href=True)
      'https://mirror.spack.io/my-package'

      # correct - simply append additional URL path components
      spack.util.url.join(prefix, 'my-package', resolve_href=False) # default
      'https://mirror.spack.io/build_cache/my-package'

      # For canonicalizing file:// URLs, take care to explicitly differentiate
      # between absolute and relative join components.
    """
    paths = [
        (x) if isinstance(x, str) else x.geturl() for x in itertools.chain((base_url, path), extra)
    ]

    paths = [convert_to_posix_path(x) for x in paths]
    n = len(paths)
    last_abs_component = None
    scheme = ""
    for i in range(n - 1, -1, -1):
        obj = urllib.parse.urlparse(paths[i], scheme="", allow_fragments=False)

        scheme = obj.scheme

        # in either case the component is absolute
        if scheme or obj.path.startswith("/"):
            if not scheme:
                # Without a scheme, we have to go back looking for the
                # next-last component that specifies a scheme.
                for j in range(i - 1, -1, -1):
                    obj = urllib.parse.urlparse(paths[j], scheme="", allow_fragments=False)

                    if obj.scheme:
                        paths[i] = "{SM}://{NL}{PATH}".format(
                            SM=obj.scheme,
                            NL=((obj.netloc + "/") if obj.scheme != "s3" else ""),
                            PATH=paths[i][1:],
                        )
                        break

            last_abs_component = i
            break

    if last_abs_component is not None:
        paths = paths[last_abs_component:]
        if len(paths) == 1:
            result = urllib.parse.urlparse(paths[0], scheme="file", allow_fragments=False)

            # another subtlety: If the last argument to join() is an absolute
            # file:// URL component with a relative path, the relative path
            # needs to be resolved.
            if result.scheme == "file" and result.netloc:
                result = urllib.parse.ParseResult(
                    scheme=result.scheme,
                    netloc="",
                    path=posixpath.abspath(result.netloc + result.path),
                    params=result.params,
                    query=result.query,
                    fragment=None,
                )

            return result.geturl()

    return _join(*paths, **kwargs)


def _join(base_url, path, *extra, **kwargs):
    base_url = urllib.parse.urlparse(base_url)
    resolve_href = kwargs.get("resolve_href", False)

    (scheme, netloc, base_path, params, query, _) = base_url
    scheme = scheme.lower()

    path_tokens = [
        part
        for part in itertools.chain(
            _split_all(path),
            itertools.chain.from_iterable(_split_all(extra_path) for extra_path in extra),
        )
        if part and part != "/"
    ]

    base_path_args = ["/fake-root"]
    if scheme == "s3":
        if netloc:
            base_path_args.append(netloc)

    if base_path.startswith("/"):
        base_path = base_path[1:]

    base_path_args.append(base_path)

    if resolve_href:
        new_base_path, _ = posixpath.split(posixpath.join(*base_path_args))
        base_path_args = [new_base_path]

    base_path_args.extend(path_tokens)
    base_path = posixpath.relpath(posixpath.join(*base_path_args), "/fake-root")

    if scheme == "s3":
        path_tokens = [part for part in _split_all(base_path) if part and part != "/"]

        if path_tokens:
            netloc = path_tokens.pop(0)
            base_path = posixpath.join("", *path_tokens)

    if sys.platform == "win32":
        base_path = convert_to_posix_path(base_path)

    return format(
        urllib.parse.ParseResult(
            scheme=scheme, netloc=netloc, path=base_path, params=params, query=query, fragment=None
        )
    )


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

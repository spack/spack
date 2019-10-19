# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import itertools
import os.path

from six import string_types
import six.moves.urllib.parse as urllib_parse

import spack.util.path


def _split_all(path):
    """Split path into its atomic components.

    Returns the shortest list, L, of strings such that os.path.join(*L) == path
    and os.path.split(element) == ('', element) for every element in L except
    possibly the first.  This first element may possibly have the value of '/',
    or some other OS-dependent path root.
    """
    result = []
    a = path
    old_a = None
    while a != old_a:
        (old_a, (a, b)) = a, os.path.split(a)

        if a or b:
            result.insert(0, b or '/')

    return result


def local_file_path(url):
    """Get a local file path from a url.

    If url is a file:// URL, return the absolute path to the local
    file or directory referenced by it.  Otherwise, return None.
    """
    if isinstance(url, string_types):
        url = parse(url)

    if url.scheme == 'file':
        return url.path
    return None


def parse(url, scheme='file'):
    """Parse a mirror url.

    For file:// URLs, the netloc and path components are concatenated and
    passed through spack.util.path.canoncalize_path().

    Otherwise, the returned value is the same as urllib's urlparse() with
    allow_fragments=False.
    """

    url_obj = (
        urllib_parse.urlparse(url, scheme=scheme, allow_fragments=False)
        if isinstance(url, string_types) else url)

    (scheme, netloc, path, params, query, _) = url_obj
    scheme = (scheme or 'file').lower()

    if scheme == 'file':
        path = spack.util.path.canonicalize_path(netloc + path)
        while path.startswith('//'):
            path = path[1:]
        netloc = ''

    return urllib_parse.ParseResult(scheme=scheme,
                                    netloc=netloc,
                                    path=path,
                                    params=params,
                                    query=query,
                                    fragment=None)


def format(parsed_url):
    """Format a URL string

    Returns a canonicalized format of the given URL as a string.
    """
    if isinstance(parsed_url, string_types):
        parsed_url = parse(parsed_url)

    return parsed_url.geturl()


def join(base_url, path, *extra, **kwargs):
    """Joins a base URL with one or more local URL path components

    If resolve_href is True, treat the base URL as though it where the locator
    of a web page, and the remaining URL path components as though they formed
    a relative URL to be resolved against it (i.e.: as in os.path.join(...)).
    The result is an absolute URL to the resource to which a user's browser
    would navigate if they clicked on a link with an "href" attribute equal to
    the relative URL.

    If resolve_href is False (default), then the URL path components are joined
    as in os.path.join().

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
    """
    base_url = parse(base_url)
    resolve_href = kwargs.get('resolve_href', False)

    (scheme, netloc, base_path, params, query, _) = base_url
    scheme = scheme.lower()

    path_tokens = [
        part for part in itertools.chain(
            _split_all(path),
            itertools.chain.from_iterable(
                _split_all(extra_path) for extra_path in extra))
        if part and part != '/']

    base_path_args = ['/fake-root']
    if scheme == 's3':
        if netloc:
            base_path_args.append(netloc)

    if base_path.startswith('/'):
        base_path = base_path[1:]

    base_path_args.append(base_path)

    if resolve_href:
        new_base_path, _ = os.path.split(os.path.join(*base_path_args))
        base_path_args = [new_base_path]

    base_path_args.extend(path_tokens)
    base_path = os.path.relpath(os.path.join(*base_path_args), '/fake-root')

    if scheme == 's3':
        path_tokens = [
            part for part in _split_all(base_path)
            if part and part != '/']

        if path_tokens:
            netloc = path_tokens.pop(0)
            base_path = os.path.join('', *path_tokens)

    return format(urllib_parse.ParseResult(scheme=scheme,
                                           netloc=netloc,
                                           path=base_path,
                                           params=params,
                                           query=query,
                                           fragment=None))

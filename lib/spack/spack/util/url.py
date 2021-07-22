# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import itertools
import os.path
import re

import six.moves.urllib.parse as urllib_parse
from six import string_types

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
    """Parse a url.

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
        path = re.sub(r'^/+', '/', path)
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

      # '$spack' is not an absolute path component
      join_result = spack.util.url.join('/a/b/c', '$spack') ; join_result
      'file:///a/b/c/$spack'
      spack.util.url.format(join_result)
      'file:///a/b/c/opt/spack'

      # '/$spack' *is* an absolute path component
      join_result = spack.util.url.join('/a/b/c', '/$spack') ; join_result
      'file:///$spack'
      spack.util.url.format(join_result)
      'file:///opt/spack'
    """
    paths = [
        (x if isinstance(x, string_types) else x.geturl())
        for x in itertools.chain((base_url, path), extra)]
    n = len(paths)
    last_abs_component = None
    scheme = ''
    for i in range(n - 1, -1, -1):
        obj = urllib_parse.urlparse(
            paths[i], scheme='', allow_fragments=False)

        scheme = obj.scheme

        # in either case the component is absolute
        if scheme or obj.path.startswith('/'):
            if not scheme:
                # Without a scheme, we have to go back looking for the
                # next-last component that specifies a scheme.
                for j in range(i - 1, -1, -1):
                    obj = urllib_parse.urlparse(
                        paths[j], scheme='', allow_fragments=False)

                    if obj.scheme:
                        paths[i] = '{SM}://{NL}{PATH}'.format(
                            SM=obj.scheme,
                            NL=(
                                (obj.netloc + '/')
                                if obj.scheme != 's3' else ''),
                            PATH=paths[i][1:])
                        break

            last_abs_component = i
            break

    if last_abs_component is not None:
        paths = paths[last_abs_component:]
        if len(paths) == 1:
            result = urllib_parse.urlparse(
                paths[0], scheme='file', allow_fragments=False)

            # another subtlety: If the last argument to join() is an absolute
            # file:// URL component with a relative path, the relative path
            # needs to be resolved.
            if result.scheme == 'file' and result.netloc:
                result = urllib_parse.ParseResult(
                    scheme=result.scheme,
                    netloc='',
                    path=os.path.abspath(result.netloc + result.path),
                    params=result.params,
                    query=result.query,
                    fragment=None)

            return result.geturl()

    return _join(*paths, **kwargs)


def _join(base_url, path, *extra, **kwargs):
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

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
    result = []
    a = path
    old_a = None
    while a != old_a:
        (old_a, (a, b)) = a, os.path.split(a)

        if a or b:
            result.insert(0, b or '/')

    return result


def local_file_path(url):
    """If [self] is a file:// URL, return the absolute path to the local
    file or directory referenced by [self].  Otherwise, return None.
    """
    if isinstance(url, string_types):
        url = parse(url)

    if url.scheme == 'file':
        return url.path
    return None


def parse(url, scheme='file'):
    """Parse a mirror url."""

    url_obj = (urllib_parse.urlparse(url, scheme=scheme, allow_fragments=False)
            if isinstance(url, string_types) else url)

    (scheme, netloc, path, params, query, _) = url_obj
    scheme = (scheme or 'file').lower()

    extra_attrs = {}

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
    if isinstance(parsed_url, string_types):
        parsed_url = parse(parsed_url)

    return parsed_url.geturl()


def join(base_url, path, *extra):
    if isinstance(base_url, string_types):
        base_url = parse(base_url)

    (scheme, netloc, base_path, params, query, _) = base_url
    scheme = scheme.lower()

    path_tokens = [
            part for part in itertools.chain(
                _split_all(path),
                itertools.chain.from_iterable(
                    _split_all(extra_path) for extra_path in extra))

                if part and part != '/']

    base_path_args = ['/']
    if scheme == 's3':
        if netloc:
            base_path_args.append(netloc)

    if base_path.startswith('/'):
        base_path = base_path[1:]

    base_path_args.append(base_path)
    base_path_args.extend(path_tokens)
    base_path = os.path.relpath(os.path.join(*base_path_args), '/')

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

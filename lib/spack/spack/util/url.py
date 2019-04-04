# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

from os.path import join as pathjoin, split as pathsplit

from six import string_types
from six.moves.urllib.parse import urlparse, ParseResult

from spack.util.path import canonicalize_path

def _split_all(path):
    result = []
    a = path
    old_a = None
    while a != old_a:
        (old_a, (a, b)) = a, pathsplit(a)

        if a or b:
            result.insert(0, b if b else a)

    return result


def parse(url):
    """Parse a mirror url."""
    (scheme, netloc, path, params, query, _) = urlparse(
            url, scheme='file', allow_fragments=False)

    scheme = scheme.lower()
    extra_attrs = {}

    if scheme == 'file':
        path = canonicalize_path(path)
    elif scheme == 's3':
        path_tokens = [part for part in _split_all(path)
                if part and part != '/']

        extra_attrs["s3_bucket"] = (
                path_tokens.pop(0) if path_tokens else None)
        path = pathjoin('', *path_tokens)

        credentials, netloc = (netloc.split('@', 1) + [None])[:2]
        if netloc is None:
            netloc, credentials = credentials, netloc

        if credentials:
            key_id, key_secret = (credentials.split(':', 1) + [None])[:2]

            if key_secret is None:
                extra_attrs["s3_profile"] = key_id
            else:
                extra_attrs["s3_access_key_id"] = key_id
                extra_attrs["s3_secret_access_key"] = key_secret

    result = ParseResult(scheme=scheme,
                         netloc=netloc,
                         path=path,
                         params=params,
                         query=query,
                         fragment=None)

    for key, val in extra_attrs.items():
        setattr(result, key, val)

    return result


def format(parsed_url):
    if isinstance(parsed_url, string_types):
        parsed_url = parse(parsed_url)

    (scheme, netloc, path, params, query, _) = parsed_url

    scheme = scheme.lower()

    if scheme == 's3':
        path = pathjoin(
                *[x for x in ('/', parsed_url.s3_bucket, path) if x])

        credentials = None

        try:
            credentials = parsed_url.s3_profile
        except AttributeError:
            pass

        try:
            if not credentials:
                credentials = ':'.join((
                    parsed_url.s3_access_key_id,
                    parsed_url.s3_secret_access_key))
        except AttributeError:
            pass

        if credentials:
            netloc = '@'.join((credentials, netloc))

    # Workaround a quirk of urlparse where the double-slash after the [scheme]
    # is left out in the case of no [netloc] and a [scheme] that is not natively
    # recognized (e.g.: s3).  S3 URLs will usually specify no [netloc], instead
    # defaulting to AWS and using other mechanisms, like environment variables,
    # to provide access credentials.
    #
    # The point of this workaround is to manipulate these URLs so that instead
    # of being formatted like so:
    #
    #  s3:/my-bucket
    #
    # ... they would be (correctly) formatted like so:
    #
    #  s3:///my-bucket
    #
    if not netloc and scheme not in ('http', 'https', 'file'):
        if not path:
            path = '//'
        else:
            path_tokens = _split_all(path)
            netloc = pathjoin(*path_tokens[:2])
            path = pathjoin('/', *path_tokens[2:])
            if path == '/':
                path = ''

    return ParseResult(scheme=scheme,
                       netloc=netloc,
                       path=path,
                       params=params,
                       query=query,
                       fragment=None).geturl()

def join(base_url, path):
    if isinstance(base_url, string_types):
        base_url = parse(base_url)

    (scheme, netloc, base_path, params, query, _) = base_url

    scheme = scheme.lower()
    extra_attrs = {}

    if scheme == 's3':
        path_tokens = [part for part in _split_all(path)
                if part and part != '/']

        extra_attrs["s3_bucket"] = (
                base_url.s3_bucket if base_url.s3_bucket
                else path_tokens.pop(0) if path_tokens else None)

        base_path = pathjoin('', base_path, *path_tokens)

    result = ParseResult(scheme=scheme,
                         netloc=netloc,
                         path=base_path,
                         params=params,
                         query=query,
                         fragment=None)

    for key, val in extra_attrs.items():
        setattr(result, key, val)

    return format(result)


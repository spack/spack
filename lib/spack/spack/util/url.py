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


class ParseResultWrapper(urllib_parse.ParseResult):
    def __setattr__(self, key, val):
        object.__setattr__(self, key, val)

    @property
    def local_file_path(self):
        """If [self] is a file:// URL, return the absolute path to the local
        file or directory referenced by [self].  Otherwise, return None.
        """
        if self.scheme == 'file':
            return self.path
        return None

    def __str__(self):
        return ''.join((
            super(ParseResultWrapper, self).__str__(),
            ' ({})'.format(str(self.__dict__)) if self.__dict__ else ''))


def _split_all(path):
    result = []
    a = path
    old_a = None
    while a != old_a:
        (old_a, (a, b)) = a, os.path.split(a)

        if a or b:
            result.insert(0, b or '/')

    return result


def parse(url, scheme='file'):
    """Parse a mirror url."""
    url_obj = (urllib_parse.urlparse(url, scheme=scheme, allow_fragments=False)
            if isinstance(url, string_types) else url)

    original_s3_attrs = {}
    for attr in ("s3_bucket", "s3_profile", "s3_access_key_id",
            "secret_access_key"):
        if hasattr(url_obj, attr):
            original_s3_attrs[attr] = getattr(url_obj, attr)

    (scheme, netloc, path, params, query, _) = url_obj
    scheme = (scheme or 'file').lower()

    extra_attrs = {}

    if scheme == 'file':
        path = spack.util.path.canonicalize_path(netloc + path)
        while path.startswith('//'):
            path = path[1:]
        netloc = ''
    elif scheme == 's3':
        if original_s3_attrs:
            extra_attrs.update(original_s3_attrs)
        else:
            # NOTE(opadron): For s3 URLs, we assume API access over https.  If
            # users provide a URL with their own endpoint, they can explicitly
            # specify the API access protocol as part of the netloc.
            #
            # e.g.:  s3://profile@http://host:9000/bucket/path...
            #
            # ...which urllib parses as:
            #
            #        (s3://)(profile@http:)(//host:9000/bucket/path...)
            #       (scheme)(    netloc   )(path                      )
            #
            # This branch takes care of this specific case where part of the
            # "path" needs to be extracted and concatenated to the "netloc".
            #
            # Note, that any API access protocol specified in these URLs are
            # not related to whether Spack validates certificates for https
            # connections.  That is controlled by Spack's config and/or
            # -k/--insecure CLI flags.
            if netloc.endswith(':') and path.startswith('//'):
                netloc_host, path = (path[2:].split('/', 1) + [''])[:2]
                netloc = '//'.join((netloc, netloc_host))

            path_tokens = [part for part in _split_all(path)
                    if part and part != '/']

            extra_attrs["s3_bucket"] = (
                    path_tokens.pop(0) if path_tokens else None)
            path = os.path.join('', *path_tokens)

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

    result = ParseResultWrapper(scheme=scheme,
                                netloc=netloc,
                                path=path,
                                params=params,
                                query=query,
                                fragment=None)

    for key, val in extra_attrs.items():
        setattr(result, key, val)

    return result


def format(parsed_url):
    if not isinstance(parsed_url, ParseResultWrapper):
        parsed_url = parse(parsed_url)

    (scheme, netloc, path, params, query, _) = parsed_url

    scheme = scheme.lower()

    if scheme == 's3':
        path = os.path.join(
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
            netloc = os.path.join(*path_tokens[:2])
            path = os.path.join('/', *path_tokens[2:])
            if path == '/':
                path = ''

    return ParseResultWrapper(scheme=scheme,
                              netloc=netloc,
                              path=path,
                              params=params,
                              query=query,
                              fragment=None).geturl()

def join(base_url, path, *extra):
    if not isinstance(base_url, ParseResultWrapper):
        base_url = parse(base_url)

    (scheme, netloc, base_path, params, query, _) = base_url

    scheme = scheme.lower()
    extra_attrs = {}

    path_tokens = [
            part for part in itertools.chain(
                _split_all(path),
                itertools.chain.from_iterable(
                    _split_all(extra_path) for extra_path in extra))

                if part and part != '/']

    if scheme == 's3':
        try:
            extra_attrs["s3_profile"] = base_url.s3_profile
        except AttributeError:
            try:
                extra_attrs["s3_access_key_id"] = base_url.s3_access_key_id
                extra_attrs["s3_secret_access_key"] = (
                        base_url.s3_secret_access_key)
            except AttributeError:
                pass

        extra_attrs["s3_bucket"] = (
                base_url.s3_bucket if base_url.s3_bucket
                else path_tokens.pop(0) if path_tokens else None)

    base_path = os.path.join('', base_path, *path_tokens)

    result = ParseResultWrapper(scheme=scheme,
                                netloc=netloc,
                                path=base_path,
                                params=params,
                                query=query,
                                fragment=None)

    for key, val in extra_attrs.items():
        setattr(result, key, val)

    return format(result)


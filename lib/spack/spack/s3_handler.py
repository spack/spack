
import itertools as it

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

from io import BufferedReader

from six.moves.urllib.parse import urlparse as _urlparse
from six.moves.urllib.response import addinfourl
from six.moves.urllib.request import build_opener, install_opener, HTTPSHandler

from llnl.util.lang import memoized

import spack
from spack.util.url import parse as urlparse

# NOTE(opadron): Workaround issue in boto where its StreamingBody implementation
# is missing several APIs expected from IOBase.  These missing APIs prevent the
# streams returned by boto from being passed as-are along to urllib.
#
# https://github.com/boto/botocore/issues/879
# https://github.com/python/cpython/pull/3249
class WrapStream(BufferedReader):
    def __init__(self, raw):
        raw.readable = lambda: True
        raw.writable = lambda: False
        raw.seekable = lambda: False
        raw.closed = False
        raw.flush = lambda: None
        super(WrapStream, self).__init__(raw)

    def detach(self):
        self.raw = None

    def read(self, *args, **kwargs):
        return self.raw.read(*args, **kwargs)

    def __getattr__(self, key):
        return getattr(self.raw, key)


class MappingViewWithKeyAliases(Mapping):
    def __init__(self, sub=None, aliases=None):
        self._sub = sub or {}
        self._aliases = []
        self._alias_table = {}

        aliases = [set(x) for x in (aliases or ())]
        num_entries = 0
        while aliases:
            entry = aliases.pop()

            while True:
                ioff = 0
                for i in range(len(aliases)):
                    index = i - ioff
                    candidate = aliases[index]
                    if entry & candidate:
                        entry |= aliases.pop(index)
                        ioff += 1

                if not ioff:
                    break

            self._aliases.append(entry)
            for key in entry:
                self._alias_table[key] = num_entries
            num_entries += 1

    def __getitem__(self, key):
        try:
            return self._sub[key]
        except KeyError as e:
            index = self._alias_table.get(key)
            aliases = (
                    () if index is None else
                    self._aliases[index])

            for alias in aliases:
                try:
                    return self._sub[alias]
                except KeyError:
                    pass

            raise e

    def __set(self):
        return set(self._alias_table.keys()) | set(self._sub.keys())

    def __iter__(self):
        return iter(self.__set())

    def __len__(self):
        return len(self.__set())


HTTP_HEADERS_KEY_ALIASES = (
        tuple(''.join((C, 'ontent', sep, L, 'ength'))
            for C, sep, L in
            it.product('Cc', [''] + list(' _-'), 'Ll')),

        tuple(''.join((A, 'ccept', sep, R, 'anges'))
            for A, sep, R in
            it.product('Aa', [''] + list(' _-'), 'Rr')),

        tuple(''.join((A, 'ccept', sep, R, 'anges'))
            for A, sep, R in
            it.product('Aa', [''] + list(' _-'), 'Rr')),

        tuple(''.join((C, 'ontent', sep, T, 'ype'))
            for C, sep, T in
            it.product('Cc', [''] + list(' _-'), 'Tt')),

        tuple(''.join((L, 'ast', sep, M, 'odified'))
            for L, sep, M in
            it.product('Ll', [''] + list(' _-'), 'Mm')),

        ('Server', 'server'),
        ('Date', 'date')
)


class UrllibS3Handler(HTTPSHandler):
    def s3_open(self, req):
        full_url = req.get_full_url()
        parsed_url = urlparse(full_url)
        assert parsed_url.scheme == 's3'

        # NOTE(opadron): import boto and friends as late as possible.  We don't
        # want to require boto as a dependency unless the user actually wants to
        # access S3 mirrors.
        from boto3 import Session
        kwargs = {}

        if hasattr(parsed_url, 's3_profile'):
            kwargs['profile_name'] = parsed_url.s3_profile

        elif (hasattr(parsed_url, 's3_access_key_id') and
                hasattr(parsed_url, 's3_secret_access_key')):
            kwargs['aws_access_key_id'] = parsed_url.s3_access_key_id
            kwargs['aws_secret_access_key'] = parsed_url.s3_secret_access_key

        session = Session(**kwargs)

        s3_client_args = {"use_ssl": spack.config.get('config:verify_ssl')}

        endpoint_url = parsed_url.netloc
        if endpoint_url:
            if _urlparse(endpoint_url, scheme=None).scheme is None:
                endpoint_url = '://'.join(('https', endpoint_url))

            s3_client_args['endpoint_url'] = endpoint_url

        # if no access credentials provided above, then access anonymously
        if not session.get_credentials():
            from botocore import UNSIGNED
            from botocore.client import Config

            s3_client_args["config"] = Config(signature_version=UNSIGNED)

        s3 = session.client('s3', **s3_client_args)
        obj = s3.get_object(
                Bucket=parsed_url.s3_bucket,
                Key=parsed_url.path)

        # NOTE(opadron): Apply workaround here (see above)
        stream = WrapStream(obj['Body'])
        headers = MappingViewWithKeyAliases(
                obj['ResponseMetadata']['HTTPHeaders'],
                HTTP_HEADERS_KEY_ALIASES)

        return addinfourl(stream, headers, full_url)

S3OpenerDirector = build_opener(UrllibS3Handler())

open = S3OpenerDirector.open


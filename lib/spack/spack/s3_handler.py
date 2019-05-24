
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
from spack.util.url import parse as urlparse, join as urljoin

from spack.util.s3 import create_s3_session


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


def _s3_open(url):
    parsed = urlparse(url)
    s3 = create_s3_session(parsed)
    obj = s3.get_object(
            Bucket=parsed.s3_bucket,
            Key=parsed.path)

    # NOTE(opadron): Apply workaround here (see above)
    stream = WrapStream(obj['Body'])
    headers = MappingViewWithKeyAliases(
            obj['ResponseMetadata']['HTTPHeaders'],
            HTTP_HEADERS_KEY_ALIASES)

    return url, headers, stream


class UrllibS3Handler(HTTPSHandler):
    def s3_open(self, req):
        orig_url = req.get_full_url()
        from botocore.exceptions import ClientError
        try:
            url, headers, stream = _s3_open(orig_url)
            return addinfourl(stream, headers, url)
        except ClientError as err:
            # if no such [KEY], but [KEY]/index.html exists,
            # return that, instead.
            if err.response['Error']['Code'] == 'NoSuchKey':
                try:
                    _, headers, stream = _s3_open(
                            urljoin(orig_url, 'index.html'))
                    return addinfourl(stream, headers, orig_url)

                except ClientError as err2:
                    if err.response['Error']['Code'] == 'NoSuchKey':
                        raise err # raise original error

                    raise err2

            raise err


S3OpenerDirector = build_opener(UrllibS3Handler())

open = S3OpenerDirector.open


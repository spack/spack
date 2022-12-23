# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections.abc
import contextlib
import functools
import hashlib
import io
import json
import shutil
import tempfile
import typing as T
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import spack.util.web as web_util
from spack.util.file_cache import CacheError, FileCache
from spack.util.web import FetchError, SpackWebError


class CacheFetchResult(T.NamedTuple):
    """Result of a cached fetch from a ``NetworkCache``.

    Args:
        file: Open read-only file for the cached/local copy of the
            fetched URL. Always opened in binary mode.
        path: pathlib.Path to the opened file.
        revision: Hashable identifier for the revision of the file. Changes
            in the remote file cause changes in this member.
    """

    file: io.BufferedIOBase
    path: Path
    revision: collections.abc.Hashable


class NetworkCache:
    """Local filesystem cache for requests made across the network.

    Some remote files change infrequently (if ever), but are requested repeatedly
    across multiple operations. This class implements a parallel-process-safe
    and efficient cache for such files, stored in the local filesystem.

    .. code-block::

        root/
        |- request/
        |  `- HA/SSSSH.json: data on cached request(s), name derived from URL hash
        `- response/
           |- HA/SSSSH: response data file, name derived from content hash
           `- HA/SSSSH.json: metadata for matching response data file
    """

    _urlopen: T.ClassVar = web_util.urlopen

    def __init__(self, root: str) -> None:
        self._cache = FileCache(root, timeout=float("inf"))

    def destroy(self):
        self._cache.destroy()

    @contextlib.contextmanager
    def fetch(
        self, url: str, *, sha256_url: T.Optional[str] = None, dry_run: bool = False
    ) -> T.Iterator[T.Optional[CacheFetchResult]]:
        """Fetch the given URL and give read access to the cached copy as a
        file-like object opened in binary mode.

        May make network requests, but avoids downloading the actual file
        whenever possible.

        Args:
            url: URL of the remote file that needs to be fetched
            sha256_url: URL of a hashfile for the url, containing the SHA256sum of
                the remote file. (If present, usually ``url + ".hash"``.)
            dry_run: Don't actually contact any remote servers, consider the cache
                always up-to-date. Returns ``None`` if not in the cache.

        Throws SpackWebError on errors in the server-side stored data or the
        client-side user configuration. Throws FetchError on errors from the
        network. Throws CacheError on errors in the filesystem backing the cache.
        """
        # Handle local files special: don't cache, just return the final Path
        parsed_url = urllib.parse.urlparse(url, scheme="file")
        if parsed_url.scheme == "file":
            try:
                p = Path(parsed_url.path).resolve(strict=True)
                f = open(p, "rb")
            except Exception as e:
                raise FetchError(str(e)) from e
            with f:
                sha256 = _file_sha256(f)
                f.seek(0)
                yield CacheFetchResult(file=f, path=p, revision=sha256)
                return

        # Probe the server (if needed) and bring the cached copy up-to-date
        request_key = self._request_key(url)
        if not dry_run:
            self._refresh(request_key, url, sha256_fetch_fn=self._sha256_fetch_fn(sha256_url))

        if dry_run and not self._cache.init_entry(request_key):
            # Request is not in the cache
            yield None
            return

        # Access the data and return the final response file under read locks
        with self._cache.read_transaction(request_key) as req_f:
            req = CachedRequest.parse(req_f)
            with self._cache.read_transaction(req.data_key, binary=True) as data_f:
                if not req.cache_valid(data_f):
                    raise CacheError(
                        f"Filesystem corruption detected in cached response for {url!r}"
                    )
                data_f.seek(0)
                yield CacheFetchResult(
                    file=data_f,
                    path=Path(self._cache.cache_path(req.data_key)),
                    revision=req.data_sha256,
                )

    def _refresh(self, request_key: str, url: str, **kwargs) -> None:
        """Implementation function for fetch(). Returns the data file's cache key.

        The caller is expected to still verify that the cached response is valid
        according to the request data before using in practice.
        """

        # Read-only pass: check if the request is already cached and still fresh
        if self._cache.init_entry(request_key):
            with self._cache.read_transaction(request_key) as req_f:
                req = CachedRequest.parse(req_f)
            if req.needs_fetch(**kwargs) is None:
                return

        # The request is either not cached or not fresh. We will need to alter
        # the CachedRequest, almost certainly.
        with CachedRequest.parsed_write(self._cache.write_transaction(request_key)) as req:
            headers = req.needs_fetch(**kwargs)
            if headers is None:
                # The request has become fresh, so escape
                return

            # Make the (possibly conditional) request to the server
            headers.update({"User-Agent": web_util.SPACK_USER_AGENT})
            try:
                response = self._urlopen(urllib.request.Request(url, headers=headers))
            except urllib.error.HTTPError as e:
                # The default urllib settings raise HTTP non-2xx responses as
                # HTTPErrors. So we need to catch them here before propagating.
                if e.code == 304:
                    # Condition failed, which means the cache is fresh! Escape.
                    req.mark_fresh(e.headers)
                    return
                raise FetchError(f"Error fetching url, got response code {e.code}: {url!r}") from e
            except urllib.error.URLError as e:
                raise FetchError(f"Error fetching url {url!r}: {e}") from e

            empty_is_fresh = False
            if response.getcode() is None:
                # The urllib handler does not support response codes. Presume
                # that an empty response indicates condition failure (and thus
                # cache freshness).
                empty_is_fresh = True
            elif response.getcode() == 304:
                # Condition failed, which means the cache is fresh! Escape.
                req.mark_fresh(response.headers)
                return
            elif not 200 <= response.getcode() < 300:
                # HTTP codes other than 2xx require additional effort, and cannot
                # be handled here.
                raise FetchError(
                    f"Error fetching url, got response code {response.getcode()}: {url!r}"
                )

            with tempfile.SpooledTemporaryFile() as tmp_f:
                shutil.copyfileobj(response, tmp_f)
                tmp_f.seek(0)
                if empty_is_fresh and not tmp_f.read(1):
                    # Consider fresh
                    req.mark_fresh(response.headers)
                    return

                # Update the Request with the results of the fetch
                old_metadata_key = req.metadata_key
                old_data_key = req.data_key
                req.fetched(response.headers, tmp_f)

                # The data_key did not change. The caller will handle the cache
                # integrity check, so we can escape here.
                if old_data_key == req.data_key:
                    return

                # Mark the final destination as having a request referencing it
                self._cache.init_entry(req.metadata_key)
                with CachedResponseMeta.parsed_write(
                    self._cache.write_transaction(req.metadata_key)
                ) as meta:
                    meta.ref_count += 1

                # Store the data in it's final destination in the cache
                tmp_f.seek(0)
                self._cache.init_entry(req.data_key)
                with self._cache.write_transaction(req.data_key, binary=True) as (_, data_f):
                    shutil.copyfileobj(tmp_f, data_f)

        # Clean up the cache files for the old data_key, since this request
        # now no longer refers to it.
        if old_metadata_key is not None:
            with CachedResponseMeta.parsed_write(
                self._cache.write_transaction(old_metadata_key)
            ) as meta:
                meta.ref_count -= 1
                remove = meta.ref_count <= 0
            if remove:
                self._cache.remove(old_metadata_key)
                self._cache.remove(old_data_key)

    @classmethod
    def _request_key(cls, url: str) -> str:
        h = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return str(Path("request", h[:2], f"{h[2:]}.json"))

    def _sha256_fetch_fn(
        self, url: T.Optional[str]
    ) -> T.Optional[T.Callable[[], T.Optional[bytes]]]:
        if url is None:
            return None

        @functools.lru_cache(maxsize=1)
        def fn() -> T.Optional[bytes]:
            try:
                res = self._urlopen(url)
                if not 200 <= (res.getcode() or 200) < 300:
                    return None

                b: T.Optional[bytes]
                try:
                    b = bytes.fromhex(res.read(64).decode("utf-8"))
                    if len(b) != 32:
                        b = None
                except ValueError:
                    b = None

                if b is None:
                    raise SpackWebError(
                        f"Remote hashfile contains an invalid SHA256sum: url was {url!r}"
                    )
                return b
            except urllib.error.URLError:
                return None

        return fn


class CachedRequest:
    """Convenience type for data about a cached request"""

    def __init__(
        self,
        *,
        data_sha256: T.Union[str, bytes, None] = None,
        etag: T.Optional[str] = None,
        **kwargs,
    ):
        self.data_sha256 = None
        if data_sha256 is not None:
            if isinstance(data_sha256, str):
                data_sha256 = bytes.fromhex(data_sha256)
            if len(data_sha256) == 32:
                self.data_sha256 = data_sha256
        self.etag = etag

    def to_dict(self) -> dict:
        result = {}
        if self.data_sha256 is not None:
            result["data_sha256"] = self.data_sha256.hex()
        for key in ("etag",):
            if getattr(self, key) is not None:
                result[key] = getattr(self, key)
        return result

    @property
    def data_key(self) -> T.Optional[str]:
        if self.data_sha256 is None:
            return None
        return str(Path("response", self.data_sha256[:1].hex(), self.data_sha256[1:].hex()))

    @property
    def metadata_key(self) -> T.Optional[str]:
        if self.data_sha256 is None:
            return None
        return str(
            Path("response", self.data_sha256[:1].hex(), f"{self.data_sha256[1:].hex()}.json")
        )

    def cache_valid(self, data_f: io.BufferedIOBase) -> bool:
        """Check whether the cached copy of this request's response is valid."""
        assert self.data_sha256
        return _file_sha256(data_f) == self.data_sha256

    @classmethod
    def parse(cls, f):
        """Parse a serialized request, absorbing corruption errors"""
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
        return cls(**data)

    @classmethod
    @contextlib.contextmanager
    def parsed_write(cls, transaction):
        """Wrapper to expose a serialized request in a WriteTransaction as a
        full CachedRequest object. Changes will be preserved if there are no
        exceptions raised in the body of the context."""
        with transaction as (old_f, new_f):
            parsed = cls.parse(old_f) if old_f is not None else cls()
            yield parsed
            json.dump(parsed.to_dict(), new_f)

    def needs_fetch(
        self, sha256_fetch_fn: T.Optional[T.Callable[[], T.Optional[bytes]]] = None
    ) -> T.Optional[T.Dict[str, str]]:
        """Determine if this request needs to be re-validated (or fetched). If
        so, returns the headers to use for the conditional fetch."""
        # Prefer ETag-based validation when available
        if self.etag is not None:
            return {"If-None-Match": f'"{self.etag}"'}

        # Fall back to hashfile-based validation in other cases
        if sha256_fetch_fn is not None and self.data_sha256 is not None:
            remote_sha256 = sha256_fetch_fn()
            if remote_sha256 is not None:
                assert len(remote_sha256) == 32
                if self.data_sha256 == remote_sha256:
                    return None

        # Not enough info to decide validity, unconditionally fetch
        return {}

    def fetched(self, headers: T.Any, data_f: io.BufferedIOBase) -> None:
        """Update this CachedRequest based on a recent fetch (200), given the
        response headers and newly fetched data (in the file-like data_f)."""
        self.data_sha256 = _file_sha256(data_f)
        self.etag = web_util.parse_etag(headers.get("etag"))

    def mark_fresh(self, headers: T.Any) -> None:
        """Update this CachedRequest based on a recent validation (304), given
        the response headers."""
        # TODO: Does nothing now, but needed for more complex caching heuristics


class CachedResponseMeta:
    """Convenience type for metadata about a cached response"""

    def __init__(self, *, ref_count: int = 0, **kwargs):
        self.ref_count = ref_count

    def to_dict(self) -> dict:
        return {"ref_count": self.ref_count}

    @classmethod
    def parse(cls, f):
        """Parse a serialized response metadata, absorbing corruption errors"""
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
        return cls(**data)

    @classmethod
    @contextlib.contextmanager
    def parsed_write(cls, transaction):
        """Wrapper to expose a serialized request in a WriteTransaction as a
        full CachedResponseMeta object. Changes will be preserved if there are
        no exceptions raised in the body of the context."""
        with transaction as (old_f, new_f):
            parsed = cls.parse(old_f) if old_f is not None else cls()
            yield parsed
            json.dump(parsed.to_dict(), new_f)


def _file_sha256(data_f: io.BufferedIOBase) -> bytes:
    """Calculate the SHA256 of the given seekable file-like object"""
    sha256 = hashlib.sha256()
    data_f.seek(0)
    while True:
        block = data_f.read(1024 * 1024 * 1024)  # 1 MB block size
        if not block:
            break
        sha256.update(block)
    return sha256.digest()

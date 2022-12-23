# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import email.message
import hashlib
import io
import json
import typing as T
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

import spack.util.network_cache as nc

# Digest of an empty SHA256sum
empty_sha256 = bytes.fromhex("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

# Another SHA256-like digest
fake_sha256 = bytes.fromhex("7f43b62daff2aae5970369bab08eab9cc981c9f4ee961ac399854d9ced6d7301")


@contextlib.contextmanager
def nullcontext(value):
    yield value


class ExampleHandler(T.MutableMapping[str, bytes], urllib.request.BaseHandler):
    """urllib handler for example:// URLs. Acts a lot like HTTP, but the
    storage for the served "files" is accessible via a dict-like interface.

    Details such as ETags, Date/Last-Modified and so on are handled automatically.
    """

    def __init__(
        self, initial_files: T.Optional[T.Dict[str, bytes]] = None, *, http_codes: bool, etag: bool
    ):
        self.http_codes = http_codes
        self.etag = etag
        self._files: T.Dict[str, dict] = {}
        self._network_log: T.List[T.Tuple[str, int]] = []
        if initial_files is not None:
            for path, data in initial_files.items():
                self[path] = data

    def example_open(self, request: urllib.request.Request):
        """Derive a urlopen handler with the given features en/disabled."""
        headers = email.message.EmailMessage()

        parsed_url = urllib.parse.urlparse(request.full_url)
        f = self._files.get(parsed_url.path)
        if f is None or "contents" not in f:
            # 404 Not found
            code = (f or {}).get("code", 404)
            self._network_log.append((parsed_url.path, code))
            if code == 0:
                # Special case: raise a URLError instead
                raise urllib.error.URLError("Code 0!")
            if not self.http_codes:
                # Presumably, failure to fetch is an error if codes are not returned
                raise urllib.error.URLError(f"example://{parsed_url.path} not found!")
            return urllib.response.addinfourl(io.BytesIO(), headers, request.full_url, code)

        if self.etag:
            headers["ETag"] = f'"{f["revnum"]:d}"'
            if request.headers.get("If-none-match") == headers["etag"]:
                # 304 Not Modified
                self._network_log.append((parsed_url.path, 304))
                return urllib.response.addinfourl(
                    io.BytesIO(), headers, request.full_url, 304 if self.http_codes else None
                )

        # 200 OK
        self._network_log.append((parsed_url.path, 200))
        return urllib.response.addinfourl(
            io.BytesIO(f["contents"]), headers, request.full_url, 200 if self.http_codes else None
        )

    @property
    def network_log(self) -> T.List[T.Tuple[str, int]]:
        log = self._network_log
        self._network_log = []
        return log

    def set_error(self, path: str, code: int) -> None:
        assert code == 0 or 400 <= code < 500
        self._files[path] = {"code": code}

    def __setitem__(self, path: str, content: bytes) -> None:
        f = self._files.setdefault(path, {})
        f["contents"] = content
        f["revnum"] = f.get("revnum", 0) + 1

    def __getitem__(self, path: str) -> bytes:
        return self._files[path]["contents"]

    def __delitem__(self, path: str) -> None:
        del self._files[path]

    def __len__(self) -> int:
        return len(self._files)

    def __iter__(self) -> T.Iterator[str]:
        return iter(self._files)


class ExampleErrorProcessor(urllib.request.BaseHandler):
    """Process example:// error codes as if they were HTTP"""

    handler_order = 1000  # after all other processing

    def example_response(self, request, response):
        code, hdrs = response.code, response.info()

        # HTTP codes outside of 2xx are not successful. Re-raise them as HTTP errors.
        if not (200 <= code < 300):
            response = self.parent.error("http", request, response, code, "Error!", hdrs)

        return response


def test_responsemeta_sanity():
    "Test that CachedResponseMeta performs basic sanitization on creation"

    # Values should be preserved in attributes and dictification
    r = nc.CachedResponseMeta(ref_count=12, foo="bar")
    assert r.ref_count == 12
    assert not hasattr(r, "foo")
    assert r.to_dict() == {"ref_count": r.ref_count}


def test_responsemeta_json():
    "Test that CachedResponseMeta implements appropriate JSON methods"

    # JSON load failures should be absorbed transparently
    assert (
        nc.CachedResponseMeta.parse(io.StringIO("not json")).to_dict()
        == nc.CachedResponseMeta().to_dict()
    )

    # Transactions write after the context is complete
    file = io.StringIO("prior")
    with nc.CachedResponseMeta.parsed_write(nullcontext((None, file))) as r:
        r.ref_count = 4
        assert file.getvalue() == "prior"
    assert json.loads(file.getvalue()) == {"ref_count": 4}

    # Transactions do not write if the context raises an exception
    file = io.StringIO("prior")
    with pytest.raises(RuntimeError, match="^foobar$"):
        with nc.CachedResponseMeta.parsed_write(nullcontext((None, file))) as r:
            r.ref_count = 4
            raise RuntimeError("foobar")
    assert file.getvalue() == "prior"


def test_request_sanity():
    "Test that CachedRequest implements basic sanitization on creation"

    # Values should be preserved in attributes and dictification
    r = nc.CachedRequest(data_sha256=empty_sha256.hex(), etag="foobar-12", foo="bar")
    assert r.data_sha256 == empty_sha256
    assert r.etag == "foobar-12"
    assert not hasattr(r, "foo")
    assert r.to_dict() == {"data_sha256": r.data_sha256.hex(), "etag": r.etag}

    # Data keys should be present with a valid SHA256
    assert r.data_key is not None
    assert r.metadata_key is not None

    # Bad SHA256 values should be elided
    r = nc.CachedRequest(data_sha256=b"foobar")
    assert r.data_sha256 is None
    assert r.data_key is None
    assert r.metadata_key is None


def test_request_json():
    "Test that CachedRequest implements appropriate JSON methods"

    # JSON load failures should be absorbed transparently
    assert (
        nc.CachedRequest.parse(io.StringIO("not json")).to_dict() == nc.CachedRequest().to_dict()
    )

    # Transactions write after the context is complete
    file = io.StringIO("prior")
    with nc.CachedRequest.parsed_write(nullcontext((None, file))) as r:
        r.etag = "foobar-12"
        assert file.getvalue() == "prior"
    assert json.loads(file.getvalue()) == {"etag": "foobar-12"}

    # Transactions do not write if the context raises an exception
    file = io.StringIO("prior")
    with pytest.raises(RuntimeError, match="^foobar$"):
        with nc.CachedRequest.parsed_write(nullcontext((None, file))) as r:
            r.etag = "foobar-12"
            raise RuntimeError("foobar")
    assert file.getvalue() == "prior"


def test_request_pre_fetch():
    "Test that CachedRequest.needs_fetch reacts to its contained state appropiately"

    def never_hash():
        raise AssertionError

    # An empty request always needs to fetch unconditionally
    assert nc.CachedRequest().needs_fetch(sha256_fetch_fn=never_hash) == {}

    # A request with a hash should fetch the hash, or unconditionally fetch
    r = nc.CachedRequest(data_sha256=empty_sha256)
    assert r.needs_fetch(sha256_fetch_fn=lambda: empty_sha256) is None
    assert r.needs_fetch(sha256_fetch_fn=lambda: fake_sha256) == {}
    assert r.needs_fetch() == {}

    # A request with an Etag should prefer conditional fetch over hash
    r = nc.CachedRequest(etag="foobar-12")
    assert r.needs_fetch(sha256_fetch_fn=never_hash) == {"If-None-Match": '"foobar-12"'}
    r.data_sha256 = empty_sha256
    assert r.needs_fetch(sha256_fetch_fn=never_hash) == {"If-None-Match": '"foobar-12"'}


def test_request_post_fetch():
    "Test that CachedRequest.fetched() and mark_fresh() alter the contained state"

    # Calling fetched() should update the hash and etag (when available)
    r = nc.CachedRequest(etag="prior", data_sha256=fake_sha256)
    r.fetched({"etag": '"foobar-12"'}, io.BytesIO())
    assert r.etag == "foobar-12"
    assert r.data_sha256 == empty_sha256
    r.fetched({}, io.BytesIO(b"something else"))
    assert r.etag is None
    assert r.data_sha256 != empty_sha256

    # Calling mark_fresh() should (currently) do nothing, for future implementation
    before = r.to_dict()
    r.mark_fresh({"etag": '"foobar-13"'})
    assert r.to_dict() == before


def test_cache_local_noop(tmpdir, monkeypatch):
    "Test that fetch() no-ops (i.e. does not cache) local files"

    xfile = tmpdir.join("foo.txt").strpath
    with open(xfile, "w") as f:
        f.write("foobar")

    def fake_refresh(*args, **kwargs):
        raise AssertionError

    monkeypatch.setattr(nc.NetworkCache, "_refresh", fake_refresh)

    # Ensure file:// scheme URLs go straight to the filesystem, without caching
    c = nc.NetworkCache(tmpdir.join("cache").strpath)
    with c.fetch("file:" + xfile) as (file, path, _):
        assert file.read() == b"foobar"
        assert path == Path(xfile)

    # Ensure missing files raise a FetchError instead of anything more specific
    with pytest.raises(nc.FetchError):
        with c.fetch("file:/does/not/exist"):
            assert False, "unreachable"


def test_cache_dry_run(tmpdir, monkeypatch):
    "Test that dry_run works properly"

    xs = ExampleHandler(http_codes=True, etag=True)
    xs["/data.txt"] = b"data"
    monkeypatch.setattr(nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs).open)
    c = nc.NetworkCache(tmpdir.strpath)

    # dry_run with a brand new request gives None
    with c.fetch("example:/data.txt", dry_run=True) as r:
        assert r is None
    assert xs.network_log == []

    # dry_run with a cached request returns the cached request as it should
    with c.fetch("example:/data.txt") as r:
        assert r.file.read() == b"data"
    assert xs.network_log != []
    xs["/data.txt"] = b"new data"
    with c.fetch("example:/data.txt", dry_run=True) as r:
        assert r.file.read() == b"data"
    assert xs.network_log == []


def test_cache_cleanup(tmpdir, monkeypatch):
    "Test that destroy() nukes the entire cache"

    xs = ExampleHandler(http_codes=True, etag=True)
    xs["/data.txt"] = b"data"
    monkeypatch.setattr(nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs).open)
    c = nc.NetworkCache(tmpdir.strpath)

    with c.fetch("example:/data.txt"):
        pass
    assert len(list(Path(tmpdir).glob("**/*"))) > 0

    c.destroy()
    assert len(list(Path(tmpdir).glob("**/*"))) == 0


@pytest.mark.parametrize("http_codes", [True, False])
def test_cache_fetch_uncachable(tmpdir, monkeypatch, http_codes):
    "Test that fetch() will always fetch if the cache cannot be validated"

    xs = ExampleHandler(http_codes=http_codes, etag=False)
    xs["/data.txt"] = b"version 1"
    monkeypatch.setattr(nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs).open)
    c = nc.NetworkCache(tmpdir.strpath)

    # Every fetch should cause a real request, stored in the same cache key
    with c.fetch("example:/data.txt") as (file, cached_path, cached_rev):
        assert file.read() == b"version 1"
    with c.fetch("example:/data.txt") as (file, path, rev):
        assert file.read() == b"version 1"
        assert path == cached_path
        assert rev == cached_rev
    assert xs.network_log == [("/data.txt", 200)] * 2


@pytest.mark.parametrize(
    "http_codes,extra_handlers", [(True, []), (True, [ExampleErrorProcessor()]), (False, [])]
)
def test_cache_fetch_hashfile(tmpdir, monkeypatch, http_codes, extra_handlers):
    "Test that fetch() can use fetches of hashfiles to maintain the cache"

    xs = ExampleHandler(http_codes=http_codes, etag=False)
    xs["/data.txt"] = b"version 1"
    xs["/data.txt.hash"] = hashlib.sha256(xs["/data.txt"]).hexdigest().encode("utf-8")
    monkeypatch.setattr(
        nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs, *extra_handlers).open
    )
    c = nc.NetworkCache(tmpdir.strpath)

    # First fetch should cause a real request
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (
        file,
        cached_path,
        cached_rev,
    ):
        assert file.read() == b"version 1"
    assert xs.network_log == [("/data.txt", 200)]

    # Second fetch should fetch the hashfile and succeed
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (file, path, rev):
        assert file.read() == b"version 1"
        assert path == cached_path
        assert rev == cached_rev
    assert xs.network_log == [("/data.txt.hash", 200)]

    # Fetching before the hash updates should remain out-of-date
    xs["/data.txt"] = b"version 2"
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (file, path, rev):
        assert file.read() == b"version 1"
        assert path == cached_path
        assert rev == cached_rev
    assert xs.network_log == [("/data.txt.hash", 200)]

    # Fetching once the hash updates should sync back up
    xs["/data.txt.hash"] = hashlib.sha256(xs["/data.txt"]).hexdigest().encode("utf-8")
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (file, path, rev):
        assert file.read() == b"version 2"
        assert path != cached_path
        assert rev != cached_rev
        cached_path, cached_rev = path, rev
    assert xs.network_log == [("/data.txt.hash", 200), ("/data.txt", 200)]

    # Cache should re-fetch if the hash changes, even erroneously:
    # it trusts the content's hash over whatever the hashfile contains
    xs["/data.txt.hash"] = fake_sha256.hex().encode("utf-8")
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (file, path, rev):
        assert file.read() == b"version 2"
        assert path == cached_path
        assert rev == cached_rev
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (file, path, rev):
        assert file.read() == b"version 2"
        assert path == cached_path
        assert rev == cached_rev
    assert xs.network_log == [("/data.txt.hash", 200), ("/data.txt", 200)] * 2

    # If the remote hashfile is corrupt an error should be raised
    xs["/data.txt.hash"] = b"not a hash"
    with pytest.raises(nc.SpackWebError, match=r"example:/data\.txt\.hash"):
        with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash"):
            assert False, "unreachable"
    xs["/data.txt.hash"] = b"deadbeef"
    with pytest.raises(nc.SpackWebError, match=r"example:/data\.txt\.hash"):
        with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash"):
            assert False, "unreachable"
    assert xs.network_log == [("/data.txt.hash", 200)] * 2

    # But the remote hashfile not existing at all is OK
    del xs["/data.txt.hash"]
    with c.fetch("example:/data.txt", sha256_url="example:/data.txt.hash") as (file, path, rev):
        assert file.read() == b"version 2"
        assert path == cached_path
        assert rev == cached_rev
    assert xs.network_log == [("/data.txt.hash", 404), ("/data.txt", 200)]


@pytest.mark.parametrize(
    "http_codes,extra_handlers", [(True, []), (True, [ExampleErrorProcessor()]), (False, [])]
)
def test_cache_fetch_etag(tmpdir, monkeypatch, http_codes, extra_handlers):
    "Test that fetch() can use etags and conditional fetches to maintain the cache"

    xs = ExampleHandler(http_codes=http_codes, etag=True)
    xs["/data.txt"] = b"version 1"
    monkeypatch.setattr(
        nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs, *extra_handlers).open
    )
    c = nc.NetworkCache(tmpdir.strpath)

    # First fetch should cause a real request
    with c.fetch("example:/data.txt") as (file, cached_path, cached_rev):
        assert file.read() == b"version 1"
    assert xs.network_log == [("/data.txt", 200)]

    # Second fetch should cause a validation request
    with c.fetch("example:/data.txt") as (file, path, rev):
        assert file.read() == b"version 1"
        assert path == cached_path
        assert rev == cached_rev
    assert xs.network_log == [("/data.txt", 304)]

    # First fetch after update should cause a conditional request
    xs["/data.txt"] = b"version 2"
    with c.fetch("example:/data.txt") as (file, path, rev):
        assert file.read() == b"version 2"
        assert path != cached_path
        assert rev != cached_rev
    assert xs.network_log == [("/data.txt", 200)]


@pytest.mark.parametrize(
    "http_codes,extra_handlers", [(True, []), (True, [ExampleErrorProcessor()]), (False, [])]
)
def test_cache_fetch_errors(tmpdir, monkeypatch, http_codes, extra_handlers):
    "Test that network errors get exposed as FetchErrors in the end"

    xs = ExampleHandler(http_codes=http_codes, etag=True)
    xs.set_error("/403.txt", 403)
    xs.set_error("/0.txt", 0)
    monkeypatch.setattr(
        nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs, *extra_handlers).open
    )
    c = nc.NetworkCache(tmpdir.strpath)

    # Errors, such as 404 or 403 or so, should be exposed as FetchErrors
    with pytest.raises(nc.FetchError, match=r"404"):
        with c.fetch("example:/404.txt"):
            assert False, "unreachable"
    with pytest.raises(nc.FetchError, match=r"403"):
        with c.fetch("example:/403.txt"):
            assert False, "unreachable"
    with pytest.raises(nc.FetchError, match=r"Code 0"):
        with c.fetch("example:/0.txt"):
            assert False, "unreachable"


def test_cache_shared_content(tmpdir, monkeypatch):
    "Test that 2 cached URLs can share the same content cache key"

    xs = ExampleHandler(http_codes=True, etag=True)
    xs["/data1.txt"] = b""
    xs["/data2.txt"] = b""
    monkeypatch.setattr(nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs).open)
    c = nc.NetworkCache(tmpdir.strpath)

    # First fetch should save the content in the cache, ref_count of 1
    with c.fetch("example:/data1.txt") as r:
        assert r.file.read() == b""
    meta_path = Path(c._cache.cache_path(nc.CachedRequest(data_sha256=empty_sha256).metadata_key))
    assert meta_path.is_file()
    with open(meta_path, "r") as f:
        assert nc.CachedResponseMeta.parse(f).ref_count == 1

    # Second fetch should share the content, ref_count bumps to 2
    with c.fetch("example:/data2.txt") as r:
        assert r.file.read() == b""
    with open(meta_path, "r") as f:
        assert nc.CachedResponseMeta.parse(f).ref_count == 2

    # After one URL updates, the next fetch should move off the shared content key
    xs["/data1.txt"] = b"data 1"
    with c.fetch("example:/data1.txt") as r:
        assert r.file.read() == b"data 1"
    with open(meta_path, "r") as f:
        assert nc.CachedResponseMeta.parse(f).ref_count == 1

    # After all URLs update, the shared content key should be deleted
    xs["/data2.txt"] = b"data 2"
    with c.fetch("example:/data2.txt") as r:
        assert r.file.read() == b"data 2"
    assert not meta_path.exists()


def test_cache_corruption(tmpdir, monkeypatch):
    "Test that corruption in the data will raise an error"

    xs = ExampleHandler(http_codes=True, etag=True)
    xs["/data.txt"] = b""
    monkeypatch.setattr(nc.NetworkCache, "_urlopen", urllib.request.build_opener(xs).open)
    c = nc.NetworkCache(tmpdir.strpath)

    with c.fetch("example:/data.txt") as r:
        assert r.file.read() == b""

    # Altering the cached data should cause an error
    assert r.path.is_file()
    with open(r.path, "w") as f:
        f.write("CORRUPTION!")

    with pytest.raises(nc.CacheError, match=r"example:/data\.txt"):
        with c.fetch("example:/data.txt"):
            assert False, "unreachable"

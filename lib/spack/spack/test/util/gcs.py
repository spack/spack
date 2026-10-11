# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import sys
import types
import urllib.error
import urllib.request

import pytest

import spack.util.gcs as gcs


@pytest.fixture
def fake_google_api_core(monkeypatch):
    """Stand in for google.api_core.exceptions.GoogleAPIError."""

    class GoogleAPIError(Exception):
        pass

    api_core_exceptions = types.ModuleType("google.api_core.exceptions")
    api_core_exceptions.GoogleAPIError = GoogleAPIError
    api_core = types.ModuleType("google.api_core")
    api_core.exceptions = api_core_exceptions
    google_pkg = types.ModuleType("google")
    google_pkg.api_core = api_core

    monkeypatch.setitem(sys.modules, "google", google_pkg)
    monkeypatch.setitem(sys.modules, "google.api_core", api_core)
    monkeypatch.setitem(sys.modules, "google.api_core.exceptions", api_core_exceptions)

    return GoogleAPIError


def test_gcs_open_wraps_google_api_error(monkeypatch, fake_google_api_core):
    """Verify that gcs_open catches GoogleAPIError and re-raises it as URLError."""

    class BoomBlob:
        def __init__(self, url):
            pass

        def exists(self):
            raise fake_google_api_core("permission denied")

    monkeypatch.setattr(gcs, "GCSBlob", BoomBlob)

    req = urllib.request.Request("gs://my-bucket/my-file")

    with pytest.raises(urllib.error.URLError):
        gcs.gcs_open(req)


def test_gcs_open_returns_response_for_existing_blob(monkeypatch, fake_google_api_core):
    """Verify success path: an existing blob gets returned as an addinfourl
    wrapping its byte stream and headers."""

    class ExistingBlob:
        def __init__(self, url):
            pass

        def exists(self):
            return True

        def get_blob_byte_stream(self):
            return io.BytesIO(b"the-data")

        def get_blob_headers(self):
            return {"Content-type": "text/plain"}

    monkeypatch.setattr(gcs, "GCSBlob", ExistingBlob)

    req = urllib.request.Request("gs://my-bucket/my-file")
    response = gcs.gcs_open(req)

    assert response.fp.read() == b"the-data"
    assert response.headers == {"Content-type": "text/plain"}


def test_gcs_open_raises_url_error_for_missing_blob(monkeypatch, fake_google_api_core):
    """Verify that gcs_open raises URLError for "blob does not exist"."""

    class MissingBlob:
        def __init__(self, url):
            self.blob_path = "my-file"

        def exists(self):
            return False

    monkeypatch.setattr(gcs, "GCSBlob", MissingBlob)

    req = urllib.request.Request("gs://my-bucket/my-file")

    with pytest.raises(urllib.error.URLError):
        gcs.gcs_open(req)

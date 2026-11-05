# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import urllib.error
import urllib.request

import pytest

import spack.util.gcs as gcs
from spack.test.web import MockGCSBucket, mock_gcs_client  # noqa


@pytest.fixture
def fake_google_api_error(monkeypatch, mock_gcs_client):
    """Stand in for google.api_core.exceptions.GoogleAPIError, raised by bucket.get_blob."""

    class GoogleAPIError(Exception):
        pass

    def get_blob(self, blob_path):
        raise GoogleAPIError("permission denied")

    mock_gcs_client.GoogleAPIError = GoogleAPIError
    monkeypatch.setattr(MockGCSBucket, "get_blob", get_blob)

    return GoogleAPIError


def test_gcs_open_wraps_google_api_error(fake_google_api_error):
    """Verify that gcs_open catches GoogleAPIError and re-raises it as URLError."""
    req = urllib.request.Request("gs://my-bucket/subdirectory/my-file")

    with pytest.raises(urllib.error.URLError) as e:
        gcs.gcs_open(req)
    assert not isinstance(e.value, urllib.error.HTTPError)
    assert isinstance(e.value.__cause__, fake_google_api_error)


def test_gcs_open_returns_response_for_existing_blob(mock_gcs_client):
    """Verify success path: an existing blob gets returned as an addinfourl
    wrapping its byte stream and headers."""
    req = urllib.request.Request("gs://my-bucket/subdirectory/my-file")
    response = gcs.gcs_open(req)

    assert response.fp.read() == b"stream of bytes"
    assert response.headers["Content-type"] == "application/octet-stream"


def test_gcs_open_raises_http_404_for_missing_blob(mock_gcs_client):
    """Verify that gcs_open raises a 404 HTTPError for "blob does not exist"."""
    req = urllib.request.Request("gs://my-bucket/subdirectory/my-notfound-file")

    with pytest.raises(urllib.error.HTTPError) as e:
        gcs.gcs_open(req)
    assert e.value.code == 404

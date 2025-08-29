# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import pathlib
from typing import List

import pytest

import spack.paths
import spack.util.download
import spack.util.web


class MockProcess:
    def __init__(self, stream, return_code: int):
        self.stream = stream
        self.returncode = return_code

    @property
    def stdout(self):
        return self.stream


@pytest.fixture()
def curl_process(monkeypatch):
    def _mock_curl_process(input_file: str, return_code: int = 0):

        data_dir = pathlib.Path(spack.paths.test_path) / "data" / "curl"
        filename = data_dir / input_file

        @contextlib.contextmanager
        def _mock(curl_cmd: List[str]):
            with filename.open("rb") as f:
                yield MockProcess(f, return_code=return_code)

        monkeypatch.setattr(spack.util.download, "_start_curl_process", _mock)

    return _mock_curl_process


def test_curl_redirection(curl_process):
    """Tests that the curl stream redirects to the final URL."""
    curl_process("curl_redirection.out", return_code=0)

    with spack.util.download.curl_stream(url="https://example.com/data", timeout=1) as stream:
        assert stream.url == "https://example.com/data"
        assert stream.geturl() == "https://archive.mesa3d.org/glu/glu-9.0.0.tar.gz"
        assert stream.headers["Content-Type"] == "application/x-gzip"


def test_curl_resource_not_found(curl_process):
    """Tests that the curl stream raises on a 404 status."""
    curl_process("curl_resource_not_found.out", return_code=0)

    with pytest.raises(spack.util.web.DetailedHTTPError):
        with spack.util.download.curl_stream(url="https://example.com/data", timeout=1):
            pass


@pytest.mark.parametrize(
    "url",
    [
        "file:///opt/spack/somefile.tar.gz",
        "ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.2.3.2.tar.bz2",
    ],
)
def test_curl_option_file_and_ftp(url):
    """Tests that we don't print headers for file:// and ftp:// URLs."""
    curl_base_option = spack.util.web.base_curl_fetch_args(url, timeout=0)
    assert "-D" not in curl_base_option
    assert "-i" not in curl_base_option
    assert "-I" not in curl_base_option

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.url
from spack.main import SpackCommand
from spack.version import Version

versions = SpackCommand("versions")


pytestmark = [pytest.mark.usefixtures("mock_packages")]


def _mock_find_versions_of_archive(*args, **kwargs):
    return {
        Version("1.3.1"): "https://zlib.net/zlib-1.3.1.tar.gz",
        Version("1.3"): "https://zlib.net/zlib-1.3.tar.gz",
        Version("1.2.13"): "https://zlib.net/zlib-1.2.13.tar.gz",
    }


def test_safe_versions():
    """Only test the safe versions of a package."""
    assert versions("--safe", "zlib") == "  1.2.11\n  1.2.8\n  1.2.3\n"


def test_remote_versions(monkeypatch):
    """Test a package for which remote versions should be available."""
    monkeypatch.setattr(spack.url, "find_versions_of_archive", _mock_find_versions_of_archive)
    assert versions("zlib") == "  1.2.11\n  1.2.8\n  1.2.3\n  1.3.1\n  1.3\n  1.2.13\n"


def test_remote_versions_only(monkeypatch):
    """Test a package for which remote versions should be available."""
    monkeypatch.setattr(spack.url, "find_versions_of_archive", _mock_find_versions_of_archive)
    assert versions("--remote", "zlib") == "  1.3.1\n  1.3\n  1.2.13\n"


def test_new_versions_only(monkeypatch):
    """Test a package for which new versions should be available."""
    from spack_repo.builtin_mock.packages.brillig.package import Brillig  # type: ignore[import]

    def mock_fetch_remote_versions(*args, **kwargs):
        mock_remote_versions = {
            # new version, we expect this to be in output:
            Version("99.99.99"): {},
            # some packages use '3.2' equivalently to '3.2.0'
            # thus '3.2.1' is considered to be a new version
            # and expected in the output also
            Version("3.2.1"): {},  # new version, we expect this to be in output
            Version("3.2"): {},
            Version("1.0.0"): {},
        }
        return mock_remote_versions

    mock_versions = {
        # already checksummed versions:
        Version("3.2"): {},
        Version("1.0.0"): {},
    }
    monkeypatch.setattr(Brillig, "versions", mock_versions)
    monkeypatch.setattr(Brillig, "fetch_remote_versions", mock_fetch_remote_versions)
    v = versions("--new", "brillig")
    assert v.strip(" \n\t") == "99.99.99\n  3.2.1"


def test_no_unchecksummed_versions(monkeypatch):
    """Test a package for which no unchecksummed versions are available."""

    def mock_find_versions_of_archive(*args, **kwargs):
        """Mock find_versions_of_archive to avoid network calls."""
        # Return some fake versions for bzip2
        return {
            Version("1.0.8"): "https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz",
            Version("1.0.7"): "https://sourceware.org/pub/bzip2/bzip2-1.0.7.tar.gz",
        }

    monkeypatch.setattr(spack.url, "find_versions_of_archive", mock_find_versions_of_archive)

    versions("bzip2")


def test_versions_no_url():
    """Test a package with versions but without a ``url`` attribute."""
    assert versions("attributes-foo-app") == "  1.0\n"


def test_no_versions_no_url():
    """Test a package without versions or a ``url`` attribute."""
    assert versions("no-url-or-version") == ""

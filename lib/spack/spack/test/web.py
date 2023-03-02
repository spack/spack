# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os
import sys

import pytest

import llnl.util.tty as tty

import spack.config
import spack.mirror
import spack.paths
import spack.util.s3
import spack.util.url as url_util
import spack.util.web
from spack.version import ver


def _create_url(relative_url):
    web_data_path = os.path.join(spack.paths.test_path, "data", "web")
    return url_util.path_to_file_url(os.path.join(web_data_path, relative_url))


root = _create_url("index.html")
root_tarball = _create_url("foo-0.0.0.tar.gz")
page_1 = _create_url("1.html")
page_2 = _create_url("2.html")
page_3 = _create_url("3.html")
page_4 = _create_url("4.html")


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
@pytest.mark.parametrize(
    "depth,expected_found,expected_not_found,expected_text",
    [
        (
            0,
            {"pages": [root], "links": [page_1]},
            {"pages": [page_1, page_2, page_3, page_4], "links": [root, page_2, page_3, page_4]},
            {root: "This is the root page."},
        ),
        (
            1,
            {"pages": [root, page_1], "links": [page_1, page_2]},
            {"pages": [page_2, page_3, page_4], "links": [root, page_3, page_4]},
            {root: "This is the root page.", page_1: "This is page 1."},
        ),
        (
            2,
            {"pages": [root, page_1, page_2], "links": [page_1, page_2, page_3, page_4]},
            {"pages": [page_3, page_4], "links": [root]},
            {root: "This is the root page.", page_1: "This is page 1.", page_2: "This is page 2."},
        ),
        (
            3,
            {
                "pages": [root, page_1, page_2, page_3, page_4],
                "links": [root, page_1, page_2, page_3, page_4],
            },
            {"pages": [], "links": []},
            {
                root: "This is the root page.",
                page_1: "This is page 1.",
                page_2: "This is page 2.",
                page_3: "This is page 3.",
                page_4: "This is page 4.",
            },
        ),
    ],
)
def test_spider(depth, expected_found, expected_not_found, expected_text):
    pages, links = spack.util.web.spider(root, depth=depth)

    for page in expected_found["pages"]:
        assert page in pages

    for page in expected_not_found["pages"]:
        assert page not in pages

    for link in expected_found["links"]:
        assert link in links

    for link in expected_not_found["links"]:
        assert link not in links

    for page, text in expected_text.items():
        assert text in pages[page]


def test_spider_no_response(monkeypatch):
    # Mock the absence of a response
    monkeypatch.setattr(spack.util.web, "read_from_url", lambda x, y: (None, None, None))
    pages, links = spack.util.web.spider(root, depth=0)
    assert not pages and not links


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_find_versions_of_archive_0():
    versions = spack.util.web.find_versions_of_archive(root_tarball, root, list_depth=0)
    assert ver("0.0.0") in versions


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_find_versions_of_archive_1():
    versions = spack.util.web.find_versions_of_archive(root_tarball, root, list_depth=1)
    assert ver("0.0.0") in versions
    assert ver("1.0.0") in versions


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_find_versions_of_archive_2():
    versions = spack.util.web.find_versions_of_archive(root_tarball, root, list_depth=2)
    assert ver("0.0.0") in versions
    assert ver("1.0.0") in versions
    assert ver("2.0.0") in versions


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_find_exotic_versions_of_archive_2():
    versions = spack.util.web.find_versions_of_archive(root_tarball, root, list_depth=2)
    # up for grabs to make this better.
    assert ver("2.0.0b2") in versions


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_find_versions_of_archive_3():
    versions = spack.util.web.find_versions_of_archive(root_tarball, root, list_depth=3)
    assert ver("0.0.0") in versions
    assert ver("1.0.0") in versions
    assert ver("2.0.0") in versions
    assert ver("3.0") in versions
    assert ver("4.5") in versions


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_find_exotic_versions_of_archive_3():
    versions = spack.util.web.find_versions_of_archive(root_tarball, root, list_depth=3)
    assert ver("2.0.0b2") in versions
    assert ver("3.0a1") in versions
    assert ver("4.5-rc5") in versions


def test_get_header():
    headers = {"Content-type": "text/plain"}

    # looking up headers should just work like a plain dict
    # lookup when there is an entry with the right key
    assert spack.util.web.get_header(headers, "Content-type") == "text/plain"

    # looking up headers should still work if there is a fuzzy match
    assert spack.util.web.get_header(headers, "contentType") == "text/plain"

    # ...unless there is an exact match for the "fuzzy" spelling.
    headers["contentType"] = "text/html"
    assert spack.util.web.get_header(headers, "contentType") == "text/html"

    # If lookup has to fallback to fuzzy matching and there are more than one
    # fuzzy match, the result depends on the internal ordering of the given
    # mapping
    headers = collections.OrderedDict()
    headers["Content-type"] = "text/plain"
    headers["contentType"] = "text/html"

    assert spack.util.web.get_header(headers, "CONTENT_TYPE") == "text/plain"
    del headers["Content-type"]
    assert spack.util.web.get_header(headers, "CONTENT_TYPE") == "text/html"

    # Same as above, but different ordering
    headers = collections.OrderedDict()
    headers["contentType"] = "text/html"
    headers["Content-type"] = "text/plain"

    assert spack.util.web.get_header(headers, "CONTENT_TYPE") == "text/html"
    del headers["contentType"]
    assert spack.util.web.get_header(headers, "CONTENT_TYPE") == "text/plain"

    # If there isn't even a fuzzy match, raise KeyError
    with pytest.raises(KeyError):
        spack.util.web.get_header(headers, "ContentLength")


def test_etag_parser():
    # This follows rfc7232 to some extent, relaxing the quote requirement.
    assert spack.util.web.parse_etag('"abcdef"') == "abcdef"
    assert spack.util.web.parse_etag("abcdef") == "abcdef"

    # No empty tags
    assert spack.util.web.parse_etag("") is None

    # No quotes or spaces allowed
    assert spack.util.web.parse_etag('"abcdef"ghi"') is None
    assert spack.util.web.parse_etag('"abc def"') is None
    assert spack.util.web.parse_etag("abc def") is None


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_list_url(tmpdir):
    testpath = str(tmpdir)
    testpath_url = url_util.path_to_file_url(testpath)

    os.mkdir(os.path.join(testpath, "dir"))

    with open(os.path.join(testpath, "file-0.txt"), "w"):
        pass
    with open(os.path.join(testpath, "file-1.txt"), "w"):
        pass
    with open(os.path.join(testpath, "file-2.txt"), "w"):
        pass

    with open(os.path.join(testpath, "dir", "another-file.txt"), "w"):
        pass

    list_url = lambda recursive: list(
        sorted(spack.util.web.list_url(testpath_url, recursive=recursive))
    )

    assert list_url(False) == ["file-0.txt", "file-1.txt", "file-2.txt"]

    assert list_url(True) == ["dir/another-file.txt", "file-0.txt", "file-1.txt", "file-2.txt"]


class MockPages(object):
    def search(self, *args, **kwargs):
        return [{"Key": "keyone"}, {"Key": "keytwo"}, {"Key": "keythree"}]


class MockPaginator(object):
    def paginate(self, *args, **kwargs):
        return MockPages()


class MockClientError(Exception):
    def __init__(self):
        self.response = {
            "Error": {"Code": "NoSuchKey"},
            "ResponseMetadata": {"HTTPStatusCode": 404},
        }


class MockS3Client(object):
    def get_paginator(self, *args, **kwargs):
        return MockPaginator()

    def delete_objects(self, *args, **kwargs):
        return {
            "Errors": [{"Key": "keyone", "Message": "Access Denied"}],
            "Deleted": [{"Key": "keytwo"}, {"Key": "keythree"}],
        }

    def delete_object(self, *args, **kwargs):
        pass

    def get_object(self, Bucket=None, Key=None):
        self.ClientError = MockClientError
        if Bucket == "my-bucket" and Key == "subdirectory/my-file":
            return {"ResponseMetadata": {"HTTPHeaders": {}}}
        raise self.ClientError

    def head_object(self, Bucket=None, Key=None):
        self.ClientError = MockClientError
        if Bucket == "my-bucket" and Key == "subdirectory/my-file":
            return {"ResponseMetadata": {"HTTPHeaders": {}}}
        raise self.ClientError


def test_gather_s3_information(monkeypatch, capfd):
    mirror = spack.mirror.Mirror.from_dict(
        {
            "fetch": {
                "access_token": "AAAAAAA",
                "profile": "SPacKDeV",
                "access_pair": ("SPA", "CK"),
                "endpoint_url": "https://127.0.0.1:8888",
            },
            "push": {
                "access_token": "AAAAAAA",
                "profile": "SPacKDeV",
                "access_pair": ("SPA", "CK"),
                "endpoint_url": "https://127.0.0.1:8888",
            },
        }
    )

    session_args, client_args = spack.util.s3.get_mirror_s3_connection_info(mirror, "push")

    # Session args are used to create the S3 Session object
    assert "aws_session_token" in session_args
    assert session_args.get("aws_session_token") == "AAAAAAA"
    assert "aws_access_key_id" in session_args
    assert session_args.get("aws_access_key_id") == "SPA"
    assert "aws_secret_access_key" in session_args
    assert session_args.get("aws_secret_access_key") == "CK"
    assert "profile_name" in session_args
    assert session_args.get("profile_name") == "SPacKDeV"

    # In addition to the session object, use the client_args to create the s3
    # Client object
    assert "endpoint_url" in client_args


def test_remove_s3_url(monkeypatch, capfd):
    fake_s3_url = "s3://my-bucket/subdirectory/mirror"

    def get_s3_session(url, method="fetch"):
        return MockS3Client()

    monkeypatch.setattr(spack.util.s3, "get_s3_session", get_s3_session)

    current_debug_level = tty.debug_level()
    tty.set_debug(1)

    spack.util.web.remove_url(fake_s3_url, recursive=True)
    err = capfd.readouterr()[1]

    tty.set_debug(current_debug_level)

    assert "Failed to delete keyone (Access Denied)" in err
    assert "Deleted keythree" in err
    assert "Deleted keytwo" in err


def test_s3_url_exists(monkeypatch, capfd):
    def get_s3_session(url, method="fetch"):
        return MockS3Client()

    monkeypatch.setattr(spack.util.s3, "get_s3_session", get_s3_session)

    fake_s3_url_exists = "s3://my-bucket/subdirectory/my-file"
    assert spack.util.web.url_exists(fake_s3_url_exists)

    fake_s3_url_does_not_exist = "s3://my-bucket/subdirectory/my-notfound-file"
    assert not spack.util.web.url_exists(fake_s3_url_does_not_exist)


def test_s3_url_parsing():
    assert spack.util.s3._parse_s3_endpoint_url("example.com") == "https://example.com"
    assert spack.util.s3._parse_s3_endpoint_url("http://example.com") == "http://example.com"

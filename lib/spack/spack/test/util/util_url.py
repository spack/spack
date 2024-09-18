# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's URL handling utility functions."""
import os
import os.path
import urllib.parse

import pytest

import spack.util.path
import spack.util.url as url_util


def test_url_local_file_path(tmpdir):
    # Create a file
    path = str(tmpdir.join("hello.txt"))
    with open(path, "wb") as f:
        f.write(b"hello world")

    # Go from path -> url -> path.
    roundtrip = url_util.local_file_path(url_util.path_to_file_url(path))

    # Verify it's the same file.
    assert os.path.samefile(roundtrip, path)

    # Test if it accepts urlparse objects
    parsed = urllib.parse.urlparse(url_util.path_to_file_url(path))
    assert os.path.samefile(url_util.local_file_path(parsed), path)


def test_url_local_file_path_no_file_scheme():
    assert url_util.local_file_path("https://example.com/hello.txt") is None
    assert url_util.local_file_path("C:\\Program Files\\hello.txt") is None


def test_relative_path_to_file_url(tmpdir):
    # Create a file
    path = str(tmpdir.join("hello.txt"))
    with open(path, "wb") as f:
        f.write(b"hello world")

    with tmpdir.as_cwd():
        roundtrip = url_util.local_file_path(url_util.path_to_file_url("hello.txt"))
        assert os.path.samefile(roundtrip, path)


@pytest.mark.parametrize("resolve_href", [True, False])
@pytest.mark.parametrize("scheme", ["http", "s3", "gs", "file"])
def test_url_join_absolute(scheme, resolve_href):
    """Test that joining a URL with an absolute path works the same for schemes we care about, and
    whether we work in web browser mode or not."""
    fst = url_util.join(f"{scheme}://example.com/a/b/c", "/d/e/f", resolve_href=resolve_href)
    assert fst == f"{scheme}://example.com/d/e/f"

    snd = url_util.join(f"{scheme}://a.com/a", "https://b.com/b", resolve_href=resolve_href)
    assert snd == "https://b.com/b"


@pytest.mark.parametrize("scheme", ["http", "s3", "gs", "file"])
def test_url_join_up(scheme):
    """Test that the netloc component is preserved when going .. up in the path."""
    t1 = url_util.join(f"{scheme}://example/a/b.html", "c", resolve_href=True)
    assert t1 == f"{scheme}://example/a/c"
    t2 = url_util.join(f"{scheme}://example/a/b.html", "../c", resolve_href=True)
    assert t2 == f"{scheme}://example/c"
    t3 = url_util.join(f"{scheme}://example/a/b.html", "../../c", resolve_href=True)
    assert t3 == f"{scheme}://example/c"

    t4 = url_util.join(f"{scheme}://example/a/b", "c", resolve_href=False)
    assert t4 == f"{scheme}://example/a/b/c"
    t5 = url_util.join(f"{scheme}://example/a/b", "../c", resolve_href=False)
    assert t5 == f"{scheme}://example/a/c"
    t6 = url_util.join(f"{scheme}://example/a/b", "../../c", resolve_href=False)
    assert t6 == f"{scheme}://example/c"
    t7 = url_util.join(f"{scheme}://example/a/b", "../../../c", resolve_href=False)
    assert t7 == f"{scheme}://example/c"


@pytest.mark.parametrize("scheme", ["http", "https", "ftp", "s3", "gs", "file"])
def test_url_join_resolve_href(scheme):
    """test that `resolve_href=True` behaves like a web browser at the base page, and
    `resolve_href=False` behaves like joining paths in a file system at the base directory."""
    # these are equivalent because of the trailing /
    t1 = url_util.join(f"{scheme}://netloc/my/path/", "other/path", resolve_href=True)
    assert t1 == f"{scheme}://netloc/my/path/other/path"

    t2 = url_util.join(f"{scheme}://netloc/my/path", "other/path", resolve_href=False)
    assert t2 == f"{scheme}://netloc/my/path/other/path"

    # this is like a web browser: relative to /my.
    t3 = url_util.join(f"{scheme}://netloc/my/path", "other/path", resolve_href=True)
    assert t3 == f"{scheme}://netloc/my/other/path"


def test_default_download_name():
    url = "https://example.com:1234/path/to/file.txt;params?abc=def#file=blob.tar"
    filename = url_util.default_download_filename(url)
    assert filename == spack.util.path.sanitize_filename(filename)


def test_default_download_name_dot_dot():
    """Avoid that downloaded files get names computed as ., .. or any hidden file."""
    assert url_util.default_download_filename("https://example.com/.") == "_"
    assert url_util.default_download_filename("https://example.com/..") == "_."
    assert url_util.default_download_filename("https://example.com/.abcdef") == "_abcdef"


def test_parse_link_rel_next():
    parse = url_util.parse_link_rel_next
    assert parse(r'</abc>; rel="next"') == "/abc"
    assert parse(r'</abc>; x=y; rel="next", </def>; x=y; rel="prev"') == "/abc"
    assert parse(r'</abc>; rel="prev"; x=y, </def>; x=y; rel="next"') == "/def"

    # example from RFC5988
    assert (
        parse(
            r"""</TheBook/chapter2>; title*=UTF-8'de'letztes%20Kapitel; rel="previous","""
            r"""</TheBook/chapter4>; title*=UTF-8'de'n%c3%a4chstes%20Kapitel; rel="next" """
        )
        == "/TheBook/chapter4"
    )

    assert (
        parse(r"""<https://example.com/example>; key=";a=b, </c/d>; e=f"; rel="next" """)
        == "https://example.com/example"
    )

    assert parse("https://example.com/example") is None
    assert parse("<https://example.com/example; broken=broken") is None
    assert parse("https://example.com/example; rel=prev") is None
    assert parse("https://example.com/example; a=b; c=d; g=h") is None

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's URL handling utility functions."""
import os
import os.path
import urllib.parse

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


def test_url_join_local_paths():
    # Resolve local link against page URL

    # wrong:
    assert (
        url_util.join("s3://bucket/index.html", "../other-bucket/document.txt")
        == "s3://bucket/other-bucket/document.txt"
    )

    # correct - need to specify resolve_href=True:
    assert (
        url_util.join("s3://bucket/index.html", "../other-bucket/document.txt", resolve_href=True)
        == "s3://other-bucket/document.txt"
    )

    # same as above: make sure several components are joined together correctly
    assert (
        url_util.join(
            # with resolve_href=True, first arg is the base url; can not be
            # broken up
            "s3://bucket/index.html",
            # with resolve_href=True, remaining arguments are the components of
            # the local href that needs to be resolved
            "..",
            "other-bucket",
            "document.txt",
            resolve_href=True,
        )
        == "s3://other-bucket/document.txt"
    )

    # Append local path components to prefix URL

    # wrong:
    assert (
        url_util.join("https://mirror.spack.io/build_cache", "my-package", resolve_href=True)
        == "https://mirror.spack.io/my-package"
    )

    # correct - Need to specify resolve_href=False:
    assert (
        url_util.join("https://mirror.spack.io/build_cache", "my-package", resolve_href=False)
        == "https://mirror.spack.io/build_cache/my-package"
    )

    # same as above; make sure resolve_href=False is default
    assert (
        url_util.join("https://mirror.spack.io/build_cache", "my-package")
        == "https://mirror.spack.io/build_cache/my-package"
    )

    # same as above: make sure several components are joined together correctly
    assert (
        url_util.join(
            # with resolve_href=False, first arg is just a prefix. No
            # resolution is done.  So, there should be no difference between
            # join('/a/b/c', 'd/e'),
            # join('/a/b', 'c', 'd/e'),
            # join('/a', 'b/c', 'd', 'e'), etc.
            "https://mirror.spack.io",
            "build_cache",
            "my-package",
        )
        == "https://mirror.spack.io/build_cache/my-package"
    )

    # For s3:// URLs, the "netloc" (bucket) is considered part of the path.
    # Make sure join() can cross bucket boundaries in this case.
    args = ["s3://bucket/a/b", "new-bucket", "c"]
    assert url_util.join(*args) == "s3://bucket/a/b/new-bucket/c"

    args.insert(1, "..")
    assert url_util.join(*args) == "s3://bucket/a/new-bucket/c"

    args.insert(1, "..")
    assert url_util.join(*args) == "s3://bucket/new-bucket/c"

    # new-bucket is now the "netloc" (bucket name)
    args.insert(1, "..")
    assert url_util.join(*args) == "s3://new-bucket/c"


def test_url_join_absolute_paths():
    # Handling absolute path components is a little tricky.  To this end, we
    # distinguish "absolute path components", from the more-familiar concept of
    # "absolute paths" as they are understood for local filesystem paths.
    #
    # - All absolute paths are absolute path components.  Joining a URL with
    #   these components has the effect of completely replacing the path of the
    #   URL with the absolute path.  These components do not specify a URL
    #   scheme, so the scheme of the URL procuced when joining them depend on
    #   those provided by components that came before it (file:// assumed if no
    #   such scheme is provided).

    # For eaxmple:
    p = "/path/to/resource"
    # ...is an absolute path

    # http:// URL
    assert url_util.join("http://example.com/a/b/c", p) == "http://example.com/path/to/resource"

    # s3:// URL
    # also notice how the netloc is treated as part of the path for s3:// URLs
    assert url_util.join("s3://example.com/a/b/c", p) == "s3://path/to/resource"

    # - URL components that specify a scheme are always absolute path
    #   components.  Joining a base URL with these components effectively
    #   discards the base URL and "resets" the joining logic starting at the
    #   component in question and using it as the new base URL.

    # For eaxmple:
    p = "http://example.com/path/to"
    # ...is an http:// URL

    join_result = url_util.join(p, "resource")
    assert join_result == "http://example.com/path/to/resource"

    # works as if everything before the http:// URL was left out
    assert url_util.join("literally", "does", "not", "matter", p, "resource") == join_result

    assert url_util.join("file:///a/b/c", "./d") == "file:///a/b/c/d"

    # Finally, resolve_href should have no effect for how absolute path
    # components are handled because local hrefs can not be absolute path
    # components.
    args = [
        "s3://does",
        "not",
        "matter",
        "http://example.com",
        "also",
        "does",
        "not",
        "matter",
        "/path",
    ]

    expected = "http://example.com/path"
    assert url_util.join(*args, resolve_href=True) == expected
    assert url_util.join(*args, resolve_href=False) == expected

    # resolve_href only matters for the local path components at the end of the
    # argument list.
    args[-1] = "/path/to/page"
    args.extend(("..", "..", "resource"))

    assert url_util.join(*args, resolve_href=True) == "http://example.com/resource"

    assert url_util.join(*args, resolve_href=False) == "http://example.com/path/resource"


def test_default_download_name():
    url = "https://example.com:1234/path/to/file.txt;params?abc=def#file=blob.tar"
    filename = url_util.default_download_filename(url)
    assert filename == spack.util.path.sanitize_filename(filename)


def test_default_download_name_dot_dot():
    """Avoid that downloaded files get names computed as ., .. or any hidden file."""
    assert url_util.default_download_filename("https://example.com/.") == "_"
    assert url_util.default_download_filename("https://example.com/..") == "_."
    assert url_util.default_download_filename("https://example.com/.abcdef") == "_abcdef"

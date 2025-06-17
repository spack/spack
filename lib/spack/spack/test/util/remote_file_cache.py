# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import sys

import pytest

import llnl.util.tty as tty
from llnl.util.filesystem import join_path

import spack.config
import spack.util.remote_file_cache as rfc_util

github_url = "https://github.com/fake/fake/{0}/develop"
gitlab_url = "https://gitlab.fake.io/user/repo/-/blob/config/defaults"


@pytest.mark.parametrize(
    "path,err",
    [
        ("ssh://git@github.com:spack/", "Unsupported URL scheme"),
        ("bad:///this/is/a/file/url/include.yaml", "Invalid URL scheme"),
    ],
)
def test_rfc_local_path_bad_scheme(path, err):
    with pytest.raises(ValueError, match=err):
        _ = rfc_util.local_path(path, "")


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/a/b/c/d/e/config.py", "/a/b/c/d/e/config.py"),
        ("file:///this/is/a/file/url/include.yaml", "/this/is/a/file/url/include.yaml"),
        (
            "relative/packages.txt",
            os.path.join(os.environ["SPACK_ROOT"], "relative", "packages.txt"),
        ),
        (r"C:\Files (x86)\Windows\10", r"C:\Files (x86)\Windows\10"),
        (r"D:/spack stage", "D:\\spack stage"),
    ],
)
def test_rfc_local_file(path, expected):
    assert rfc_util.local_path(path, "") == os.path.normpath(expected)


def test_rfc_remote_local_path_no_dest():
    path = f"{gitlab_url}/packages.yaml"
    with pytest.raises(ValueError, match="Requires the destination argument"):
        _ = rfc_util.local_path(path, "")


packages_yaml_sha256 = (
    "6a1b26c857ca7e5bcd7342092e2f218da43d64b78bd72771f603027ea3c8b4af"
    if sys.platform != "win32"
    else "ae3239d769f9e6dc137a998489b0d44c70b03e21de4ecd6a623a3463a1a5c3f4"
)


@pytest.mark.parametrize(
    "url,sha256,err,msg",
    [
        (
            f"{join_path(github_url.format('tree'), 'config.yaml')}",
            "",
            ValueError,
            "Requires sha256",
        ),
        # This is the packages.yaml in lib/spack/spack/test/data/config
        (f"{gitlab_url}/packages.yaml", packages_yaml_sha256, None, ""),
        (f"{gitlab_url}/packages.yaml", "abcdef", ValueError, "does not match"),
        (f"{github_url.format('blob')}/README.md", "", OSError, "No such"),
        (github_url.format("tree"), "", OSError, "No such"),
        ("", "", ValueError, "argument is required"),
    ],
)
def test_rfc_remote_local_path(
    tmpdir, mutable_empty_config, mock_fetch_url_text, url, sha256, err, msg
):
    def _has_content(filename):
        # The first element of all configuration files for this test happen to
        # be the basename of the file so this check leverages that feature. If
        # that changes, then this check will need to change accordingly.
        element = f"{os.path.splitext(os.path.basename(filename))[0]}:"
        with open(filename, "r", encoding="utf-8") as fd:
            for line in fd:
                if element in line:
                    return True
        tty.debug(f"Expected {element} in '{filename}'")
        return False

    def _dest_dir():
        return join_path(tmpdir.strpath, "cache")

    if err is not None:
        with spack.config.override("config:url_fetch_method", "curl"):
            with pytest.raises(err, match=msg):
                rfc_util.local_path(url, sha256, _dest_dir)
    else:
        with spack.config.override("config:url_fetch_method", "curl"):
            path = rfc_util.local_path(url, sha256, _dest_dir)
            assert os.path.exists(path)
            # Ensure correct file is "fetched"
            assert os.path.basename(path) == os.path.basename(url)
            # Ensure contents of the file contains expected config element
            assert _has_content(path)

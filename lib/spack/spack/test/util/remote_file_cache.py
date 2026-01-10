# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import pathlib
import sys

import pytest

import spack.config
import spack.llnl.util.tty as tty
import spack.util.remote_file_cache as rfc_util
from spack.llnl.util.filesystem import join_path

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


@pytest.mark.not_on_windows("Unix path")
def test_rfc_local_file_unix():
    assert rfc_util.local_path("/a/b/c/d/e/config.py", "") == "/a/b/c/d/e/config.py"
    assert (
        rfc_util.local_path("file:///this/is/a/file/url/include.yaml", "")
        == "/this/is/a/file/url/include.yaml"
    )


@pytest.mark.only_windows("Windows path")
def test_rfc_local_file_windows():
    assert rfc_util.local_path(r"C:\Files (x86)\Windows\10", "") == r"C:\Files (x86)\Windows\10"
    assert rfc_util.local_path(r"D:/spack stage", "") == r"D:\spack stage"


def test_rfc_local_file_relative():
    path = "relative/packages.txt"
    expected = os.path.join(os.getcwd(), "relative", "packages.txt")
    assert rfc_util.local_path(path, "") == expected


def test_rfc_remote_local_path_no_dest():
    path = f"{gitlab_url}/packages.yaml"
    with pytest.raises(ValueError, match="Requires the destination argument"):
        _ = rfc_util.local_path(path, "")


packages_yaml_sha256 = (
    "8d428c600b215e3b4a207a08236659dfc2c9ae2782c35943a00ee4204a135702"
    if sys.platform != "win32"
    else "6c094ec3ee1eb5068860cdd97d8da965bf281be29e60ab9afc8f6e4d72d24f21"
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
    tmp_path: pathlib.Path, mutable_empty_config, mock_fetch_url_text, url, sha256, err, msg
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
        return join_path(str(tmp_path), "cache")

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

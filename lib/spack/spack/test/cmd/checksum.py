# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

import pytest

import llnl.util.tty as tty

import spack.cmd.checksum
import spack.repo
from spack.main import SpackCommand

spack_checksum = SpackCommand("checksum")


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["--batch", "patch"], (True, False, False, False)),
        (["--latest", "patch"], (False, True, False, False)),
        (["--preferred", "patch"], (False, False, True, False)),
        (["--add-to-package", "patch"], (False, False, False, True)),
    ],
)
def test_checksum_args(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.checksum.setup_parser(parser)
    args = parser.parse_args(arguments)
    check = args.batch, args.latest, args.preferred, args.add_to_package
    assert check == expected


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["--batch", "preferred-test"], "version of preferred-test"),
        (["--latest", "preferred-test"], "Found 1 version"),
        (["--preferred", "preferred-test"], "Found 1 version"),
        (["--add-to-package", "preferred-test"], "Added 1 new versions to"),
    ],
)
def test_checksum(arguments, expected, mock_packages, mock_clone_repo, mock_stage):
    output = spack_checksum(*arguments)
    assert expected in output
    assert "version(" in output


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_checksum_interactive(mock_packages, mock_fetch, mock_stage, monkeypatch):
    # TODO: mock_fetch doesn't actually work with stage, working around with ignoring
    # fail_on_error for now
    def _get_number(*args, **kwargs):
        return 1

    monkeypatch.setattr(tty, "get_number", _get_number)

    output = spack_checksum("preferred-test", fail_on_error=False)
    assert "version of preferred-test" in output
    assert "version(" in output


def test_checksum_versions(mock_packages, mock_clone_repo, mock_fetch, mock_stage):
    pkg_cls = spack.repo.path.get_pkg_class("preferred-test")
    versions = [str(v) for v in pkg_cls.versions if not v.isdevelop()]
    output = spack_checksum("preferred-test", versions[0])
    assert "Found 1 version" in output
    assert "version(" in output
    output = spack_checksum("--add-to-package", "preferred-test", versions[0])
    assert "Found 1 version" in output
    assert "version(" in output
    assert "Added 1 new versions to" in output


def test_checksum_missing_version(mock_packages, mock_clone_repo, mock_fetch, mock_stage):
    output = spack_checksum("preferred-test", "99.99.99", fail_on_error=False)
    assert "Could not find any remote versions" in output
    output = spack_checksum("--add-to-package", "preferred-test", "99.99.99", fail_on_error=False)
    assert "Could not find any remote versions" in output
    assert "Added 1 new versions to" not in output


def test_checksum_deprecated_version(mock_packages, mock_clone_repo, mock_fetch, mock_stage):
    output = spack_checksum("deprecated-versions", "1.1.0", fail_on_error=False)
    assert "Version 1.1.0 is deprecated" in output
    output = spack_checksum(
        "--add-to-package", "deprecated-versions", "1.1.0", fail_on_error=False
    )
    assert "Version 1.1.0 is deprecated" in output
    assert "Added 1 new versions to" not in output

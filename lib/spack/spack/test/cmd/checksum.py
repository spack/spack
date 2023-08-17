# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import llnl.util.tty as tty

import spack.cmd.checksum
import spack.repo
import spack.spec
from spack.main import SpackCommand

spack_checksum = SpackCommand("checksum")


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["--batch", "patch"], (True, False, False, False, False)),
        (["--latest", "patch"], (False, True, False, False, False)),
        (["--preferred", "patch"], (False, False, True, False, False)),
        (["--add-to-package", "patch"], (False, False, False, True, False)),
        (["--verify", "patch"], (False, False, False, False, True)),
    ],
)
def test_checksum_args(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.checksum.setup_parser(parser)
    args = parser.parse_args(arguments)
    check = args.batch, args.latest, args.preferred, args.add_to_package, args.verify
    assert check == expected


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["--batch", "preferred-test"], "version of preferred-test"),
        (["--latest", "preferred-test"], "Found 1 version"),
        (["--preferred", "preferred-test"], "Found 1 version"),
        (["--add-to-package", "preferred-test"], "Added 0 new versions to"),
        (["--verify", "preferred-test"], "Verified 1 of 1"),
        (["--verify", "zlib", "1.2.13"], "1.2.13  [-] No previous checksum"),
    ],
)
def test_checksum(arguments, expected, mock_packages, mock_clone_repo, mock_stage):
    output = spack_checksum(*arguments)
    assert expected in output

    # --verify doesn't print versions strings like other flags
    if "--verify" not in arguments:
        assert "version(" in output


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
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
    pkg_cls = spack.repo.PATH.get_pkg_class("zlib")
    versions = [str(v) for v in pkg_cls.versions]
    output = spack_checksum("zlib", *versions)
    assert "Found 3 versions" in output
    assert "version(" in output
    output = spack_checksum("--add-to-package", "zlib", *versions)
    assert "Found 3 versions" in output
    assert "Added 0 new versions to" in output


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
    assert "Added 0 new versions to" not in output


def test_checksum_at(mock_packages):
    pkg_cls = spack.repo.PATH.get_pkg_class("zlib")
    versions = [str(v) for v in pkg_cls.versions]
    output = spack_checksum(f"zlib@{versions[0]}")
    assert "Found 1 version" in output


def test_checksum_url(mock_packages):
    pkg_cls = spack.repo.PATH.get_pkg_class("zlib")
    output = spack_checksum(f"{pkg_cls.url}", fail_on_error=False)
    assert "accepts package names" in output


def test_checksum_verification_fails(install_mockery, capsys):
    spec = spack.spec.Spec("zlib").concretized()
    pkg = spec.package
    versions = list(pkg.versions.keys())
    version_hashes = {versions[0]: "abadhash", spack.version.Version("0.1"): "123456789"}
    with pytest.raises(SystemExit):
        spack.cmd.checksum.print_checksum_status(pkg, version_hashes)
    out = str(capsys.readouterr())
    assert out.count("Correct") == 0
    assert "No previous checksum" in out
    assert "Invalid checksum" in out

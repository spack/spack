# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import spack.cmd.checksum
import spack.parser
import spack.repo
import spack.spec
from spack.main import SpackCommand
from spack.stage import interactive_version_filter
from spack.version import Version

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


def input_from_commands(*commands):
    """Create a function that returns the next command from a list of inputs for interactive spack
    checksum. If None is encountered, this is equivalent to EOF / ^D."""
    commands = iter(commands)

    def _input(prompt):
        cmd = next(commands)
        if cmd is None:
            raise EOFError
        assert isinstance(cmd, str)
        return cmd

    return _input


def test_checksum_interactive_filter():
    # Filter effectively by 1:1.0, then checksum.
    input = input_from_commands("f", "@1:", "f", "@:1.0", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
    }


def test_checksum_interactive_return_from_filter_prompt():
    # Enter and then exit filter subcommand.
    input = input_from_commands("f", None, "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
        Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
        Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
    }


def test_checksum_interactive_quit_returns_none():
    # Quit after filtering something out (y to confirm quit)
    input = input_from_commands("f", "@1:", "q", "y")
    assert (
        interactive_version_filter(
            {
                Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
                Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
                Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
            },
            input=input,
        )
        is None
    )


def test_checksum_interactive_reset_resets():
    # Filter 1:, then reset, then filter :0, should just given 0.9 (it was filtered out
    # before reset)
    input = input_from_commands("f", "@1:", "r", "f", ":0", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz"}


def test_checksum_interactive_ask_each():
    # Ask each should run on the filtered list. First select 1.x, then select only the second
    # entry, which is 1.0.1.
    input = input_from_commands("f", "@1:", "a", "n", "y", "n")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz"}


def test_checksum_interactive_quit_from_ask_each():
    # Enter ask each mode, select the second item, then quit from submenu, then checksum, which
    # should still include the last item at which ask each stopped.
    input = input_from_commands("a", "n", "y", None, "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
        Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
    }


def test_checksum_interactive_nothing_left():
    """If nothing is left after interactive filtering, return an empty dict."""
    input = input_from_commands("f", "@2", "c")
    assert (
        interactive_version_filter(
            {
                Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
                Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
                Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
            },
            input=input,
        )
        == {}
    )


def test_checksum_interactive_new_only():
    # The 1.0 version is known already, and should be dropped on `n`.
    input = input_from_commands("n", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        known_versions=[Version("1.0")],
        input=input,
    ) == {
        Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
        Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
    }


def test_checksum_interactive_top_n():
    """Test integers select top n versions"""
    input = input_from_commands("2", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
    }


def test_checksum_interactive_unrecognized_command():
    """Unrecognized commands should be ignored"""
    input = input_from_commands("-1", "0", "hello", "c")
    v = {Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz"}
    assert interactive_version_filter(v.copy(), input=input) == v


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


def test_checksum_url(mock_packages):
    pkg_cls = spack.repo.PATH.get_pkg_class("zlib")
    with pytest.raises(spack.parser.SpecSyntaxError):
        spack_checksum(f"{pkg_cls.url}")


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

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``llnl/util/argparsewriter.py``

These tests are fairly minimal, and ArgparseWriter is more extensively
tested in ``cmd/commands.py``.
"""

import argparse
import io

import pytest

import spack.main
import spack.util.argparsewriter as aw

parser = spack.main.make_argument_parser()
spack.main.add_all_commands(parser)


class ProgWriter(aw.ArgparseWriter):
    """Writer that prints the program name of every parser it visits."""

    def format(self, cmd: aw.Command) -> str:
        return cmd.prog + "\n"


def test_format_not_overridden():
    with pytest.raises(TypeError):
        aw.ArgparseWriter("spack")


def suppress_parser() -> argparse.ArgumentParser:
    """Parser with a shown and a hidden argument of every kind."""
    root = argparse.ArgumentParser(prog="root")
    root.add_argument("--shown-flag", help="shown")
    root.add_argument("--hidden-flag", help=argparse.SUPPRESS)

    subparsers = root.add_subparsers()
    shown = subparsers.add_parser("shown-command", help="shown")
    subparsers.add_parser("hidden-command", help=argparse.SUPPRESS)

    shown.add_argument("shown_positional", help="shown")
    shown.add_argument("hidden_positional", help=argparse.SUPPRESS)

    return root


def test_suppressed_arguments_not_parsed():
    """Arguments with suppressed help are left out entirely."""
    writer = ProgWriter("root")
    cmd = writer.parse(suppress_parser(), "root")

    flags = [flag for option in cmd.optionals for flag in option.flags]
    assert "--shown-flag" in flags
    assert "--hidden-flag" not in flags

    assert [subcommand.name for subcommand in cmd.subcommands] == ["shown-command"]

    sub = writer.parse(cmd.subcommands[0].parser, "shown-command")
    assert [positional.name for positional in sub.positionals] == ["shown_positional"]


def test_suppressed_subcommand_not_written():
    """Suppressed subcommands are not recursed into."""
    out = io.StringIO()
    ProgWriter("root", out=out).write(suppress_parser())
    assert out.getvalue().splitlines() == ["root", "root shown-command"]

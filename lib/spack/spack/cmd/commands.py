# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import copy
import os
import re
import sys
from argparse import ArgumentParser, Namespace
from typing import IO, Any, Callable, Dict, Sequence, Set

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.argparsewriter import (
    ArgparseCompletionWriter,
    ArgparseRstWriter,
    ArgparseWriter,
    Command,
)
from llnl.util.tty.colify import colify

import spack.cmd
import spack.main
import spack.paths
from spack.main import section_descriptions

description = "list available spack commands"
section = "developer"
level = "long"


#: list of command formatters
formatters: Dict[str, Callable[[Namespace, IO], None]] = {}


#: standard arguments for updating completion scripts
#: we iterate through these when called with --update-completion
update_completion_args: Dict[str, Dict[str, Any]] = {
    "bash": {
        "aliases": True,
        "format": "bash",
        "header": os.path.join(spack.paths.share_path, "bash", "spack-completion.in"),
        "update": os.path.join(spack.paths.share_path, "spack-completion.bash"),
    }
}


def formatter(func: Callable[[Namespace, IO], None]) -> Callable[[Namespace, IO], None]:
    """Decorator used to register formatters.

    Args:
        func: Formatting function.

    Returns:
        The same function.
    """
    formatters[func.__name__] = func
    return func


def setup_parser(subparser: ArgumentParser) -> None:
    """Set up the argument parser.

    Args:
        subparser: Preliminary argument parser.
    """
    subparser.add_argument(
        "--update-completion",
        action="store_true",
        default=False,
        help="regenerate spack's tab completion scripts",
    )

    subparser.add_argument(
        "-a", "--aliases", action="store_true", default=False, help="include command aliases"
    )
    subparser.add_argument(
        "--format",
        default="names",
        choices=formatters,
        help="format to be used to print the output (default: names)",
    )
    subparser.add_argument(
        "--header",
        metavar="FILE",
        default=None,
        action="store",
        help="prepend contents of FILE to the output (useful for rst format)",
    )
    subparser.add_argument(
        "--update",
        metavar="FILE",
        default=None,
        action="store",
        help="write output to the specified file, if any command is newer",
    )
    subparser.add_argument(
        "rst_files",
        nargs=argparse.REMAINDER,
        help="list of rst files to search for `_cmd-spack-<cmd>` cross-refs",
    )


class SpackArgparseRstWriter(ArgparseRstWriter):
    """RST writer tailored for spack documentation."""

    def __init__(
        self,
        prog: str,
        out: IO = sys.stdout,
        aliases: bool = False,
        documented_commands: Set[str] = set(),
        rst_levels: Sequence[str] = ["-", "-", "^", "~", ":", "`"],
    ):
        """Initialize a new SpackArgparseRstWriter instance.

        Args:
            prog: Program name.
            out: File object to write to.
            aliases: Whether or not to include subparsers for aliases.
            documented_commands: Set of commands with additional documentation.
            rst_levels: List of characters for rst section headings.
        """
        super().__init__(prog, out, aliases, rst_levels)
        self.documented = documented_commands

    def usage(self, usage: str) -> str:
        """Example usage of a command.

        Args:
            usage: Command usage.

        Returns:
            Usage of a command.
        """
        string = super().usage(usage)

        cmd = self.parser.prog.replace(" ", "-")
        if cmd in self.documented:
            string += "\n:ref:`More documentation <cmd-{0}>`\n".format(cmd)

        return string


class SubcommandWriter(ArgparseWriter):
    """Write argparse output as a list of subcommands."""

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of this subcommand.
        """
        return "    " * self.level + cmd.prog + "\n"


_positional_to_subroutine: Dict[str, str] = {
    "package": "_all_packages",
    "spec": "_all_packages",
    "filter": "_all_packages",
    "installed": "_installed_packages",
    "compiler": "_installed_compilers",
    "section": "_config_sections",
    "env": "_environments",
    "extendable": "_extensions",
    "keys": "_keys",
    "help_command": "_subcommands",
    "mirror": "_mirrors",
    "virtual": "_providers",
    "namespace": "_repos",
    "hash": "_all_resource_hashes",
    "pytest": "_unit_tests",
}


class BashCompletionWriter(ArgparseCompletionWriter):
    """Write argparse output as bash programmable tab completion."""

    def body(
        self, positionals: Sequence[str], optionals: Sequence[str], subcommands: Sequence[str]
    ) -> str:
        """Return the body of the function.

        Args:
            positionals: List of positional arguments.
            optionals: List of optional arguments.
            subcommands: List of subcommand parsers.

        Returns:
            Function body.
        """
        if positionals:
            return """
    if $list_options
    then
        {0}
    else
        {1}
    fi
""".format(
                self.optionals(optionals), self.positionals(positionals)
            )
        elif subcommands:
            return """
    if $list_options
    then
        {0}
    else
        {1}
    fi
""".format(
                self.optionals(optionals), self.subcommands(subcommands)
            )
        else:
            return """
    {0}
""".format(
                self.optionals(optionals)
            )

    def positionals(self, positionals: Sequence[str]) -> str:
        """Return the syntax for reporting positional arguments.

        Args:
            positionals: List of positional arguments.

        Returns:
            Syntax for positional arguments.
        """
        # If match found, return function name
        for positional in positionals:
            for key, value in _positional_to_subroutine.items():
                if positional.startswith(key):
                    return value

        # If no matches found, return empty list
        return 'SPACK_COMPREPLY=""'

    def optionals(self, optionals: Sequence[str]) -> str:
        """Return the syntax for reporting optional flags.

        Args:
            optionals: List of optional arguments.

        Returns:
            Syntax for optional flags.
        """
        return 'SPACK_COMPREPLY="{0}"'.format(" ".join(optionals))

    def subcommands(self, subcommands: Sequence[str]) -> str:
        """Return the syntax for reporting subcommands.

        Args:
            subcommands: List of subcommand parsers.

        Returns:
            Syntax for subcommand parsers
        """
        return 'SPACK_COMPREPLY="{0}"'.format(" ".join(subcommands))


@formatter
def subcommands(args: Namespace, out: IO) -> None:
    """Hierarchical tree of subcommands.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)
    writer = SubcommandWriter(parser.prog, out, args.aliases)
    writer.write(parser)


def rst_index(out: IO) -> None:
    """Generate an index of all commands.

    Args:
        out: File object to write to.
    """
    out.write("\n")

    index = spack.main.index_commands()
    sections = index["long"]

    dmax = max(len(section_descriptions.get(s, s)) for s in sections) + 2
    cmax = max(len(c) for _, c in sections.items()) + 60

    row = "%s  %s\n" % ("=" * dmax, "=" * cmax)
    line = "%%-%ds  %%s\n" % dmax

    out.write(row)
    out.write(line % (" Category ", " Commands "))
    out.write(row)
    for section, commands in sorted(sections.items()):
        description = section_descriptions.get(section, section)

        for i, cmd in enumerate(sorted(commands)):
            description = description.capitalize() if i == 0 else ""
            ref = ":ref:`%s <spack-%s>`" % (cmd, cmd)
            comma = "," if i != len(commands) - 1 else ""
            bar = "| " if i % 8 == 0 else "  "
            out.write(line % (description, bar + ref + comma))
    out.write(row)


@formatter
def rst(args: Namespace, out: IO) -> None:
    """ReStructuredText documentation of subcommands.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    # create a parser with all commands
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    # extract cross-refs of the form `_cmd-spack-<cmd>:` from rst files
    documented_commands: Set[str] = set()
    for filename in args.rst_files:
        with open(filename) as f:
            for line in f:
                match = re.match(r"\.\. _cmd-(spack-.*):", line)
                if match:
                    documented_commands.add(match.group(1).strip())

    # print an index to each command
    rst_index(out)
    out.write("\n")

    # print sections for each command and subcommand
    writer = SpackArgparseRstWriter(parser.prog, out, args.aliases, documented_commands)
    writer.write(parser)


@formatter
def names(args: Namespace, out: IO) -> None:
    """Simple list of top-level commands.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    commands = copy.copy(spack.cmd.all_commands())

    if args.aliases:
        commands.extend(spack.main.aliases.keys())

    colify(commands, output=out)


@formatter
def bash(args: Namespace, out: IO) -> None:
    """Bash tab-completion script.

    args:
        args: Command-line arguments.
        out: File object to write to.
    """
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    writer = BashCompletionWriter(parser.prog, out, args.aliases)
    writer.write(parser)


def prepend_header(args: Namespace, out: IO) -> None:
    """Prepend header text at the beginning of a file.

    Args:
        args: Command-line arguments.
        out: File object to write to.
    """
    if not args.header:
        return

    with open(args.header) as header:
        out.write(header.read())


def _commands(parser: ArgumentParser, args: Namespace) -> None:
    """This is the 'regular' command, which can be called multiple times.

    See ``commands()`` below for ``--update-completion`` handling.

    Args:
        parser: Argument parser.
        args: Command-line arguments.
    """
    formatter = formatters[args.format]

    # check header first so we don't open out files unnecessarily
    if args.header and not os.path.exists(args.header):
        tty.die("No such file: '%s'" % args.header)

    if args.update:
        tty.msg("Updating file: %s" % args.update)
        with open(args.update, "w") as f:
            prepend_header(args, f)
            formatter(args, f)

        if args.update_completion:
            fs.set_executable(args.update)

    else:
        prepend_header(args, sys.stdout)
        formatter(args, sys.stdout)


def update_completion(parser: ArgumentParser, args: Namespace) -> None:
    """Iterate through the shells and update the standard completion files.

    This is a convenience method to avoid calling this command many
    times, and to simplify completion update for developers.

    Args:
        parser: Argument parser.
        args: Command-line arguments.
    """
    for shell, shell_args in update_completion_args.items():
        for attr, value in shell_args.items():
            setattr(args, attr, value)
        _commands(parser, args)


def commands(parser: ArgumentParser, args: Namespace) -> None:
    """Main function that calls formatter functions.

    Args:
        parser: Argument parser.
        args: Command-line arguments.
    """
    if args.update_completion:
        if args.format != "names" or any([args.aliases, args.update, args.header]):
            tty.die("--update-completion can only be specified alone.")

        # this runs the command multiple times with different arguments
        update_completion(parser, args)

    else:
        # run commands normally
        _commands(parser, args)

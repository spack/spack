# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import abc
import argparse
import io
import re
import sys
from argparse import ArgumentParser
from typing import IO, Optional, Sequence, Tuple


class Command:
    """Parsed representation of a command from argparse.

    This is a single command from an argparse parser. ``ArgparseWriter`` creates these and returns
    them from ``parse()``, and it passes one of these to each call to ``format()`` so that we can
    take an action for a single command.
    """

    def __init__(
        self,
        prog: str,
        description: Optional[str],
        usage: str,
        positionals: Sequence[Tuple[str, str]],
        optionals: Sequence[Tuple[Sequence[str], str, str]],
        subcommands: Sequence[Tuple[ArgumentParser, str]],
    ) -> None:
        """Initialize a new Command instance.

        Args:
            prog: Program name.
            description: Command description.
            usage: Command usage.
            positionals: List of positional arguments.
            optionals: List of optional arguments.
            subcommands: List of subcommand parsers.
        """
        self.prog = prog
        self.description = description
        self.usage = usage
        self.positionals = positionals
        self.optionals = optionals
        self.subcommands = subcommands


# NOTE: The only reason we subclass argparse.HelpFormatter is to get access to self._expand_help(),
# ArgparseWriter is not intended to be used as a formatter_class.
class ArgparseWriter(argparse.HelpFormatter, abc.ABC):
    """Analyze an argparse ArgumentParser for easy generation of help."""

    def __init__(self, prog: str, out: IO = sys.stdout, aliases: bool = False) -> None:
        """Initialize a new ArgparseWriter instance.

        Args:
            prog: Program name.
            out: File object to write to.
            aliases: Whether or not to include subparsers for aliases.
        """
        super().__init__(prog)
        self.level = 0
        self.prog = prog
        self.out = out
        self.aliases = aliases

    def parse(self, parser: ArgumentParser, prog: str) -> Command:
        """Parse the parser object and return the relavent components.

        Args:
            parser: Command parser.
            prog: Program name.

        Returns:
            Information about the command from the parser.
        """
        self.parser = parser

        split_prog = parser.prog.split(" ")
        split_prog[-1] = prog
        prog = " ".join(split_prog)
        description = parser.description

        fmt = parser._get_formatter()
        actions = parser._actions
        groups = parser._mutually_exclusive_groups
        usage = fmt._format_usage(None, actions, groups, "").strip()

        # Go through actions and split them into optionals, positionals, and subcommands
        optionals = []
        positionals = []
        subcommands = []
        for action in actions:
            if action.option_strings:
                flags = action.option_strings
                dest_flags = fmt._format_action_invocation(action)
                help = self._expand_help(action) if action.help else ""
                help = help.replace("\n", " ")
                optionals.append((flags, dest_flags, help))
            elif isinstance(action, argparse._SubParsersAction):
                for subaction in action._choices_actions:
                    subparser = action._name_parser_map[subaction.dest]
                    subcommands.append((subparser, subaction.dest))

                    # Look for aliases of the form 'name (alias, ...)'
                    if self.aliases and isinstance(subaction.metavar, str):
                        match = re.match(r"(.*) \((.*)\)", subaction.metavar)
                        if match:
                            aliases = match.group(2).split(", ")
                            for alias in aliases:
                                subparser = action._name_parser_map[alias]
                                subcommands.append((subparser, alias))
            else:
                args = fmt._format_action_invocation(action)
                help = self._expand_help(action) if action.help else ""
                help = help.replace("\n", " ")
                positionals.append((args, help))

        return Command(prog, description, usage, positionals, optionals, subcommands)

    @abc.abstractmethod
    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Override this in subclasses to define how each subcommand should be displayed.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of this subcommand.
        """

    def _write(self, parser: ArgumentParser, prog: str, level: int = 0) -> None:
        """Recursively write a parser.

        Args:
            parser: Command parser.
            prog: Program name.
            level: Current level.
        """
        self.level = level

        cmd = self.parse(parser, prog)
        self.out.write(self.format(cmd))

        for subparser, prog in cmd.subcommands:
            self._write(subparser, prog, level=level + 1)

    def write(self, parser: ArgumentParser) -> None:
        """Write out details about an ArgumentParser.

        Args:
            parser: Command parser.
        """
        try:
            self._write(parser, self.prog)
        except BrokenPipeError:
            # Swallow pipe errors
            pass


_rst_levels = ["=", "-", "^", "~", ":", "`"]


class ArgparseRstWriter(ArgparseWriter):
    """Write argparse output as rst sections."""

    def __init__(
        self,
        prog: str,
        out: IO = sys.stdout,
        aliases: bool = False,
        rst_levels: Sequence[str] = _rst_levels,
    ) -> None:
        """Initialize a new ArgparseRstWriter instance.

        Args:
            prog: Program name.
            out: File object to write to.
            aliases: Whether or not to include subparsers for aliases.
            rst_levels: List of characters for rst section headings.
        """
        super().__init__(prog, out, aliases)
        self.rst_levels = rst_levels

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of a node.
        """
        string = io.StringIO()
        string.write(self.begin_command(cmd.prog))

        if cmd.description:
            string.write(self.description(cmd.description))

        string.write(self.usage(cmd.usage))

        if cmd.positionals:
            string.write(self.begin_positionals())
            for args, help in cmd.positionals:
                string.write(self.positional(args, help))
            string.write(self.end_positionals())

        if cmd.optionals:
            string.write(self.begin_optionals())
            for flags, dest_flags, help in cmd.optionals:
                string.write(self.optional(dest_flags, help))
            string.write(self.end_optionals())

        if cmd.subcommands:
            string.write(self.begin_subcommands(cmd.subcommands))

        return string.getvalue()

    def begin_command(self, prog: str) -> str:
        """Text to print before a command.

        Args:
            prog: Program name.

        Returns:
            Text before a command.
        """
        return """
----

.. _{0}:

{1}
{2}

""".format(
            prog.replace(" ", "-"), prog, self.rst_levels[self.level] * len(prog)
        )

    def description(self, description: str) -> str:
        """Description of a command.

        Args:
            description: Command description.

        Returns:
            Description of a command.
        """
        return description + "\n\n"

    def usage(self, usage: str) -> str:
        """Example usage of a command.

        Args:
            usage: Command usage.

        Returns:
            Usage of a command.
        """
        return """\
.. code-block:: console

    {0}

""".format(
            usage
        )

    def begin_positionals(self) -> str:
        """Text to print before positional arguments.

        Returns:
            Positional arguments header.
        """
        return "\n**Positional arguments**\n\n"

    def positional(self, name: str, help: str) -> str:
        """Description of a positional argument.

        Args:
            name: Argument name.
            help: Help text.

        Returns:
            Positional argument description.
        """
        return """\
{0}
  {1}

""".format(
            name, help
        )

    def end_positionals(self) -> str:
        """Text to print after positional arguments.

        Returns:
            Positional arguments footer.
        """
        return ""

    def begin_optionals(self) -> str:
        """Text to print before optional arguments.

        Returns:
            Optional arguments header.
        """
        return "\n**Optional arguments**\n\n"

    def optional(self, opts: str, help: str) -> str:
        """Description of an optional argument.

        Args:
            opts: Optional argument.
            help: Help text.

        Returns:
            Optional argument description.
        """
        return """\
``{0}``
  {1}

""".format(
            opts, help
        )

    def end_optionals(self) -> str:
        """Text to print after optional arguments.

        Returns:
            Optional arguments footer.
        """
        return ""

    def begin_subcommands(self, subcommands: Sequence[Tuple[ArgumentParser, str]]) -> str:
        """Table with links to other subcommands.

        Arguments:
            subcommands: List of subcommands.

        Returns:
            Subcommand linking text.
        """
        string = """
**Subcommands**

.. hlist::
   :columns: 4

"""

        for cmd, _ in subcommands:
            prog = re.sub(r"^[^ ]* ", "", cmd.prog)
            string += "   * :ref:`{0} <{1}>`\n".format(prog, cmd.prog.replace(" ", "-"))

        return string + "\n"


class ArgparseCompletionWriter(ArgparseWriter):
    """Write argparse output as shell programmable tab completion functions."""

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of this subcommand.
        """

        assert cmd.optionals  # we should always at least have -h, --help
        assert not (cmd.positionals and cmd.subcommands)  # one or the other

        # We only care about the arguments/flags, not the help messages
        positionals: Tuple[str, ...] = ()
        if cmd.positionals:
            positionals, _ = zip(*cmd.positionals)
        optionals, _, _ = zip(*cmd.optionals)
        subcommands: Tuple[str, ...] = ()
        if cmd.subcommands:
            _, subcommands = zip(*cmd.subcommands)

        # Flatten lists of lists
        optionals = [x for xx in optionals for x in xx]

        return (
            self.start_function(cmd.prog)
            + self.body(positionals, optionals, subcommands)
            + self.end_function(cmd.prog)
        )

    def start_function(self, prog: str) -> str:
        """Return the syntax needed to begin a function definition.

        Args:
            prog: Program name.

        Returns:
            Function definition beginning.
        """
        name = prog.replace("-", "_").replace(" ", "_")
        return "\n_{0}() {{".format(name)

    def end_function(self, prog: str) -> str:
        """Return the syntax needed to end a function definition.

        Args:
            prog: Program name

        Returns:
            Function definition ending.
        """
        return "}\n"

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
        return ""

    def positionals(self, positionals: Sequence[str]) -> str:
        """Return the syntax for reporting positional arguments.

        Args:
            positionals: List of positional arguments.

        Returns:
            Syntax for positional arguments.
        """
        return ""

    def optionals(self, optionals: Sequence[str]) -> str:
        """Return the syntax for reporting optional flags.

        Args:
            optionals: List of optional arguments.

        Returns:
            Syntax for optional flags.
        """
        return ""

    def subcommands(self, subcommands: Sequence[str]) -> str:
        """Return the syntax for reporting subcommands.

        Args:
            subcommands: List of subcommand parsers.

        Returns:
            Syntax for subcommand parsers
        """
        return ""

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import abc
import argparse
import io
import re
import sys
from argparse import ArgumentParser
from typing import IO, Any, Iterable, List, NamedTuple, Optional, Sequence, Union


class Positional(NamedTuple):
    """A positional argument of a command."""

    #: Name of the argument as it appears in the usage string
    name: str
    #: Allowed values, if the argument is restricted to a set of choices
    choices: Optional[Iterable[Any]]
    #: Number of values the argument takes
    nargs: Union[int, str, None]
    #: First line of the help message
    help: str


class Option(NamedTuple):
    """An optional argument of a command."""

    #: Flags that select this option, such as ``-h`` and ``--help``
    flags: Sequence[str]
    #: Allowed values if the option is restricted to a set of choices, otherwise the destination
    dest: List[str]
    #: Flags with their arguments, as they appear in the usage string
    dest_flags: str
    #: Number of values the option takes
    nargs: Union[int, str, None]
    #: First line of the help message
    help: str


class Subcommand(NamedTuple):
    """A subcommand of a command."""

    #: Parser of the subcommand
    parser: ArgumentParser
    #: Name of the subcommand, which is an alias if the command was reached through one
    name: str
    #: First line of the help message
    help: str


class Command(NamedTuple):
    """Parsed representation of a command from argparse.

    This is a single command from an argparse parser. ``ArgparseWriter`` creates these and returns
    them from ``parse()``, and it passes one of these to each call to ``format()`` so that we can
    take an action for a single command.
    """

    #: Program name.
    prog: str
    #: Command description.
    description: Optional[str]
    #: Command usage.
    usage: str
    #: List of positional arguments.
    positionals: List[Positional]
    #: List of optional arguments.
    optionals: List[Option]
    #: List of subcommands.
    subcommands: List[Subcommand]


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
        """Parse the parser object and return the relevant components.

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
        optionals: List[Option] = []
        positionals: List[Positional] = []
        subcommands: List[Subcommand] = []
        for action in actions:
            if action.option_strings:
                dest_flags = fmt._format_action_invocation(action)
                help = (
                    self._expand_help(action)
                    if action.help and action.help != argparse.SUPPRESS
                    else ""
                )
                help = help.split("\n")[0]

                if action.choices is not None:
                    dest = [str(choice) for choice in action.choices]
                else:
                    dest = [action.dest]

                optionals.append(
                    Option(action.option_strings, dest, dest_flags, action.nargs, help)
                )
            elif isinstance(action, argparse._SubParsersAction):
                for subaction in action._choices_actions:
                    subparser = action._name_parser_map[subaction.dest]
                    help = (
                        self._expand_help(subaction)
                        if subaction.help and action.help != argparse.SUPPRESS
                        else ""
                    )
                    help = help.split("\n")[0]
                    subcommands.append(Subcommand(subparser, subaction.dest, help))

                    # Look for aliases of the form 'name (alias, ...)'
                    if self.aliases and isinstance(subaction.metavar, str):
                        match = re.match(r"(.*) \((.*)\)", subaction.metavar)
                        if match:
                            aliases = match.group(2).split(", ")
                            for alias in aliases:
                                subparser = action._name_parser_map[alias]
                                help = (
                                    self._expand_help(subaction)
                                    if subaction.help and action.help != argparse.SUPPRESS
                                    else ""
                                )
                                help = help.split("\n")[0]
                                subcommands.append(Subcommand(subparser, alias, help))
            else:
                name = fmt._format_action_invocation(action)
                help = (
                    self._expand_help(action)
                    if action.help and action.help != argparse.SUPPRESS
                    else ""
                )
                help = help.split("\n")[0]
                positionals.append(Positional(name, action.choices, action.nargs, help))

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

        for subcommand in cmd.subcommands:
            self._write(subcommand.parser, subcommand.name, level=level + 1)

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
            for positional in cmd.positionals:
                string.write(self.positional(positional.name, positional.help))
            string.write(self.end_positionals())

        if cmd.optionals:
            string.write(self.begin_optionals())
            for option in cmd.optionals:
                string.write(self.optional(option.dest_flags, option.help))
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

""".format(prog.replace(" ", "-"), prog, self.rst_levels[self.level] * len(prog))

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

""".format(usage)

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
``{0}``
  {1}

""".format(name, help)

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

""".format(opts, help)

    def end_optionals(self) -> str:
        """Text to print after optional arguments.

        Returns:
            Optional arguments footer.
        """
        return ""

    def begin_subcommands(self, subcommands: List[Subcommand]) -> str:
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

        for subcommand in subcommands:
            full_prog = subcommand.parser.prog
            prog = re.sub(r"^[^ ]* ", "", full_prog)
            string += "   * :ref:`{0} <{1}>`\n".format(prog, full_prog.replace(" ", "-"))

        return string + "\n"

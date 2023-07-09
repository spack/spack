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
from typing import IO, Any, Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union

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
    },
    "fish": {
        "aliases": True,
        "format": "fish",
        "header": os.path.join(spack.paths.share_path, "fish", "spack-completion.in"),
        "update": os.path.join(spack.paths.share_path, "spack-completion.fish"),
    },
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


# Map argument destination names to their complete commands
# Earlier items in the list have higher precedence
_dest_to_fish_complete = {
    ("activate", r"view"): '-f -a "(__fish_complete_directories)"',
    ("bootstrap root", r"path"): '-f -a "(__fish_complete_directories)"',
    ("mirror add", r"mirror"): "-f",
    ("repo add", r"path"): '-f -a "(__fish_complete_directories)"',
    ("test find", r"filter"): '-f -a "(__fish_spack_tests)"',
    ("bootstrap", r"name"): '-f -a "(__fish_spack_bootstrap_names)"',
    ("buildcache create", r"key"): '-f -a "(__fish_spack_gpg_keys)"',
    ("build-env", r"spec \[--\].*"): '-f -a "(__fish_spack_build_env_spec)"',
    ("checksum", r"package"): '-f -a "(__fish_spack_packages)"',
    (
        "checksum",
        r"versions",
    ): "-f -a '(__fish_spack_package_versions $__fish_spack_argparse_argv[1])'",
    ("config", r"path"): '-f -a "(__fish_spack_colon_path)"',
    ("config", r"section"): '-f -a "(__fish_spack_config_sections)"',
    ("develop", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("diff", r"specs?"): '-f -a "(__fish_spack_installed_specs)"',
    ("gpg sign", r"output"): '-f -a "(__fish_complete_directories)"',
    ("gpg", r"keys?"): '-f -a "(__fish_spack_gpg_keys)"',
    ("graph", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("help", r"help_command"): '-f -a "(__fish_spack_commands)"',
    ("install", r"specfiles"): '-f -a "(__fish_spack_yamls)"',
    ("list", r"filter"): '-f -a "(__fish_spack_packages)"',
    ("mirror", r"mirror"): '-f -a "(__fish_spack_mirrors)"',
    ("pkg", r"package"): '-f -a "(__fish_spack_pkg_packages)"',
    ("remove", r"specs?"): '-f -a "(__fish_spack_installed_specs)"',
    ("repo", r"namespace_or_path"): '$__fish_spack_force_files -a "(__fish_spack_repos)"',
    ("restage", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("rm", r"specs?"): '-f -a "(__fish_spack_installed_specs)"',
    ("solve", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("spec", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("stage", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("test-env", r"spec \[--\].*"): '-f -a "(__fish_spack_build_env_spec)"',
    ("test", r"\[?name.*"): '-f -a "(__fish_spack_tests)"',
    ("undevelop", r"specs?"): '-f -k -a "(__fish_spack_specs_or_id)"',
    ("verify", r"specs_or_files"): '$__fish_spack_force_files -a "(__fish_spack_installed_specs)"',
    ("view", r"path"): '-f -a "(__fish_complete_directories)"',
    ("", r"comment"): "-f",
    ("", r"compiler_spec"): '-f -a "(__fish_spack_installed_compilers)"',
    ("", r"config_scopes"): '-f -a "(__fish_complete_directories)"',
    ("", r"sorted_profile"): '-f -a "calls ncalls cumtime cumulative filename line module"',
    ("", r"extendable"): '-f -a "(__fish_spack_extensions)"',
    ("", r"installed_specs?"): '-f -a "(__fish_spack_installed_specs)"',
    ("", r"job_url"): "-f",
    ("", r"location_env"): '-f -a "(__fish_complete_directories)"',
    ("", r"pytest_args"): '-f -a "(__fish_spack_unit_tests)"',
    ("", r"package_or_file"): '$__fish_spack_force_files -a "(__fish_spack_packages)"',
    ("", r"package_or_user"): '-f -a "(__fish_spack_packages)"',
    ("", r"package"): '-f -a "(__fish_spack_packages)"',
    ("", r"PKG"): '-f -a "(__fish_spack_packages)"',
    ("", r"prefix"): '-f -a "(__fish_complete_directories)"',
    ("", r"rev\d?"): '-f -a "(__fish_spack_git_rev)"',
    ("", r"specs?"): '-f -k -a "(__fish_spack_specs)"',
    ("", r"tags?"): '-f -a "(__fish_spack_tags)"',
    ("", r"virtual_package"): '-f -a "(__fish_spack_providers)"',
    ("", r"working_dir"): '-f -a "(__fish_complete_directories)"',
    ("", r"(\w*_)?env"): '-f -a "(__fish_spack_environments)"',
    ("", r"(\w*_)?dir(ectory)?"): '-f -a "(__fish_spack_environments)"',
    ("", r"(\w*_)?mirror_name"): '-f -a "(__fish_spack_mirrors)"',
}


def _fish_dest_get_complete(prog: str, dest: str) -> Optional[str]:
    """Map from subcommand to autocompletion argument.

    Args:
        prog: Program name.
        dest: Destination.

    Returns:
        Autocompletion argument.
    """
    s = prog.split(None, 1)
    subcmd = s[1] if len(s) == 2 else ""

    for (prog_key, pos_key), value in _dest_to_fish_complete.items():
        if subcmd.startswith(prog_key) and re.match("^" + pos_key + "$", dest):
            return value
    return None


class FishCompletionWriter(ArgparseCompletionWriter):
    """Write argparse output as bash programmable tab completion."""

    def format(self, cmd: Command) -> str:
        """Return the string representation of a single node in the parser tree.

        Args:
            cmd: Parsed information about a command or subcommand.

        Returns:
            String representation of a node.
        """
        assert cmd.optionals  # we should always at least have -h, --help
        assert not (cmd.positionals and cmd.subcommands)  # one or the other

        # We also need help messages and how arguments are used
        # So we pass everything to completion writer
        positionals = cmd.positionals
        optionals = cmd.optionals
        subcommands = cmd.subcommands

        return (
            self.prog_comment(cmd.prog)
            + self.optspecs(cmd.prog, optionals)
            + self.complete(cmd.prog, positionals, optionals, subcommands)
        )

    def optspecs(
        self,
        prog: str,
        optionals: List[Tuple[Sequence[str], List[str], str, Union[int, str, None], str]],
    ) -> str:
        """Read the optionals and return the command to set optspec.

        Args:
            prog: Program name.
            optionals: List of optional arguments.

        Returns:
            Command to set optspec variable.
        """
        # Variables of optspecs
        optspec_var = "__fish_spack_optspecs_" + prog.replace(" ", "_").replace("-", "_")

        if optionals is None:
            return "set -g %s\n" % optspec_var

        # Build optspec by iterating over options
        args = []

        # Record not actually supported options
        comment = ""

        for flags, dest, _, nargs, _ in optionals:
            if len(flags) == 0:
                continue

            required = ""

            # Because nargs '?' is treated differently in fish,
            # we treat it as required.
            # Also, because multi-argument options are not supported,
            # we treat it like one argument and leave a comment.
            if nargs == 0:
                pass
            elif nargs in [1, None, "?"]:
                required = "="
            else:
                required = "="
                comment += "\n# TODO: %s -> %r: %r not supported" % (flags, dest, nargs)

            # Pair short options with long options

            # We need to do this because fish doesn't support multiple short
            # or long options.
            # However, since we are paring options only, this is fine

            short = [f[1:] for f in flags if f.startswith("-") and len(f) == 2]
            long = [f[2:] for f in flags if f.startswith("--")]

            while len(short) > 0 and len(long) > 0:
                arg = "%s/%s%s" % (short.pop(), long.pop(), required)
            while len(short) > 0:
                arg = "%s/%s" % (short.pop(), required)
            while len(long) > 0:
                arg = "%s%s" % (long.pop(), required)

            args.append(arg)

        # Even if there is no option, we still set variable.
        # In fish such variable is an empty array, we use it to
        # indicate that such subcommand exists.
        args = " ".join(args)

        return "set -g %s %s\n" % (optspec_var, args)

    @staticmethod
    def is_iterable(arg: Any) -> bool:
        """Check if a variable is iterable.

        Args:
            arg: Variable to check.

        Returns:
            True if variable is iterable, else False.
        """
        return isinstance(arg, (list, tuple, set, frozenset))

    @staticmethod
    def complete_head(prog: str, positional: Optional[str] = None) -> str:
        """Return the head of the completion command.

        Args:
            prog: Program name.
            positionals: Optional positional argument.

        Returns:
            Head of the completion command.
        """
        # Split command and subcommand
        s = prog.split(None, 1)
        subcmd = s[1] if len(s) == 2 else ""

        if positional is None:
            return 'complete -c %s -n "__fish_spack_using_command %s"' % (s[0], subcmd)
        else:
            ret = 'complete -c %s -n "__fish_spack_using_command_pos %d %s"'
            return ret % (s[0], positional, subcmd)

    def complete(
        self,
        prog: str,
        positionals: List[Tuple[str, Optional[Iterable[Any]], Union[int, str, None], str]],
        optionals: List[Tuple[Sequence[str], List[str], str, Union[int, str, None], str]],
        subcommands: List[Tuple[ArgumentParser, str, Optional[str]]],
    ) -> str:
        """Return all the completion commands.

        Args:
            prog: Program name.
            positionals: List of positional arguments.
            optionals: List of optional arguments.
            subcommands: List of subcommand parsers.

        Returns:
            Completion command.
        """
        commands = []

        if positionals:
            commands.append(self.positionals(prog, positionals))

        if subcommands:
            commands.append(self.subcommands(prog, subcommands))

        if optionals:
            commands.append(self.optionals(prog, optionals))

        return "".join(commands)

    def positionals(
        self,
        prog: str,
        positionals: List[Tuple[str, Optional[Iterable[Any]], Union[int, str, None], str]],
    ) -> str:
        """Return the completion for positional arguments.

        Args:
            prog: Program name.
            positionals: List of positional arguments.

        Returns:
            Completion command.
        """
        commands = []

        for idx, (args, choices, nargs, help) in enumerate(positionals):
            # Make sure we always get same order of output
            if isinstance(choices, dict):
                choices = sorted(choices.keys())
            elif isinstance(choices, (set, frozenset)):
                choices = sorted(choices)

            commands.append("# %d -> %s %r (%s): %r" % (idx, args, choices, help, nargs))

            head = self.complete_head(prog, idx if nargs != "..." else None)

            if self.is_iterable(choices):
                # If there are choices, we provide a completion for all
                # possible values
                choices = " ".join(choices)
                commands.append(head + ' -f -a "%s"' % choices)
            else:
                # Otherwise, we try to find a predefined completion for it
                value = _fish_dest_get_complete(prog, args)
                if value is not None:
                    commands.append(head + " " + value)

        return "\n".join(commands) + "\n"

    def prog_comment(self, prog: str) -> str:
        """Return a comment line for the command.

        Args:
            prog: Program name.

        Returns:
            Comment line.
        """
        return "\n# %s\n" % prog

    def optionals(
        self,
        prog: str,
        optionals: List[Tuple[Sequence[str], List[str], str, Union[int, str, None], str]],
    ) -> str:
        """Return the completion for optional arguments.

        Args:
            prog: Program name.
            optionals: List of optional arguments.

        Returns:
            Completion command.
        """
        commands = []
        head = self.complete_head(prog)

        for flags, dest, _, nargs, help in optionals:
            # Make sure we always get same order of output
            if isinstance(dest, dict):
                dest = sorted(dest.keys())
            elif isinstance(dest, (set, frozenset)):
                dest = sorted(dest)

            commands.append("# %s -> %r: %r" % (flags, dest, nargs))

            # To provide description for optionals, and also possible values,
            # we need to use two split completion command.
            # Otherwise, each option will have same description.
            prefix = head

            # Add all flags to the completion
            for f in flags:
                if f.startswith("--"):
                    long = f[2:]
                    prefix += " -l %s" % long
                elif f.startswith("-"):
                    short = f[1:]
                    assert len(short) == 1
                    prefix += " -s %s" % short

            # Check if option require argument
            # Currently multi-argument options are not supported,
            # so we treat it like one argument and leave a comment
            if nargs == 0:
                pass
            elif nargs in [1, None, "?"]:
                prefix += " -r"
            else:
                commands.append("# TODO: %s -> %r: %r not supported" % (flags, dest, nargs))
                prefix += " -r"

            if self.is_iterable(dest):
                # If there are choices, we provide a completion for all
                # possible values
                choices = " ".join(dest)
                commands.append(prefix + ' -f -a "%s"' % choices)
            else:
                # Otherwise, we try to find a predefined completion for it
                value = _fish_dest_get_complete(prog, dest)
                if value is not None:
                    commands.append(prefix + " " + value)

            if len(help) > 0:
                help = help.split("\n")[0]
                commands.append(prefix + ' -d "%s"' % help)

        return "\n".join(commands) + "\n"

    def subcommands(
        self, prog: str, subcommands: List[Tuple[ArgumentParser, str, Optional[str]]]
    ) -> str:
        """Return the completion for subcommands.

        Args:
            prog: Program name.
            subcommands: List of subcommand parsers.

        Returns:
            Completion command.
        """
        commands = []
        head = self.complete_head(prog, 0)

        for _, subcommand, help in subcommands:
            command = head + ' -f -a "%s"' % subcommand

            if help is not None and len(help) > 0:
                help = help.split("\n")[0]
                command += ' -d "%s"' % help

            commands.append(command)

        return "\n".join(commands) + "\n"


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


@formatter
def fish(args, out):
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    writer = FishCompletionWriter(parser.prog, out, args.aliases)
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

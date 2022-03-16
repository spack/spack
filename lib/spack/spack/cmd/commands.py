# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import copy
import os
import re
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.argparsewriter import (
    ArgparseCompletionWriter,
    ArgparseRstWriter,
    ArgparseWriter,
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
formatters = {}


#: standard arguments for updating completion scripts
#: we iterate through these when called with --update-completion
update_completion_args = {
    "bash":  {
        "aliases": True,
        "format": "bash",
        "header": os.path.join(
            spack.paths.share_path, "bash", "spack-completion.in"),
        "update": os.path.join(
            spack.paths.share_path, "spack-completion.bash"),
    },
}


def formatter(func):
    """Decorator used to register formatters"""
    formatters[func.__name__] = func
    return func


def setup_parser(subparser):
    subparser.add_argument(
        "--update-completion", action='store_true', default=False,
        help="regenerate spack's tab completion scripts")

    subparser.add_argument(
        '-a', '--aliases', action='store_true', default=False,
        help='include command aliases')
    subparser.add_argument(
        '--format', default='names', choices=formatters,
        help='format to be used to print the output (default: names)')
    subparser.add_argument(
        '--header', metavar='FILE', default=None, action='store',
        help='prepend contents of FILE to the output (useful for rst format)')
    subparser.add_argument(
        '--update', metavar='FILE', default=None, action='store',
        help='write output to the specified file, if any command is newer')
    subparser.add_argument(
        'rst_files', nargs=argparse.REMAINDER,
        help='list of rst files to search for `_cmd-spack-<cmd>` cross-refs')


class SpackArgparseRstWriter(ArgparseRstWriter):
    """RST writer tailored for spack documentation."""

    def __init__(self, prog, out=None, aliases=False,
                 documented_commands=[],
                 rst_levels=['-', '-', '^', '~', ':', '`']):
        out = sys.stdout if out is None else out
        super(SpackArgparseRstWriter, self).__init__(
            prog, out, aliases, rst_levels)
        self.documented = documented_commands

    def usage(self, *args):
        string = super(SpackArgparseRstWriter, self).usage(*args)

        cmd = self.parser.prog.replace(' ', '-')
        if cmd in self.documented:
            string += '\n:ref:`More documentation <cmd-{0}>`\n'.format(cmd)

        return string


class SubcommandWriter(ArgparseWriter):
    def format(self, cmd):
        return '    ' * self.level + cmd.prog + '\n'


_positional_to_subroutine = {
    'package': '_all_packages',
    'spec': '_all_packages',
    'filter': '_all_packages',
    'installed': '_installed_packages',
    'compiler': '_installed_compilers',
    'section': '_config_sections',
    'env': '_environments',
    'extendable': '_extensions',
    'keys': '_keys',
    'help_command': '_subcommands',
    'mirror': '_mirrors',
    'virtual': '_providers',
    'namespace': '_repos',
    'hash': '_all_resource_hashes',
    'pytest': '_unit_tests',
}


class BashCompletionWriter(ArgparseCompletionWriter):
    """Write argparse output as bash programmable tab completion."""

    def body(self, positionals, optionals, subcommands):
        if positionals:
            return """
    if $list_options
    then
        {0}
    else
        {1}
    fi
""".format(self.optionals(optionals), self.positionals(positionals))
        elif subcommands:
            return """
    if $list_options
    then
        {0}
    else
        {1}
    fi
""".format(self.optionals(optionals), self.subcommands(subcommands))
        else:
            return """
    {0}
""".format(self.optionals(optionals))

    def positionals(self, positionals):
        # If match found, return function name
        for positional in positionals:
            for key, value in _positional_to_subroutine.items():
                if positional.startswith(key):
                    return value

        # If no matches found, return empty list
        return 'SPACK_COMPREPLY=""'

    def optionals(self, optionals):
        return 'SPACK_COMPREPLY="{0}"'.format(' '.join(optionals))

    def subcommands(self, subcommands):
        return 'SPACK_COMPREPLY="{0}"'.format(' '.join(subcommands))


_dest_to_fish_complete = {
    ('spack activate', r'view'): '-f -a "(__fish_complete_directories)"',
    ('spack bootstrap root', r'path'): '-f -a "(__fish_complete_directories)"',
    ('spack mirror add', r'mirror'): '-f',
    ('spack repo add', r'path'): '-f -a "(__fish_complete_directories)"',
    ('spack test find', r'filter'): '-f -a "(__fish_spack_tests)"',
    ('spack bootstrap', r'name'): '-f -a "(__fish_spack_bootstrap_names)"',
    ('spack buildcache create', r'key'): '-f -a "(__fish_spack_gpg_keys)"',
    ('spack build-env', r'spec \[--\].*'): '-f -a "(__fish_spack_build_env_spec)"',
    ('spack checksum', r'package'): '-f -a "(__fish_spack_packages)"',
    ('spack checksum', r'versions'): "-f -a '(__fish_spack_package_versions $__fish_spack_argparse_argv[1])'",
    ('spack config', r'path'): '-f -a "(__fish_spack_colon_path)"',
    ('spack config', r'section'): '-f -a "(__fish_spack_config_sections)"',
    ('spack gpg', r'keys?'): '-f -a "(__fish_spack_gpg_keys)"',
    ('spack gpg sign', r'output'): '-f -a "(__fish_complete_directories)"',
    ('spack help', r'help_command'): '-f -a "(__fish_spack_commands)"',
    ('spack install', r'specfiles'): '-f -a "(__fish_spack_yamls)"',
    ('spack list', r'filter'): '-f -a "(__fish_spack_specs)"',
    ('spack mirror', r'mirror'): '-f -a "(__fish_spack_mirrors)"',
    ('spack pkg', r'package'): '-f -a "(__fish_spack_pkg_packages)"',
    ('spack repo', r'namespace_or_path'): '-F -a "(__fish_spack_repos)"',
    ('spack test-env', r'spec \[--\].*'): '-f -a "(__fish_spack_build_env_spec)"',
    ('spack test', r'\[?name.*'): '-f -a "(__fish_spack_tests)"',
    ('spack verify', r'specs_or_files'): '-F -a "(__fish_spack_installed_specs)"',
    ('spack view', r'path'): '-f -a "(__fish_complete_directories)"',
    ('', r'comment'): '-f',
    ('', r'compiler_spec'): '-f -a "(__fish_spack_installed_compilers)"',
    ('', r'config_scopes'): '-f -a "(__fish_complete_directories)"',
    ('', r'sorted-profile'): '-f -a "calls ncalls cumtime cumulative filename line module"',
    ('', r'extendable'): '-f -a "(__fish_spack_extensions)"',
    ('', r'installed_specs?'): '-f -a "(__fish_spack_installed_specs)"',
    ('', r'job_url'): '-f',
    ('', r'location_env'): '-f -a "(__fish_complete_directories)"',
    ('', r'pytest_args'): '-f -a "(__fish_spack_unit_tests)"',
    ('', r'package_or_file'): '-F -a "(__fish_spack_packages)"',
    ('', r'package_or_user'): '-f -a "(__fish_spack_packages)"',
    ('', r'package'): '-f -a "(__fish_spack_packages)"',
    ('', r'PKG'): '-f -a "(__fish_spack_packages)"',
    ('', r'prefix'): '-f -a "(__fish_complete_directories)"',
    ('', r'rev\d?'): '-f -a "(__fish_spack_git_rev)"',
    ('', r'scope'): '-f -a "(__fish_spack_scopes)"',
    ('', r'specs?'): '-f -a "(__fish_spack_specs)"',
    ('', r'tags?'): '-F -a "(__fish_spack_tags)"',
    ('', r'virtual_package'): '-f -a "(__fish_spack_providers)"',
    ('', r'working_dir'): '-f -a "(__fish_complete_directories)"',
    ('', r'(\w*_)?env'): '-f -a "(__fish_spack_environments)"',
    ('', r'(\w*_)?dir(ectory)?'): '-f -a "(__fish_spack_environments)"',
    ('', r'(\w*_)?mirror_name'): '-f -a "(__fish_spack_mirrors)"',
}

class FishCompletionWriter(ArgparseCompletionWriter):
    """Write argparse output as bash programmable tab completion."""
    # TODO: alias duplicate?

    def format(self, cmd):
        """Returns the string representation of a single node in the
        parser tree.

        Override this in subclasses to define how each subcommand
        should be displayed.

        Parameters:
            (Command): parsed information about a command or subcommand

        Returns:
            str: the string representation of this subcommand
        """

        assert cmd.optionals  # we should always at least have -h, --help
        assert not (cmd.positionals and cmd.subcommands)  # one or the other

        positionals = cmd.positionals
        optionals = cmd.optionals
        subcommands = cmd.subcommands
        head = self.complete_head(cmd.prog)

        return (self.prog_comment(cmd.prog) +
                self.optspecs(cmd.prog, optionals) +
                self.complete(cmd.prog, positionals, optionals, subcommands))

    def optspecs(self, prog, optionals):
        name = prog.replace(' ', '_').replace('-', '_')

        if optionals is None:
            return 'set -g __fish_spack_optspecs_%s\n' % name

        args = ''
        for (flags, dest, dest_flags, nargs, help) in optionals:
            if len(flags) == 0:
                continue
            required = ''
            match nargs:
                case 0:
                    pass
                # It's better to use required = '?' here, but that doesn't
                # work with fish.
                case 1 | None | '?':
                    required = '='
                case _:
                    return '# TODO: %s -> %r: %r not supported' % (flags, dest, nargs)

            short = [f[1:] for f in flags if f.startswith('-') and len(f) == 2]
            long = [f[2:] for f in flags if f.startswith('--')]

            while len(short) > 0 and len(long) > 0:
                arg = '"%s/%s%s"' % (short.pop(), long.pop(), required)
            while len(short) > 0:
                arg = '"%s/%s"' % (short.pop(), required)
            while len(long) > 0:
                arg = '"%s%s"' % (long.pop(), required)
            args += ' %s' % arg

        return 'set -g __fish_spack_optspecs_%s%s\n' % (name, args)

    def complete_head(self, prog, positional):
        s = prog.split(maxsplit=1)
        if positional is None:
            return 'complete -c %s -n "__fish_spack_using_command %s"' % (s[0], prog)
        else:
            return 'complete -c %s -n "__fish_spack_using_command_pos %d %s"' % (s[0], positional, prog)

    def complete(self, prog, positionals, optionals, subcommands):
        ret = ''

        if positionals:
            assert len(subcommands) == 0
            ret += self.positionals(prog, positionals)

        if subcommands:
            assert len(positionals) == 0
            ret += self.subcommands(prog, subcommands)

        if optionals:
            ret += self.optionals(prog, optionals)

        return ret

    def positionals(self, prog, positionals):
        string = ''

        for (idx, (positional, help, choices, nargs)) in enumerate(positionals):
            string += '# %d -> %s %r (%s): %r\n' % (idx, positional, choices, help, nargs)
            head = self.complete_head(prog, idx if nargs != '...' else None)
            if choices is not None:
                string += '%s -f -a "%s"\n' % (head, ' '.join(choices))
            else:
                for (prog_key, pos_key), value in _dest_to_fish_complete.items():
                    if prog.startswith(prog_key) and re.match('^' + pos_key + '$', positional):
                        string += '%s %s\n' % (head, value)
                        break
        return string

    def prog_comment(self, prog):
        return f"\n# {prog}\n"

    def optionals(self, prog, optionals):
        string = ''
        head = self.complete_head(prog)

        for (flags, dest, dest_flags, nargs, help) in optionals:
            string += '# %s -> %r: %r\n' % (flags, dest, nargs)
            prefix = head
            for f in flags:
                if f.startswith('--'):
                    long = f[2:]
                    prefix += ' -l %s' % long
                elif f.startswith('-'):
                    short = f[1:]
                    assert len(short) == 1
                    prefix += ' -s %s' % short
            match nargs:
                case 0:
                    pass
                case 1 | None | '?':
                    prefix += ' -r'
                case _:
                    return '# TODO: %s -> %r: %r not supported' % (flags, dest, nargs)

            if isinstance(dest, list):
                string += '%s -f -a "%s"\n' % (prefix, ' '.join(dest))
            else:
                for (prog_key, pos_key), value in _dest_to_fish_complete.items():
                    if prog.startswith(prog_key) and re.match('^' + pos_key + '$', dest):
                        string += '%s %s\n' % (prefix, value)
                        break

            if len(help) > 0:
                help = help.split("\n")[0]
                string += '%s -d "%s"\n' % (prefix, help)

        return string

    def subcommands(self, prog, subcommands):
        string = ''
        head = self.complete_head(prog, 0)

        for (subparser, command, help) in subcommands:
            string += head
            string += ' -f'
            string += ' -a %s' % command

            if help is not None and len(help) > 0:
                help = help.split("\n")[0]
                string += ' -d "%s"' % help
            string += '\n'

        return string


@formatter
def subcommands(args, out):
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)
    writer = SubcommandWriter(parser.prog, out, args.aliases)
    writer.write(parser)


def rst_index(out):
    out.write('\n')

    index = spack.main.index_commands()
    sections = index['long']

    dmax = max(len(section_descriptions.get(s, s)) for s in sections) + 2
    cmax = max(len(c) for _, c in sections.items()) + 60

    row = "%s  %s\n" % ('=' * dmax, '=' * cmax)
    line = '%%-%ds  %%s\n' % dmax

    out.write(row)
    out.write(line % (" Category ", " Commands "))
    out.write(row)
    for section, commands in sorted(sections.items()):
        description = section_descriptions.get(section, section)

        for i, cmd in enumerate(sorted(commands)):
            description = description.capitalize() if i == 0 else ''
            ref = ':ref:`%s <spack-%s>`' % (cmd, cmd)
            comma = ',' if i != len(commands) - 1 else ''
            bar = '| ' if i % 8 == 0 else '  '
            out.write(line % (description, bar + ref + comma))
    out.write(row)


@formatter
def rst(args, out):
    # create a parser with all commands
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    # extract cross-refs of the form `_cmd-spack-<cmd>:` from rst files
    documented_commands = set()
    for filename in args.rst_files:
        with open(filename) as f:
            for line in f:
                match = re.match(r'\.\. _cmd-(spack-.*):', line)
                if match:
                    documented_commands.add(match.group(1).strip())

    # print an index to each command
    rst_index(out)
    out.write('\n')

    # print sections for each command and subcommand
    writer = SpackArgparseRstWriter(
        parser.prog, out, args.aliases, documented_commands)
    writer.write(parser)


@formatter
def names(args, out):
    commands = copy.copy(spack.cmd.all_commands())

    if args.aliases:
        commands.extend(spack.main.aliases.keys())

    colify(commands, output=out)


@formatter
def bash(args, out):
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


def prepend_header(args, out):
    if not args.header:
        return

    with open(args.header) as header:
        out.write(header.read())


def _commands(parser, args):
    """This is the 'regular' command, which can be called multiple times.

    See ``commands()`` below for ``--update-completion`` handling.
    """
    formatter = formatters[args.format]

    # check header first so we don't open out files unnecessarily
    if args.header and not os.path.exists(args.header):
        tty.die("No such file: '%s'" % args.header)

    if args.update:
        tty.msg('Updating file: %s' % args.update)
        with open(args.update, 'w') as f:
            prepend_header(args, f)
            formatter(args, f)

        if args.update_completion:
            fs.set_executable(args.update)

    else:
        prepend_header(args, sys.stdout)
        formatter(args, sys.stdout)


def update_completion(parser, args):
    """Iterate through the shells and update the standard completion files.

    This is a convenience method to avoid calling this command many
    times, and to simplify completion update for developers.

    """
    for shell, shell_args in update_completion_args.items():
        for attr, value in shell_args.items():
            setattr(args, attr, value)
        _commands(parser, args)


def commands(parser, args):
    if args.update_completion:
        if args.format != 'names' or any([
                args.aliases, args.update, args.header
        ]):
            tty.die("--update-completion can only be specified alone.")

        # this runs the command multiple times with different arguments
        return update_completion(parser, args)

    else:
        # run commands normally
        return _commands(parser, args)

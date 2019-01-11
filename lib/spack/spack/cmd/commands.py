# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import sys
import re
import argparse

from llnl.util.argparsewriter import ArgparseWriter, ArgparseRstWriter

import spack.main
from spack.main import section_descriptions


description = "list available spack commands"
section = "developer"
level = "long"


#: list of command formatters
formatters = {}


def formatter(func):
    """Decorator used to register formatters"""
    formatters[func.__name__] = func
    return func


def setup_parser(subparser):
    subparser.add_argument(
        '--format', default='names', choices=formatters,
        help='format to be used to print the output (default: names)')
    subparser.add_argument(
        'documented_commands', nargs=argparse.REMAINDER,
        help='list of documented commands to cross-references')


class SpackArgparseRstWriter(ArgparseRstWriter):
    """RST writer tailored for spack documentation."""

    def __init__(self, documented_commands, out=sys.stdout):
        super(SpackArgparseRstWriter, self).__init__(out)
        self.documented = documented_commands if documented_commands else []

    def usage(self, *args):
        super(SpackArgparseRstWriter, self).usage(*args)
        cmd = re.sub(' ', '-', self.parser.prog)
        if cmd in self.documented:
            self.line()
            self.line(':ref:`More documentation <cmd-%s>`' % cmd)


class SubcommandWriter(ArgparseWriter):
    def begin_command(self, prog):
        print('    ' * self.level + prog)


@formatter
def subcommands(args):
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)
    SubcommandWriter().write(parser)


def rst_index(out=sys.stdout):
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
def rst(args):
    # print an index to each command
    rst_index()
    print()

    # create a parser with all commands
    parser = spack.main.make_argument_parser()
    spack.main.add_all_commands(parser)

    # get documented commands from the command line
    documented_commands = set(args.documented_commands)

    # print sections for each command and subcommand
    SpackArgparseRstWriter(documented_commands).write(parser, root=1)


@formatter
def names(args):
    for cmd in spack.cmd.all_commands():
        print(cmd)


def commands(parser, args):

    # Print to stdout
    formatters[args.format](args)
    return

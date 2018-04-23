##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function
import re
import argparse
import errno
import sys


class ArgparseWriter(object):
    """Analyzes an argparse ArgumentParser for easy generation of help."""
    def __init__(self):
        self.level = 0

    def _write(self, parser, root=True, level=0):
        self.parser = parser
        self.level = level
        actions = parser._actions

        # allow root level to be flattened with rest of commands
        if type(root) == int:
            self.level = root
            root = True

        # go through actions and split them into optionals, positionals,
        # and subcommands
        optionals = []
        positionals = []
        subcommands = []
        for action in actions:
            if action.option_strings:
                optionals.append(action)
            elif isinstance(action, argparse._SubParsersAction):
                for subaction in action._choices_actions:
                    subparser = action._name_parser_map[subaction.dest]
                    subcommands.append(subparser)
            else:
                positionals.append(action)

        groups = parser._mutually_exclusive_groups
        fmt = parser._get_formatter()
        description = parser.description

        def action_group(function, actions):
            for action in actions:
                arg = fmt._format_action_invocation(action)
                help = action.help if action.help else ''
                function(arg, re.sub('\n', ' ', help))

        if root:
            self.begin_command(parser.prog)

            if description:
                self.description(parser.description)

            usage = fmt._format_usage(None, actions, groups, '').strip()
            self.usage(usage)

            if positionals:
                self.begin_positionals()
                action_group(self.positional, positionals)
                self.end_positionals()

            if optionals:
                self.begin_optionals()
                action_group(self.optional, optionals)
                self.end_optionals()

        if subcommands:
            self.begin_subcommands(subcommands)
            for subparser in subcommands:
                self._write(subparser, root=True, level=level + 1)
            self.end_subcommands(subcommands)

        if root:
            self.end_command(parser.prog)

    def write(self, parser, root=True):
        """Write out details about an ArgumentParser.

        Args:
            parser (ArgumentParser): an ``argparse`` parser
            root (bool or int): if bool, whether to include the root parser;
                or ``1`` to flatten the root parser with first-level
                subcommands
        """
        try:
            self._write(parser, root, level=0)
        except IOError as e:
            # swallow pipe errors
            if e.errno != errno.EPIPE:
                raise

    def begin_command(self, prog):
        pass

    def end_command(self, prog):
        pass

    def description(self, description):
        pass

    def usage(self, usage):
        pass

    def begin_positionals(self):
        pass

    def positional(self, name, help):
        pass

    def end_positionals(self):
        pass

    def begin_optionals(self):
        pass

    def optional(self, option, help):
        pass

    def end_optionals(self):
        pass

    def begin_subcommands(self, subcommands):
        pass

    def end_subcommands(self, subcommands):
        pass


_rst_levels = ['=', '-', '^', '~', ':', '`']


class ArgparseRstWriter(ArgparseWriter):
    """Write argparse output as rst sections."""

    def __init__(self, out=sys.stdout, rst_levels=_rst_levels,
                 strip_root_prog=True):
        """Create a new ArgparseRstWriter.

        Args:
            out (file object): file to write to
            rst_levels (list of str): list of characters
                for rst section headings
            strip_root_prog (bool): if ``True``, strip the base command name
                from subcommands in output
        """
        super(ArgparseWriter, self).__init__()
        self.out = out
        self.rst_levels = rst_levels
        self.strip_root_prog = strip_root_prog

    def line(self, string=''):
        self.out.write('%s\n' % string)

    def begin_command(self, prog):
        self.line()
        self.line('----')
        self.line()
        self.line('.. _%s:\n' % prog.replace(' ', '-'))
        self.line('%s' % prog)
        self.line(self.rst_levels[self.level] * len(prog) + '\n')

    def description(self, description):
        self.line('%s\n' % description)

    def usage(self, usage):
        self.line('.. code-block:: console\n')
        self.line('    %s\n' % usage)

    def begin_positionals(self):
        self.line()
        self.line('**Positional arguments**\n')

    def positional(self, name, help):
        self.line(name)
        self.line('  %s\n' % help)

    def begin_optionals(self):
        self.line()
        self.line('**Optional arguments**\n')

    def optional(self, opts, help):
        self.line('``%s``' % opts)
        self.line('  %s\n' % help)

    def begin_subcommands(self, subcommands):
        self.line()
        self.line('**Subcommands**\n')
        self.line('.. hlist::')
        self.line('   :columns: 4\n')

        for cmd in subcommands:
            prog = cmd.prog
            if self.strip_root_prog:
                prog = re.sub(r'^[^ ]* ', '', prog)

            self.line('   * :ref:`%s <%s>`'
                      % (prog, cmd.prog.replace(' ', '-')))
        self.line()

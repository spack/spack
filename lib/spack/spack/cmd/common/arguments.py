##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import argparse

import spack.store
import spack.modules
from spack.util.pattern import Args
__all__ = ['add_common_arguments']

_arguments = {}


def add_common_arguments(parser, list_of_arguments):
    for argument in list_of_arguments:
        if argument not in _arguments:
            message = 'Trying to add non existing argument "{0}" to a command'
            raise KeyError(message.format(argument))
        x = _arguments[argument]
        parser.add_argument(*x.flags, **x.kwargs)


class ConstraintAction(argparse.Action):
    """Constructs a list of specs based on a constraint given on the command line

    An instance of this class is supposed to be used as an argument action
    in a parser. It will read a constraint and will attach a function to the
    arguments that accepts optional keyword arguments.

    To obtain the specs from a command the function must be called.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Query specs from command line
        self.values = values
        namespace.contraint = values
        namespace.specs = self._specs

    def _specs(self, **kwargs):
        specs = [s for s in spack.store.db.query(**kwargs)]
        values = ' '.join(self.values)
        if values:
            specs = [x for x in specs if x.satisfies(values, strict=True)]
        return specs


_arguments['constraint'] = Args(
    'constraint', nargs='*', action=ConstraintAction,
    help='Constraint to select a subset of installed packages')

_arguments['module_type'] = Args(
    '-m', '--module-type', help='Type of module files',
    default='tcl', choices=spack.modules.module_types)

_arguments['yes_to_all'] = Args(
    '-y', '--yes-to-all', action='store_true', dest='yes_to_all',
    help='Assume "yes" is the answer to every confirmation request.')

_arguments['recurse_dependencies'] = Args(
    '-r', '--dependencies', action='store_true', dest='recurse_dependencies',
    help='Recursively traverse spec dependencies')

_arguments['clean'] = Args(
    '--clean', action='store_false', dest='dirty',
    help='Clean environment before installing package.')

_arguments['dirty'] = Args(
    '--dirty', action='store_true', dest='dirty',
    help='Do NOT clean environment before installing.')

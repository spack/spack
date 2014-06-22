##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse

from pprint import pprint

import llnl.util.tty as tty
from llnl.util.tty.colify import colify
from llnl.util.lang import index_by

import spack.compilers
import spack.spec
import spack.config
from spack.compilation import get_path

description = "Manage compilers"

def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='compiler_command')

    update_parser = sp.add_parser(
        'add', help='Add compilers to the Spack configuration.')
    update_parser.add_argument('add_paths', nargs=argparse.REMAINDER)

    remove_parser = sp.add_parser('remove', help='remove compiler')
    remove_parser.add_argument('path')

    list_parser   = sp.add_parser('list', help='list available compilers')


def compiler_add(args):
    paths = args.add_paths
    if not paths:
        paths = get_path('PATH')

    compilers = spack.compilers.find_compilers(*args.add_paths)
    spack.compilers.add_compilers_to_config('user', *compilers)


def compiler_remove(args):
    pass


def compiler_list(args):
    tty.msg("Available compilers")

    index = index_by(spack.compilers.all_compilers(), 'name')
    for name, compilers in index.items():
        tty.hline(name, char='-', color=spack.spec.compiler_color)
        colify(reversed(sorted(compilers)), indent=4)


def compiler(parser, args):
    action = { 'add'    : compiler_add,
               'remove' : compiler_remove,
               'list'   : compiler_list }
    action[args.compiler_command](args)


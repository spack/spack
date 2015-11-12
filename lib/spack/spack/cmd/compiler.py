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

import llnl.util.tty as tty
from llnl.util.tty.color import colorize
from llnl.util.tty.colify import colify
from llnl.util.lang import index_by

import spack.compilers
import spack.spec
import spack.config
from spack.util.environment import get_path
from spack.spec import CompilerSpec

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

    info_parser   = sp.add_parser('info', help='Show compiler paths.')
    info_parser.add_argument('compiler_spec')


def compiler_add(args):
    """Search either $PATH or a list of paths for compilers and add them
       to Spack's configuration."""
    paths = args.add_paths
    if not paths:
        paths = get_path('PATH')

    compilers = [c for c in spack.compilers.find_compilers(*args.add_paths)
                 if c.spec not in spack.compilers.all_compilers()]

    if compilers:
        spack.compilers.add_compilers_to_config('user', *compilers)
        n = len(compilers)
        tty.msg("Added %d new compiler%s to %s" % (
            n, 's' if n > 1 else '', spack.config.get_config_scope_filename('user', 'compilers')))
        colify(reversed(sorted(c.spec for c in compilers)), indent=4)
    else:
        tty.msg("Found no new compilers")


def compiler_remove(args):
    pass


def compiler_info(args):
    """Print info about all compilers matching a spec."""
    cspec = CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec)

    if not compilers:
        tty.error("No compilers match spec %s." % cspec)
    else:
        for c in compilers:
            print str(c.spec) + ":"
            print "\tcc  = %s" % c.cc
            print "\tcxx = %s" % c.cxx
            print "\tf77 = %s" % c.f77
            print "\tfc  = %s" % c.fc


def compiler_list(args):
    tty.msg("Available compilers")
    index = index_by(spack.compilers.all_compilers(), 'name')
    for i, (name, compilers) in enumerate(index.items()):
        if i >= 1: print

        cname = "%s{%s}" % (spack.spec.compiler_color, name)
        tty.hline(colorize(cname), char='-')
        colify(reversed(sorted(compilers)))


def compiler(parser, args):
    action = { 'add'    : compiler_add,
               'remove' : compiler_remove,
               'info'   : compiler_info,
               'list'   : compiler_list }
    action[args.compiler_command](args)

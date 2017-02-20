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
import sys

import llnl.util.tty as tty
import spack.compilers
import spack.config
import spack.spec
from llnl.util.lang import index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize
from spack.spec import CompilerSpec, ArchSpec
from spack.util.environment import get_path

description = "manage compilers"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='compiler_command')

    scopes = spack.config.config_scopes

    # Find
    find_parser = sp.add_parser(
        'find', aliases=['add'],
        help='search the system for compilers to add to Spack configuration')
    find_parser.add_argument('add_paths', nargs=argparse.REMAINDER)
    find_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_modify_scope,
        help="configuration scope to modify")

    # Remove
    remove_parser = sp.add_parser(
        'remove', aliases=['rm'], help='remove compiler by spec')
    remove_parser.add_argument(
        '-a', '--all', action='store_true',
        help='remove ALL compilers that match spec')
    remove_parser.add_argument('compiler_spec')
    remove_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_modify_scope,
        help="configuration scope to modify")

    # List
    list_parser = sp.add_parser('list', help='list available compilers')
    list_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_list_scope,
        help="configuration scope to read from")

    # Info
    info_parser = sp.add_parser('info', help='show compiler paths')
    info_parser.add_argument('compiler_spec')
    info_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_list_scope,
        help="configuration scope to read from")


def compiler_find(args):
    """Search either $PATH or a list of paths OR MODULES for compilers and
       add them to Spack's configuration.

    """
    paths = args.add_paths
    if not paths:
        paths = get_path('PATH')

    # Don't initialize compilers config via compilers.get_compiler_config.
    # Just let compiler_find do the
    # entire process and return an empty config from all_compilers
    # Default for any other process is init_config=True
    compilers = [c for c in spack.compilers.find_compilers(*paths)]
    new_compilers = []
    for c in compilers:
        arch_spec = ArchSpec(None, c.operating_system, c.target)
        same_specs = spack.compilers.compilers_for_spec(c.spec,
                                                        arch_spec,
                                                        args.scope)

        if not same_specs:
            new_compilers.append(c)

    if new_compilers:
        spack.compilers.add_compilers_to_config(new_compilers,
                                                scope=args.scope,
                                                init_config=False)
        n = len(new_compilers)
        s = 's' if n > 1 else ''
        filename = spack.config.get_config_filename(args.scope, 'compilers')
        tty.msg("Added %d new compiler%s to %s" % (n, s, filename))
        colify(reversed(sorted(c.spec for c in new_compilers)), indent=4)
    else:
        tty.msg("Found no new compilers")


def compiler_remove(args):
    cspec = CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)
    if not compilers:
        tty.die("No compilers match spec %s" % cspec)
    elif not args.all and len(compilers) > 1:
        tty.error("Multiple compilers match spec %s. Choose one:" % cspec)
        colify(reversed(sorted([c.spec for c in compilers])), indent=4)
        tty.msg("Or, use `spack compiler remove -a` to remove all of them.")
        sys.exit(1)

    for compiler in compilers:
        spack.compilers.remove_compiler_from_config(
            compiler.spec, scope=args.scope)
        tty.msg("Removed compiler %s" % compiler.spec)


def compiler_info(args):
    """Print info about all compilers matching a spec."""
    cspec = CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)

    if not compilers:
        tty.error("No compilers match spec %s" % cspec)
    else:
        for c in compilers:
            print str(c.spec) + ":"
            print "\tpaths:"
            for cpath in ['cc', 'cxx', 'f77', 'fc']:
                print "\t\t%s = %s" % (cpath, getattr(c, cpath, None))
            if c.flags:
                print "\tflags:"
                for flag, flag_value in c.flags.iteritems():
                    print "\t\t%s = %s" % (flag, flag_value)
            if len(c.environment) != 0:
                if len(c.environment['set']) != 0:
                    print "\tenvironment:"
                    print "\t    set:"
                    for key, value in c.environment['set'].iteritems():
                        print "\t        %s = %s" % (key, value)
            if c.extra_rpaths:
                print "\tExtra rpaths:"
                for extra_rpath in c.extra_rpaths:
                    print "\t\t%s" % extra_rpath
            print "\tmodules  = %s" % c.modules
            print "\toperating system  = %s" % c.operating_system


def compiler_list(args):
    tty.msg("Available compilers")
    index = index_by(spack.compilers.all_compilers(scope=args.scope), 'name')
    for i, (name, compilers) in enumerate(index.items()):
        if i >= 1:
            print

        cname = "%s{%s}" % (spack.spec.compiler_color, name)
        tty.hline(colorize(cname), char='-')
        colify(reversed(sorted(compilers)))


def compiler(parser, args):
    action = {'add': compiler_find,
              'find': compiler_find,
              'remove': compiler_remove,
              'rm': compiler_remove,
              'info': compiler_info,
              'list': compiler_list}
    action[args.compiler_command](args)

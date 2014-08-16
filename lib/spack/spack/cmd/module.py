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
import sys
import os
import shutil
import argparse

import llnl.util.tty as tty
from llnl.util.lang import partition_list
from llnl.util.filesystem import mkdirp

import spack.cmd
import spack.modules
from spack.util.string import *

from spack.spec import Spec

description ="Manipulate modules and dotkits."

module_types = {
    'dotkit' : spack.modules.Dotkit,
    'tcl'    : spack.modules.TclModule
}


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='module_command')

    refresh_parser = sp.add_parser('refresh', help='Regenerate all module files.')

    find_parser = sp.add_parser('find', help='Find module files for packages.')
    find_parser.add_argument(
        'module_type', help="Type of module to find file for. [" + '|'.join(module_types) + "]")
    find_parser.add_argument('spec', nargs='+', help='spec to find a module file for.')


def module_find(mtype, spec_array):
    specs = spack.cmd.parse_specs(spec_array)
    if len(specs) > 1:
        tty.die("You can only pass one spec.")
    spec = specs[0]

    if not spack.db.exists(spec.name):
        tty.die("No such package: %s" % spec.name)

    if mtype not in module_types:
        tty.die("Invalid module type: '%s'.  Options are " + comma_and(module_types))

    specs = [s for s in spack.db.installed_package_specs() if s.satisfies(spec)]
    if len(specs) == 0:
        tty.die("No installed packages match spec %s" % spec)

    if len(specs) > 1:
        tty.error("Multiple matches for spec %s.  Choose one:" % spec)
        for s in specs:
            sys.stderr.write(s.tree(color=True))
        sys.exit(1)

    mt = module_types[mtype]
    mod = mt(spec.package)
    if not os.path.isfile(mod.file_name):
        tty.die("No dotkit is installed for package %s." % spec)

    print mod.file_name


def module_refresh():
    shutil.rmtree(spack.dotkit_path, ignore_errors=False)
    mkdirp(spack.dotkit_path)

    specs = spack.db.installed_package_specs()
    for spec in specs:
        for mt in module_types:
            mt(spec.package).write()


def module(parser, args):
    if args.module_command == 'refresh':
        module_refresh()

    elif args.module_command == 'find':
        module_find(args.module_type, args.spec)

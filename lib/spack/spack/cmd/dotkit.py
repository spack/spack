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
import spack.hooks.dotkit
from spack.spec import Spec


description ="Find dotkits for packages if they exist."

def setup_parser(subparser):
    subparser.add_argument(
        '--refresh', action='store_true', help='Regenerate all dotkits')

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER, help='spec to find a dotkit for.')


def dotkit_find(parser, args):
    if not args.spec:
        parser.parse_args(['dotkit', '-h'])

    spec = spack.cmd.parse_specs(args.spec)
    if len(spec) > 1:
        tty.die("You can only pass one spec.")
    spec = spec[0]

    if not spack.db.exists(spec.name):
        tty.die("No such package: %s" % spec.name)

    specs = [s for s in spack.db.installed_package_specs() if s.satisfies(spec)]

    if len(specs) == 0:
        tty.die("No installed packages match spec %s" % spec)

    if len(specs) > 1:
        tty.error("Multiple matches for spec %s.  Choose one:" % spec)
        for s in specs:
            sys.stderr.write(s.tree(color=True))
        sys.exit(1)

    match = specs[0]
    if not os.path.isfile(spack.hooks.dotkit.dotkit_file(match.package)):
        tty.die("No dotkit is installed for package %s." % spec)

    print match.format('$_$@$+$%@$=$#')


def dotkit_refresh(parser, args):
    query_specs = spack.cmd.parse_specs(args.spec)

    specs = spack.db.installed_package_specs()
    if query_specs:
        specs = [s for s in specs
                 if any(s.satisfies(q) for q in query_specs)]
    else:
        shutil.rmtree(spack.dotkit_path, ignore_errors=False)
        mkdirp(spack.dotkit_path)

    for spec in specs:
        spack.hooks.dotkit.post_install(spec.package)



def dotkit(parser, args):
    if args.refresh:
        dotkit_refresh(parser, args)
    else:
        dotkit_find(parser, args)

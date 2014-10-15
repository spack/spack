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
import os
import sys
from datetime import datetime

from external import argparse
import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack
import spack.cmd
import spack.config
import spack.mirror
from spack.spec import Spec
from spack.error import SpackError

description = "Manage mirrors."

def setup_parser(subparser):
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check fetched packages against checksum")

    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='mirror_command')

    create_parser = sp.add_parser('create', help=mirror_create.__doc__)
    create_parser.add_argument('-d', '--directory', default=None,
                               help="Directory in which to create mirror.")
    create_parser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="Specs of packages to put in mirror")
    create_parser.add_argument(
        '-f', '--file', help="File with specs of packages to put in mirror.")

    add_parser = sp.add_parser('add', help=mirror_add.__doc__)
    add_parser.add_argument('name', help="Mnemonic name for mirror.")
    add_parser.add_argument(
        'url', help="URL of mirror directory created by 'spack mirror create'.")

    remove_parser = sp.add_parser('remove', help=mirror_remove.__doc__)
    remove_parser.add_argument('name')

    list_parser = sp.add_parser('list', help=mirror_list.__doc__)


def mirror_add(args):
    """Add a mirror to Spack."""
    config = spack.config.get_config('user')
    config.set_value('mirror', args.name, 'url', args.url)
    config.write()


def mirror_remove(args):
    """Remove a mirror by name."""
    config = spack.config.get_config('user')
    name = args.name

    if not config.has_named_section('mirror', name):
        tty.die("No such mirror: %s" % name)
    config.remove_named_section('mirror', name)
    config.write()


def mirror_list(args):
    """Print out available mirrors to the console."""
    config = spack.config.get_config()
    sec_names = config.get_section_names('mirror')

    if not sec_names:
        tty.msg("No mirrors configured.")
        return

    max_len = max(len(s) for s in sec_names)
    fmt = "%%-%ds%%s" % (max_len + 4)

    for name in sec_names:
        val = config.get_value('mirror', name, 'url')
        print fmt % (name, val)


def _read_specs_from_file(filename):
    with closing(open(filename, "r")) as stream:
        for i, string in enumerate(stream):
            try:
                s = Spec(string)
                s.package
                args.specs.append(s)
            except SpackError, e:
                tty.die("Parse error in %s, line %d:" % (args.file, i+1),
                        ">>> " + string, str(e))


def mirror_create(args):
    """Create a directory to be used as a spack mirror, and fill it with
       package archives."""
    # try to parse specs from the command line first.
    specs = spack.cmd.parse_specs(args.specs)

    # If there is a file, parse each line as a spec and add it to the list.
    if args.file:
        if specs:
            tty.die("Cannot pass specs on the command line with --file.")
        specs = _read_specs_from_file(args.file)

    # If nothing is passed, use all packages.
    if not specs:
        specs = [Spec(n) for n in spack.db.all_package_names()]

    # Default name for directory is spack-mirror-<DATESTAMP>
    if not args.directory:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        args.directory = 'spack-mirror-' + timestamp

    # Make sure nothing is in the way.
    existed = False
    if os.path.isfile(args.directory):
        tty.error("%s already exists and is a file." % args.directory)
    elif os.path.isdir(args.directory):
        existed = True

    # Actually do the work to create the mirror
    present, mirrored, error = spack.mirror.create(args.directory, specs)
    p, m, e = len(present), len(mirrored), len(error)

    verb = "updated" if existed else "created"
    tty.msg(
        "Successfully %s mirror in %s." % (verb, args.directory),
        "Archive stats:",
        "  %-4d already present"  % p,
        "  %-4d added"            % m,
        "  %-4d failed to fetch." % e)


def mirror(parser, args):
    action = { 'create' : mirror_create,
               'add'    : mirror_add,
               'remove' : mirror_remove,
               'list'   : mirror_list }

    action[args.mirror_command](args)

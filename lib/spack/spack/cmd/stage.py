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
import os

import llnl.util.tty as tty

import spack
import spack.cmd

description="Expand downloaded archive in preparation for install"

def setup_parser(subparser):
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check downloaded packages against checksum")

    dir_parser = subparser.add_mutually_exclusive_group()
    dir_parser.add_argument(
        '-d', '--stage-dir', action='store_const', dest='print_dir',
        const='stage', help="Prints out the stage directory for a spec.")
    dir_parser.add_argument(
        '-b', '--build-dir', action='store_const', dest='print_dir',
        const='build', help="Prints out the expanded archive path for a spec.")

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages to stage")


def stage(parser, args):
    if not args.specs:
        tty.die("stage requires at least one package argument")

    if args.no_checksum:
        spack.do_checksum = False

    specs = spack.cmd.parse_specs(args.specs, concretize=True)

    if args.print_dir:
        if len(specs) != 1:
            tty.die("--stage-dir and --build-dir options only take one spec.")

        spec = specs[0]
        pkg = spack.db.get(spec)

        if args.print_dir == 'stage':
            print pkg.stage.path
        elif args.print_dir == 'build':
            if not os.listdir(pkg.stage.path):
                tty.die("Stage directory is empty.  Run this first:",
                        "spack stage " + " ".join(args.specs))
            print pkg.stage.expanded_archive_path

    else:
        for spec in specs:
            package = spack.db.get(spec)
            package.do_stage()


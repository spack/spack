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

from external import argparse

import spack

description="Manage spack symlinks"

def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='symlink_command')

    list_parser = sp.add_parser('list', help=symlink_list.__doc__)
    update_parser = sp.add_parser('update', help=symlink_update.__doc__)
    update_parser.add_argument('packages', nargs=argparse.REMAINDER, help="Optional package names to update")

def symlink_list(args):
    """List all spack-managed symlinks"""
    spack.symlinks.list_symlinks()

def symlink_update(args):
    """Update symlinks"""
    spack.symlinks.update_symlinks(args.packages)

def symlink(parser, arg):
    action = { 'list' : symlink_list,
               'update' : symlink_update }

    action[arg.symlink_command](arg)

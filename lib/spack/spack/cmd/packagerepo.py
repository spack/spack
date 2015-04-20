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

import llnl.util.tty as tty
from llnl.util.tty.color import colorize
from llnl.util.tty.colify import colify
from llnl.util.lang import index_by

import spack.spec
import spack.config
from spack.util.environment import get_path

description = "Manage package sources"

def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='packagerepo_command')

    add_parser = sp.add_parser('add', help=packagerepo_add.__doc__)
    add_parser.add_argument('directory', help="Directory containing the packages.")
    
    remove_parser = sp.add_parser('remove', help=packagerepo_remove.__doc__)
    remove_parser.add_argument('name')

    list_parser = sp.add_parser('list', help=packagerepo_list.__doc__)


def packagerepo_add(args):
    """Add package sources to the Spack configuration."""
    config = spack.config.get_config()
    user_config = spack.config.get_config('user')
    orig = None
    if config.has_value('packagerepo', '', 'directories'):
        orig = config.get_value('packagerepo', '', 'directories')
    if orig and args.directory in orig.split(':'):
        tty.die('Repo directory %s already exists in the repo list' % args.directory)

    newsetting = orig + ':' + args.directory if orig else args.directory
    user_config.set_value('packagerepo', '', 'directories', newsetting)
    user_config.write()


def packagerepo_remove(args):
    """Remove a package source from the Spack configuration"""
    pass


def packagerepo_list(args):
    """List package sources and their mnemoics"""
    root_names = spack.db.repos
    max_len = max(len(s[0]) for s in root_names)
    fmt = "%%-%ds%%s" % (max_len + 4)
    for root in root_names:
        print fmt % (root[0], root[1])
        
    

def packagerepo(parser, args):
    action = { 'add'    : packagerepo_add,
               'remove' : packagerepo_remove,
               'list'   : packagerepo_list }
    action[args.packagerepo_command](args)

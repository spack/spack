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
from llnl.util.filesystem import join_path, mkdirp

import spack.spec
import spack.config
from spack.util.environment import get_path
from spack.repository import repo_config_filename

import os
import exceptions
from contextlib import closing

description = "Manage package sources"

def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='repo_command')

    add_parser = sp.add_parser('add', help=repo_add.__doc__)
    add_parser.add_argument('directory', help="Directory containing the packages.")

    create_parser = sp.add_parser('create', help=repo_create.__doc__)
    create_parser.add_argument('directory', help="Directory containing the packages.")
    create_parser.add_argument('name', help="Name of new package repository.")

    remove_parser = sp.add_parser('remove', help=repo_remove.__doc__)
    remove_parser.add_argument('name')

    list_parser = sp.add_parser('list', help=repo_list.__doc__)


def add_to_config(dir):
    config = spack.config.get_config()
    user_config = spack.config.get_config('user')
    orig = None
    if config.has_value('repo', '', 'directories'):
        orig = config.get_value('repo', '', 'directories')
    if orig and dir in orig.split(':'):
        return False

    newsetting = orig + ':' + dir if orig else dir
    user_config.set_value('repo', '', 'directories', newsetting)
    user_config.write()
    return True


def repo_add(args):
    """Add package sources to the Spack configuration."""
    if not add_to_config(args.directory):
        tty.die('Repo directory %s already exists in the repo list' % dir)


def repo_create(args):
    """Create a new package repo at a directory and name"""
    dir = args.directory
    name = args.name

    if os.path.exists(dir) and not os.path.isdir(dir):
        tty.die('File %s already exists and is not a directory' % dir)
    if not os.path.exists(dir):
        try:
            mkdirp(dir)
        except exceptions.OSError, e:
            tty.die('Failed to create new directory %s' % dir)
    path = os.path.join(dir, repo_config_filename)
    try:
        with closing(open(path, 'w')) as repofile:
            repofile.write(name + '\n')
    except exceptions.IOError, e:
        tty.die('Could not create new file %s' % path)

    if not add_to_config(args.directory):
        tty.warn('Repo directory %s already exists in the repo list' % dir)


def repo_remove(args):
    """Remove a package source from the Spack configuration"""
    pass


def repo_list(args):
    """List package sources and their mnemoics"""
    root_names = spack.db.repos
    max_len = max(len(s[0]) for s in root_names)
    fmt = "%%-%ds%%s" % (max_len + 4)
    for root in root_names:
        print fmt % (root[0], root[1])



def repo(parser, args):
    action = { 'add'    : repo_add,
               'create' : repo_create,
               'remove' : repo_remove,
               'list'   : repo_list }
    action[args.repo_command](args)

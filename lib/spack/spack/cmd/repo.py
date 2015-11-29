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
import re
import shutil

from external import argparse
import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp

import spack.spec
import spack.config
from spack.util.environment import get_path
from spack.repository import packages_dir_name, repo_config_name, Repo

description = "Manage package source repositories."

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='repo_command')

    # Create
    create_parser = sp.add_parser('create', help=repo_create.__doc__)
    create_parser.add_argument(
        'namespace', help="Namespace to identify packages in the repository.")
    create_parser.add_argument(
        'directory', help="Directory to create the repo in.  Defaults to same as namespace.", nargs='?')

    # List
    list_parser = sp.add_parser('list', help=repo_list.__doc__)


def repo_create(args):
    """Create a new package repo for a particular namespace."""
    namespace = args.namespace
    if not re.match(r'\w[\.\w-]*', namespace):
        tty.die("Invalid namespace: '%s'" % namespace)

    root = args.directory
    if not root:
        root = namespace

    existed = False
    if os.path.exists(root):
        if os.path.isfile(root):
            tty.die('File %s already exists and is not a directory' % root)
        elif os.path.isdir(root):
            if not os.access(root, os.R_OK | os.W_OK):
                tty.die('Cannot create new repo in %s: cannot access directory.' % root)
            if os.listdir(root):
                tty.die('Cannot create new repo in %s: directory is not empty.' % root)
        existed = True

    full_path = os.path.realpath(root)
    parent = os.path.dirname(full_path)
    if not os.access(parent, os.R_OK | os.W_OK):
        tty.die("Cannot create repository in %s: can't access parent!" % root)

    try:
        config_path = os.path.join(root, repo_config_name)
        packages_path = os.path.join(root, packages_dir_name)

        mkdirp(packages_path)
        with open(config_path, 'w') as config:
            config.write("repo:\n")
            config.write("  namespace: '%s'\n" % namespace)

    except (IOError, OSError) as e:
        tty.die('Failed to create new repository in %s.' % root,
                "Caused by %s: %s" % (type(e), e))

        # try to clean up.
        if existed:
            shutil.rmtree(config_path, ignore_errors=True)
            shutil.rmtree(packages_path, ignore_errors=True)
        else:
            shutil.rmtree(root, ignore_errors=True)

    tty.msg("Created repo with namespace '%s'." % namespace)
    tty.msg("To register it with Spack, add a line like this to ~/.spack/repos.yaml:",
            'repos:',
            '  - ' + full_path)


def repo_add(args):
    """Remove a package source from the Spack configuration"""
    # FIXME: how to deal with this with the current config architecture?
    # FIXME: Repos do not have mnemonics, which I assumed would be simpler... should they have them after all?


def repo_remove(args):
    """Remove a package source from the Spack configuration"""
    # FIXME: see above.


def repo_list(args):
    """List package sources and their mnemoics"""
    roots = spack.config.get_repos_config()
    repos = [Repo(r) for r in roots]

    msg = "%d package repositor" % len(repos)
    msg += "y." if len(repos) == 1 else "ies."
    tty.msg(msg)

    max_ns_len = max(len(r.namespace) for r in repos)
    for repo in repos:
        fmt = "%%-%ds%%s" % (max_ns_len + 4)
        print fmt % (repo.namespace, repo.root)


def repo(parser, args):
    action = { 'create' : repo_create,
               'list'   : repo_list }
    action[args.repo_command](args)

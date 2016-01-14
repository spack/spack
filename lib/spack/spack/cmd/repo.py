##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://llnl.github.io/spack
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
from spack.repository import *

description = "Manage package source repositories."

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='repo_command')
    scopes = spack.config.config_scopes

    # Create
    create_parser = sp.add_parser('create', help=repo_create.__doc__)
    create_parser.add_argument(
        'namespace', help="Namespace to identify packages in the repository.")
    create_parser.add_argument(
        'directory', help="Directory to create the repo in.  Defaults to same as namespace.", nargs='?')

    # List
    list_parser = sp.add_parser('list', help=repo_list.__doc__)
    list_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_list_scope,
        help="Configuration scope to read from.")

    # Add
    add_parser = sp.add_parser('add', help=repo_add.__doc__)
    add_parser.add_argument('path', help="Path to a Spack package repository directory.")
    add_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_modify_scope,
        help="Configuration scope to modify.")

    # Remove
    remove_parser = sp.add_parser('remove', help=repo_remove.__doc__, aliases=['rm'])
    remove_parser.add_argument(
        'path_or_namespace',
        help="Path or namespace of a Spack package repository.")
    remove_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_modify_scope,
        help="Configuration scope to modify.")


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
    tty.msg("To register it with spack, run this command:",
            'spack repo add %s' % full_path)


def repo_add(args):
    """Add a package source to the Spack configuration"""
    path = args.path

    # check if the path is relative to the spack directory.
    real_path = path
    if path.startswith('$spack'):
        real_path = spack.repository.substitute_spack_prefix(path)
    elif not os.path.isabs(real_path):
        real_path = os.path.abspath(real_path)
        path = real_path

    # check if the path exists
    if not os.path.exists(real_path):
        tty.die("No such file or directory: '%s'." % path)

    # Make sure the path is a directory.
    if not os.path.isdir(real_path):
        tty.die("Not a Spack repository: '%s'." % path)

    # Make sure it's actually a spack repository by constructing it.
    repo = Repo(real_path)

    # If that succeeds, finally add it to the configuration.
    repos = spack.config.get_config('repos', args.scope)
    if not repos: repos = []

    if repo.root in repos or path in repos:
        tty.die("Repository is already registered with Spack: '%s'" % path)

    repos.insert(0, path)
    spack.config.update_config('repos', repos, args.scope)
    tty.msg("Created repo with namespace '%s'." % repo.namespace)


def repo_remove(args):
    """Remove a repository from the Spack configuration."""
    repos = spack.config.get_config('repos', args.scope)
    path_or_namespace = args.path_or_namespace

    # If the argument is a path, remove that repository from config.
    path = os.path.abspath(path_or_namespace)
    if path in repos:
        repos.remove(path)
        spack.config.update_config('repos', repos, args.scope)
        tty.msg("Removed repository '%s'." % path)
        return

    # If it is a namespace, remove corresponding repo
    for path in repos:
        try:
            repo = Repo(path)
            if repo.namespace == path_or_namespace:
                repos.remove(repo.root)
                spack.config.update_config('repos', repos, args.scope)
                tty.msg("Removed repository '%s' with namespace %s."
                        % (repo.root, repo.namespace))
                return
        except RepoError as e:
            continue

    tty.die("No repository with path or namespace: '%s'"
            % path_or_namespace)


def repo_list(args):
    """List package sources and their mnemoics"""
    roots = spack.config.get_config('repos', args.scope)
    repos = []
    for r in roots:
        try:
            repos.append(Repo(r))
        except RepoError as e:
            continue

    msg = "%d package repositor" % len(repos)
    msg += "y." if len(repos) == 1 else "ies."
    tty.msg(msg)

    if not repos:
        return

    max_ns_len = max(len(r.namespace) for r in repos)
    for repo in repos:
        fmt = "%%-%ds%%s" % (max_ns_len + 4)
        print fmt % (repo.namespace, repo.root)


def repo(parser, args):
    action = { 'create' : repo_create,
               'list'   : repo_list,
               'add'    : repo_add,
               'remove' : repo_remove,
               'rm'     : repo_remove}
    action[args.repo_command](args)

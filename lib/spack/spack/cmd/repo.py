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
from __future__ import print_function

import os

import llnl.util.tty as tty

import spack.spec
import spack.config
from spack.repository import *

description = "manage package source repositories"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='repo_command')
    scopes = spack.config.config_scopes

    # Create
    create_parser = sp.add_parser('create', help=repo_create.__doc__)
    create_parser.add_argument(
        'directory', help="directory to create the repo in")
    create_parser.add_argument(
        'namespace', help="namespace to identify packages in the repository. "
        "defaults to the directory name", nargs='?')

    # List
    list_parser = sp.add_parser('list', help=repo_list.__doc__)
    list_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_list_scope,
        help="configuration scope to read from")

    # Add
    add_parser = sp.add_parser('add', help=repo_add.__doc__)
    add_parser.add_argument(
        'path', help="path to a Spack package repository directory")
    add_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_modify_scope,
        help="configuration scope to modify")

    # Remove
    remove_parser = sp.add_parser(
        'remove', help=repo_remove.__doc__, aliases=['rm'])
    remove_parser.add_argument(
        'path_or_namespace',
        help="path or namespace of a Spack package repository")
    remove_parser.add_argument(
        '--scope', choices=scopes, default=spack.cmd.default_modify_scope,
        help="configuration scope to modify")


def repo_create(args):
    """Create a new package repository."""
    full_path, namespace = create_repo(args.directory, args.namespace)
    tty.msg("Created repo with namespace '%s'." % namespace)
    tty.msg("To register it with spack, run this command:",
            'spack repo add %s' % full_path)


def repo_add(args):
    """Add a package source to Spack's configuration."""
    path = args.path

    # real_path is absolute and handles substitution.
    canon_path = canonicalize_path(path)

    # check if the path exists
    if not os.path.exists(canon_path):
        tty.die("No such file or directory: %s" % path)

    # Make sure the path is a directory.
    if not os.path.isdir(canon_path):
        tty.die("Not a Spack repository: %s" % path)

    # Make sure it's actually a spack repository by constructing it.
    repo = Repo(canon_path)

    # If that succeeds, finally add it to the configuration.
    repos = spack.config.get_config('repos', args.scope)
    if not repos:
        repos = []

    if repo.root in repos or path in repos:
        tty.die("Repository is already registered with Spack: %s" % path)

    repos.insert(0, canon_path)
    spack.config.update_config('repos', repos, args.scope)
    tty.msg("Added repo with namespace '%s'." % repo.namespace)


def repo_remove(args):
    """Remove a repository from Spack's configuration."""
    repos = spack.config.get_config('repos', args.scope)
    path_or_namespace = args.path_or_namespace

    # If the argument is a path, remove that repository from config.
    canon_path = canonicalize_path(path_or_namespace)
    for repo_path in repos:
        repo_canon_path = canonicalize_path(repo_path)
        if canon_path == repo_canon_path:
            repos.remove(repo_path)
            spack.config.update_config('repos', repos, args.scope)
            tty.msg("Removed repository %s" % repo_path)
            return

    # If it is a namespace, remove corresponding repo
    for path in repos:
        try:
            repo = Repo(path)
            if repo.namespace == path_or_namespace:
                repos.remove(path)
                spack.config.update_config('repos', repos, args.scope)
                tty.msg("Removed repository %s with namespace '%s'."
                        % (repo.root, repo.namespace))
                return
        except RepoError:
            continue

    tty.die("No repository with path or namespace: %s"
            % path_or_namespace)


def repo_list(args):
    """Show registered repositories and their namespaces."""
    roots = spack.config.get_config('repos', args.scope)
    repos = []
    for r in roots:
        try:
            repos.append(Repo(r))
        except RepoError:
            continue

    msg = "%d package repositor" % len(repos)
    msg += "y." if len(repos) == 1 else "ies."
    tty.msg(msg)

    if not repos:
        return

    max_ns_len = max(len(r.namespace) for r in repos)
    for repo in repos:
        fmt = "%%-%ds%%s" % (max_ns_len + 4)
        print(fmt % (repo.namespace, repo.root))


def repo(parser, args):
    action = {'create': repo_create,
              'list': repo_list,
              'add': repo_add,
              'remove': repo_remove,
              'rm': repo_remove}
    action[args.repo_command](args)

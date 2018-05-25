##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os
import glob

import llnl.util.tty as tty

import spack.cmd
import spack.paths
import spack.repo
from spack.spec import Spec
from spack.util.editor import editor

description = "open package files in $EDITOR"
section = "packaging"
level = "short"


def edit_package(name, repo_path, namespace):
    """Opens the requested package file in your favorite $EDITOR.

    Args:
        name (str): The name of the package
        repo_path (str): The path to the repository containing this package
        namespace (str): A valid namespace registered with Spack
    """
    # Find the location of the package
    if repo_path:
        repo = spack.repo.Repo(repo_path)
    elif namespace:
        repo = spack.repo.path.get_repo(namespace)
    else:
        repo = spack.repo.path
    path = repo.filename_for_package_name(name)

    spec = Spec(name)
    if os.path.exists(path):
        if not os.path.isfile(path):
            tty.die("Something is wrong. '{0}' is not a file!".format(path))
        if not os.access(path, os.R_OK | os.W_OK):
            tty.die("Insufficient permissions on '%s'!" % path)
    else:
        tty.die("No package for '{0}' was found.".format(spec.name),
                "  Use `spack create` to create a new package")

    editor(path)


def setup_parser(subparser):
    excl_args = subparser.add_mutually_exclusive_group()

    # Various types of Spack files that can be edited
    # Edits package files by default
    excl_args.add_argument(
        '-b', '--build-system', dest='path', action='store_const',
        const=spack.paths.build_systems_path,
        help="Edit the build system with the supplied name.")
    excl_args.add_argument(
        '-c', '--command', dest='path', action='store_const',
        const=spack.paths.command_path,
        help="edit the command with the supplied name")
    excl_args.add_argument(
        '-d', '--docs', dest='path', action='store_const',
        const=os.path.join(spack.paths.lib_path, 'docs'),
        help="edit the docs with the supplied name")
    excl_args.add_argument(
        '-t', '--test', dest='path', action='store_const',
        const=spack.paths.test_path,
        help="edit the test with the supplied name")
    excl_args.add_argument(
        '-m', '--module', dest='path', action='store_const',
        const=spack.paths.module_path,
        help="edit the main spack module with the supplied name")

    # Options for editing packages
    excl_args.add_argument(
        '-r', '--repo', default=None,
        help="path to repo to edit package in")
    excl_args.add_argument(
        '-N', '--namespace', default=None,
        help="namespace of package to edit")

    subparser.add_argument(
        'name', nargs='?', default=None,
        help="name of package to edit")


def edit(parser, args):
    name = args.name

    # By default, edit package files
    path = spack.paths.packages_path

    # If `--command`, `--test`, or `--module` is chosen, edit those instead
    if args.path:
        path = args.path
        if name:
            # convert command names to python module name
            if path == spack.paths.command_path:
                name = spack.cmd.python_name(name)

            path = os.path.join(path, name)
            if not os.path.exists(path):
                files = glob.glob(path + '*')
                blacklist = ['.pyc', '~']  # blacklist binaries and backups
                files = list(filter(
                    lambda x: all(s not in x for s in blacklist), files))
                if len(files) > 1:
                    m = 'Multiple files exist with the name {0}.'.format(name)
                    m += ' Please specify a suffix. Files are:\n\n'
                    for f in files:
                        m += '        ' + os.path.basename(f) + '\n'
                    tty.die(m)
                if not files:
                    tty.die("No file for '{0}' was found in {1}".format(name,
                                                                        path))
                path = files[0]  # already confirmed only one entry in files

        editor(path)
    elif name:
        edit_package(name, args.repo, args.namespace)
    else:
        # By default open the directory where packages live
        editor(path)

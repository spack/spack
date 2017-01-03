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
import os

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, join_path

import spack
import spack.cmd
from spack.spec import Spec
from spack.repository import Repo
from spack.util.naming import mod_to_class

description = "Open package files in $EDITOR"

# When `--force` is supplied, we'll create a very minimal skeleton.
package_template = '''
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install {name}
#
# You can edit this file again by typing:
#
#     spack edit {name}
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class {class_name}(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
'''


def edit_package(name, repo_path, namespace, force=False):
    """Opens the requested package file in your favorite $EDITOR.

    :param str name: The name of the package
    :param str repo_path: The path to the repository containing this package
    :param str namespace: A valid namespace registered with Spack
    :param bool force: [DEPRECATED] Create a new empty package
    """
    # Find the location of the package
    if repo_path:
        repo = Repo(repo_path)
    elif namespace:
        repo = spack.repo.get_repo(namespace)
    else:
        repo = spack.repo
    path = repo.filename_for_package_name(name)

    spec = Spec(name)
    if os.path.exists(path):
        if not os.path.isfile(path):
            tty.die("Something is wrong. '{0}' is not a file!".format(path))
        if not os.access(path, os.R_OK | os.W_OK):
            tty.die("Insufficient permissions on '%s'!" % path)
    elif not force:
        tty.die("No package for '{0}' was found.".format(spec.name),
                "  Use `spack create` to create a new package")
    else:
        # Force create a new package (deprecated)
        mkdirp(os.path.dirname(path))
        with open(path, 'w') as pkg_file:
            pkg_file.write(package_template.format(
                name=spec.name, class_name=mod_to_class(spec.name)))

    spack.editor(path)


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', dest='force', action='store_true',
        help='deprecated, use `spack create` instead')

    excl_args = subparser.add_mutually_exclusive_group()

    # Various types of Spack files that can be edited
    # Edits package files by default
    excl_args.add_argument(
        '-c', '--command', dest='path', action='store_const',
        const=spack.cmd.command_path,
        help='edit the command with the supplied name')
    excl_args.add_argument(
        '-t', '--test', dest='path', action='store_const',
        const=spack.test_path, help='edit the test with the supplied name')
    excl_args.add_argument(
        '-m', '--module', dest='path', action='store_const',
        const=spack.module_path,
        help='edit the main spack module with the supplied name')

    # Options for editing packages
    excl_args.add_argument(
        '-r', '--repo', default=None,
        help='path to repo to edit package in')
    excl_args.add_argument(
        '-N', '--namespace', default=None,
        help='namespace of package to edit')

    subparser.add_argument(
        'name', nargs='?', default=None,
        help='name of package to edit')


def edit(parser, args):
    # Deprecate `--force`
    if args.force:
        tty.warn("`spack edit --force` is deprecated, please use "
                 "`spack create` instead!")

    name = args.name

    # By default, edit package files
    path = spack.packages_path

    # If `--command`, `--test`, or `--module` is chosen, edit those instead
    if args.path:
        path = args.path
        if name:
            path = join_path(path, name + ".py")
            if not args.force and not os.path.exists(path):
                tty.die("No command for '{0}' was found.".format(name))
        spack.editor(path)
    elif name:
        edit_package(name, args.repo, args.namespace, args.force)
    else:
        # By default open the directory where packages live
        spack.editor(path)

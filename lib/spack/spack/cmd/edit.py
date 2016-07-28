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
import string

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, join_path

import spack
import spack.cmd
from spack.spec import Spec
from spack.repository import Repo
from spack.util.naming import mod_to_class

description = "Open package files in $EDITOR"

# When -f is supplied, we'll create a very minimal skeleton.
package_template = string.Template("""\
from spack import *

class ${class_name}(Package):
    ""\"Description""\"

    homepage = "http://www.example.com"
    url      = "http://www.example.com/${name}-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
""")


def edit_package(name, repo_path, namespace, force=False):
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
            tty.die("Something's wrong.  '%s' is not a file!" % path)
        if not os.access(path, os.R_OK|os.W_OK):
            tty.die("Insufficient permissions on '%s'!" % path)
    elif not force:
        tty.die("No package '%s'.  Use spack create, or supply -f/--force "
                "to edit a new file." % spec.name)
    else:
        mkdirp(os.path.dirname(path))
        with open(path, "w") as pkg_file:
            pkg_file.write(
                package_template.substitute(
                    name=spec.name, class_name=mod_to_class(spec.name)))

    spack.editor(path)


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', dest='force', action='store_true',
        help="Open a new file in $EDITOR even if package doesn't exist.")

    excl_args = subparser.add_mutually_exclusive_group()

    # Various filetypes you can edit directly from the cmd line.
    excl_args.add_argument(
        '-c', '--command', dest='path', action='store_const',
        const=spack.cmd.command_path, help="Edit the command with the supplied name.")
    excl_args.add_argument(
        '-t', '--test', dest='path', action='store_const',
        const=spack.test_path, help="Edit the test with the supplied name.")
    excl_args.add_argument(
        '-m', '--module', dest='path', action='store_const',
        const=spack.module_path, help="Edit the main spack module with the supplied name.")

    # Options for editing packages
    excl_args.add_argument(
        '-r', '--repo', default=None, help="Path to repo to edit package in.")
    excl_args.add_argument(
        '-N', '--namespace', default=None, help="Namespace of package to edit.")

    subparser.add_argument(
        'name', nargs='?', default=None, help="name of package to edit")


def edit(parser, args):
    name = args.name

    path = spack.packages_path
    if args.path:
        path = args.path
        if name:
            path = join_path(path, name + ".py")
            if not args.force and not os.path.exists(path):
                tty.die("No command named '%s'." % name)
        spack.editor(path)

    elif name:
        edit_package(name, args.repo, args.namespace, args.force)
    else:
        # By default open the directory where packages or commands live.
        spack.editor(path)

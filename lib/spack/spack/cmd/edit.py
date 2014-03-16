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
import string
from contextlib import closing

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack
import spack.packages as packages

description = "Open package files in $EDITOR"

# When -f is supplied, we'll create a very minimal skeleton.
package_template = string.Template("""\
from spack import *

class ${class_name}(Package):
    ""\"Description""\"

    homepage = "http://www.example.com"
    url      = "http://www.example.com/${name}-1.0.tar.gz"

    versions = { '1.0' : '0123456789abcdef0123456789abcdef' }

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
""")


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', dest='force', action='store_true',
        help="Open a new file in $EDITOR even if package doesn't exist.")
    subparser.add_argument(
        'name', nargs='?', default=None, help="name of package to edit")


def edit(parser, args):
    name = args.name

    # By default open the directory where packages live.
    if not name:
        path = spack.packages_path
    else:
        path = spack.db.filename_for_package_name(name)

        if os.path.exists(path):
            if not os.path.isfile(path):
                tty.die("Something's wrong.  '%s' is not a file!" % path)
            if not os.access(path, os.R_OK|os.W_OK):
                tty.die("Insufficient permissions on '%s'!" % path)
        elif not args.force:
            tty.die("No package '%s'.  Use spack create, or supply -f/--force "
                    "to edit a new file." % name)
        else:
            mkdirp(os.path.dirname(path))
            class_name = packages.class_name_for_package_name(name)
            with closing(open(path, "w")) as pkg_file:
                pkg_file.write(
                    package_template.substitute(name=name, class_name=class_name))

    # If everything checks out, go ahead and edit.
    spack.editor(path)

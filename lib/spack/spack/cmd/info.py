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
import re
import textwrap
from llnl.util.tty.colify import colify
import spack
import spack.fetch_strategy as fs

description = "Get detailed information on a particular package"

def setup_parser(subparser):
    subparser.add_argument('name', metavar="PACKAGE", help="name of packages to get info on")


def info(parser, args):
    pkg = spack.db.get(args.name)
    print "Package:   ", pkg.name
    print "Homepage:  ", pkg.homepage

    print
    print "Versions:  "

    if not pkg.versions:
        print("None.")
    else:
        maxlen = max(len(str(v)) for v in pkg.versions)
        fmt = "%%-%ss" % maxlen
        for v in reversed(sorted(pkg.versions)):
            f = fs.for_package_version(pkg, v)
            print "    " + (fmt % v) + "    " + str(f)

    print
    print "Dependencies:"
    if pkg.dependencies:
        colify(pkg.dependencies, indent=4)
    else:
        print "    None"

    print
    print "Virtual pkgs: "
    if pkg.provided:
        for spec, when in pkg.provided.items():
            print "    %s provides %s" % (when, spec)
    else:
        print "    None"

    print
    print "Description:"
    if pkg.__doc__:
        doc = re.sub(r'\s+', ' ', pkg.__doc__)
        lines = textwrap.wrap(doc, 72)
        for line in lines:
            print "    " + line
    else:
        print "    None"

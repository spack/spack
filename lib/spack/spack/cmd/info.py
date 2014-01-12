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

import spack
import spack.packages as packages
from spack.colify import colify

description = "Get detailed information on a particular package"

def setup_parser(subparser):
    subparser.add_argument('name', metavar="PACKAGE", help="name of packages to get info on")


def info(parser, args):
    package = packages.get(args.name)
    print "Package:   ", package.name
    print "Homepage:  ", package.homepage
    print "Download:  ", package.url

    print
    print "Safe versions:  "

    if package.versions:
        colify(reversed(sorted(package.versions)), indent=4)
    else:
        print "None.  Use spack versions %s to get a list of downloadable versions." % package.name

    print
    print "Dependencies:"
    if package.dependencies:
        colify(package.dependencies, indent=4)
    else:
        print "    None"

    print
    print "Virtual packages: "
    if package.provided:
        for spec, when in package.provided.items():
            print "    %s provides %s" % (when, spec)
    else:
        print "    None"

    print
    print "Description:"
    if package.__doc__:
        doc = re.sub(r'\s+', ' ', package.__doc__)
        lines = textwrap.wrap(doc, 72)
        for line in lines:
            print "    " + line
    else:
        print "    None"

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
import textwrap
from llnl.util.tty.colify import *
import spack
import spack.fetch_strategy as fs

description = "get detailed information on a particular package"


def padder(str_list, extra=0):
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string):
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * ' ')
    return pad


def setup_parser(subparser):
    subparser.add_argument(
        'name', metavar="PACKAGE", help="name of package to get info for")


def print_text_info(pkg):
    """Print out a plain text description of a package."""
    header = "{0}:   ".format(pkg.build_system_class)

    print header, pkg.name
    whitespaces = ''.join([' '] * (len(header) - len("Homepage: ")))
    print "Homepage:", whitespaces, pkg.homepage

    print
    print "Safe versions:  "

    if not pkg.versions:
        print("    None")
    else:
        pad = padder(pkg.versions, 4)
        for v in reversed(sorted(pkg.versions)):
            f = fs.for_package_version(pkg, v)
            print "    %s%s" % (pad(v), str(f))

    print
    print "Variants:"
    if not pkg.variants:
        print "    None"
    else:
        pad = padder(pkg.variants, 4)

        maxv = max(len(v) for v in sorted(pkg.variants))
        fmt = "%%-%ss%%-10s%%s" % (maxv + 4)

        print "    " + fmt % ('Name',   'Default',   'Description')
        print
        for name in sorted(pkg.variants):
            v = pkg.variants[name]
            default = 'on' if v.default else 'off'

            lines = textwrap.wrap(v.description)
            lines[1:] = ["      " + (" " * maxv) + l for l in lines[1:]]
            desc = "\n".join(lines)

            print "    " + fmt % (name, default, desc)

    print
    print "Installation Phases:"
    phase_str = ''
    for phase in pkg.phases:
        phase_str += "    {0}".format(phase)
    print phase_str

    for deptype in ('build', 'link', 'run'):
        print
        print "%s Dependencies:" % deptype.capitalize()
        deps = sorted(pkg.dependencies_of_type(deptype))
        if deps:
            colify(deps, indent=4)
        else:
            print "    None"

    print
    print "Virtual Packages: "
    if pkg.provided:
        inverse_map = {}
        for spec, whens in pkg.provided.items():
            for when in whens:
                if when not in inverse_map:
                    inverse_map[when] = set()
                inverse_map[when].add(spec)
        for when, specs in reversed(sorted(inverse_map.items())):
            print "    %s provides %s" % (
                when, ', '.join(str(s) for s in specs))
    else:
        print "    None"

    print
    print "Description:"
    if pkg.__doc__:
        print pkg.format_doc(indent=4)
    else:
        print "    None"


def info(parser, args):
    pkg = spack.repo.get(args.name)
    print_text_info(pkg)

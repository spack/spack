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
import llnl.util.tty as tty

import spack
import spack.url
from spack.util.web import find_versions_of_archive

description = "Show parsing of a URL, optionally spider web for versions."


def setup_parser(subparser):
    subparser.add_argument('url', help="url of a package archive")
    subparser.add_argument(
        '-s', '--spider', action='store_true',
        help="Spider the source page for versions.")


def print_name_and_version(url):
    name, ns, nl, ntup, ver, vs, vl, vtup = spack.url.substitution_offsets(url)
    underlines = [" "] * max(ns + nl, vs + vl)
    for i in range(ns, ns + nl):
        underlines[i] = '-'
    for i in range(vs, vs + vl):
        underlines[i] = '~'

    print "    %s" % url
    print "    %s" % ''.join(underlines)


def url_parse(parser, args):
    url = args.url

    ver,  vs, vl = spack.url.parse_version_offset(url, debug=True)
    name, ns, nl = spack.url.parse_name_offset(url, ver, debug=True)
    print

    tty.msg("Detected:")
    try:
        print_name_and_version(url)
    except spack.url.UrlParseError as e:
        tty.error(str(e))

    print '    name:     %s' % name
    print '    version:  %s' % ver

    print
    tty.msg("Substituting version 9.9.9b:")
    newurl = spack.url.substitute_version(url, '9.9.9b')
    print_name_and_version(newurl)

    if args.spider:
        print
        tty.msg("Spidering for versions:")
        versions = find_versions_of_archive(url)
        for v in sorted(versions):
            print "%-20s%s" % (v, versions[v])

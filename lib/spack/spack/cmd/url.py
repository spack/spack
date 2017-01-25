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

import spack
import spack.url
from spack.util.web import find_versions_of_archive
from llnl.util import tty

description = "debugging tool for url parsing"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand')

    # Parse
    parse_parser = sp.add_parser('parse', help='attempt to parse a url')

    parse_parser.add_argument(
        'url',
        help='url to parse')
    parse_parser.add_argument(
        '-s', '--spider', action='store_true',
        help='spider the source page for versions')

    # List
    list_parser = sp.add_parser('list', help='list urls in all packages')

    list_parser.add_argument(
        '-c', '--color', action='store_true',
        help='color the parsed version and name in the urls shown '
             '(versions will be cyan, name red)')
    list_parser.add_argument(
        '-e', '--extrapolation', action='store_true',
        help='color the versions used for extrapolation as well '
             '(additional versions will be green, names magenta)')

    excl_args = list_parser.add_mutually_exclusive_group()

    excl_args.add_argument(
        '-n', '--incorrect-name', action='store_true',
        help='only list urls for which the name was incorrectly parsed')
    excl_args.add_argument(
        '-v', '--incorrect-version', action='store_true',
        help='only list urls for which the version was incorrectly parsed')

    # Test
    test_parser = sp.add_parser(
        'test', help='print a summary of how well we are parsing package urls')

    #test_parser.add_argument(
    #    'package', nargs='*',
    #    help="package(s) to parse url(s) from [default: all]")


def url_parse(args):
    url = args.url

    tty.msg('Parsing URL: {0}'.format(url))
    print()

    ver,  vs, vl, vi, vregex = spack.url.parse_version_offset(url)
    tty.msg("Matched version regex {0:>2}: r'{1}'".format(vi, vregex))

    name, ns, nl, ni, nregex = spack.url.parse_name_offset(url, ver)
    tty.msg("Matched  name   regex {0:>2}: r'{1}'".format(ni, nregex))

    print()
    tty.msg('Detected:')
    try:
        print_name_and_version(url)
    except spack.url.UrlParseError as e:
        tty.error(str(e))

    print('    name:    {0}'.format(name))
    print('    version: {0}'.format(ver))
    print()

    tty.msg('Substituting version 9.9.9b:')
    newurl = spack.url.substitute_version(url, '9.9.9b')
    print_name_and_version(newurl)

    if args.spider:
        print()
        tty.msg('Spidering for versions:')
        versions = find_versions_of_archive(url)

        max_len = max(len(str(v)) for v in versions)

        for v in sorted(versions):
            print('{0:{1}}  {2}'.format(v, max_len, versions[v]))


def url_list(args):
    urls = set()
    for pkg in spack.repo.all_packages():
        url = getattr(pkg.__class__, 'url', None)
        if url:
            urls.add(url)

        for params in pkg.versions.values():
            url = params.get('url', None)
            if url:
                urls.add(url)

    for url in sorted(urls):
        if args.color or args.extrapolation:
            print(spack.url.color_url(
                url, subs=args.extrapolation, errors=True))
        else:
            print(url)


def url_test(args):
    print('in url_test')


def url(parser, args):
    action = {
        'parse': url_parse,
        'list':  url_list,
        'test':  url_test
    }

    action[args.subcommand](args)


def print_name_and_version(url):
    name, ns, nl, ntup, ver, vs, vl, vtup = spack.url.substitution_offsets(url)
    underlines = [' '] * max(ns + nl, vs + vl)
    for i in range(ns, ns + nl):
        underlines[i] = '-'
    for i in range(vs, vs + vl):
        underlines[i] = '~'

    print('    {0}'.format(url))
    print('    {0}'.format(''.join(underlines)))


def urls(parser, args):
    total_urls = 0
    bad_urls = 0

    # Loop through all packages
    for pkg in spack.repo.all_packages():
        # A package may have multiple URLs
        urls = []

        url = getattr(pkg.__class__, 'url', None)

        if url:
            urls.append(url)

        for params in pkg.versions.values():
            url = params.get('url', None)
            if url:
                urls.add(url)

        # Keep track of how many packages actually have a url attribute
        total_urls += 1

    for url in sorted(urls):
        if args.color or args.extrapolation:
            print(spack.url.color_url(
                url, subs=args.extrapolation, errors=True))
        else:
            print(url)


def check_parsing(pkg, url):
    """See whether or not we correctly parsed"""
    pass

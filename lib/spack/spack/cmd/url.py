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

from llnl.util import tty
from spack.url import *
from spack.util.web import find_versions_of_archive

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

    ver,  vs, vl, vi, vregex = parse_version_offset(url)
    tty.msg("Matched version regex {0:>2}: r'{1}'".format(vi, vregex))

    name, ns, nl, ni, nregex = parse_name_offset(url, ver)
    tty.msg("Matched  name   regex {0:>2}: r'{1}'".format(ni, nregex))

    print()
    tty.msg('Detected:')
    try:
        print_name_and_version(url)
    except UrlParseError as e:
        tty.error(str(e))

    print('    name:    {0}'.format(name))
    print('    version: {0}'.format(ver))
    print()

    tty.msg('Substituting version 9.9.9b:')
    newurl = substitute_version(url, '9.9.9b')
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

    # Gather set of URLs from all packages
    for pkg in spack.repo.all_packages():
        url = getattr(pkg.__class__, 'url', None)
        if url:
            if args.incorrect_name:
                # Only add URLs whose name was parsed incorrectly
                try:
                    name = parse_name(url)
                    if not name_parsed_correctly(pkg, name):
                        urls.add(url)
                except UndetectableNameError:
                    urls.add(url)
            elif args.incorrect_version:
                # Only add URLs whose version was parsed incorrectly
                try:
                    version = parse_version(url)
                    if not version_parsed_correctly(pkg, version):
                        urls.add(url)
                except UndetectableVersionError:
                    urls.add(url)
            else:
                urls.add(url)

        for params in pkg.versions.values():
            url = params.get('url', None)
            if url:
                if args.incorrect_name:
                    # Only add URLs whose name was parsed incorrectly
                    try:
                        name = parse_name(url)
                        if not name_parsed_correctly(pkg, name):
                            urls.add(url)
                    except UndetectableNameError:
                        urls.add(url)
                elif args.incorrect_version:
                    # Only add URLs whose version was parsed incorrectly
                    try:
                        version = parse_version(url)
                        if not version_parsed_correctly(pkg, version):
                            urls.add(url)
                    except UndetectableVersionError:
                        urls.add(url)
                else:
                    urls.add(url)

    # Print URLs
    for url in sorted(urls):
        if args.color or args.extrapolation:
            print(color_url(
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
    name, ns, nl, ntup, ver, vs, vl, vtup = substitution_offsets(url)
    underlines = [' '] * max(ns + nl, vs + vl)
    for i in range(ns, ns + nl):
        underlines[i] = '-'
    for i in range(vs, vs + vl):
        underlines[i] = '~'

    print('    {0}'.format(url))
    print('    {0}'.format(''.join(underlines)))


def name_parsed_correctly(pkg, name):
    """Determine if the name of a package was correctly parsed.

    :param Package pkg: The package in Spack
    :param str name: The name that was extracted from the URL
    :returns: True if the name was correctly parsed, else False
    :rtype: bool
    """
    pkg_name = pkg.name

    # After determining a name, `spack create` determines a build system
    # Some build systems prepend a special string to the front of the name
    # Since this can't be guessed from the URL, it would be unfair to say
    # that these names are incorrectly guessed, so we remove them
    if pkg_name.startswith('r-'):
        pkg_name = pkg_name[2:]
    elif pkg_name.startswith('py-'):
        pkg_name = pkg_name[3:]
    elif pkg_name.startswith('octave-'):
        pkg_name = pkg_name[7:]

    return name == pkg_name


def version_parsed_correctly(pkg, version):
    """Determine if the version of a package was correctly parsed.

    :param Package pkg: The package in Spack
    :param str name: The version that was extracted from the URL
    :returns: True if the name was correctly parsed, else False
    :rtype: bool
    """
    # If the version parsed from the URL is listed in a version()
    # directive, we assume it was correctly parsed
    for pkg_version in pkg.versions:
        if pkg_version == version:
            return True
    return False

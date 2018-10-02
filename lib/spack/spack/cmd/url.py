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
from __future__ import division, print_function
from collections import defaultdict
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import spack.fetch_strategy as fs
import spack.repo
import spack.util.crypto as crypto

from llnl.util import tty
from spack.url import parse_version_offset, parse_name_offset
from spack.url import parse_name, parse_version, color_url
from spack.url import substitute_version, substitution_offsets
from spack.url import UndetectableNameError, UndetectableVersionError
from spack.url import UrlParseError
from spack.util.web import find_versions_of_archive
from spack.util.naming import simplify_name

description = "debugging tool for url parsing"
section = "developer"
level = "long"


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
        '-N', '--correct-name', action='store_true',
        help='only list urls for which the name was correctly parsed')
    excl_args.add_argument(
        '-v', '--incorrect-version', action='store_true',
        help='only list urls for which the version was incorrectly parsed')
    excl_args.add_argument(
        '-V', '--correct-version', action='store_true',
        help='only list urls for which the version was correctly parsed')

    # Summary
    sp.add_parser(
        'summary',
        help='print a summary of how well we are parsing package urls')

    # Stats
    sp.add_parser(
        'stats',
        help='print statistics on versions and checksums for all packages')


def url(parser, args):
    action = {
        'parse':   url_parse,
        'list':    url_list,
        'summary': url_summary,
        'stats':   url_stats,
    }

    action[args.subcommand](args)


def url_parse(args):
    url = args.url

    tty.msg('Parsing URL: {0}'.format(url))
    print()

    ver,  vs, vl, vi, vregex = parse_version_offset(url)
    tty.msg('Matched version regex {0:>2}: r{1!r}'.format(vi, vregex))

    name, ns, nl, ni, nregex = parse_name_offset(url, ver)
    tty.msg('Matched  name   regex {0:>2}: r{1!r}'.format(ni, nregex))

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

        if not versions:
            print('  Found no versions for {0}'.format(name))
            return

        max_len = max(len(str(v)) for v in versions)

        for v in sorted(versions):
            print('{0:{1}}  {2}'.format(v, max_len, versions[v]))


def url_list(args):
    urls = set()

    # Gather set of URLs from all packages
    for pkg in spack.repo.path.all_packages():
        url = getattr(pkg.__class__, 'url', None)
        urls = url_list_parsing(args, urls, url, pkg)

        for params in pkg.versions.values():
            url = params.get('url', None)
            urls = url_list_parsing(args, urls, url, pkg)

    # Print URLs
    for url in sorted(urls):
        if args.color or args.extrapolation:
            print(color_url(url, subs=args.extrapolation, errors=True))
        else:
            print(url)

    # Return the number of URLs that were printed, only for testing purposes
    return len(urls)


def url_summary(args):
    # Collect statistics on how many URLs were correctly parsed
    total_urls       = 0
    correct_names    = 0
    correct_versions = 0

    # Collect statistics on which regexes were matched and how often
    name_regex_dict    = dict()
    name_count_dict    = defaultdict(int)
    version_regex_dict = dict()
    version_count_dict = defaultdict(int)

    tty.msg('Generating a summary of URL parsing in Spack...')

    # Loop through all packages
    for pkg in spack.repo.path.all_packages():
        urls = set()

        url = getattr(pkg.__class__, 'url', None)
        if url:
            urls.add(url)

        for params in pkg.versions.values():
            url = params.get('url', None)
            if url:
                urls.add(url)

        # Calculate statistics
        for url in urls:
            total_urls += 1

            # Parse versions
            version = None
            try:
                version, vs, vl, vi, vregex = parse_version_offset(url)
                version_regex_dict[vi] = vregex
                version_count_dict[vi] += 1
                if version_parsed_correctly(pkg, version):
                    correct_versions += 1
            except UndetectableVersionError:
                pass

            # Parse names
            try:
                name, ns, nl, ni, nregex = parse_name_offset(url, version)
                name_regex_dict[ni] = nregex
                name_count_dict[ni] += 1
                if name_parsed_correctly(pkg, name):
                    correct_names += 1
            except UndetectableNameError:
                pass

    print()
    print('    Total URLs found:          {0}'.format(total_urls))
    print('    Names correctly parsed:    {0:>4}/{1:>4} ({2:>6.2%})'.format(
        correct_names, total_urls, correct_names / total_urls))
    print('    Versions correctly parsed: {0:>4}/{1:>4} ({2:>6.2%})'.format(
        correct_versions, total_urls, correct_versions / total_urls))
    print()

    tty.msg('Statistics on name regular expressions:')

    print()
    print('    Index  Count  Regular Expression')
    for ni in sorted(name_regex_dict.keys()):
        print('    {0:>3}: {1:>6}   r{2!r}'.format(
            ni, name_count_dict[ni], name_regex_dict[ni]))
    print()

    tty.msg('Statistics on version regular expressions:')

    print()
    print('    Index  Count  Regular Expression')
    for vi in sorted(version_regex_dict.keys()):
        print('    {0:>3}: {1:>6}   r{2!r}'.format(
            vi, version_count_dict[vi], version_regex_dict[vi]))
    print()

    # Return statistics, only for testing purposes
    return (total_urls, correct_names, correct_versions,
            name_count_dict, version_count_dict)


def url_stats(args):
    stats = {}  # stats about fetchers in packages.
    nvers = 0   # total number of versions
    npkgs = 0   # total number of packages

    def inc(fstype, category, attr=None):
        """Increment statistics in the stats dict."""
        categories = stats.setdefault(fstype, {})
        if attr:
            cat_stats = categories.setdefault(category, {})
            val = cat_stats.setdefault(attr, 0)
            stats[fstype][category][attr] = val + 1
        else:
            val = categories.setdefault(category, 0)
            stats[fstype][category] = val + 1

    # over all packages
    for pkg in spack.repo.path.all_packages():
        npkgs += 1

        # look at each version
        for v, args in pkg.versions.items():
            # figure out what type of fetcher it is
            fetcher = fs.for_package_version(pkg, v)
            nvers += 1

            fstype = fetcher.url_attr
            inc(fstype, 'total')

            # put some special stats in for particular types of fetchers.
            if fstype == 'git':
                if 'commit' in args:
                    inc('git', 'security', 'commit')
                else:
                    inc('git', 'security', 'no commit')
            elif fstype == 'url':
                for h in crypto.hashes:
                    if h in args:
                        inc('url', 'checksums', h)
                        break
                else:
                    if 'checksum' in args:
                        h = crypto.hash_algo_for_digest(args['checksum'])
                        inc('url', 'checksums', h)
                    else:
                        inc('url', 'checksums', 'no checksum')

                # parse out the URL scheme (https/http/ftp/etc.)
                urlinfo = urlparse(fetcher.url)
                inc('url', 'schemes', urlinfo.scheme)

    # print a nice summary table
    tty.msg("%d total versions for %d packages:" % (nvers, npkgs))
    line_width = 36
    print("-" * line_width)
    for fetcher, fetcher_stats in sorted(stats.items(), reverse=True):
        fs_total = fetcher_stats['total']
        fs_pct = float(fs_total) / nvers * 100
        print("%-22s%5d%8.1f%%" % (fetcher, fs_total, fs_pct))

        for category, cat_stats in sorted(fetcher_stats.items(), reverse=True):
            if category == 'total':
                continue
            print("  %s" % category)

            for name, number in sorted(cat_stats.items(), reverse=True):
                pct = float(number) / fs_total * 100
                print("    %-18s%5d%8.1f%%" % (name, number, pct))
        print("-" * line_width)


def print_name_and_version(url):
    """Prints a URL. Underlines the detected name with dashes and
    the detected version with tildes.

    Args:
        url (str): The url to parse
    """
    name, ns, nl, ntup, ver, vs, vl, vtup = substitution_offsets(url)
    underlines = [' '] * max(ns + nl, vs + vl)
    for i in range(ns, ns + nl):
        underlines[i] = '-'
    for i in range(vs, vs + vl):
        underlines[i] = '~'

    print('    {0}'.format(url))
    print('    {0}'.format(''.join(underlines)))


def url_list_parsing(args, urls, url, pkg):
    """Helper function for :func:`url_list`.

    Args:
        args (argparse.Namespace): The arguments given to ``spack url list``
        urls (set): List of URLs that have already been added
        url (str or None): A URL to potentially add to ``urls`` depending on
            ``args``
        pkg (spack.package.PackageBase): The Spack package

    Returns:
        set: The updated set of ``urls``
    """
    if url:
        if args.correct_name or args.incorrect_name:
            # Attempt to parse the name
            try:
                name = parse_name(url)
                if (args.correct_name and
                    name_parsed_correctly(pkg, name)):
                    # Add correctly parsed URLs
                    urls.add(url)
                elif (args.incorrect_name and
                      not name_parsed_correctly(pkg, name)):
                    # Add incorrectly parsed URLs
                    urls.add(url)
            except UndetectableNameError:
                if args.incorrect_name:
                    # Add incorrectly parsed URLs
                    urls.add(url)
        elif args.correct_version or args.incorrect_version:
            # Attempt to parse the version
            try:
                version = parse_version(url)
                if (args.correct_version and
                    version_parsed_correctly(pkg, version)):
                    # Add correctly parsed URLs
                    urls.add(url)
                elif (args.incorrect_version and
                      not version_parsed_correctly(pkg, version)):
                    # Add incorrectly parsed URLs
                    urls.add(url)
            except UndetectableVersionError:
                if args.incorrect_version:
                    # Add incorrectly parsed URLs
                    urls.add(url)
        else:
            urls.add(url)

    return urls


def name_parsed_correctly(pkg, name):
    """Determine if the name of a package was correctly parsed.

    Args:
        pkg (spack.package.PackageBase): The Spack package
        name (str): The name that was extracted from the URL

    Returns:
        bool: True if the name was correctly parsed, else False
    """
    pkg_name = pkg.name

    name = simplify_name(name)

    # After determining a name, `spack create` determines a build system.
    # Some build systems prepend a special string to the front of the name.
    # Since this can't be guessed from the URL, it would be unfair to say
    # that these names are incorrectly parsed, so we remove them.
    if pkg_name.startswith('r-'):
        pkg_name = pkg_name[2:]
    elif pkg_name.startswith('py-'):
        pkg_name = pkg_name[3:]
    elif pkg_name.startswith('perl-'):
        pkg_name = pkg_name[5:]
    elif pkg_name.startswith('octave-'):
        pkg_name = pkg_name[7:]

    return name == pkg_name


def version_parsed_correctly(pkg, version):
    """Determine if the version of a package was correctly parsed.

    Args:
        pkg (spack.package.PackageBase): The Spack package
        version (str): The version that was extracted from the URL

    Returns:
        bool: True if the name was correctly parsed, else False
    """
    version = remove_separators(version)

    # If the version parsed from the URL is listed in a version()
    # directive, we assume it was correctly parsed
    for pkg_version in pkg.versions:
        pkg_version = remove_separators(pkg_version)
        if pkg_version == version:
            return True
    return False


def remove_separators(version):
    """Removes separator characters ('.', '_', and '-') from a version.

    A version like 1.2.3 may be displayed as 1_2_3 in the URL.
    Make sure 1.2.3, 1-2-3, 1_2_3, and 123 are considered equal.
    Unfortunately, this also means that 1.23 and 12.3 are equal.

    Args:
        version (str or Version): A version

    Returns:
        str: The version with all separator characters removed
    """
    version = str(version)

    version = version.replace('.', '')
    version = version.replace('_', '')
    version = version.replace('-', '')

    return version

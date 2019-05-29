# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from __future__ import division

import argparse
import cgi
import fnmatch
import os
import re
import sys
import math

from six import StringIO

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.dependency
import spack.repo
import spack.cmd.common.arguments as arguments

description = "list and search available packages"
section = "basic"
level = "short"


formatters = {}


def formatter(func):
    """Decorator used to register formatters"""
    formatters[func.__name__] = func
    return func


def setup_parser(subparser):
    subparser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results')
    subparser.add_argument(
        '-d', '--search-description', action='store_true', default=False,
        help='filtering will also search the description for a match')
    subparser.add_argument(
        '--format', default='name_only', choices=formatters,
        help='format to be used to print the output [default: name_only]')
    subparser.add_argument(
        '--update', metavar='FILE', default=None, action='store',
        help='write output to the specified file, if any package is newer')

    arguments.add_common_arguments(subparser, ['tags'])


def filter_by_name(pkgs, args):
    """
    Filters the sequence of packages according to user prescriptions

    Args:
        pkgs: sequence of packages
        args: parsed command line arguments

    Returns:
        filtered and sorted list of packages
    """
    if args.filter:
        res = []
        for f in args.filter:
            if '*' not in f and '?' not in f:
                r = fnmatch.translate('*' + f + '*')
            else:
                r = fnmatch.translate(f)

            rc = re.compile(r, flags=re.IGNORECASE)
            res.append(rc)

        if args.search_description:
            def match(p, f):
                if f.match(p):
                    return True

                pkg = spack.repo.get(p)
                if pkg.__doc__:
                    return f.match(pkg.__doc__)
                return False
        else:
            def match(p, f):
                return f.match(p)
        pkgs = [p for p in pkgs if any(match(p, f) for f in res)]

    return sorted(pkgs, key=lambda s: s.lower())


@formatter
def name_only(pkgs, out):
    indent = 0
    if out.isatty():
        tty.msg("%d packages." % len(pkgs))
    colify(pkgs, indent=indent, output=out)


def github_url(pkg):
    """Link to a package file on github."""
    url = 'https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/{0}/package.py'
    return url.format(pkg.name)


def rst_table(elts):
    """Print out a RST-style table."""
    cols = StringIO()
    ncol, widths = colify(elts, output=cols, tty=True)
    header = ' '.join('=' * (w - 1) for w in widths)
    return '%s\n%s%s' % (header, cols.getvalue(), header)


def rows_for_ncols(elts, ncols):
    """Print out rows in a table with ncols of elts laid out vertically."""
    clen = int(math.ceil(len(elts) / ncols))
    for r in range(clen):
        row = []
        for c in range(ncols):
            i = c * clen + r
            row.append(elts[i] if i < len(elts) else None)
        yield row


@formatter
def rst(pkg_names, out):
    """Print out information on all packages in restructured text."""

    pkgs = [spack.repo.get(name) for name in pkg_names]

    out.write('.. _package-list:\n')
    out.write('\n')
    out.write('============\n')
    out.write('Package List\n')
    out.write('============\n')
    out.write('\n')
    out.write('This is a list of things you can install using Spack.  It is\n')
    out.write(
        'automatically generated based on the packages in the latest Spack\n')
    out.write('release.\n')
    out.write('\n')
    out.write('Spack currently has %d mainline packages:\n' % len(pkgs))
    out.write('\n')
    out.write(rst_table('`%s`_' % p for p in pkg_names))
    out.write('\n')
    out.write('\n')

    # Output some text for each package.
    for pkg in pkgs:
        out.write('-----\n')
        out.write('\n')
        out.write('.. _%s:\n' % pkg.name)
        out.write('\n')
        # Must be at least 2 long, breaks for single letter packages like R.
        out.write('-' * max(len(pkg.name), 2))
        out.write('\n')
        out.write(pkg.name)
        out.write('\n')
        out.write('-' * max(len(pkg.name), 2))
        out.write('\n\n')
        out.write('Homepage:\n')
        out.write(
            '  * `%s <%s>`__\n' % (cgi.escape(pkg.homepage), pkg.homepage))
        out.write('\n')
        out.write('Spack package:\n')
        out.write('  * `%s/package.py <%s>`__\n' % (pkg.name, github_url(pkg)))
        out.write('\n')
        if pkg.versions:
            out.write('Versions:\n')
            out.write('  ' + ', '.join(str(v) for v in
                                       reversed(sorted(pkg.versions))))
            out.write('\n\n')

        for deptype in spack.dependency.all_deptypes:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                out.write('%s Dependencies\n' % deptype.capitalize())
                out.write('  ' + ', '.join('%s_' % d if d in pkg_names
                                           else d for d in deps))
                out.write('\n\n')

        out.write('Description:\n')
        out.write(pkg.format_doc(indent=2))
        out.write('\n\n')


@formatter
def html(pkg_names, out):
    """Print out information on all packages in Sphinx HTML.

    This is intended to be inlined directly into Sphinx documentation.
    We write HTML instead of RST for speed; generating RST from *all*
    packages causes the Sphinx build to take forever. Including this as
    raw HTML is much faster.
    """

    # Read in all packages
    pkgs = [spack.repo.get(name) for name in pkg_names]

    # Start at 2 because the title of the page from Sphinx is id1.
    span_id = 2

    # HTML header with an increasing id span
    def head(n, span_id, title, anchor=None):
        if anchor is None:
            anchor = title
        out.write(('<span id="id%d"></span>'
                   '<h1>%s<a class="headerlink" href="#%s" '
                   'title="Permalink to this headline">&para;</a>'
                   '</h1>\n') % (span_id, title, anchor))

    # Start with the number of packages, skipping the title and intro
    # blurb, which we maintain in the RST file.
    out.write('<p>\n')
    out.write('Spack currently has %d mainline packages:\n' % len(pkgs))
    out.write('</p>\n')

    # Table of links to all packages
    out.write('<table border="1" class="docutils">\n')
    out.write('<tbody valign="top">\n')
    for i, row in enumerate(rows_for_ncols(pkg_names, 3)):
        out.write('<tr class="row-odd">\n' if i % 2 == 0 else
                  '<tr class="row-even">\n')
        for name in row:
            out.write('<td>\n')
            out.write('<a class="reference internal" href="#%s">%s</a></td>\n'
                      % (name, name))
            out.write('</td>\n')
        out.write('</tr>\n')
    out.write('</tbody>\n')
    out.write('</table>\n')
    out.write('<hr class="docutils"/>\n')

    # Output some text for each package.
    for pkg in pkgs:
        out.write('<div class="section" id="%s">\n' % pkg.name)
        head(2, span_id, pkg.name)
        span_id += 1

        out.write('<dl class="docutils">\n')

        out.write('<dt>Homepage:</dt>\n')
        out.write('<dd><ul class="first last simple">\n')
        out.write(('<li>'
                   '<a class="reference external" href="%s">%s</a>'
                   '</li>\n') % (pkg.homepage, cgi.escape(pkg.homepage)))
        out.write('</ul></dd>\n')

        out.write('<dt>Spack package:</dt>\n')
        out.write('<dd><ul class="first last simple">\n')
        out.write(('<li>'
                   '<a class="reference external" href="%s">%s/package.py</a>'
                   '</li>\n') % (github_url(pkg), pkg.name))
        out.write('</ul></dd>\n')

        if pkg.versions:
            out.write('<dt>Versions:</dt>\n')
            out.write('<dd>\n')
            out.write(', '.join(
                str(v) for v in reversed(sorted(pkg.versions))))
            out.write('\n')
            out.write('</dd>\n')

        for deptype in spack.dependency.all_deptypes:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                out.write('<dt>%s Dependencies:</dt>\n' % deptype.capitalize())
                out.write('<dd>\n')
                out.write(', '.join(
                    d if d not in pkg_names else
                    '<a class="reference internal" href="#%s">%s</a>' % (d, d)
                    for d in deps))
                out.write('\n')
                out.write('</dd>\n')

        out.write('<dt>Description:</dt>\n')
        out.write('<dd>\n')
        out.write(cgi.escape(pkg.format_doc(indent=2)))
        out.write('\n')
        out.write('</dd>\n')
        out.write('</dl>\n')

        out.write('<hr class="docutils"/>\n')
        out.write('</div>\n')


def list(parser, args):
    # retrieve the formatter to use from args
    formatter = formatters[args.format]

    # Retrieve the names of all the packages
    pkgs = set(spack.repo.all_package_names())
    # Filter the set appropriately
    sorted_packages = filter_by_name(pkgs, args)

    # Filter by tags
    if args.tags:
        packages_with_tags = set(
            spack.repo.path.packages_with_tags(*args.tags))
        sorted_packages = set(sorted_packages) & packages_with_tags
        sorted_packages = sorted(sorted_packages)

    if args.update:
        # change output stream if user asked for update
        if os.path.exists(args.update):
            if os.path.getmtime(args.update) > spack.repo.path.last_mtime():
                tty.msg('File is up to date: %s' % args.update)
                return

        tty.msg('Updating file: %s' % args.update)
        with open(args.update, 'w') as f:
            formatter(sorted_packages, f)

    else:
        # Print to stdout
        formatter(sorted_packages, sys.stdout)

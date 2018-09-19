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
import os
import re

import llnl.util.tty as tty
from llnl.util.lang import pretty_date
from llnl.util.filesystem import working_dir
from llnl.util.tty.colify import colify_table

import spack.paths
import spack.repo
from spack.util.executable import which
from spack.cmd import spack_is_git_repo


description = "show contributors to packages"
section = "developer"
level = "long"


def setup_parser(subparser):
    view_group = subparser.add_mutually_exclusive_group()
    view_group.add_argument(
        '-t', '--time', dest='view', action='store_const', const='time',
        default='time', help='sort by last modification date (default)')
    view_group.add_argument(
        '-p', '--percent', dest='view', action='store_const', const='percent',
        help='sort by percent of code')
    view_group.add_argument(
        '-g', '--git', dest='view', action='store_const', const='git',
        help='show git blame output instead of summary')

    subparser.add_argument(
        'package_name', help='name of package to show contributions for, '
        'or path to a file in the spack repo')


def blame(parser, args):
    # make sure this is a git repo
    if not spack_is_git_repo():
        tty.die("This spack is not a git clone. Can't use 'spack blame'")
    git = which('git', required=True)

    # Get name of file to blame
    blame_file = None
    if os.path.isfile(args.package_name):
        path = os.path.realpath(args.package_name)
        if path.startswith(spack.paths.prefix):
            blame_file = path

    if not blame_file:
        pkg = spack.repo.get(args.package_name)
        blame_file = pkg.module.__file__.rstrip('c')  # .pyc -> .py

    # get git blame for the package
    with working_dir(spack.paths.prefix):
        if args.view == 'git':
            git('blame', blame_file)
            return
        else:
            output = git('blame', '--line-porcelain', blame_file, output=str)
            lines = output.split('\n')

    # Histogram authors
    counts = {}
    emails = {}
    last_mod = {}
    total_lines = 0
    for line in lines:
        match = re.match(r'^author (.*)', line)
        if match:
            author = match.group(1)

        match = re.match(r'^author-mail (.*)', line)
        if match:
            email = match.group(1)

        match = re.match(r'^author-time (.*)', line)
        if match:
            mod = int(match.group(1))
            last_mod[author] = max(last_mod.setdefault(author, 0), mod)

        # ignore comments
        if re.match(r'^\t[^#]', line):
            counts[author] = counts.setdefault(author, 0) + 1
            emails.setdefault(author, email)
            total_lines += 1

    if args.view == 'time':
        rows = sorted(
            counts.items(), key=lambda t: last_mod[t[0]], reverse=True)
    else:  # args.view == 'percent'
        rows = sorted(counts.items(), key=lambda t: t[1], reverse=True)

    # Print a nice table with authors and emails
    table = [['LAST_COMMIT', 'LINES', '%', 'AUTHOR', 'EMAIL']]
    for author, nlines in rows:
        table += [[
            pretty_date(last_mod[author]),
            nlines,
            round(nlines / float(total_lines) * 100, 1),
            author,
            emails[author]]]

    table += [[''] * 5]
    table += [[pretty_date(max(last_mod.values())), total_lines, '100.0'] +
              [''] * 3]

    colify_table(table)

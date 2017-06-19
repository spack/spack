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
import sys
import os
import re
import argparse
import pytest
from StringIO import StringIO

from llnl.util.filesystem import *
from llnl.util.tty.colify import colify

import spack

description = "a thin wrapper around the pytest command"


def setup_parser(subparser):
    subparser.add_argument(
        '-H', '--pytest-help', action='store_true', default=False,
        help="print full pytest help message, showing advanced options")

    list_group = subparser.add_mutually_exclusive_group()
    list_group.add_argument(
        '-l', '--list', action='store_true', default=False,
        help="list basic test names")
    list_group.add_argument(
        '-L', '--long-list', action='store_true', default=False,
        help="list the entire hierarchy of tests")
    subparser.add_argument(
        'tests', nargs=argparse.REMAINDER,
        help="list of tests to run (will be passed to pytest -k)")


def do_list(args, unknown_args):
    """Print a lists of tests than what pytest offers."""
    # Run test collection and get the tree out.
    old_output = sys.stdout
    try:
        sys.stdout = output = StringIO()
        pytest.main(['--collect-only'])
    finally:
        sys.stdout = old_output

    # put the output in a more readable tree format.
    lines = output.getvalue().split('\n')
    output_lines = []
    for line in lines:
        match = re.match(r"(\s*)<([^ ]*) '([^']*)'", line)
        if not match:
            continue
        indent, nodetype, name = match.groups()

        # only print top-level for short list
        if args.list:
            if not indent:
                output_lines.append(
                    os.path.basename(name).replace('.py', ''))
        else:
            print indent + name

    if args.list:
        colify(output_lines)


def test(parser, args, unknown_args):
    if args.pytest_help:
        # make the pytest.main help output more accurate
        sys.argv[0] = 'spack test'
        pytest.main(['-h'])
        return

    # pytest.ini lives in the root of the sapck repository.
    with working_dir(spack.prefix):
        # --list and --long-list print the test output better.
        if args.list or args.long_list:
            do_list(args, unknown_args)
            return

        # Allow keyword search without -k if no options are specified
        if (args.tests and not unknown_args and
            not any(arg.startswith('-') for arg in args.tests)):
            return pytest.main(['-k'] + args.tests)

        # Just run the pytest command
        return pytest.main(unknown_args + args.tests)

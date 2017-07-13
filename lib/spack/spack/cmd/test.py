##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from __future__ import print_function

import sys
import os
import re
import argparse
import pytest
from six import StringIO

from llnl.util.filesystem import *
from llnl.util.tty.colify import colify

import spack

description = "run spack's unit tests"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-H', '--pytest-help', action='store_true', default=False,
        help="print full pytest help message, showing advanced options")
    subparser.add_argument(
        '-c', '--clean-config', action='store_true', dest='clean_config',
        default=False,
        help="backup (to ~/.spack-saved) and remove ~/.spack first") 

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
            print(indent + name)

    if args.list:
        colify(output_lines)

import os
import shutil
import datetime
def test(parser, args, unknown_args):
    if args.pytest_help:
        # make the pytest.main help output more accurate
        sys.argv[0] = 'spack test'
        pytest.main(['-h'])
        return

    #sleak: save ~/.spack from being overwritten:
    sd = os.path.expandvars('$HOME/.spack-saved')
    try:
        os.makedirs(sd)
    except OSError as err:
        if err.errno == 17: # already exists
            pass
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    shutil.move(os.path.expandvars('$HOME/.spack'), sd+'/spack.save.'+now)
    if not args.clean_config:
        shutil.copytree(sd+'/spack.save.'+now, os.path.expandvars('$HOME/.spack'))

    # pytest.ini lives in the root of the sapck repository.
    with working_dir(spack.prefix):
        # --list and --long-list print the test output better.
        if args.list or args.long_list:
            do_list(args, unknown_args)
            errcode = 0

        # Allow keyword search without -k if no options are specified
        if (args.tests and not unknown_args and
            not any(arg.startswith('-') for arg in args.tests)):
            errcode = pytest.main(['-k'] + args.tests)

        # Just run the pytest command
        errcode = pytest.main(unknown_args + args.tests)

    # restore saved config:
    shutil.move(os.path.expandvars('$HOME/.spack'), sd+'/spack.test.'+now)
    shutil.move(sd+'/spack.save.'+now, os.path.expandvars('$HOME/.spack'))
    return errcode

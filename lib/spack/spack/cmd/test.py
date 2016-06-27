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
import os
from pprint import pprint

from llnl.util.filesystem import join_path, mkdirp
from llnl.util.tty.colify import colify
from llnl.util.lang import list_modules

import spack
import spack.test

description ="Run unit tests"

def setup_parser(subparser):
    subparser.add_argument(
        'names', nargs='*', help="Names of tests to run.")
    subparser.add_argument(
        '-l', '--list', action='store_true', dest='list', help="Show available tests")
    subparser.add_argument(
        '--createXmlOutput', action='store_true', dest='createXmlOutput', 
        help="Create JUnit XML from test results")
    subparser.add_argument(
        '--xmlOutputDir', dest='xmlOutputDir', 
        help="Nose creates XML files in this directory")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="verbose output")


def test(parser, args):
    if args.list:
        print "Available tests:"
        colify(spack.test.list_tests(), indent=2)

    else:
        if not args.createXmlOutput:
            outputDir = None
        else:
            if not args.xmlOutputDir:
                outputDir = join_path(os.getcwd(), "test-output")
            else:
                outputDir = os.path.abspath(args.xmlOutputDir)
            
            if not os.path.exists(outputDir):
                mkdirp(outputDir)
        spack.test.run(args.names, outputDir, args.verbose)

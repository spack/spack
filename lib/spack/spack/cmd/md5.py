##############################################################################
# Copyright (c) 2013-2014, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import hashlib
import argparse

import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack.util.crypto

description = "Calculate md5 checksums for files."

def setup_parser(subparser):
    setup_parser.parser = subparser
    subparser.add_argument('files', nargs=argparse.REMAINDER,
                           help="Files to checksum.")

def md5(parser, args):
    if not args.files:
        setup_parser.parser.print_help()
        return 1

    for f in args.files:
        if not os.path.isfile(f):
            tty.die("Not a file: %s" % f)
        if not can_access(f):
            tty.die("Cannot read file: %s" % f)

        checksum = spack.util.crypto.checksum(hashlib.md5, f)
        print "%s  %s" % (checksum, f)

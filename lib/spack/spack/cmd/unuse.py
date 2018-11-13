# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
from spack.cmd.common import print_module_placeholder_help

description = "remove package from environment using dotkit"
section = "modules"
level = "long"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
       message with -h. """
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help='spec of package to unuse with dotkit')


def unuse(parser, args):
    print_module_placeholder_help()

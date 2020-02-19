##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import collections
import sys

import spack
import spack.cmd

description = "filter specs based on their properties"
section = "build"
level = "long"


def setup_parser(subparser):
    install_status = subparser.add_mutually_exclusive_group()
    install_status.add_argument(
        '--installed', dest='installed', default=None, action='store_true',
        help='select installed specs'
    )
    install_status.add_argument(
        '--not-installed', dest='installed', default=None,
        action='store_false',
        help='select specs that are not yet installed'
    )

    explicit_status = subparser.add_mutually_exclusive_group()
    explicit_status.add_argument(
        '--explicit', dest='explicit', default=None, action='store_true',
        help='select specs that were installed explicitly'
    )
    explicit_status.add_argument(
        '--implicit', dest='explicit', default=None,
        action='store_false',
        help='select specs that are not installed or were installed implicitly'
    )

    subparser.add_argument(
        '--output', default=sys.stdout, type=argparse.FileType('w'),
        help='where to dump the result'
    )

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help='specs to be filtered'
    )


def filter(parser, args):
    Request = collections.namedtuple('Request', 'abstract,concrete')

    with spack.store.db.read_transaction():
        specs = [Request(s, s.concretized())
                 for s in spack.cmd.parse_specs(args.specs)]

        # Filter specs eagerly
        if args.installed is True:
            specs = [s for s in specs if s.concrete.package.installed]
        elif args.installed is False:
            specs = [s for s in specs if not s.concrete.package.installed]

        if args.explicit is True:
            specs = [s for s in specs if s.concrete._installed_explicitly()]
        elif args.explicit is False:
            specs = [s for s in specs
                     if not s.concrete._installed_explicitly()]

        for spec in specs:
            args.output.write(str(spec.abstract) + '\n')

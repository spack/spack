# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util import tty

import spack.config

description = "toggle metrics collection"
section = "admin"
level = "long"


def setup_parser(subparser):
    metrics_cmd_group = subparser.add_mutually_exclusive_group()
    metrics_cmd_group.add_argument('metrics_toggle',
                                   nargs='?',
                                   default=None,
                                   help='enable/disable')


def metrics(parser, args):
    if args.metrics_toggle == "enable":
        spack.config.set('config:metrics', 'enable', scope='site')
    elif args.metrics_toggle == "disable":
        spack.config.set('config:metrics', 'disable', scope='site')
    else:
        tty.die("Error: Unrecognized Option: %s" % args.metrics_toggle)

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function
import argparse

import llnl.util.tty as tty

import spack.store
import spack.verify
import spack.environment as ev

description = "Check that all spack packages are on disk as installed"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('-l', '--local', action='store_true',
                           help="Verify only locally installed packages")
    subparser.add_argument('-s', '--strict', action='store_true',
                           help="Raise error for prefixes not owned by user")
    subparser.add_argument('specs', nargs=argparse.REMAINDER,
                           help="Specs to verify (default all)")


def verify(parser, args):
    if args.specs:
        specs = spack.cmd.parse_specs(args.specs)
        env = ev.get_env(args, 'verify')
        specs = list(map(lambda x: spack.cmd.disambiguate_spec(x, env), specs))
    else:
        if args.local:
            specs = spack.store.db.query_local(installed=True)
        else:
            specs = spack.store.db.query(installed=True)

    for spec in specs:
        tty.debug("Verifying package %s")
        results = spack.verify.check(spec)
        if results:
            tty.msg("In package %s" % spec.format('{name}/{hash:7}'))
            print(results)
        else:
            tty.debug(results)

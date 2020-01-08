# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os
import argparse
import textwrap

import llnl.util.tty as tty

import spack.environment as ev
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.report

description = "run spack's tests for an install"
section = "administrator"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--log-format',
        default=None,
        choices=spack.report.valid_formats,
        help="format to be used for log files"
    )
    subparser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )
    arguments.add_cdash_args(subparser, False)
    subparser.add_argument(
        '--help-cdash',
        action='store_true',
        help="Show usage instructions for CDash reporting"
    )

    length_group = subparser.add_mutually_exclusive_group()
    length_group.add_argument(
        '--smoke', action='store_true', dest='smoke_test', default=True,
        help='run smoke tests (default)')
    length_group.add_argument(
        '--capability', action='store_false', dest='smoke_test', default=True,
        help='run full capability tests using pavilion')

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help="list of specs to test")


def test(parser, args):
    # cdash help option
    if args.help_cdash:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''\
environment variables:
  SPACK_CDASH_AUTH_TOKEN
                        authentication token to present to CDash
                        '''))
        arguments.add_cdash_args(parser, True)
        parser.print_help()
        return

    # Get specs to test
    env = ev.get_env(args, 'test')
    hashes = env.all_hashes() if env else None

    specs = spack.cmd.parse_specs(args.specs) if args.specs else [None]
    specs_to_test = []
    for spec in specs:
        matching = spack.store.db.query_local(spec, hashes=hashes)
        if spec and not matching:
            tty.warn("No installed packages match spec %s" % spec)
        specs_to_test.extend(matching)

    # Set up reporter
    setattr(args, 'package', [s.format() for s in specs_to_test])
    reporter = spack.report.collect_info(args.log_format, args)
    if not reporter.filename:
        if args.log_file:
            if os.path.isabs(args.log_file):
                log_file = args.log_file
            else:
                log_dir = os.getcwd()
                log_file = os.path.join(log_dir, args.log_file)
        else:
            log_file = os.path.join(os.getcwd(),
                                    'test-%s' % specs_to_test[0].dag_hash())
        reporter.filename = log_file
    reporter.specs = specs_to_test

    with reporter:
        if args.smoke_test:
            for spec in specs_to_test:
                spec.package.do_test()
        else:
            raise NotImplementedError

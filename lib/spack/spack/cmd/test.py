# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os
import argparse

import llnl.util.tty as tty

import spack.environment as ev
import spack.cmd

description = "run spack's tests for an install"
section = "administrator"
level = "long"


def setup_parser(subparser):
#     subparser.add_argument(
#         '--log-format',
#         default=None,
#         choices=spack.report.valid_formats,
#         help="format to be used for log files"
#     )
#     subparser.add_argument(
#         '--output-file',
#         default=None,
#         help="filename for the log file. if not passed a default will be used"
#     )
#     subparser.add_argument(
#         '--cdash-upload-url',
#         default=None,
#         help="CDash URL where reports will be uploaded"
#     )
#     subparser.add_argument(
#         '--cdash-build',
#         default=None,
#         help="""The name of the build that will be reported to CDash.
# Defaults to spec of the package to install."""
#     )
#     subparser.add_argument(
#         '--cdash-site',
#         default=None,
#         help="""The site name that will be reported to CDash.
# Defaults to current system hostname."""
#     )
#     cdash_subgroup = subparser.add_mutually_exclusive_group()
#     cdash_subgroup.add_argument(
#         '--cdash-track',
#         default='Experimental',
#         help="""Results will be reported to this group on CDash.
# Defaults to Experimental."""
#     )
#     cdash_subgroup.add_argument(
#         '--cdash-buildstamp',
#         default=None,
#         help="""Instead of letting the CDash reporter prepare the
# buildstamp which, when combined with build name, site and project,
# uniquely identifies the build, provide this argument to identify
# the build yourself.  Format: %%Y%%m%%d-%%H%%M-[cdash-track]"""
#     )
#     arguments.add_common_arguments(subparser, ['yes_to_all'])
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
    env = ev.get_env(args, 'test')
    hashes = env.all_hashes() if env else None

    specs = spack.cmd.parse_specs(args.specs) if args.specs else [None]
    specs_to_test = []
    for spec in specs:
        matching = spack.store.db.query_local(spec, hashes=hashes)
        if spec and not matching:
            tty.warn("No installed packages match spec %s" % spec)
        specs_to_test.extend(matching)

    log_dir = os.getcwd()

    if args.smoke_test:
        for spec in specs_to_test:
            log_file = os.path.join(log_dir, 'test-%s' % spec.dag_hash())
            spec.package.do_test(log_file)
    else:
        raise NotImplementedError

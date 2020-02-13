# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import sys

from llnl.util.tty.colify import colify
import llnl.util.tty as tty

import spack.cmd.common.arguments as arguments
import spack.repo

description = "list available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('-s', '--safe-only', action='store_true',
                           help='only list safe versions of the package')
    arguments.add_common_arguments(subparser, ['package'])


def versions(parser, args):
    pkg = spack.repo.get(args.package)

    if sys.stdout.isatty():
        tty.msg('Safe versions (already checksummed):')

    safe_versions = pkg.versions

    if not safe_versions:
        if sys.stdout.isatty():
            tty.warn('Found no versions for {0}'.format(pkg.name))
            tty.debug('Manually add versions to the package.')
    else:
        colify(sorted(safe_versions, reverse=True), indent=2)

    if args.safe_only:
        return

    if sys.stdout.isatty():
        tty.msg('Remote versions (not yet checksummed):')

    fetched_versions = pkg.fetch_remote_versions()
    remote_versions = set(fetched_versions).difference(safe_versions)

    if not remote_versions:
        if sys.stdout.isatty():
            if not fetched_versions:
                tty.warn('Found no versions for {0}'.format(pkg.name))
                tty.debug('Check the list_url and list_depth attributes of '
                          'the package to help Spack find versions.')
            else:
                tty.warn('Found no unchecksummed versions for {0}'.format(
                    pkg.name))
    else:
        colify(sorted(remote_versions, reverse=True), indent=2)
